const fs=require('fs');
global.window=global;
eval(fs.readFileSync(__dirname+'/raid_intelligence.js','utf8'));
const p=(name,cls,spec,role)=>({name,class:cls,spec,role});
window.raid=[
 [p('EnhWrong','Shaman','Enhancement','Melee'),p('MageA','Mage','Arcane','Ranged'),p('LockA','Warlock','Destruction','Ranged'),p('HunterA','Hunter','Beast Mastery','Ranged'),p('PriestA','Priest','Shadow','Ranged')],
 [p('ElemWrong','Shaman','Elemental','Ranged'),p('RogueA','Rogue','Combat','Melee'),p('WarA','Warrior','Fury','Melee'),p('FeralA','Druid','Feral','Melee'),p('RetA','Paladin','Retribution','Melee')],
 [p('TankA','Warrior','Protection','Tank'),p('TankB','Paladin','Protection','Tank'),p('HealA','Priest','Holy','Healer'),p('HealB','Druid','Restoration','Healer'),p('HealC','Shaman','Restoration','Healer')],
 [p('MageB','Mage','Fire','Ranged'),p('LockB','Warlock','Destruction','Ranged'),p('HunterB','Hunter','Beast Mastery','Ranged'),p('Moonkin','Druid','Balance','Ranged'),p('HealD','Paladin','Holy','Healer')],
 [p('RogueB','Rogue','Combat','Melee'),p('WarB','Warrior','Arms','Melee'),p('HunterC','Hunter','Survival','Ranged'),p('LockC','Warlock','Affliction','Ranged'),p('HealE','Priest','Discipline','Healer')]
];
window.wrSelectedRaid='Black Temple';window.wrSelectedBoss='Illidan Stormrage';
const result=window.WarRoomRaidIntelligence.analyze();
if(result.players.length!==25)throw new Error('Expected 25 players');
if(!Array.isArray(result.swaps)||!result.swaps.length)throw new Error('Expected at least one scored swap');
if(!result.recommendations.some(x=>x.includes('EnhWrong')||x.includes('ElemWrong')))throw new Error('Expected named Shaman swap recommendation');
if(result.encounter.boss!=='Illidan Stormrage')throw new Error('Encounter selection failed');
if(result.method!=='heuristic')throw new Error('Method disclosure missing');
console.log('Raid Intelligence regression test passed:',result.recommendations[0]);
