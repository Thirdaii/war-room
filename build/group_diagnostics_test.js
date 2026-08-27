const fs=require('fs');
global.window=global;
const now=Date.now();
const iso=h=>new Date(now-h*3600000).toISOString();
global.roster=[
{name:'FreshEnh',class:'Shaman',spec:'Enhancement',role:'Melee',specUpdatedAt:iso(10)},
{name:'StaleShadow',class:'Priest',spec:'Shadow',role:'Ranged',specUpdatedAt:iso(240)},
{name:'MissingMage',class:'Mage',role:'Ranged'},
{name:'FreshTank',class:'Warrior',spec:'Protection',role:'Tank',specUpdatedAt:iso(12)},
{name:'FreshHeal',class:'Priest',spec:'Holy',role:'Healer',specUpdatedAt:iso(12)}
];
global.raid=['FreshEnh','FreshTank','FreshHeal','FreshEnh','FreshEnh','StaleShadow','MissingMage','FreshHeal','FreshTank','FreshEnh'];
eval(fs.readFileSync(__dirname+'/raid_intelligence.js','utf8'));
const r=window.WarRoomRaidIntelligence.analyze();
const g2=r.parties.find(x=>x.group===2);
if(!g2)throw new Error('Missing group 2 diagnostics');
const stale=g2.diagnostics.find(x=>x.name==='StaleShadow');
const missing=g2.diagnostics.find(x=>x.name==='MissingMage');
if(!stale||stale.state!=='stale'||stale.action!=='Refresh now')throw new Error('Stale raider diagnostic failed');
if(!missing||missing.state!=='missing'||missing.action!=='Refresh or set spec')throw new Error('Missing raider diagnostic failed');
if(g2.diagnostics.some(x=>x.name==='FreshEnh'))throw new Error('Fresh raider incorrectly flagged');
console.log('Group diagnostics regression passed');
