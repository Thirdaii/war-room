from pathlib import Path

here=Path(__file__).resolve().parent
core=here/'v178_launcher_patch_core.py'
extra=here/'v178_display_map_patch.py'
for script in (core,extra):
    ns={'__name__':'__main__','__file__':str(script)}
    exec(compile(script.read_text(encoding='utf-8'),str(script),'exec'),ns,ns)
