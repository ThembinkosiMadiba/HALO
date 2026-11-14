# initdb

This folder is mounted read-only over `/docker-entrypoint-initdb.d` in the database container.

Why: the `postgis/postgis` image ships a first-run script (`10_postgis.sh`) that enables PostGIS, PostGIS topology, fuzzystrmatch and the US tiger geocoder in the new database. HALO does not want any of that at start-up. PostGIS is enabled later by a database migration, when geospatial work begins, so every schema change is versioned.

The image only runs `*.sh`, `*.sql` and compressed SQL files from this directory, and only when the data directory is empty. This README is ignored by the image on purpose.

Effect: a fresh database contains only the default extension (plpgsql) and no PostGIS tables.
