# Command: UC GREEN — UnitConverter 최소 구현

**RED 1묶음(TD-NN)** 당 `unit_converter/` 최소 구현으로 해당 Test ID **PASS**.

**1 RED 묶음 = 1 GREEN 커밋** (사용자 명시 요청 시만 commit).

**Skill:** `unit-converter-tdd` · **SSOT:** `tests/test_*.py` + `docs/traceability.md`

---

## 실행

```
/uc-green
```

선택: `TD-01` ~ `TD-04`

---

## Phase 선언 (첫 줄)

`Phase: green | Layer: entity | Track: Logic` (CLI만이면 `boundary | UI`)

---

## 절차

1. **RED 재확인** — 묶음 테스트 `pytest` → FAILED
2. **최소 구현** — 이번 TD Test ID만 통과 (`unit_converter/`)
3. **PASS** — 묶음 + 전체 `pytest tests/ -v` 회귀
4. **보고** — 변경 파일 · PASS Test ID

---

## TD별 구현 힌트 (테스트 계약)

| TD | 모듈 | API |
|----|------|-----|
| TD-01 | `app/input_parser.py` | `parse(str)→(unit,value)`, `ParseError`, E-FMT/E-NUM/E-NEG |
| TD-02 | `domain/converter.py` | `to_meter(unit,value)`, `convert_all(unit,value, registry=None)` |
| TD-03 | `domain/unit_registry.py` | `UnitRegistry.default()`, `.register()`, `UnknownUnitError` |
| TD-04 | `cli.py`, `__main__.py` | `python -m unit_converter "meter:2.5"`, 3줄+ 4자리 출력 |

---

## 금지

- 이번 TD 외 Test ID 선제 구현
- assert 완화 · skip · xfail
- `UnitConverter.py` 시드 수정 (GREEN은 `unit_converter/` 패키지)
- 사용자 요청 없이 git commit

---

## pytest

```bash
pytest tests/test_converter.py -v -k "d_par"   # TD-01 B
pytest tests/test_cli.py -v -k "u_in"          # TD-01 A
pytest tests/ -v
```
