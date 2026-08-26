/* War Room v1.7 - live Raid Intelligence dashboard */
(function(){
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const raidBosses={
    'Black Temple':['High Warlord Naj\'entus','Supremus','Shade of Akama','Teron Gorefiend','Gurtogg Bloodboil','Reliquary of Souls','Mother Shahraz','The Illidari Council','Illidan Stormrage'],
    'Battle for Mount Hyjal':['Rage Winterchill','Anetheron','Kaz\'rogal','Azgalor','Archimonde']
  };
  function selectOptions(arr,selected){return arr.map(x=>`<option value="${esc(x)}"${x===selected?' selected':''}>${esc(x)}</option>`).join('')}
  function ensurePanel(){
    let host=document.getElementById('wrRaidIntelLive');if(host)return host;
    const anchor=document.getElementById('raidIntelligence')||document.getElementById('raidFrame');if(!anchor)return null;
    host=document.createElement('section');host.id='wrRaidIntelLive';host.className='wr-intel-live';
    host.innerHTML='<div class="wr-intel-head"><div><span class="wr-intel-kicker">TBC PHASE 3</span><h2>Raid Intelligence</h2><div class="wr-encounter-controls"><label>Raid<select id="wrRaidSelect"></select></label><label>Encounter<select id="wrBossSelect"></select></label></div><div class="wr-encounter-label" id="wrEncounterLabel"></div></div><div class="wr-intel-score" id="wrIntelScore">--</div></div><div class="wr-intel-grid"><div class="wr-intel-block"><h3>Role Balance</h3><div id="wrIntelRoles"></div></div><div class="wr-intel-block"><h3>Critical Coverage</h3><div id="wrIntelCoverage"></div></div><div class="wr-intel-block wide"><h3>Command Warnings</h3><div id="wrIntelWarnings"></div></div><div class="wr-intel-block wide"><h3>Recommended Actions</h3><div id="wrIntelRecommendations"></div></div></div>';
    anchor.parentNode.insertBefore(host,anchor.nextSibling);
    const rs=document.getElementById('wrRaidSelect'),bs=document.getElementById('wrBossSelect');
    rs.innerHTML=selectOptions(Object.keys(raidBosses),'Black Temple');bs.innerHTML=selectOptions(raidBosses['Black Temple'],'Illidan Stormrage');
    rs.addEventListener('change',()=>{const bosses=raidBosses[rs.value]||[];bs.innerHTML=selectOptions(bosses,bosses[bosses.length-1]||'');if(bs.value)window.WarRoomRaidIntelligence.setEncounter(rs.value,bs.value)});
    bs.addEventListener('change',()=>window.WarRoomRaidIntelligence.setEncounter(rs.value,bs.value));
    window.WarRoomRaidIntelligence.setEncounter('Black Temple','Illidan Stormrage');
    return host;
  }
  function pill(label,value){return `<div class="wr-intel-role"><span>${esc(label)}</span><b>${value||0}</b></div>`}
  function encounterWarning(r){const b=r.encounter.boss,w=r.encounter.weights||{},out=[];if(b==='Illidan Stormrage'){out.push('Illidan profile: tank specialization, healing stability, utility coverage and execution receive extra weight.');}if(b==='Mother Shahraz'){out.push('Mother Shahraz profile: survivability and healing are emphasized.');}if(b==='The Illidari Council'){out.push('Illidari Council profile: utility and control are emphasized.');}if(b==='Archimonde'){out.push('Archimonde profile: survivability and movement discipline are emphasized.');}if(Object.keys(w).length===0)out.push('Generic Phase 3 baseline profile: no extra encounter weighting is applied.');return out}
  function render(){
    if(!window.WarRoomRaidIntelligence)return;const host=ensurePanel();if(!host)return;const r=window.WarRoomRaidIntelligence.analyze();
    const score=document.getElementById('wrIntelScore');score.textContent=r.score+'%';score.dataset.grade=r.score>=85?'ready':r.score>=65?'warn':'danger';score.title=`Encounter-weighted readiness for ${r.encounter.boss}`;
    document.getElementById('wrEncounterLabel').textContent=`${r.encounter.raid} • ${r.encounter.boss}`;
    document.getElementById('wrIntelRoles').innerHTML=['Tank','Healer','Melee','Ranged'].map(x=>pill(x,r.roles[x])).join('');
    document.getElementById('wrIntelCoverage').innerHTML=r.coverage.map(x=>`<div class="wr-intel-check ${x.ok?'ok':'miss'}"><span>${x.ok?'✓':'!'}</span>${esc(x.name)}</div>`).join('');
    const warnings=[...encounterWarning(r),...r.warnings];document.getElementById('wrIntelWarnings').innerHTML=warnings.length?warnings.slice(0,9).map((x,i)=>`<div class="wr-intel-line ${i===0?'encounter':'warning'}">${i===0?'◆':'⚠'} ${esc(x)}</div>`).join(''):'<div class="wr-intel-line good">✓ No major composition warnings.</div>';
    document.getElementById('wrIntelRecommendations').innerHTML=r.recommendations.length?r.recommendations.slice(0,6).map(x=>`<div class="wr-intel-line action">→ ${esc(x)}</div>`).join(''):'<div class="wr-intel-line good">✓ Current party structure has no immediate placement recommendation.</div>';
  }
  window.renderRaidIntelligence=render;document.addEventListener('DOMContentLoaded',()=>{render();setTimeout(render,250)});document.addEventListener('click',()=>setTimeout(render,25));document.addEventListener('drop',()=>setTimeout(render,50));
})();
