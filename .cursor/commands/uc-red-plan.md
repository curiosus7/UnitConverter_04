# Command: UC RED Plan — UnitConverter TD 묶음 설계

**C2C 설계표만** 작성. `unit_converter/` **구현 금지**. `tests/` 수정은 `/uc-green` 전 RED 스켈레톤 단계에서만.

**Skill:** `unit-converter-tdd` · **SSOT:** `docs/traceability.md`, `docs/TODO.md`

---

## 실행

```
/uc-red-plan
```

선택: `TD-01` ~ `TD-04` (미지정 시 `docs/TODO.md`에서 다음 pending TD)

---

## Phase 선언 (첫 줄)

- Domain: `Phase: red | Layer: entity | Track: Logic`
- Boundary: `Phase: red | Layer: boundary | Track: UI`

---

## 출력 (표 형식, 파일 쓰기 없음)

### 1. C2C (Rule1~3)

| Rule | 내용 |
|------|------|
| Rule1 | PRD FR/NFR 인용 (`docs/PRD.md`) |
| Rule2 | To-Do 1개 (`docs/TODO.md` TD-NN) |
| Rule3 | Test ID + Given / When / Then (`docs/traceability.md`) |

### 2. Dual-Track 표

| Test ID | Track | 파일 | 대상 API / CLI |
|---------|-------|------|----------------|
| … | A or B | `test_cli.py` / `test_converter.py` | … |

### 3. RED 묶음 범위

- 이번 커밋에 포함할 Test ID 목록 (1 TD = 1 커밋)
- `pytest` 명령 (묶음·전체)

### 4. 금지 확인

- [ ] `unit_converter/` 미작성
- [ ] skip / xfail 없음
- [ ] 오류 메시지 SSOT 문자열 사용

---

## TD → Test ID 빠른 참조

| TD | Test ID |
|----|---------|
| TD-01 | D-PAR-01~03, U-IN-01~04 |
| TD-02 | D-CNV-01~03 |
| TD-03 | D-REG-01~02 |
| TD-04 | U-OUT-01 |

P1 (`D-CFG`, `U-FMT`, `D-REG-03`) · REFACTOR (`D-STR`)는 `new_features` / `refactoring` 브랜치.
