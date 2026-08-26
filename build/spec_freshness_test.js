const fs=require('fs');
global.window=global;
const now=Date.now();
const iso=h=>new Date(now-h*3600000).toISOString();
const p=(name,cls,spec,role,h,stamp=true)=>{let x={name,class:cls,spec,role};if(stamp)x.specUpdatedAt=iso(h);return x};
global.roster=[
 p('FreshEnh','Shaman','Enhancement','Melee',12),
 p('AgingShadow','Priest','Shadow','Ranged',100),
 p('StaleElem','Shaman','Elemental','Ranged',240),
 p('UnverifiedMoonkin','Druid','Balance','Ranged',0,false),
 {name:'MissingSpec',class:'Mage',role:'Ranged'}
];
global.raid=global.roster.map(x=>x.name);
eval(fs.readFileSync(__dirname+'/raid_intelligence.js','utf8'));
const r=window.WarRoomRaidIntelligence.analyze();
if(!r.dataQuality)throw new Error('Missing dataQuality output');
if(r.dataQuality.fresh!==1)throw new Error('Fresh spec classification failed');
if(r.dataQuality.aging!==1)throw new Error('Aging spec classification failed');
if(r.dataQuality.stale!==1)throw new Error('Stale spec classification failed');
if(r.dataQuality.unverified!==1)throw new Error('Unverified spec classification failed');
if(r.dataQuality.missing!==1)throw new Error('Missing spec classification failed');
if(r.dataQuality.confidence>=100||r.dataQuality.confidence<=0)throw new Error('Confidence score did not reflect mixed freshness');
if(r.coverage.find(x=>x.name==='Totem of Wrath').ok)throw new Error('Stale Elemental spec incorrectly counted as trusted coverage');
if(!r.coverage.find(x=>x.name==='Windfury / Melee Totems').ok)throw new Error('Fresh Enhancement spec failed trusted coverage');
console.log('Spec freshness regression passed:',r.dataQuality);
