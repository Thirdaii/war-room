from pathlib import Path
import json,re,sys
root=Path(sys.argv[1]); index=root/'index.html'; vf=root/'version.json'; updater=root/'WarRoomUpdater.ps1'
h=index.read_text(encoding='utf-8')
# Keep the v1.5 cinematic UI already present in the base package.
# Repair updater by replacing the fragile splash-injected implementation with a clean parser-safe updater.
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
v=json.loads(vf.read_text(encoding='utf-8'));v['version']='1.5.1';v['notes']=['Hotfix: repaired PowerShell updater parser','Preserved dedicated Edge/Chrome app-mode launcher','Automatic GitHub update pipeline retained','v1.5 cinematic interface retained'];vf.write_text(json.dumps(v,indent=2),encoding='utf-8')
index.write_text(h,encoding='utf-8')
