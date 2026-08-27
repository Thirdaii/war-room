const fs=require('fs');
global.window=global;
global.CustomEvent=function(n,o){this.type=n;this.detail=o?.detail};
global.dispatchEvent=()=>{};
global.roster=[{name:'A'},{name:'B'},{name:'C'},{name:'D'},{name:'E'},{name:'F'}];
global.raid=global.roster.map(x=>x.name);
global.WarRoomSpecRefresh={apply:(rows)=>({updated:rows.map(x=>x.name),missing:[],ignored:[]})};
global.fetch=()=>new Promise(()=>{});
eval(fs.readFileSync(__dirname+'/armory_refresh_adapter.js','utf8'));
(async()=>{
 const start=Date.now();
 const r=await window.WarRoomArmoryRefresh.refreshRaid({timeoutMs:40,deadlineMs:120,concurrency:3,retryTransient:false});
 const ms=Date.now()-start;
 if(ms>500)throw new Error('Refresh exceeded hard deadline: '+ms+'ms');
 if(!r.timedOut)throw new Error('Expected timedOut=true');
 if(!r.errors.length)throw new Error('Expected timeout errors');
 console.log('Refresh deadline regression passed in',ms,'ms');
})().catch(e=>{console.error(e);process.exit(1)});
