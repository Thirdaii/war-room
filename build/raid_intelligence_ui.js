/* War Room v1.7 - live Raid Intelligence dashboard */
(function(){
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function ensurePanel(){
    let host=document.getElementById('wrRaidIntelLive');
    if(host)return host;
    const anchor=document.getElementById('raidIntelligence')||document.getElementById('raidFrame');
    if(!anchor)return null;
    host=document.createElement('section');host.id='wrRaidIntelLive';host.className='wr-intel-live';
    host.innerHTML='<div class="wr-intel-head"><div><span class="wr-intel-kicker">TBC PHASE 3</span><h2>Raid Intelligence</h2></div><div class="wr-intel-score" id="wrIntelScore">--</div></div><div class="wr-intel-grid"><div class="wr-intel-block"><h3>Role Balance</h3><div id="wrIntelRoles"></div></div><div class="wr-intel-block"><h3>Critical Coverage</h3><div id="wrIntelCoverage"></div></div><div class="wr-intel-block wide"><h3>Command Warnings</h3><div id="wrIntelWarnings"></div></div><div class="wr-intel-block wide"><h3>Recommended Actions</h3><div id="wrIntelRecommendations"></div></div></div>';
    anchor.parentNode.insertBefore(host,anchor.nextSibling);return host;
  }
  function pill(label,value){return `<div class="wr-intel-role"><span>${esc(label)}</span><b>${value||0}</b></div>`;}
  function render(){
    if(!window.WarRoomRaidIntelligence)return;
    const host=ensurePanel();if(!host)return;const r=window.WarRoomRaidIntelligence.analyze();
    const score=document.getElementById('wrIntelScore');score.textContent=r.score+'%';score.dataset.grade=r.score>=85?'ready':r.score>=65?'warn':'danger';
    document.getElementById('wrIntelRoles').innerHTML=['Tank','Healer','Melee','Ranged'].map(x=>pill(x,r.roles[x])).join('');
    document.getElementById('wrIntelCoverage').innerHTML=r.coverage.map(x=>`<div class="wr-intel-check ${x.ok?'ok':'miss'}"><span>${x.ok?'✓':'!'}</span>${esc(x.name)}</div>`).join('');
    document.getElementById('wrIntelWarnings').innerHTML=r.warnings.length?r.warnings.slice(0,8).map(x=>`<div class="wr-intel-line warning">⚠ ${esc(x)}</div>`).join(''):'<div class="wr-intel-line good">✓ No major composition warnings.</div>';
    document.getElementById('wrIntelRecommendations').innerHTML=r.recommendations.length?r.recommendations.slice(0,6).map(x=>`<div class="wr-intel-line action">→ ${esc(x)}</div>`).join(''):'<div class="wr-intel-line good">✓ Current party structure has no immediate placement recommendation.</div>';
  }
  window.renderRaidIntelligence=render;
  document.addEventListener('DOMContentLoaded',()=>{render();setTimeout(render,250);});
  document.addEventListener('click',()=>setTimeout(render,25));
  document.addEventListener('drop',()=>setTimeout(render,50));
})();
