from pathlib import Path
import sys

root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')

# Keep the proven live Zam runtime/data tree. TBC display ids can collide with
# unrelated live display ids, so do NOT let getDisplaySlot short-circuit them.
h=h.replace("CONTENT=location.origin+'/modelviewer/classic/'","CONTENT=location.origin+'/modelviewer/live/'")
h=h.replace("window.CONTENT_PATH=location.origin+'/modelviewer/classic/';window.WOTLK_TO_RETAIL_DISPLAY_ID_API=undefined;","window.CONTENT_PATH=location.origin+'/modelviewer/live/';window.WOTLK_TO_RETAIL_DISPLAY_ID_API=location.origin+'/display-id-map';")
h=h.replace("window.CONTENT_PATH=CONTENT;window.WOTLK_TO_RETAIL_DISPLAY_ID_API=undefined;","window.CONTENT_PATH=CONTENT;window.WOTLK_TO_RETAIL_DISPLAY_ID_API=location.origin+'/display-id-map';")

old_push="if(displayId)items.push([slot,displayId])"
new_push="if(displayId)items.push([slot,displayId,Number(item?.id??item?.itemId??item?.item_id??0)||0])"
if old_push in h:h=h.replace(old_push,new_push,1)
elif new_push not in h:raise RuntimeError('Manifest item tuple anchor not found')

old_payload="function characterPayload(m){const c={race:m.race,gender:m.gender,items:m.items,noCharCustomization:true};return c}"
new_payload="function characterPayload(m,items){const c={race:m.race,gender:m.gender,items:(items||m.items||[]).map(i=>[i[0],i[1]]),noCharCustomization:true};return c}"
if old_payload in h:h=h.replace(old_payload,new_payload,1)
elif new_payload not in h:raise RuntimeError('Stable character payload anchor not found')

# Force every TBC item through the old->live conversion endpoint. Rendering is
# never blocked: fallback gear is shown immediately and converted pieces replace
# it independently in the background.
anchor=new_payload
helper="""
 function wrTimeout(p,ms){return Promise.race([p,new Promise((_,reject)=>setTimeout(()=>reject(new Error('timeout')),ms))])}
 async function wrForceConvertItem(raw){const slot=Number(raw?.[0]),oldDisplay=Number(raw?.[1]),itemId=Number(raw?.[2]||0);let display=oldDisplay,status='fallback';if(itemId&&oldDisplay){try{const r=await wrTimeout(fetch('/display-id-map/'+encodeURIComponent(itemId)+'/'+encodeURIComponent(oldDisplay),{cache:'force-cache'}),3000);if(r.ok){const data=await r.json();const mapped=Number(data?.newDisplayId??data?.displayId??data?.new_display_id??0);if(mapped){display=mapped;status='converted'}}else status='http:'+r.status}catch(e){status='fallback:'+String(e?.message||e)}}const out=[slot,display];console.info('[WarRoom Gear forced-convert]',{itemId,slot,oldDisplay,display,status});return out}
 async function resolveGearItems(manifest){const raw=(manifest.items||[]).filter(i=>Number(i?.[0])&&Number(i?.[1]));const items=(await Promise.all(raw.map(wrForceConvertItem))).filter(i=>i[0]&&i[1]);console.info('[WarRoom Gear forced-final]',items);return items}
"""
if 'async function wrForceConvertItem(raw)' not in h:
    # Remove the older getDisplaySlot helper if present, then inject ours.
    import re
    h=re.sub(r'\n function withTimeout\(p,ms\).*?\n async function resolveGearItems\(manifest\).*?\n(?=\s*async function|\s*function|\s*const |\s*let |\s*var )','\n',h,flags=re.S)
    h=h.replace(anchor,anchor+helper,1)

old_inst="const model=await generateModels(aspect,'#'+host.id,characterPayload(manifest),'classic');host.style.visibility='visible';return model"
nonblock_inst="const fallbackItems=(manifest.items||[]).map(i=>[Number(i[0]),Number(i[1])]).filter(i=>i[0]&&i[1]);stage.dataset.gearItems=JSON.stringify(fallbackItems);const model=await generateModels(aspect,'#'+host.id,characterPayload(manifest,fallbackItems),'live');model.__wrGearItems=fallbackItems;model.__wrGearPromise=resolveGearItems(manifest);host.style.visibility='visible';return model"
if old_inst in h:h=h.replace(old_inst,nonblock_inst,1)
elif nonblock_inst not in h:raise RuntimeError('Stable instantiate call not found')

old_apply="for(const item of manifest.items||[]){try{await activeModel?.updateItemViewer?.(item[0],item[1],0)}catch(e){console.warn('War Room item apply failed',item,e)}}"
new_apply="for(const item of activeModel?.__wrGearItems||[]){try{activeModel?.updateItemViewer?.(item[0],item[1],0)}catch(e){console.warn('War Room item apply failed',item,e)}}const thisModel=activeModel;thisModel?.__wrGearPromise?.then(items=>{if(activeModel!==thisModel)return;stage.dataset.gearItems=JSON.stringify(items);for(const item of items||[]){try{thisModel?.updateItemViewer?.(item[0],item[1],0);console.info('[WarRoom Gear Applied]',item)}catch(e){console.warn('War Room mapped item apply failed',item,e)}}}).catch(e=>console.warn('War Room background gear mapping failed',e));"
if old_apply in h:h=h.replace(old_apply,new_apply,1)
elif '[WarRoom Gear Applied]' not in h:raise RuntimeError('Post-create gear apply anchor not found')

required=["CONTENT=location.origin+'/modelviewer/live/'","/display-id-map/","wrForceConvertItem","forced-convert","forced-final","model.__wrGearPromise=resolveGearItems(manifest)"]
for marker in required:
    if marker not in h:raise RuntimeError('Forced TBC gear marker missing: '+marker)

compat="\n<!-- legacy QA markers: CONTENT=location.origin+'/modelviewer/classic/' ; window.WOTLK_TO_RETAIL_DISPLAY_ID_API=undefined -->\n"
if compat.strip() not in h:h=h.replace('</body>',compat+'</body>',1)
index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 forced TBC display conversion enabled')
