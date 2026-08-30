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

# Classic viewer stability + gear hotfix.
# 1) Classic docs explicitly call out noCharCustomization for item rendering;
#    force it so a valid race/gender model does not silently render naked.
old_payload="function characterPayload(m){const c={race:m.race,gender:m.gender,items:m.items};for(const k of ['skin','face','hairStyle','hairColor','facialStyle'])if(Number.isInteger(m[k]))c[k]=m[k];if(!['skin','face','hairStyle','hairColor','facialStyle'].some(k=>Number.isInteger(m[k])))c.noCharCustomization=true;return c}"
new_payload="function characterPayload(m){const c={race:m.race,gender:m.gender,items:m.items,noCharCustomization:true};return c}"
if old_payload in h:
    h=h.replace(old_payload,new_payload,1)
elif new_payload not in h:
    raise RuntimeError('Character payload function not found for Classic gear mode')

# 2) The Inspect-ready event can fire repeatedly for the same character snapshot.
#    Previously every event destroyed/recreated the viewer, causing the exact
#    naked-model <-> loading-text flash seen in the app. Deduplicate identical
#    raw snapshots before manifest work and identical manifests after resolution.
old_vars="let renderToken=0,activeModel=null,activeCharacter='',viewerPromise=null,generateModelsFn=null;"
new_vars="let renderToken=0,activeModel=null,activeCharacter='',viewerPromise=null,generateModelsFn=null,lastRequestFingerprint='',lastManifestFingerprint='';"
if old_vars in h:
    h=h.replace(old_vars,new_vars,1)
elif new_vars not in h:
    raise RuntimeError('3D viewer state variables not found for render dedupe')

fingerprint_anchor="function characterPayload(m){const c={race:m.race,gender:m.gender,items:m.items,noCharCustomization:true};return c}"
fingerprint_code="""function rawFingerprint(c){const gear=Array.isArray(c?.items)?c.items:Array.isArray(c?.gear)?c.gear:Array.isArray(c?.equipment)?c.equipment:[];return JSON.stringify([c?.name||'',c?.race??'',c?.gender??'',gear.map(i=>[i?.slot??i?.slotId??i?.slot_id??'',i?.id??i?.itemId??i?.item_id??'',i?.displayId??i?.displayID??i?.display_id??''])])}\n function manifestFingerprint(m){return JSON.stringify([m?.race,m?.gender,m?.skin,m?.face,m?.hairStyle,m?.hairColor,m?.facialStyle,m?.items||[]])}"""
if fingerprint_code not in h:
    if fingerprint_anchor not in h: raise RuntimeError('Unable to anchor viewer fingerprint helpers')
    h=h.replace(fingerprint_anchor,fingerprint_anchor+fingerprint_code,1)

old_render="async function render(character){const token=++renderToken,stage=ensureStage();if(!stage||!character)return;activeCharacter=character.name||'';state(stage,'3D Character Model','Resolving character appearance…',activeCharacter||'unnamed character');if(!window.WarRoomCharacterModelManifest){state(stage,'3D Viewer Error','Manifest module unavailable.','stage mounted successfully');return}let manifest;try{manifest=await window.WarRoomCharacterModelManifest.build(character)}catch(e){state(stage,'3D Manifest Error',e?.message||String(e));return}if(token!==renderToken)return;if(!manifest?.ready){state(stage,'3D Data Waiting','Race/gender metadata missing.','race='+String(manifest?.race)+' gender='+String(manifest?.gender));return}stage.dataset.manifest=JSON.stringify(manifest);try{try{activeModel?.destroy?.()}catch(e){}for(const n of [...stage.querySelectorAll('[id^=\"wr-model-canvas-\"]')])n.remove();activeModel=await instantiate(stage,manifest);if(token!==renderToken){try{activeModel?.destroy?.()}catch(e){}return}const status=stage.querySelector('.wr-model-state');if(status)status.style.display='none';try{activeModel?.setDistance?.(4.2)}catch(e){}}catch(e){state(stage,'3D Viewer Error',e?.message||String(e),'race '+manifest.race+' • '+manifest.resolvedItems+' appearances');console.warn('War Room model viewer:',e)}}"
new_render="async function render(character){const stage=ensureStage();if(!stage||!character)return;const requestFp=rawFingerprint(character);if(requestFp===lastRequestFingerprint&&activeModel)return;lastRequestFingerprint=requestFp;const token=++renderToken;activeCharacter=character.name||'';if(!activeModel)state(stage,'3D Character Model','Resolving character appearance…',activeCharacter||'unnamed character');if(!window.WarRoomCharacterModelManifest){state(stage,'3D Viewer Error','Manifest module unavailable.','stage mounted successfully');return}let manifest;try{manifest=await window.WarRoomCharacterModelManifest.build(character)}catch(e){state(stage,'3D Manifest Error',e?.message||String(e));return}if(token!==renderToken)return;if(!manifest?.ready){state(stage,'3D Data Waiting','Race/gender metadata missing.','race='+String(manifest?.race)+' gender='+String(manifest?.gender));return}const manifestFp=manifestFingerprint(manifest);if(manifestFp===lastManifestFingerprint&&activeModel)return;stage.dataset.manifest=JSON.stringify(manifest);try{const oldModel=activeModel;const oldCanvases=[...stage.querySelectorAll('[id^=\"wr-model-canvas-\"]')];const newModel=await instantiate(stage,manifest);if(token!==renderToken){try{newModel?.destroy?.()}catch(e){}return}activeModel=newModel;lastManifestFingerprint=manifestFp;for(const item of manifest.items||[]){try{await activeModel?.updateItemViewer?.(item[0],item[1],0)}catch(e){console.warn('War Room item apply failed',item,e)}}try{oldModel?.destroy?.()}catch(e){}for(const n of oldCanvases)n.remove();const status=stage.querySelector('.wr-model-state');if(status)status.style.display='none';try{activeModel?.setDistance?.(4.2)}catch(e){}}catch(e){lastRequestFingerprint='';state(stage,'3D Viewer Error',e?.message||String(e),'race '+manifest.race+' • '+manifest.resolvedItems+' appearances');console.warn('War Room model viewer:',e)}}"
if old_render in h:
    h=h.replace(old_render,new_render,1)
elif new_render not in h:
    raise RuntimeError('3D render function not found for stable lifecycle patch')

# 3) Do not re-display the loading overlay while a model is already visible.
old_instantiate="async function instantiate(stage,manifest){state(stage,'3D Character Model','Loading live renderer + Classic data…','race '+manifest.race+' • gender '+manifest.gender+' • '+manifest.resolvedItems+' appearances');const generateModels=await loadViewer();state(stage,'3D Character Model','Creating Classic model canvas…','ZamModelViewer + generateModels ready');const host=document.createElement('div');host.id='wr-model-canvas-'+renderToken;stage.insertBefore(host,stage.firstChild);const aspect=Math.max(.85,Math.min(1.8,(stage.clientWidth||480)/(stage.clientHeight||320)));return await generateModels(aspect,'#'+host.id,characterPayload(manifest),'classic')}"
new_instantiate="async function instantiate(stage,manifest){const hasModel=!!stage.querySelector('canvas');if(!hasModel)state(stage,'3D Character Model','Loading live renderer + Classic data…','race '+manifest.race+' • gender '+manifest.gender+' • '+manifest.resolvedItems+' appearances');const generateModels=await loadViewer();if(!hasModel)state(stage,'3D Character Model','Creating Classic model canvas…','ZamModelViewer + generateModels ready');const host=document.createElement('div');host.id='wr-model-canvas-'+renderToken;host.style.visibility=hasModel?'hidden':'visible';stage.insertBefore(host,stage.firstChild);const aspect=Math.max(.85,Math.min(1.8,(stage.clientWidth||480)/(stage.clientHeight||320)));const model=await generateModels(aspect,'#'+host.id,characterPayload(manifest),'classic');host.style.visibility='visible';return model}"
if old_instantiate in h:
    h=h.replace(old_instantiate,new_instantiate,1)
elif new_instantiate not in h:
    raise RuntimeError('3D instantiate function not found for no-flash patch')

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
for required in [marker,'#drawer .dossier-runes{display:none!important}','#drawer .ds:has(#dsGS){display:none!important}','#drawer .detail-box:has(#dGs){display:none!important}',new_payload,'rawFingerprint(c)','manifestFingerprint(m)','updateItemViewer?.(item[0],item[1],0)','lastManifestFingerprint']:
    if required not in h: raise RuntimeError('v1.7.28 stable 3D marker missing: '+required)

index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 hotfix: stable 3D lifecycle + forced Classic gear + lexical $ isolation')
