from pathlib import Path
import sys
root=Path(sys.argv[1]); index=root/'index.html'; h=index.read_text(encoding='utf-8')
MARK='War Room v1.7.28 - Raid Layout Finish v19'
if MARK in h:
    print('V19 raid layout finish already installed'); raise SystemExit(0)
block=r'''
<style id="wr-raid-layout-finish-v19-style">
/* War Room v1.7.28 - Raid Layout Finish v19 */
#builder .slot.drop{outline:none!important}
body.wr-raid-drag-active #builder .slot.drop{outline:1px dashed rgba(190,126,65,.72)!important;outline-offset:-3px!important}
#builder .slot.empty{border-color:#2a211c!important;background:linear-gradient(90deg,rgba(255,255,255,.008),transparent)!important}
body.wr-raid-drag-active #builder .slot.empty{border-style:dashed!important;border-color:#5b3b29!important}
#builder .slot.empty:hover{border-color:#5f422f!important}
#builder .group-buffs{padding:5px 6px!important;border-top:1px solid #1e1713!important}
#builder .group-ready{min-height:26px!important;padding:4px 7px!important;border-top:1px solid #211914!important}
#builder .party-icon{opacity:.72;transition:opacity .1s ease,border-color .1s ease}
#builder .party-icon.active,#builder .party-icon:hover{opacity:1}
@media (min-width:1101px) and (max-width:1550px){
  #builder{grid-template-columns:repeat(6,minmax(0,1fr))!important}
  #builder>.group{grid-column:span 2!important}
  #builder>.group:nth-of-type(4){grid-column:2 / span 2!important}
  #builder>.group:nth-of-type(5){grid-column:4 / span 2!important}
}
</style>
<script id="wr-raid-layout-finish-v19-script">
/* War Room v1.7.28 - Raid Layout Finish v19 */
(function(){
  if(window.__wrRaidLayoutFinishV19)return;window.__wrRaidLayoutFinishV19=true;
  function finish(){
    const b=document.getElementById('builder');if(!b)return;
    b.querySelectorAll('.group[data-group]').forEach(group=>{
      const slots=[...group.querySelectorAll('.slot[data-slot]')];
      const assigned=slots.filter(x=>!x.classList.contains('empty')).length;
      const badge=group.querySelector('.gtitle>span:last-child');
      if(badge){badge.textContent=assigned===5?'5/5 READY':assigned+'/5 ASSIGNED';badge.title=assigned===5?'Group full':'Raiders assigned to this group'}
    });
  }
  try{if(typeof renderRaid==='function'){const prev=renderRaid;renderRaid=function(){const out=prev.apply(this,arguments);finish();return out}}}catch(e){console.warn('[War Room] V19 render hook failed',e)}
  finish();setTimeout(finish,120);setTimeout(finish,650);
  window.WarRoomRaidLayoutFinishV19={finish};
  console.info('[War Room v1.7.28] raid layout finish v19 active');
})();
</script>
'''
if '</body>' not in h: raise RuntimeError('body close marker missing')
h=h.replace('</body>',block+'\n</body>',1); index.write_text(h,encoding='utf-8'); print('War Room v1.7.28 raid layout finish v19 installed')
