from pathlib import Path
import sys

if len(sys.argv)<2:
    raise SystemExit('usage: v178_wow_portraits_patch.py <app-root>')
root=Path(sys.argv[1])
index=root/'index.html'
if not index.exists():
    raise RuntimeError('index.html missing: '+str(index))
h=index.read_text(encoding='utf-8')
MARK='War Room v1.7.28 - WoW-style race portrait pass v15'
if MARK in h:
    print('War Room WoW-style portraits v15 already installed')
    raise SystemExit(0)
block=r'''
<style id="wr-wow-portraits-v15-style">
/* War Room v1.7.28 - WoW-style race portrait pass v15 */
.race-portrait.wr-photo-portrait.wr-wow-portrait{width:62px!important;height:62px!important;min-width:62px!important;border-radius:50%!important;border:3px solid #b7833e!important;background:#090706!important;overflow:visible!important;box-shadow:0 0 0 1px #2d170b,0 0 0 2px rgba(229,190,103,.35),inset 0 0 0 2px rgba(255,222,144,.16),0 0 14px color-mix(in srgb,var(--class-accent,#9a6a45) 28%,transparent),0 5px 14px rgba(0,0,0,.55)!important}
.race-portrait.wr-photo-portrait.wr-wow-portrait:before{content:""!important;display:block!important;position:absolute;inset:3px;border-radius:50%;border:1px solid rgba(255,222,151,.36);pointer-events:none;z-index:3}
.race-portrait.wr-photo-portrait.wr-wow-portrait .race-photo{position:absolute;inset:4px;width:calc(100% - 8px);height:calc(100% - 8px);border-radius:50%;object-fit:cover;object-position:var(--portrait-position,50% 42%);filter:saturate(1.04) contrast(1.07) brightness(.97);background:#0a0807}
.race-portrait.wr-photo-portrait.wr-wow-portrait .race-photo-label{display:none!important}
.wr-wow-level-badge{position:absolute;right:-5px;bottom:-3px;z-index:5;min-width:20px;height:20px;padding:0 4px;border-radius:10px;border:1px solid #e1b85d;background:linear-gradient(180deg,#2b1a0d,#0e0906);color:#f4d878;display:grid;place-items:center;font:900 9px/1 Arial,sans-serif;text-shadow:0 1px 2px #000;box-shadow:0 1px 4px #000,inset 0 0 4px rgba(255,214,125,.16)}
.wr-wow-race-pip{position:absolute;left:-3px;bottom:-2px;z-index:5;width:17px;height:17px;border-radius:50%;border:1px solid #8d5a2d;background:#100b08;color:#d8b66f;display:grid;place-items:center;font-size:8px;font-weight:1000;text-shadow:0 1px 2px #000;box-shadow:0 1px 4px #000}
.wr-raid-race-photo.wr-wow-raid-portrait{width:34px!important;height:34px!important;min-width:34px!important;border-radius:50%!important;border:2px solid #a87339!important;outline:1px solid #2d180d;outline-offset:0;object-fit:cover;object-position:var(--portrait-position,50% 42%);box-shadow:0 0 9px color-mix(in srgb,var(--member-class,#a36c43) 35%,transparent),0 2px 6px #000!important;filter:saturate(1.04) contrast(1.06)}
</style>
<script id="wr-wow-portraits-v15-script">
/* War Room v1.7.28 - WoW-style race portrait pass v15 */
(function(){
  const raceKey=r=>String(r||'').toLowerCase().replace(/[^a-z]/g,'');
  const raceMap={
    orc:{remote:'https://wow.zamimg.com/uploads/screenshots/normal/924486.jpg',local:'assets/races/orc.svg',pos:'50% 42%',pip:'OR'},
    troll:{remote:'https://wow.zamimg.com/uploads/screenshots/normal/923458-troll-customization.jpg',local:'assets/races/troll.svg',pos:'50% 40%',pip:'TR'},
    tauren:{remote:'https://wow.zamimg.com/uploads/screenshots/normal/944337-tauren-male.jpg',local:'assets/races/tauren.svg',pos:'50% 44%',pip:'TA'},
    undead:{remote:'https://i.imgur.com/PvOjaQp.jpg',local:'assets/races/undead.svg',pos:'50% 31%',pip:'UD'},
    scourge:{remote:'https://i.imgur.com/PvOjaQp.jpg',local:'assets/races/undead.svg',pos:'50% 31%',pip:'UD'},
    bloodelf:{remote:'https://main.judgehype.com/images/news-bases/2018/376411-1522228314.jpg',local:'assets/races/bloodelf.svg',pos:'50% 42%',pip:'BE'}
  };
  const unknown={remote:'assets/races/unknown.svg',local:'assets/races/unknown.svg',pos:'50% 50%',pip:'?'};
  const cfg=p=>raceMap[raceKey(p?.race)]||unknown;
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const cls=p=>window.classColors?.[p?.class]||'#9a6a45';
  const lvl=p=>Number(p?.level)||70;
  function imgMarkup(p){
    const c=cfg(p),race=String(p?.race||'Unknown Race');
    return `<div class="race-portrait wr-photo-portrait wr-wow-portrait" style="--class-accent:${cls(p)};--portrait-position:${c.pos}" title="${esc(race)} • WoW-style base portrait"><img class="race-photo" referrerpolicy="no-referrer" src="${c.remote}" data-fallback="${c.local}" alt="${esc(race)} portrait" onerror="if(this.src.indexOf(this.dataset.fallback)<0){this.src=this.dataset.fallback}else{this.onerror=null}"><span class="wr-wow-race-pip">${c.pip}</span><span class="wr-wow-level-badge">${lvl(p)}</span></div>`;
  }
  try{window.racePortraitHTML=imgMarkup}catch(e){console.warn('[War Room] WoW portrait roster override unavailable',e)}
  function memberByName(name){try{return window.roster?.find?.(x=>x.name===name)||null}catch(e){return null}}
  function slotName(slot){const b=slot.querySelector('b');return b?String(b.textContent||'').trim():''}
  function upgradeRaidPortraits(){
    document.querySelectorAll('#builder .slot').forEach(slot=>{
      const p=memberByName(slotName(slot));if(!p)return;
      const img=slot.querySelector('.wr-raid-race-photo');if(!img)return;
      const c=cfg(p);img.classList.add('wr-wow-raid-portrait');img.referrerPolicy='no-referrer';img.src=c.remote;img.dataset.fallback=c.local;img.style.setProperty('--portrait-position',c.pos);img.onerror=function(){if(this.src.indexOf(this.dataset.fallback)<0)this.src=this.dataset.fallback;else this.onerror=null};
    });
  }
  try{
    if(typeof window.renderRaid==='function'){
      const prevRaid=window.renderRaid;
      window.renderRaid=function(){const r=prevRaid.apply(this,arguments);upgradeRaidPortraits();return r};
    }
    window.renderRoster?.();upgradeRaidPortraits();
    const root=document.getElementById('builder');if(root)new MutationObserver(()=>upgradeRaidPortraits()).observe(root,{childList:true,subtree:true});
  }catch(e){console.warn('[War Room] WoW portrait pass failed',e)}
})();
</script>
'''
needle='<!-- legacy QA markers:'
if needle in h:
    h=h.replace(needle,block+'\n'+needle,1)
elif '</body>' in h:
    h=h.replace('</body>',block+'\n</body>',1)
else:
    raise RuntimeError('body marker missing for WoW portrait pass')
index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 WoW-style race portraits v15 installed')
