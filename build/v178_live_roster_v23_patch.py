from pathlib import Path
import sys
root=Path(sys.argv[1]); p=root/'index.html'; h=p.read_text(encoding='utf-8')
MARK='War Room v1.7.28 - Live guild roster v23 diagnostics'
if MARK in h: raise SystemExit(0)
# V21 deliberately hid the useful error detail from the visible status. V23 puts it on-screen.
old="setStatus('error','Live sync unavailable • fallback snapshot kept');"
new="setStatus('error','Live sync unavailable • '+String(err?.message||err||'unknown error'))"
if old in h: h=h.replace(old,new,1)
elif new not in h: raise RuntimeError('V23 visible roster error anchor missing')
marker='''\n<script id="wr-live-roster-v23-marker">/* War Room v1.7.28 - Live guild roster v23 diagnostics */</script>\n'''
if '</body>' not in h: raise RuntimeError('V23 body anchor missing')
h=h.replace('</body>',marker+'</body>',1); p.write_text(h,encoding='utf-8')
print('V23 visible live-roster diagnostics installed')
