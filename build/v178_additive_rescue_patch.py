from pathlib import Path
import sys

root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')

MARK='War Room v1.7.28 - Rectangle Hunter v7'
script=r'''<script>
/* War Room v1.7.28 - Rectangle Hunter v7 */
(function(){
  if(window.__wrRectangleHunterInstalled)return;
  window.__wrRectangleHunterInstalled=true;
  window.__wrDrawCensus=[];
  window.__wrDrawCensusMax=3000;
  window.__wrRectangleSkips=new Set();
  window.__wrRectangleHunterStats={draws:0,skipped:0,lastSkipped:null};
  const states=new WeakMap(),programIds=new WeakMap(); let nextProgramId=1;
  const enumNames={0:'ZERO',1:'ONE',4:'TRIANGLES',5:'TRIANGLE_STRIP',6:'TRIANGLE_FAN',768:'SRC_COLOR',769:'ONE_MINUS_SRC_COLOR',770:'SRC_ALPHA',771:'ONE_MINUS_SRC_ALPHA',772:'DST_ALPHA',773:'ONE_MINUS_DST_ALPHA',774:'DST_COLOR',775:'ONE_MINUS_DST_COLOR',32774:'FUNC_ADD',32778:'FUNC_SUBTRACT',32779:'FUNC_REVERSE_SUBTRACT'};
  const nm=v=>enumNames[v]||v;
  function st(gl){let s=states.get(gl);if(!s){s={blend:false,cull:false,depthMask:true,srcRGB:null,dstRGB:null,srcAlpha:null,dstAlpha:null,eqRGB:null,eqAlpha:null,program:0};states.set(gl,s)}return s}
  function pid(p){if(!p)return 0;let id=programIds.get(p);if(!id){id=nextProgramId++;programIds.set(p,id)}return id}
  function sigKey(s,kind,args){const mode=args[0],count=Number(kind==='drawElements'?args[1]:args[2])||0;return `${s.program}|${mode}|${count}`}
  function push(gl,kind,args,skipped){
    const s=st(gl),mode=args[0],count=Number(kind==='drawElements'?args[1]:args[2])||0;
    const row={t:Math.round(performance.now()),kind,mode,count,blend:s.blend,cull:s.cull,depthMask:s.depthMask,srcRGB:s.srcRGB,dstRGB:s.dstRGB,srcAlpha:s.srcAlpha,dstAlpha:s.dstAlpha,eqRGB:s.eqRGB,eqAlpha:s.eqAlpha,program:s.program,skipped:!!skipped};
    const a=window.__wrDrawCensus;a.push(row);if(a.length>window.__wrDrawCensusMax)a.shift();
  }
  function install(p){
    if(!p||p.__wrRectangleHunter)return;p.__wrRectangleHunter=true;
    const raw={enable:p.enable,disable:p.disable,depthMask:p.depthMask,blendFunc:p.blendFunc,blendFuncSeparate:p.blendFuncSeparate,blendEquation:p.blendEquation,blendEquationSeparate:p.blendEquationSeparate,useProgram:p.useProgram,drawElements:p.drawElements,drawArrays:p.drawArrays};
    if(typeof raw.enable==='function')p.enable=function(cap){try{const s=st(this);if(cap===this.BLEND)s.blend=true;if(cap===this.CULL_FACE)s.cull=true}catch(_e){}return raw.enable.apply(this,arguments)};
    if(typeof raw.disable==='function')p.disable=function(cap){try{const s=st(this);if(cap===this.BLEND)s.blend=false;if(cap===this.CULL_FACE)s.cull=false}catch(_e){}return raw.disable.apply(this,arguments)};
    if(typeof raw.depthMask==='function')p.depthMask=function(flag){try{st(this).depthMask=!!flag}catch(_e){}return raw.depthMask.apply(this,arguments)};
    if(typeof raw.blendFunc==='function')p.blendFunc=function(src,dst){try{const s=st(this);s.srcRGB=src;s.dstRGB=dst;s.srcAlpha=src;s.dstAlpha=dst}catch(_e){}return raw.blendFunc.apply(this,arguments)};
    if(typeof raw.blendFuncSeparate==='function')p.blendFuncSeparate=function(sr,dr,sa,da){try{const s=st(this);s.srcRGB=sr;s.dstRGB=dr;s.srcAlpha=sa;s.dstAlpha=da}catch(_e){}return raw.blendFuncSeparate.apply(this,arguments)};
    if(typeof raw.blendEquation==='function')p.blendEquation=function(eq){try{const s=st(this);s.eqRGB=eq;s.eqAlpha=eq}catch(_e){}return raw.blendEquation.apply(this,arguments)};
    if(typeof raw.blendEquationSeparate==='function')p.blendEquationSeparate=function(er,ea){try{const s=st(this);s.eqRGB=er;s.eqAlpha=ea}catch(_e){}return raw.blendEquationSeparate.apply(this,arguments)};
    if(typeof raw.useProgram==='function')p.useProgram=function(program){try{st(this).program=pid(program)}catch(_e){}return raw.useProgram.apply(this,arguments)};
    function draw(kind,original,args){
      const s=st(this),key=sigKey(s,kind,args),skip=window.__wrRectangleSkips.has(key);
      window.__wrRectangleHunterStats.draws++;
      if(skip){window.__wrRectangleHunterStats.skipped++;window.__wrRectangleHunterStats.lastSkipped={key,t:Math.round(performance.now())};}
      try{push(this,kind,args,skip)}catch(_e){}
      if(skip)return;
      return original.apply(this,args);
    }
    if(typeof raw.drawElements==='function')p.drawElements=function(){return draw.call(this,'drawElements',raw.drawElements,arguments)};
    if(typeof raw.drawArrays==='function')p.drawArrays=function(){return draw.call(this,'drawArrays',raw.drawArrays,arguments)};
  }
  install(window.WebGLRenderingContext&&WebGLRenderingContext.prototype);
  install(window.WebGL2RenderingContext&&WebGL2RenderingContext.prototype);
  window.wrDrawCensusSummary=function(){
    const groups=new Map();
    for(const r of window.__wrDrawCensus){const k=[r.program,nm(r.mode),r.count,r.blend?'B1':'B0',r.depthMask?'D1':'D0',r.cull?'C1':'C0',nm(r.srcRGB),nm(r.dstRGB),nm(r.eqRGB),r.skipped?'SKIP':'DRAW'].join('|');groups.set(k,(groups.get(k)||0)+1)}
    return [...groups.entries()].map(([signature,draws])=>({draws,signature})).sort((a,b)=>b.draws-a.draws);
  };
  window.wrDrawCensusLast=function(n){return window.__wrDrawCensus.slice(-Math.max(1,Math.min(500,Number(n)||100))).map(r=>({...r,mode:nm(r.mode),srcRGB:nm(r.srcRGB),dstRGB:nm(r.dstRGB),srcAlpha:nm(r.srcAlpha),dstAlpha:nm(r.dstAlpha),eqRGB:nm(r.eqRGB),eqAlpha:nm(r.eqAlpha)}))};
  window.wrDrawCensusText=function(){return JSON.stringify({hunter:{skips:[...window.__wrRectangleSkips],stats:window.__wrRectangleHunterStats},summary:window.wrDrawCensusSummary().slice(0,120),last:window.wrDrawCensusLast(240)},null,2)};
  const candidates=[
    {label:'PAIR A · P13 × 36',key:'13|4|36'},
    {label:'PAIR B · P13 × 1596',key:'13|4|1596'},
    {label:'P13 × 1494',key:'13|4|1494'},
    {label:'P13 × 462',key:'13|4|462'},
    {label:'P12 × 576',key:'12|4|576'},
    {label:'P11 × 96',key:'11|4|96'}
  ];
  function setBtnState(b,key){const on=window.__wrRectangleSkips.has(key);b.dataset.on=on?'1':'0';b.style.background=on?'#5b1717':'rgba(8,7,7,.92)';b.style.borderColor=on?'#d76a4a':'#6d5135';b.textContent=(on?'HIDDEN · ':'SHOW · ')+b.dataset.label;}
  function addPanel(){
    const stage=document.getElementById('wr-character-model-stage');if(!stage||stage.querySelector('.wr-rectangle-hunter'))return;
    const panel=document.createElement('div');panel.className='wr-rectangle-hunter';panel.style.cssText='position:absolute;z-index:40;left:8px;top:8px;width:170px;padding:7px;border:1px solid #6d5135;background:rgba(7,6,6,.92);box-shadow:0 4px 18px rgba(0,0,0,.45);font:700 8px Arial;color:#d4b47a;letter-spacing:.05em';
    const title=document.createElement('div');title.textContent='RECTANGLE HUNTER V7';title.style.cssText='font-size:9px;margin-bottom:6px;color:#e6c78b';panel.appendChild(title);
    const sub=document.createElement('div');sub.textContent='Toggle one candidate at a time.';sub.style.cssText='font-size:7px;color:#9f8d78;margin-bottom:6px';panel.appendChild(sub);
    for(const c of candidates){const b=document.createElement('button');b.type='button';b.dataset.label=c.label;b.style.cssText='display:block;width:100%;margin:3px 0;padding:5px 6px;border:1px solid #6d5135;color:#ead9b7;text-align:left;font:800 7px Arial;cursor:pointer';setBtnState(b,c.key);b.onclick=()=>{if(window.__wrRectangleSkips.has(c.key))window.__wrRectangleSkips.delete(c.key);else window.__wrRectangleSkips.add(c.key);setBtnState(b,c.key)};panel.appendChild(b)}
    const reset=document.createElement('button');reset.type='button';reset.textContent='RESET ALL';reset.style.cssText='display:block;width:100%;margin-top:6px;padding:5px;border:1px solid #8c653f;background:#241910;color:#e6c78b;font:800 7px Arial;cursor:pointer';reset.onclick=()=>{window.__wrRectangleSkips.clear();panel.querySelectorAll('button[data-label]').forEach(b=>{const c=candidates.find(x=>x.label===b.dataset.label);if(c)setBtnState(b,c.key)})};panel.appendChild(reset);
    const copy=document.createElement('button');copy.type='button';copy.textContent='COPY TRACE';copy.style.cssText=reset.style.cssText;copy.onclick=async()=>{const t=window.wrDrawCensusText();try{await navigator.clipboard.writeText(t);copy.textContent='TRACE COPIED';setTimeout(()=>copy.textContent='COPY TRACE',1200)}catch(e){console.info('[WarRoom Rectangle Hunter]',t);copy.textContent='TRACE IN CONSOLE'}};panel.appendChild(copy);
    stage.appendChild(panel);
  }
  new MutationObserver(addPanel).observe(document.documentElement,{subtree:true,childList:true});setTimeout(addPanel,500);setTimeout(addPanel,1800);
  console.info('[WarRoom Rectangle Hunter v7] installed. Rendering is original until a candidate is toggled HIDDEN.');
})();
</script>'''

if MARK not in h:
    if '</head>' not in h: raise RuntimeError('head marker missing for Rectangle Hunter')
    h=h.replace('</head>',script+'\n</head>',1)
index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 Rectangle Hunter v7 installed')
