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

if CSS_MARK not in h:
    h=h.replace('</style>', '\n'+css+'\n</style>', 1)

# Inject engine + renderer before the existing application script closes so all state is shared.
if JS_MARK not in h or UI_MARK not in h:
    scripts=list(re.finditer(r'<script>(.*?)</script>',h,re.S))
    if not scripts:
        raise RuntimeError('No inline application script found')
    m=scripts[-1]
    body=m.group(1)
    addon='\n'+engine+'\n'+ui+'\n'
    new_script='<script>'+body+addon+'</script>'
    h=h[:m.start()]+new_script+h[m.end():]

# Upgrade visible version language without altering functional controls.
h=re.sub(r'WAR ROOM APP • COMMAND CENTER 1\.6','WAR ROOM APP • RAID INTELLIGENCE 1.7',h,count=1)
h=re.sub(r'WAR ROOM v1\.6 • NATIVE LAUNCHER','WAR ROOM v1.7 • TBC RAID INTELLIGENCE',h,count=1)

v=json.loads(version_file.read_text(encoding='utf-8'))
v['version']='1.7.0'
v['notes']=[
    'TBC Phase 3 Raid Intelligence dashboard',
    'Live 25-player readiness score',
    'Five-party synergy and Shaman placement analysis',
    'Tank/Healer/Melee/Ranged role-balance checks',
    'Critical TBC raid coverage warnings',
    'Actionable raid-leader recommendations',
    'Black Temple and Mount Hyjal rules foundation',
    'Native War Room.exe launcher and automatic updater retained'
]
version_file.write_text(json.dumps(v,indent=2),encoding='utf-8')
index.write_text(h,encoding='utf-8')

# Hard integration gates.
final=index.read_text(encoding='utf-8')
for marker in (CSS_MARK,JS_MARK,UI_MARK,'wrRaidIntelLive','WarRoomRaidIntelligence'):
    if marker not in final:
        raise RuntimeError(f'Missing v1.7 integration marker: {marker}')
print('War Room v1.7 Raid Intelligence integration complete')
