/* War Room v1.7.14 - Inspect Auto Enrichment */
(function(){
  const norm=s=>String(s||'').trim();
  const key=s=>norm(s).toLowerCase();
  const inflight=new Map();
  const freshForMs=10*60*1000;
  function rosterRef(){try{if(typeof roster!=='undefined'&&Array.isArray(roster))return roster}catch(e){}return Array.isArray(window.roster)?window.roster:[]}
  function byName(name){return rosterRef().find(p=>key(p?.name)===key(name))||null}
  function talentText(p){const t=p?.talentsData??p?.talents;if(!t)return 'Loading armory data…';if(typeof t==='string')return t;if(Array.isArray(t))return t.map(x=>`${x.name||x.tree||'?'} ${x.points??x.value??''}`.trim()).filter(Boolean).join(' / ')||'Talents loaded';if(typeof t==='object')return Object.entries(t).map(([k,v])=>typeof v==='object'&&v?`${v.name||k} ${v.points??v.value??''}`.trim():`${k} ${v}`).join(' / ');return 'Talents loaded'}
  function gearRows(p){return Array.isArray(p?.gear)?p.gear:Array.isArray(p?.equipment)?p.equipment:Array.isArray(p?.items)?p.items:[]}
  function hasEnrichment(p){return !!(p&&(p.spec||p.talentSpec||p.ilvl!=null||p.gearscore!=null||p.gearScore!=null||p.talentsData||p.talents||gearRows(p).length))}
  function status(name){return window.WarRoomArmoryRefresh?.getStatus?.(name)||null}
  function isFresh(name,p){const st=status(name);if(st?.lastSuccessAt){const age=Date.now()-Date.parse(st.lastSuccessAt);if(Number.isFinite(age)&&age>=0&&age<freshForMs)return true}return hasEnrichment(p)}
  function findExact(root,text){return [...root.querySelectorAll('*')].find(el=>norm(el.textContent).toUpperCase()===text.toUpperCase())||null}
  function setMetric(root,label,value){const lab=findExact(root,label);if(!lab)return false;const box=lab.parentElement;if(!box)return false;const candidates=[...box.children].filter(x=>x!==lab);const target=candidates.find(x=>/^(DIV|SPAN|B|STRONG|P)$/i.test(x.tagName))||candidates[0];if(target){target.textContent=value;return true}return false}
  function detectName(root){const names=rosterRef().map(p=>p?.name).filter(Boolean);for(const n of names){const hit=[...root.querySelectorAll('h1,h2,h3,h4,strong,b,div,span')].find(el=>norm(el.textContent)===n);if(hit)return n}return ''}
  function scopeFor(root=document){const awaiting=[...root.querySelectorAll('*')].find(el=>/Awaiting armory enrichment|Loading armory data/i.test(el.textContent||''));const metric=findExact(root,'AVG ILVL')||findExact(root,'GEARSCORE')||findExact(root,'ROLE / SPEC');if(!awaiting&&!metric)return null;return (awaiting||metric).closest('[role="dialog"],.modal,.overlay,.drawer,.dossier,.wr-dossier-fixed')||document.body}
  function showLoading(scope){setMetric(scope,'ROLE / SPEC','Loading…');setMetric(scope,'GEARSCORE','…');setMetric(scope,'AVG ILVL','…');const talentLabel=findExact(scope,'TALENT BUILD');if(talentLabel&&talentLabel.parentElement){const val=[...talentLabel.parentElement.children].find(x=>x!==talentLabel);if(val)val.textContent='Loading armory data…'}}
  function render(scope,name){const p=byName(name);if(!p)return false;const st=status(name);const spec=p.spec||p.talentSpec||p.activeSpec||p.role||'Unknown';setMetric(scope,'ROLE / SPEC',spec);setMetric(scope,'GEARSCORE',p.gearscore??p.gearScore??'—');setMetric(scope,'AVG ILVL',p.ilvl??p.itemLevel??'—');const talentLabel=findExact(scope,'TALENT BUILD');if(talentLabel&&talentLabel.parentElement){const box=talentLabel.parentElement;const val=[...box.children].find(x=>x!==talentLabel);if(val)val.textContent=hasEnrichment(p)?talentText(p):(st?.lastError?`Armory error: ${st.lastError}`:'Awaiting armory enrichment')}
    const eqLabel=findExact(scope,'EQUIPMENT');if(eqLabel&&eqLabel.parentElement){const box=eqLabel.parentElement;const val=[...box.children].find(x=>x!==eqLabel);const gear=gearRows(p);if(val)val.textContent=gear.length?`${gear.length} equipped items loaded from armory.`:(st?.lastError?`Armory error: ${st.lastError}`:'Current gear will appear here when verified from armory data.')}
    return true}
  async function enrich(name,scope){const k=key(name);if(inflight.has(k))return inflight.get(k);const job=(async()=>{try{showLoading(scope);const api=window.WarRoomArmoryRefresh;if(!api?.refreshNames)throw new Error('Armory refresh service unavailable');await api.refreshNames([name],{concurrency:1,deadlineMs:10000});render(scope,name);if(typeof window.renderWarRoomCharacterData==='function')window.renderWarRoomCharacterData();}catch(e){render(scope,name)}finally{inflight.delete(k)}})();inflight.set(k,job);return job}
  function sync(root=document){const scope=scopeFor(root);if(!scope)return false;const name=detectName(scope);if(!name)return false;const p=byName(name);if(!p)return false;if(isFresh(name,p)){render(scope,name);return true}enrich(name,scope);return true}
  let timer=null;function queue(){clearTimeout(timer);timer=setTimeout(()=>sync(document),60)}
  new MutationObserver(queue).observe(document.documentElement,{subtree:true,childList:true,characterData:true});
  document.addEventListener('click',()=>{setTimeout(queue,40);setTimeout(queue,180)});
  window.addEventListener('warroom:spec-refresh',()=>{sync(document);setTimeout(()=>sync(document),150)});
  window.syncWarRoomInspectEnrichment=()=>sync(document);
})();
