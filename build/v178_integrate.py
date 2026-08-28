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
if "window.WOTLK_TO_RETAIL_DISPLAY_ID_API=undefined" not in h: raise RuntimeError('Classic display-ID mode missing')
required=['wr-character-model-stage','generateModels(aspect','/item-appearance?id=','WarRoomCharacterModelManifest']
for marker in required:
    if marker not in h: raise RuntimeError('Protected v1.7.26 3D/appearance marker missing: '+marker)
if h.count("VIEWER_SRC='/modelviewer/classic/viewer/viewer.min.js'")!=1: raise RuntimeError('Local Classic renderer route not unique')
if "VIEWER_SRC='https://wow.zamimg.com/modelviewer/" in h: raise RuntimeError('Direct Zam renderer dependency survived integration')
index.write_text(h,encoding='utf-8')
print('War Room v'+version+' 3D stage routed through local Classic model proxy')
