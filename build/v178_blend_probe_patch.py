from pathlib import Path
import sys

# Diagnostic-only probe for the Zam live viewer. This does NOT alter pixels,
# equipment IDs, model lifecycle, or WebGL blend state. It records blend state
# transitions so the rectangle artifact can be tied to the exact draw path
# before we make a surgical renderer patch.
root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')

probe=r'''<script>
(function(){
  if(window.__wrBlendProbeInstalled)return;
  window.__wrBlendProbeInstalled=true;
  window.__wrBlendEvents=[];
  const push=(kind,args)=>{
    const row={t:Math.round(performance.now()),kind,args:Array.from(args||[])};
    window.__wrBlendEvents.push(row);
    if(window.__wrBlendEvents.length>600)window.__wrBlendEvents.shift();
  };
  const proto=window.WebGLRenderingContext&&WebGLRenderingContext.prototype;
  const proto2=window.WebGL2RenderingContext&&WebGL2RenderingContext.prototype;
  for(const p of [proto,proto2]){
    if(!p||p.__wrBlendProbe)continue;
    p.__wrBlendProbe=true;
    for(const name of ['enable','disable','blendFunc','blendFuncSeparate','blendEquation','blendEquationSeparate','depthMask']){
      const original=p[name]; if(typeof original!=='function')continue;
      p[name]=function(...args){
        try{
          if(name==='enable'||name==='disable'){
            if(args[0]===this.BLEND||args[0]===this.DEPTH_TEST||args[0]===this.CULL_FACE)push(name,args);
          }else push(name,args);
        }catch(_e){}
        return original.apply(this,args);
      };
    }
  }
  window.wrBlendReport=()=>{
    const names={0:'ZERO',1:'ONE',768:'SRC_COLOR',769:'ONE_MINUS_SRC_COLOR',770:'SRC_ALPHA',771:'ONE_MINUS_SRC_ALPHA',772:'DST_ALPHA',773:'ONE_MINUS_DST_ALPHA',774:'DST_COLOR',775:'ONE_MINUS_DST_COLOR',32769:'CONSTANT_COLOR',32770:'ONE_MINUS_CONSTANT_COLOR',32771:'CONSTANT_ALPHA',32772:'ONE_MINUS_CONSTANT_ALPHA'};
    return window.__wrBlendEvents.map(e=>({...e,args:e.args.map(v=>names[v]||v)}));
  };
  console.info('[WarRoom Blend Probe] installed; call wrBlendReport() for decoded state history');
})();
</script>'''

if 'WarRoom Blend Probe' not in h:
    # Install before the application scripts execute so Zam's GL calls are seen.
    marker='</head>'
    if marker not in h: raise RuntimeError('head marker missing for blend probe')
    h=h.replace(marker,probe+'\n'+marker,1)

index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 blend-state diagnostic probe enabled (no render-state mutation)')
