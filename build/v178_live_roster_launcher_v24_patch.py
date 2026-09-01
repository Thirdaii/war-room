from pathlib import Path

p=Path('build/WarRoomLauncher.cs')
s=p.read_text(encoding='utf-8')
MARK='WarRoomRosterV24'
if MARK in s:
    print('V24 live roster JSON fix already installed')
    raise SystemExit(0)
if 'private static string GuildRosterJson' not in s or 'private static void HandleGuildRoster' not in s:
    raise RuntimeError('V21/V22 live roster launcher patches must run before V24')

# The V21 generator accidentally emitted C# string literals containing \\".
# At runtime that produces bodies like {\"source\":... which are NOT valid JSON.
# Restrict the repair to the guild-roster JSON/output block only.
start=s.index('    private static string GuildRosterJson')
end=s.index('    private static void ServeStatic',start)
block=s[start:end]
bad=r'\\\"'
if bad not in block:
    raise RuntimeError('V24 expected malformed guild-roster JSON escape pattern was not found')
block=block.replace(bad,r'\"')
if bad in block:
    raise RuntimeError('V24 malformed JSON escapes remain after repair')
# Marker lives in the repaired block so compiled EXE provenance is obvious.
anchor='    private static string GuildRosterJson(List<GuildMemberRow> rows,string source,string upstream)\n    {'
replacement=anchor+'\n        const string WarRoomRosterV24 = "valid-json-wire-format";'
if anchor not in block:
    raise RuntimeError('V24 GuildRosterJson anchor missing')
block=block.replace(anchor,replacement,1)
s=s[:start]+block+s[end:]

for marker in [MARK,'valid-json-wire-format','sb.Append("{\\\"source\\\":\\\"")','Write(ctx,502,"application/json","{\\\"error\\\":']:
    if marker not in s:
        raise RuntimeError('V24 live roster JSON marker missing: '+marker)
p.write_text(s,encoding='utf-8')
print('War Room v1.7.28 live guild roster v24 valid JSON wire-format fix installed')
