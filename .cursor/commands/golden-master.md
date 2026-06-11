# Command: Golden Master — Approval Test 구축·검증

**GREEN PASS** 직후, 대상 Test ID의 **Golden Master(Approval Test)** 를 구축하고 `matched`를 검증한다.

구현 변경 시 golden diff로 **회귀**를 잡는다. golden 파일 **수동 편집으로 통과 우회 금지**.

**Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름**.

---

## 실행 트리거

```
/golden-master
```

추가 입력 없이 동작. **선행:** 대상 Test ID **pytest PASS** (`/green-minimal` 완료).

---

## 자동 추출

| 항목 | 출처 |
|------|------|
| **Test ID** | 채팅 지정 · `/green-minimal` 보고 · 테스트 파일명(`test_d_loc_01` → `D-LOC-01`) |
| **pytest 대상** | `tests/entity/test_{slug}.py` 또는 플랜 블록 3 |
| **golden ID** | Test ID를 파일명으로 (`D-LOC-01` → `tests/golden/D-LOC-01.approved.txt`) |
| **Layer / Track** | 기본 `entity` · `Logic` |

Test ID가 없으면 PASS된 테스트 함수 1건에서 추출 후 보고에 명시.

---

## Phase 선언

응답 **첫 줄**:

```
Phase: green | Layer: entity | Track: Logic
```

---

## 전제

| 전제 | 확인 |
|------|------|
| **대상 Test ID pytest PASS** | `pytest {대상} -v` → **PASSED**. FAIL이면 golden 구축 **중단**·원인 보고. |
| **GREEN 완료** | `src/` 최소 구현 반영됨 |
| **`src/` 추가 변경 없음** | golden 기준은 **현재 PASS 출력** 스냅샷 |

---

## 절차

| # | 단계 | 내용 |
|---|------|------|
| 1 | **`tests/_approval.py`** | `assert_matches_golden` 없으면 **생성**. 있으면 재사용. |
| 2 | **golden 연결** | 테스트 Then에 `assert_matches_golden(actual_text, golden_id)` 연결. 경로: `tests/golden/{id}.approved.txt` |
| 3 | **기준 생성** | `UPDATE_GOLDEN=1 pytest {대상} -v` — golden 파일 **자동 생성·갱신** |
| 4 | **matched 확인** | `UPDATE_GOLDEN` **없이** 동일 pytest → **PASSED** (`matched`). 불일치 시 diff 보고·**수동 golden 편집 금지** → 구현 또는 직렬화 수정 |

---

## `tests/_approval.py` (공통 헬퍼)

없으면 아래 계약으로 생성:

```python
# tests/_approval.py
from __future__ import annotations

import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def golden_path(golden_id: str) -> Path:
    return GOLDEN_DIR / f"{golden_id}.approved.txt"


def assert_matches_golden(actual: str, golden_id: str) -> None:
    """actual 문자열을 golden 파일과 비교. UPDATE_GOLDEN=1 이면 기준 갱신."""
    path = golden_path(golden_id)
    normalized = actual.rstrip() + "\n"

    if os.environ.get("UPDATE_GOLDEN") == "1":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(normalized, encoding="utf-8")
        return

    if not path.is_file():
        raise AssertionError(f"golden missing: {path} (run UPDATE_GOLDEN=1 pytest …)")

    expected = path.read_text(encoding="utf-8")
    if normalized != expected:
        raise AssertionError(
            f"golden mismatch: {path}\n--- expected ---\n{expected}--- actual ---\n{normalized}"
        )
```

---

## Golden 출력 포맷 (고정)

Approval 직렬화는 **한 줄·고정 포맷**. 테스트마다 `format_*_golden()` 헬퍼로 생성.

### int[6] · 1-index (좌표·상태 묶음)

| 필드 | 인덱스 | 의미 | 규칙 |
|------|--------|------|------|
| `i0` `i1` | 0–1 | 1번째 빈칸 `(row, col)` | **1-index** (1~4) |
| `i2` `i3` | 2–3 | 2번째 빈칸 `(row, col)` | **1-index**; 빈칸 1개면 `0 0` |
| `i4` | 4 | 상태 코드 | Entity: `0`=ok / Boundary: 아래 에러 코드 매핑 |
| `i5` | 5 | 예약 | 항상 `0` (미사용) |

**한 줄 예 (공백 구분, 6정수):**

```
2 2 4 3 0 0
```

- 0-based `(1,1)` → 1-index `2 2`; 0-based `(3,2)` → `4 3`.
- Entity Logic Track 성공: `i4=0`.

### 에러 코드 문자열 (Boundary · `i4` 대체 라인)

Boundary Approval 또는 에러 golden은 **별도 줄**에 고정 문자열만:

| 코드 | 문자열 (고정) |
|------|----------------|
| E001 | `E001` |
| E002 | `E002` |
| E003 | `E003` |
| E004 | `E004` |
| E005 | `E005` |

Entity golden(`int[6]`)과 **혼용 금지** — Test ID당 포맷 1종.

---

## 테스트 연결 예 — D-LOC-01

```python
# tests/entity/test_d_loc_01.py
from entity.blank_loc import blank_coords_row_major
from tests._approval import assert_matches_golden

GOLDEN_ID = "D-LOC-01"


def _format_d_loc_01_golden(coords: list[tuple[int, int]]) -> str:
    """int[6] 1-index: 두 빈칸 좌표 + status 0 + reserved 0."""
    padded = coords + [(0, 0)] * (2 - len(coords))
    (r1, c1), (r2, c2) = padded[0], padded[1]
    return f"{r1 + 1} {c1 + 1} {r2 + 1} {c2 + 1} 0 0"


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given
    grid = grid_g1

    # When
    coords = blank_coords_row_major(grid)

    # Then — unit assert + golden
    assert coords == [(1, 1), (3, 2)]
    assert_matches_golden(_format_d_loc_01_golden(coords), GOLDEN_ID)
```

---

## pytest 명령

**3. 기준 생성 (최초 1회·의도적 갱신):**

```bash
UPDATE_GOLDEN=1 pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v
```

**4. matched 확인 (CI·일상):**

```bash
pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v
```

파일 전체:

```bash
pytest tests/entity/ -v
```

기대: `UPDATE_GOLDEN` 없이 **PASSED** — golden과 actual 일치.

---

## 금지

| 금지 | 이유 |
|------|------|
| **golden `.approved.txt` 수동 편집으로 통과** | Approval 우회 — 반드시 `UPDATE_GOLDEN=1`로 재생성 |
| **포맷 임의 변경** (`int[6]`·에러 문자열) | diff 비교 무의미 |
| **0-index golden 혼입** | 1-index SSOT 위반 |
| **PASS 전 golden 구축** | 기준 불안정 |
| **`src/` 변경과 golden 갱신 분리 누락** | 구현 바뀌면 `UPDATE_GOLDEN=1` 재실행 후 matched 재확인 |
| **skip · xfail** | 회귀 은폐 |

---

## 보고 형식

```
Phase: green | Layer: entity | Track: Logic

## Test ID
- D-LOC-01

## golden 경로
- tests/golden/D-LOC-01.approved.txt

## matched
- yes (UPDATE_GOLDEN 없이 PASSED)

## diff 요약
- 없음 (또는: mismatch — expected "2 2 4 3 0 0" vs actual "…" → 구현/직렬화 수정, golden 수동 편집 안 함)

## pytest
- UPDATE_GOLDEN=1: … → golden 생성
- matched: pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v → PASSED

## 변경 파일
- tests/_approval.py
- tests/golden/D-LOC-01.approved.txt
- tests/entity/test_d_loc_01.py (assert_matches_golden 연결)
```

mismatch 시 `AssertionError` 본문에서 **expected / actual** 블록을 diff 요약으로 인용한다.

---

## 파이프라인 위치

| 단계 | Command | 산출 |
|------|---------|------|
| GREEN | `/green-minimal` | PASS |
| **Golden** | **`/golden-master`** | **`*.approved.txt` · matched** |
| REFACTOR | *(별도)* | Green·golden 유지 |

---

## 참조

| SSOT | 경로 |
|------|------|
| GREEN | `.cursor/commands/green-minimal.md` |
| 에러 코드 | `.cursor/commands/red-test-plan.md` (E001~E005) |
| 상수 | `entity/constants.py` |
| Skill | `magic-square-tdd` — 있으면 자동 따름 |
