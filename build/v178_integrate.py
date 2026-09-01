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

OLD_RACE="race:norm(record?.race||base.race),gender:record?.gender??base.gender??null"
NEW_RACE="race:norm(record?.race?.name??record?.race?.type??record?.race?.id??record?.race??base?.race?.name??base?.race?.type??base?.race?.id??base.race),gender:(record?.gender?.type??record?.gender?.name??record?.gender?.id??record?.gender??record?.sex?.type??record?.sex?.name??record?.sex??base?.gender?.type??base?.gender?.name??base?.gender?.id??base.gender??base?.sex?.type??base?.sex?.name??base?.sex??null)"
if OLD_RACE in h:
    h=h.replace(OLD_RACE,NEW_RACE,1)
elif NEW_RACE not in h:
    raise RuntimeError('Protected Inspect race/gender snapshot expression not found')

# The upstream armory currently omits gender for some Classic profiles. Keep
# rendering available by falling back to a remembered per-character choice,
# defaulting to male only when no metadata/choice exists. The UI below exposes
# a Male/Female switch and stores the user's choice locally for that character.
OLD_BUILD="async function build(character){if(!character)return null;const race=raceId(character.race),gender=genderId(character.gender);if(!race||gender==null)return{ready:false,reason:'missing-race-or-gender',race,gender,items:[]};"
NEW_BUILD="async function build(character){if(!character)return null;const race=raceId(character.race);let gender=genderId(character.gender),genderFallback=false;const gkey='wr-gender:'+key(character.name||'');if(gender==null){try{const saved=localStorage.getItem(gkey);if(saved==='0'||saved==='1')gender=Number(saved)}catch(e){}if(gender==null)gender=1;genderFallback=true}if(!race)return{ready:false,reason:'missing-race',race,gender,items:[]};"
if OLD_BUILD in h:
    h=h.replace(OLD_BUILD,NEW_BUILD,1)
elif NEW_BUILD not in h:
    raise RuntimeError('Character model manifest build signature not found')
h=h.replace("return{ready:true,race,gender,...customization(character),items,sourceCharacter:character.name||'',resolvedItems:items.length};","return{ready:true,race,gender,genderFallback,...customization(character),items,sourceCharacter:character.name||'',resolvedItems:items.length};",1)

IDENTITY_MARKER='/* War Room v1.7.28 - Inspect identity strip */'
identity_css='''\n/* War Room v1.7.28 - Inspect identity strip */\n#drawer .wr-inspect-preview{display:none!important}\n#drawer .wr-identity-strip{display:flex;align-items:center;justify-content:space-between;gap:16px;margin:6px 5px 10px;padding:12px 14px;border:1px solid #4a3128;background:linear-gradient(90deg,rgba(45,18,13,.96),rgba(16,10,9,.98) 48%,rgba(8,7,7,.98));box-shadow:inset 3px 0 #c28c46,0 5px 18px rgba(0,0,0,.24)}\n#drawer .wr-identity-main{min-width:0}\n#drawer .wr-identity-name{font:700 22px Georgia,serif;color:#f0d8b8;letter-spacing:.01em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}\n#drawer .wr-identity-meta{display:flex;flex-wrap:wrap;gap:6px;margin-top:5px}\n#drawer .wr-identity-chip{padding:3px 7px;border:1px solid #4a342b;background:rgba(8,6,6,.65);color:#a9917c;font-size:8px;font-weight:900;letter-spacing:.09em;text-transform:uppercase}\n#drawer .wr-identity-chip.rank{border-color:#76512f;color:#d2a55d}\n#drawer .wr-identity-kicker{flex:0 0 auto;color:#6f5d50;font-size:8px;font-weight:900;letter-spacing:.16em;text-transform:uppercase;text-align:right}\n#drawer .wr-gender-fallback{position:absolute;z-index:5;left:10px;bottom:8px;display:flex;gap:5px;align-items:center;font-size:8px;color:#8e866f;text-transform:uppercase;letter-spacing:.05em}\n#drawer .wr-gender-fallback button{pointer-events:auto;border:1px solid #5f4934;background:rgba(12,9,8,.9);color:#c8b98c;padding:3px 6px;font-size:8px;font-weight:800;cursor:pointer}\n#drawer .wr-gender-fallback button.active{border-color:#c28c46;color:#f0d8b8}\n@media(max-width:620px){#drawer .wr-identity-strip{align-items:flex-start;padding:10px 11px}#drawer .wr-identity-name{font-size:18px}#drawer .wr-identity-kicker{display:none}}\n'''
if IDENTITY_MARKER not in h:
    if '</style>' not in h: raise RuntimeError('Unable to locate style block for Inspect identity strip')
    h=h.replace('</style>',identity_css+'</style>',1)

# Safe late-body helper: unlike the previous failed pass, this is appended just
# before </body>, after War Room's bootstrap scripts have already been defined.
HELPER_MARKER='/* War Room v1.7.28 - Late identity and gender helper */'
helper=r'''\n<script>\n/* War Room v1.7.28 - Late identity and gender helper */\n(function(){\n const norm=s=>String(s??'').trim();\n const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));\n function installIdentity(scope,p){\n   if(!scope?.isConnected||!p)return;\n   let bar=scope.querySelector(':scope > .wr-identity-strip');\n   if(!bar){bar=document.createElement('div');bar.className='wr-identity-strip';scope.insertBefore(bar,scope.firstChild);}\n   const rank=norm(p.rank||p.guildRank||p.guild_rank||p.rankName||p.guildRankName||'Member');\n   const cls=norm(p.class||p.className||'Unknown Class');\n   const race=norm(p.race||'Unknown Race');\n   const role=norm(p.spec||p.activeSpec||p.talentSpec||p.role||'');\n   bar.innerHTML=`<div class="wr-identity-main"><div class="wr-identity-name">${esc(p.name||'Unknown')}</div><div class="wr-identity-meta"><span class="wr-identity-chip">${esc(cls)}</span><span class="wr-identity-chip">${esc(race)}</span>${role?`<span class="wr-identity-chip">${esc(role)}</span>`:''}<span class="wr-identity-chip rank">${esc(rank)}</span></div></div><div class="wr-identity-kicker">Raider Dossier</div>`;\n }\n function installGender(scope,p){\n   if(!scope?.isConnected||!p)return;\n   setTimeout(()=>{\n     const stage=scope.querySelector('#wr-character-model-stage');if(!stage)return;\n     let box=stage.querySelector('.wr-gender-fallback');\n     if(!box){box=document.createElement('div');box.className='wr-gender-fallback';stage.appendChild(box);}\n     const key='wr-gender:'+norm(p.name).toLowerCase().replace(/[^a-z0-9_]+/g,'');\n     let g=null;try{const v=localStorage.getItem(key);if(v==='0'||v==='1')g=Number(v)}catch(e){}\n     const explicit=window.WarRoomCharacterModelManifest?.genderId?.(p.gender);\n     if(explicit===0||explicit===1){box.remove();return;}\n     if(g==null)g=1;\n     box.innerHTML='<span>Gender fallback</span><button data-g="1">Male</button><button data-g="0">Female</button>';\n     for(const b of box.querySelectorAll('button')){const n=Number(b.dataset.g);if(n===g)b.classList.add('active');b.onclick=()=>{try{localStorage.setItem(key,String(n))}catch(e){};p.gender=n;window.WarRoomCharacterModelStage?.render?.(p)}}\n   },0);\n }\n window.addEventListener('warroom:inspect-character-ready',e=>{const d=e.detail||{};installIdentity(d.scope,d.character);installGender(d.scope,d.character)});\n})();\n</script>\n'''
if HELPER_MARKER not in h:
    if '</body>' not in h: raise RuntimeError('Unable to locate body end for safe late helper')
    h=h.replace('</body>',helper+'</body>',1)

if "window.WOTLK_TO_RETAIL_DISPLAY_ID_API=undefined" not in h: raise RuntimeError('Classic display-ID mode missing')
required=['wr-character-model-stage','generateModels(aspect','/item-appearance?id=','WarRoomCharacterModelManifest',NEW_RACE,IDENTITY_MARKER,HELPER_MARKER,'genderFallback']
for marker in required:
    if marker not in h: raise RuntimeError('v1.7.28 integration marker missing: '+marker)
if h.count("VIEWER_SRC='/modelviewer/classic/viewer/viewer.min.js'")!=1: raise RuntimeError('Local Classic renderer route not unique')
if "VIEWER_SRC='https://wow.zamimg.com/modelviewer/" in h: raise RuntimeError('Direct Zam renderer dependency survived integration')
index.write_text(h,encoding='utf-8')
print('War Room v'+version+' all-in-one integration complete: roster-safe identity + gender fallback + local 3D proxy')
