# Command: RED Skeleton — ARRR A단계 (RED ④)

`/red-test-plan` 설계표 기준 **`pytest.fail` 스켈레톤만** `tests/`에 작성한다.

ARRR **A(Ask)** = RED ④ — Assert 본문 없이 **FAIL 골격**만 만든다. 실제 `assert`는 다음 `/tdd-red`에서 치환.

**Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름** (픽스처·명명·AAA·상수 import 규칙 우선).

---

## 실행 트리거

```
/red-skeleton
```

추가 입력 없이 동작. **선행:** 같은 세션의 `/red-test-plan` 출력(채팅·Report) 또는 블록 3 테스트 플랜.

---

## 자동 추출

| 항목 | 출처 |
|------|------|
| Test ID · 함수명 · 픽스처 | `/red-test-plan` 블록 2·3 |
| GWT · Then 기대 | `/red-test-plan` 블록 1 Rule3 |
| 파일 경로 | 블록 3 **파일 경로** (기본 `tests/test_validate_lines.py`) |
| Layer / Track | 플랜 Phase 선언과 동일 (기본 `entity` · `Logic`) |

플랜이 없으면 채팅·Report·`.cursorrules`에서 시나리오 1건 추론 후 **플랜 없음**을 보고에 명시.

---

## Phase 선언

응답 **첫 줄**:

```
Phase: red | Layer: entity | Track: Logic
```

Track A(Boundary): `Layer: boundary` — 스켈레톤 형식 동일, 대상 함수만 Boundary로 치환.

---

## 절차

1. `/red-test-plan` 블록 3 확인 (Test ID, 함수명, conftest, pytest 명령).
2. **`tests/`만** 수정: `conftest.py`(필요 시), 테스트 파일에 스켈레톤 **1건** 추가(또는 플랜 묶음 범위).
3. **AAA 주석** + **Act까지** 작성; **Then = `pytest.fail(...)` 한 줄만**.
4. `src/` **미수정** 확인.
5. 루트에서 `pytest` 실행 → **FAILED** (`pytest.fail` 메시지) 확인.
6. 보고 형식으로 결과 제출.

---

## 스켈레톤 규칙 (RED ④)

| 규칙 | 내용 |
|------|------|
| **AAA 주석** | `# Given` · `# When` · `# Then` (또는 Arrange/Act/Assert) — 플랜 GWT와 1:1 |
| **Then** | `pytest.fail("RED: {Test ID} — {Then 기대 한 줄}")` **한 줄만** |
| **Assert** | `assert` 본문 **금지** (스켈레톤 단계) |
| **통과 더미** | `pass`·빈 함수·항상 성공 코드 **금지** |
| **skip / xfail** | `@pytest.mark.skip` · `pytest.skip()` · `xfail` **금지** |
| **`src/`** | 수정 **금지** |
| **상수** | `34` · `16` · `4` 리터럴 금지 — **`entity.constants`** import (픽스처·Arrange 데이터만). `MAGIC_CONSTANT`·`LINE_IDS` 등 검증 SSOT는 `validate_lines` import (`.cursorrules`) |
| **Domain Mock** | `validate_lines` mock/stub **금지** (플랜 블록 4) |

### Then 한 줄 형식

```python
pytest.fail("RED: T3 — status=incomplete, failed_lines=[]")
```

- `{Test ID}` = 플랜 Track B 표 ID (`T3`, `T_d_loc_01` 등).
- 메시지에 Then 기대(`status`·`failed_lines` 등)를 **한 줄**로 포함.

---

## conftest (필수 픽스처)

`tests/conftest.py` — 플랜에 conftest가 있거나 빈칸(0) 격자가 필요하면 생성·갱신.

| 픽스처 | 설명 |
|--------|------|
| **`grid_g1`** | 4×4, **0 두 칸**, row-major 순서로 1~16 배치(빈칸 위치는 SSOT·Skill 또는 플랜). `@pytest.fixture` |

**row-major:** 인덱스 `(r,c)` → flat `r * GRID_SIZE + c`. 빈칸 좌표 assert용 시나리오(`test_d_loc_01_*`)에서 사용.

`entity.constants`에서 `GRID_SIZE`, `CELL_MAX`, `MAGIC_CONSTANT`(또는 동등 이름) import 후 픽스처 구성.

```python
# tests/conftest.py (예시 골격)
import pytest

from entity.constants import GRID_SIZE


@pytest.fixture
def grid_g1():
    """4×4, 0 두 칸, row-major 1~16 (위치는 플랜·Skill SSOT)."""
    return [
        [1, 2, 3, 4],
        [5, 0, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 0, 16],
    ]
```

> `entity/constants.py`가 없으면 **tests/ 스켈레톤 작성 시** `src/entity/constants.py` 최소 골격만 추가할지, Skill·플랜 지시를 따른다. **`src/validate_lines.py`는 건드리지 않음.**

---

## 템플릿 예시 — `test_d_loc_01_blank_coords_row_major`

플랜 Test ID `T_d_loc_01` · 빈칸 좌표(row-major) 검증 스켈레톤:

```python
# tests/test_validate_lines.py
import pytest

from entity.constants import GRID_SIZE
from validate_lines import validate_lines


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given — grid_g1: 0 두 칸, row-major
    grid = grid_g1
    blanks = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]

    # When
    result = validate_lines(grid)

    # Then — 스켈레톤: assert 없음
    pytest.fail(f"RED: T_d_loc_01 — blanks={blanks}, status=incomplete, failed_lines=[]")
```

| 단계 | 내용 |
|------|------|
| Given | `grid_g1` + 빈칸 좌표 수집( Arrange 데이터만; 상수는 `entity.constants` ) |
| When | `result = validate_lines(grid)` |
| Then | `pytest.fail` 한 줄 (Test ID + 기대 요약) |

---

## incomplete 시나리오 예시 (T3)

```python
def test_incomplete_when_grid_has_zero(grid_g1):
    # Given
    grid = grid_g1

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail("RED: T3 — status=incomplete, failed_lines=[]")
```

---

## pytest 실행

플랜 블록 3 명령 우선:

```bash
pytest tests/test_validate_lines.py::{함수명} -v
```

묶음:

```bash
pytest tests/test_validate_lines.py -v
```

**기대:** `FAILED` — `pytest.fail: RED: {Test ID} — …` (구현 부재·assert 없음이 정상).

---

## 금지

| 금지 | 이유 |
|------|------|
| **`src/validate_lines.py` 등 구현 수정** | GREEN까지 금지 |
| **`assert` 본문** | RED ④는 스켈레톤만; assert는 `/tdd-red` |
| **`pass`·빈 테스트·항상 성공** | RED 우회 |
| **skip · xfail** | 실패 회피 |
| **리터럴 `34`·`16`·`4` (픽스처)** | `entity.constants` import |
| **Domain Mock** | ECB 플랜 위반 |
| **플랜에 없는 Test ID·파일 추측** | SSOT 위반 |

---

## 보고 형식

```
Phase: red | Layer: entity | Track: Logic

## Test ID
- T3 (또는 플랜 ID)

## FAIL
- pytest.fail: RED: T3 — status=incomplete, failed_lines=[]

## 변경 파일
- tests/conftest.py
- tests/test_validate_lines.py

## pytest
- 명령: pytest tests/test_validate_lines.py::test_incomplete_when_grid_has_zero -v
- 결과: 1 failed

## 다음
- /tdd-red: pytest.fail → assert 치환
```

---

## RED 파이프라인 위치

| 단계 | Command | 산출 |
|------|---------|------|
| ③ | `/red-test-plan` | C2C·테스트 플랜 (파일 없음) |
| **④** | **`/red-skeleton`** | **`pytest.fail` 스켈레톤 (`tests/`만)** |
| ⑤ | `/tdd-red` | `assert` 본문 · RED FAIL(미구현) 확인 |

---

## 참조

| 문서 | 경로 |
|------|------|
| 설계 (앞단) | `.cursor/commands/red-test-plan.md` |
| Assert RED | `.cursor/commands/tdd-red.md` |
| Skill | `magic-square-tdd` — **있으면 자동 따름** |
| 규칙 | `.cursorrules` |
| 상수 (픽스처) | `entity/constants.py` — `GRID_SIZE`, `CELL_MAX`, `MAGIC_CONSTANT` |
| API SSOT | `src/validate_lines.py` — `LINE_IDS`, `LINE_CELLS` |
