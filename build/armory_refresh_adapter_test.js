const fs=require('fs');
global.window=global;
let mode='hard',calls=0;
global.fetch=async()=>{calls++;if(mode==='retry-then-success'&&calls===1)throw new Error('network transient');if(mode==='retry-then-success')return{ok:true,headers:{get:()=> 'application/json'},json:async()=>({character:{name:'Retryman',spec:'Enhancement',updated_at:'2026-08-26T12:00:00Z'}})};throw new Error('network disabled in unit test')};
global.WarRoomSpecRefresh={apply:(rows)=>({updated:rows.map(x=>x.name),missing:[],ignored:[]})};
eval(fs.readFileSync(__dirname+'/armory_refresh_adapter.js','utf8'));
const a=window.WarRoomArmoryRefresh;
const u=a.characterUrl('Test Player');
if(!u.includes('classicarmory.gg/character/us/dreamscythe/')||!u.includes('Test%20Player')||!u.includes('ns=classicann'))throw new Error('Character URL construction failed: '+u);
const j=a.extractFromPayload({character:{name:'Enhman',spec:'Enhancement',secondary_spec:'Restoration',updated_at:'2026-08-26T12:00:00Z'}},'Enhman','x');
if(!j||j.activeSpec!=='Enhancement'||j.secondarySpec!=='Restoration'||j.source!=='ClassicArmory.gg')throw new Error('JSON payload parsing failed');
(async()=>{
  calls=0;mode='retry-then-success';let r=await a.refreshNames(['Retryman'],{retryDelayMs:1});if(r.errors.length!==0||r.updated[0]!=='Retryman')throw new Error('Transient retry did not recover');let s=a.getStatus('Retryman');if(!s||s.status!=='success'||s.attempts!==2)throw new Error('Successful retry state not recorded');
  calls=0;mode='hard';r=await a.refreshNames(['Nobody'],{retryDelayMs:1});if(!r.errors||r.errors.length!==1)throw new Error('Network failure was not isolated');s=a.getStatus('Nobody');if(!s||s.status!=='retryable-failure'||s.attempts!==2)throw new Error('Retryable failure state not recorded');
  console.log('Armory reliability regression passed');
})().catch(e=>{console.error(e);process.exit(1)});
