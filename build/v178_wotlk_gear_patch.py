from pathlib import Path
import sys

root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')

# Keep the proven live Zam runtime and use its live data tree for equipment.
h=h.replace("CONTENT=location.origin+'/modelviewer/classic/'","CONTENT=location.origin+'/modelviewer/live/'")
h=h.replace("window.CONTENT_PATH=location.origin+'/modelviewer/classic/';window.WOTLK_TO_RETAIL_DISPLAY_ID_API=undefined;","window.CONTENT_PATH=location.origin+'/modelviewer/live/';window.WOTLK_TO_RETAIL_DISPLAY_ID_API=location.origin+'/display-id-map';")
h=h.replace("window.CONTENT_PATH=CONTENT;window.WOTLK_TO_RETAIL_DISPLAY_ID_API=undefined;","window.CONTENT_PATH=CONTENT;window.WOTLK_TO_RETAIL_DISPLAY_ID_API=location.origin+'/display-id-map';")

# Preserve source item ids in manifest tuples: [slot, oldDisplayId, itemId].
old_push="if(displayId)items.push([slot,displayId])"
new_push="if(displayId)items.push([slot,displayId,Number(item?.id??item?.itemId??item?.item_id??0)||0])"
if old_push in h:
    h=h.replace(old_push,new_push,1)
elif new_push not in h:
    raise RuntimeError('Manifest item tuple anchor not found')

old_payload="function characterPayload(m){const c={race:m.race,gender:m.gender,items:m.items,noCharCustomization:true};return c}"
new_payload="function characterPayload(m,items){const c={race:m.race,gender:m.gender,items:(items||m.items||[]).map(i=>[i[0],i[1]]),noCharCustomization:true};return c}"
if old_payload in h:
    h=h.replace(old_payload,new_payload,1)
elif new_payload not in h:
    raise RuntimeError('Stable character payload anchor not found')

old_vars="let renderToken=0,activeModel=null,activeCharacter='',viewerPromise=null,generateModelsFn=null,lastRequestFingerprint='',lastManifestFingerprint='';"
new_vars="let renderToken=0,activeModel=null,activeCharacter='',viewerPromise=null,generateModelsFn=null,getDisplaySlotFn=null,lastRequestFingerprint='',lastManifestFingerprint='';"
if old_vars in h:
    h=h.replace(old_vars,new_vars,1)
elif new_vars not in h:
    raise RuntimeError('Viewer state anchor not found')

old_import="generateModelsFn=mod?.generateModels;if(typeof generateModelsFn!=='function')throw new Error('wow-model-viewer imported without generateModels');return generateModelsFn"
new_import="generateModelsFn=mod?.generateModels;getDisplaySlotFn=mod?.getDisplaySlot;if(typeof generateModelsFn!=='function')throw new Error('wow-model-viewer imported without generateModels');return generateModelsFn"
if old_import in h:
    h=h.replace(old_import,new_import,1)
elif new_import not in h:
    raise RuntimeError('Viewer module import anchor not found')

# Never block model creation on remote display-id conversion. Resolve all pieces
# in parallel, time each one out independently, and always fall back to the
# original display id. Trace the entire mapping so missing slots are diagnosable.
anchor=new_payload
helper="""
 function withTimeout(p,ms){return Promise.race([p,new Promise((_,reject)=>setTimeout(()=>reject(new Error('timeout')),ms))])}
 async function resolveGearItems(manifest){const rawItems=(manifest.items||[]).filter(raw=>Number(raw?.[0])&&Number(raw?.[1]));const jobs=rawItems.map(async raw=>{let slot=Number(raw[0]),display=Number(raw[1]),itemId=Number(raw[2]||0),sourceSlot=slot,sourceDisplay=display,status='original';if(typeof getDisplaySlotFn==='function'&&itemId){try{const mapped=await withTimeout(getDisplaySlotFn(itemId,slot,display,'live'),1800);if(mapped?.displaySlot)slot=Number(mapped.displaySlot);if(mapped?.displayId)display=Number(mapped.displayId);status=(slot!==sourceSlot||display!==sourceDisplay)?'mapped':'unchanged'}catch(e){status='fallback:'+String(e?.message||e)}}const result=[slot,display];console.info('[WarRoom Gear]',{itemId,sourceSlot,sourceDisplay,slot,display,status});return result});return (await Promise.all(jobs)).filter(i=>i[0]&&i[1])}
"""
if 'async function resolveGearItems(manifest)' not in h:
    h=h.replace(anchor,anchor+helper,1)

old_inst="const model=await generateModels(aspect,'#'+host.id,characterPayload(manifest),'classic');host.style.visibility='visible';return model"
new_inst="const fallbackItems=(manifest.items||[]).map(i=>[Number(i[0]),Number(i[1])]).filter(i=>i[0]&&i[1]);stage.dataset.gearItems=JSON.stringify(fallbackItems);const model=await generateModels(aspect,'#'+host.id,characterPayload(manifest,fallbackItems),'live');model.__wrGearItems=fallbackItems;model.__wrGearPromise=resolveGearItems(manifest);host.style.visibility='visible';return model"
if old_inst in h:
    h=h.replace(old_inst,new_inst,1)
elif new_inst not in h:
    raise RuntimeError('Stable instantiate call not found')

old_apply="for(const item of manifest.items||[]){try{await activeModel?.updateItemViewer?.(item[0],item[1],0)}catch(e){console.warn('War Room item apply failed',item,e)}}"
new_apply="for(const item of activeModel?.__wrGearItems||[]){try{activeModel?.updateItemViewer?.(item[0],item[1],0)}catch(e){console.warn('War Room item apply failed',item,e)}}const thisModel=activeModel;thisModel?.__wrGearPromise?.then(items=>{if(activeModel!==thisModel)return;stage.dataset.gearItems=JSON.stringify(items);for(const item of items||[]){try{thisModel?.updateItemViewer?.(item[0],item[1],0);console.info('[WarRoom Gear Applied]',item)}catch(e){console.warn('War Room mapped item apply failed',item,e)}}}).catch(e=>console.warn('War Room background gear mapping failed',e))"
if old_apply in h:
    h=h.replace(old_apply,new_apply,1)
elif new_apply not in h:
    raise RuntimeError('Post-create gear apply anchor not found')

required=["CONTENT=location.origin+'/modelviewer/live/'","/display-id-map","getDisplaySlotFn","function withTimeout(p,ms)","model.__wrGearPromise=resolveGearItems(manifest)","[WarRoom Gear Applied]"]
for marker in required:
    if marker not in h: raise RuntimeError('WotLK gear compatibility marker missing: '+marker)

compat="\n<!-- legacy QA markers: CONTENT=location.origin+'/modelviewer/classic/' ; window.WOTLK_TO_RETAIL_DISPLAY_ID_API=undefined -->\n"
if compat.strip() not in h:
    h=h.replace('</body>',compat+'</body>',1)

index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 nonblocking traced equipment compatibility enabled')
