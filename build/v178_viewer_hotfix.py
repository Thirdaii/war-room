from pathlib import Path
import re
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

# The production War Room page declares a top-level lexical `$` helper:
#     const $=s=>document.querySelector(s);
# External scripts execute in the same global lexical environment, so the Wowhead
# viewer resolves `$` to that helper instead of window.jQuery.  That is why its
# $('<canvas/>') call reaches document.querySelector and throws the exact error
# seen in the real app.  Rename War Room's helper and every War Room `$(` call so
# the viewer is free to resolve global `$` to jQuery for its entire lifetime.
old_helper='const $=s=>document.querySelector(s);'
new_helper='const wrQuery=s=>document.querySelector(s);'
if old_helper in h:
    h=h.replace(old_helper,new_helper,1)
    h=re.sub(r'(?<![A-Za-z0-9_$])\$\(', 'wrQuery(', h)
elif new_helper not in h:
    raise RuntimeError('War Room querySelector helper not found for lexical $ isolation')

# Mirror the passing Windows/Edge QA bootstrap order exactly.  jQuery must exist
# before the parser-loaded viewer runtime.  Classic assets remain same-origin.
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

# Remove the obsolete scoped window.$ swap from the previous test build.  It
# could never shadow a top-level lexical `$`; the helper rename above fixes the
# collision at the correct JavaScript binding boundary.
old_generate="return await generateModels(aspect,'#'+host.id,characterPayload(manifest),'classic')"
scoped_generate="const wrDollar=window.$;if(window.jQuery)window.$=window.jQuery;try{return await generateModels(aspect,'#'+host.id,characterPayload(manifest),'classic')}finally{window.$=wrDollar}"
if scoped_generate in h:
    h=h.replace(scoped_generate,old_generate,1)
elif old_generate not in h:
    raise RuntimeError('3D generateModels call not found after lexical $ isolation')

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
if old_helper in h or re.search(r'(?<![A-Za-z0-9_$])\$\(', h):
    raise RuntimeError('Lexical War Room $ collision or unrenamed War Room $ call remains')
if new_helper not in h or 'wrQuery("#toast")' not in h:
    raise RuntimeError('War Room query helper rename did not propagate to app calls')
for required in [marker,'#drawer .dossier-runes{display:none!important}','#drawer .ds:has(#dsGS){display:none!important}','#drawer .detail-box:has(#dGs){display:none!important}']:
    if required not in h: raise RuntimeError('Inspect cleanup marker missing: '+required)

index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 hotfix: lexical $ isolated + static jQuery/viewer runtime + GearScore UI removed')
