from pathlib import Path
import sys

root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')
MARK='War Room v1.7.28 - Live guild roster v22 deadline hotfix'
if MARK in h:
    print('V22 live roster deadline hotfix already installed')
    raise SystemExit(0)

old="const ctl=new AbortController(),timer=setTimeout(()=>ctl.abort(),12000);"
new="const ctl=new AbortController(),timer=setTimeout(()=>ctl.abort(),30000);"
if old in h:
    h=h.replace(old,new,1)
elif new not in h:
    raise RuntimeError('V22 live roster AbortController deadline anchor missing')

# Make an upstream/proxy failure visible in the console instead of throwing away
# the launcher's useful detail string. The UI remains compact, but diagnostics
# now tell us exactly which source failed if this ever regresses.
old_error="if(!res.ok)throw new Error(data?.error||('HTTP '+res.status));"
new_error="if(!res.ok)throw new Error((data?.error||('HTTP '+res.status))+(data?.detail?' — '+data.detail:''));"
if old_error in h:
    h=h.replace(old_error,new_error,1)
elif new_error not in h:
    raise RuntimeError('V22 live roster proxy error anchor missing')

marker='''\n<script id="wr-live-roster-v22-marker">\n/* War Room v1.7.28 - Live guild roster v22 deadline hotfix */\nconsole.info('[War Room v1.7.28] live guild roster v22: 30s proxy deadline active');\n</script>\n'''
if '</body>' not in h:
    raise RuntimeError('V22 body close marker missing')
h=h.replace('</body>',marker+'\n</body>',1)
index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 live guild roster v22 frontend hotfix installed')
