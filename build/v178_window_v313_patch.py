from pathlib import Path

p=Path('build/WarRoomLauncher.cs')
s=p.read_text(encoding='utf-8')
MARK='WarRoomWindowV313'
if MARK in s:
    print('V31.3 default window size already installed')
    raise SystemExit(0)
old='--start-maximized --no-first-run --disable-features=msEdgeFirstRunExperience'
new='--window-size=1120,760 --no-first-run --disable-features=msEdgeFirstRunExperience'
if old not in s:
    raise RuntimeError('V31.3 Edge launch-size anchor missing')
s=s.replace(old,new,1)
# Keep a compile-time marker in the source/binary so CI can prove this launcher has the new default.
anchor='private static Process LaunchEdgeApp(string url)'
if anchor not in s:
    raise RuntimeError('V31.3 launch method anchor missing')
s=s.replace(anchor,'private const string WarRoomWindowV313="1120x760-restored-default";\n    '+anchor,1)
p.write_text(s,encoding='utf-8')
print('War Room v1.7.28 V31.3 default restored window size installed')
