from pathlib import Path
import sys

if len(sys.argv)<2:
    raise SystemExit('usage: v178_roster_drag_patch.py <app-root>')
out=Path(sys.argv[1])
index=out/'index.html'
if not index.exists():
    raise RuntimeError('index.html missing: '+str(index))
assets=out/'assets'/'races'
assets.mkdir(parents=True,exist_ok=True)

base_start='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128"><defs><radialGradient id="bg" cx="50%" cy="35%" r="75%"><stop offset="0" stop-color="#2d211b"/><stop offset="1" stop-color="#080605"/></radialGradient><linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#e0b56c"/><stop offset=".5" stop-color="#6f3a29"/><stop offset="1" stop-color="#24120e"/></linearGradient></defs><rect width="128" height="128" rx="18" fill="url(#bg)"/><rect x="4" y="4" width="120" height="120" rx="15" fill="none" stroke="url(#rim)" stroke-width="4"/><circle cx="64" cy="66" r="47" fill="#0d0908" opacity=".7"/>'''
end='</svg>'
svgs={
'orc': base_start+'''<path d="M34 47 18 32l18 28M94 47l16-15-18 28" fill="#60833e" stroke="#23351f" stroke-width="3"/><path d="M34 31c7-15 52-15 60 1l8 32c2 33-18 48-38 48S24 97 27 64z" fill="#6f9148" stroke="#2a351f" stroke-width="4"/><path d="M36 39c9-19 50-20 58-1-12-7-46-8-58 1z" fill="#21130f"/><path d="M42 65h16M70 65h16" stroke="#d8b850" stroke-width="5" stroke-linecap="round"/><path d="M45 88 38 109l13-14M83 88l7 21-13-14" fill="#d8ccb0" stroke="#665b47" stroke-width="2"/><path d="M52 79c7 5 17 5 24 0" stroke="#2d2017" stroke-width="4" fill="none"/>'''+end,
'troll': base_start+'''<path d="M30 46 13 52l19 6M98 46l17 6-19 6" fill="#4d8ea0"/><path d="M38 26c7-10 45-11 54 2l6 39c1 27-13 46-34 46S29 94 30 67z" fill="#5798a9" stroke="#244852" stroke-width="4"/><path d="M39 32c12-16 45-15 52 0l-9 4-18-8-18 8z" fill="#a94444"/><path d="M40 66h17M71 66h17" stroke="#f2c55e" stroke-width="4" stroke-linecap="round"/><path d="M45 88 29 113l25-18M83 88l16 25-25-18" fill="#e0d3af" stroke="#6a5c47" stroke-width="2"/><path d="M55 80c5 2 13 2 18 0" stroke="#2a5059" stroke-width="4"/>'''+end,
'tauren': base_start+'''<path d="M43 36C34 15 16 13 8 20c19 2 28 13 34 27M85 36c9-21 27-23 35-16-19 2-28 13-34 27" fill="#d0b489" stroke="#715c40" stroke-width="3"/><path d="M31 41c6-19 60-19 66 0l2 37c0 24-17 36-35 36S29 102 29 78z" fill="#7b583a" stroke="#3a281b" stroke-width="4"/><path d="M36 38c15-17 43-17 56 0l-4 13-48 0z" fill="#2b1d14"/><path d="M40 69h15M73 69h15" stroke="#e2b75b" stroke-width="4" stroke-linecap="round"/><path d="M48 83c8 9 24 9 32 0l-3 17H51z" fill="#5d3e2a"/><ellipse cx="56" cy="89" rx="3" ry="2" fill="#241812"/><ellipse cx="72" cy="89" rx="3" ry="2" fill="#241812"/>'''+end,
'undead': base_start+'''<path d="M34 39c8-18 52-20 61 0l-4 22 7 12-8 32-22 11-25-11-11-31 7-13z" fill="#747d77" stroke="#323a36" stroke-width="4"/><path d="M36 38c13-17 45-18 56-1l-10 7-15-6-14 7z" fill="#332923"/><path d="M41 66h17M70 66h17" stroke="#6ee4ef" stroke-width="4" stroke-linecap="round"/><circle cx="49" cy="66" r="3" fill="#9ff5ff"/><circle cx="78" cy="66" r="3" fill="#9ff5ff"/><path d="M52 83h24l-4 17H56z" fill="#313a36"/><path d="M56 85v12M63 84v14M70 85v12" stroke="#9ca39b" stroke-width="3"/><path d="m36 55-10 8 9 7m57-15 10 8-9 7" stroke="#56605a" stroke-width="5" fill="none"/>'''+end,
'bloodelf': base_start+'''<path d="M33 48 8 38l27 25M95 48l25-10-27 25" fill="#d29a7b" stroke="#7e5846" stroke-width="3"/><path d="M35 29c8-14 50-15 58 0l6 38c0 29-15 46-35 46S29 96 29 67z" fill="#d7a183" stroke="#755343" stroke-width="4"/><path d="M35 34c11-23 49-25 60-2l-11 6-14-7-18 6-10 15z" fill="#c8ad60"/><path d="M41 66h17M70 66h17" stroke="#58ef80" stroke-width="4" stroke-linecap="round"/><circle cx="49" cy="66" r="3" fill="#8cff9e"/><circle cx="78" cy="66" r="3" fill="#8cff9e"/><path d="M51 87c8 6 19 6 27 0" stroke="#855c4e" stroke-width="3" fill="none"/>'''+end,
'unknown': base_start+'''<circle cx="64" cy="59" r="28" fill="#4a3b34"/><path d="M37 109c3-23 17-35 27-35s24 12 27 35" fill="#342822"/><text x="64" y="67" text-anchor="middle" font-family="Georgia,serif" font-size="32" fill="#d1a95f">?</text>'''+end,
}
for name,svg in svgs.items():
    (assets/f'{name}.svg').write_text(svg,encoding='utf-8')

css=r'''
<style id="wr-roster-drag-v14-style">
/* War Room v1.7.28 - Roster Portrait + Raid Drag Pass */
.player-card{min-height:72px!important;padding:7px 8px!important;transition:border-color .12s ease,background .12s ease,transform .12s ease!important}
.player-card:hover{transform:translateX(2px)}
.race-portrait.wr-photo-portrait{position:relative;width:58px!important;height:58px!important;min-width:58px;border:1px solid color-mix(in srgb,var(--class-accent,#9a6a45) 55%,#5d4135)!important;background:#080605!important;overflow:hidden;box-shadow:inset 0 0 0 1px rgba(225,184,104,.08),0 3px 12px rgba(0,0,0,.35)!important}
.race-portrait.wr-photo-portrait:before{display:none!important}
.race-photo{width:100%;height:100%;display:block;object-fit:cover;filter:saturate(.96) contrast(1.05)}
.race-photo-label{position:absolute;left:3px;right:3px;bottom:3px;padding:2px 3px;background:rgba(6,4,3,.78);border-top:1px solid rgba(218,176,100,.16);color:#e0c18a;font-size:6px;font-weight:1000;letter-spacing:.7px;text-align:center;text-transform:uppercase;text-shadow:0 1px 2px #000}
.player-card .player-main{gap:9px!important}
.player-card .name{font-size:12px!important;line-height:1.15}
.player-card .tag{font-size:7px!important}
.group.wr-group-drop-ready{outline:1px solid color-mix(in srgb,var(--group-accent,#8d1b15) 75%,#d8aa58);outline-offset:-2px;box-shadow:inset 0 0 24px color-mix(in srgb,var(--group-accent,#8d1b15) 20%,transparent)!important}
.group .slot.wr-raid-draggable{cursor:grab;transition:background .1s ease,border-color .1s ease,transform .1s ease}
.group .slot.wr-raid-draggable:active{cursor:grabbing}
.group .slot.wr-raid-dragging{opacity:.38;transform:scale(.98)}
.group .slot.drag-over{background:linear-gradient(90deg,rgba(115,48,31,.45),rgba(34,22,17,.96))!important;box-shadow:inset 0 0 0 1px #b67b47!important}
.wr-raid-member-main{display:flex!important;align-items:center;gap:7px;min-width:0}
.wr-raid-race-photo{width:30px;height:30px;min-width:30px;object-fit:cover;border:1px solid color-mix(in srgb,var(--member-class,#a36c43) 58%,#5b3d31);background:#080605;box-shadow:inset 0 0 0 1px rgba(216,172,91,.08)}
.wr-drag-grip{margin-left:auto;margin-right:18px;color:#6d5a4e;font-size:11px;letter-spacing:-2px;opacity:.62;pointer-events:none}
.group .slot:hover .wr-drag-grip{color:#c69b61;opacity:1}
.wr-drop-hint{display:block;color:#725f53;font-size:7px;margin-top:2px;text-transform:uppercase;letter-spacing:.6px}
</style>
'''

js=r'''
<script id="wr-roster-drag-v14-script">
/* War Room v1.7.28 - Roster Portrait + Group-to-Group Drag */
(function(){
  const raceAsset={orc:'orc',troll:'troll',tauren:'tauren',undead:'undead',scourge:'undead',bloodelf:'bloodelf'};
  const raceSlug=r=>String(r||'').toLowerCase().replace(/[^a-z]/g,'');
  const raceSrc=p=>'assets/races/'+(raceAsset[raceSlug(p?.race)]||'unknown')+'.svg';
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

  try{
    racePortraitHTML=function(p){
      const race=String(p?.race||'Unknown Race');
      return `<div class="race-portrait wr-photo-portrait" style="--class-accent:${classColors[p?.class]||'#9a6a45'}" title="${esc(race)} base portrait"><img class="race-photo" src="${raceSrc(p)}" alt="${esc(race)} portrait"><span class="race-photo-label">${esc(race)}</span></div>`;
    };
  }catch(e){console.warn('[War Room] race portrait override unavailable',e)}

  function memberByName(name){
    try{return roster.find(x=>x.name===name)||null}catch(e){return null}
  }
  function slotName(slot){
    const b=slot.querySelector('b');
    return b?String(b.textContent||'').trim():'';
  }
  function clearGroupHighlights(){document.querySelectorAll('.group').forEach(g=>g.classList.remove('wr-group-drop-ready'))}

  window.wrStartRaidDrag=function(e,name){
    if(!e?.dataTransfer||!name)return;
    e.stopPropagation();
    e.dataTransfer.setData('text/plain',name);
    e.dataTransfer.effectAllowed='move';
    e.currentTarget?.classList.add('wr-raid-dragging');
    document.body.classList.add('wr-raid-drag-active');
  };
  window.wrEndRaidDrag=function(e){
    e?.currentTarget?.classList.remove('wr-raid-dragging');
    document.body.classList.remove('wr-raid-drag-active');
    clearGroupHighlights();
  };
  window.wrDropRaidGroup=function(e,groupNumber){
    e.preventDefault();e.stopPropagation();clearGroupHighlights();
    const name=e.dataTransfer?.getData('text/plain');
    if(!name)return;
    const start=(Number(groupNumber)-1)*5;
    const end=start+5;
    const current=raid.indexOf(name);
    if(current>=start&&current<end){toast(name+' is already in Group '+groupNumber+'.');return;}
    let target=-1;
    for(let i=start;i<end;i++){if(!raid[i]){target=i;break}}
    if(target<0){toast('Group '+groupNumber+' is full — drop onto a raider to swap.');return;}
    dropRaid(e,target);
  };

  const baseDropRaid=window.dropRaid;
  if(typeof baseDropRaid==='function'){
    window.dropRaid=function(e,slot){
      e?.stopPropagation?.();
      const before=e?.dataTransfer?.getData('text/plain')||'';
      baseDropRaid(e,slot);
      clearGroupHighlights();
      if(before)console.info('[War Room Raid Move]',before,'-> slot',slot+1);
    };
  }

  function enhanceRaid(){
    document.querySelectorAll('#builder .group').forEach((group,gi)=>{
      group.ondragover=e=>{e.preventDefault();e.dataTransfer.dropEffect='move';group.classList.add('wr-group-drop-ready')};
      group.ondragenter=e=>{e.preventDefault();group.classList.add('wr-group-drop-ready')};
      group.ondragleave=e=>{if(!group.contains(e.relatedTarget))group.classList.remove('wr-group-drop-ready')};
      group.ondrop=e=>wrDropRaidGroup(e,gi+1);
    });
    document.querySelectorAll('#builder .slot').forEach(slot=>{
      const name=slotName(slot); if(!name)return;
      const p=memberByName(name); if(!p)return;
      slot.classList.add('wr-raid-draggable');
      slot.setAttribute('draggable','true');
      slot.dataset.raidName=name;
      slot.ondragstart=e=>wrStartRaidDrag(e,name);
      slot.ondragend=wrEndRaidDrag;
      const first=slot.querySelector(':scope > span');
      if(first){
        first.classList.add('wr-raid-member-main');
        const old=first.querySelector('.raid-portrait'); if(old)old.style.display='none';
        if(!first.querySelector('.wr-raid-race-photo')){
          const img=document.createElement('img');img.className='wr-raid-race-photo';img.src=raceSrc(p);img.alt=p.race+' portrait';img.style.setProperty('--member-class',classColors[p.class]||'#9a6a45');first.insertBefore(img,first.firstChild);
        }
      }
      if(!slot.querySelector('.wr-drag-grip')){
        const grip=document.createElement('span');grip.className='wr-drag-grip';grip.textContent='⋮⋮';grip.title='Drag to another raid slot or group';slot.appendChild(grip);
      }
      const remove=slot.querySelector('button.remove'); if(remove)remove.setAttribute('draggable','false');
    });
  }

  try{
    if(typeof renderRaid==='function'){
      const baseRenderRaid=renderRaid;
      renderRaid=function(){baseRenderRaid();enhanceRaid()};
    }
    if(typeof renderRoster==='function'){
      const baseRenderRoster=renderRoster;
      renderRoster=function(){baseRenderRoster()};
    }
    renderRoster?.();
    enhanceRaid();
  }catch(e){console.warn('[War Room] roster/raid enhancement failed',e)}
})();
</script>
'''

s=index.read_text(encoding='utf-8')
marker='<!-- legacy QA markers:'
if marker not in s: raise SystemExit('marker missing')
if 'wr-roster-drag-v14-script' not in s:
    s=s.replace(marker,css+'\n'+js+'\n'+marker,1)
index.write_text(s,encoding='utf-8')
print('War Room v1.7.28 roster portraits + raid drag/drop v14 installed')
