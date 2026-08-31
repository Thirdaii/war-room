from pathlib import Path
import sys

root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')
MARK='War Room v1.7.28 - Pointer raid drag/drop v17'
if MARK in h:
    print('V17 pointer drag already installed')
    raise SystemExit(0)

block=r'''
<style id="wr-group-drag-v17-style">
/* War Room v1.7.28 - Pointer raid drag/drop v17 */
#rosterPanel{
  display:flex!important;
  flex-direction:column!important;
  min-height:0!important;
}
#rosterPanel .wr-side-heading{order:0;flex:0 0 auto!important}
#rosterPanel .panel-head{order:1;flex:0 0 auto!important;grid-row:auto!important}
#rosterPanel #wrRaidBenchDrop{order:2;flex:0 0 auto!important}
#rosterPanel .roster{
  order:3;
  flex:1 1 auto!important;
  min-height:0!important;
  max-height:810px!important;
  align-content:start!important;
  align-items:start!important;
  grid-auto-rows:max-content!important;
  overflow:auto!important;
}
#rosterPanel .class-strip{order:4;flex:0 0 auto!important}
#builder .slot[data-slot],#roster .player-card{touch-action:none}
body.wr-pointer-raid-dragging{cursor:grabbing!important;user-select:none!important}
body.wr-pointer-raid-dragging *{cursor:grabbing!important}
.wr-v17-drag-ghost{
  position:fixed;z-index:2147483646;pointer-events:none;display:flex;align-items:center;gap:7px;
  min-width:120px;max-width:240px;padding:7px 10px;border:1px solid #c28a4e;border-radius:4px;
  background:linear-gradient(180deg,rgba(31,20,15,.98),rgba(11,8,7,.98));color:#ead7b1;
  box-shadow:0 12px 32px rgba(0,0,0,.62),inset 0 0 0 1px rgba(255,220,150,.06);
  font:900 10px/1.1 Arial,sans-serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
  transform:translate(14px,14px)
}
#builder .slot.wr-v17-target{
  border-color:#d19a52!important;
  background:linear-gradient(90deg,rgba(117,57,30,.62),rgba(26,17,13,.98))!important;
  box-shadow:inset 0 0 0 1px rgba(238,184,102,.28),0 0 14px rgba(184,104,45,.18)!important
}
#builder .slot.wr-v17-swap:after{
  content:'SWAP';position:absolute;right:30px;top:50%;transform:translateY(-50%);
  color:#f0c57d;font-size:6px;font-weight:1000;letter-spacing:.8px;pointer-events:none
}
#builder .group.wr-v17-group-target{
  outline:1px solid #a96537!important;outline-offset:-2px;
  box-shadow:inset 0 0 28px rgba(177,89,42,.13)!important
}
#wrRaidBenchDrop.wr-v17-roster-target{
  color:#f3ce88!important;border-color:#c08347!important;
  background:linear-gradient(180deg,rgba(102,52,29,.76),rgba(30,18,13,.97))!important;
  box-shadow:inset 0 0 24px rgba(203,127,57,.16),0 0 12px rgba(0,0,0,.36)!important
}
</style>
<script id="wr-group-drag-v17-script">
/* War Room v1.7.28 - Pointer raid drag/drop v17 */
(function(){
  if(window.__wrGroupDragV17)return;window.__wrGroupDragV17=true;
  const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
  let drag=null,suppressClickUntil=0;

  function nameFromCard(card){try{return decodeURIComponent(card?.dataset?.name||'')}catch(_){return card?.dataset?.name||''}}
  function raidNameAt(i){try{return raid?.[i]||''}catch(_){return ''}}
  function person(name){try{return roster.find(x=>x.name===name)||null}catch(_){return null}}
  function groupOf(i){return Math.floor(i/5)+1}
  function posOf(i){return (i%5)+1}
  function ensure25(){while(raid.length<25)raid.push(null)}
  function trimRaid(){while(raid.length&&!raid[raid.length-1])raid.pop()}
  function firstEmpty(start,end,exclude=-1){for(let i=start;i<end;i++)if(i!==exclude&&!raid[i])return i;return -1}
  function firstEmptyRaid(exclude=-1){for(let i=0;i<25;i++)if(i!==exclude&&!raid[i])return i;return -1}
  function finish(msg){trimRaid();save();if(msg)toast(msg)}

  function moveNameToSlot(name,slot){
    slot=Number(slot);if(!name||!Number.isInteger(slot)||slot<0||slot>=25)return false;
    ensure25();
    const from=raid.indexOf(name),target=raid[slot]||null;
    if(from===slot){toast(name+' is already in G'+groupOf(slot)+' slot '+posOf(slot)+'.');return false}
    if(from>=0){
      raid[from]=target;raid[slot]=name;
      finish(target?name+' swapped with '+target+' (G'+groupOf(slot)+').':name+' moved to G'+groupOf(slot)+' slot '+posOf(slot)+'.');
      return true;
    }
    if(target){
      const empty=firstEmptyRaid(slot);
      if(empty<0){toast('Raid is full — remove someone before adding '+name+'.');return false}
      raid[empty]=target;
      raid[slot]=name;
      finish(name+' assigned to G'+groupOf(slot)+'; '+target+' moved to G'+groupOf(empty)+'.');
      return true;
    }
    raid[slot]=name;finish(name+' assigned to G'+groupOf(slot)+' slot '+posOf(slot)+'.');return true;
  }

  function moveNameToGroup(name,g){
    g=Number(g);if(!name||g<1||g>5)return false;
    ensure25();const start=(g-1)*5,end=start+5,from=raid.indexOf(name);
    if(from>=start&&from<end){toast(name+' is already in Group '+g+'.');return false}
    const target=firstEmpty(start,end,from);
    if(target<0){toast('Group '+g+' is full — drop directly on a raider to swap.');return false}
    return moveNameToSlot(name,target);
  }

  function removeName(name){
    const from=raid.indexOf(name);if(from<0)return false;
    raid[from]=null;finish(name+' returned to the roster.');return true;
  }

  function clearTargets(){
    $$('#builder .slot').forEach(x=>x.classList.remove('wr-v17-target','wr-v17-swap','wr-slot-drop-ready','wr-slot-swap-ready','drag-over'));
    $$('#builder .group').forEach(x=>x.classList.remove('wr-v17-group-target','wr-group-drop-ready'));
    $('#wrRaidBenchDrop')?.classList.remove('wr-v17-roster-target','wr-bench-over');
  }
  function disableNative(){
    $$('#roster .player-card,#builder .slot').forEach(el=>{
      el.draggable=false;el.setAttribute('draggable','false');
      el.ondragstart=null;el.ondragend=null;
    });
    $$('#builder .group').forEach(el=>{el.ondragstart=null;el.ondragend=null});
  }
  function makeGhost(name,x,y){
    const p=person(name),el=document.createElement('div');el.className='wr-v17-drag-ghost';
    const color=(typeof classColors!=='undefined'&&classColors[p?.class])||'#d3ad72';
    const glyph=(typeof classGlyphs!=='undefined'&&classGlyphs[p?.class])||'◆';
    el.innerHTML='<span style="color:'+color+'">'+glyph+'</span><span>'+String(name).replace(/[&<>]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[m]))+'</span>';
    document.body.appendChild(el);el.style.left=x+'px';el.style.top=y+'px';return el;
  }
  function beginDrag(e){
    if(!drag||drag.active)return;drag.active=true;drag.ghost=makeGhost(drag.name,e.clientX,e.clientY);
    document.body.classList.add('wr-pointer-raid-dragging','wr-raid-drag-active');
    if(drag.origin==='raid')document.body.classList.add('wr-drag-from-raid');
    drag.source?.classList.add('wr-raid-dragging');
  }
  function hitAt(x,y){
    const el=document.elementFromPoint(x,y);if(!el)return {};
    const slot=el.closest?.('#builder .slot[data-slot]');if(slot)return{kind:'slot',el:slot,slot:Number(slot.dataset.slot)};
    const bench=el.closest?.('#wrRaidBenchDrop');if(bench)return{kind:'roster',el:bench};
    const panel=el.closest?.('#rosterPanel');if(panel&&drag?.origin==='raid')return{kind:'roster',el:$('#wrRaidBenchDrop')||panel};
    const group=el.closest?.('#builder .group[data-group]');if(group)return{kind:'group',el:group,group:Number(group.dataset.group)};
    return{};
  }
  function paintHit(hit){
    clearTargets();
    if(hit.kind==='slot'){
      hit.el.classList.add('wr-v17-target');
      if(raidNameAt(hit.slot)&&raidNameAt(hit.slot)!==drag?.name)hit.el.classList.add('wr-v17-swap');
      hit.el.closest('.group')?.classList.add('wr-v17-group-target');
    }else if(hit.kind==='group')hit.el.classList.add('wr-v17-group-target');
    else if(hit.kind==='roster')hit.el?.classList.add('wr-v17-roster-target');
  }
  function cleanup(){
    clearTargets();drag?.source?.classList.remove('wr-raid-dragging');drag?.ghost?.remove();
    document.body.classList.remove('wr-pointer-raid-dragging','wr-raid-drag-active','wr-drag-from-raid');drag=null;disableNative();
  }

  document.addEventListener('pointerdown',e=>{
    if(e.button!==0||e.isPrimary===false)return;
    if(e.target.closest?.('button,input,select,textarea,a,[contenteditable="true"]'))return;
    const slot=e.target.closest?.('#builder .slot[data-slot]');
    if(slot){const i=Number(slot.dataset.slot),name=raidNameAt(i);if(name){drag={name,origin:'raid',from:i,source:slot,x:e.clientX,y:e.clientY,pointerId:e.pointerId,active:false,ghost:null};return}}
    const card=e.target.closest?.('#roster .player-card');
    if(card){const name=nameFromCard(card);if(name){const from=raid.indexOf(name);drag={name,origin:from>=0?'raid':'roster',from,source:card,x:e.clientX,y:e.clientY,pointerId:e.pointerId,active:false,ghost:null}}}
  },true);

  window.addEventListener('pointermove',e=>{
    if(!drag||e.pointerId!==drag.pointerId)return;
    const dx=e.clientX-drag.x,dy=e.clientY-drag.y;
    if(!drag.active&&Math.hypot(dx,dy)>=6)beginDrag(e);
    if(!drag.active)return;
    e.preventDefault();if(drag.ghost){drag.ghost.style.left=e.clientX+'px';drag.ghost.style.top=e.clientY+'px'}
    paintHit(hitAt(e.clientX,e.clientY));
  },{capture:true,passive:false});

  window.addEventListener('pointerup',e=>{
    if(!drag||e.pointerId!==drag.pointerId)return;
    if(!drag.active){drag=null;return}
    e.preventDefault();e.stopPropagation();const d=drag,hit=hitAt(e.clientX,e.clientY);suppressClickUntil=Date.now()+350;
    clearTargets();d.source?.classList.remove('wr-raid-dragging');d.ghost?.remove();document.body.classList.remove('wr-pointer-raid-dragging','wr-raid-drag-active','wr-drag-from-raid');drag=null;
    if(hit.kind==='slot')moveNameToSlot(d.name,hit.slot);
    else if(hit.kind==='group')moveNameToGroup(d.name,hit.group);
    else if(hit.kind==='roster'&&d.origin==='raid')removeName(d.name);
    disableNative();
  },true);
  window.addEventListener('pointercancel',()=>cleanup(),true);
  document.addEventListener('click',e=>{if(Date.now()<suppressClickUntil){e.preventDefault();e.stopImmediatePropagation()}},true);

  try{
    if(typeof renderRoster==='function'){const prev=renderRoster;renderRoster=function(){const r=prev.apply(this,arguments);disableNative();return r}}
    if(typeof renderRaid==='function'){const prev=renderRaid;renderRaid=function(){const r=prev.apply(this,arguments);disableNative();return r}}
    if(typeof bindDrag==='function')bindDrag=function(){disableNative()};
  }catch(e){console.warn('[War Room] V17 render hook failed',e)}

  const mo=new MutationObserver(()=>disableNative());
  if(document.body)mo.observe(document.body,{childList:true,subtree:true});
  disableNative();
  window.WarRoomGroupDragV17={moveNameToSlot,moveNameToGroup,removeName,disableNative};
  console.info('[War Room v1.7.28] pointer raid drag/drop v17 active');
})();
</script>
'''

if '</body>' not in h:
    raise RuntimeError('body close marker missing')
h=h.replace('</body>',block+'\n</body>',1)
index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 pointer raid drag/drop v17 installed')
