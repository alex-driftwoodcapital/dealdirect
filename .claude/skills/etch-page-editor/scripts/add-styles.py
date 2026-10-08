#!/usr/bin/env python3
"""Add NEW class style records to etch_styles (the step between an ACSS style spec and writing markup).
usage: add-styles.py records.json [--yes]    records.json: {"<7-char id>": {"type":"class","selector":".x","collection":"default","css":"...","readonly":false}}
Refuses ids/selectors that already exist, backs up etch_styles to ~/backups first on the host, dry run unless --yes.
Create style records BEFORE any block references their ids (lint errors on unknown ids). Staging profile only."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
prof = os.environ.get('ETCH_PROFILE', f'{HERE}/../profiles/dealdirect-staging.env')
if 'staging' not in os.path.basename(prof).lower(): sys.exit('REFUSED: staging profile only')
recs = json.load(open(sys.argv[1])); yes = '--yes' in sys.argv
for k, v in recs.items():
    if v.get('type') != 'class' or not str(v.get('selector', '')).startswith('.'): sys.exit(f'{k}: only class records (selector starts with .) are supported')
def sh(c, stdin=None):
    r = subprocess.run(['bash', '-c', f'. {prof}; eval "$SSH_CMD" "\'cd $WP_PATH && {c}\'"'], input=stdin, capture_output=True, text=True); return r.returncode, r.stdout + r.stderr
rc, o = sh('wp option get etch_styles --format=json'); live = json.loads(o)
taken = {v.get('selector') for v in live.values()}
for k, v in recs.items():
    if k in live: sys.exit(f'REFUSED: id {k} exists')
    if v['selector'] in taken: sys.exit(f"REFUSED: selector {v['selector']} already has a record (use it; delete+recreate is the only edit path)")
print(f'{len(recs)} new records OK; live has {len(live)}'); 
if not yes: sys.exit('dry run (use --yes)')
sh('mkdir -p ~/backups && wp option get etch_styles --format=json > ~/backups/etch_styles-pre-add-$(date +%Y%m%d%H%M%S).json')
live.update(recs)
rc, o = sh('cat > /tmp/etch_styles_new.json && wp option update etch_styles --format=json < /tmp/etch_styles_new.json && rm -f /tmp/etch_styles_new.json', json.dumps(live)); print(o.strip())
