# backend-fastapi

## Supabase CLI troubleshooting

Running `supabase db pull` boots the local Supabase stack using the version
information cached under `supabase/.temp`. The cache currently records the
latest storage migration as `iceberg-catalog-ids` (`supabase/.temp/storage-migration:1`),
but the checked-in CLI binary (`supabase --version` → `2.54.11`) ships an older
storage image that does not include that migration. As a result the pull fails
with `StorageBackendError: Migration iceberg-catalog-ids not found`.

Update the Supabase CLI to `2.58.5` or later so the bundled storage service
knows about that migration:

```bash
brew update
brew upgrade supabase/tap/supabase
supabase --version  # expect >= 2.58.5
```

If the cache under `supabase/.temp` was created with the old binary, remove it so
the CLI refreshes the project metadata after upgrading:

```bash
rm -rf supabase/.temp
supabase login --profile supabase
```

Re-run `supabase db pull --debug` afterwards. The command should reach the
remote database and exit cleanly once the CLI and cached stack metadata are in
sync.
