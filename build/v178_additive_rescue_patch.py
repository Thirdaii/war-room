from pathlib import Path
import sys

root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')

MARK='War Room v1.7.28 - Final animated additive alpha mask v13'
script=r'''<script>
/* War Room v1.7.28 - Final animated additive alpha mask v13 */
(function(){
  if(window.__wrAnimatedAdditiveMaskInstalled)return;
  window.__wrAnimatedAdditiveMaskInstalled=true;
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
      const gl=this,s=st(gl),mode=args[0];
      const flamePass=mode===gl.TRIANGLES&&s.blend===true&&s.cull===false&&s.depthMask===false&&s.srcRGB===gl.SRC_ALPHA&&s.dstRGB===gl.ONE;
      if(!flamePass||typeof raw.colorMask!=='function')return original.apply(gl,args);
      const old=s.colorMask.slice();
      try{
        /* WoW additive flame/glow boards should contribute RGB only here.
           Preserve destination alpha so black texels cannot become opaque quads. */
        raw.colorMask.call(gl,old[0],old[1],old[2],false);
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
  console.info('[WarRoom v1.7.28] animated additive flame alpha-mask fix active');
})();
</script>'''

if MARK not in h:
    if '</head>' not in h: raise RuntimeError('head marker missing for final animated additive alpha mask')
    h=h.replace('</head>',script+'\n</head>',1)
index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 final animated additive alpha mask v13 installed')
