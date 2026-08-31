from pathlib import Path
import sys

root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')

MARK='War Room v1.7.28 - Animated additive family alpha mask v12'
script=r'''<script>
/* War Room v1.7.28 - Animated additive family alpha mask v12 */
(function(){
  if(window.__wrAnimatedAdditiveMaskInstalled)return;
  window.__wrAnimatedAdditiveMaskInstalled=true;
  window.__wrAnimatedAdditiveMaskEnabled=true;
  window.__wrAnimatedAdditiveMaskStats={draws:0,candidates:0,fixed:0,byCount:{},last:null};
  const states=new WeakMap();
  function st(gl){let s=states.get(gl);if(!s){s={blend:false,cull:false,depthMask:true,srcRGB:null,dstRGB:null,colorMask:[true,true,true,true]};states.set(gl,s)}return s}
  function install(p){
    if(!p||p.__wrAnimatedAdditiveMask)return;p.__wrAnimatedAdditiveMask=true;
    const raw={enable:p.enable,disable:p.disable,depthMask:p.depthMask,blendFunc:p.blendFunc,blendFuncSeparate:p.blendFuncSeparate,colorMask:p.colorMask,drawElements:p.drawElements,drawArrays:p.drawArrays};
    if(typeof raw.enable==='function')p.enable=function(cap){try{const s=st(this);if(cap===this.BLEND)s.blend=true;if(cap===this.CULL_FACE)s.cull=true}catch(_e){}return raw.enable.apply(this,arguments)};
    if(typeof raw.disable==='function')p.disable=function(cap){try{const s=st(this);if(cap===this.BLEND)s.blend=false;if(cap===this.CULL_FACE)s.cull=false}catch(_e){}return raw.disable.apply(this,arguments)};
    if(typeof raw.depthMask==='function')p.depthMask=function(v){try{st(this).depthMask=!!v}catch(_e){}return raw.depthMask.apply(this,arguments)};
    if(typeof raw.blendFunc==='function')p.blendFunc=function(a,b){try{const s=st(this);s.srcRGB=a;s.dstRGB=b}catch(_e){}return raw.blendFunc.apply(this,arguments)};
    if(typeof raw.blendFuncSeparate==='function')p.blendFuncSeparate=function(a,b,c,d){try{const s=st(this);s.srcRGB=a;s.dstRGB=b}catch(_e){}return raw.blendFuncSeparate.apply(this,arguments)};
    if(typeof raw.colorMask==='function')p.colorMask=function(r,g,b,a){try{st(this).colorMask=[!!r,!!g,!!b,!!a]}catch(_e){}return raw.colorMask.apply(this,arguments)};
    function draw(kind,original,args){
      const gl=this,s=st(gl),mode=args[0],count=Number(kind==='drawElements'?args[1]:args[2])||0,stats=window.__wrAnimatedAdditiveMaskStats;stats.draws++;
      const candidate=mode===gl.TRIANGLES&&s.blend===true&&s.cull===false&&s.depthMask===false&&s.srcRGB===gl.SRC_ALPHA&&s.dstRGB===gl.ONE;
      if(candidate){stats.candidates++;stats.byCount[count]=(stats.byCount[count]||0)+1}
      if(!candidate||window.__wrAnimatedAdditiveMaskEnabled===false||typeof raw.colorMask!=='function')return original.apply(gl,args);
      const old=s.colorMask.slice();
      try{
        raw.colorMask.call(gl,old[0],old[1],old[2],false);
        stats.fixed++;stats.last={t:Math.round(performance.now()),kind,count,oldColorMask:old};
        return original.apply(gl,args);
      } finally {
        raw.colorMask.call(gl,old[0],old[1],old[2],old[3]);
        s.colorMask=old;
      }
    }
    if(typeof raw.drawElements==='function')p.drawElements=function(){return draw.call(this,'drawElements',raw.drawElements,arguments)};
    if(typeof raw.drawArrays==='function')p.drawArrays=function(){return draw.call(this,'drawArrays',raw.drawArrays,arguments)};
  }
  install(window.WebGLRenderingContext&&WebGLRenderingContext.prototype);
  install(window.WebGL2RenderingContext&&WebGL2RenderingContext.prototype);
  window.wrAnimatedAdditiveMaskReport=function(){return {...window.__wrAnimatedAdditiveMaskStats,enabled:window.__wrAnimatedAdditiveMaskEnabled}};
  function addBadge(){
    const stage=document.getElementById('wr-character-model-stage');if(!stage||stage.querySelector('.wr-alpha-mask-fix-v12'))return;
    const b=document.createElement('button');b.type='button';b.className='wr-alpha-mask-fix-v12';
    b.style.cssText='position:absolute;z-index:42;right:8px;top:8px;padding:5px 8px;border:1px solid #7b5938;background:rgba(7,6,6,.9);color:#e5c98f;font:800 7px Arial;letter-spacing:.06em;cursor:pointer';
    function refresh(){const s=window.__wrAnimatedAdditiveMaskStats;const kinds=Object.keys(s.byCount).length;b.textContent='FLAME ALPHA V12 · '+(window.__wrAnimatedAdditiveMaskEnabled?'ON':'OFF')+' · '+s.fixed+' HITS / '+kinds+' SIZES'}
    b.onclick=()=>{window.__wrAnimatedAdditiveMaskEnabled=!window.__wrAnimatedAdditiveMaskEnabled;refresh()};
    stage.appendChild(b);refresh();setInterval(refresh,500);
  }
  new MutationObserver(addPanel=>addBadge()).observe(document.documentElement,{subtree:true,childList:true});setTimeout(addBadge,500);setTimeout(addBadge,1800);
  console.info('[WarRoom Flame Alpha v12] alpha masked for full SRC_ALPHA/ONE no-depth/no-cull animated additive family regardless of index count.');
})();
</script>'''

if MARK not in h:
    if '</head>' not in h: raise RuntimeError('head marker missing for animated additive alpha mask')
    h=h.replace('</head>',script+'\n</head>',1)
index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 animated additive family alpha mask v12 installed')
