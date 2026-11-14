<#
.SYNOPSIS
  Destroys and recreates the HALO development database volume, then verifies the baseline.

.DESCRIPTION
  DESTRUCTIVE. Deletes the Docker volume that holds the HALO database.
  Safety gates:
    1. If the volume exists, the script starts the database and counts relations that
       do not belong to an extension. Anything above zero means the database holds
       HALO data, and the script stops unless -IKnowThisDeletesHaloData is given.
    2. You must type DELETE to continue.
  After recreating the volume it runs verify-database-baseline.ps1.
#>
param([switch]$IKnowThisDeletesHaloData)

$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

$Container = "halo-db"
$Volume    = "halo_halo_pgdata"
$DbUser    = "halo_owner"
$Database  = "halo"

function Invoke-Sql([string]$Sql) {
  $out = docker exec $Container psql -h 127.0.0.1 -U $DbUser -d $Database -tA -c $Sql 2>&1
  if ($LASTEXITCODE -ne 0) { throw ("psql failed: " + ($out | Out-String).Trim()) }
  return (($out | Out-String).Trim())
}

function Wait-DbReady {
  for ($i = 1; $i -le 45; $i++) {
    $r = docker exec $Container psql -h 127.0.0.1 -U $DbUser -d $Database -tA -c "SELECT 1;" 2>&1
    if ($LASTEXITCODE -eq 0 -and (($r | Out-String).Trim() -eq "1")) { return $true }
    Start-Sleep -Seconds 2
  }
  return $false
}

docker info *> $null
if ($LASTEXITCODE -ne 0) {
  Write-Host "Docker engine is not running. Start Docker Desktop and try again." -ForegroundColor Red
  exit 2
}
if (-not (Test-Path (Join-Path $repo ".env"))) {
  Write-Host ".env is missing. Create it first." -ForegroundColor Red
  exit 2
}

docker volume inspect $Volume *> $null
$volumeExists = ($LASTEXITCODE -eq 0)

if ($volumeExists) {
  Write-Host ("Volume '" + $Volume + "' exists. Starting the database to inspect it...")
  docker compose up -d | Out-Null
  if (-not (Wait-DbReady)) {
    Write-Host "Database did not become ready. Not deleting anything." -ForegroundColor Red
    exit 2
  }
  try {
    $ext     = Invoke-Sql "SELECT string_agg(extname, ',' ORDER BY extname) FROM pg_extension;"
    $schemas = Invoke-Sql "SELECT string_agg(nspname, ',' ORDER BY nspname) FROM pg_namespace WHERE nspname !~ '^pg_' AND nspname <> 'information_schema';"
    $notExt  = "FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname NOT IN ('pg_catalog','information_schema','pg_toast') AND c.relkind IN ('r','p','v','m','S','f') AND NOT EXISTS (SELECT 1 FROM pg_depend d WHERE d.classid = 'pg_class'::regclass AND d.objid = c.oid AND d.deptype = 'e')"
    $count   = Invoke-Sql ("SELECT count(*) " + $notExt + ";")
  } catch {
    Write-Host ("Could not inspect the database: " + $_.Exception.Message) -ForegroundColor Red
    exit 2
  }
  Write-Host ("Extensions: " + $ext)
  Write-Host ("Schemas:    " + $schemas)
  Write-Host ("Relations NOT owned by an extension: " + $count)

  if ($count -ne "0" -and -not $IKnowThisDeletesHaloData) {
    Write-Host "STOPPED: the database holds objects that are not part of an extension. Listing them:" -ForegroundColor Red
    Invoke-Sql ("SELECT n.nspname || '.' || c.relname " + $notExt + " ORDER BY 1 LIMIT 50;")
    Write-Host "If you really want to delete this data, re-run with -IKnowThisDeletesHaloData." -ForegroundColor Red
    exit 3
  }

  Write-Host ""
  Write-Host ("This will DELETE the Docker volume '" + $Volume + "' and everything in it.") -ForegroundColor Yellow
  $answer = Read-Host "Type DELETE (capitals) to continue, anything else cancels"
  if ($answer -cne "DELETE") {
    Write-Host "Cancelled. Nothing was changed."
    exit 0
  }
  docker compose down -v
  if ($LASTEXITCODE -ne 0) {
    Write-Host "docker compose down -v failed." -ForegroundColor Red
    exit 2
  }
} else {
  Write-Host ("Volume '" + $Volume + "' does not exist. Nothing to delete.")
}

docker compose up -d
if ($LASTEXITCODE -ne 0) {
  Write-Host "docker compose up failed." -ForegroundColor Red
  exit 2
}
if (-not (Wait-DbReady)) {
  Write-Host "The new database did not become ready in time." -ForegroundColor Red
  exit 2
}

& (Join-Path $PSScriptRoot "verify-database-baseline.ps1")
exit $LASTEXITCODE
