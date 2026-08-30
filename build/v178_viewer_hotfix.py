from pathlib import Path

here=Path(__file__).resolve().parent
core=here/'v178_viewer_hotfix_core.py'
gear=here/'v178_wotlk_gear_patch.py'
for script in (core,gear):
    ns={'__name__':'__main__','__file__':str(script)}
    exec(compile(script.read_text(encoding='utf-8'),str(script),'exec'),ns,ns)
