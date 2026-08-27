from pathlib import Path
import json,re,sys
root=Path(sys.argv[1]); index=root/'index.html'; version_file=root/'version.json'; updater=root/'WarRoomUpdater.ps1'; repo=Path(__file__).parent
h=index.read_text(encoding='utf-8'); css=(repo/'raid_intelligence.css').read_text(encoding='utf-8'); engine=(repo/'raid_intelligence.js').read_text(encoding='utf-8'); refresh=(repo/'spec_refresh.js').read_text(encoding='utf-8'); armory=(repo/'armory_refresh_adapter.js').read_text(encoding='utf-8'); ui=(repo/'raid_intelligence_ui.js').read_text(encoding='utf-8'); charui=(repo/'character_data_ui.js').read_text(encoding='utf-8'); inspectui=(repo/'inspect_enrichment_sync.js').read_text(encoding='utf-8'); graphics=(repo/'inspect_graphics.js').read_text(encoding='utf-8'); manifest=(repo/'character_model_manifest.js').read_text(encoding='utf-8'); stage=(repo/'character_model_stage.js').read_text(encoding='utf-8')
CSS_MARK='/* War Room v1.7 Raid Intelligence */'; JS_MARK='/* War Room v1.7 - TBC Phase 3 Raid Intelligence */'; INSPECT_MARK='/* War Room v1.7.21 - Inspect enrichment publishes live character binding */'; GRAPHICS_MARK='/* War Room v1.7.25 - Live gems and enchantments in WoW tooltips */'; ARMORY_MARK='/* War Room v1.7.26 - Character model metadata + live gem and enchant normalization */'; MODEL_MARK='/* War Room v1.7.26 - Character model manifest builder */'; STAGE_MARK='/* War Room v1.7.26 - Isolated 3D character model stage */'
if CSS_MARK in h:
 start=h.index(CSS_MARK); end=h.find('</style>',start); h=h[:start]+css+'\n'+h[end:]
else: h=h.replace('</style>','\n'+css+'\n</style>',1)
scripts=list(re.finditer(r'<script>(.*?)</script>',h,re.S)); m=scripts[-1]; body=m.group(1)
if JS_MARK in body: body=body[:body.index(JS_MARK)].rstrip()
h=h[:m.start()]+'<script>'+body+'\n'+engine+'\n'+refresh+'\n'+armory+'\n'+ui+'\n'+charui+'\n'+inspectui+'\n'+graphics+'\n'+manifest+'\n'+stage+'\n</script>'+h[m.end():]
h=re.sub(r'WAR ROOM APP • (?:COMMAND CENTER 1\.6|RAID INTELLIGENCE 1\.7(?:\.[0-9]+)?)','WAR ROOM APP • RAID INTELLIGENCE 1.7.26',h,count=1)
h=re.sub(r'WAR ROOM v1\.(?:6|7(?:\.[0-9]+)?) • (?:NATIVE LAUNCHER|TBC RAID INTELLIGENCE)','WAR ROOM v1.7.26 • TBC RAID INTELLIGENCE',h,count=1)
v=json.loads(version_file.read_text(encoding='utf-8')); v['version']='1.7.26'; v['notes']=['Adds the isolated visible 3D character stage above Inspect identity','Preserves race, gender, customization, and upstream equipment appearance IDs','Builds viewer-ready TBC character equipment manifests','Resolves missing equipment display IDs through the local item-appearance service','Preserves v1.7.25 gear artwork, tooltips, gems, enchantments, and launcher behavior']; version_file.write_text(json.dumps(v,indent=2),encoding='utf-8'); index.write_text(h,encoding='utf-8')
if updater.exists():
 ps=updater.read_text(encoding='utf-8-sig'); replacement='function Start-WarRoom { if(-not(Test-Path $IndexFile)){throw "index.html not found"}; Status "Opening the War Room..."; $exe=Join-Path $AppRoot "War Room.exe"; if(Test-Path $exe){ Start-Process -FilePath $exe -ArgumentList "--app" -WorkingDirectory $AppRoot; return }; Start-Process $IndexFile }'; ps=re.sub(r'function Start-WarRoom \{.*?\ntry \{',replacement+'\ntry {',ps,count=1,flags=re.S); updater.write_text(ps,encoding='utf-8-sig')
final=index.read_text(encoding='utf-8')
for marker in (CSS_MARK,JS_MARK,INSPECT_MARK,GRAPHICS_MARK,ARMORY_MARK,MODEL_MARK,STAGE_MARK,'WarRoomInspectLive','WarRoomCharacterModelManifest','WarRoomCharacterModelStage','wr-character-model-stage','resolveAppearance','/item-appearance?id=','directSlotLabels','found.length===1','/item-icon?id=','wr-live-item-icon','wr-wow-tooltip','bindTooltip','tooltipHtml','resolveLive','enrichLiveItem',"resolveLive('gem'", "resolveLive('enchantment'",'gemHtml','Enchant:','gemCache','enchantmentCache'):
 if marker not in final: raise RuntimeError(f'Missing v1.7.26 integration marker: {marker}')
if 'txt.includes' in graphics: raise RuntimeError('Legacy whole-matrix selector returned')
if '||document.body' in graphics or '||document.body' in inspectui: raise RuntimeError('Unsafe Inspect fallback detected')
if final.count(GRAPHICS_MARK)!=1 or final.count(ARMORY_MARK)!=1 or final.count(MODEL_MARK)!=1 or final.count(STAGE_MARK)!=1: raise RuntimeError('Duplicate/missing v1.7.26 modules')
if updater.exists() and 'ArgumentList "--app"' not in updater.read_text(encoding='utf-8-sig'): raise RuntimeError('Updater lost native app mode')
print('War Room v1.7.26 character model stage integration complete')
