from pathlib import Path
import sys

root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')

old="VIEWER_SRC='/modelviewer/classic/viewer/viewer.min.js',CONTENT=location.origin+'/modelviewer/classic/'"
new="VIEWER_SRC='/modelviewer/live/viewer/viewer.min.js',CONTENT=location.origin+'/modelviewer/classic/'"
if old in h:
    h=h.replace(old,new,1)
elif new not in h:
    raise RuntimeError('Local viewer constants not found for live-runtime hotfix')

# The protected v1.7.26 block validates a window property immediately after
# dynamically loading the viewer. On current Edge/Wowhead this can miss the
# global lexical constructor. Bridge it with an indirect global eval compiled
# after the dependency has loaded, then expose a stable window property.
protected_loader="await script(VIEWER_SRC,'ZamModelViewer');if(typeof window.ZamModelViewer!=='function')throw new Error('live viewer loaded without ZamModelViewer');"
lexical_loader="await script(VIEWER_SRC);if(typeof ZamModelViewer!=='function'){const keys=Object.keys(window).filter(k=>/zam|model/i.test(k)).slice(0,12).join(',');throw new Error('viewer runtime loaded but ZamModelViewer binding missing'+(keys?' globals='+keys:''));}"
bridge_loader="await script(VIEWER_SRC);let zamCtor=window.ZamModelViewer;try{if(typeof zamCtor!=='function')zamCtor=(0,eval)('typeof ZamModelViewer===\\\"function\\\"?ZamModelViewer:null')}catch(e){}if(typeof zamCtor==='function')window.ZamModelViewer=zamCtor;if(typeof window.ZamModelViewer!=='function'){const keys=Object.keys(window).filter(k=>/zam|model/i.test(k)).slice(0,12).join(',');throw new Error('viewer runtime loaded but ZamModelViewer binding missing'+(keys?' globals='+keys:''));}"
if protected_loader in h:
    h=h.replace(protected_loader,bridge_loader,1)
elif lexical_loader in h:
    h=h.replace(lexical_loader,bridge_loader,1)
elif bridge_loader not in h:
    raise RuntimeError('No supported ZamModelViewer loader guard found for bridge hotfix')

marker='/* War Room v1.7.28 - Remove dossier rune row */'
css='''\n/* War Room v1.7.28 - Remove dossier rune row */\n#drawer .dossier-runes{display:none!important}\n#drawer #dsGS{display:none!important}\n#drawer #dsGS + span{display:none!important}\n#drawer .ds:has(#dsGS){display:none!important}\n#drawer .detail-box:has(#dGs){display:none!important}\n'''
if marker not in h:
    if '</style>' not in h: raise RuntimeError('No style block found for Inspect cleanup')
    h=h.replace('</style>',css+'</style>',1)

if h.count("VIEWER_SRC='/modelviewer/live/viewer/viewer.min.js'")!=1:
    raise RuntimeError('Local live viewer runtime route not unique')
if "CONTENT=location.origin+'/modelviewer/classic/'" not in h:
    raise RuntimeError('Classic content path missing')
if bridge_loader not in h:
    raise RuntimeError('ZamModelViewer global bridge missing')
for required in [marker,'#drawer .dossier-runes{display:none!important}','#drawer .ds:has(#dsGS){display:none!important}','#drawer .detail-box:has(#dGs){display:none!important}']:
    if required not in h: raise RuntimeError('Inspect cleanup marker missing: '+required)

index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 hotfix: ZamModelViewer global bridge + Classic content + GearScore UI removed')
