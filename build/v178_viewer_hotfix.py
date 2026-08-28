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

# Mirror the passing Windows/Edge QA bootstrap order exactly.  The Wowhead
# viewer runtime expects jQuery to exist when its parser-loaded script runs, so
# load jQuery first, then configure Classic CONTENT_PATH, then load the same-
# origin viewer runtime.  The wrapper import can then consume the lexical
# ZamModelViewer binding without relying on window.ZamModelViewer.
STATIC_MARKER='War Room v1.7.28 - Static viewer runtime bootstrap'
static_boot="""<script src=\"https://code.jquery.com/jquery-3.7.1.min.js\"></script><script>/* War Room v1.7.28 - Static viewer runtime bootstrap */window.CONTENT_PATH=location.origin+'/modelviewer/classic/';window.WOTLK_TO_RETAIL_DISPLAY_ID_API=undefined;</script><script src=\"/modelviewer/live/viewer/viewer.min.js\"></script>"""
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

# War Room itself uses `$` as a document.querySelector shorthand.  The Wowhead
# runtime also expects `$` to be jQuery while it creates DOM nodes such as
# $('<canvas/>').  Temporarily restore jQuery only around generateModels so the
# viewer can construct its canvas without breaking War Room's own `$` helper.
old_generate="return await generateModels(aspect,'#'+host.id,characterPayload(manifest),'classic')"
new_generate="const wrDollar=window.$;if(window.jQuery)window.$=window.jQuery;try{return await generateModels(aspect,'#'+host.id,characterPayload(manifest),'classic')}finally{window.$=wrDollar}"
if old_generate in h:
    h=h.replace(old_generate,new_generate,1)
elif new_generate not in h:
    raise RuntimeError('3D generateModels call not found for jQuery collision fix')

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
if '<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>' not in h:
    raise RuntimeError('Static jQuery bootstrap missing before viewer runtime')
if new_generate not in h:
    raise RuntimeError('jQuery collision guard missing around generateModels')
for required in [marker,'#drawer .dossier-runes{display:none!important}','#drawer .ds:has(#dsGS){display:none!important}','#drawer .detail-box:has(#dGs){display:none!important}']:
    if required not in h: raise RuntimeError('Inspect cleanup marker missing: '+required)

index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 hotfix: static jQuery + viewer runtime + scoped $ collision guard + GearScore UI removed')
