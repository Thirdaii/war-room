from pathlib import Path
import sys
root=Path(sys.argv[1]); p=root/'index.html'; h=p.read_text(encoding='utf-8')
MARK='War Room v1.7.28 - Live guild roster v25 current source'
if MARK in h:
    print('V25 current live roster frontend already installed'); raise SystemExit(0)

# Normalize ClassicArmory's current API shape: class_name/race_name/numeric rank.
old="const norm=v=>String(v??'').trim(), key=v=>norm(v).toLocaleLowerCase();"
new="const norm=v=>String(v??'').trim(), key=v=>norm(v).toLocaleLowerCase(), rankLabel=raw=>{const rn=norm(raw?.rank_name||raw?.rankName);if(rn)return rn;const rv=raw?.rank;if(rv!==undefined&&rv!==null&&String(rv).trim()!==''){const n=Number(rv);if(Number.isFinite(n))return n===0?'Guild Master':n===1?'Officer':'Rank '+n;return norm(rv)}return 'Member'};"
if old in h: h=h.replace(old,new,1)
elif new not in h: raise RuntimeError('V25 normalizer helper anchor missing')

oldp="class:norm(raw?.class||raw?.className||old.class),race:norm(raw?.race||raw?.raceName||old.race),rank:norm(raw?.rank||raw?.rankName||old.rank||'Member')"
newp="class:norm(raw?.class||raw?.className||raw?.class_name||old.class),race:norm(raw?.race||raw?.raceName||raw?.race_name||old.race),rank:rankLabel(raw)||norm(old.rank||'Member')"
if oldp in h: h=h.replace(oldp,newp,1)
elif newp not in h: raise RuntimeError('V25 member normalizer anchor missing')

oldsync="const count=applyMembers(data.members||[],data,true);lastSuccess=Date.now();\n        const src=norm(data.source||'Live armory');const when=data.fetchedAt?new Date(data.fetchedAt):new Date();const stamp=isNaN(when)?'now':when.toLocaleTimeString([],{hour:'numeric',minute:'2-digit'});\n        status('LIVE • '+count+' level 70 • '+src+' • '+stamp,'live');"
newsync="const members=data.members||data.roster||[];const src=norm(data.source||res.headers.get('X-WarRoom-Roster-Source')||(data.roster?'ClassicArmory.org':'Live armory'));const sourceStamp=data.fetchedAt||data.guild?.updated_at||data.guild?.updatedAt||null;const meta={...data,source:src,fetchedAt:sourceStamp||new Date().toISOString()};const count=applyMembers(members,meta,true);lastSuccess=Date.now();\n        const when=sourceStamp?new Date(sourceStamp):new Date();const ageMs=isNaN(when)?0:(Date.now()-when.getTime());const degraded=/EpicForge/i.test(src);const stale=!degraded&&ageMs>36*60*60*1000;const label=degraded?'SNAPSHOT':stale?'SOURCE STALE':'LIVE';const stamp=isNaN(when)?'now':when.toLocaleString([],{month:'short',day:'numeric',hour:'numeric',minute:'2-digit'});\n        status(label+' • '+count+' level 70 • '+src+' • '+stamp,label==='LIVE'?'live':'cached');"
if oldsync in h: h=h.replace(oldsync,newsync,1)
elif newsync not in h: raise RuntimeError('V25 sync payload anchor missing')

marker='''\n<script id="wr-live-roster-v25-marker">/* War Room v1.7.28 - Live guild roster v25 current source */console.info('[War Room v1.7.28] V25 current ClassicArmory guild API normalizer active');</script>\n'''
if '</body>' not in h: raise RuntimeError('V25 body anchor missing')
h=h.replace('</body>',marker+'</body>',1);p.write_text(h,encoding='utf-8')
print('War Room v1.7.28 V25 current live roster frontend installed')
