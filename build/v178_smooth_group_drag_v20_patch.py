from pathlib import Path
import sys
root=Path(sys.argv[1]); index=root/'index.html'; h=index.read_text(encoding='utf-8')
MARK='War Room v1.7.28 - Smooth group drag v20'
if MARK in h:
    print('V20 smooth group drag already installed'); raise SystemExit(0)
repls=[
("""  function clearTargets(){\n    $$('#builder .slot').forEach(x=>x.classList.remove('wr-v17-target','wr-v17-swap','wr-slot-drop-ready','wr-slot-swap-ready','drag-over'));\n    $$('#builder .group').forEach(x=>x.classList.remove('wr-v17-group-target','wr-group-drop-ready'));\n    $('#wrRaidBenchDrop')?.classList.remove('wr-v17-roster-target','wr-bench-over');\n  }""",
"""  let painted={slot:null,group:null,roster:null,key:''};\n  function clearTargets(full=false){\n    painted.slot?.classList.remove('wr-v17-target','wr-v17-swap','wr-slot-drop-ready','wr-slot-swap-ready','drag-over');\n    painted.group?.classList.remove('wr-v17-group-target','wr-group-drop-ready');\n    painted.roster?.classList.remove('wr-v17-roster-target','wr-bench-over');\n    painted={slot:null,group:null,roster:null,key:''};\n    if(full){\n      $$('#builder .slot.wr-v17-target,#builder .slot.wr-v17-swap,#builder .slot.wr-slot-drop-ready,#builder .slot.wr-slot-swap-ready,#builder .slot.drag-over').forEach(x=>x.classList.remove('wr-v17-target','wr-v17-swap','wr-slot-drop-ready','wr-slot-swap-ready','drag-over'));\n      $$('#builder .group.wr-v17-group-target,#builder .group.wr-group-drop-ready').forEach(x=>x.classList.remove('wr-v17-group-target','wr-group-drop-ready'));\n      $('#wrRaidBenchDrop')?.classList.remove('wr-v17-roster-target','wr-bench-over');\n    }\n  }"""),
("document.body.appendChild(el);el.style.left=x+'px';el.style.top=y+'px';return el;","document.body.appendChild(el);el.style.left='0px';el.style.top='0px';el.style.transform='translate3d('+(x+14)+'px,'+(y+14)+'px,0)';return el;"),
("document.body.classList.add('wr-pointer-raid-dragging','wr-raid-drag-active');","clearTargets(true);document.body.classList.add('wr-pointer-raid-dragging','wr-v20-raid-dragging');"),
("""  function paintHit(hit){\n    clearTargets();\n    if(hit.kind==='slot'){\n      hit.el.classList.add('wr-v17-target');\n      if(raidNameAt(hit.slot)&&raidNameAt(hit.slot)!==drag?.name)hit.el.classList.add('wr-v17-swap');\n      hit.el.closest('.group')?.classList.add('wr-v17-group-target');\n    }else if(hit.kind==='group')hit.el.classList.add('wr-v17-group-target');\n    else if(hit.kind==='roster')hit.el?.classList.add('wr-v17-roster-target');\n  }""",
"""  function paintHit(hit){\n    const key=hit.kind==='slot'?'s'+hit.slot:hit.kind==='group'?'g'+hit.group:hit.kind==='roster'?'r':'none';\n    if(key===painted.key)return;\n    clearTargets(false);\n    if(hit.kind==='slot'){\n      const group=hit.el.closest('.group');\n      hit.el.classList.add('wr-v17-target');\n      if(raidNameAt(hit.slot)&&raidNameAt(hit.slot)!==drag?.name)hit.el.classList.add('wr-v17-swap');\n      group?.classList.add('wr-v17-group-target');\n      painted={slot:hit.el,group,roster:null,key};\n    }else if(hit.kind==='group'){\n      hit.el.classList.add('wr-v17-group-target');painted={slot:null,group:hit.el,roster:null,key};\n    }else if(hit.kind==='roster'){\n      hit.el?.classList.add('wr-v17-roster-target');painted={slot:null,group:null,roster:hit.el||null,key};\n    }else painted={slot:null,group:null,roster:null,key};\n  }"""),
("""  function cleanup(){\n    clearTargets();drag?.source?.classList.remove('wr-raid-dragging');drag?.ghost?.remove();\n    document.body.classList.remove('wr-pointer-raid-dragging','wr-raid-drag-active','wr-drag-from-raid');drag=null;disableNative();\n  }""",
"""  function cleanup(){\n    clearTargets(true);drag?.source?.classList.remove('wr-raid-dragging');drag?.ghost?.remove();\n    document.body.classList.remove('wr-pointer-raid-dragging','wr-v20-raid-dragging','wr-raid-drag-active','wr-drag-from-raid');drag=null;disableNative();\n  }"""),
("""  window.addEventListener('pointermove',e=>{\n    if(!drag||e.pointerId!==drag.pointerId)return;\n    const dx=e.clientX-drag.x,dy=e.clientY-drag.y;\n    if(!drag.active&&Math.hypot(dx,dy)>=6)beginDrag(e);\n    if(!drag.active)return;\n    e.preventDefault();if(drag.ghost){drag.ghost.style.left=e.clientX+'px';drag.ghost.style.top=e.clientY+'px'}\n    paintHit(hitAt(e.clientX,e.clientY));\n  },{capture:true,passive:false});""",
"""  let moveFrame=0,movePoint=null;\n  function flushMove(){\n    moveFrame=0;if(!drag||!drag.active||!movePoint)return;\n    const {x,y}=movePoint;movePoint=null;\n    if(drag.ghost)drag.ghost.style.transform='translate3d('+(x+14)+'px,'+(y+14)+'px,0)';\n    paintHit(hitAt(x,y));\n  }\n  window.addEventListener('pointermove',e=>{\n    if(!drag||e.pointerId!==drag.pointerId)return;\n    const dx=e.clientX-drag.x,dy=e.clientY-drag.y;\n    if(!drag.active&&Math.hypot(dx,dy)>=6)beginDrag(e);\n    if(!drag.active)return;\n    e.preventDefault();movePoint={x:e.clientX,y:e.clientY};if(!moveFrame)moveFrame=requestAnimationFrame(flushMove);\n  },{capture:true,passive:false});"""),
("clearTargets();d.source?.classList.remove('wr-raid-dragging');d.ghost?.remove();document.body.classList.remove('wr-pointer-raid-dragging','wr-raid-drag-active','wr-drag-from-raid');drag=null;","if(moveFrame){cancelAnimationFrame(moveFrame);moveFrame=0}movePoint=null;clearTargets(true);d.source?.classList.remove('wr-raid-dragging');d.ghost?.remove();document.body.classList.remove('wr-pointer-raid-dragging','wr-v20-raid-dragging','wr-raid-drag-active','wr-drag-from-raid');drag=null;")
]
for old,new in repls:
    if old not in h: raise RuntimeError('V20 anchor missing: '+old[:80])
    h=h.replace(old,new,1)
block=r'''
<style id="wr-smooth-group-drag-v20-style">
/* War Room v1.7.28 - Smooth group drag v20 */
body.wr-pointer-raid-dragging #builder .slot,body.wr-pointer-raid-dragging #builder .group,body.wr-pointer-raid-dragging #builder .party-icon{transition:none!important}
.wr-v17-drag-ghost{left:0!important;top:0!important;margin:0!important;transform:translate3d(-9999px,-9999px,0);will-change:transform;contain:layout paint style;box-shadow:0 7px 18px rgba(0,0,0,.48),inset 0 0 0 1px rgba(255,220,150,.05)!important}
body.wr-v20-raid-dragging #builder .slot.drop{outline:none!important}
body.wr-v20-raid-dragging #builder .slot.empty{border-style:solid!important;border-color:#2a211c!important}
body.wr-v20-raid-dragging #builder .group .wr-group-drop-caption{display:none!important}
body.wr-v20-raid-dragging #builder .group.wr-v17-group-target{outline:1px solid rgba(177,112,57,.68)!important;outline-offset:-2px!important;box-shadow:inset 0 0 0 1px rgba(204,139,76,.08)!important;transform:none!important}
body.wr-v20-raid-dragging #builder .slot.wr-v17-target{border-color:#b97b43!important;background:linear-gradient(90deg,rgba(92,46,26,.34),rgba(20,14,11,.98))!important;box-shadow:inset 0 0 0 1px rgba(225,170,96,.16)!important;transform:none!important}
body.wr-v20-raid-dragging #builder .slot.wr-v17-swap:after{opacity:.92}
</style>
<script id="wr-smooth-group-drag-v20-script">
/* War Room v1.7.28 - Smooth group drag v20 */
(function(){window.WarRoomSmoothGroupDragV20={version:20,frameThrottled:true,targetDiffing:true,bodyWideLighting:false};console.info('[War Room v1.7.28] smooth group drag v20 active')})();
</script>
'''
if '</body>' not in h: raise RuntimeError('body close marker missing')
h=h.replace('</body>',block+'\n</body>',1); index.write_text(h,encoding='utf-8'); print('War Room v1.7.28 smooth group drag v20 installed')
