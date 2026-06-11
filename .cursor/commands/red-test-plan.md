# Command: RED Test Plan — ARRR A단계 (Ask = RED ③)

> **UnitConverter_04:** Magic Square 템플릿 — **`/uc-red-plan` 사용** (`.cursor/commands/README.md`).

**C2C 설계표·테스트 플랜만** 작성한다. `tests/`·`src/` **파일 생성·수정 금지**.

ARRR **A(Ask)** = RED ③ — 다음 `/red-skeleton`(또는 `/tdd-red`)에 넘길 **설계 산출물**만 만든다.

---

## 실행 트리거

사용자가 아래만 입력해도 이 Command를 따른다 (**추가 입력 불필요**):

```
/red-test-plan
```

---

## 자동 추출 (입력 없이)

| 항목 | 추출 순서 |
|------|-----------|
| **세션 주제** | ① `docs/PRD.md` 주제·Goal 1문장 → ② `Report/*.REPORT.md` 최신 세션 요약 → ③ 채팅 맥락(현재 TDD 대상·시나리오) |
| **Test ID** | ① PRD FR·시나리오 번호(T1, T3 등) → ② 채팅에 이미 언급된 `test_*` → ③ 없으면 `T{n}` 자동 부여(기존 테스트·플랜과 중복 금지) |
| **대상 API** | `.cursorrules` API 계약 + `src/` 시그니처 (추측 금지) |
| **Layer / Track** | 기본: `Layer: entity` · `Track: Logic`. UI·표시 검증이 주제면 `Track: UI`. Boundary 계층이면 `Layer: boundary` (아래 Track A 참고) |

`docs/PRD.md`가 없으면 **`.cursorrules` + 최신 `Report/*.REPORT.md`** 를 PRD 대용 SSOT로 사용한다.

---

## Phase 선언

응답 **첫 줄**에 반드시 (대소문자·구분자 그대로):

```
Phase: red | Layer: entity | Track: Logic
```

- **Logic Track (기본):** `Layer: entity` — `validate_lines` 등 도메인·Command 검증.
- **UI Track:** `Layer: entity | Track: UI` — 표시·포맷 검증(후속).
- **Track A (Boundary):** `Layer: boundary` — ECB Boundary 계층. **본문 절차·4블록 형식은 동일**하고 `Layer`만 `boundary`로 바꾸면 재사용 가능.

---

## 절차

1. SSOT 읽기: `.cursorrules`, `docs/PRD.md`(있을 때), 채팅·Report에서 세션 주제·FR·기존 Test ID 확인.
2. 이번 RED 묶음 **시나리오 1개** 확정 (한 Command 실행 = 한 시나리오 플랜).
3. 아래 **출력 4블록**을 표 형식으로 작성 (**파일 쓰기 없음**).
4. ECB·Mock 점검 블록에서 Logic Track 위반 여부 확인.
5. 마지막 줄에 완료 문구 1줄.

---

## 출력 4블록 (필수 · 표 형식)

### 블록 1 — C2C (Rule1~3)

PRD Functional Requirement 1건당 아래 3행. **Rule1 → Rule2 → Rule3** 순.

| Rule | 열 | 내용 |
|------|-----|------|
| **Rule1** | PRD FR 인용 | `docs/PRD.md`의 FR 문장 그대로 인용 (없으면 `.cursorrules`·Report R-G-I-O 해당 조항 인용) |
| **Rule2** | To-Do 1개 | 이번 RED에서 검증할 행위 **한 가지** (구현·GREEN 내용 금지) |
| **Rule3** | Test ID · Given / When / Then | Test ID + GWT 3줄 (Given=격자·전제, When=호출, Then=기대 status·failed_lines) |

**예시 (Logic · incomplete 시나리오):**

| Rule | 내용 |
|------|------|
| Rule1 | FR-R5: 격자에 `0`이 하나라도 있으면 `status=incomplete`, 합 계산·34 비교 수행하지 않음, `failed_lines=[]` |
| Rule2 | 0 포함 4×4 격자 1건에 대해 `validate_lines` 호출 시 incomplete 반환을 RED로 고정 |
| Rule3 | **T3** — Given: 0이 1칸 이상인 4×4 grid / When: `validate_lines(grid)` / Then: `status=="incomplete"`, `failed_lines==[]` |

---

### 블록 2 — Track B 표 (Logic Track 기본)

`Track: Logic`일 때 **Track B** 표를 채운다. (`Track: UI`면 동일 열에 UI 대상 함수·표시 기대치로 치환.)

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---------|-----------|--------------|-----------|----------------------|
| T3 | `validate_lines` | 0 포함 grid → `incomplete`, `failed_lines=[]` | `MAGIC_CONSTANT`·`LINE_IDS` import; 리터럴 34·줄 ID 하드코딩 금지 | `TypeError` / `AssertionError` (stub `...` 또는 미구현) |

- **Invariant:** SSOT·API 계약·10선 전부·`LINE_IDS` 순서 등 **테스트가 지켜야 할 불변식**.
- **Expected RED Failure:** GREEN 전 정상 실패 유형 (미구현·assert 불일치). skip/xfail로 우회 금지.

---

### 블록 3 — 테스트 플랜 (설계만 · 파일 미생성)

| 항목 | 값 |
|------|-----|
| **파일 경로** | `tests/test_validate_lines.py` (또는 PRD·세션에 명시된 경로) |
| **함수명** | `test_{시나리오_슬러그}` (예: `test_incomplete_when_grid_has_zero`) |
| **conftest 픽스처** | 없으면 `—`. 필요 시: `grid_4x4_incomplete`(0 1칸), `grid_4x4_pass`, `grid_4x4_fail_r1` 등 **이름만** 기재 |
| **pytest 명령** | `pytest tests/test_validate_lines.py::{함수명} -v` 또는 묶음: `pytest tests/test_validate_lines.py -v` |
| **RED 묶음 범위** | 이번 플랜에 포함되는 Test ID 목록 (예: `T3` 단독 / `T3,T4` 묶음) |

AAA 순서 메모 (플랜에만 기재):

| 단계 | 내용 |
|------|------|
| Arrange | 4×4 `grid`; `MAGIC_CONSTANT`, `LINE_IDS`는 `validate_lines`에서 import |
| Act | `result = validate_lines(grid)` |
| Assert | `result["status"]`, `result["failed_lines"]` — API 계약대로 |

---

### 블록 4 — ECB · Mock 점검

Logic Track(`Layer: entity`) 전용 점검표. **위반 시 플랜 수정 후 완료 문구 금지.**

| 점검 | Logic Track (entity) | Boundary Track (Layer: boundary) |
|------|----------------------|----------------------------------|
| **Domain Mock** | **금지** — `validate_lines`·도메인 로직을 mock/stub으로 대체하지 않음 | Boundary 입출력만 격리; Domain은 실제 또는 테스트 더블 최소 |
| **E001~E005 emit** | **금지** — Entity 테스트에서 Boundary 오류 코드(E001~E005) 발생·assert 하지 않음 | Boundary 전용 시나리오에서만 해당 코드 검증 |
| **ECB 분류** | 대상 = **Entity/Command** (`validate_lines`) | 대상 = **Boundary** (표시·입력 변환 등) |
| **SSOT** | 리터럴 `34`·줄 ID 문자열 하드코딩 금지 → `MAGIC_CONSTANT`, `LINE_IDS` import | 표시 문자열은 Boundary 책임; Entity 결과 dict만 입력 |

**E001~E005 (Boundary 예약 · Logic Track에서 다루지 않음):**

| 코드 | 의미 (Boundary) |
|------|-----------------|
| E001 | 잘못된 격자 크기 (4×4 아님) |
| E002 | 셀 값 범위 오류 (0~16 밖) |
| E003 | 1~16 중복 |
| E004 | 입력 형식 오류 |
| E005 | Boundary 내부 처리 실패 |

> Logic Track RED는 **E001~E005를 emit·기대하지 않는다**. `ValueError`(4×4 아님) 등 Entity 예외는 API·PRD에 명시된 경우만 별도 Test ID로 플랜.

---

## 금지

| 금지 | 이유 |
|------|------|
| **`tests/`·`src/` 파일 생성·수정** | RED ③은 설계만; 구현은 `/red-skeleton`·`/tdd-red` |
| **`src/` 수정** | GREEN까지 구현 금지 |
| **GREEN / REFACTOR 진행** | Test Loop 순서 위반 |
| **`@pytest.mark.skip` · `pytest.skip()` · `xfail`** | 실패 회피 |
| **assert 완화·기대값 변경으로 Red 우회** | Test Loop 위반 |
| **채팅·PRD에 없는 FR·파일 경로 추측** | SSOT 위반 |

---

## 완료 한 줄

4블록·ECB 점검을 모두 채운 뒤 응답 **마지막 줄**에 반드시:

```
/red-skeleton 으로 넘길 준비됐다
```

---

## Track A (Boundary) 재사용

**Track A = `Layer: boundary`.** 절차·4블록·금지·완료 문구는 동일하다.

| 변경점 | 내용 |
|--------|------|
| Phase 선언 | `Phase: red \| Layer: boundary \| Track: Logic` (또는 `Track: UI`) |
| 블록 1 Rule1 | Boundary FR 인용 (표시·에러 메시지·입력 검증) |
| 블록 2 | 대상 = Boundary 함수/컴포넌트; E001~E005는 **Boundary 플랜에서만** 사용 |
| 블록 4 | Domain Mock 금지 → Boundary는 Domain **실제 호출** 전제로 플랜 |

Entity(Logic) 플랜을 복사해 **`Layer: entity` → `Layer: boundary`** 만 바꿔도 Track A 플랜으로 재사용 가능하다고 명시한다.

---

## 보고 형식 (요약)

```
Phase: red | Layer: entity | Track: Logic

## 세션 주제
- (자동 추출 1문장)

## 블록 1 — C2C
(표)

## 블록 2 — Track B
(표)

## 블록 3 — 테스트 플랜
(표)

## 블록 4 — ECB · Mock 점검
(표)

/red-skeleton 으로 넘길 준비됐다
```

---

## 참조

| SSOT | 경로 |
|------|------|
| 도메인 · API · TDD | `.cursorrules` |
| Functional Requirements | `docs/PRD.md` (없으면 `Report/03.REPORT.md` R-G-I-O·성공 기준) |
| RED 구현(다음 단계) | `.cursor/commands/tdd-red.md` |
| 상수 · 시그니처 | `src/validate_lines.py` — `MAGIC_CONSTANT`, `LINE_IDS`, `LINE_CELLS` |
