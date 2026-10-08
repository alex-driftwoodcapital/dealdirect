#!/usr/bin/env python3
"""Unsupervised run of a brief: pieces in order, stop on the first problem, write a report.
usage: run-brief.py brief.json [--yes] [--out DIR]     (dry run unless --yes; staging profile only)
brief: {"goal": "...", "done": "...", "pieces":[
   {"name":"A","new":{"title":"..","slug":".."},"content":"a.html"},          # creates a DRAFT page
   {"name":"B","post":123,"content":"b.html","verify":["https://.../b/"]} ]}   # edits an existing page named in the brief
Stop rules (exit 1, later pieces NOT run): lint error, page changed since the baseline read (conflict, e.g. a builder save),
protected/out-of-brief page, unknown piece keys. There is no delete / publish / go-live piece type: those need Alex's typed words."""
import json, os, re, subprocess, sys, time, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser(); ap.add_argument('brief'); ap.add_argument('--yes', action='store_true'); ap.add_argument('--out')
a = ap.parse_args(); brief = json.load(open(a.brief)); base = os.path.dirname(os.path.abspath(a.brief))
PROF = os.environ.get('ETCH_PROFILE', os.path.join(HERE, '..', 'profiles', 'dealdirect-staging.env'))
env0 = dict(os.environ)
if 'staging' not in os.path.basename(PROF).lower() and os.environ.get('ALLOW_NON_STAGING') != '1':
    sys.exit('REFUSED: unsupervised runs use a staging profile only (go-live needs Alex\'s typed words)')
OUT = a.out or os.path.expanduser(f"~/etch-runs/{time.strftime('%Y%m%d-%H%M%S')}"); os.makedirs(OUT, exist_ok=True)
ALLOWED = {'name', 'new', 'post', 'content', 'verify', 'expect'}  # expect: sha from an earlier read (else the baseline read at run start)
def sh(cmd, env=None):
    r = subprocess.run(cmd, capture_output=True, text=True, env={**env0, **(env or {})}); return r.returncode, r.stdout + r.stderr
def baseline(pid):
    r = subprocess.run([f'{HERE}/snapshot.sh', str(pid)], capture_output=True, text=True, env=env0)
    d = r.stdout.strip().splitlines()[-1]
    sha = [l.split('\t')[3].strip() for l in open(d + '/manifest.tsv') if l.startswith(f'post\t{pid}\t')][0]
    return sha
for p in brief['pieces']:
    bad = set(p) - ALLOWED
    if bad: sys.exit(f"REFUSED: piece {p.get('name')} has unsupported keys {sorted(bad)} (out of brief / irreversible actions are not runnable)")
    if ('new' in p) == ('post' in p): sys.exit(f"REFUSED: piece {p.get('name')} needs exactly one of new/post")
# baseline read of every existing page named in the brief, BEFORE any write
sha = {}
for p in brief['pieces']:
    if 'post' in p and p['post'] not in sha: sha[p['post']] = baseline(p['post'])
names = {}  # piece name -> post id created in this run
log = [f"# Run report\nGoal: {brief.get('goal','')}\nDone when: {brief.get('done','')}\nMode: {'WRITE' if a.yes else 'dry run'}  Profile: {PROF}\n"]
stopped = None
for i, p in enumerate(brief['pieces'], 1):
    name = p.get('name', f'piece{i}'); content = os.path.join(base, p['content'])
    env = {'RUN_YES': '1' if a.yes else '0'}
    if 'new' in p:
        cmd = [f'{HERE}/edit-run.sh', '--new', p['new']['title'], p['new']['slug'], content]
    else:
        cmd = [f'{HERE}/edit-run.sh', str(p['post']), content, '--expect-sha', p.get('expect', sha[p['post']])]
    if p.get('verify') and a.yes: cmd += ['--verify'] + p['verify']
    rc, out = sh(cmd, env)
    open(f'{OUT}/{i}-{name}.log', 'w').write(out)
    m = re.search(r'post id: (\d+)', out); snap = re.search(r'snapshot: (\S+)', out)
    status = {0: 'ok', 3: 'REFUSED (protected / out of brief)', 4: 'CONFLICT (page changed since baseline read)', 5: 'LINT ERRORS', 6: 'VERIFY FAILED (page written; roll back or fix)'}.get(rc, f'FAILED rc={rc}')
    log.append(f"## {i}. {name}: {status}\n- snapshot: {snap.group(1) if snap else '-'}\n" + (f"- post id: {m.group(1)}\n- rollback: RESTORE_YES=1 {HERE}/restore.sh {snap.group(1)} post {m.group(1)}\n" if m and snap else '') + f"- log: {OUT}/{i}-{name}.log\n")
    if rc != 0: stopped = f"{name}: {status}"; log.append(f"STOPPED at piece {i}; pieces {i+1}..{len(brief['pieces'])} NOT run. Needs Alex.\n"); break
log.append('RESULT: ' + (f'STOPPED ({stopped})' if stopped else ('COMPLETE' if a.yes else 'DRY RUN OK')))
open(f'{OUT}/report.md', 'w').write('\n'.join(log)); print('\n'.join(log)); sys.exit(1 if stopped else 0)
