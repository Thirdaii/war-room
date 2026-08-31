from pathlib import Path
import sys

root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')

MARK='War Room v1.7.28 - Small effect-plane additive rescue v3'
script=r'''<script>
/* War Room v1.7.28 - Small effect-plane additive rescue v3 */
(function(){
  if(window.__wrSmallPlaneRescueInstalled)return;
  window.__wrSmallPlaneRescueInstalled=true;
  window.__wrAlphaPlaneRescueEnabled=false;
  window.__wrSmallPlaneRescueEnabled=true;
  window.__wrSmallPlaneRescueStats={draws:0,candidates:0,rescued:0,last:null};
  const states=new WeakMap();
  function st(gl){let s=states.get(gl);if(!s){s={blend:false,depthMask:true,srcRGB:null,dstRGB:null,srcAlpha:null,dstAlpha:null};states.set(gl,s)}return s}
  function install(p){
    if(!p||p.__wrSmallPlaneRescue)return;
    p.__wrSmallPlaneRescue=true;
    const raw={enable:p.enable,disable:p.disable,depthMask:p.depthMask,blendFunc:p.blendFunc,blendFuncSeparate:p.blendFuncSeparate,drawElements:p.drawElements,drawArrays:p.drawArrays};
    if(typeof raw.enable==='function')p.enable=function(cap){try{if(cap===this.BLEND)st(this).blend=true}catch(_e){}return raw.enable.apply(this,arguments)};
    if(typeof raw.disable==='function')p.disable=function(cap){try{if(cap===this.BLEND)st(this).blend=false}catch(_e){}return raw.disable.apply(this,arguments)};
    if(typeof raw.depthMask==='function')p.depthMask=function(flag){try{st(this).depthMask=!!flag}catch(_e){}return raw.depthMask.apply(this,arguments)};
    if(typeof raw.blendFunc==='function')p.blendFunc=function(src,dst){try{const s=st(this);s.srcRGB=src;s.dstRGB=dst;s.srcAlpha=src;s.dstAlpha=dst}catch(_e){}return raw.blendFunc.apply(this,arguments)};
    if(typeof raw.blendFuncSeparate==='function')p.blendFuncSeparate=function(sr,dr,sa,da){try{const s=st(this);s.srcRGB=sr;s.dstRGB=dr;s.srcAlpha=sa;s.dstAlpha=da}catch(_e){}return raw.blendFuncSeparate.apply(this,arguments)};
    function draw(original,args,kind){
      const s=st(this),stats=window.__wrSmallPlaneRescueStats;stats.draws++;
      const mode=args[0];
      const count=Number(kind==='drawElements'?args[1]:args[2])||0;
      const triangleMode=mode===this.TRIANGLES||mode===this.TRIANGLE_STRIP||mode===this.TRIANGLE_FAN;
      const normalAlpha=s.blend && s.srcRGB===this.SRC_ALPHA && s.dstRGB===this.ONE_MINUS_SRC_ALPHA;
      const candidate=normalAlpha && s.depthMask===false && triangleMode && count>0 && count<=36;
      if(candidate)stats.candidates++;
      if(window.__wrSmallPlaneRescueEnabled===false||!candidate)return original.apply(this,args);
      const old=[s.srcRGB,s.dstRGB,s.srcAlpha,s.dstAlpha];
      try{
        raw.blendFuncSeparate.call(this,this.ONE,this.ONE,this.ONE,this.ONE);
        stats.rescued++;stats.last={kind,count,mode,t:Math.round(performance.now()),old:old.slice()};
        return original.apply(this,args);
      } finally {
        if(old[0]!=null){
          if(typeof raw.blendFuncSeparate==='function'&&old[2]!=null)raw.blendFuncSeparate.call(this,old[0],old[1],old[2],old[3]);
          else raw.blendFunc.call(this,old[0],old[1]);
        }
      }
    }
    if(typeof raw.drawElements==='function')p.drawElements=function(){return draw.call(this,raw.drawElements,arguments,'drawElements')};
    if(typeof raw.drawArrays==='function')p.drawArrays=function(){return draw.call(this,raw.drawArrays,arguments,'drawArrays')};
  }
  install(window.WebGLRenderingContext&&WebGLRenderingContext.prototype);
  install(window.WebGL2RenderingContext&&WebGL2RenderingContext.prototype);
  window.wrSmallPlaneRescue=function(on){window.__wrSmallPlaneRescueEnabled=on!==false;return {...window.__wrSmallPlaneRescueStats,enabled:window.__wrSmallPlaneRescueEnabled}};
  window.wrSmallPlaneRescueReport=function(){return {...window.__wrSmallPlaneRescueStats,enabled:window.__wrSmallPlaneRescueEnabled}};
  console.info('[WarRoom Small Plane Rescue v3] armed: small normal-alpha depth-write-off triangle batches -> ONE/ONE additive');
})();
</script>'''

if MARK not in h:
    if '</head>' not in h: raise RuntimeError('head marker missing for small-plane rescue')
    h=h.replace('</head>',script+'\n</head>',1)
index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 small effect-plane additive rescue v3 installed')
