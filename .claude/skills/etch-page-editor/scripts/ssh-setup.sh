#!/usr/bin/env bash
# Prepare SSH for unattended runs (cloud sessions or a fresh machine). Idempotent; safe to run every session.
# usage: ssh-setup.sh [--check]     --check also runs a read-only WP-CLI probe on the host.
# Reads (environment secrets, never committed):
#   ETCH_SSH_KEY          private key, raw PEM/OpenSSH text or base64 of it
#   ETCH_SSH_KNOWN_HOSTS  the host's known_hosts line(s) (ssh-keyscan -p PORT HOST, verified once on a trusted machine)
# Host, port, user and WP path come from the profile (ETCH_PROFILE, default profiles/dealdirect-staging.env).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PROFILE="${ETCH_PROFILE:-$HERE/../profiles/dealdirect-staging.env}"
# shellcheck disable=SC1090
. "$PROFILE"
if ! command -v ssh >/dev/null; then
  if [ "$(id -u)" = 0 ] && command -v apt-get >/dev/null; then
    echo "installing openssh-client" >&2
    (apt-get install -y -qq openssh-client >/dev/null 2>&1 || { apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq openssh-client >/dev/null 2>&1; }) \
      || { echo "ssh-setup: could not install openssh-client; add it to the environment setup script" >&2; exit 1; }
  else echo "ssh-setup: ssh not installed" >&2; exit 1; fi
fi
mkdir -p "$HOME/.ssh"; chmod 700 "$HOME/.ssh"
if [ -n "${ETCH_SSH_KEY:-}" ] && [ ! -s "$SSH_KEY_FILE" ]; then
  umask 077
  case "$ETCH_SSH_KEY" in
    *"PRIVATE KEY"*) printf '%s\n' "$ETCH_SSH_KEY" | sed 's/\\n/\n/g' > "$SSH_KEY_FILE" ;;  # secrets UIs sometimes flatten newlines to \n
    *) printf '%s' "$ETCH_SSH_KEY" | base64 -d > "$SSH_KEY_FILE" ;;
  esac
  chmod 600 "$SSH_KEY_FILE"
fi
[ -s "$SSH_KEY_FILE" ] || { echo "ssh-setup: no key at $SSH_KEY_FILE (set the ETCH_SSH_KEY secret)" >&2; exit 1; }
grep -q "PRIVATE KEY" "$SSH_KEY_FILE" || { echo "ssh-setup: $SSH_KEY_FILE is not a private key (the secret must hold the OUTPUT of the copy command, not the command)" >&2; rm -f "$SSH_KEY_FILE"; exit 1; }
if [ -n "${ETCH_SSH_KNOWN_HOSTS:-}" ]; then
  touch "$HOME/.ssh/known_hosts"; chmod 600 "$HOME/.ssh/known_hosts"
  printf '%s\n' "$ETCH_SSH_KNOWN_HOSTS" | sed 's/\\n/\n/g' | while IFS= read -r l; do
    # if/fi, not a && chain: an already-present line must not end the loop with status 1 under set -e
    if [ -n "$l" ] && ! grep -qxF "$l" "$HOME/.ssh/known_hosts"; then printf '%s\n' "$l" >> "$HOME/.ssh/known_hosts"; fi
  done
  grep -q "^\(\[\?${SSH_HOST}\)" "$HOME/.ssh/known_hosts" || { echo "ssh-setup: ETCH_SSH_KNOWN_HOSTS has no line for $SSH_HOST (paste the OUTPUT of ssh-keyscan, not the command)" >&2; exit 1; }
fi
for v in SSH_HOST SSH_USER WP_PATH; do [ "${!v}" != TBD ] || { echo "ssh-setup: $v is TBD in $PROFILE (or set ETCH_$v)" >&2; exit 1; }; done
echo "ssh-setup: ready for $SSH_USER@$SSH_HOST:$SSH_PORT ($SITE_NAME)" >&2
if [ "${1:-}" = --check ]; then
  eval "$SSH_CMD" "'cd $WP_PATH && wp core version && wp plugin list --fields=name,status,version --format=csv | grep -iE \"^(etch|automatic)\" ; wp theme list --status=active --fields=name,version --format=csv'" </dev/null
fi
