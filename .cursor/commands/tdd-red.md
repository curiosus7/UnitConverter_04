# Command: TDD RED — validate_lines

`validate_lines` RED 단계 전용. **tests/ 만** 수정한다.

---

## Phase 선언

응답 **첫 줄**에 반드시:

```
Phase: RED
```

---

## 절차 (AAA)

한 테스트 = 한 행위. **Arrange → Act → Assert** 순서.

| 단계 | 내용 |
|------|------|
| **Arrange** | 4×4 `grid` fixture 준비. `MAGIC_CONSTANT`·`LINE_IDS`는 import (리터럴 34·줄 ID 금지). |
| **Act** | `result = validate_lines(grid)` |
| **Assert** | `result["status"]`, `result["failed_lines"]`를 API 계약대로 검증. |

RED 완료 조건:

1. `tests/test_validate_lines.py`에 테스트 **1개** 추가 (또는 사용자 지정 1 시나리오).
2. 루트에서 `pytest` 실행 → **FAIL** 확인 (AssertionError 등. 미구현 `...` 상태가 정상).
3. **src/ 미수정** 확인.

---

## pytest 예시

```python
# tests/test_validate_lines.py
from validate_lines import MAGIC_CONSTANT, validate_lines


def test_incomplete_when_grid_has_zero():
    # Arrange — 0(빈칸) 1개 포함
    grid = [
        [0, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]

    # Act
    result = validate_lines(grid)

    # Assert — 선행: incomplete, failed_lines=[]
    assert result["status"] == "incomplete"
    assert result["failed_lines"] == []
```

```python
def test_fail_lists_wrong_lines_in_line_ids_order():
    # Arrange — 16칸 완성, R1 합 ≠ MAGIC_CONSTANT
    grid = [
        [1, 1, 1, 1],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]

    result = validate_lines(grid)

    assert result["status"] == "fail"
    assert result["failed_lines"] == ["R1"]
```

실행:

```bash
pytest tests/test_validate_lines.py -v
```

기대: **FAILED** (구현 전).

---

## 금지 (RED)

| 금지 | 이유 |
|------|------|
| **`src/` 수정** | GREEN까지 구현 금지 |
| **assert 완화·기대값 변경·assert/조건 삭제** | Red를 Green으로 속임 |
| **`@pytest.mark.skip` · `pytest.skip()` · `xfail`** | 실패 회피 |
| **리터럴 `34`·줄 ID 문자열 하드코딩** | SSOT 위반 (`MAGIC_CONSTANT`, `LINE_IDS` import) |
| **skip/xfail로 FAIL 우회** | Test Loop 위반 |

---

## 보고 형식

RED 완료 시 아래 형식으로 보고:

```
Phase: RED

## 시나리오
- (한 줄: 무엇을 검증하는 테스트인지)

## 변경 파일
- tests/test_validate_lines.py

## pytest 결과
- 명령: pytest tests/test_validate_lines.py -v
- 결과: FAILED (N failed) — (실패 assert 한 줄 요약)

## 다음
- GREEN: src/validate_lines.py 최소 구현
```

---

## 참조

- API·도메인: 루트 `.cursorrules`
- SSOT: `src/validate_lines.py` — `MAGIC_CONSTANT`, `LINE_IDS`, `LINE_CELLS`
