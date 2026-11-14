<#
.SYNOPSIS
  Read-only check that a fresh HALO database is in its controlled baseline state.

.DESCRIPTION
  Baseline = a new database BEFORE the first Alembic migration: only the plpgsql
  extension, only the public schema, no tables or views, no template_postgis
  database, and one role (halo_owner). The PostGIS binaries remain installed in the
  image so that a later migration can enable them.

  This check is EXPECTED TO FAIL once HALO tables or extensions exist. It describes
  the starting state only.
#>
param(
  [string]$Container = "halo-db",
  [string]$Database  = "halo",
  [string]$DbUser    = "halo_owner"
)

$script:failures = 0

function Invoke-Sql([string]$Db, [string]$Sql) {
  $out = docker exec $Container psql -h 127.0.0.1 -U $DbUser -d $Db -tA -c $Sql 2>&1
  if ($LASTEXITCODE -ne 0) { throw ("psql failed: " + ($out | Out-String).Trim()) }
  return (($out | Out-String).Trim())
}

function Test-Value([string]$Name, [string]$Actual, [string]$Expected) {
  if ($Actual -ceq $Expected) {
    Write-Host ("PASS  " + $Name) -ForegroundColor Green
  } else {
    Write-Host ("FAIL  " + $Name + " (expected '" + $Expected + "', got '" + $Actual + "')") -ForegroundColor Red
    $script:failures++
  }
}

try {
  Write-Host ("Server version: " + (Invoke-Sql $Database "SHOW server_version;"))

  Test-Value "Extensions installed" `
    (Invoke-Sql $Database "SELECT string_agg(extname, ',' ORDER BY extname) FROM pg_extension;") "plpgsql"

  Test-Value "Schemas (excluding system schemas)" `
    (Invoke-Sql $Database "SELECT string_agg(nspname, ',' ORDER BY nspname) FROM pg_namespace WHERE nspname !~ '^pg_' AND nspname <> 'information_schema';") "public"

  Test-Value "Tables, views and sequences outside system schemas" `
    (Invoke-Sql $Database "SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname NOT IN ('pg_catalog','information_schema','pg_toast') AND c.relkind IN ('r','p','v','m','S','f');") "0"

  Test-Value "Databases" `
    (Invoke-Sql "postgres" "SELECT string_agg(datname, ',' ORDER BY datname) FROM pg_database;") "halo,postgres,template0,template1"

  Test-Value "Roles (excluding built-in pg_ roles)" `
    (Invoke-Sql "postgres" "SELECT string_agg(rolname, ',' ORDER BY rolname) FROM pg_roles WHERE rolname !~ '^pg_';") "halo_owner"

  Test-Value "PostGIS installable later (binaries present)" `
    (Invoke-Sql $Database "SELECT count(*) FROM pg_available_extensions WHERE name = 'postgis';") "1"
}
catch {
  Write-Host ("ERROR " + $_.Exception.Message) -ForegroundColor Red
  exit 2
}

if ($script:failures -gt 0) {
  Write-Host ("Baseline NOT verified: " + $script:failures + " check(s) failed.") -ForegroundColor Red
  exit 1
}
Write-Host "Baseline verified." -ForegroundColor Green
exit 0
