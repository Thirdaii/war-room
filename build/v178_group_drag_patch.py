from pathlib import Path
import sys

if len(sys.argv)<2:
    raise SystemExit('usage: v178_group_drag_patch.py <app-root>')
root=Path(sys.argv[1])
index=root/'index.html'
if not index.exists():
    raise RuntimeError('index.html missing: '+str(index))
h=index.read_text(encoding='utf-8')
MARK='War Room v1.7.28 - Raid group drag/drop v16'
if MARK in h:
    print('War Room raid group drag/drop v16 already installed')
    raise SystemExit(0)

block=r'''
<style id="wr-group-drag-v16-style">
/* War Room v1.7.28 - Raid group drag/drop v16 */
#wrRaidBenchDrop{
  max-height:0;opacity:0;overflow:hidden;margin:0;border:0 solid transparent;padding:0 12px;
  display:flex;align-items:center;justify-content:center;gap:8px;
  color:#8d7462;background:linear-gradient(180deg,rgba(42,25,19,.72),rgba(18,12,10,.9));
  font-size:9px;font-weight:900;letter-spacing:.8px;text-transform:uppercase;
  transition:max-height .15s ease,opacity .15s ease,margin .15s ease,padding .15s ease,border-color .15s ease,background .15s ease;
}
body.wr-drag-from-raid #wrRaidBenchDrop{
  max-height:44px;opacity:1;margin:0 10px 8px;padding:9px 12px;border-width:1px;border-color:#5d4132;
}
body.wr-drag-from-raid #wrRaidBenchDrop.wr-bench-over{
  color:#f4d18e;border-color:#b67b47;background:linear-gradient(180deg,rgba(104,52,28,.74),rgba(32,18,13,.96));
  box-shadow:inset 0 0 20px rgba(201,124,57,.16),0 0 10px rgba(0,0,0,.35);
}
.wr-group-drop-caption{
  display:none;margin:5px 8px 7px;padding:5px 7px;border:1px dashed rgba(180,125,70,.42);
  color:#806a59;background:rgba(10,7,6,.52);font-size:7px;font-weight:900;letter-spacing:.65px;text-align:center;text-transform:uppercase;
}
body.wr-raid-drag-active #builder .group .wr-group-drop-caption{display:block}
body.wr-raid-drag-active #builder .group.wr-group-drop-ready .wr-group-drop-caption{color:#e1bd79;border-color:#b67b47;background:rgba(89,43,24,.36)}
#builder .slot.wr-slot-drop-ready{
  border-color:#b67b47!important;background:linear-gradient(90deg,rgba(112,55,31,.52),rgba(27,18,14,.96))!important;
  box-shadow:inset 0 0 0 1px rgba(226,171,93,.22),0 0 10px rgba(0,0,0,.28)!important;
}
#builder .slot.wr-slot-swap-ready{border-color:#d4a45d!important}
#builder .slot.wr-slot-swap-ready:after{
  content:'SWAP';position:absolute;right:31px;top:50%;transform:translateY(-50%);
  color:#d6ae6e;font-size:6px;font-weight:1000;letter-spacing:.8px;pointer-events:none;
}
#builder .slot{position:relative}
#builder .slot.empty.wr-slot-drop-ready{color:#d6ae6e!important}
.wr-drag-grip{cursor:grab!important;user-select:none}
.wr-drag-grip:active{cursor:grabbing!important}
.wr-raid-drag-ghost{
  position:fixed;left:-9999px;top:-9999px;display:flex;align-items:center;gap:7px;
  padding:6px 9px;border:1px solid #b67b47;border-radius:4px;background:#140e0b;color:#ead2a4;
  font:900 10px/1.1 Arial,sans-serif;box-shadow:0 8px 22px rgba(0,0,0,.55);white-space:nowrap;
}
</style>
<script id="wr-group-drag-v16-script">
/* War Room v1.7.28 - Raid group drag/drop v16 */
(function(){
  if(window.__wrGroupDragV16)return;window.__wrGroupDragV16=true;
  const TYPE='application/x-warroom-raider';
  const qs=s=>document.querySelector(s);
  const qsa=s=>[...document.querySelectorAll(s)];
  const text=v=>String(v??'').trim();

  function trimRaid(){while(raid.length&&!raid[raid.length-1])raid.pop()}
  function persist(msg){trimRaid();save();if(msg)toast(msg)}
  function groupOf(slot){return Math.floor(slot/5)+1}
  function posOf(slot){return (slot%5)+1}
  function member(name){try{return roster.find(x=>x.name===name)||null}catch(_){return null}}
  function payload(dt){
    let raw='';try{raw=dt?.getData(TYPE)||''}catch(_){}
    if(raw){try{const p=JSON.parse(raw);if(p&&p.name)return p}catch(_){}}
    let name='';try{name=text(dt?.getData('text/plain'))}catch(_){}
    if(!name)return null;
    const from=raid.indexOf(name);
    return {name,origin:from>=0?'raid':'roster',from};
  }
  function setPayload(dt,name,origin,from){
    const p={name,origin,from:Number.isInteger(from)?from:-1};
    try{dt.setData(TYPE,JSON.stringify(p))}catch(_){}
    try{dt.setData('text/plain',name)}catch(_){}
    try{dt.effectAllowed='move'}catch(_){}
  }
  function firstEmpty(start,end,exclude=-1){for(let i=start;i<end;i++)if(i!==exclude&&!raid[i])return i;return -1}
  function firstEmptyRaid(exclude=-1){for(let i=0;i<25;i++)if(i!==exclude&&!raid[i])return i;return -1}
  function clearTargets(){
    qsa('#builder .group').forEach(x=>x.classList.remove('wr-group-drop-ready'));
    qsa('#builder .slot').forEach(x=>x.classList.remove('wr-slot-drop-ready','wr-slot-swap-ready','drag-over'));
    qs('#wrRaidBenchDrop')?.classList.remove('wr-bench-over');
  }
  function endDrag(){
    clearTargets();document.body.classList.remove('wr-raid-drag-active','wr-drag-from-raid');
    qsa('.wr-raid-dragging').forEach(x=>x.classList.remove('wr-raid-dragging'));
  }
  function ghost(name){
    const p=member(name);const el=document.createElement('div');el.className='wr-raid-drag-ghost';
    el.innerHTML='<span style="color:'+(classColors[p?.class]||'#d3ad72')+'">'+(classGlyphs[p?.class]||'◆')+'</span><span>'+name+'</span>';
    document.body.appendChild(el);setTimeout(()=>el.remove(),0);return el;
  }
  function start(e,name,origin,from){
    if(!e?.dataTransfer||!name)return;
    setPayload(e.dataTransfer,name,origin,from);
    document.body.classList.add('wr-raid-drag-active');
    if(origin==='raid')document.body.classList.add('wr-drag-from-raid');
    e.currentTarget?.classList.add('wr-raid-dragging');
    try{const g=ghost(name);e.dataTransfer.setDragImage(g,16,16)}catch(_){}
  }

  function moveToSlot(e,slot){
    e?.preventDefault?.();e?.stopPropagation?.();
    const p=payload(e?.dataTransfer);clearTargets();
    if(!p||slot<0||slot>=25)return;
    const name=p.name;let from=raid.indexOf(name);const target=raid[slot]||null;
    if(from===slot){endDrag();toast(name+' is already in Group '+groupOf(slot)+' slot '+posOf(slot)+'.');return;}
    while(raid.length<25)raid.push(null);
    if(from>=0){
      raid[from]=target;
      raid[slot]=name;
      const msg=target
        ? name+' swapped with '+target+' (G'+groupOf(slot)+').'
        : name+' moved to G'+groupOf(slot)+' slot '+posOf(slot)+'.';
      endDrag();persist(msg);return;
    }
    if(!target){
      raid[slot]=name;endDrag();persist(name+' assigned to G'+groupOf(slot)+' slot '+posOf(slot)+'.');return;
    }
    const empty=firstEmptyRaid(slot);
    if(empty<0){endDrag();toast('Raid is full — remove someone before adding '+name+'.');return;}
    raid[empty]=target;raid[slot]=name;endDrag();persist(name+' assigned to G'+groupOf(slot)+'; '+target+' moved to G'+groupOf(empty)+'.');
  }

  function moveToGroup(e,groupNumber){
    e?.preventDefault?.();e?.stopPropagation?.();
    const p=payload(e?.dataTransfer);clearTargets();if(!p)return;
    const g=Number(groupNumber);if(g<1||g>5)return;
    const start=(g-1)*5,end=start+5,from=raid.indexOf(p.name);
    if(from>=start&&from<end){endDrag();toast(p.name+' is already in Group '+g+'.');return;}
    const target=firstEmpty(start,end,from);
    if(target<0){endDrag();toast('Group '+g+' is full — drop onto a raider to swap.');return;}
    moveToSlot(e,target);
  }

  function removeToRoster(e){
    e?.preventDefault?.();e?.stopPropagation?.();
    const p=payload(e?.dataTransfer);clearTargets();if(!p)return;
    const from=raid.indexOf(p.name);if(from<0){endDrag();return;}
    raid[from]=null;endDrag();persist(p.name+' returned to the roster.');
  }

  function ensureBench(){
    const panel=qs('#rosterPanel');if(!panel)return null;
    let z=qs('#wrRaidBenchDrop');if(!z){
      z=document.createElement('div');z.id='wrRaidBenchDrop';z.innerHTML='<span>↩</span><span>Drop here to remove from raid</span>';
      const head=panel.querySelector('.panel-head');(head?.nextSibling?panel.insertBefore(z,head.nextSibling):panel.appendChild(z));
    }
    z.ondragover=e=>{const p=payload(e.dataTransfer);if(raid.indexOf(p?.name)>=0){e.preventDefault();e.dataTransfer.dropEffect='move';z.classList.add('wr-bench-over')}};
    z.ondragleave=()=>z.classList.remove('wr-bench-over');
    z.ondrop=removeToRoster;
    return z;
  }

  function enhance(){
    ensureBench();
    qsa('#builder .group').forEach((group,gi)=>{
      let cap=group.querySelector('.wr-group-drop-caption');if(!cap){cap=document.createElement('div');cap.className='wr-group-drop-caption';group.appendChild(cap)}
      const start=gi*5,end=start+5,filled=raid.slice(start,end).filter(Boolean).length;
      cap.textContent=filled<5?'Drop here → first open slot':'Full group → drop on a raider to swap';
      group.ondragover=e=>{const p=payload(e.dataTransfer);if(!p)return;e.preventDefault();e.dataTransfer.dropEffect='move';group.classList.add('wr-group-drop-ready')};
      group.ondragenter=e=>{const p=payload(e.dataTransfer);if(p){e.preventDefault();group.classList.add('wr-group-drop-ready')}};
      group.ondragleave=e=>{if(!group.contains(e.relatedTarget))group.classList.remove('wr-group-drop-ready')};
      group.ondrop=e=>moveToGroup(e,gi+1);
    });
    qsa('#builder .slot').forEach((slot,si)=>{
      slot.ondragover=e=>{const p=payload(e.dataTransfer);if(!p)return;e.preventDefault();e.stopPropagation();e.dataTransfer.dropEffect='move';slot.classList.add('wr-slot-drop-ready');if(raid[si]&&raid[si]!==p.name)slot.classList.add('wr-slot-swap-ready');slot.closest('.group')?.classList.add('wr-group-drop-ready')};
      slot.ondragleave=e=>{slot.classList.remove('wr-slot-drop-ready','wr-slot-swap-ready');if(!slot.closest('.group')?.contains(e.relatedTarget))slot.closest('.group')?.classList.remove('wr-group-drop-ready')};
      slot.ondrop=e=>moveToSlot(e,si);
      const name=raid[si];if(!name)return;
      slot.setAttribute('draggable','true');slot.dataset.raidName=name;
      slot.ondragstart=e=>{e.stopPropagation();start(e,name,'raid',si)};
      slot.ondragend=endDrag;
      const grip=slot.querySelector('.wr-drag-grip');if(grip){grip.title='Drag '+name+' to another slot/group • drop on roster to remove'}
    });
  }

  document.addEventListener('dragstart',e=>{
    const card=e.target?.closest?.('.player-card');if(!card||!e.dataTransfer)return;
    const name=decodeURIComponent(card.dataset.name||'');if(!name)return;
    const from=raid.indexOf(name);setPayload(e.dataTransfer,name,from>=0?'raid':'roster',from);
    document.body.classList.add('wr-raid-drag-active');if(from>=0)document.body.classList.add('wr-drag-from-raid');
    try{const g=ghost(name);e.dataTransfer.setDragImage(g,16,16)}catch(_){}
  },true);
  document.addEventListener('dragend',endDrag,true);

  try{
    if(typeof renderRaid==='function'){
      const prev=renderRaid;renderRaid=function(){prev();enhance()};
    }
    enhance();
    console.info('[War Room v1.7.28] raid group drag/drop v16 active');
  }catch(e){console.warn('[War Room] raid group drag/drop v16 failed',e)}
})();
</script>
'''

if '</body>' in h:
    h=h.replace('</body>',block+'\n</body>',1)
else:
    h+=block
index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 raid group drag/drop v16 installed')
