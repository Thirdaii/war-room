/* War Room v1.7.4 - ClassicArmory Refresh Adapter */
(function(){
  const norm=s=>String(s||'').trim();
  const slug=s=>norm(s).toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
  const config={region:'us',version:'tbc-anniversary',realm:'dreamscythe',source:'ClassicArmory'};
  function characterUrl(name,opts={}){
    const c={...config,...opts};
    return `https://classic-armory.org/character/${encodeURIComponent(c.region)}/${encodeURIComponent(c.version)}/${encodeURIComponent(slug(c.realm))}/${encodeURIComponent(slug(name))}`;
  }
  function extractFromPayload(payload,name,url){
    if(!payload)return null;
    const c=payload.character||payload.data?.character||payload.data||payload;
    const specs=c.specializations||c.specs||c.talents||[];
    let active='',secondary='';
    if(Array.isArray(specs)){
      const mapped=specs.map(x=>typeof x==='string'?x:(x?.name||x?.spec_name||x?.specialization||'')).filter(Boolean);
      active=mapped[0]||''; secondary=mapped[1]||'';
    }
    active=active||c.active_spec||c.activeSpec||c.spec_name||c.spec||c.specialization||'';
    secondary=secondary||c.secondary_spec||c.secondarySpec||c.off_spec||c.offSpec||'';
    const updated=c.updated_at||c.updatedAt||c.last_updated||c.lastUpdated||payload.updated_at||payload.updatedAt||'';
    if(!active)return null;
    return {name:c.name||name,activeSpec:active,secondarySpec:secondary,updatedAt:updated||new Date().toISOString(),source:config.source,sourceUrl:url,talents:c.talent_build||c.talentBuild||c.talents_data||null};
  }
  function extractFromHtml(html,name,url){
    if(!html)return null;
    const text=String(html);
    const jsonScripts=[...text.matchAll(/<script[^>]*type=["']application\/json["'][^>]*>([\s\S]*?)<\/script>/gi)].map(m=>m[1]);
    for(const raw of jsonScripts){try{const row=extractFromPayload(JSON.parse(raw),name,url);if(row)return row}catch(e){}}
    const next=text.match(/<script[^>]*id=["']__NEXT_DATA__["'][^>]*>([\s\S]*?)<\/script>/i);
    if(next){try{const row=extractFromPayload(JSON.parse(next[1]),name,url);if(row)return row}catch(e){}}
    const specMatches=[...text.matchAll(/(?:spec(?:ialization)?[_\s-]*(?:name)?|active[_\s-]*spec)["'\s:=]+([A-Za-z ]{3,24})/gi)].map(m=>norm(m[1]));
    const active=specMatches.find(Boolean)||'';
    const updated=(text.match(/updated[_\s-]*at["'\s:=]+([^"'<,}]+)/i)||[])[1]||'';
    return active?{name,activeSpec:active,secondarySpec:specMatches[1]||'',updatedAt:updated||new Date().toISOString(),source:config.source,sourceUrl:url}:null;
  }
  async function fetchCharacter(name,opts={}){
    const url=characterUrl(name,opts), timeoutMs=opts.timeoutMs||8000, controller=new AbortController(), timer=setTimeout(()=>controller.abort(),timeoutMs);
    try{
      const res=await fetch(url,{headers:{'Accept':'application/json,text/html;q=0.9,*/*;q=0.8'},signal:controller.signal,cache:'no-store'});
      if(!res.ok)throw new Error(`HTTP ${res.status}`);
      const type=(res.headers.get('content-type')||'').toLowerCase();
      if(type.includes('json'))return extractFromPayload(await res.json(),name,url);
      return extractFromHtml(await res.text(),name,url);
    } finally {clearTimeout(timer)}
  }
  async function refreshNames(names,opts={}){
    const list=[...new Set((names||[]).map(norm).filter(Boolean))], records=[],errors=[];
    for(const name of list){
      try{const row=await fetchCharacter(name,opts);if(row)records.push(row);else errors.push({name,error:'No spec data found'});}catch(e){errors.push({name,error:e?.message||String(e)})}
    }
    const result=window.WarRoomSpecRefresh?window.WarRoomSpecRefresh.apply(records,{source:config.source}):{updated:[],missing:[],ignored:[]};
    return {...result,fetched:records.length,errors,records};
  }
  async function refreshRaid(opts={}){
    let names=[];try{if(typeof raid!=='undefined'&&Array.isArray(raid))names=raid}catch(e){}if(!names.length&&Array.isArray(window.raid))names=window.raid;
    return refreshNames(names,opts);
  }
  window.WarRoomArmoryRefresh={config,characterUrl,extractFromPayload,extractFromHtml,fetchCharacter,refreshNames,refreshRaid};
})();
