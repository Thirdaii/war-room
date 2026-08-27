from pathlib import Path
import json,re,sys
root=Path(sys.argv[1]); index=root/'index.html'; version_file=root/'version.json'; updater=root/'WarRoomUpdater.ps1'; repo=Path(__file__).parent
h=index.read_text(encoding='utf-8'); css=(repo/'raid_intelligence.css').read_text(encoding='utf-8'); engine=(repo/'raid_intelligence.js').read_text(encoding='utf-8'); refresh=(repo/'spec_refresh.js').read_text(encoding='utf-8'); armory=(repo/'armory_refresh_adapter.js').read_text(encoding='utf-8'); ui=(repo/'raid_intelligence_ui.js').read_text(encoding='utf-8'); charui=(repo/'character_data_ui.js').read_text(encoding='utf-8'); inspectui=(repo/'inspect_enrichment_sync.js').read_text(encoding='utf-8')
CSS_MARK='/* War Room v1.7 Raid Intelligence */'; JS_MARK='/* War Room v1.7 - TBC Phase 3 Raid Intelligence */'; REFRESH_MARK='/* War Room v1.7.8 - Spec Refresh Bridge */'; ARMORY_MARK='/* War Room v1.7.12 - ClassicArmory Proxy Diagnostics */'; UI_MARK='/* War Room v1.7 - live Raid Intelligence dashboard */'; CHAR_MARK='/* War Room v1.7.12 - Raid Character Data Diagnostics */'; INSPECT_MARK='/* War Room v1.7.15 - Inspect Armory Polish */'
if CSS_MARK in h:
    start=h.index(CSS_MARK); end=h.find('</style>',start)
    if end<0: raise RuntimeError('Could not find end of v1.7 style block')
    h=h[:start]+css+'\n'+h[end:]
else: h=h.replace('</style>','\n'+css+'\n</style>',1)
scripts=list(re.finditer(r'<script>(.*?)</script>',h,re.S))
if not scripts: raise RuntimeError('No inline application script found')
m=scripts[-1]; body=m.group(1)
if JS_MARK in body: body=body[:body.index(JS_MARK)].rstrip()
h=h[:m.start()]+'<script>'+body+'\n'+engine+'\n'+refresh+'\n'+armory+'\n'+ui+'\n'+charui+'\n'+inspectui+'\n</script>'+h[m.end():]
h=re.sub(r'WAR ROOM APP • (?:COMMAND CENTER 1\.6|RAID INTELLIGENCE 1\.7(?:\.[0-9]+)?)','WAR ROOM APP • RAID INTELLIGENCE 1.7.15',h,count=1)
h=re.sub(r'WAR ROOM v1\.(?:6|7(?:\.[0-9]+)?) • (?:NATIVE LAUNCHER|TBC RAID INTELLIGENCE)','WAR ROOM v1.7.15 • TBC RAID INTELLIGENCE',h,count=1)
v=json.loads(version_file.read_text(encoding='utf-8')); v['version']='1.7.15'; v['notes']=['Inspect keeps automatic single-character armory enrichment','Top Inspect role summary now shows the true specialization instead of fallback raid role','Equipment matrix shows live item names and item levels from armory data','Average item level remains the primary gear metric; GearScore is not required','TLS-enabled native armory proxy and raid intelligence retained']; version_file.write_text(json.dumps(v,indent=2),encoding='utf-8'); index.write_text(h,encoding='utf-8')
if updater.exists():
    ps=updater.read_text(encoding='utf-8-sig')
    replacement='function Start-WarRoom { if(-not(Test-Path $IndexFile)){throw "index.html not found"}; Status "Opening the War Room..."; $exe=Join-Path $AppRoot "War Room.exe"; if(Test-Path $exe){ Start-Process -FilePath $exe -ArgumentList "--app" -WorkingDirectory $AppRoot; return }; Start-Process $IndexFile }'
    ps=re.sub(r'function Start-WarRoom \{.*?\ntry \{',replacement+'\ntry {',ps,count=1,flags=re.S)
    updater.write_text(ps,encoding='utf-8-sig')
final=index.read_text(encoding='utf-8')
for marker in (CSS_MARK,JS_MARK,REFRESH_MARK,ARMORY_MARK,UI_MARK,CHAR_MARK,INSPECT_MARK,'WarRoomArmoryRefresh','WarRoomSpecRefresh','syncWarRoomInspectEnrichment','refreshNames([name]','EQUIPMENT MATRIX • ARMORY VERIFIED','wr-inspect-item-name','setMetric(scope,\'ROLE\',spec)','classicarmory.gg'):
    if marker not in final: raise RuntimeError(f'Missing v1.7.15 integration marker: {marker}')
if final.count(JS_MARK)!=1 or final.count(UI_MARK)!=1 or final.count(REFRESH_MARK)!=1 or final.count(ARMORY_MARK)!=1 or final.count(CHAR_MARK)!=1 or final.count(INSPECT_MARK)!=1: raise RuntimeError('Duplicate v1.7.15 modules detected after upgrade')
if updater.exists() and 'Start-Process -FilePath $exe -ArgumentList "--app"' not in updater.read_text(encoding='utf-8-sig'): raise RuntimeError('Updater did not wire native app mode')
print('War Room v1.7.15 Inspect armory polish integration complete')
