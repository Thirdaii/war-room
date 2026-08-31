from pathlib import Path
import sys

root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')

MARK='War Room v1.7.28 - Non-mutating WebGL draw census v5'
script=r'''<script>
/* War Room v1.7.28 - Non-mutating WebGL draw census v5 */
(function(){
  if(window.__wrDrawCensusInstalled)return;
  window.__wrDrawCensusInstalled=true;
  window.__wrDrawCensus=[];
  window.__wrDrawCensusMax=3000;
  const states=new WeakMap(),programIds=new WeakMap(); let nextProgramId=1;
  const enumNames={0:'ZERO',1:'ONE',4:'TRIANGLES',5:'TRIANGLE_STRIP',6:'TRIANGLE_FAN',768:'SRC_COLOR',769:'ONE_MINUS_SRC_COLOR',770:'SRC_ALPHA',771:'ONE_MINUS_SRC_ALPHA',772:'DST_ALPHA',773:'ONE_MINUS_DST_ALPHA',774:'DST_COLOR',775:'ONE_MINUS_DST_COLOR',32774:'FUNC_ADD',32778:'FUNC_SUBTRACT',32779:'FUNC_REVERSE_SUBTRACT'};
  const nm=v=>enumNames[v]||v;
  function st(gl){let s=states.get(gl);if(!s){s={blend:false,cull:false,depthMask:true,srcRGB:null,dstRGB:null,srcAlpha:null,dstAlpha:null,eqRGB:null,eqAlpha:null,program:0};states.set(gl,s)}return s}
  function pid(p){if(!p)return 0;let id=programIds.get(p);if(!id){id=nextProgramId++;programIds.set(p,id)}return id}
  function push(gl,kind,args){
    const s=st(gl),mode=args[0],count=Number(kind==='drawElements'?args[1]:args[2])||0;
    const row={t:Math.round(performance.now()),kind,mode,count,blend:s.blend,cull:s.cull,depthMask:s.depthMask,srcRGB:s.srcRGB,dstRGB:s.dstRGB,srcAlpha:s.srcAlpha,dstAlpha:s.dstAlpha,eqRGB:s.eqRGB,eqAlpha:s.eqAlpha,program:s.program};
    const a=window.__wrDrawCensus;a.push(row);if(a.length>window.__wrDrawCensusMax)a.shift();
  }
  function install(p){
    if(!p||p.__wrDrawCensus)return;p.__wrDrawCensus=true;
    const raw={enable:p.enable,disable:p.disable,depthMask:p.depthMask,blendFunc:p.blendFunc,blendFuncSeparate:p.blendFuncSeparate,blendEquation:p.blendEquation,blendEquationSeparate:p.blendEquationSeparate,useProgram:p.useProgram,drawElements:p.drawElements,drawArrays:p.drawArrays};
    if(typeof raw.enable==='function')p.enable=function(cap){try{const s=st(this);if(cap===this.BLEND)s.blend=true;if(cap===this.CULL_FACE)s.cull=true}catch(_e){}return raw.enable.apply(this,arguments)};
    if(typeof raw.disable==='function')p.disable=function(cap){try{const s=st(this);if(cap===this.BLEND)s.blend=false;if(cap===this.CULL_FACE)s.cull=false}catch(_e){}return raw.disable.apply(this,arguments)};
    if(typeof raw.depthMask==='function')p.depthMask=function(flag){try{st(this).depthMask=!!flag}catch(_e){}return raw.depthMask.apply(this,arguments)};
    if(typeof raw.blendFunc==='function')p.blendFunc=function(src,dst){try{const s=st(this);s.srcRGB=src;s.dstRGB=dst;s.srcAlpha=src;s.dstAlpha=dst}catch(_e){}return raw.blendFunc.apply(this,arguments)};
    if(typeof raw.blendFuncSeparate==='function')p.blendFuncSeparate=function(sr,dr,sa,da){try{const s=st(this);s.srcRGB=sr;s.dstRGB=dr;s.srcAlpha=sa;s.dstAlpha=da}catch(_e){}return raw.blendFuncSeparate.apply(this,arguments)};
    if(typeof raw.blendEquation==='function')p.blendEquation=function(eq){try{const s=st(this);s.eqRGB=eq;s.eqAlpha=eq}catch(_e){}return raw.blendEquation.apply(this,arguments)};
    if(typeof raw.blendEquationSeparate==='function')p.blendEquationSeparate=function(er,ea){try{const s=st(this);s.eqRGB=er;s.eqAlpha=ea}catch(_e){}return raw.blendEquationSeparate.apply(this,arguments)};
    if(typeof raw.useProgram==='function')p.useProgram=function(program){try{st(this).program=pid(program)}catch(_e){}return raw.useProgram.apply(this,arguments)};
    if(typeof raw.drawElements==='function')p.drawElements=function(){try{push(this,'drawElements',arguments)}catch(_e){}return raw.drawElements.apply(this,arguments)};
    if(typeof raw.drawArrays==='function')p.drawArrays=function(){try{push(this,'drawArrays',arguments)}catch(_e){}return raw.drawArrays.apply(this,arguments)};
  }
  install(window.WebGLRenderingContext&&WebGLRenderingContext.prototype);
  install(window.WebGL2RenderingContext&&WebGL2RenderingContext.prototype);
  window.wrDrawCensusSummary=function(){
    const groups=new Map();
    for(const r of window.__wrDrawCensus){const k=[r.program,nm(r.mode),r.count,r.blend?'B1':'B0',r.depthMask?'D1':'D0',r.cull?'C1':'C0',nm(r.srcRGB),nm(r.dstRGB),nm(r.eqRGB)].join('|');groups.set(k,(groups.get(k)||0)+1)}
    return [...groups.entries()].map(([signature,draws])=>({draws,signature})).sort((a,b)=>b.draws-a.draws);
  };
  window.wrDrawCensusLast=function(n){return window.__wrDrawCensus.slice(-Math.max(1,Math.min(500,Number(n)||100))).map(r=>({...r,mode:nm(r.mode),srcRGB:nm(r.srcRGB),dstRGB:nm(r.dstRGB),srcAlpha:nm(r.srcAlpha),dstAlpha:nm(r.dstAlpha),eqRGB:nm(r.eqRGB),eqAlpha:nm(r.eqAlpha)}))};
  window.wrDrawCensusText=function(){return JSON.stringify({summary:window.wrDrawCensusSummary().slice(0,120),last:window.wrDrawCensusLast(240)},null,2)};
  function addButton(){const stage=document.getElementById('wr-character-model-stage');if(!stage||stage.querySelector('.wr-copy-render-trace'))return;const b=document.createElement('button');b.type='button';b.className='wr-copy-render-trace';b.textContent='COPY RENDER TRACE';b.style.cssText='position:absolute;z-index:30;right:8px;top:8px;padding:5px 8px;border:1px solid #6d5135;background:rgba(8,7,7,.88);color:#d4b47a;font:800 8px Arial;letter-spacing:.08em;cursor:pointer';b.onclick=async()=>{const t=window.wrDrawCensusText();try{await navigator.clipboard.writeText(t);b.textContent='TRACE COPIED';setTimeout(()=>b.textContent='COPY RENDER TRACE',1500)}catch(e){console.info('[WarRoom Draw Census]',t);b.textContent='TRACE IN CONSOLE'}};stage.appendChild(b)}
  new MutationObserver(addButton).observe(document.documentElement,{subtree:true,childList:true});setTimeout(addButton,500);setTimeout(addButton,1800);
  console.info('[WarRoom Draw Census v5] installed; rendering is untouched. Use wrDrawCensusSummary(), wrDrawCensusLast(), or COPY RENDER TRACE.');
})();
</script>'''

if MARK not in h:
    if '</head>' not in h: raise RuntimeError('head marker missing for draw census')
    h=h.replace('</head>',script+'\n</head>',1)
index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 non-mutating WebGL draw census v5 installed')
