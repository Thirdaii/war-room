from pathlib import Path

here=Path(__file__).resolve().parent
core=here/'v178_viewer_hotfix_core.py'
gear=here/'v178_wotlk_gear_patch.py'
blend_probe=here/'v178_blend_probe_patch.py'
additive_rescue=here/'v178_additive_rescue_patch.py'
roster_drag=here/'v178_roster_drag_patch.py'
wow_portraits=here/'v178_wow_portraits_patch.py'
for script in (core,gear,blend_probe,additive_rescue,roster_drag,wow_portraits):
    ns={'__name__':'__main__','__file__':str(script)}
    exec(compile(script.read_text(encoding='utf-8'),str(script),'exec'),ns,ns)
