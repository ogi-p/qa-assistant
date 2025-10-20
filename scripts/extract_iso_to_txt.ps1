$ErrorActionPreference = 'Stop'

$stdDir = Join-Path (Get-Location) '06-documentation/standards'

# Download and extract Xpdf tools (pdftotext)
$zip = Join-Path $env:TEMP 'xpdf-tools-win-4.05.zip'
$dest = Join-Path $env:TEMP 'xpdf-tools-win-4.05'
Invoke-WebRequest -Uri 'https://dl.xpdfreader.com/xpdf-tools-win-4.05.zip' -OutFile $zip
if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
Expand-Archive -Path $zip -DestinationPath $dest -Force

$pdftotext = Get-ChildItem -Recurse -Path $dest -Filter 'pdftotext.exe' | Select-Object -First 1 -ExpandProperty FullName
if (-not (Test-Path $pdftotext)) { throw 'pdftotext.exe not found' }

$iso1 = Join-Path $stdDir 'ISO_IEC 25010_2023 Systems and software engineering Systems and software Quality Requirements and Evaluation (SQuaRE) Product - libgen.li.pdf'
$iso2 = Join-Path $stdDir 'ISO_IEC_IEEE 29119-1_2022 Software and systems engineering Software testing Part 1_ General concepts - libgen.li.pdf'
$out1 = Join-Path $stdDir 'ISO_25010.txt'
$out2 = Join-Path $stdDir 'ISO_29119-1.txt'

& $pdftotext '-layout' '-nopgbrk' $iso1 $out1
& $pdftotext '-layout' '-nopgbrk' $iso2 $out2

Write-Output "Extracted:`n - $out1`n - $out2"


