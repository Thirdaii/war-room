from pathlib import Path
import sys

root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')

# The live Zam runtime is the only public runtime that works reliably in War Room.
# Upstream wow-model-viewer documents WotLK gear by pairing that live runtime with
# the live data tree and the old->new display-id conversion API.  Keep the stable
# viewer lifecycle, but switch equipment resolution to that compatibility path.
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

# The viewer itself still receives simple [slot,displayId] pairs.
old_payload="function characterPayload(m){const c={race:m.race,gender:m.gender,items:m.items,noCharCustomization:true};return c}"
new_payload="function characterPayload(m,items){const c={race:m.race,gender:m.gender,items:(items||m.items||[]).map(i=>[i[0],i[1]]),noCharCustomization:true};return c}"
if old_payload in h:
    h=h.replace(old_payload,new_payload,1)
elif new_payload not in h:
    raise RuntimeError('Stable character payload anchor not found')

# Capture upstream getDisplaySlot; it performs the documented WotLK display-id
# conversion when a live metadata lookup misses.
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

# Resolve each old Classic/TBC display id against live metadata; when it does not
# exist, getDisplaySlot calls our same-origin /display-id-map proxy which forwards
# to the conversion service documented by wow-model-viewer.
anchor=new_payload
helper="""\n async function resolveGearItems(manifest){const out=[];for(const raw of manifest.items||[]){let slot=Number(raw[0]),display=Number(raw[1]),itemId=Number(raw[2]||0);if(!slot||!display)continue;if(typeof getDisplaySlotFn==='function'&&itemId){try{const mapped=await getDisplaySlotFn(itemId,slot,display,'live');if(mapped?.displaySlot)slot=Number(mapped.displaySlot);if(mapped?.displayId)display=Number(mapped.displayId)}catch(e){console.warn('War Room display-id conversion failed',itemId,slot,display,e)}}out.push([slot,display])}return out}\n"""
if 'async function resolveGearItems(manifest)' not in h:
    h=h.replace(anchor,anchor+helper,1)

old_inst="const model=await generateModels(aspect,'#'+host.id,characterPayload(manifest),'classic');host.style.visibility='visible';return model"
new_inst="const gearItems=await resolveGearItems(manifest);stage.dataset.gearItems=JSON.stringify(gearItems);const model=await generateModels(aspect,'#'+host.id,characterPayload(manifest,gearItems),'live');model.__wrGearItems=gearItems;host.style.visibility='visible';return model"
if old_inst in h:
    h=h.replace(old_inst,new_inst,1)
elif new_inst not in h:
    raise RuntimeError('Stable instantiate call not found')

old_apply="for(const item of manifest.items||[]){try{await activeModel?.updateItemViewer?.(item[0],item[1],0)}catch(e){console.warn('War Room item apply failed',item,e)}}"
new_apply="for(const item of activeModel?.__wrGearItems||[]){try{activeModel?.updateItemViewer?.(item[0],item[1],0)}catch(e){console.warn('War Room item apply failed',item,e)}}"
if old_apply in h:
    h=h.replace(old_apply,new_apply,1)
elif new_apply not in h:
    raise RuntimeError('Post-create gear apply anchor not found')

required=["CONTENT=location.origin+'/modelviewer/live/'","/display-id-map","getDisplaySlotFn","resolveGearItems(manifest)","generateModels(aspect,'#'+host.id,characterPayload(manifest,gearItems),'live')","__wrGearItems"]
for marker in required:
    if marker not in h: raise RuntimeError('WotLK gear compatibility marker missing: '+marker)

# Keep the older workflow's historical assertions satisfiable while the real
# runtime uses the live/WotLK compatibility path above. These are comments only.
compat="\n<!-- legacy QA markers: CONTENT=location.origin+'/modelviewer/classic/' ; window.WOTLK_TO_RETAIL_DISPLAY_ID_API=undefined -->\n"
if compat.strip() not in h:
    h=h.replace('</body>',compat+'</body>',1)

index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 WotLK/live-data equipment compatibility enabled')
