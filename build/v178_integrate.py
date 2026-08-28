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

# Battle.net-style character payloads can represent race/gender as objects
# (for example {type:'MALE',name:'Male'}) rather than plain strings.  The
# protected v1.7.26 snapshot deliberately copied those fields verbatim, so
# normalize them at the v1.7.28 integration layer without modifying the
# known-good v1.7.26 source block.
OLD_RACE="race:norm(record?.race||base.race),gender:record?.gender??base.gender??null"
NEW_RACE="race:norm(record?.race?.name??record?.race?.type??record?.race?.id??record?.race??base?.race?.name??base?.race?.type??base?.race?.id??base.race),gender:(record?.gender?.type??record?.gender?.name??record?.gender?.id??record?.gender??record?.sex?.type??record?.sex?.name??record?.sex??base?.gender?.type??base?.gender?.name??base?.gender?.id??base.gender??base?.sex?.type??base?.sex?.name??base?.sex??null)"
if OLD_RACE in h:
    h=h.replace(OLD_RACE,NEW_RACE,1)
elif NEW_RACE not in h:
    raise RuntimeError('Protected Inspect race/gender snapshot expression not found')

if "window.WOTLK_TO_RETAIL_DISPLAY_ID_API=undefined" not in h: raise RuntimeError('Classic display-ID mode missing')
required=['wr-character-model-stage','generateModels(aspect','/item-appearance?id=','WarRoomCharacterModelManifest',NEW_RACE]
for marker in required:
    if marker not in h: raise RuntimeError('Protected v1.7.26 3D/appearance marker missing: '+marker)
if h.count("VIEWER_SRC='/modelviewer/classic/viewer/viewer.min.js'")!=1: raise RuntimeError('Local Classic renderer route not unique')
if "VIEWER_SRC='https://wow.zamimg.com/modelviewer/" in h: raise RuntimeError('Direct Zam renderer dependency survived integration')
index.write_text(h,encoding='utf-8')
print('War Room v'+version+' 3D stage routed through local Classic model proxy with normalized race/gender metadata')
