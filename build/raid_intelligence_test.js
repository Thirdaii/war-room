const fs=require('fs');
global.window=global;
eval(fs.readFileSync(__dirname+'/raid_intelligence.js','utf8'));
const p=(name,cls,spec,role)=>({name,class:cls,spec,role});
window.raid=undefined;
window.raidGroups=[
 [p('EnhWrong','Shaman','Enhancement','Melee'),p('MageA','Mage','Arcane','Ranged'),p('LockA','Warlock','Destruction','Ranged'),p('HunterA','Hunter','Beast Mastery','Ranged'),p('PriestA','Priest','Shadow','Ranged')],
 [p('ElemWrong','Shaman','Elemental','Ranged'),p('RogueA','Rogue','Combat','Melee'),p('WarA','Warrior','Fury','Melee'),p('FeralA','Druid','Feral','Melee'),p('RetA','Paladin','Retribution','Melee')],
 [p('TankA','Warrior','Protection','Tank'),p('TankB','Paladin','Protection','Tank'),p('HealA','Priest','Holy','Healer'),p('HealB','Druid','Restoration','Healer'),p('HealC','Shaman','Restoration','Healer')],
 [p('MageB','Mage','Fire','Ranged'),p('LockB','Warlock','Destruction','Ranged'),p('HunterB','Hunter','Beast Mastery','Ranged'),p('Moonkin','Druid','Balance','Ranged'),p('HealD','Paladin','Holy','Healer')],
 [p('RogueB','Rogue','Combat','Melee'),p('WarB','Warrior','Arms','Melee'),p('HunterC','Hunter','Survival','Ranged'),p('LockC','Warlock','Affliction','Ranged'),p('HealE','Priest','Discipline','Healer')]
];
window.wrSelectedRaid='Black Temple';window.wrSelectedBoss='Illidan Stormrage';
let result=window.WarRoomRaidIntelligence.analyze();
if(result.players.length!==25)throw new Error('raidGroups adapter failed');
if(!result.swaps.length)throw new Error('Expected scored swap');
const before=result.parties.map(x=>x.synergy).join(',');
const t=window.raidGroups[0][0];window.raidGroups[0][0]=window.raidGroups[1][0];window.raidGroups[1][0]=t;
result=window.WarRoomRaidIntelligence.analyze();
const after=result.parties.map(x=>x.synergy).join(',');
if(before===after)throw new Error('Moving raiders did not change live intelligence');
if(result.encounter.boss!=='Illidan Stormrage')throw new Error('Encounter selection failed');
console.log('Raid Intelligence live-state regression passed:',before,'->',after);
