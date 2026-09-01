from pathlib import Path
import sys
root=Path(sys.argv[1]); p=root/'index.html'; h=p.read_text(encoding='utf-8')
MARK='War Room v1.7.28 - V27 Horde command-center visual overhaul'
if MARK in h:
    print('V27 visual overhaul already installed'); raise SystemExit(0)

# Preserve the live/current armory name for identity and API calls while restoring the
# guild's canonical accented spelling from the embedded fallback snapshot for display.
helper_old="const norm=v=>String(v??'').trim(), key=v=>norm(v).toLocaleLowerCase(), rankLabel=raw=>{const rn=norm(raw?.rank_name||raw?.rankName);"
helper_new="const norm=v=>String(v??'').trim(), key=v=>norm(v).toLocaleLowerCase(), fold=v=>norm(v).normalize('NFKD').replace(/[\\u0300-\\u036f]/g,'').replace(/[øØ]/g,'o').replace(/[ðÐ]/g,'d').replace(/[þÞ]/g,'th').replace(/[æÆ]/g,'ae').replace(/[œŒ]/g,'oe').replace(/ß/g,'ss').toLocaleLowerCase(), legacyFold=new Map([...legacy.values()].map(p=>[fold(p?.name),p])), rankLabel=raw=>{const rn=norm(raw?.rank_name||raw?.rankName);"
if helper_old in h:
    h=h.replace(helper_old,helper_new,1)
elif helper_new not in h:
    raise RuntimeError('V27 live roster helper anchor missing')

old_lookup="const old=legacy.get(key(name))||roster.find(p=>key(p?.name)===key(name))||{};"
new_lookup="const old=legacy.get(key(name))||legacyFold.get(fold(name))||roster.find(p=>key(p?.name)===key(name)||fold(p?.displayName||p?.name)===fold(name))||{};"
if old_lookup in h:
    h=h.replace(old_lookup,new_lookup,1)
elif new_lookup not in h:
    raise RuntimeError('V27 canonical name lookup anchor missing')

old_obj="const p={...old,...raw,name,level:70,class:norm(raw?.class||raw?.className||raw?.class_name||old.class),race:norm(raw?.race||raw?.raceName||raw?.race_name||old.race),rank:rankLabel(raw)||norm(old.rank||'Member')};"
new_obj="const p={...old,...raw,name,liveName:name,displayName:norm(old?.displayName||old?.name||name),level:70,class:norm(raw?.class||raw?.className||raw?.class_name||old.class),race:norm(raw?.race||raw?.raceName||raw?.race_name||old.race),rank:rankLabel(raw)||norm(old.rank||'Member')};"
if old_obj in h:
    h=h.replace(old_obj,new_obj,1)
elif new_obj not in h:
    raise RuntimeError('V27 member displayName anchor missing')

# Search matches both canonical accented display spelling and the live source name.
old_search='const arr=roster.filter(x=>(!q||x.name.toLowerCase().includes(q))&&(!cf||x.class===cf)&&(!rf||x.rank===rf));'
new_search="const wrNameFold=v=>String(v??'').normalize('NFKD').replace(/[\\u0300-\\u036f]/g,'').replace(/[øØ]/g,'o').replace(/[ðÐ]/g,'d').replace(/[þÞ]/g,'th').replace(/[æÆ]/g,'ae').replace(/[œŒ]/g,'oe').replace(/ß/g,'ss').toLowerCase(); const fq=wrNameFold(q); const arr=roster.filter(x=>(!q||String(x.name||'').toLowerCase().includes(q)||String(x.displayName||'').toLowerCase().includes(q)||wrNameFold(x.name).includes(fq)||wrNameFold(x.displayName).includes(fq))&&(!cf||x.class===cf)&&(!rf||x.rank===rf));"
if old_search in h:
    h=h.replace(old_search,new_search,1)
elif new_search not in h:
    raise RuntimeError('V27 roster search anchor missing')

# Display canonical spelling without changing internal keys / API identity.
old_card='<span class="class-crest">${classGlyphs[x.class]||"•"}</span>${x.name}</div>'
new_card='<span class="class-crest">${classGlyphs[x.class]||"•"}</span>${x.displayName||x.name}</div>'
if old_card in h:
    h=h.replace(old_card,new_card,1)
elif new_card not in h:
    raise RuntimeError('V27 roster card display anchor missing')

old_raid='<b>${n}</b> <span style="color:${classColors[p.class]}">• ${p.class}</span>'
new_raid='<b>${p.displayName||n}</b> <span style="color:${classColors[p.class]}">• ${p.class}</span>'
if old_raid in h:
    h=h.replace(old_raid,new_raid,1)
elif new_raid not in h:
    raise RuntimeError('V27 raid display anchor missing')

for old,new in [
    ('wrQuery("#dName").textContent=p.name;','wrQuery("#dName").textContent=p.displayName||p.name;'),
    ('wrQuery("#dPreviewName").textContent=p.name;','wrQuery("#dPreviewName").textContent=p.displayName||p.name;'),
    ('wrQuery("#fixedDossierName").textContent=p.name;','wrQuery("#fixedDossierName").textContent=p.displayName||p.name;'),
    ("${esc(p.name||'Unknown')}","${esc(p.displayName||p.name||'Unknown')}")
]:
    if old in h: h=h.replace(old,new)

# Premium one-pass Phase 1+2+3 visual overhaul. CSS-only so protected logic/3D remains untouched.
style=r'''
<style id="wr-v27-command-center-style">
/* War Room v1.7.28 - V27 Horde command-center visual overhaul */
:root{
  --wr-void:#050403;--wr-iron:#120d0b;--wr-iron2:#1d120f;--wr-steel:#3f3029;
  --wr-blood:#5f110d;--wr-blood2:#9f2419;--wr-ember:#e55b2d;--wr-gold:#d4a350;--wr-gold2:#f0cc82;
  --wr-line:#52372d;--wr-line-hot:#8b4a35;--wr-parch:#ead8bd;--wr-smoke:#9a8878;
}
html{background:#050403}
body{
  font-family:"Segoe UI Variable","Segoe UI",Tahoma,Arial,sans-serif!important;
  background:
    radial-gradient(ellipse at 12% -8%,rgba(141,28,18,.36),transparent 36%),
    radial-gradient(ellipse at 92% 8%,rgba(211,114,47,.12),transparent 30%),
    linear-gradient(180deg,#100806 0,#070504 28%,#030303 100%)!important;
  background-attachment:fixed!important;
}
body:before{
  content:""!important;position:fixed!important;inset:0!important;pointer-events:none!important;z-index:-2!important;opacity:.24!important;
  background:
    linear-gradient(90deg,rgba(0,0,0,.82),rgba(0,0,0,.26) 36%,rgba(0,0,0,.38) 68%,rgba(0,0,0,.86)),
    url("assets/images/right_art.jpg") right top/620px auto no-repeat!important;
  filter:saturate(1.1) contrast(1.08);
}
body:after{
  content:"";position:fixed;inset:0;pointer-events:none;z-index:9999;opacity:.13;
  background:
    repeating-linear-gradient(0deg,rgba(255,255,255,.014) 0 1px,transparent 1px 4px),
    repeating-linear-gradient(90deg,transparent 0 47px,rgba(255,169,91,.012) 48px 49px,transparent 50px 96px);
  mix-blend-mode:screen;
}
.shell{max-width:1840px!important;padding:10px 12px 4px!important;position:relative}
.shell:before{content:"";position:absolute;inset:0 4px auto;height:1px;background:linear-gradient(90deg,transparent,#9d3a28,#d8a750,#9d3a28,transparent);opacity:.85}
.hero{
  min-height:178px!important;border-radius:3px!important;border:1px solid #6c3528!important;padding:20px 26px!important;
  background:
    linear-gradient(90deg,rgba(7,5,4,.88),rgba(26,8,6,.64) 34%,rgba(8,5,4,.76) 72%,rgba(4,3,3,.92)),
    linear-gradient(180deg,transparent 64%,rgba(0,0,0,.72)),
    url("assets/images/header.jpg") center 10%/cover no-repeat!important;
  box-shadow:0 20px 55px rgba(0,0,0,.6),inset 0 1px rgba(255,211,137,.10),inset 0 -1px rgba(0,0,0,.8)!important;
}
.hero:before{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(90deg,rgba(0,0,0,.28),transparent 27%,transparent 70%,rgba(0,0,0,.34));box-shadow:inset 0 0 52px #000}
.hero:after{color:rgba(242,190,102,.07)!important;text-shadow:0 2px #000;font-family:Georgia,serif!important;letter-spacing:8px!important}
.brand h1{font-family:Georgia,"Times New Roman",serif!important;font-size:44px!important;color:#f1d5ad!important;text-transform:uppercase;text-shadow:0 2px 0 #1c0906,0 0 18px rgba(221,90,44,.45)!important}
.brand .sub{color:#c9ae8d!important;font-size:11px!important;letter-spacing:1.6px;text-transform:uppercase}
.badge{border-radius:2px!important;border-color:#8b4a35!important;background:linear-gradient(180deg,rgba(85,20,14,.96),rgba(25,9,7,.96))!important;color:#f2c990!important;box-shadow:0 8px 22px #000,inset 0 1px rgba(255,215,149,.11)!important}
.topbar{margin:7px 0!important;padding:5px;border:1px solid #402b24;background:rgba(7,5,4,.78);box-shadow:inset 0 1px rgba(255,255,255,.025)}
.quick,input,select,button{border-radius:2px!important}
.quick{background:linear-gradient(180deg,#21140f,#0c0807)!important;border-color:#51362c!important;color:#d9c1a1!important;box-shadow:inset 0 1px rgba(255,220,164,.04)}
.quick:hover,button:hover{border-color:#9a563e!important;color:#f4d7a8!important;background:linear-gradient(180deg,#32160f,#120a07)!important}
.stats{gap:6px!important;margin-bottom:7px!important}
.stat{position:relative;border-radius:2px!important;border-color:#463027!important;background:linear-gradient(145deg,rgba(29,18,14,.96),rgba(8,6,5,.98))!important;padding:11px 13px!important;box-shadow:0 8px 20px rgba(0,0,0,.28),inset 0 1px rgba(255,209,139,.04)!important;overflow:hidden}
.stat:after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:linear-gradient(90deg,transparent,#8a4834,transparent)}
.stat .n{font-family:Georgia,serif!important;color:#edcf9b!important;text-shadow:0 1px #000}.stat .l{color:#8d7767!important;letter-spacing:1.25px!important}
.layout{gap:6px!important}
.panel,.bottom-panel,.overview-left,.overview-right,.wr-intel-live{
  border-radius:2px!important;border-color:#4a3129!important;
  background:linear-gradient(180deg,rgba(20,13,11,.97),rgba(7,5,4,.985))!important;
  box-shadow:0 14px 34px rgba(0,0,0,.42),inset 0 1px rgba(255,214,154,.035)!important;
}
.panel{position:relative}.panel:before{content:"";position:absolute;z-index:2;left:0;right:0;top:0;height:2px;background:linear-gradient(90deg,#3b100d,#a63825 25%,#d0a354 50%,#7b2b20 75%,#2d0d0b);opacity:.68;pointer-events:none}
.panel-head{padding:10px 12px!important;border-bottom-color:#482c23!important;background:linear-gradient(90deg,#2f110d,#1b0d0a 45%,#0c0807)!important;box-shadow:inset 0 -1px #080504}
.panel-head h2{font:700 16px Georgia,serif!important;color:#efd1a5!important;text-transform:uppercase;letter-spacing:1px!important;text-shadow:0 1px #000}
.panel-head .hint{color:#8e7868!important}
.wr-nav{position:relative;overflow:hidden;border-color:#55352b!important;background:linear-gradient(180deg,rgba(19,11,9,.95),rgba(5,4,3,.99))!important;box-shadow:0 12px 28px rgba(0,0,0,.4)}
.wr-nav:before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.18),rgba(0,0,0,.82)),url("assets/images/left_banner.jpg") center top/cover no-repeat;opacity:.34;pointer-events:none}
.wr-nav>*{position:relative;z-index:1}.wr-nav-title{font-family:Georgia,serif!important;letter-spacing:1.4px!important;color:#e8c88f!important;background:linear-gradient(90deg,rgba(95,20,14,.94),rgba(18,10,8,.94))!important;border-bottom:1px solid #6e382b}
.wr-nav-btn{border-radius:2px!important;border-color:#463029!important;background:linear-gradient(180deg,rgba(25,16,13,.93),rgba(8,6,5,.96))!important;color:#bca791!important;box-shadow:inset 0 1px rgba(255,214,145,.025)}
.wr-nav-btn:hover{background:linear-gradient(90deg,#38120e,#120b09)!important}.wr-nav-btn.active{background:linear-gradient(90deg,#60170f,#1a0d0a 72%)!important;color:#f0d2a3!important;border-color:#8b4b36!important;box-shadow:inset 3px 0 #e0ad56,0 0 20px rgba(137,38,25,.18)!important}
#rosterPanel{background:linear-gradient(180deg,rgba(19,12,10,.97),rgba(5,4,3,.99))!important}
.roster{scrollbar-width:thin;scrollbar-color:#66372a #090605}
.player-card{position:relative;overflow:hidden;border-radius:2px!important;margin:4px 6px!important;padding:8px 10px!important;border-color:#392922!important;background:linear-gradient(90deg,rgba(15,11,9,.98),rgba(8,6,5,.99))!important;box-shadow:inset 0 1px rgba(255,255,255,.018)!important}
.player-card:before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--class-accent,#79523b);box-shadow:0 0 11px color-mix(in srgb,var(--class-accent,#79523b) 45%,transparent)}
.player-card:after{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(circle at 84% 30%,rgba(179,66,31,.055),transparent 33%)}
.player-card:hover{transform:translateY(-1px)!important;border-color:#684536!important;background:linear-gradient(90deg,rgba(31,17,13,.99),rgba(8,6,5,.99))!important;box-shadow:0 8px 20px rgba(0,0,0,.32),inset 0 1px rgba(255,218,158,.035)!important}
.player-card .name{font-family:"Segoe UI Variable","Segoe UI",Tahoma,Arial,sans-serif!important;font-size:13px!important;font-weight:800!important;letter-spacing:.12px!important;text-shadow:0 1px 2px #000}
.class-crest{filter:drop-shadow(0 0 5px currentColor)}
.player-meta{gap:4px!important;margin-top:5px!important}.tag{border-radius:2px!important;font-size:7px!important;padding:3px 5px!important;border-color:#463127!important;background:#090605!important;color:#ad9886!important;text-transform:none}.tag.role{color:#d9b76f!important}.tag.gs{color:#e59a72!important}.tag.ilvl{color:#95bccc!important}
.card-actions button{min-width:58px!important;border-color:#53362b!important;background:linear-gradient(180deg,#160d0a,#070504)!important;color:#d8b983!important;font-weight:800!important}.card-actions button:hover{border-color:#9b573d!important;color:#ffe0a9!important}
.race-portrait,.avatar{box-shadow:0 0 0 1px #0a0605,0 0 0 2px #6b432f,0 5px 16px #000!important}
.group{border-radius:2px!important;border-color:#493028!important;background:#070504!important;box-shadow:0 10px 22px rgba(0,0,0,.28)!important}.group:hover{border-color:#704334!important}.gtitle{background:linear-gradient(90deg,#40140f,#180c09 56%,#090605)!important;color:#e7c792!important;border-bottom:1px solid #4e2f26!important;font-family:Georgia,serif!important;letter-spacing:1.2px!important}.slot{background:linear-gradient(90deg,#0e0907,#080605)!important;border-left:2px solid transparent!important}.slot:not(.empty):hover{border-left-color:#b2603d!important;background:linear-gradient(90deg,#24120d,#090605)!important}.slot.empty{color:#55473f!important}.slot.drop,.wr-slot-drop-ready{outline:1px solid #c26a43!important;box-shadow:inset 0 0 18px rgba(194,106,67,.09)!important}
.wr-command-card{border-radius:2px!important;border-color:#4d332a!important;background:linear-gradient(145deg,#1e120e,#080605 72%)!important;box-shadow:0 9px 22px rgba(0,0,0,.26),inset 0 1px rgba(255,214,145,.035)!important}.wr-command-card.primary{background:linear-gradient(135deg,#58170f,#190d09 70%)!important;border-color:#7e4734!important}.wr-command-card strong{color:#edc995!important;text-shadow:0 1px #000}.wr-command-card:hover{border-color:#9a583f!important;box-shadow:0 12px 26px rgba(0,0,0,.34),0 0 14px rgba(130,41,27,.11)!important}
.wr-intel-live{background:linear-gradient(160deg,rgba(38,14,10,.96),rgba(7,5,4,.985) 48%),url("assets/images/right_art.jpg") center top/cover no-repeat!important;background-blend-mode:multiply!important}.wr-intel-head h2{color:#efcf9e!important;text-shadow:0 1px #000}.wr-intel-score{box-shadow:0 0 0 2px #0a0605,0 0 18px rgba(210,122,53,.12),inset 0 0 20px #000!important}
.wr-dossier-fixed{position:relative;overflow:hidden;border-radius:2px!important;border-color:#523329!important;background:linear-gradient(180deg,rgba(13,8,7,.66),rgba(5,4,3,.98))!important;box-shadow:0 12px 26px rgba(0,0,0,.4)!important}.wr-dossier-fixed:before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.16),rgba(0,0,0,.92)),url("assets/images/right_art.jpg") center 12%/cover no-repeat;opacity:.38;pointer-events:none}.wr-dossier-fixed>*{position:relative;z-index:1}.wr-dossier-portrait{border-radius:1px!important;border-color:#67402f!important;background:linear-gradient(180deg,rgba(8,5,4,.04),rgba(5,3,3,.72)),url("assets/images/right_art.jpg") center 18%/cover no-repeat!important;box-shadow:inset 0 0 35px #000!important}.wr-dossier-name,.wr-identity-name{font-family:Georgia,"Times New Roman",serif!important;color:#f0d1a2!important;text-shadow:0 2px 3px #000!important}.wr-dossier-metric,.detail-box,.wr-spec-confidence,.wr-refresh-detail,.wr-character-data{border-radius:2px!important;border-color:#493027!important;background:rgba(7,5,4,.92)!important}.wr-dossier-metric b{color:#edc88e!important}
input,select{border-color:#51362b!important;background:#080605!important;color:#ddc9ae!important;box-shadow:inset 0 2px 8px rgba(0,0,0,.5)}input:focus,select:focus{outline:none!important;border-color:#a55a3e!important;box-shadow:0 0 0 1px rgba(197,103,65,.18),inset 0 2px 8px rgba(0,0,0,.55)!important}
#wrLiveRosterStatus{font-family:"Segoe UI Variable","Segoe UI",Tahoma,Arial,sans-serif!important;letter-spacing:.15px}#wrLiveRosterStatus[data-state="live"]{color:#91d49e!important;text-shadow:0 0 8px rgba(93,190,112,.18)}#wrLiveRosterStatus[data-state="live"]:before{animation:wrV27LivePulse 2.6s ease-in-out infinite}@keyframes wrV27LivePulse{0%,100%{box-shadow:0 0 5px rgba(101,195,125,.42)}50%{box-shadow:0 0 13px rgba(101,195,125,.82)}}
.footer{position:relative;margin:8px 0 0!important;min-height:44px;padding:17px 18px 8px!important;border-top:1px solid #473027;background:linear-gradient(180deg,rgba(12,8,6,.62),rgba(3,3,3,.92)),url("assets/images/bottom.jpg") center bottom/cover no-repeat!important;color:#836f60!important;text-transform:uppercase;letter-spacing:.6px}.footer:before{content:"VICTORY OR DEATH";position:absolute;left:18px;top:8px;color:#9a382d;font:700 10px Georgia,serif;letter-spacing:2px}.footer:after{color:#9a806d!important}
::-webkit-scrollbar{width:9px;height:9px}::-webkit-scrollbar-track{background:#070504}::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#633425,#321c16);border:2px solid #090605;border-radius:0}::-webkit-scrollbar-thumb:hover{background:linear-gradient(180deg,#8c4a34,#4b271d)}
@media(max-width:1100px){.hero{min-height:150px!important}.brand h1{font-size:34px!important}}
</style>
<script id="wr-v27-command-center-script">
/* War Room v1.7.28 - V27 Horde command-center visual overhaul */
(function(){
  window.WarRoomDisplayName=function(p){return String((p&&p.displayName)||(p&&p.name)||'').normalize('NFC')};
  // Keep every visible canonical name composed so accented Latin glyphs render reliably in Edge/Windows.
  function repairVisibleNames(){
    try{
      for(const p of (window.roster||roster||[]))if(p&&p.displayName)p.displayName=String(p.displayName).normalize('NFC');
    }catch(_){ }
  }
  repairVisibleNames();
  window.addEventListener('focus',repairVisibleNames);
  console.info('[War Room v1.7.28] V27 Horde command-center visuals + canonical character names active');
})();
</script>
'''
if '</body>' not in h: raise RuntimeError('V27 body anchor missing')
h=h.replace('</body>',style+'\n</body>',1)
p.write_text(h,encoding='utf-8')
print('War Room v1.7.28 V27 Horde command-center visual overhaul installed')
