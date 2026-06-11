# Command: GREEN Minimal — ARRR R단계 (Respond = GREEN)

**RED 1묶음**당 `src/` **최소 구현**으로 해당 Test ID를 **PASS**시킨다.

**1커밋 = 1 RED 묶음** 원칙. git commit은 **사용자 명시 요청 시만**.

**Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름**.

---

## 실행 트리거

```
/green-minimal
```

추가 입력 없이 동작. **선행:** `/red-test-plan` 블록 3 **RED 묶음 범위** + `/red-skeleton` 또는 `/tdd-red`로 FAIL 확인된 테스트.

---

## 자동 추출

| 항목 | 출처 |
|------|------|
| **RED 묶음 · Test ID** | `/red-test-plan` 블록 3 `RED 묶음 범위` |
| **함수명 · pytest 명령** | 블록 3 테스트 플랜 |
| **Then 기대** | 블록 1 Rule3 · 블록 2 Given→Then |
| **Layer / Track** | 플랜 Phase (기본 `entity` · `Logic`) |

---

## Phase 선언

응답 **첫 줄**:

```
Phase: green | Layer: entity | Track: Logic
```

Boundary: `Layer: boundary` — 동일 절차, 구현 대상만 Boundary 모듈.

---

## 절차

| # | 단계 | 내용 |
|---|------|------|
| 1 | **RED 재확인** | 묶음 내 테스트만 `pytest` → **FAILED** 확인 (`pytest.fail` 또는 미구현·assert 불일치). PASS면 GREEN 진행 금지·원인 보고. |
| 2 | **`src/` 최소 구현** | 이번 RED 묶음 Test ID **만** 통과시키는 최소 코드. 다른 ID·시나리오 선제 구현 금지. |
| 3 | **`pytest.fail` → `assert` 교체** | 스켈레톤(`RED ④`) 잔존 시 `tests/`에서 `pytest.fail` 제거 후 플랜 Then에 맞는 **assert만** 추가. 이미 `/tdd-red`로 assert가 있으면 **tests/ 미수정**. |
| 4 | **PASS 확인** | 묶음 pytest → **전부 PASSED**. 파일 전체 pytest로 **회귀** 확인. |
| 5 | **보고** | PASS Test ID · 변경 파일 · 회귀 결과. 실패 시 즉시 수정 후 재실행. |

---

## 구현 규칙

| 규칙 | 내용 |
|------|------|
| **최소 구현** | 묶음 Test ID 통과에 필요한 분기·로직만. `pass`·`...` stub 제거. |
| **하드코딩 · 매직넘버 금지** | `34` · `16` · `4` 리터럴 금지 → **`entity/constants.py`**(또는 `src/validate_lines.py` SSOT) import |
| **줄 ID** | `LINE_IDS`·`LINE_CELLS` SSOT (`src/validate_lines.py`) — 문자열 하드코딩 금지 |
| **API 계약** | `.cursorrules` — `status` · `failed_lines` · `incomplete` 선행 규칙 |
| **tests/ 수정 범위** | `pytest.fail` → `assert` 치환**만**. 기대값·assert 완화·skip·xfail **금지** |

### ECB (Entity 계층)

| 점검 | Entity (`Layer: entity`) |
|------|--------------------------|
| **import** | **boundary** · **control** 모듈 import **금지** |
| **E001~E005** | `raise` · `return` · emit **금지** — Boundary 예약 코드 |
| **책임** | 도메인·Command (`validate_lines`) 로직만 |

**E001~E005 (Entity에서 사용 금지):** E001 격자 크기 / E002 셀 범위 / E003 중복 / E004 입력 형식 / E005 Boundary 내부 실패.

> `ValueError`(4×4 아님) 등은 PRD·API에 명시된 Entity 예외 Test ID에서만 처리.

---

## 금지

| 금지 | 이유 |
|------|------|
| **이번 RED 묶음 외 Test ID 동시 해결** | 1묶음 = 1 GREEN; 범위 초과 구현 금지 |
| **REFACTOR** | Green 유지 구조 정리는 별도 단계 |
| **assert 완화 · 기대값 변경 · 조건 삭제** | Green을 Red로 속임 |
| **skip · xfail** | 실패 회피 |
| **E001~E005 raise/return** | ECB 위반 |
| **boundary/control import (entity)** | ECB 위반 |
| **리터럴 34·16·4·줄 ID** | SSOT 위반 |
| **git commit / push (명시 없을 때)** | `.cursorrules` |

---

## pytest 명령 예시

**단일 테스트 (묶음 1건):**

```bash
pytest tests/test_validate_lines.py::test_incomplete_when_grid_has_zero -v
```

**파일 전체 (회귀):**

```bash
pytest tests/test_validate_lines.py -v
```

기대: 묶음 **PASSED**, 기존 테스트 **회귀 없음**. 회귀 실패 시 **즉시 수정** 후 재실행·보고.

---

## 구현 예시 (T3 · incomplete 최소)

`src/validate_lines.py` — 0 포함 시만 (다른 status 선제 구현 금지):

```python
def validate_lines(grid: list[list[int]]) -> dict:
    for row in grid:
        for cell in row:
            if cell == 0:
                return {"status": "incomplete", "failed_lines": []}
    ...
```

`tests/` — 스켈레톤 잔존 시 Then만 교체:

```python
    # Then
    assert result["status"] == "incomplete"
    assert result["failed_lines"] == []
```

---

## git (1커밋 = 1 RED 묶음)

| 규칙 | 내용 |
|------|------|
| **원칙** | RED 묶음 1개 GREEN 완료 = 커밋 1개 분량 |
| **실행** | 사용자가 **명시적으로 요청할 때만** `git commit` |
| **메시지** | Test ID·묶음 범위 포함 (예: `green: T3 incomplete`) |

---

## 보고 형식

```
Phase: green | Layer: entity | Track: Logic

## PASS Test ID
- T3

## 변경 파일
- src/validate_lines.py
- tests/test_validate_lines.py  (pytest.fail→assert 치환한 경우만)

## pytest
- 묶음: pytest tests/test_validate_lines.py::test_incomplete_when_grid_has_zero -v → PASSED
- 회귀: pytest tests/test_validate_lines.py -v → N passed

## 회귀
- 없음 (또는: 실패 N건 → 수정 완료 → 재실행 PASSED)

## 다음
- REFACTOR (별도 요청 시) 또는 다음 RED 묶음
```

회귀 실패 시 보고에 **실패 Test ID · 원인 · 수정 내용**을 반드시 기재하고, PASS 확인 전까지 완료로 보고하지 않는다.

---

## ARRR 파이프라인 위치

| 단계 | Command | 산출 |
|------|---------|------|
| A · RED ③ | `/red-test-plan` | 설계표 |
| A · RED ④ | `/red-skeleton` | `pytest.fail` 스켈레톤 |
| A · RED ⑤ | `/tdd-red` | `assert` · FAIL 확인 |
| **R · GREEN** | **`/green-minimal`** | **`src/` 최소 구현 · PASS** |
| R · REFACTOR | *(별도)* | 구조 정리 (Green 유지) |

---

## 참조

| SSOT | 경로 |
|------|------|
| 도메인 · API · TDD | `.cursorrules` |
| 설계 | `.cursor/commands/red-test-plan.md` |
| RED assert | `.cursor/commands/tdd-red.md` |
| 스켈레톤 | `.cursor/commands/red-skeleton.md` |
| 상수 | `entity/constants.py` · `src/validate_lines.py` |
| Skill | `magic-square-tdd` — 있으면 자동 따름 |
