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

# The Windows/Edge QA that creates a real Classic canvas loads viewer.min.js as
# a normal parser script.  War Room was still dynamically injecting it later,
# which is the material difference left between QA and the real app.  Mirror
# the passing path exactly: establish CONTENT_PATH, load the same-origin viewer
# runtime statically, then let the existing wrapper import consume its global
# lexical ZamModelViewer binding.  Do not require window.ZamModelViewer: the
# upstream runtime does not promise that property.
STATIC_MARKER='War Room v1.7.28 - Static viewer runtime bootstrap'
static_boot="""<script>/* War Room v1.7.28 - Static viewer runtime bootstrap */window.CONTENT_PATH=location.origin+'/modelviewer/classic/';window.WOTLK_TO_RETAIL_DISPLAY_ID_API=undefined;</script><script src=\"/modelviewer/live/viewer/viewer.min.js\"></script>"""
if STATIC_MARKER not in h:
    if '</head>' not in h: raise RuntimeError('No head end found for static viewer bootstrap')
    h=h.replace('</head>',static_boot+'</head>',1)

protected_loader="await script(VIEWER_SRC,'ZamModelViewer');if(typeof window.ZamModelViewer!=='function')throw new Error('live viewer loaded without ZamModelViewer');"
lexical_loader="await script(VIEWER_SRC);if(typeof ZamModelViewer!=='function'){const keys=Object.keys(window).filter(k=>/zam|model/i.test(k)).slice(0,12).join(',');throw new Error('viewer runtime loaded but ZamModelViewer binding missing'+(keys?' globals='+keys:''));}"
bridge_loader="await script(VIEWER_SRC);let zamCtor=window.ZamModelViewer;try{if(typeof zamCtor!=='function')zamCtor=(0,eval)('typeof ZamModelViewer===\\\"function\\\"?ZamModelViewer:null')}catch(e){}if(typeof zamCtor==='function')window.ZamModelViewer=zamCtor;if(typeof window.ZamModelViewer!=='function'){const keys=Object.keys(window).filter(k=>/zam|model/i.test(k)).slice(0,12).join(',');throw new Error('viewer runtime loaded but ZamModelViewer binding missing'+(keys?' globals='+keys:''));}"
static_loader="if(!document.querySelector('script[src=\"/modelviewer/live/viewer/viewer.min.js\"]'))await script(VIEWER_SRC);"
if bridge_loader in h:
    h=h.replace(bridge_loader,static_loader,1)
elif lexical_loader in h:
    h=h.replace(lexical_loader,static_loader,1)
elif protected_loader in h:
    h=h.replace(protected_loader,static_loader,1)
elif static_loader not in h:
    raise RuntimeError('No supported ZamModelViewer loader guard found for static-runtime hotfix')

marker='/* War Room v1.7.28 - Remove dossier rune row */'
css='''\n/* War Room v1.7.28 - Remove dossier rune row */\n#drawer .dossier-runes{display:none!important}\n#drawer #dsGS{display:none!important}\n#drawer #dsGS + span{display:none!important}\n#drawer .ds:has(#dsGS){display:none!important}\n#drawer .detail-box:has(#dGs){display:none!important}\n'''
if marker not in h:
    if '</style>' not in h: raise RuntimeError('No style block found for Inspect cleanup')
    h=h.replace('</style>',css+'</style>',1)

if h.count("VIEWER_SRC='/modelviewer/live/viewer/viewer.min.js'")!=1:
    raise RuntimeError('Local live viewer runtime route not unique')
if "CONTENT=location.origin+'/modelviewer/classic/'" not in h:
    raise RuntimeError('Classic content path missing')
if STATIC_MARKER not in h or static_loader not in h:
    raise RuntimeError('Static viewer runtime bootstrap missing')
for required in [marker,'#drawer .dossier-runes{display:none!important}','#drawer .ds:has(#dsGS){display:none!important}','#drawer .detail-box:has(#dGs){display:none!important}']:
    if required not in h: raise RuntimeError('Inspect cleanup marker missing: '+required)

index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 hotfix: static same-origin viewer runtime + Classic content + GearScore UI removed')
