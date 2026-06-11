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

UnitConverter **길이 단위 변환 CLI** TDD Skill. Command 본문과 충돌 시 **Command 우선**, 도메인·API는 SSOT 우선.

## SSOT

| 문서 | 경로 |
|------|------|
| PRD | `docs/PRD.md` |
| Traceability | `docs/traceability.md` |
| To-Do | `docs/TODO.md` |
| Rules | `.cursor/rules/unit-converter.mdc` |

## ARRR ↔ TDD

| ARRR | TDD | Command |
|------|-----|---------|
| Ask | RED | `/red-test-plan` → `/red-skeleton` → `/tdd-red` |
| Respond | GREEN | `/green-minimal` |
| Refine | REFACTOR | `/refactor-smell` → `/refactor-safe` |

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

## pytest

```bash
pytest tests/ -v
pytest tests/test_converter.py -v
pytest tests/test_cli.py -v
```

## Commands 주의

`.cursor/commands/`의 `red-test-plan` 등은 **Magic Square 템플릿** 기반이다.  
UnitConverter 작업 시 **본 Skill + `docs/PRD.md` + `docs/traceability.md`** 를 SSOT로 사용하고, Command는 워크플로 참고만 한다.
