from pathlib import Path
import sys

if len(sys.argv) < 2:
    raise SystemExit('usage: v178_raidframe_polish_patch.py <app-root>')
root = Path(sys.argv[1])
index = root / 'index.html'
if not index.exists():
    raise RuntimeError('index.html missing: ' + str(index))

h = index.read_text(encoding='utf-8')
MARK = 'War Room v1.7.28 - Raid frame polish v18'
if MARK in h:
    print('War Room v1.7.28 raid frame polish v18 already installed')
    raise SystemExit(0)

block = r'''
<style id="wr-raidframe-polish-v18-style">
/* War Room v1.7.28 - Raid frame polish v18 */
#builder{
  gap:7px!important;
  align-items:start!important;
}
#builder .group{
  min-height:0!important;
  margin:0!important;
  position:relative!important;
  overflow:hidden!important;
  background:linear-gradient(180deg,#100c0a,#090706)!important;
  border-width:1px!important;
  box-shadow:0 10px 24px rgba(0,0,0,.24),inset 0 0 0 1px rgba(255,218,155,.025)!important;
}
#builder .group .squad-banner{
  margin:0!important;
  min-height:28px;
  display:flex;align-items:center;
  padding:5px 8px!important;
  border:0!important;border-bottom:1px solid color-mix(in srgb,var(--group-accent,#8d1813) 52%,#2f211c)!important;
  background:linear-gradient(90deg,color-mix(in srgb,var(--group-accent,#8d1813) 48%,#160d0a),#0d0907 78%)!important;
  color:#dbc3a6!important;
  font-size:7px!important;letter-spacing:1.15px!important;
}
#builder .group .gtitle{
  min-height:42px!important;
  padding:6px 8px!important;
  background:linear-gradient(90deg,color-mix(in srgb,var(--group-accent,#8d1813) 22%,#15100d),#0d0a08 72%)!important;
  border-bottom:1px solid #2d211c!important;
}
#builder .group .gtitle>span:first-child{
  font:1000 12px/1 Arial,sans-serif!important;
  letter-spacing:.9px!important;
  color:#f0dfcf!important;
}
#builder .group .gtitle>span:last-child{
  min-width:42px!important;
  padding:4px 6px!important;
  border-radius:2px!important;
  font-size:8px!important;
  letter-spacing:.55px!important;
}
.wr-v18-group-meta{
  display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:3px;
  padding:5px 6px;border-bottom:1px solid #281e19;background:#0a0807;
}
.wr-v18-role-count{
  min-width:0;height:25px;display:flex;align-items:center;justify-content:center;gap:3px;
  border:1px solid #342821;background:#0d0a08;color:#8d7d71;
  font:900 7px/1 Arial,sans-serif;letter-spacing:.35px;text-transform:uppercase;
}
.wr-v18-role-count b{font-size:9px;color:#d9c8b8}
.wr-v18-role-count.tank{border-color:#704622;color:#c58b51}
.wr-v18-role-count.healer{border-color:#546254;color:#aebdaf}
.wr-v18-role-count.melee{border-color:#604638;color:#b59179}
.wr-v18-role-count.ranged{border-color:#35556a;color:#78a9c7}
#builder .slots{gap:2px!important;padding:4px!important;background:#080605!important}
#builder .slot{
  min-height:48px!important;
  padding:5px 6px!important;
  border:1px solid #2c211c!important;
  background:linear-gradient(90deg,color-mix(in srgb,var(--wr-class,#3b2a23) 7%,#100c0a),#0c0908 72%)!important;
  box-shadow:inset 3px 0 0 color-mix(in srgb,var(--wr-class,#5d4336) 72%,#2a1c17)!important;
  transition:border-color .1s ease,background .1s ease,transform .1s ease!important;
}
#builder .slot:not(.empty):hover{
  border-color:color-mix(in srgb,var(--wr-class,#81523e) 55%,#685044)!important;
  background:linear-gradient(90deg,color-mix(in srgb,var(--wr-class,#5a362b) 13%,#15100d),#0d0a08 75%)!important;
}
#builder .slot .wr-raid-member-main{gap:6px!important;flex:1;min-width:0}
#builder .slot .wr-raid-race-photo{width:32px!important;height:32px!important;min-width:32px!important}
#builder .slot b{font-size:9px!important;color:#eee0d2!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#builder .slot .remove{
  width:22px;height:22px;padding:0!important;display:grid;place-items:center;
  border-radius:2px!important;border-color:#3e2a23!important;background:#0b0807!important;
  color:#865d52!important;font-size:12px!important;line-height:1!important;
}
#builder .slot .remove:hover{border-color:#8d4637!important;color:#e5a18e!important;background:#1a0d0a!important}
.wr-v18-slot-no{
  flex:0 0 auto;width:17px;height:17px;display:grid;place-items:center;
  border:1px solid #3b2b24;background:#080605;color:#72645b;
  font:900 6px/1 Arial,sans-serif;
}
.wr-v18-role-badge{
  flex:0 0 auto;min-width:20px;height:20px;padding:0 4px;display:grid;place-items:center;
  border:1px solid #3d3029;background:#0a0807;color:#8e7e72;
  font:1000 6px/1 Arial,sans-serif;letter-spacing:.4px;
}
.wr-v18-role-badge.tank{color:#e3a467;border-color:#76502d;background:#150e09}
.wr-v18-role-badge.healer{color:#d8e0d8;border-color:#596a59;background:#0c120d}
.wr-v18-role-badge.melee{color:#d0aa8d;border-color:#665043;background:#130e0b}
.wr-v18-role-badge.ranged{color:#9ac8e3;border-color:#41667c;background:#091117}
#builder .slot.empty{
  min-height:48px!important;
  justify-content:flex-start!important;
  gap:7px!important;
  border:1px dashed #33271f!important;
  box-shadow:none!important;
  background:linear-gradient(90deg,rgba(255,255,255,.012),transparent)!important;
  color:#5f534b!important;font-style:normal!important;
}
#builder .slot.empty .wr-v18-empty-copy{display:grid;gap:1px}
#builder .slot.empty .wr-v18-empty-copy b{font-size:7px!important;color:#6f6157!important;letter-spacing:.6px;text-transform:uppercase}
#builder .slot.empty .wr-v18-empty-copy small{font-size:6px;color:#4c423c;text-transform:uppercase;letter-spacing:.5px}
#builder .slot.empty:hover{
  border-color:#6f4b31!important;color:#b58a5b!important;
  background:linear-gradient(90deg,rgba(132,70,31,.12),transparent)!important;
}
#builder .group-health{height:3px!important;background:#090706!important;border-top:1px solid #211914!important}
#builder .group-buffs{padding:6px!important;background:#0b0807!important}
#builder .buff-section-title{font-size:6px!important;letter-spacing:.8px!important;margin-bottom:4px!important}
#builder .party-icon-row{gap:3px!important}
#builder .party-icon{width:23px!important;height:23px!important;font-size:9px!important}
#builder .group-ready{
  min-height:29px!important;padding:5px 7px!important;
  background:linear-gradient(90deg,#0d0a08,#080605)!important;
}
#builder .ready-text{font-size:6px!important;letter-spacing:.45px!important}
#builder .ready-text b{font-size:7px!important}
#builder .group.wr-v18-full .gtitle>span:last-child{color:#9ed4a4!important;border-color:#3f6245!important;background:#0a130c!important}
#builder .group.wr-v18-open .gtitle>span:last-child{color:#dbb26f!important}
#builder .group.wr-v17-group-target{transform:translateY(-1px)}
#builder .slot.wr-v17-target{transform:translateX(1px)}
@media(max-width:1550px){
  .wr-v18-group-meta{grid-template-columns:repeat(4,1fr)}
}
</style>
<script id="wr-raidframe-polish-v18-script">
/* War Room v1.7.28 - Raid frame polish v18 */
(function(){
  if(window.__wrRaidFramePolishV18)return;window.__wrRaidFramePolishV18=true;
  function pAt(i){try{const n=raid?.[i];return n?roster.find(x=>x.name===n)||null:null}catch(_){return null}}
  function roleOf(p){
    if(!p)return 'Unknown';
    try{if(typeof wrRole==='function'){const r=wrRole(p);if(r)return r}}catch(_){}
    const r=String(p.role||'').toLowerCase();
    if(r.includes('tank'))return'Tank';if(r.includes('heal'))return'Healer';if(r.includes('melee'))return'Melee';if(r.includes('ranged')||r.includes('caster'))return'Ranged';
    const spec=String(p.spec||p.talentSpec||p.activeSpec||'').toLowerCase(),cl=String(p.class||'');
    if(/protection|guardian|feral.*tank/.test(spec))return'Tank';
    if(/holy|restoration|discipline/.test(spec))return'Healer';
    if(/arms|fury|combat|assassination|subtlety|retribution|enhancement|feral/.test(spec)||cl==='Rogue')return'Melee';
    if(['Mage','Warlock','Hunter'].includes(cl)||spec)return'Ranged';
    return'Unknown';
  }
  function roleClass(r){return String(r||'unknown').toLowerCase()}
  function roleShort(r){return({Tank:'T',Healer:'H',Melee:'M',Ranged:'R'})[r]||'?'}
  function enhance(){
    const builder=document.getElementById('builder');if(!builder)return;
    builder.querySelectorAll('.group[data-group]').forEach(group=>{
      const g=Number(group.dataset.group)||1,start=(g-1)*5;
      const players=[0,1,2,3,4].map(j=>pAt(start+j)).filter(Boolean);
      const counts={Tank:0,Healer:0,Melee:0,Ranged:0,Unknown:0};players.forEach(p=>counts[roleOf(p)]++);
      group.classList.toggle('wr-v18-full',players.length===5);group.classList.toggle('wr-v18-open',players.length<5);
      let meta=group.querySelector('.wr-v18-group-meta');
      if(!meta){meta=document.createElement('div');meta.className='wr-v18-group-meta';group.querySelector('.gtitle')?.insertAdjacentElement('afterend',meta)}
      if(meta)meta.innerHTML=[['Tank','T'],['Healer','H'],['Melee','M'],['Ranged','R']].map(([r,l])=>`<span class="wr-v18-role-count ${roleClass(r)}" title="${r}"><span>${l}</span><b>${counts[r]||0}</b></span>`).join('');
      const count=group.querySelector('.gtitle>span:last-child');if(count)count.textContent=players.length===5?'5/5 READY':players.length+'/5 OPEN';
    });
    builder.querySelectorAll('.slot[data-slot]').forEach(slot=>{
      const i=Number(slot.dataset.slot),p=pAt(i),slotNo=(i%5)+1;
      slot.style.setProperty('--wr-class',p&&typeof classColors!=='undefined'&&classColors[p.class]?classColors[p.class]:'#4a372e');
      let no=slot.querySelector('.wr-v18-slot-no');
      if(!no){no=document.createElement('span');no.className='wr-v18-slot-no';slot.insertBefore(no,slot.firstChild)}
      no.textContent=String(slotNo);no.title='Group slot '+slotNo;
      slot.querySelectorAll(':scope > .wr-v18-role-badge').forEach(x=>x.remove());
      if(p){
        const r=roleOf(p),badge=document.createElement('span');badge.className='wr-v18-role-badge '+roleClass(r);badge.textContent=roleShort(r);badge.title=r;
        const remove=slot.querySelector(':scope > .remove');if(remove)slot.insertBefore(badge,remove);else slot.appendChild(badge);
        slot.dataset.role=r;slot.title=(p.name||'Raider')+' • '+r+' • '+(p.class||'');
      }else{
        slot.removeAttribute('data-role');slot.title='Drop a raider into Group '+(Math.floor(i/5)+1)+' slot '+slotNo;
        const textNodes=[...slot.childNodes].filter(n=>n.nodeType===3&&String(n.textContent||'').trim());textNodes.forEach(n=>n.remove());
        let copy=slot.querySelector('.wr-v18-empty-copy');if(!copy){copy=document.createElement('span');copy.className='wr-v18-empty-copy';slot.appendChild(copy)}
        copy.innerHTML='<b>Open Raid Slot</b><small>Drop raider here</small>';
      }
    });
  }
  try{
    if(typeof renderRaid==='function'){
      const prev=renderRaid;renderRaid=function(){const out=prev.apply(this,arguments);enhance();return out};
    }
  }catch(e){console.warn('[War Room] V18 render hook failed',e)}
  enhance();setTimeout(enhance,100);setTimeout(enhance,600);
  window.WarRoomRaidFramePolishV18={enhance,roleOf};
  console.info('[War Room v1.7.28] raid frame polish v18 active');
})();
</script>
'''

if '</body>' not in h:
    raise RuntimeError('body marker missing for raid frame polish v18')
h = h.replace('</body>', block + '\n</body>', 1)
index.write_text(h, encoding='utf-8')
print('War Room v1.7.28 raid frame polish v18 installed')
