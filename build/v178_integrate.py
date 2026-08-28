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

# Compact the oversized character preview.  Several visual passes raised the
# portrait to 520px and CSS grid auto-placement put the subtitle onto a second
# row, which created the huge dead area visible in the Inspect drawer.
COMPACT_MARKER='/* War Room v1.7.28 - Compact Inspect preview */'
compact_css='''\n/* War Room v1.7.28 - Compact Inspect preview */\n#drawer .wr-inspect-preview{display:grid!important;grid-template-columns:230px minmax(0,1fr)!important;grid-template-rows:auto auto!important;gap:4px 14px!important;align-items:start!important;padding:8px!important}\n#drawer .wr-portrait-panel{grid-column:1!important;grid-row:1 / span 2!important;min-height:220px!important;height:220px!important}\n#drawer .wr-inspect-name{grid-column:2!important;grid-row:1!important;align-self:end!important;margin:0 0 2px!important;font-size:18px!important}\n#drawer .wr-inspect-sub{grid-column:2!important;grid-row:2!important;align-self:start!important;margin:0!important}\n@media(max-width:620px){#drawer .wr-inspect-preview{grid-template-columns:1fr!important}#drawer .wr-portrait-panel,#drawer .wr-inspect-name,#drawer .wr-inspect-sub{grid-column:1!important;grid-row:auto!important}#drawer .wr-portrait-panel{height:190px!important;min-height:190px!important}}\n'''
if COMPACT_MARKER not in h:
    if '</style>' not in h: raise RuntimeError('Unable to locate style block for compact Inspect override')
    h=h.replace('</style>',compact_css+'</style>',1)

if "window.WOTLK_TO_RETAIL_DISPLAY_ID_API=undefined" not in h: raise RuntimeError('Classic display-ID mode missing')
required=['wr-character-model-stage','generateModels(aspect','/item-appearance?id=','WarRoomCharacterModelManifest',NEW_RACE,COMPACT_MARKER]
for marker in required:
    if marker not in h: raise RuntimeError('Protected v1.7.26 3D/appearance marker missing: '+marker)
if h.count("VIEWER_SRC='/modelviewer/classic/viewer/viewer.min.js'")!=1: raise RuntimeError('Local Classic renderer route not unique')
if "VIEWER_SRC='https://wow.zamimg.com/modelviewer/" in h: raise RuntimeError('Direct Zam renderer dependency survived integration')
index.write_text(h,encoding='utf-8')
print('War Room v'+version+' 3D integration complete with compact Inspect preview')
