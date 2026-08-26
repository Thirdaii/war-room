from pathlib import Path
import json,re,sys
root=Path(sys.argv[1])
index=root/'index.html'
version_file=root/'version.json'
repo=Path(__file__).parent
h=index.read_text(encoding='utf-8')
css=(repo/'raid_intelligence.css').read_text(encoding='utf-8')
engine=(repo/'raid_intelligence.js').read_text(encoding='utf-8')
ui=(repo/'raid_intelligence_ui.js').read_text(encoding='utf-8')
CSS_MARK='/* War Room v1.7 Raid Intelligence */'
JS_MARK='/* War Room v1.7 - TBC Phase 3 Raid Intelligence */'
UI_MARK='/* War Room v1.7 - live Raid Intelligence dashboard */'

if CSS_MARK in h:
    start=h.index(CSS_MARK)
    end=h.find('</style>',start)
    if end<0: raise RuntimeError('Could not find end of v1.7 style block')
    h=h[:start]+css+'\n'+h[end:]
else:
    h=h.replace('</style>','\n'+css+'\n</style>',1)

scripts=list(re.finditer(r'<script>(.*?)</script>',h,re.S))
if not scripts: raise RuntimeError('No inline application script found')
m=scripts[-1]
body=m.group(1)
if JS_MARK in body:
    body=body[:body.index(JS_MARK)].rstrip()
addon='\n'+engine+'\n'+ui+'\n'
h=h[:m.start()]+'<script>'+body+addon+'</script>'+h[m.end():]

h=re.sub(r'WAR ROOM APP • (?:COMMAND CENTER 1\.6|RAID INTELLIGENCE 1\.7(?:\.[0-9]+)?)','WAR ROOM APP • RAID INTELLIGENCE 1.7.2',h,count=1)
h=re.sub(r'WAR ROOM v1\.(?:6|7(?:\.[0-9]+)?) • (?:NATIVE LAUNCHER|TBC RAID INTELLIGENCE)','WAR ROOM v1.7.2 • TBC RAID INTELLIGENCE',h,count=1)

v=json.loads(version_file.read_text(encoding='utf-8'))
v['version']='1.7.2'
v['notes']=[
    'Raid Intelligence docked beside the five-group raid composition',
    'Sticky desktop sidecar keeps readiness visible while building the raid',
    'Compact live party-synergy, coverage, warnings and recommendations',
    'Responsive fallback stacks the intelligence panel on narrower windows',
    'Production flat raid/roster live-state binding retained',
    'TBC Phase 3 encounter-aware analysis retained'
]
version_file.write_text(json.dumps(v,indent=2),encoding='utf-8')
index.write_text(h,encoding='utf-8')
final=index.read_text(encoding='utf-8')
for marker in (CSS_MARK,JS_MARK,UI_MARK,'wrRaidIntelLive','WarRoomRaidIntelligence','extractFromDOM','wrRaidCommandDock'):
    if marker not in final: raise RuntimeError(f'Missing v1.7.2 integration marker: {marker}')
if final.count(JS_MARK)!=1 or final.count(UI_MARK)!=1:
    raise RuntimeError('Duplicate Raid Intelligence modules detected after upgrade')
print('War Room v1.7.2 side-by-side Raid Intelligence integration complete')
