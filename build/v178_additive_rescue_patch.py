from pathlib import Path
import sys

root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')

MARK='War Room v1.7.28 - Program14 additive alpha preserve v10'
script=r'''<script>
/* War Room v1.7.28 - Program14 additive alpha preserve v10 */
(function(){
  if(window.__wrP14AlphaFixInstalled)return;
  window.__wrP14AlphaFixInstalled=true;
  window.__wrP14AlphaFixEnabled=true;
  window.__wrP14AlphaFixStats={draws:0,candidates:0,fixed:0,last:null};
  const states=new WeakMap(),programIds=new WeakMap();let nextProgramId=1;
  function pid(p){if(!p)return 0;let id=programIds.get(p);if(!id){id=nextProgramId++;programIds.set(p,id)}return id}
  function st(gl){let s=states.get(gl);if(!s){s={program:0,blend:false,srcRGB:null,dstRGB:null,srcAlpha:null,dstAlpha:null};states.set(gl,s)}return s}
  function install(p){
    if(!p||p.__wrP14AlphaFix)return;p.__wrP14AlphaFix=true;
    const raw={enable:p.enable,disable:p.disable,blendFunc:p.blendFunc,blendFuncSeparate:p.blendFuncSeparate,useProgram:p.useProgram,drawElements:p.drawElements,drawArrays:p.drawArrays};
    if(typeof raw.enable==='function')p.enable=function(cap){try{if(cap===this.BLEND)st(this).blend=true}catch(_e){}return raw.enable.apply(this,arguments)};
    if(typeof raw.disable==='function')p.disable=function(cap){try{if(cap===this.BLEND)st(this).blend=false}catch(_e){}return raw.disable.apply(this,arguments)};
    if(typeof raw.blendFunc==='function')p.blendFunc=function(a,b){try{const s=st(this);s.srcRGB=a;s.dstRGB=b;s.srcAlpha=a;s.dstAlpha=b}catch(_e){}return raw.blendFunc.apply(this,arguments)};
    if(typeof raw.blendFuncSeparate==='function')p.blendFuncSeparate=function(a,b,c,d){try{const s=st(this);s.srcRGB=a;s.dstRGB=b;s.srcAlpha=c;s.dstAlpha=d}catch(_e){}return raw.blendFuncSeparate.apply(this,arguments)};
    if(typeof raw.useProgram==='function')p.useProgram=function(pr){try{st(this).program=pid(pr)}catch(_e){}return raw.useProgram.apply(this,arguments)};
    function draw(kind,original,args){
      const gl=this,s=st(gl),mode=args[0],count=Number(kind==='drawElements'?args[1]:args[2])||0,stats=window.__wrP14AlphaFixStats;stats.draws++;
      const candidate=s.program===14&&mode===gl.TRIANGLES&&count===48&&s.blend===true&&s.srcRGB===gl.SRC_ALPHA&&s.dstRGB===gl.ONE;
      if(candidate)stats.candidates++;
      if(!candidate||window.__wrP14AlphaFixEnabled===false||typeof raw.blendFuncSeparate!=='function')return original.apply(gl,args);
      const old={srcRGB:s.srcRGB,dstRGB:s.dstRGB,srcAlpha:s.srcAlpha,dstAlpha:s.dstAlpha};
      try{
        /* RGB stays exactly as Zam requested: SRC_ALPHA + ONE additive.
           Alpha is preserved from the destination so a black additive texel cannot
           turn a transparent canvas pixel into opaque black. */
        raw.blendFuncSeparate.call(gl,gl.SRC_ALPHA,gl.ONE,gl.ZERO,gl.ONE);
        stats.fixed++;stats.last={t:Math.round(performance.now()),program:s.program,count,old};
        return original.apply(gl,args);
      } finally {
        if(old.srcRGB!=null&&old.dstRGB!=null){
          if(old.srcAlpha!=null&&old.dstAlpha!=null)raw.blendFuncSeparate.call(gl,old.srcRGB,old.dstRGB,old.srcAlpha,old.dstAlpha);
          else if(typeof raw.blendFunc==='function')raw.blendFunc.call(gl,old.srcRGB,old.dstRGB);
        }
      }
    }
    if(typeof raw.drawElements==='function')p.drawElements=function(){return draw.call(this,'drawElements',raw.drawElements,arguments)};
    if(typeof raw.drawArrays==='function')p.drawArrays=function(){return draw.call(this,'drawArrays',raw.drawArrays,arguments)};
  }
  install(window.WebGLRenderingContext&&WebGLRenderingContext.prototype);
  install(window.WebGL2RenderingContext&&WebGL2RenderingContext.prototype);
  window.wrP14AlphaFixReport=function(){return {...window.__wrP14AlphaFixStats,enabled:window.__wrP14AlphaFixEnabled}};
  function addBadge(){const stage=document.getElementById('wr-character-model-stage');if(!stage||stage.querySelector('.wr-alpha-fix-v10'))return;const b=document.createElement('button');b.type='button';b.className='wr-alpha-fix-v10';b.textContent='ALPHA FIX V10 · ON';b.style.cssText='position:absolute;z-index:42;right:8px;top:8px;padding:5px 8px;border:1px solid #7b5938;background:rgba(7,6,6,.9);color:#e5c98f;font:800 7px Arial;letter-spacing:.06em;cursor:pointer';b.onclick=()=>{window.__wrP14AlphaFixEnabled=!window.__wrP14AlphaFixEnabled;b.textContent='ALPHA FIX V10 · '+(window.__wrP14AlphaFixEnabled?'ON':'OFF');b.style.borderColor=window.__wrP14AlphaFixEnabled?'#7b5938':'#7a2f2f'};stage.appendChild(b)}
  new MutationObserver(addBadge).observe(document.documentElement,{subtree:true,childList:true});setTimeout(addBadge,500);setTimeout(addBadge,1800);
  console.info('[WarRoom Alpha Fix v10] P14 x48 additive RGB preserved; destination alpha preserved. Toggle with the viewer badge or window.__wrP14AlphaFixEnabled.');
})();
</script>'''

if MARK not in h:
    if '</head>' not in h: raise RuntimeError('head marker missing for alpha preserve fix')
    h=h.replace('</head>',script+'\n</head>',1)
index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 program14 additive alpha preserve v10 installed')
