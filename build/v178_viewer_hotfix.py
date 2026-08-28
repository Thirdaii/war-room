from pathlib import Path
import sys

root=Path(sys.argv[1])
index=root/'index.html'
h=index.read_text(encoding='utf-8')

old="VIEWER_SRC='/modelviewer/classic/viewer/viewer.min.js',CONTENT=location.origin+'/modelviewer/classic/'"
new="VIEWER_SRC='/modelviewer/live/viewer/viewer.min.js',CONTENT=location.origin+'/modelviewer/classic/'"
if old in h:
    h=h.replace(old,new,1)
elif new not in h:
    raise RuntimeError('Local viewer constants not found for live-runtime hotfix')

marker='/* War Room v1.7.28 - Remove dossier rune row */'
css='''\n/* War Room v1.7.28 - Remove dossier rune row */\n#drawer .dossier-runes{display:none!important}\n'''
if marker not in h:
    if '</style>' not in h: raise RuntimeError('No style block found for dossier rune removal')
    h=h.replace('</style>',css+'</style>',1)

if h.count("VIEWER_SRC='/modelviewer/live/viewer/viewer.min.js'")!=1:
    raise RuntimeError('Local live viewer runtime route not unique')
if "CONTENT=location.origin+'/modelviewer/classic/'" not in h:
    raise RuntimeError('Classic content path missing')
if marker not in h:
    raise RuntimeError('Dossier rune removal marker missing')

index.write_text(h,encoding='utf-8')
print('War Room v1.7.28 viewer hotfix: live Zam runtime + Classic content + dossier rune row removed')
