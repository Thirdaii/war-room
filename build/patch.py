from pathlib import Path
import json,re,sys
root=Path(sys.argv[1]); index=root/'index.html'; vf=root/'version.json'; updater=root/'WarRoomUpdater.ps1'
h=index.read_text(encoding='utf-8')

# Keep updater parser-safe and app-mode aware on every release.
ps=r'''param([switch]$SkipUpdate)
$ErrorActionPreference = "Stop"
$AppRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoOwner = "Thirdaii"
$RepoName = "war-room"
$AssetName = "WarRoom-App.zip"
$VersionFile = Join-Path $AppRoot "version.json"
$IndexFile = Join-Path $AppRoot "index.html"
$LogFile = Join-Path $AppRoot "WarRoomUpdater.log"
function Log([string]$m){ Add-Content -Path $LogFile -Value ("[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"),$m) }
function Status([string]$m){ Write-Host "[WAR ROOM] $m" -ForegroundColor DarkRed; Log $m }
function Get-LocalVersion { try { if(Test-Path $VersionFile){ $v=Get-Content $VersionFile -Raw|ConvertFrom-Json; if($v.version){return [version]$v.version} } } catch { Log ("Version read failed: "+$_.Exception.Message) }; return [version]"0.0.0" }
function Start-WarRoom { if(-not(Test-Path $IndexFile)){throw "index.html not found"}; Status "Opening the War Room..."; $launcher=Join-Path $AppRoot "LaunchAppWindow.ps1"; if(Test-Path $launcher){ & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $launcher -IndexFile $IndexFile; if($LASTEXITCODE -ne 0){throw "App launcher exited with code $LASTEXITCODE"} } else { Start-Process $IndexFile } }
try {
 Log "----- updater start -----"
 if($SkipUpdate){Start-WarRoom;exit 0}
 $localVersion=Get-LocalVersion; Status "Installed version: $localVersion"; Status "Checking GitHub for updates..."
 $headers=@{ "User-Agent"="Me-Not-That-Kind-Of-Orc-War-Room"; "Accept"="application/vnd.github+json"; "X-GitHub-Api-Version"="2022-11-28" }
 $release=Invoke-RestMethod -Uri "https://api.github.com/repos/$RepoOwner/$RepoName/releases/latest" -Headers $headers -Method Get -TimeoutSec 20
 $remoteVersion=[version]([string]$release.tag_name).TrimStart("v","V"); Status "Latest GitHub version: $remoteVersion"
 if($remoteVersion -le $localVersion){Status "War Room is up to date.";Start-WarRoom;exit 0}
 $asset=$release.assets|Where-Object{$_.name -eq $AssetName}|Select-Object -First 1; if(-not $asset){throw "Required release asset $AssetName not found"}
 Status "Update found: $localVersion -> $remoteVersion"
 $tempRoot=Join-Path $env:TEMP ("WarRoomUpdate_"+[guid]::NewGuid().ToString("N"));$zipPath=Join-Path $tempRoot $AssetName;$extractPath=Join-Path $tempRoot "extract";New-Item -ItemType Directory -Path $extractPath -Force|Out-Null
 Status "Downloading update...";Invoke-WebRequest -Uri $asset.browser_download_url -Headers $headers -OutFile $zipPath -UseBasicParsing -TimeoutSec 90
 Status "Extracting update...";Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
 $source=$extractPath;$children=@(Get-ChildItem $extractPath);if($children.Count -eq 1 -and $children[0].PSIsContainer){$source=$children[0].FullName};if(-not(Test-Path(Join-Path $source "index.html"))){throw "Downloaded update missing index.html"}
 Status "Installing update...";Get-ChildItem $source -Force|ForEach-Object{$dest=Join-Path $AppRoot $_.Name;if($_.PSIsContainer){if(-not(Test-Path $dest)){New-Item -ItemType Directory -Path $dest -Force|Out-Null};Copy-Item (Join-Path $_.FullName "*") $dest -Recurse -Force}else{Copy-Item $_.FullName $dest -Force}}
 Remove-Item $tempRoot -Recurse -Force -ErrorAction SilentlyContinue;Status "Update installed successfully.";Start-WarRoom;exit 0
} catch { Log ("ERROR: "+$_.Exception.Message);Write-Host ("[WAR ROOM] Updater error: "+$_.Exception.Message) -ForegroundColor Red;try{Start-WarRoom;exit 0}catch{Log ("FALLBACK LAUNCH ERROR: "+$_.Exception.Message);exit 1} }
'''
updater.write_text(ps,encoding='utf-8-sig')

css='''
/* WAR ROOM v1.6 COMMAND CENTER */
.wr-command-deck{display:grid;grid-template-columns:1.15fr repeat(3,.82fr);gap:5px;margin:5px 0}.wr-command-card{position:relative;overflow:hidden;min-height:88px;border:1px solid #4b332a;background:linear-gradient(145deg,#17100d,#090706);padding:11px;text-align:left;color:#cdb9a6;cursor:pointer}.wr-command-card:before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 100% 0,rgba(151,39,26,.18),transparent 45%);pointer-events:none}.wr-command-card:hover{border-color:#8a4c38;transform:translateY(-1px)}.wr-command-card.primary{background:linear-gradient(135deg,#43130f,#160c0a 72%);border-color:#744032}.wr-command-card .kicker{display:block;color:#8e7768;font-size:7px;font-weight:1000;letter-spacing:1.2px;text-transform:uppercase}.wr-command-card strong{display:block;margin-top:5px;color:#ead6bf;font:700 17px Georgia,serif}.wr-command-card.primary strong{font-size:22px;color:#f0c982}.wr-command-card small{display:block;margin-top:5px;color:#8d796c;font-size:8px;line-height:1.4}.wr-live-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#5bb36b;box-shadow:0 0 9px rgba(91,179,107,.55);margin-right:6px}.wr-nav-btn{cursor:pointer!important}.wr-nav-btn:not(:disabled):hover{border-color:#784235!important;color:#f0d9bd!important}.wr-nav-btn.active{box-shadow:inset 3px 0 #d1a04e,0 0 16px rgba(153,45,29,.08)!important}.wr-nav-btn small{display:block;margin-top:2px;color:#75665d;font-size:7px}.wr-section-flash{animation:wrFlash 1.1s ease}@keyframes wrFlash{0%{box-shadow:0 0 0 1px #c9633e,0 0 30px rgba(201,99,62,.28)}100%{box-shadow:inherit}}.panel,.bottom-panel,.overview-left,.overview-right{scroll-margin-top:16px}.player-card{transition:transform .12s ease,border-color .12s ease,background .12s ease}.player-card:hover{transform:translateY(-1px);background:linear-gradient(90deg,#18120f,#0b0807)!important}.group{transition:transform .12s ease,border-color .12s ease}.group:hover{transform:translateY(-1px);border-color:#684235!important}.wr-dossier-fixed{background:linear-gradient(180deg,rgba(13,9,8,.72),rgba(8,6,5,.96));border:1px solid #3e2b24;margin:5px}.wr-dossier-name{margin-top:9px}.wr-dossier-metric{position:relative}.wr-dossier-metric:after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:linear-gradient(90deg,transparent,#704634,transparent)}.native-action{transition:transform .1s ease,border-color .1s ease}.native-action:hover{transform:translateY(-1px);border-color:#8a5139}.footer:after{content:"WAR ROOM v1.6 • NATIVE LAUNCHER";margin-left:18px;color:#8d7868;font-size:8px;letter-spacing:1px}@media(max-width:1450px){.wr-command-deck{grid-template-columns:repeat(2,1fr)}}@media(max-width:900px){.wr-command-deck{grid-template-columns:1fr}}
'''
if 'WAR ROOM v1.6 COMMAND CENTER' not in h:h=h.replace('</style>',css+'</style>',1)

# Give major panels stable navigation anchors.
h=h.replace('<div class="raid-overview">','<div class="raid-overview" id="raidOverview">',1)
h=h.replace('<div class="layout">','<div class="layout" id="commandLayout">',1)
h=h.replace('<section class="bottom-panel">','<section class="bottom-panel" id="raidIntelligence">',1)
h=h.replace('<div class="wr-dossier-fixed">','<div class="wr-dossier-fixed" id="raiderDossier">',1)

# Replace decorative v1.5 nav with functional navigation.
nav='''<nav class="wr-nav" aria-label="War Room navigation"><div class="wr-nav-title"><span class="wr-live-dot"></span>Command Modules</div><div class="wr-nav-items"><button class="wr-nav-btn active" type="button" data-jump="raidOverview"><span class="wr-nav-icon">⚔</span><span>War Room<small>Command overview</small></span></button><button class="wr-nav-btn" type="button" data-jump="rosterPanel"><span class="wr-nav-icon">☷</span><span>Raid Roster<small>Characters & filters</small></span></button><button class="wr-nav-btn" type="button" data-jump="raidFrame"><span class="wr-nav-icon">♜</span><span>Assignments<small>Five raid groups</small></span></button><button class="wr-nav-btn" type="button" data-jump="raidIntelligence"><span class="wr-nav-icon">✦</span><span>Intelligence<small>Buffs & attendance</small></span></button><button class="wr-nav-btn" type="button" data-jump="raiderDossier"><span class="wr-nav-icon">◇</span><span>Raider Dossier<small>Gear & role view</small></span></button></div><div class="wr-nav-note"><b>DIRECTIVE:</b><br>Build the raid. Cover the buffs. Protect the parse.</div></nav>'''
h=re.sub(r'<nav class="wr-nav".*?</nav>',nav,h,count=1,flags=re.S)

# Add ids to the main roster panel and raid frame when possible.
h=h.replace('<section class="panel">','<section class="panel" id="rosterPanel">',1)
h=h.replace('<div class="wr-raidframe">','<div class="wr-raidframe" id="raidFrame">',1)

# Command deck: actual shortcuts, not decoration.
deck='''<div class="wr-command-deck"><button class="wr-command-card primary" type="button" data-jump="raidFrame"><span class="kicker"><span class="wr-live-dot"></span>Raid Command Online</span><strong>Build Tonight's Raid</strong><small>Jump directly to the five-group raid composition and party-buff view.</small></button><button class="wr-command-card" type="button" data-jump="rosterPanel"><span class="kicker">Roster</span><strong>Find Raiders</strong><small>Filter by role, class, rank and search.</small></button><button class="wr-command-card" type="button" data-jump="raiderDossier"><span class="kicker">Inspection</span><strong>Character Dossier</strong><small>Inspect role, attendance, gear score and item level.</small></button><button class="wr-command-card" type="button" data-jump="raidIntelligence"><span class="kicker">Coverage</span><strong>Raid Intelligence</strong><small>Review buff coverage, attendance and War Room activity.</small></button></div>'''
if 'class="wr-command-deck"' not in h:
    marker='<div class="layout" id="commandLayout">'
    h=h.replace(marker,deck+'\n'+marker,1)

# Navigation behavior and active state.
js='''
function wrJump(targetId,source){const target=document.getElementById(targetId);if(!target)return;target.scrollIntoView({behavior:"smooth",block:"start"});target.classList.remove("wr-section-flash");void target.offsetWidth;target.classList.add("wr-section-flash");document.querySelectorAll(".wr-nav-btn").forEach(b=>b.classList.toggle("active",b===source));}
document.querySelectorAll("[data-jump]").forEach(btn=>btn.addEventListener("click",()=>wrJump(btn.dataset.jump,btn.classList.contains("wr-nav-btn")?btn:null)));
'''
if 'function wrJump(' not in h:
    h=h.replace('renderClassStrip();renderRaid();renderRoster();',js+'\nrenderClassStrip();renderRaid();renderRoster();',1)

h=re.sub(r'<strong>WAR ROOM APP • [^<]+</strong>','<strong>WAR ROOM APP • COMMAND CENTER 1.6</strong>',h,count=1)

v=json.loads(vf.read_text(encoding='utf-8'));v['version']='1.6.0';v['notes']=['Native War Room.exe launcher built with official Orc icon','Functional command-center sidebar navigation','New command deck shortcuts','Improved raid-group, roster and dossier interaction polish','Parser-safe automatic GitHub updater retained'];vf.write_text(json.dumps(v,indent=2),encoding='utf-8')
index.write_text(h,encoding='utf-8')
