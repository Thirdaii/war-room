from pathlib import Path
import sys
root=Path(sys.argv[1]); index=root/'index.html'; h=index.read_text(encoding='utf-8')
MARK='War Room v1.7.28 - Live guild roster v21'
if MARK in h:
    print('V21 live roster already installed'); raise SystemExit(0)
# Remove screenshot-era wording without removing the embedded fallback snapshot itself.
replacements={
    'SCREENSHOT-VERIFIED ROSTER':'LIVE GUILD ROSTER',
    'Verified from in-game screenshots':'<span id="wrLiveRosterStatus">Connecting to live guild source…</span>',
    'Roster verified • raid planner armed • party intelligence active':'Roster sync armed • raid planner armed • party intelligence active',
    'Roster derived from provided in-game screenshots':'Live guild roster sync • cached fallback when upstream is unavailable',
    '<b>Roster:</b> Screenshot-verified level 70 roster loaded.':'<b>Roster:</b> Live level 70 guild roster sync enabled.'
}
for old,new in replacements.items():
    if old in h: h=h.replace(old,new)
# Keep saved raid assignments visible even when a member has just left the live guild roster.
old="const i=g*5+s,n=raid[i],p=roster.find(x=>x.name===n);"
new="const i=g*5+s,n=raid[i],p=roster.find(x=>x.name===n)||(window.WarRoomLiveRosterV21?.legacyPlayer?.(n)||null);"
if old not in h: raise RuntimeError('V21 renderRaid player lookup anchor missing')
h=h.replace(old,new,1)
block=r'''
<style id="wr-live-roster-v21-style">
/* War Room v1.7.28 - Live guild roster v21 */
#wrLiveRosterStatus{display:inline-flex;align-items:center;gap:6px;color:#d4b47a;font-weight:800}
#wrLiveRosterStatus:before{content:'';width:7px;height:7px;border-radius:50%;background:#d69d48;box-shadow:0 0 7px rgba(214,157,72,.42)}
#wrLiveRosterStatus[data-state="live"]{color:#8ed49d}
#wrLiveRosterStatus[data-state="live"]:before{background:#65c37d;box-shadow:0 0 8px rgba(101,195,125,.5)}
#wrLiveRosterStatus[data-state="cached"]{color:#e0b866}
#wrLiveRosterStatus[data-state="error"]{color:#d98272}
#wrRefreshLiveRoster{white-space:nowrap;min-width:96px}
#wrRefreshLiveRoster.wr-syncing{opacity:.65;pointer-events:none}
</style>
<script id="wr-live-roster-v21-script">
/* War Room v1.7.28 - Live guild roster v21 */
(function(){
  if(window.__wrLiveRosterV21)return;window.__wrLiveRosterV21=true;
  const CACHE='wr_live_guild_roster_v21',REFRESH_MS=5*60*1000,FOCUS_REFRESH_MS=2*60*1000;
  const legacy=new Map((Array.isArray(roster)?roster:[]).map(p=>[String(p?.name||'').toLocaleLowerCase(),{...p}]));
  let lastSuccess=0,inFlight=null;
  const norm=v=>String(v??'').trim(), key=v=>norm(v).toLocaleLowerCase();
  function status(text,state='cached'){
    const el=document.getElementById('wrLiveRosterStatus');if(!el)return;el.textContent=text;el.dataset.state=state;
  }
  function rebuildFilters(){
    const cf=document.getElementById('classFilter'),rf=document.getElementById('rankFilter');
    if(cf){const keep=cf.value;cf.innerHTML='<option value="">All classes</option>';[...new Set(roster.map(x=>x.class).filter(Boolean))].sort().forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;cf.append(o)});if([...cf.options].some(o=>o.value===keep))cf.value=keep}
    if(rf){const keep=rf.value;rf.innerHTML='<option value="">All ranks</option>';[...new Set(roster.map(x=>x.rank).filter(Boolean))].forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;rf.append(o)});if([...rf.options].some(o=>o.value===keep))rf.value=keep}
  }
  function refreshCounters(){
    const total=document.getElementById('totalN'),classes=document.getElementById('classN'),leaders=document.getElementById('leaderN');
    if(total)total.textContent=roster.length;
    if(classes)classes.textContent=new Set(roster.map(x=>x.class).filter(Boolean)).size;
    if(leaders)leaders.textContent=roster.filter(x=>/guild master|officer|veteran/i.test(x.rank||'')).length;
  }
  function applyMembers(input,meta={},persist=true){
    const rows=[],seen=new Set();
    for(const raw of (Array.isArray(input)?input:[])){
      const name=norm(raw?.name),level=Number(raw?.level||0);if(!name||level!==70||seen.has(key(name)))continue;seen.add(key(name));
      const old=legacy.get(key(name))||roster.find(p=>key(p?.name)===key(name))||{};
      const p={...old,...raw,name,level:70,class:norm(raw?.class||raw?.className||old.class),race:norm(raw?.race||raw?.raceName||old.race),rank:norm(raw?.rank||raw?.rankName||old.rank||'Member')};
      if((p.gearscore===undefined||p.gearscore===null||p.gearscore==='')&&old.gearscore!=null)p.gearscore=old.gearscore;
      try{if(!p.role&&typeof inferRole==='function')p.role=inferRole(p)}catch(_){ }
      rows.push(p);
    }
    if(rows.length<10)throw new Error('Live roster returned too few level 70 members ('+rows.length+')');
    rows.sort((a,b)=>String(a.rank||'').localeCompare(String(b.rank||''))||String(a.name).localeCompare(String(b.name)));
    roster.splice(0,roster.length,...rows);
    rebuildFilters();refreshCounters();
    try{if(typeof renderClassStrip==='function')renderClassStrip()}catch(_){ }
    try{if(typeof renderRoster==='function')renderRoster()}catch(_){ }
    try{if(typeof renderRaid==='function')renderRaid()}catch(_){ }
    try{if(typeof renderOverview==='function')renderOverview()}catch(_){ }
    try{window.WarRoomGroupDragV17?.disableNative?.()}catch(_){ }
    if(persist){try{localStorage.setItem(CACHE,JSON.stringify({members:rows.map(({gear,equipment,items,talentsData,...p})=>p),source:meta.source||'',fetchedAt:meta.fetchedAt||new Date().toISOString(),savedAt:Date.now()}))}catch(_){ }}
    return rows.length;
  }
  function loadCache(){
    try{const c=JSON.parse(localStorage.getItem(CACHE)||'null');if(!c||!Array.isArray(c.members)||c.members.length<10)return false;const n=applyMembers(c.members,c,false);status('Cached live roster • refreshing…','cached');return n>0}catch(_){return false}
  }
  function ensureButton(){
    if(document.getElementById('wrRefreshLiveRoster'))return;
    const host=document.querySelector('#rosterPanel .controls');if(!host)return;
    const b=document.createElement('button');b.id='wrRefreshLiveRoster';b.type='button';b.className='quick';b.textContent='↻ Live Sync';b.title='Refresh the guild roster from the live armory source';b.addEventListener('click',()=>sync(true));host.appendChild(b);
  }
  async function sync(force=false){
    if(inFlight&&!force)return inFlight;
    const btn=document.getElementById('wrRefreshLiveRoster');if(btn){btn.classList.add('wr-syncing');btn.textContent='↻ Syncing…'}
    status('Syncing live guild roster…','cached');
    const task=(async()=>{
      const ctl=new AbortController(),timer=setTimeout(()=>ctl.abort(),12000);
      try{
        const res=await fetch('/guild-roster'+(force?'?refresh=1':''),{cache:'no-store',signal:ctl.signal,headers:{Accept:'application/json'}});
        let data=null;try{data=await res.json()}catch(_){throw new Error('Roster proxy returned malformed JSON')}
        if(!res.ok)throw new Error(data?.error||('HTTP '+res.status));
        const count=applyMembers(data.members||[],data,true);lastSuccess=Date.now();
        const src=norm(data.source||'Live armory');const when=data.fetchedAt?new Date(data.fetchedAt):new Date();const stamp=isNaN(when)?'now':when.toLocaleTimeString([],{hour:'numeric',minute:'2-digit'});
        status('LIVE • '+count+' level 70 • '+src+' • '+stamp,'live');
        return data;
      }finally{clearTimeout(timer)}
    })();
    inFlight=task;
    try{return await task}catch(e){const hasCache=(()=>{try{return !!localStorage.getItem(CACHE)}catch(_){return false}})();status(hasCache?'Live refresh failed • cached roster kept':'Live sync unavailable • fallback snapshot kept','error');console.warn('[War Room] live roster sync failed',e);return null}
    finally{inFlight=null;if(btn){btn.classList.remove('wr-syncing');btn.textContent='↻ Live Sync'}}
  }
  ensureButton();const hadCache=loadCache();setTimeout(()=>sync(false),hadCache?180:60);
  setInterval(()=>sync(false),REFRESH_MS);
  document.addEventListener('visibilitychange',()=>{if(!document.hidden&&Date.now()-lastSuccess>FOCUS_REFRESH_MS)sync(false)});
  window.addEventListener('focus',()=>{if(Date.now()-lastSuccess>FOCUS_REFRESH_MS)sync(false)});
  window.WarRoomLiveRosterV21={sync,applyMembers,legacyPlayer:n=>legacy.get(key(n))||null,get lastSuccess(){return lastSuccess}};
  console.info('[War Room v1.7.28] live guild roster v21 active');
})();
</script>
'''
if '</body>' not in h: raise RuntimeError('body close marker missing')
h=h.replace('</body>',block+'\n</body>',1);index.write_text(h,encoding='utf-8');print('War Room v1.7.28 live guild roster v21 installed')
