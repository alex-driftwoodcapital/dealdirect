#!/usr/bin/env python3
"""Deploy a built page to STAGING over SSH + WP-CLI. Run from the repo root on the Mac.
  python3 ops/page/deploy.py eb5             dry run: what would be imported, added, updated, written
  RUN_YES=1 python3 ops/page/deploy.py eb5   do it
Steps: build (copy gate) -> media: reuse by filename or import (local files uploaded, live URLs fetched by the host)
-> style records upserted by selector (backup of etch_styles first) -> placeholders resolved -> page written by
etch-page-editor/scripts/edit-run.sh (snapshot, lint, write, purge, diff; a new page is created as a draft)
-> sha recorded in post meta -> status set from the page's META (staging pages publish; live is never written). An existing page that changed since our last deploy (builder save, manual edit) STOPS."""
import json, os, re, shlex, subprocess, sys, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path[:0] = [os.path.join(ROOT, 'site', 'lib')]
import etch, svg

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
    for slug, m in media.items():
        src = m['src']
        if not src.startswith('http'):  # local handoff file: upload to the host's tmp dir under its real filename
            path = f'{TMP}/{os.path.basename(src)}'
            if WRITE:
                upload(open(os.path.join(ROOT, src), 'rb').read(), path)
            src = path
        sources[slug] = {'src': src, 'collection': m['collection'], **({'name': m['name']} if m.get('name') else {})}
    got = helper('media', sources, mode) if sources else {}
    got = got or {}  # PHP encodes an empty map as []
    for slug, r in got.items():
        print(f'  {slug:36} {r["status"]}' + (f' (#{r["id"]})' if r['id'] else '') + f'  -> {r.get("collection", "")}')
    errors = [s for s, r in got.items() if str(r['status']).startswith('ERROR')]
    if errors:
        sys.exit(f'STOP: media failed: {errors}')

    step('style records')
    if WRITE:
        stamp = time.strftime('%Y%m%d-%H%M%S')
        remote(f'mkdir -p ~/backups && wp option get etch_styles --format=json > ~/backups/etch_styles-pre-{PAGE}-{stamp}.json')
        print(f'  backup: ~/backups/etch_styles-pre-{PAGE}-{stamp}.json')
    st = helper('styles', records, mode) if records else {'records': {}, 'written': False}
    st['records'] = st['records'] or {}
    counts = {}
    for sel, r in st['records'].items():
        counts[r['status']] = counts.get(r['status'], 0) + 1
        if r['status'] != 'same':
            print(f'  {sel:40} {r["status"]}')
    print(f'  {counts}; written: {st["written"]}')

    KIND = meta.get('kind', 'page')
    PTYPE = {'page': 'page', 'offering': 'offering', 'component': 'wp_block', 'template': 'wp_template'}[KIND]
    want = meta.get('status', 'draft' if KIND in ('page', 'offering') else 'publish')
    step(KIND)
    pg = helper('page', {'slug': meta['slug'], 'post_type': PTYPE}, 'dry')
    template = open(f'{B}/content.tpl.html').read()
    ref_slugs = sorted(set(re.findall(r'\{\{ref:([^}]*)\}\}', template)))
    refs = helper('refs', {'slugs': ref_slugs}, 'dry') if ref_slugs else {}
    if not WRITE:
        if KIND == 'template':
            inv = helper('inventory', {}, 'dry')
            print(f'  staging now (theme {inv["active_theme"]}): ' + ('; '.join(inv['posts']) or 'no templates, parts or components yet'))
            print('  asset storage (Etch Asset Manager): ' + json.dumps(inv.get('asset_storage', {})))
            print('  Etch compressor: ' + json.dumps(inv.get('etch_compressor', {})))
        what = f'{PTYPE} "{meta["title"]}" ({meta["slug"]})'
        if pg['id']:
            print(f'  would update {what} #{pg["id"]} ({pg["status"]})' + (f', then set status {want}' if pg['status'] != want else ''))
        else:
            print(f'  would create {what} as {want}')
        for slug, rid in refs.items():
            print(f'  component {slug}: ' + (f'#{rid}' if rid else 'not on staging yet: created by the component step of this deploy'))
        if svg.MARKER.search(template):  # fetch + sanitize now, so a bad SVG fails the PR check, not the deploy
            n = svg.expand(template).count('"tag":"path"')
            print(f'  inline SVG fetched and converted ({n} paths)')
        print('dry run OK (set RUN_YES=1 to write)')
        sys.exit(0)

    missing_refs = [s for s, rid in refs.items() if not rid]
    if missing_refs:
        sys.exit(f'STOP: components not on staging yet: {missing_refs} (deploy them first; ops/deploy-all.sh orders them)')
    sel2id = {sel: r['id'] for sel, r in st['records'].items()}
    content = etch.resolve(svg.expand(template), sel2id, {s: r['id'] for s, r in got.items()}, refs, {s: r.get('url') for s, r in got.items()})
    final = f'{B}/content.html'
    open(final, 'w').write(content)
    run_env = {**os.environ, 'RUN_YES': '1', 'ETCH_PROFILE': PROFILE}

    def live_sha(pid):
        snap = subprocess.run([f'{EDITOR}/snapshot.sh', str(pid)], capture_output=True, text=True, env=run_env, check=True).stdout.strip().splitlines()[-1]
        return [l.split('\t')[3].strip() for l in open(f'{snap}/manifest.tsv') if l.startswith(f'post\t{pid}\t')][0]

    if not pg['id'] and KIND != 'page':
        # offerings, components and templates are created empty, then filled through the same guarded update path
        pg = {'id': helper('create', {'post_type': PTYPE, 'slug': meta['slug'], 'title': meta['title']}, 'write')['id'], 'deployed_sha': ''}
        print(f'  created {PTYPE} #{pg["id"]} {meta["slug"]}')
    if pg['id']:
        sha = live_sha(pg['id'])
        if pg['deployed_sha'] and sha != pg['deployed_sha']:
            sys.exit(f'STOP: {PTYPE} #{pg["id"]} changed since the last deploy (live {sha}, deployed {pg["deployed_sha"]}). '
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
    st_ = helper('status', {'id': pid, 'status': want}, 'write')
    print(f'done: {PTYPE} #{pid} {meta["slug"]} status {st_["to"]}' + (f' (was {st_["from"]})' if st_['changed'] else ''))
finally:
    remote(f'rm -rf {TMP}', check=False)
