from pathlib import Path

here=Path(__file__).resolve().parent
core=here/'v178_launcher_patch_core.py'
extra=here/'v178_display_map_patch.py'
live_roster=here/'v178_live_roster_launcher_patch.py'
live_roster_v22=here/'v178_live_roster_launcher_v22_patch.py'
live_roster_v24=here/'v178_live_roster_launcher_v24_patch.py'
live_roster_v25=here/'v178_live_roster_launcher_v25_patch.py'
for script in (core,extra,live_roster,live_roster_v22,live_roster_v24,live_roster_v25):
    ns={'__name__':'__main__','__file__':str(script)}
    exec(compile(script.read_text(encoding='utf-8'),str(script),'exec'),ns,ns)
