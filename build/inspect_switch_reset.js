/* War Room v1.7.26 - Inspect character switch isolation */
(function(){
  function clear(scope){if(!scope?.isConnected)return;for(const card of scope.querySelectorAll('[data-wr-gear-card="1"],[data-wr-slot]')){for(const n of card.querySelectorAll(':scope > .wr-live-item-icon,:scope > .wr-live-item-details'))n.remove();card.__wrTooltipItem=null;card.style.borderColor='';card.style.boxShadow='';for(const n of card.children)if(n.matches?.('svg,img,.icon,[class*="icon"]')&&!n.classList.contains('wr-live-item-icon'))n.style.display=''}const h=[...scope.querySelectorAll('*')].find(e=>/EQUIPMENT MATRIX/i.test((e.textContent||'').trim())&&!e.children.length);if(h)h.textContent=h.textContent.replace(/LIVE ARMORY EQUIPMENT/i,'AWAITING VERIFIED ARMORY FEED');const t=document.querySelector('.wr-wow-tooltip');if(t)t.style.display='none'}
  window.addEventListener('warroom:inspect-character-changing',e=>clear(e?.detail?.scope));
  window.WarRoomInspectSwitchReset={clear};
})();
