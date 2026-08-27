/* War Room v1.7.13 - Inspect Enrichment Sync */
(function(){
  const norm=s=>String(s||'').trim();
  const key=s=>norm(s).toLowerCase();
  function rosterRef(){try{if(typeof roster!=='undefined'&&Array.isArray(roster))return roster}catch(e){}return Array.isArray(window.roster)?window.roster:[]}
  function byName(name){return rosterRef().find(p=>key(p?.name)===key(name))||null}
  function talentText(p){const t=p?.talentsData??p?.talents;if(!t)return 'Awaiting armory enrichment';if(typeof t==='string')return t;if(Array.isArray(t))return t.map(x=>`${x.name||x.tree||'?'} ${x.points??x.value??''}`.trim()).filter(Boolean).join(' / ')||'Talents loaded';if(typeof t==='object')return Object.entries(t).map(([k,v])=>typeof v==='object'&&v?`${v.name||k} ${v.points??v.value??''}`.trim():`${k} ${v}`).join(' / ');return 'Talents loaded'}
  function gearRows(p){return Array.isArray(p?.gear)?p.gear:Array.isArray(p?.equipment)?p.equipment:Array.isArray(p?.items)?p.items:[]}
  function findExact(root,text){return [...root.querySelectorAll('*')].find(el=>norm(el.textContent).toUpperCase()===text.toUpperCase())||null}
  function setMetric(root,label,value){const lab=findExact(root,label);if(!lab)return false;const box=lab.parentElement;if(!box)return false;const candidates=[...box.children].filter(x=>x!==lab);const target=candidates.find(x=>/^(DIV|SPAN|B|STRONG|P)$/i.test(x.tagName))||candidates[0];if(target){target.textContent=value;return true}return false}
  function detectName(root){const names=rosterRef().map(p=>p?.name).filter(Boolean);for(const n of names){const hit=[...root.querySelectorAll('h1,h2,h3,h4,strong,b,div,span')].find(el=>norm(el.textContent)===n);if(hit)return n}return ''}
  function sync(root=document){const awaiting=[...root.querySelectorAll('*')].find(el=>/Awaiting armory enrichment/i.test(el.textContent||''));const metric=findExact(root,'AVG ILVL')||findExact(root,'GEARSCORE')||findExact(root,'ROLE / SPEC');if(!awaiting&&!metric)return false;const scope=(awaiting||metric).closest('[role="dialog"],.modal,.overlay,.drawer,.dossier,.wr-dossier-fixed')||document.body;const name=detectName(scope);if(!name)return false;const p=byName(name);if(!p)return false;
    const spec=p.spec||p.talentSpec||p.activeSpec||p.role||'Unknown';
    setMetric(scope,'ROLE / SPEC',spec);
    setMetric(scope,'GEARSCORE',p.gearscore??p.gearScore??'—');
    setMetric(scope,'AVG ILVL',p.ilvl??p.itemLevel??'—');
    const talentLabel=findExact(scope,'TALENT BUILD');if(talentLabel&&talentLabel.parentElement){const box=talentLabel.parentElement;const val=[...box.children].find(x=>x!==talentLabel);if(val)val.textContent=talentText(p)}
    const eqLabel=findExact(scope,'EQUIPMENT');if(eqLabel&&eqLabel.parentElement){const box=eqLabel.parentElement;const val=[...box.children].find(x=>x!==eqLabel);const gear=gearRows(p);if(val)val.textContent=gear.length?`${gear.length} equipped items loaded from armory.`:'Current gear will appear here when verified from armory data.'}
    return true
  }
  let timer=null;function queue(){clearTimeout(timer);timer=setTimeout(()=>sync(document),60)}
  new MutationObserver(queue).observe(document.documentElement,{subtree:true,childList:true,characterData:true});
  document.addEventListener('click',()=>{setTimeout(queue,40);setTimeout(queue,180)});
  window.addEventListener('warroom:spec-refresh',()=>{sync(document);setTimeout(()=>sync(document),150)});
  window.syncWarRoomInspectEnrichment=()=>sync(document);
})();
