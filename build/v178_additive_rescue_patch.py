from pathlib import Path
import sys

root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')

MARK='War Room v1.7.28 - Additive effect-plane rescue'
script=r'''<script>
/* War Room v1.7.28 - Additive effect-plane rescue */
(function(){
  if(window.__wrAdditiveRescueInstalled)return;
  window.__wrAdditiveRescueInstalled=true;
  window.__wrAdditiveRescueEnabled=true;
  window.__wrAdditiveRescueStats={rescued:0,draws:0,last:null};
  const states=new WeakMap();
  function state(gl){let s=states.get(gl);if(!s){s={blend:false,depthMask:true};states.set(gl,s)}return s}
  function install(p){
    if(!p||p.__wrAdditiveRescue)return;
    p.__wrAdditiveRescue=true;
    const enable=p.enable,disable=p.disable,depthMask=p.depthMask,drawElements=p.drawElements,drawArrays=p.drawArrays;
    if(typeof enable==='function')p.enable=function(cap){try{if(cap===this.BLEND)state(this).blend=true}catch(_e){}return enable.apply(this,arguments)};
    if(typeof disable==='function')p.disable=function(cap){try{if(cap===this.BLEND)state(this).blend=false}catch(_e){}return disable.apply(this,arguments)};
    if(typeof depthMask==='function')p.depthMask=function(flag){try{state(this).depthMask=!!flag}catch(_e){}return depthMask.apply(this,arguments)};
    function rescueDraw(original,args,kind){
      const s=state(this);window.__wrAdditiveRescueStats.draws++;
      const rescue=window.__wrAdditiveRescueEnabled!==false && s.depthMask===false && s.blend===false;
      if(!rescue)return original.apply(this,args);
      try{
        enable.call(this,this.BLEND);
        this.blendEquation(this.FUNC_ADD);
        this.blendFunc(this.ONE,this.ONE);
        window.__wrAdditiveRescueStats.rescued++;
        window.__wrAdditiveRescueStats.last={kind,t:Math.round(performance.now())};
        return original.apply(this,args);
      } finally {
        disable.call(this,this.BLEND);
        s.blend=false;
      }
    }
    if(typeof drawElements==='function')p.drawElements=function(){return rescueDraw.call(this,drawElements,arguments,'drawElements')};
    if(typeof drawArrays==='function')p.drawArrays=function(){return rescueDraw.call(this,drawArrays,arguments,'drawArrays')};
  }
  install(window.WebGLRenderingContext&&WebGLRenderingContext.prototype);
  install(window.WebGL2RenderingContext&&WebGL2RenderingContext.prototype);
  window.wrAdditiveRescue=function(on){window.__wrAdditiveRescueEnabled=on!==false;return {...window.__wrAdditiveRescueStats,enabled:window.__wrAdditiveRescueEnabled}};
  window.wrAdditiveRescueReport=function(){return {...window.__wrAdditiveRescueStats,enabled:window.__wrAdditiveRescueEnabled}};
  console.info('[WarRoom Additive Rescue] armed: only depth-write-off draws with BLEND disabled are converted to ONE/ONE additive for that draw');
})();
</script>'''

if MARK not in h:
    if '</head>' not in h: raise RuntimeError('head marker missing for additive rescue')
    h=h.replace('</head>',script+'\n</head>',1)
index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 additive effect-plane rescue installed (surgical depthMask=false + BLEND-off draws only)')
