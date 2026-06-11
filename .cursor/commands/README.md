# Cursor Commands — UnitConverter_04

## ⚠️ 중요: Magic Square 템플릿 잔재

`red-test-plan.md`, `red-skeleton.md`, `green-minimal.md`, `refactor-*.md`, `golden-master.md`, `tdd-red.md`, `export-session.md`는 **Magic Square 실습용**입니다.

| Magic Square Command | UnitConverter에서 쓰면 안 되는 이유 |
|----------------------|-------------------------------------|
| `/red-test-plan` 등 | `src/`, `validate_lines`, `entity.constants` 전제 |
| `/green-minimal` | `src/validate_lines.py` 예시, ECB E001~E005 |
| `/export-session` | Report 템플릿이 `MagicSquare_00` |

**UnitConverter 작업 시 SSOT 우선순위:**

1. `docs/PRD.md` v0.2
2. `docs/traceability.md`
3. `docs/TODO.md`
4. `.cursor/rules/unit-converter.mdc`
5. `.cursor/skills/unit-converter-tdd/SKILL.md`
6. 기존 `tests/test_*.py` (RED에서 고정된 계약)

## UnitConverter 전용 Command (권장)

| Command | 파일 | 용도 |
|---------|------|------|
| `/uc-red-plan` | `uc-red-plan.md` | TD 묶음별 RED 테스트 플랜 (파일 쓰기 없음) |
| `/uc-green` | `uc-green.md` | TD 묶음별 최소 GREEN 구현 |
| `/uc-export-session` | `uc-export-session.md` | Report + Transcript Export |

## Magic Square → UnitConverter 치환표

| Magic Square | UnitConverter |
|--------------|---------------|
| `src/` | `unit_converter/` |
| `.cursorrules` | `.cursor/rules/unit-converter.mdc` |
| `tests/test_validate_lines.py` | `tests/test_converter.py` (B), `tests/test_cli.py` (A) |
| `validate_lines(grid)` | `parse()`, `to_meter()`, `convert_all()`, CLI |
| Test ID `T3` | `D-PAR-01`, `U-IN-01` 등 (`docs/traceability.md`) |
| `magic-square-tdd` Skill | `unit-converter-tdd` Skill |
