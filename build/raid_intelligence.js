/* War Room v1.7 - TBC Phase 3 Raid Intelligence */
const TBC_PHASE3={raidSize:25,groupSize:5,targets:{Tank:{min:2,max:4},Healer:{min:5,max:8},Melee:{min:4,max:10},Ranged:{min:7,max:14}}};
const SPEC_SYNERGY={
  Shaman:{Enhancement:['Melee'],Elemental:['Ranged'],Restoration:['Healer','Ranged']},
  Druid:{Feral:['Melee','Tank'],Balance:['Ranged'],Restoration:['Healer']},
  Hunter:{'Beast Mastery':['Ranged'],Marksmanship:['Ranged'],Survival:['Ranged']},
  Paladin:{Holy:['Healer'],Protection:['Tank'],Retribution:['Melee']},
  Priest:{Discipline:['Healer'],Holy:['Healer'],Shadow:['Ranged']},
  Warrior:{Arms:['Melee'],Fury:['Melee'],Protection:['Tank']},
  Rogue:{Assassination:['Melee'],Combat:['Melee'],Subtlety:['Melee']},
  Mage:{Arcane:['Ranged'],Fire:['Ranged'],Frost:['Ranged']},
  Warlock:{Affliction:['Ranged'],Demonology:['Ranged'],Destruction:['Ranged']}
};
function wrNorm(v){return String(v||'').trim();}
function wrRole(p){return wrNorm(p.role)||'Unknown';}
function wrSpec(p){return wrNorm(p.spec||p.talentSpec||p.build);}
function wrClass(p){return wrNorm(p.class);}
function wrRaidPlayers(){
  if(!Array.isArray(window.raid))return [];
  return window.raid.flatMap((g,gi)=>(Array.isArray(g)?g:[]).filter(Boolean).map(p=>({...p,_group:gi+1})));
}
function wrCountByRole(players){return players.reduce((a,p)=>{let r=wrRole(p);a[r]=(a[r]||0)+1;return a;},{});}
function wrPartyAnalysis(players){
  const groups=[1,2,3,4,5].map(n=>({group:n,players:players.filter(p=>p._group===n)}));
  return groups.map(g=>{
    const roles=wrCountByRole(g.players), shamans=g.players.filter(p=>wrClass(p)==='Shaman'), notes=[];
    if(g.players.length<5)notes.push(`${5-g.players.length} open slot${5-g.players.length===1?'':'s'}`);
    if(g.players.length===5 && !shamans.length)notes.push('No Shaman party support');
    const melee=(roles.Melee||0)+(roles.Tank||0), ranged=(roles.Ranged||0)+(roles.Healer||0);
    shamans.forEach(s=>{let sp=wrSpec(s);if(sp==='Enhancement'&&melee<3)notes.push('Enhancement Shaman has low melee value in this party');if(sp==='Elemental'&&(roles.Ranged||0)<2)notes.push('Elemental Shaman has low caster value in this party');});
    return {...g,roles,notes};
  });
}
function wrCoverage(players){
  const classes=new Set(players.map(wrClass)), specs=new Set(players.map(p=>`${wrClass(p)}:${wrSpec(p)}`));
  return [
    ['Paladin Blessings',classes.has('Paladin')],['Power Word: Fortitude',classes.has('Priest')],['Mark of the Wild',classes.has('Druid')],['Arcane Intellect',classes.has('Mage')],['Healthstones',classes.has('Warlock')],['Shaman Party Support',classes.has('Shaman')],['Bloodlust / Heroism',classes.has('Shaman')],['Shadow Priest Mana Support',specs.has('Priest:Shadow')],['Totem of Wrath',specs.has('Shaman:Elemental')],['Windfury / Melee Totems',specs.has('Shaman:Enhancement')]
  ].map(([name,ok])=>({name,ok}));
}
function wrRaidIntelligence(){
  const players=wrRaidPlayers(),roles=wrCountByRole(players),parties=wrPartyAnalysis(players),coverage=wrCoverage(players),warnings=[],recommendations=[];
  if(players.length<25)warnings.push(`Raid is ${25-players.length} player${25-players.length===24?'':'s'} short of 25.`);
  if((roles.Tank||0)<2)warnings.push('Tank coverage is below the normal 25-player baseline.');
  if((roles.Healer||0)<5)warnings.push('Healing coverage is below the normal 25-player baseline.');
  if(!players.some(p=>wrClass(p)==='Shaman'))warnings.push('No Shaman assigned: major TBC party utility is missing.');
  parties.forEach(g=>g.notes.forEach(n=>warnings.push(`Group ${g.group}: ${n}`)));
  const missing=coverage.filter(x=>!x.ok);missing.forEach(x=>warnings.push(`Missing coverage: ${x.name}`));
  parties.forEach(g=>{if(g.players.length===5&&!g.players.some(p=>wrClass(p)==='Shaman'))recommendations.push(`Consider a Shaman in Group ${g.group} for TBC party-specific support.`);});
  const filled=Math.min(players.length/25,1), roleHealth=Math.min(((roles.Tank||0)>=2?1:0)+((roles.Healer||0)>=5?1:0)+((roles.Ranged||0)>=7?1:0),3)/3, coverageHealth=coverage.filter(x=>x.ok).length/coverage.length;
  const score=Math.round((filled*.40+roleHealth*.30+coverageHealth*.30)*100);
  return {score,players,roles,parties,coverage,warnings,recommendations};
}
window.WarRoomRaidIntelligence={analyze:wrRaidIntelligence,rules:TBC_PHASE3,specSynergy:SPEC_SYNERGY};
