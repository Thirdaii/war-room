from pathlib import Path
import sys

root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')

MARK='War Room v1.7.28 - Micro-quad additive rescue v4'
script=r'''<script>
/* War Room v1.7.28 - Micro-quad additive rescue v4 */
(function(){
  if(window.__wrMicroQuadRescueInstalled)return;
  window.__wrMicroQuadRescueInstalled=true;
  window.__wrMicroQuadRescueEnabled=true;
  window.__wrMicroQuadRescueStats={draws:0,candidates:0,rescued:0,last:null};
  const states=new WeakMap();
  function st(gl){let s=states.get(gl);if(!s){s={blend:false,cull:false,depthMask:true,srcRGB:null,dstRGB:null,srcAlpha:null,dstAlpha:null,eqRGB:null,eqAlpha:null};states.set(gl,s)}return s}
  function install(p){
    if(!p||p.__wrMicroQuadRescue)return;
    p.__wrMicroQuadRescue=true;
    const raw={enable:p.enable,disable:p.disable,depthMask:p.depthMask,blendFunc:p.blendFunc,blendFuncSeparate:p.blendFuncSeparate,blendEquation:p.blendEquation,blendEquationSeparate:p.blendEquationSeparate,drawElements:p.drawElements,drawArrays:p.drawArrays};
    if(typeof raw.enable==='function')p.enable=function(cap){try{const s=st(this);if(cap===this.BLEND)s.blend=true;if(cap===this.CULL_FACE)s.cull=true}catch(_e){}return raw.enable.apply(this,arguments)};
    if(typeof raw.disable==='function')p.disable=function(cap){try{const s=st(this);if(cap===this.BLEND)s.blend=false;if(cap===this.CULL_FACE)s.cull=false}catch(_e){}return raw.disable.apply(this,arguments)};
    if(typeof raw.depthMask==='function')p.depthMask=function(flag){try{st(this).depthMask=!!flag}catch(_e){}return raw.depthMask.apply(this,arguments)};
    if(typeof raw.blendFunc==='function')p.blendFunc=function(src,dst){try{const s=st(this);s.srcRGB=src;s.dstRGB=dst;s.srcAlpha=src;s.dstAlpha=dst}catch(_e){}return raw.blendFunc.apply(this,arguments)};
    if(typeof raw.blendFuncSeparate==='function')p.blendFuncSeparate=function(sr,dr,sa,da){try{const s=st(this);s.srcRGB=sr;s.dstRGB=dr;s.srcAlpha=sa;s.dstAlpha=da}catch(_e){}return raw.blendFuncSeparate.apply(this,arguments)};
    if(typeof raw.blendEquation==='function')p.blendEquation=function(eq){try{const s=st(this);s.eqRGB=eq;s.eqAlpha=eq}catch(_e){}return raw.blendEquation.apply(this,arguments)};
    if(typeof raw.blendEquationSeparate==='function')p.blendEquationSeparate=function(er,ea){try{const s=st(this);s.eqRGB=er;s.eqAlpha=ea}catch(_e){}return raw.blendEquationSeparate.apply(this,arguments)};
    function draw(original,args,kind){
      const s=st(this),stats=window.__wrMicroQuadRescueStats;stats.draws++;
      const mode=args[0];
      const count=Number(kind==='drawElements'?args[1]:args[2])||0;
      const triangleMode=mode===this.TRIANGLES||mode===this.TRIANGLE_STRIP||mode===this.TRIANGLE_FAN;
      const candidate=triangleMode && count>0 && count<=12;
      if(candidate)stats.candidates++;
      if(window.__wrMicroQuadRescueEnabled===false||!candidate)return original.apply(this,args);
      const old={blend:s.blend,cull:s.cull,depthMask:s.depthMask,srcRGB:s.srcRGB,dstRGB:s.dstRGB,srcAlpha:s.srcAlpha,dstAlpha:s.dstAlpha,eqRGB:s.eqRGB,eqAlpha:s.eqAlpha};
      try{
        raw.enable.call(this,this.BLEND);
        raw.depthMask.call(this,false);
        if(typeof raw.blendEquationSeparate==='function')raw.blendEquationSeparate.call(this,this.FUNC_ADD,this.FUNC_ADD);else raw.blendEquation.call(this,this.FUNC_ADD);
        if(typeof raw.blendFuncSeparate==='function')raw.blendFuncSeparate.call(this,this.ONE,this.ONE,this.ONE,this.ONE);else raw.blendFunc.call(this,this.ONE,this.ONE);
        stats.rescued++;stats.last={kind,count,mode,t:Math.round(performance.now()),old};
        return original.apply(this,args);
      } finally {
        if(old.srcRGB!=null){
          if(typeof raw.blendFuncSeparate==='function'&&old.srcAlpha!=null)raw.blendFuncSeparate.call(this,old.srcRGB,old.dstRGB,old.srcAlpha,old.dstAlpha);
          else raw.blendFunc.call(this,old.srcRGB,old.dstRGB);
        }
        if(old.eqRGB!=null){
          if(typeof raw.blendEquationSeparate==='function'&&old.eqAlpha!=null)raw.blendEquationSeparate.call(this,old.eqRGB,old.eqAlpha);
          else raw.blendEquation.call(this,old.eqRGB);
        }
        raw.depthMask.call(this,old.depthMask);
        if(old.blend)raw.enable.call(this,this.BLEND);else raw.disable.call(this,this.BLEND);
        s.blend=old.blend;s.depthMask=old.depthMask;s.srcRGB=old.srcRGB;s.dstRGB=old.dstRGB;s.srcAlpha=old.srcAlpha;s.dstAlpha=old.dstAlpha;s.eqRGB=old.eqRGB;s.eqAlpha=old.eqAlpha;
      }
    }
    if(typeof raw.drawElements==='function')p.drawElements=function(){return draw.call(this,raw.drawElements,arguments,'drawElements')};
    if(typeof raw.drawArrays==='function')p.drawArrays=function(){return draw.call(this,raw.drawArrays,arguments,'drawArrays')};
  }
  install(window.WebGLRenderingContext&&WebGLRenderingContext.prototype);
  install(window.WebGL2RenderingContext&&WebGL2RenderingContext.prototype);
  window.wrMicroQuadRescue=function(on){window.__wrMicroQuadRescueEnabled=on!==false;return {...window.__wrMicroQuadRescueStats,enabled:window.__wrMicroQuadRescueEnabled}};
  window.wrMicroQuadRescueReport=function(){return {...window.__wrMicroQuadRescueStats,enabled:window.__wrMicroQuadRescueEnabled}};
  console.info('[WarRoom Micro Quad Rescue v4] armed: <=12-vertex triangle batches forced additive for that draw only');
})();
</script>'''

if MARK not in h:
    if '</head>' not in h: raise RuntimeError('head marker missing for micro-quad rescue')
    h=h.replace('</head>',script+'\n</head>',1)
index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 micro-quad additive rescue v4 installed')
