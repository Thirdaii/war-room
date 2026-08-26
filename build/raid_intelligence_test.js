const fs=require('fs');
global.window=global;
const p=(name,cls,spec,role)=>({name,class:cls,spec,role});
global.roster=[
 p('EnhWrong','Shaman','Enhancement','Melee'),p('MageA','Mage','Arcane','Ranged'),p('LockA','Warlock','Destruction','Ranged'),p('HunterA','Hunter','Beast Mastery','Ranged'),p('PriestA','Priest','Shadow','Ranged'),
 p('ElemWrong','Shaman','Elemental','Ranged'),p('RogueA','Rogue','Combat','Melee'),p('WarA','Warrior','Fury','Melee'),p('FeralA','Druid','Feral','Melee'),p('RetA','Paladin','Retribution','Melee'),
 p('TankA','Warrior','Protection','Tank'),p('TankB','Paladin','Protection','Tank'),p('HealA','Priest','Holy','Healer'),p('HealB','Druid','Restoration','Healer'),p('HealC','Shaman','Restoration','Healer'),
 p('MageB','Mage','Fire','Ranged'),p('LockB','Warlock','Destruction','Ranged'),p('HunterB','Hunter','Beast Mastery','Ranged'),p('Moonkin','Druid','Balance','Ranged'),p('HealD','Paladin','Holy','Healer'),
 p('RogueB','Rogue','Combat','Melee'),p('WarB','Warrior','Arms','Melee'),p('HunterC','Hunter','Survival','Ranged'),p('LockC','Warlock','Affliction','Ranged'),p('HealE','Priest','Discipline','Healer')
];
global.raid=global.roster.map(x=>x.name);
eval(fs.readFileSync(__dirname+'/raid_intelligence.js','utf8'));
window.wrSelectedRaid='Black Temple';window.wrSelectedBoss='Illidan Stormrage';
let result=window.WarRoomRaidIntelligence.analyze();
if(result.players.length!==25)throw new Error('Production flat raid adapter failed');
if(result.players[0].class!=='Shaman'||result.players[0]._group!==1)throw new Error('Roster lookup/group mapping failed');
const before=result.parties.map(x=>x.synergy).join(',');
const t=global.raid[0];global.raid[0]=global.raid[5];global.raid[5]=t;
result=window.WarRoomRaidIntelligence.analyze();
const after=result.parties.map(x=>x.synergy).join(',');
if(before===after)throw new Error('Moving production raid names did not change intelligence');
if(result.encounter.boss!=='Illidan Stormrage')throw new Error('Encounter selection failed');
console.log('Production Raid Intelligence regression passed:',before,'->',after);
