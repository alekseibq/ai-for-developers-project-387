# AGENTS.md — CalCom Clone

## Project Overview

Full-stack meeting booking app (Calendly/Cal.com clone).
Guests browse meeting types, pick time slots, book appointments.
Admins manage meeting types (CRUD).

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Frontend | Vue 3 (Composition API, `<script setup>`) | ^3.5 |
| Build tool | Vite | ^6.2 |
| State manager | Pinia (composition stores) | ^3.0 |
| Router | Vue Router (lazy routes) | ^4.5 |
| Styling | Tailwind CSS (utility classes only, no scoped CSS) | ^3.4 |
| Language (FE) | TypeScript (strict) | ^5.7 |
| Testing (FE) | Vitest + @vue/test-utils + jsdom | ^4.1 / ^2.4 |
| E2E | Playwright | ^1.60 |
| Backend | FastAPI | ^0.115 |
| Language (BE) | Python | ^3.12 |
| Data validation | Pydantic (BaseModel) | ^2.10 |
| DB driver | Motor (async MongoDB) | ^3.7 |
| ASGI server | Uvicorn | ^0.34 |
| Dependency mgr | Poetry | — |
| Testing (BE) | pytest + pytest-asyncio + httpx + testcontainers | — |
| Linter (BE) | Ruff (line-length=100) | ^0.9 |
| API contracts | TypeSpec → OpenAPI3 | latest |
| Infra | Docker (multi-stage), docker-compose, Nginx | — |

## Architecture

### Backend — Clean / Layered Architecture

```
api/v1/          # Thin HTTP layer (parse request → call use case → map DTO → respond)
usecases/        # Single-responsibility callable classes, one per operation
services/        # Reusable stateless business logic
repositories/    # Data access (MongoDB documents ↔ domain objects)
domain/          # Pure Pydantic domain objects, no infra deps
infrastructure/  # DB connection manager, DI wiring (FastAPI Depends)
```

- Import style: **absolute imports only**, full path from `app/` root.
  - ✅ `from app.domain.result import Success, Failure`
  - ❌ `from ..result import Success`
- UseCase pattern:
  ```python
  class CreateMeetingTypeUseCase:
      def __init__(self, repo: MeetingTypeRepository): ...
      async def __call__(self, name: str, ...) -> Success[MeetingTypeObj] | Failure: ...
  ```
- DI wiring: centralized in `infrastructure/di.py`, composed via `Depends()`.

### Frontend — Feature-based

```
api/       # HTTP client (base wrappers in client.ts, one file per entity)
stores/    # Pinia composition stores
router/    # Lazy-loaded routes
types/     # Hand-written TS types matching TypeSpec contracts
pages/     # Route-level page components, grouped by domain (booking/, admin/)
components/# Reusable UI components
```

- Import style: **`@/` path alias** (maps to `src/`).
  - ✅ `import { useMeetingTypesStore } from "@/stores/meetingTypes"`
  - ✅ `import type { MeetingType } from "@/types/generated"`
- Components: always `<script setup lang="ts">`, Tailwind classes only, no scoped CSS.
- Page components fetch data in `onMounted`, render 3 states: loading / error / data.

## Naming Conventions

### Python (Backend)
| Entity | Convention | Example |
|---|---|---|
| Domain object | `*Obj` suffix | `MeetingTypeObj`, `SlotObj` |
| API DTO | `*Dto` / `*Request` suffix | `MeetingTypeDto`, `CreateMeetingTypeRequest` |
| Use case | `*UseCase` class | `FindSlotsUseCase` |
| Repository method | `find_*`, `create` | `find_all`, `create` |
| Private methods | underscore prefix | `_doc_to_obj`, `_overlaps` |
| Files | `snake_case` | `meeting_type_repository.py` |

### TypeScript / Vue (Frontend)
| Entity | Convention | Example |
|---|---|---|
| Components | PascalCase file | `BookingSlotPage.vue` |
| Stores | camelCase file | `meetingTypes.ts` |
| Store accessor | `use*Store` | `useMeetingTypesStore` |
| Types/Interfaces | PascalCase | `MeetingType`, `SlotDto` |
| Functions/vars | camelCase | `fetchMeetingTypes`, `selectedDate` |
| Files | camelCase | `meetingTypes.ts`, `client.ts` |

## Result Pattern (Critical)

Every API response across all layers uses the **Success/Failure discriminated union**:

### TypeSpec
```
alias Result<T> = Success<T> | Failure;
model Success<T> { type: "success", data: T };
model Failure { type: "failure", error: string, code: string };
```

### Python
```python
class Success(BaseModel, Generic[T]):
    type: Literal["success"] = "success"
    data: T

class Failure(BaseModel):
    type: Literal["failure"] = "failure"
    error: str
    code: str  # UPPER_SNAKE_CASE error codes
```

### TypeScript
```typescript
type Result<T> =
  | { type: "success"; data: T }
  | { type: "failure"; error: string; code: string };
```

- **Always** narrow before accessing: `if (result.type === "success") { result.data }`.
- Error codes examples: `INVALID_NAME`, `SLOT_TAKEN`, `DB_ERROR`, `NETWORK`.

## Component Patterns (Vue 3)

```vue
<script setup lang="ts">
import { onMounted } from "vue"
import { useMeetingTypesStore } from "@/stores/meetingTypes"

const store = useMeetingTypesStore()
onMounted(() => { store.fetchMeetingTypes() })
</script>

<template>
  <div v-if="store.loading">Загрузка...</div>
  <div v-else-if="store.error" class="text-red-600">{{ store.error }}</div>
  <div v-else>...</div>
</template>
```

- Store actions are `async`, handle both success and failure.
- API functions return `Promise<Result<T>>` (typed).

## Testing

### Backend (pytest)
- Async tests use `asyncio_mode = "auto"` (no decorator needed).
- Integration tests: `testcontainers` for real MongoDB.
- API tests: `httpx.AsyncClient` with `ASGITransport`.
- Repo mocking: `unittest.mock.AsyncMock`.
- Test files mirror source structure under `tests/`.

### Frontend (Vitest)
- Pinia must be activated per test: `setActivePinia(createPinia())` in `beforeEach`.
- API mocking: `vi.mock()` + `vi.stubGlobal("fetch", ...)`.
- Component mounting: `mount(Component, { global: { plugins: [router, pinia] } })`.
- Time-dependent tests: `vi.useFakeTimers()` / `vi.setSystemTime()`.
- Test files mirror source structure under `tests/`.

### E2E (Playwright)
- API mocking via `page.route("**/api/v1/...", handler)`.
- Run: `npm run e2e` (frontend/) or `make e2e` (Docker).

## Commands

| Make | What it does |
|---|---|
| `make dev` | Docker compose up (full stack) |
| `make dev-backend` | uvicorn hot-reload on :8000 |
| `make dev-frontend` | `npm run dev` on :5173 |
| `make test` | `pytest -v` (backend) |
| `make lint` | ruff (BE) + vue-tsc (FE) |
| `make coverage` | pytest + coverage report |
| `make generate` | TypeSpec → OpenAPI |
| `make ci` | test + lint + e2e |

Also: `npm run test:unit` (FE vitest), `npm run lint` (FE vue-tsc only).

## Conventional Commits (Required)

Every commit **must** follow the [Conventional Commits](https://www.conventionalcommits.org/) format.
Both hooks (local) and CI (PR) enforce it via commitlint.

```
type(scope): description

[optional body]

[optional footer]
```

**Allowed types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

**Examples:**
```
feat(api): add create meeting type endpoint
fix(frontend): handle empty slot list
docs: update API contract in AGENTS.md
refactor(backend): extract slot overlap logic
```

- `scope` is optional but encouraged (e.g. `backend`, `frontend`, `typespec`, `infra`).
- `BREAKING CHANGE:` in footer (or `!` after type/scope) marks a breaking change.
- Reverts: `revert: type: message` (commitlint infers type from the reverted commit).

## Branching & PR Workflow

- **Direct pushes to `main` are forbidden.** All changes must go through a feature branch and a Pull Request.
- Branch from `main`, push your feature branch, open a PR, get it reviewed and merged.
- PR title should also follow Conventional Commits (used for squash-merge commit message).

## Conventions Summary
1. Result Pattern on every API response.
2. Absolute imports only (Python); `@/` alias (TS).
3. UseCase as callable class with DI.
4. Pinia composition stores (not options API).
5. Vue components: `<script setup lang="ts">`, Tailwind only, 3-state rendering.
6. Test files mirror source (one-to-one).
7. TypeSpec is source of truth for API contracts; generated OpenAPI is checked in.
8. Ruff line-length=100, no trailing commas convention observed.
9. **Conventional Commits** enforced locally (commit-msg hook) and in CI (PR).
