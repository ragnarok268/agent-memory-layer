# DS2 Report

DS2 is `ps + netstat + tree for dependency/runtime authority`.

## 1. Project path

- `examples/fastapi_app`

## 2. Detected dependency sources

- `requirements.txt`
- `source_import_scan`

## 3. Direct dependencies

| Package | Source | Imported | Exposures | Authority |
| --- | --- | --- | --- | --- |
| `fastapi` | `requirements.txt` | `true` | `ASYNC_RUNTIME, NETWORK_SERVER` | `HIGH_ATTENTION` |
| `httpx` | `requirements.txt` | `true` | `ASYNC_RUNTIME, NETWORK_CLIENT` | `REVIEW_RECOMMENDED` |
| `sqlalchemy` | `requirements.txt` | `true` | `DATABASE_PERSISTENCE` | `REVIEW_RECOMMENDED` |

## 4. Import-observed packages

- `fastapi`
- `httpx`
- `sqlalchemy`
- `starlette`

## 5. Runtime exposure classifications

- `ASYNC_RUNTIME`: 3
- `DATABASE_PERSISTENCE`: 1
- `NETWORK_CLIENT`: 1
- `NETWORK_SERVER`: 2
- `fastapi` -> ASYNC_RUNTIME, NETWORK_SERVER
- `httpx` -> ASYNC_RUNTIME, NETWORK_CLIENT
- `sqlalchemy` -> DATABASE_PERSISTENCE
- `starlette` -> ASYNC_RUNTIME, NETWORK_SERVER

## 6. Authority expansion notes

- `fastapi`: HIGH_ATTENTION; exposures=ASYNC_RUNTIME, NETWORK_SERVER.
- `httpx`: REVIEW_RECOMMENDED; exposures=ASYNC_RUNTIME, NETWORK_CLIENT.
- `sqlalchemy`: REVIEW_RECOMMENDED; exposures=DATABASE_PERSISTENCE.
- `starlette`: HIGH_ATTENTION; exposures=ASYNC_RUNTIME, NETWORK_SERVER.

## 7. Build-time vs runtime exposure

- Build-only dependencies: none detected.
- Runtime-observed packages: fastapi, httpx, sqlalchemy, starlette.
- Transitive dependency graph is partial.
- Exposure classes observed: ASYNC_RUNTIME, DATABASE_PERSISTENCE, NETWORK_CLIENT, NETWORK_SERVER.

## 8. Dependency chains if available

- No dependency chains available.

## 9. Manual review notes

- High-attention packages expand execution authority and should be reviewed for actual runtime reachability.

## 10. Deterministic receipt hash

- `b02f53ea9bafb7658270805dc54905edd13755450502cc1c135dedccb425006f`
