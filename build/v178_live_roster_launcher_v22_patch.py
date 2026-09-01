from pathlib import Path

p=Path('build/WarRoomLauncher.cs')
s=p.read_text(encoding='utf-8')
MARK='WarRoomRosterV22'
if MARK in s:
    print('V22 live roster launcher hotfix already installed')
    raise SystemExit(0)
if 'HandleGuildRoster' not in s:
    raise RuntimeError('V21 live roster launcher patch must run before V22')

# V21 could wait up to 8s on each of two ClassicArmory URLs before it ever
# reached the working EpicForge fallback, while the browser aborted the whole
# request at 12s. Put the known guild source first and keep each upstream
# attempt bounded so fallbacks remain reachable.
old_timeout='req.Timeout=8000;req.ReadWriteTimeout=8000;'
new_timeout='req.Timeout=6000;req.ReadWriteTimeout=6000;'
if old_timeout in s:
    s=s.replace(old_timeout,new_timeout,1)
elif new_timeout not in s:
    raise RuntimeError('V22 upstream timeout anchor missing')

old_urls='''        string[] urls={\n            "https://classicarmory.gg/guild/us/dreamscythe/me-not-that-kind-of-orc?ns=classicann",\n            "https://classicarmory.gg/guild/us/dreamscythe/Me%20Not%20That%20Kind%20Of%20Orc?ns=classicann",\n            "https://epicforge.au/guild/dreamscythe/Me%20Not%20That%20Kind%20Of%20Orc?mode=anniversary"\n        };\n        string[] sources={"ClassicArmory.gg","ClassicArmory.gg","EpicForge.au"};string lastError="";'''
new_urls='''        string[] urls={\n            "https://epicforge.au/guild/dreamscythe/Me%20Not%20That%20Kind%20Of%20Orc?mode=anniversary",\n            "https://classicarmory.gg/guild/us/dreamscythe/me-not-that-kind-of-orc?ns=classicann",\n            "https://classicarmory.gg/guild/us/dreamscythe/Me%20Not%20That%20Kind%20Of%20Orc?ns=classicann"\n        };\n        string[] sources={"EpicForge.au","ClassicArmory.gg","ClassicArmory.gg"};string lastError="";'''
if old_urls in s:
    s=s.replace(old_urls,new_urls,1)
elif new_urls not in s:
    raise RuntimeError('V22 guild upstream ordering anchor missing')

field_anchor='    private static DateTime GuildRosterCacheAtUtc = DateTime.MinValue;'
field_new=field_anchor+'\n    private const string WarRoomRosterV22 = "epicforge-first-30s-client-deadline";'
if field_anchor in s:
    s=s.replace(field_anchor,field_new,1)
else:
    raise RuntimeError('V22 guild roster field anchor missing')

# Surface which live source won so the UI can be diagnosed without guessing.
s=s.replace('ctx.Response.Headers["X-WarRoom-Roster"]="live";Write(ctx,200,"application/json; charset=utf-8",json);return;',
            'ctx.Response.Headers["X-WarRoom-Roster"]="live";ctx.Response.Headers["X-WarRoom-Roster-Source"]=sources[i];Write(ctx,200,"application/json; charset=utf-8",json);return;',1)

for marker in [MARK,'EpicForge.au","ClassicArmory.gg','req.Timeout=6000','X-WarRoom-Roster-Source']:
    if marker not in s:
        raise RuntimeError('V22 live roster launcher marker missing: '+marker)
p.write_text(s,encoding='utf-8')
print('War Room v1.7.28 live guild roster v22 launcher hotfix installed')
