# Command: Refactor Safe — ARRR R단계 (Refine ⑧)

`/refactor-smell` 표에서 **선택한 스멜 1개만** Budget 내 **Safe Refactor** 실행.

**동작·golden·API 계약 불변** — 구조·이름·중복 제거만.

**Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름**.

---

## 실행 트리거

```
/refactor-safe
```

**필수 입력 (1개):** `/refactor-smell` 후보 번호 또는 `P등급 + 유형 + 위치`.

```
/refactor-safe 후보 1
```

또는:

```
/refactor-safe P1 Duplicated Code — blank_loc.py / solver.py 격자 순회
```

선택 스멜이 없으면 **실행 중단** · smell 표 재확인 요청.

---

## 자동 추출

| 항목 | 출처 |
|------|------|
| **대상 스멜** | 채팅 지정 · 직전 `/refactor-smell` 후보 1~3 |
| **위치·유형·P** | smell 표 해당 행 |
| **Budget** | smell 표 `Budget 적합=yes` 항목만 실행 |

`Budget 적합=no` 항목은 **분할** 후 재-smell 또는 여러 번 `/refactor-safe`로 나눔.

---

## Phase 선언

응답 **첫 줄**:

```
Phase: refactor | Layer: entity | Track: Logic
```

Boundary·UI 스멜: `Layer: boundary` 또는 `Track: UI` — smell 표와 동일.

---

## 전제

| 전제 | 확인 |
|------|------|
| **pytest 전부 PASS** | `python -m pytest tests/ -v` → PASSED (실행 전·후) |
| **smell 1건** | 한 번에 **스멜 1개**만 처리 |
| **GREEN·golden 기존** | Approval Test 연결 Test ID golden 존재 |

FAIL 시 **즉시 롤백** · 원인 보고.

---

## Safe Refactor 원칙 (불변)

| 항목 | 규칙 |
|------|------|
| **입출력** | 공개 함수 시그니처·반환 값·의미 **동일** |
| **예외** | 발생 조건·타입 **동일** (`ValueError` 등) |
| **int[6] 1-index** | golden 직렬화 포맷·순서 **변경 금지** |
| **E001~E005** | Entity에서 **emit·raise·return 금지** |
| **ECB** | Entity ↔ boundary/control import 관계 **악화 금지** |
| **기능** | **추가 금지** — 새 시나리오·Test ID 통과는 **별도 GREEN** |
| **버그 수정** | **금지** — 동작 변경은 GREEN 범위 |
| **assert·golden 의미** | 테스트 기대·Approval 내용 **동일** |

---

## Change Budget (1회 상한 · 준수 필수)

| 항목 | 상한 |
|------|------|
| **파일** | ≤ 3 |
| **클래스** | ≤ 1 |
| **메서드** | ≤ 3 (추출·이름 변경·이동 합산) |

초과 시 **이번 실행 중단** · smell 표에서 분할 후 재시도.

---

## 절차

| # | 단계 | 내용 |
|---|------|------|
| 1 | **선택 확인** | 스멜 1건 · Budget 적합 · pytest PASS |
| 2 | **최소 diff 리팩터** | 선택 스멜만 해소 (extract·rename·SSOT import·dedupe) |
| 3 | **pytest** | `python -m pytest tests/ -v` → **전부 PASSED** |
| 4 | **golden matched** | `UPDATE_GOLDEN` **없이** 동일 — Approval 연결 테스트 포함 |
| 5 | **golden diff 처리** | 아래 분기 |
| 6 | **보고** | 변경 요약 · pytest · golden matched |

**git commit** — 사용자 명시 요청 시만.

---

## golden diff 처리

리팩터 후 `assert_matches_golden` 실패 시:

| 구분 | 조치 |
|------|------|
| **비의도 diff** | **롤백** — 리팩터 변경 되돌림 · pytest·golden 재확인 |
| **의도적 diff** (포맷 함수 추출만, 출력 문자열 동일해야 함) | 원칙상 **발생하면 안 됨** — 직렬화 결과가 바뀌었다면 비의도로 간주·롤백 |
| **의도적 golden 갱신** (포맷 SSOT 문서화 등 **드묾**) | **ISS 문서** (`Report/` 또는 `docs/`)에 사유 기록 → `UPDATE_GOLDEN=1 pytest {대상}` → matched 재확인 |

**golden `.approved.txt` 수동 편집 금지.**

```bash
# matched 확인 (일상·완료 게이트)
python -m pytest tests/ -v

# 의도적 갱신 시만 (ISS 기록 후)
UPDATE_GOLDEN=1 pytest tests/entity/test_d_sol_01.py::test_d_sol_01_step_a_success -v
python -m pytest tests/ -v
```

---

## 스멜 유형별 Safe 조치 (허용 예)

| 유형 | Safe 조치 예 |
|------|----------------|
| **Duplicated Code** | 공통 헬퍼 추출 (`_iter_cells`, `_count_blanks`) — **메서드 ≤3** |
| **Long Method** | private 함수 분리 — 동작 동일 |
| **Mysterious Name** | 도메인 이름으로 rename — 호출부만 |
| **Magic Number** | `entity.constants` / `validate_lines` import 치환 |
| **Feature Envy** | 직렬화를 `tests/golden_format.py` 등으로 이동 — **출력 문자열 동일** |
| **ECB 위반** | 잘못된 import 제거·계층 분리 — **API 동일** |

---

## 금지

| 금지 | 이유 |
|------|------|
| **스멜 2개 이상 동시 처리** | 1회 = 1 smell |
| **Budget 초과** | Safe Refactor 범위 이탈 |
| **기능 추가·버그 수정** | GREEN 담당 |
| **입출력·예외·int[6] 변경** | 계약 파괴 |
| **E001~E005 emit** | ECB 위반 |
| **assert 완화 · skip · xfail** | Green 우회 |
| **golden 수동 편집** | Approval 우회 |
| **pytest FAIL 상태로 완료 보고** | Refactor 실패 |
| **git commit (명시 없을 때)** | `.cursorrules` |

---

## 보고 형식

```
Phase: refactor | Layer: entity | Track: Logic

## 선택 스멜
- [P1] Duplicated Code — blank_loc.py / solver.py 격자 순회

## 변경 요약
- (한 줄: extract `_iter_cells` → blank_loc 재사용, 동작 동일)

## Change Budget
- 파일 2 · 클래스 0 · 메서드 1

## pytest
- python -m pytest tests/ -v → N passed

## golden matched
- yes (UPDATE_GOLDEN 없음)
- (또는: ISS 기록 후 UPDATE_GOLDEN=1 → matched)

## 변경 파일
- src/entity/grid_iter.py
- src/entity/blank_loc.py
- src/entity/solver.py

## 다음
- `/refactor-smell` 재실행 또는 다음 RED 묶음
```

---

## ARRR 파이프라인 위치

| 단계 | Command | 산출 |
|------|---------|------|
| Refine ⑦ | `/refactor-smell` | 스멜 표 · 후보 (수정 없음) |
| **Refine ⑧** | **`/refactor-safe`** | **Budget 내 리팩터 · PASS · golden** |
| 이후 | `/refactor-smell` | 잔여 스멜 재탐지 |

---

## 참조

| SSOT | 경로 |
|------|------|
| 스멜 탐지 | `.cursor/commands/refactor-smell.md` |
| golden | `.cursor/commands/golden-master.md` |
| TDD · ECB | `.cursorrules` |
| Approval 헬퍼 | `tests/_approval.py` |
| Skill | `magic-square-tdd` — 있으면 자동 따름 |
