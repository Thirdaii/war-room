from pathlib import Path
import re,sys
root=Path(sys.argv[1]); index=root/'index.html'
h=index.read_text(encoding='utf-8')
version=Path(__file__).with_name('version.txt').read_text(encoding='utf-8').strip()
LIVE="VIEWER_SRC='https://wow.zamimg.com/modelviewer/live/viewer/viewer.min.js',CONTENT='https://wow.zamimg.com/modelviewer/classic/'"
CLASSIC="VIEWER_SRC='https://wow.zamimg.com/modelviewer/classic/viewer/viewer.min.js',CONTENT='https://wow.zamimg.com/modelviewer/classic/'"
LOCAL="VIEWER_SRC='/modelviewer/classic/viewer/viewer.min.js',CONTENT=location.origin+'/modelviewer/classic/'"
if LOCAL not in h:
    if LIVE in h: h=h.replace(LIVE,LOCAL,1)
    elif CLASSIC in h: h=h.replace(CLASSIC,LOCAL,1)
    else: raise RuntimeError('Protected 3D viewer constants not found; refusing unsafe rewrite')

# Battle.net-style character payloads can represent race/gender as objects.
OLD_RACE="race:norm(record?.race||base.race),gender:record?.gender??base.gender??null"
NEW_RACE="race:norm(record?.race?.name??record?.race?.type??record?.race?.id??record?.race??base?.race?.name??base?.race?.type??base?.race?.id??base.race),gender:(record?.gender?.type??record?.gender?.name??record?.gender?.id??record?.gender??record?.sex?.type??record?.sex?.name??record?.sex??base?.gender?.type??base?.gender?.name??base?.gender?.id??base.gender??base?.sex?.type??base?.sex?.name??base?.sex??null)"
if OLD_RACE in h:
    h=h.replace(OLD_RACE,NEW_RACE,1)
elif NEW_RACE not in h:
    raise RuntimeError('Protected Inspect race/gender snapshot expression not found')

# Remove the old portrait/preview area entirely and replace it with a compact
# command-style identity strip at the top of the active Inspect dossier.
IDENTITY_MARKER='/* War Room v1.7.28 - Inspect identity strip */'
identity_css='''\n/* War Room v1.7.28 - Inspect identity strip */\n#drawer .wr-inspect-preview{display:none!important}\n#drawer .wr-identity-strip{display:flex;align-items:center;justify-content:space-between;gap:16px;margin:6px 5px 10px;padding:12px 14px;border:1px solid #4a3128;background:linear-gradient(90deg,rgba(45,18,13,.96),rgba(16,10,9,.98) 48%,rgba(8,7,7,.98));box-shadow:inset 3px 0 #c28c46,0 5px 18px rgba(0,0,0,.24)}\n#drawer .wr-identity-main{min-width:0}\n#drawer .wr-identity-name{font:700 22px Georgia,serif;color:#f0d8b8;letter-spacing:.01em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}\n#drawer .wr-identity-meta{display:flex;flex-wrap:wrap;gap:6px;margin-top:5px}\n#drawer .wr-identity-chip{padding:3px 7px;border:1px solid #4a342b;background:rgba(8,6,6,.65);color:#a9917c;font-size:8px;font-weight:900;letter-spacing:.09em;text-transform:uppercase}\n#drawer .wr-identity-chip.rank{border-color:#76512f;color:#d2a55d}\n#drawer .wr-identity-kicker{flex:0 0 auto;color:#6f5d50;font-size:8px;font-weight:900;letter-spacing:.16em;text-transform:uppercase;text-align:right}\n@media(max-width:620px){#drawer .wr-identity-strip{align-items:flex-start;padding:10px 11px}#drawer .wr-identity-name{font-size:18px}#drawer .wr-identity-kicker{display:none}}\n'''
identity_js=r'''\n(function(){\n const esc=s=>String(s??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c]));\n const norm=s=>String(s??'').trim();\n function ensure(scope,p){\n   if(!scope?.isConnected||!p)return;\n   let bar=scope.querySelector(':scope > .wr-identity-strip');\n   if(!bar){bar=document.createElement('div');bar.className='wr-identity-strip';scope.insertBefore(bar,scope.firstChild);}\n   const rank=norm(p.rank||p.guildRank||p.guild_rank||p.rankName||p.guildRankName||'Member');\n   const cls=norm(p.class||p.className||'Unknown Class');\n   const race=norm(p.race||'Unknown Race');\n   const role=norm(p.spec||p.activeSpec||p.talentSpec||p.role||'');\n   bar.innerHTML=`<div class="wr-identity-main"><div class="wr-identity-name">${esc(p.name||'Unknown')}</div><div class="wr-identity-meta"><span class="wr-identity-chip">${esc(cls)}</span><span class="wr-identity-chip">${esc(race)}</span>${role?`<span class="wr-identity-chip">${esc(role)}</span>`:''}<span class="wr-identity-chip rank">${esc(rank)}</span></div></div><div class="wr-identity-kicker">Raider Dossier</div>`;\n }\n window.addEventListener('warroom:inspect-character-ready',e=>ensure(e?.detail?.scope,e?.detail?.character));\n})();\n'''
if IDENTITY_MARKER not in h:
    if '</style>' not in h: raise RuntimeError('Unable to locate style block for Inspect identity strip')
    h=h.replace('</style>',identity_css+'</style>',1)
    if '</script>' not in h: raise RuntimeError('Unable to locate script block for Inspect identity strip')
    h=h.replace('</script>',identity_js+'</script>',1)

if "window.WOTLK_TO_RETAIL_DISPLAY_ID_API=undefined" not in h: raise RuntimeError('Classic display-ID mode missing')
required=['wr-character-model-stage','generateModels(aspect','/item-appearance?id=','WarRoomCharacterModelManifest',NEW_RACE,IDENTITY_MARKER,'wr-identity-strip']
for marker in required:
    if marker not in h: raise RuntimeError('Protected v1.7.26 3D/appearance marker missing: '+marker)
if h.count("VIEWER_SRC='/modelviewer/classic/viewer/viewer.min.js'")!=1: raise RuntimeError('Local Classic renderer route not unique')
if "VIEWER_SRC='https://wow.zamimg.com/modelviewer/" in h: raise RuntimeError('Direct Zam renderer dependency survived integration')
index.write_text(h,encoding='utf-8')
print('War Room v'+version+' 3D integration complete with compact Inspect identity strip')
