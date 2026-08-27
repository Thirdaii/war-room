/* War Room v1.7.8 - Spec Refresh Bridge */
(function(){
  const norm=s=>String(s||'').trim();
  const key=s=>norm(s).toLowerCase();
  const tankSpecs=/^(Protection|Feral.*Tank|Guardian)$/i;
  const healerSpecs=/^(Holy|Discipline|Restoration)$/i;
  const meleeSpecs=/^(Arms|Fury|Combat|Assassination|Subtlety|Enhancement|Retribution|Feral)$/i;
  function deriveRole(activeSpec,className,currentRole=''){
    const spec=norm(activeSpec),cls=norm(className),cur=norm(currentRole);
    if(cur&&cur!=='Role TBD'&&cur!=='Unknown')return cur;
    if(tankSpecs.test(spec))return 'Tank';
    if(healerSpecs.test(spec))return 'Healer';
    if(meleeSpecs.test(spec))return 'Melee';
    if(spec)return 'Ranged';
    if(['Rogue'].includes(cls))return 'Melee';
    if(['Mage','Warlock','Hunter'].includes(cls))return 'Ranged';
    return cur;
  }
  function rosterRef(){try{if(typeof roster!=='undefined'&&Array.isArray(roster))return roster}catch(e){}return Array.isArray(window.roster)?window.roster:[]}
  function normalizeRecord(r){
    if(!r||!r.name)return null;
    const active=norm(r.activeSpec||r.spec||r.talentSpec||r.primarySpec);
    const secondary=norm(r.secondarySpec||r.offSpec||r.dualSpec);
    const updated=r.updatedAt||r.specUpdatedAt||r.armoryUpdatedAt||new Date().toISOString();
    return {name:norm(r.name),activeSpec:active,secondarySpec:secondary,updatedAt:updated,source:norm(r.source||'import'),sourceUrl:norm(r.sourceUrl||''),talents:r.talents||null};
  }
  function apply(records,opts={}){
    const rr=rosterRef(), rows=(Array.isArray(records)?records:[]).map(normalizeRecord).filter(Boolean), byName=new Map(rr.map(p=>[key(p&&p.name),p])), result={updated:[],missing:[],ignored:[]};
    rows.forEach(row=>{
      const p=byName.get(key(row.name));
      if(!p){result.missing.push(row.name);return}
      if(!row.activeSpec){result.ignored.push(row.name);return}
      p.spec=row.activeSpec; p.talentSpec=row.activeSpec; p.specUpdatedAt=row.updatedAt; p.specSource=row.source;
      p.role=deriveRole(row.activeSpec,p.class,p.role);
      if(row.sourceUrl)p.specSourceUrl=row.sourceUrl;
      if(row.secondarySpec){p.secondarySpec=row.secondarySpec;p.dualSpec=row.secondarySpec}
      if(row.talents)p.talentsData=row.talents;
      result.updated.push(row.name);
    });
    try{if(typeof saveState==='function')saveState();else if(typeof saveRoster==='function')saveRoster()}catch(e){}
    try{if(typeof renderRoster==='function')renderRoster()}catch(e){}
    try{if(typeof renderRaid==='function')renderRaid()}catch(e){}
    try{if(window.renderRaidIntelligence)window.renderRaidIntelligence()}catch(e){}
    window.dispatchEvent(new CustomEvent('warroom:spec-refresh',{detail:result}));
    return result;
  }
  function exportStatus(){return rosterRef().map(p=>({name:p.name,spec:p.spec||p.talentSpec||'',role:p.role||'',secondarySpec:p.secondarySpec||p.dualSpec||'',specUpdatedAt:p.specUpdatedAt||p.armoryUpdatedAt||'',specSource:p.specSource||''}))}
  window.WarRoomSpecRefresh={normalizeRecord,apply,deriveRole,exportStatus,contract:{required:['name','activeSpec'],optional:['secondarySpec','updatedAt','source','sourceUrl','talents']}};
})();
