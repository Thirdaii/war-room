from pathlib import Path
import sys

root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')

MARK='War Room v1.7.28 - Additive alpha write-mask fix v11'
script=r'''<script>
/* War Room v1.7.28 - Additive alpha write-mask fix v11 */
(function(){
  if(window.__wrAdditiveMaskFixInstalled)return;
  window.__wrAdditiveMaskFixInstalled=true;
  window.__wrAdditiveMaskFixEnabled=true;
  window.__wrAdditiveMaskFixStats={draws:0,candidates:0,fixed:0,last:null};
  const states=new WeakMap();
  function st(gl){let s=states.get(gl);if(!s){s={blend:false,cull:false,depthMask:true,srcRGB:null,dstRGB:null,colorMask:[true,true,true,true]};states.set(gl,s)}return s}
  function install(p){
    if(!p||p.__wrAdditiveMaskFix)return;p.__wrAdditiveMaskFix=true;
    const raw={enable:p.enable,disable:p.disable,depthMask:p.depthMask,blendFunc:p.blendFunc,blendFuncSeparate:p.blendFuncSeparate,colorMask:p.colorMask,drawElements:p.drawElements,drawArrays:p.drawArrays};
    if(typeof raw.enable==='function')p.enable=function(cap){try{const s=st(this);if(cap===this.BLEND)s.blend=true;if(cap===this.CULL_FACE)s.cull=true}catch(_e){}return raw.enable.apply(this,arguments)};
    if(typeof raw.disable==='function')p.disable=function(cap){try{const s=st(this);if(cap===this.BLEND)s.blend=false;if(cap===this.CULL_FACE)s.cull=false}catch(_e){}return raw.disable.apply(this,arguments)};
    if(typeof raw.depthMask==='function')p.depthMask=function(v){try{st(this).depthMask=!!v}catch(_e){}return raw.depthMask.apply(this,arguments)};
    if(typeof raw.blendFunc==='function')p.blendFunc=function(a,b){try{const s=st(this);s.srcRGB=a;s.dstRGB=b}catch(_e){}return raw.blendFunc.apply(this,arguments)};
    if(typeof raw.blendFuncSeparate==='function')p.blendFuncSeparate=function(a,b,c,d){try{const s=st(this);s.srcRGB=a;s.dstRGB=b}catch(_e){}return raw.blendFuncSeparate.apply(this,arguments)};
    if(typeof raw.colorMask==='function')p.colorMask=function(r,g,b,a){try{st(this).colorMask=[!!r,!!g,!!b,!!a]}catch(_e){}return raw.colorMask.apply(this,arguments)};
    function draw(kind,original,args){
      const gl=this,s=st(gl),mode=args[0],count=Number(kind==='drawElements'?args[1]:args[2])||0,stats=window.__wrAdditiveMaskFixStats;stats.draws++;
      const candidate=mode===gl.TRIANGLES&&count===48&&s.blend===true&&s.cull===false&&s.depthMask===false&&s.srcRGB===gl.SRC_ALPHA&&s.dstRGB===gl.ONE;
      if(candidate)stats.candidates++;
      if(!candidate||window.__wrAdditiveMaskFixEnabled===false||typeof raw.colorMask!=='function')return original.apply(gl,args);
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
  window.wrAdditiveMaskFixReport=function(){return {...window.__wrAdditiveMaskFixStats,enabled:window.__wrAdditiveMaskFixEnabled}};
  function addBadge(){
    const stage=document.getElementById('wr-character-model-stage');if(!stage||stage.querySelector('.wr-alpha-mask-fix-v11'))return;
    const b=document.createElement('button');b.type='button';b.className='wr-alpha-mask-fix-v11';
    b.style.cssText='position:absolute;z-index:42;right:8px;top:8px;padding:5px 8px;border:1px solid #7b5938;background:rgba(7,6,6,.9);color:#e5c98f;font:800 7px Arial;letter-spacing:.06em;cursor:pointer';
    function refresh(){const s=window.__wrAdditiveMaskFixStats;b.textContent='ALPHA MASK V11 · '+(window.__wrAdditiveMaskFixEnabled?'ON':'OFF')+' · '+s.fixed+' HITS';}
    b.onclick=()=>{window.__wrAdditiveMaskFixEnabled=!window.__wrAdditiveMaskFixEnabled;refresh()};
    stage.appendChild(b);refresh();setInterval(refresh,500);
  }
  new MutationObserver(addBadge).observe(document.documentElement,{subtree:true,childList:true});setTimeout(addBadge,500);setTimeout(addBadge,1800);
  console.info('[WarRoom Alpha Mask v11] exact additive 48-index state matched without program IDs; RGB writes allowed, alpha writes masked.');
})();
</script>'''

if MARK not in h:
    if '</head>' not in h: raise RuntimeError('head marker missing for alpha write-mask fix')
    h=h.replace('</head>',script+'\n</head>',1)
index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 additive alpha write-mask fix v11 installed')
