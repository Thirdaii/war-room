from pathlib import Path
import re
h=Path('work/app/index.html').read_text(encoding='utf-8')
patterns=[
 r'(?:const|let|var)\s+\w+\s*=\s*\[',
 r'function\s+renderRaid\s*\([^)]*\)\s*\{',
 r'function\s+assign\w*\s*\([^)]*\)\s*\{',
 r'function\s+move\w*\s*\([^)]*\)\s*\{'
]
seen=0
for pat in patterns:
    for m in re.finditer(pat,h):
        seen+=1
        print('\n---MATCH---')
        print(h[max(0,m.start()-500):min(len(h),m.start()+3500)])
print(f'\nDIAGNOSTIC_MATCHES={seen}')
