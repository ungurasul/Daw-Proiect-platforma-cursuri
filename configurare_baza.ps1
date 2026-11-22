# Rulează cu dot-sourcing din terminalul care va porni Django:
# . .\configurare_baza.ps1
$pgCtl = 'C:\Program Files\PostgreSQL\18\bin\pg_ctl.exe'
$pgIsReady = 'C:\Program Files\PostgreSQL\18\bin\pg_isready.exe'
$clusterPath = Join-Path $env:LOCALAPPDATA 'Cursora\PostgreSQL\data'
$logPath = Join-Path (Split-Path $clusterPath -Parent) 'server.log'

if (-not (Test-Path -LiteralPath $clusterPath)) {
    throw "Instanța PostgreSQL Cursora nu a fost inițializată: $clusterPath"
}
if (-not (Test-Path -LiteralPath $pgCtl)) {
    throw "Nu am găsit pg_ctl: $pgCtl"
}
if (-not (Test-Path -LiteralPath $pgIsReady)) {
    throw "Nu am găsit pg_isready: $pgIsReady"
}

& $pgIsReady -h 127.0.0.1 -p 5433 *> $null
if ($LASTEXITCODE -ne 0) {
    & $pgCtl start -D $clusterPath -l $logPath -o '-h 127.0.0.1 -p 5433' -w
    if ($LASTEXITCODE -ne 0) {
        throw 'The Cursora PostgreSQL instance did not start.'
    }
}

$env:POSTGRES_DB = 'cursora_db'
$env:POSTGRES_USER = 'cursora_user'
$env:POSTGRES_HOST = '127.0.0.1'
$env:POSTGRES_PORT = '5433'
$env:POSTGRES_PASSWORD = ''

$envFile = Join-Path $PSScriptRoot '.env'
if (-not $env:DJANGO_SECRET_KEY) {
    if (Test-Path -LiteralPath $envFile) {
        $keyLine = Get-Content -LiteralPath $envFile -Encoding utf8 | Where-Object { $_ -like 'DJANGO_SECRET_KEY=*' } | Select-Object -First 1
        if ($keyLine) {
            $env:DJANGO_SECRET_KEY = $keyLine.Substring('DJANGO_SECRET_KEY='.Length)
        }
    }

    if (-not $env:DJANGO_SECRET_KEY) {
        $secretBytes = [byte[]]::new(48)
        $random = [System.Security.Cryptography.RandomNumberGenerator]::Create()
        $random.GetBytes($secretBytes)
        $random.Dispose()
        $env:DJANGO_SECRET_KEY = [Convert]::ToBase64String($secretBytes)
        Set-Content -LiteralPath $envFile -Value "DJANGO_SECRET_KEY=$env:DJANGO_SECRET_KEY" -Encoding ascii
        $secretBytes = $null
    }
}

Write-Host 'PostgreSQL Cursora este pornit pe localhost:5433.'
