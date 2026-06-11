---
name: unit-converter-tdd
description: >-
  UnitConverter ARRR·Dual-Track TDD (RED/GREEN/REFACTOR, C2C, pytest).
  Use when Phase is red|green|refactor; when running /red-test-plan,
  /red-skeleton, /green-minimal; or when the user mentions Unit Converter,
  TDD, RED, GREEN, REFACTOR, Dual-Track, or C2C for this project.
disable-model-invocation: true
---

# unit-converter-tdd

UnitConverter **길이 단위 변환 CLI** TDD Skill.

**우선순위 (충돌 시):** `docs/PRD.md` · `docs/traceability.md` · `tests/` > **본 Skill** · `.cursor/rules/` > Magic Square Commands (`/red-test-plan` 등). UnitConverter 전용: `/uc-red-plan`, `/uc-green`, `/uc-export-session`.

## SSOT

| 문서 | 경로 |
|------|------|
| PRD | `docs/PRD.md` |
| Traceability | `docs/traceability.md` |
| To-Do | `docs/TODO.md` |
| Rules | `.cursor/rules/unit-converter.mdc` |

## ARRR ↔ TDD

| ARRR | TDD | Command (UnitConverter) |
|------|-----|-------------------------|
| Ask | RED | `/uc-red-plan` → tests 작성 (1 TD = 1 commit) |
| Respond | GREEN | `/uc-green` |
| Refine | REFACTOR | `/refactor-smell` → `/refactor-safe` (참고만; TD-05~06) |
| Export | 문서화 | `/uc-export-session` |

## Phase 선언 (응답 첫 줄)

- RED Domain: `Phase: red | Layer: entity | Track: Logic`
- RED Boundary: `Phase: red | Layer: boundary | Track: UI`
- GREEN: `Phase: green | Layer: entity | Track: Logic`
- REFACTOR: `Phase: refactor | Layer: entity | Track: Logic`

## Dual-Track

| Track | 파일 | 검증 대상 |
|-------|------|-----------|
| A (Boundary) | `tests/test_cli.py` | U-IN-*, U-OUT-*, U-FMT-* |
| B (Domain) | `tests/test_converter.py` | D-PAR-*, D-CNV-*, D-REG-*, D-CFG-*, D-STR-* |

## C2C Rules

1. 판단 포함 FR만 테스트로 변환
2. 1 To-Do : 1+ Test Case
3. RED first — FAIL 확인 후 GREEN

## RED 금지

- `src/` / `unit_converter/` 구현 (스켈레톤 테스트만)
- skip / xfail
- 한 커밋에 여러 RED 묶음

## Test ID prefix

- `D-PAR` — parsing
- `D-CNV` — conversion
- `D-REG` — registry / OCP
- `D-CFG` — config load
- `D-STR` — SRP module structure
- `U-IN` / `U-OUT` / `U-FMT` — CLI boundary

## TD → Test ID (P0 RED 완료 기준)

| TD | Test ID | Track |
|----|---------|-------|
| TD-01 | D-PAR-01~03, U-IN-01~04 | B + A |
| TD-02 | D-CNV-01~03 | B |
| TD-03 | D-REG-01~02 | B |
| TD-04 | U-OUT-01 | A |

## GREEN API (tests가 고정한 계약)

| 모듈 | 심볼 |
|------|------|
| `app/input_parser.py` | `parse`, `ParseError` |
| `domain/converter.py` | `to_meter`, `convert_all(unit, value, registry=None)` |
| `domain/unit_registry.py` | `UnitRegistry`, `UnknownUnitError` |
| `cli.py` + `__main__.py` | `python -m unit_converter` subprocess 대상 |

## pytest

```bash
pytest tests/ -v
pytest tests/test_converter.py -v
pytest tests/test_cli.py -v
```

## Commands

| 사용 | 파일 |
|------|------|
| ✅ `/uc-red-plan` | `uc-red-plan.md` |
| ✅ `/uc-green` | `uc-green.md` |
| ✅ `/uc-export-session` | `uc-export-session.md` |
| ⚠️ 참고만 | `red-test-plan`, `green-minimal`, … (Magic Square — `src/`, `validate_lines`) |

상세: `.cursor/commands/README.md`
