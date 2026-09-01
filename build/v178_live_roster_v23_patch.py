from pathlib import Path
import sys
root=Path(sys.argv[1]); p=root/'index.html'; h=p.read_text(encoding='utf-8')
MARK='War Room v1.7.28 - Live guild roster v23 diagnostics'
if MARK in h: raise SystemExit(0)
# V21/V22 preserve the useful proxy detail in the thrown Error, but the V21 catch
# collapses it to a generic red status line. V23 keeps the old message and appends
# the actual exception so the next Windows test tells us exactly where the chain failed.
old="status(hasCache?'Live refresh failed • cached roster kept':'Live sync unavailable • fallback snapshot kept','error');console.warn"
new="status((hasCache?'Live refresh failed • cached roster kept':'Live sync unavailable • fallback snapshot kept')+' • '+String(e?.message||e||'unknown error'),'error');console.warn"
if old in h:
    h=h.replace(old,new,1)
elif new not in h:
    raise RuntimeError('V23 visible roster catch anchor missing')
marker='''\n<script id="wr-live-roster-v23-marker">/* War Room v1.7.28 - Live guild roster v23 diagnostics */</script>\n'''
if '</body>' not in h: raise RuntimeError('V23 body anchor missing')
h=h.replace('</body>',marker+'</body>',1); p.write_text(h,encoding='utf-8')
print('V23 visible live-roster diagnostics installed')
