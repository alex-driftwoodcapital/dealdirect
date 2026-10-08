#!/usr/bin/env python3
"""Deploy a built page to STAGING over SSH + WP-CLI. Run from the repo root on the Mac.
  python3 ops/page/deploy.py eb5             dry run: what would be imported, added, updated, written
  RUN_YES=1 python3 ops/page/deploy.py eb5   do it
Steps: build (copy gate) -> media: reuse by filename or import (local files uploaded, live URLs fetched by the host)
-> style records upserted by selector (backup of etch_styles first) -> placeholders resolved -> page written by
etch-page-editor/scripts/edit-run.sh (snapshot, lint, write, purge, diff; a new page is created as a DRAFT)
-> sha recorded in post meta. An existing page that changed since our last deploy (builder save, manual edit) STOPS."""
import json, os, re, shlex, subprocess, sys, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path[:0] = [os.path.join(ROOT, 'site', 'lib')]
import etch

PAGE = sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)
WRITE = os.environ.get('RUN_YES') == '1'
EDITOR = os.path.join(ROOT, '.claude', 'skills', 'etch-page-editor', 'scripts')
PROFILE = os.environ.get('ETCH_PROFILE', os.path.join(ROOT, '.claude', 'skills', 'etch-page-editor', 'profiles', 'dealdirect-staging.env'))
env_dump = subprocess.run(['bash', '-c', f'set -a; . {shlex.quote(PROFILE)}; echo "$SITE_NAME"; echo "$SSH_CMD"; echo "$WP_PATH"; echo "$PURGE_CMD"'],
                          capture_output=True, text=True, check=True).stdout.splitlines()
SITE, SSH, WP, PURGE = env_dump[:4]
if 'STAGING' not in SITE:
    sys.exit(f'REFUSED: staging profile only ({SITE})')


def remote(cmd, stdin=None, check=True):
    r = subprocess.run(['bash', '-c', f'{SSH} {shlex.quote("cd " + WP + " && " + cmd)}'], input=stdin, capture_output=True)
    if check and r.returncode:
        sys.exit(f'remote failed ({cmd[:80]}): {r.stderr.decode()[-400:]}')
    return r.stdout.decode()


def upload(local_bytes, path):
    remote(f'cat > {shlex.quote(path)}', stdin=local_bytes)


def helper(action, payload, mode):
    upload(json.dumps(payload).encode(), f'{TMP}/in.json')
    out = remote(f'wp eval-file {TMP}/remote.php {action} {TMP}/in.json {mode}').strip().splitlines()
    return json.loads(out[-1])


def step(msg):
    print(f'== {msg}', flush=True)


step(f'{SITE} · {PAGE} · {"WRITE" if WRITE else "dry run"}')
if subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'site', 'build.py'), PAGE]).returncode:
    sys.exit('build failed')
B = os.path.join(ROOT, 'build', PAGE)
records = json.load(open(f'{B}/records.json'))
media = json.load(open(f'{B}/media.json'))
meta = json.load(open(f'{B}/meta.json'))
mode = 'write' if WRITE else 'dry'

TMP = f'/tmp/dd-page-{os.getpid()}'
remote(f'mkdir -p {TMP}')
upload(open(os.path.join(ROOT, 'ops', 'page', 'remote.php'), 'rb').read(), f'{TMP}/remote.php')
try:
    step('media')
    sources = {}
    for slug, src in media.items():
        if src.startswith('http'):
            sources[slug] = src
        else:  # local handoff file: upload to the host's tmp dir under its real filename
            path = f'{TMP}/{os.path.basename(src)}'
            if WRITE:
                upload(open(os.path.join(ROOT, src), 'rb').read(), path)
            sources[slug] = path
    got = helper('media', sources, mode)
    for slug, r in got.items():
        print(f'  {slug:36} {r["status"]}' + (f' (#{r["id"]})' if r['id'] else ''))
    errors = [s for s, r in got.items() if str(r['status']).startswith('ERROR')]
    if errors:
        sys.exit(f'STOP: media failed: {errors}')

    step('style records')
    if WRITE:
        stamp = time.strftime('%Y%m%d-%H%M%S')
        remote(f'mkdir -p ~/backups && wp option get etch_styles --format=json > ~/backups/etch_styles-pre-{PAGE}-{stamp}.json')
        print(f'  backup: ~/backups/etch_styles-pre-{PAGE}-{stamp}.json')
    st = helper('styles', records, mode)
    counts = {}
    for sel, r in st['records'].items():
        counts[r['status']] = counts.get(r['status'], 0) + 1
        if r['status'] != 'same':
            print(f'  {sel:40} {r["status"]}')
    print(f'  {counts}; written: {st["written"]}')

    step('page')
    pg = helper('page', {'slug': meta['slug']}, 'dry')
    if not WRITE:
        if pg['id']:
            print(f'  would update page #{pg["id"]} ({pg["status"]}) /{meta["slug"]}/')
        else:
            print(f'  would create DRAFT page "{meta["title"]}" /{meta["slug"]}/')
        missing_media = [s for s, r in got.items() if not r['id']]
        print(f'  placeholders resolve after media import ({len(missing_media)} pending) and style upsert')
        print('dry run OK (set RUN_YES=1 to write)')
        sys.exit(0)

    sel2id = {sel: r['id'] for sel, r in st['records'].items()}
    content = etch.resolve(open(f'{B}/content.tpl.html').read(), sel2id, {s: r['id'] for s, r in got.items()})
    final = f'{B}/content.html'
    open(final, 'w').write(content)
    run_env = {**os.environ, 'RUN_YES': '1', 'ETCH_PROFILE': PROFILE}

    def live_sha(pid):
        snap = subprocess.run([f'{EDITOR}/snapshot.sh', str(pid)], capture_output=True, text=True, env=run_env, check=True).stdout.strip().splitlines()[-1]
        return [l.split('\t')[3].strip() for l in open(f'{snap}/manifest.tsv') if l.startswith(f'post\t{pid}\t')][0]

    if pg['id']:
        sha = live_sha(pg['id'])
        if pg['deployed_sha'] and sha != pg['deployed_sha']:
            sys.exit(f'STOP: page #{pg["id"]} changed since the last deploy (live {sha}, deployed {pg["deployed_sha"]}). '
                     'Someone saved it in the builder or edited it: re-read and merge before overwriting.')
        args = [f'{EDITOR}/edit-run.sh', str(pg['id']), final, '--expect-sha', sha]
    else:
        args = [f'{EDITOR}/edit-run.sh', '--new', meta['title'], meta['slug'], final]
    r = subprocess.run(args, capture_output=True, text=True, env=run_env)
    print(r.stdout[-2500:], r.stderr[-800:], sep='')
    if r.returncode:
        sys.exit(f'STOP: edit-run.sh exited {r.returncode}')
    pid = int(re.findall(r'post id: (\d+)', r.stdout)[-1])
    helper('mark', {'id': pid, 'sha': live_sha(pid)}, 'write')
    print(f'done: page #{pid} /{meta["slug"]}/ (draft until published on Alex\'s word)')
finally:
    remote(f'rm -rf {TMP}', check=False)
