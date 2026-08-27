/* War Room v1.7.26 - Spec refresh bridge with model metadata */
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
    const gs=Number(r.gearscore??r.gearScore),il=Number(r.ilvl??r.itemLevel),lvl=Number(r.level);
    const gender=(r.gender===0||r.gender===1)?r.gender:null;
    return {name:norm(r.name),activeSpec:active,secondarySpec:secondary,updatedAt:updated,source:norm(r.source||'import'),sourceUrl:norm(r.sourceUrl||''),talents:r.talents??null,gearscore:Number.isFinite(gs)?gs:null,ilvl:Number.isFinite(il)?il:null,items:Array.isArray(r.items)?r.items:[],className:norm(r.className||r.class||''),race:norm(r.race||''),gender,appearance:r.appearance&&typeof r.appearance==='object'?r.appearance:null,level:Number.isFinite(lvl)?lvl:null};
  }
  function apply(records,opts={}){
    const rr=rosterRef(),rows=(Array.isArray(records)?records:[]).map(normalizeRecord).filter(Boolean),byName=new Map(rr.map(p=>[key(p&&p.name),p])),result={updated:[],missing:[],ignored:[]};
    rows.forEach(row=>{
      const p=byName.get(key(row.name));
      if(!p){result.missing.push(row.name);return}
      if(!row.activeSpec&&!row.talents&&row.gearscore==null&&row.ilvl==null&&!row.items.length&&!row.race&&row.gender==null){result.ignored.push(row.name);return}
      if(row.activeSpec){p.spec=row.activeSpec;p.talentSpec=row.activeSpec;p.role=deriveRole(row.activeSpec,row.className||p.class,p.role)}
      p.specUpdatedAt=row.updatedAt;p.armoryUpdatedAt=row.updatedAt;p.specSource=row.source;
      if(row.sourceUrl)p.specSourceUrl=row.sourceUrl;
      if(row.secondarySpec){p.secondarySpec=row.secondarySpec;p.dualSpec=row.secondarySpec}
      if(row.talents){p.talentsData=row.talents;p.talents=typeof row.talents==='string'?row.talents:JSON.stringify(row.talents)}
      if(row.gearscore!=null)p.gearscore=Math.round(row.gearscore);
      if(row.ilvl!=null)p.ilvl=Math.round(row.ilvl*10)/10;
      if(row.items.length){p.gear=row.items;p.equipment=row.items;p.items=row.items}
      if(row.className&&!p.class)p.class=row.className;
      if(row.race)p.race=row.race;
      if(row.gender!=null)p.gender=row.gender;
      if(row.appearance){p.appearance=row.appearance;for(const k of ['skin','face','hairStyle','hairColor','facialStyle'])if(Number.isInteger(row.appearance[k]))p[k]=row.appearance[k]}
      if(row.level!=null)p.level=row.level;
      result.updated.push(row.name);
    });
    try{if(typeof saveState==='function')saveState();else if(typeof saveRoster==='function')saveRoster()}catch(e){}
    try{if(typeof renderRoster==='function')renderRoster()}catch(e){}
    try{if(typeof renderRaid==='function')renderRaid()}catch(e){}
    try{if(window.renderRaidIntelligence)window.renderRaidIntelligence()}catch(e){}
    window.dispatchEvent(new CustomEvent('warroom:spec-refresh',{detail:result}));
    return result;
  }
  function exportStatus(){return rosterRef().map(p=>({name:p.name,spec:p.spec||p.talentSpec||'',role:p.role||'',secondarySpec:p.secondarySpec||p.dualSpec||'',specUpdatedAt:p.specUpdatedAt||p.armoryUpdatedAt||'',specSource:p.specSource||'',gearscore:p.gearscore??null,ilvl:p.ilvl??null,gear:p.gear||p.equipment||[],race:p.race||'',gender:p.gender??null,appearance:p.appearance||null}))}
  window.WarRoomSpecRefresh={normalizeRecord,apply,deriveRole,exportStatus,contract:{required:['name'],optional:['activeSpec','secondarySpec','updatedAt','source','sourceUrl','talents','gearscore','ilvl','items','className','race','gender','appearance','level']}};
})();
