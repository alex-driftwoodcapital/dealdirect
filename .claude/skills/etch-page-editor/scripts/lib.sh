# shared helpers; sourced by snapshot.sh / diff.sh / restore.sh
set -euo pipefail
PROFILE="${ETCH_PROFILE:-$(dirname "$0")/../profiles/dealdirect-staging.env}"
[ -f "$PROFILE" ] || { echo "profile not found: $PROFILE" >&2; exit 2; }
# shellcheck disable=SC1090
. "$PROFILE"
# cloud sessions: materialise the key from the ETCH_SSH_KEY secret on first use
[ -s "$SSH_KEY_FILE" ] || [ -z "${ETCH_SSH_KEY:-}" ] || "$(dirname "$0")/ssh-setup.sh" >&2
# run a command on the host inside the WP path
remote() { eval "$SSH_CMD" "'cd $WP_PATH && $*'" </dev/null; }
# normalize block markup: drop whitespace between block comments, so builder reformatting is not a "change"
norm() { python3 -c 'import re,sys;print(re.sub(r"(-->)\s+(<!--)",r"\1\2",sys.stdin.read().strip()))'; }
