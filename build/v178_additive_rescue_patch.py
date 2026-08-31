from pathlib import Path
import sys

root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')

MARK='War Room v1.7.28 - Shoulder Material Lab v8'
script=r'''<script>
/* War Room v1.7.28 - Shoulder Material Lab v8 */
(function(){
  if(window.__wrShoulderLabInstalled)return;
  window.__wrShoulderLabInstalled=true;
  window.__wrShoulderMode='normal';
  window.__wrShoulderLabStats={draws:0,targetDraws:0,modified:0,skipped:0,last:null};
  const states=new WeakMap(),programIds=new WeakMap(); let nextProgramId=1;
  function st(gl){let s=states.get(gl);if(!s){s={blend:false,cull:false,depthMask:true,srcRGB:null,dstRGB:null,srcAlpha:null,dstAlpha:null,eqRGB:null,eqAlpha:null,program:0};states.set(gl,s)}return s}
  function pid(p){if(!p)return 0;let id=programIds.get(p);if(!id){id=nextProgramId++;programIds.set(p,id)}return id}
  function install(p){
    if(!p||p.__wrShoulderLab)return;p.__wrShoulderLab=true;
    const raw={enable:p.enable,disable:p.disable,depthMask:p.depthMask,blendFunc:p.blendFunc,blendFuncSeparate:p.blendFuncSeparate,blendEquation:p.blendEquation,blendEquationSeparate:p.blendEquationSeparate,useProgram:p.useProgram,drawElements:p.drawElements};
    if(typeof raw.enable==='function')p.enable=function(cap){try{const s=st(this);if(cap===this.BLEND)s.blend=true;if(cap===this.CULL_FACE)s.cull=true}catch(_e){}return raw.enable.apply(this,arguments)};
    if(typeof raw.disable==='function')p.disable=function(cap){try{const s=st(this);if(cap===this.BLEND)s.blend=false;if(cap===this.CULL_FACE)s.cull=false}catch(_e){}return raw.disable.apply(this,arguments)};
    if(typeof raw.depthMask==='function')p.depthMask=function(flag){try{st(this).depthMask=!!flag}catch(_e){}return raw.depthMask.apply(this,arguments)};
    if(typeof raw.blendFunc==='function')p.blendFunc=function(src,dst){try{const s=st(this);s.srcRGB=src;s.dstRGB=dst;s.srcAlpha=src;s.dstAlpha=dst}catch(_e){}return raw.blendFunc.apply(this,arguments)};
    if(typeof raw.blendFuncSeparate==='function')p.blendFuncSeparate=function(sr,dr,sa,da){try{const s=st(this);s.srcRGB=sr;s.dstRGB=dr;s.srcAlpha=sa;s.dstAlpha=da}catch(_e){}return raw.blendFuncSeparate.apply(this,arguments)};
    if(typeof raw.blendEquation==='function')p.blendEquation=function(eq){try{const s=st(this);s.eqRGB=eq;s.eqAlpha=eq}catch(_e){}return raw.blendEquation.apply(this,arguments)};
    if(typeof raw.blendEquationSeparate==='function')p.blendEquationSeparate=function(er,ea){try{const s=st(this);s.eqRGB=er;s.eqAlpha=ea}catch(_e){}return raw.blendEquationSeparate.apply(this,arguments)};
    if(typeof raw.useProgram==='function')p.useProgram=function(program){try{st(this).program=pid(program)}catch(_e){}return raw.useProgram.apply(this,arguments)};
    if(typeof raw.drawElements!=='function')return;
    p.drawElements=function(mode,count,type,offset){
      const s=st(this),stats=window.__wrShoulderLabStats;stats.draws++;
      const target=s.program===13&&mode===this.TRIANGLES&&Number(count)===1596;
      if(!target||window.__wrShoulderMode==='normal')return raw.drawElements.apply(this,arguments);
      stats.targetDraws++;
      const chosen=window.__wrShoulderMode;
      if(chosen==='skip'){stats.skipped++;stats.last={t:Math.round(performance.now()),mode:chosen};return;}
      const old={blend:s.blend,depthMask:s.depthMask,srcRGB:s.srcRGB,dstRGB:s.dstRGB,srcAlpha:s.srcAlpha,dstAlpha:s.dstAlpha,eqRGB:s.eqRGB,eqAlpha:s.eqAlpha};
      try{
        raw.enable.call(this,this.BLEND);
        raw.depthMask.call(this,false);
        if(typeof raw.blendEquationSeparate==='function')raw.blendEquationSeparate.call(this,this.FUNC_ADD,this.FUNC_ADD);else raw.blendEquation.call(this,this.FUNC_ADD);
        if(chosen==='alpha'){
          if(typeof raw.blendFuncSeparate==='function')raw.blendFuncSeparate.call(this,this.SRC_ALPHA,this.ONE_MINUS_SRC_ALPHA,this.ONE,this.ONE_MINUS_SRC_ALPHA);else raw.blendFunc.call(this,this.SRC_ALPHA,this.ONE_MINUS_SRC_ALPHA);
        }else if(chosen==='addalpha'){
          if(typeof raw.blendFuncSeparate==='function')raw.blendFuncSeparate.call(this,this.SRC_ALPHA,this.ONE,this.ONE,this.ONE);else raw.blendFunc.call(this,this.SRC_ALPHA,this.ONE);
        }else if(chosen==='oneone'){
          if(typeof raw.blendFuncSeparate==='function')raw.blendFuncSeparate.call(this,this.ONE,this.ONE,this.ONE,this.ONE);else raw.blendFunc.call(this,this.ONE,this.ONE);
        }
        stats.modified++;stats.last={t:Math.round(performance.now()),mode:chosen,old};
        return raw.drawElements.apply(this,arguments);
      } finally {
        if(old.srcRGB!=null){if(typeof raw.blendFuncSeparate==='function'&&old.srcAlpha!=null)raw.blendFuncSeparate.call(this,old.srcRGB,old.dstRGB,old.srcAlpha,old.dstAlpha);else raw.blendFunc.call(this,old.srcRGB,old.dstRGB)}
        if(old.eqRGB!=null){if(typeof raw.blendEquationSeparate==='function'&&old.eqAlpha!=null)raw.blendEquationSeparate.call(this,old.eqRGB,old.eqAlpha);else raw.blendEquation.call(this,old.eqRGB)}
        raw.depthMask.call(this,old.depthMask);
        if(old.blend)raw.enable.call(this,this.BLEND);else raw.disable.call(this,this.BLEND);
        s.blend=old.blend;s.depthMask=old.depthMask;s.srcRGB=old.srcRGB;s.dstRGB=old.dstRGB;s.srcAlpha=old.srcAlpha;s.dstAlpha=old.dstAlpha;s.eqRGB=old.eqRGB;s.eqAlpha=old.eqAlpha;
      }
    };
  }
  install(window.WebGLRenderingContext&&WebGLRenderingContext.prototype);
  install(window.WebGL2RenderingContext&&WebGL2RenderingContext.prototype);

  const modes=[
    ['normal','NORMAL · original shoulder material'],
    ['alpha','ALPHA · SRCα / 1-SRCα'],
    ['addalpha','ADD-ALPHA · SRCα / ONE'],
    ['oneone','ADDITIVE · ONE / ONE'],
    ['skip','HIDE · confirmed shoulder batch']
  ];
  function refresh(panel){panel.querySelectorAll('button[data-mode]').forEach(b=>{const on=b.dataset.mode===window.__wrShoulderMode;b.style.background=on?'#5b1717':'rgba(8,7,7,.92)';b.style.borderColor=on?'#e06d4f':'#6d5135';b.textContent=(on?'ACTIVE · ':'TEST · ')+b.dataset.label;});}
  function addPanel(){
    const stage=document.getElementById('wr-character-model-stage');if(!stage||stage.querySelector('.wr-shoulder-lab'))return;
    const panel=document.createElement('div');panel.className='wr-shoulder-lab';panel.style.cssText='position:absolute;z-index:45;left:8px;top:8px;width:190px;padding:7px;border:1px solid #6d5135;background:rgba(7,6,6,.94);box-shadow:0 4px 18px rgba(0,0,0,.45);font:700 8px Arial;color:#d4b47a;letter-spacing:.04em';
    const title=document.createElement('div');title.textContent='SHOULDER MATERIAL LAB V8';title.style.cssText='font-size:9px;margin-bottom:4px;color:#e6c78b';panel.appendChild(title);
    const sub=document.createElement('div');sub.textContent='P13 × 1596 isolated. Test one render mode.';sub.style.cssText='font-size:7px;color:#9f8d78;margin-bottom:6px';panel.appendChild(sub);
    for(const [mode,label] of modes){const b=document.createElement('button');b.type='button';b.dataset.mode=mode;b.dataset.label=label;b.style.cssText='display:block;width:100%;margin:3px 0;padding:5px 6px;border:1px solid #6d5135;color:#ead9b7;text-align:left;font:800 7px Arial;cursor:pointer';b.onclick=()=>{window.__wrShoulderMode=mode;refresh(panel)};panel.appendChild(b)}
    const copy=document.createElement('button');copy.type='button';copy.textContent='COPY LAB STATUS';copy.style.cssText='display:block;width:100%;margin-top:6px;padding:5px;border:1px solid #8c653f;background:#241910;color:#e6c78b;font:800 7px Arial;cursor:pointer';copy.onclick=async()=>{const t=JSON.stringify({mode:window.__wrShoulderMode,stats:window.__wrShoulderLabStats},null,2);try{await navigator.clipboard.writeText(t);copy.textContent='STATUS COPIED';setTimeout(()=>copy.textContent='COPY LAB STATUS',1200)}catch(e){console.info('[WarRoom Shoulder Lab]',t)}};panel.appendChild(copy);
    stage.appendChild(panel);refresh(panel);
  }
  new MutationObserver(addPanel).observe(document.documentElement,{subtree:true,childList:true});setTimeout(addPanel,500);setTimeout(addPanel,1800);
  console.info('[WarRoom Shoulder Material Lab v8] P13 x 1596 isolated. Rendering starts NORMAL.');
})();
</script>'''

if MARK not in h:
    if '</head>' not in h: raise RuntimeError('head marker missing for Shoulder Material Lab')
    h=h.replace('</head>',script+'\n</head>',1)
index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 Shoulder Material Lab v8 installed')
