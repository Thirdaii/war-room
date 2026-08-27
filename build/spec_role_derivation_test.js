const fs=require('fs');
global.window=global;
global.CustomEvent=function(type,init){this.type=type;this.detail=init&&init.detail};
global.dispatchEvent=()=>{};
global.roster=[
 {name:'ProtPally',class:'Paladin'},
 {name:'HolyPriest',class:'Priest'},
 {name:'EnhSham',class:'Shaman'},
 {name:'ShadowPriest',class:'Priest'},
 {name:'Magey',class:'Mage'}
];
eval(fs.readFileSync(__dirname+'/spec_refresh.js','utf8'));
const d=window.WarRoomSpecRefresh.deriveRole;
const cases=[
 ['Protection','Paladin','Tank'],
 ['Holy','Priest','Healer'],
 ['Enhancement','Shaman','Melee'],
 ['Shadow','Priest','Ranged'],
 ['Arcane','Mage','Ranged']
];
for(const [spec,cls,want] of cases){const got=d(spec,cls,'');if(got!==want)throw new Error(`${cls} ${spec}: expected ${want}, got ${got}`)}
window.WarRoomSpecRefresh.apply([
 {name:'ProtPally',activeSpec:'Protection'},
 {name:'HolyPriest',activeSpec:'Holy'},
 {name:'EnhSham',activeSpec:'Enhancement'},
 {name:'ShadowPriest',activeSpec:'Shadow'},
 {name:'Magey',activeSpec:'Arcane'}
]);
for(const p of global.roster){if(!p.role)throw new Error(`Role not applied for ${p.name}`)}
console.log('TBC spec-to-role derivation passed',global.roster.map(p=>`${p.name}:${p.role}`).join(', '));
