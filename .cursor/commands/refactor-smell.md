# Command: Refactor Smell — ARRR R단계 (Refine ⑦)

**코드 스멜 탐지만** 수행한다. **`src/`·`tests/` 수정 금지** · **git commit 금지**.

ARRR **R(Refine)** = ⑦ — `/refactor-safe`에 넘길 **후보 목록**만 산출.

**Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름**.

---

## 실행 트리거

```
/refactor-smell
```

추가 입력 없이 동작. **선행:** 전체 테스트 **PASS**.

---

## Phase 선언

응답 **첫 줄**:

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
```

---

## 전제 (중단 조건)

| 전제 | 확인 |
|------|------|
| **전체 pytest PASS** | `python -m pytest tests/ -v` → **전부 PASSED** |
| **중단** | 1건이라도 FAIL·ERROR·xfail·skip 우회 → 스멜 탐지 **중단** · 실패 목록 보고 · REFACTOR 금지 |

```bash
python -m pytest tests/ -v
```

---

## 절차

| # | 단계 | 내용 |
|---|------|------|
| 1 | **pytest 게이트** | 전제 명령 실행 — PASS 아니면 **즉시 중단** |
| 2 | **범위 스캔** | `src/` · `tests/` 읽기 전용 분석 (Logic + UI Track) |
| 3 | **스멜 표 작성** | 아래 7종 × P0/P1/P2 우선순위로 표 채움 |
| 4 | **Change Budget 점검** | 후보가 Budget 초과 시 P2로 강등 또는 분할 제안 |
| 5 | **후보 1~3개** | `/refactor-safe` 넘김용으로 선정 |
| 6 | **다음 안내** | P0 1개만 골라 `/refactor-safe` 실행 안내 |

**코드 수정 · commit · golden 수동 편집 — 금지.**

---

## 스멜 유형 (7종)

| 유형 | 탐지 기준 (MagicSquare_00) |
|------|---------------------------|
| **Long Method** | 함수·메서드 **>25줄** 또는 AAA·분기·직렬화가 한 블록에 혼재 |
| **Duplicated Code** | 동일·유사 로직 2곳 이상 (격자 순회, 빈칸 수집, int[6] 직렬화 등) |
| **Mysterious Name** | `i0`·`tmp`·`data`·`fn` 등 의도 불명; Test ID·도메인 용어 미사용 |
| **Magic Number** | 리터럴 `34`·`16`·`4`·`0` — `entity.constants`·`validate_lines` SSOT 미사용 |
| **ECB 위반** | Entity가 boundary/control import; Domain Mock; E001~E005 Entity emit |
| **Feature Envy** | 한 모듈이 타 계층 데이터·상수를 과다 참조 (예: test가 직렬화·도메인 혼재) |
| **기타** | dead code · 미사용 import · golden 포맷 불일치 · assert·golden 이중 검증 과다 |

---

## 우선순위 (P0 / P1 / P2)

| 등급 | 의미 | 예 |
|------|------|-----|
| **P0** | Green·golden 깨뜨릴 위험 · SSOT·ECB 위반 · 회귀 유발 가능 | Magic Number in `src/`, ECB import |
| **P1** | 가독성·중복 · Budget 내 안전 리팩터 가능 | Duplicated blank-scan |
| **P2** | 미미 · 후속 또는 Budget 초과 | Naming nit · 주석 정리 |

---

## Change Budget (`/refactor-safe` 1회 상한)

| 항목 | 상한 |
|------|------|
| **파일** | ≤ 3 |
| **클래스** | ≤ 1 |
| **메서드** | ≤ 3 |

`/refactor-smell`은 Budget을 **초과하는 작업을 후보에서 제외**하거나 **여러 safe 실행으로 분할** 제안한다.

---

## 스멜 표 (필수 출력)

| P | 유형 | 위치 (파일:줄·심볼) | 요약 | Budget 적합 |
|---|------|---------------------|------|-------------|
| P0 | Magic Number | `…` | … | yes/no |
| P1 | Duplicated Code | `…` | … | yes/no |
| … | … | … | … | … |

- **위치:** 실제 코드 근거 (추측 금지).
- **Budget 적합:** 1회 `/refactor-safe`로 처리 가능 여부.

---

## `/refactor-safe` 후보 (1~3개)

표에서 Budget 적합·효과 큰 항목만:

```
1. [P0] {유형} — {파일} — {한 줄 조치 방향}
2. [P1] …
3. [P1] …
```

후보 없으면: `스멜 없음 — REFACTOR 생략 가능` 명시.

---

## 다음 안내 (필수)

응답 **마지막**에 반드시:

```
P0 후보 중 1개를 골라 /refactor-safe 를 실행하세요. (이 Command는 수정하지 않습니다.)
```

P0가 없으면:

```
P1 후보 중 1개를 골라 /refactor-safe 를 실행하세요. 전체 pytest PASS 유지 전제.
```

---

## 금지

| 금지 | 이유 |
|------|------|
| **`src/`·`tests/` 수정** | Refine ⑦ = 탐지만 |
| **git commit / push** | 사용자 명시 요청 전까지 금지 |
| **pytest FAIL 상태에서 스멜 보고** | Green 미확보 |
| **Budget 초과 후보를 safe 1회로 묶기** | 안전 REFACTOR 위반 |
| **스멜 없이 코드 제안·패치** | smell ≠ implement |

---

## 보고 형식

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI

## pytest 게이트
- python -m pytest tests/ -v → N passed

## 스멜 표
(표)

## /refactor-safe 후보
1. …
2. …

## Change Budget
- 후보 1: 파일 n · 클래스 n · 메서드 n

P0 후보 중 1개를 골라 /refactor-safe 를 실행하세요. (이 Command는 수정하지 않습니다.)
```

---

## ARRR 파이프라인 위치

| 단계 | Command | 산출 |
|------|---------|------|
| GREEN | `/green-minimal` | PASS |
| Golden | `/golden-master` | matched |
| **Refine ⑦** | **`/refactor-smell`** | **스멜 표 · safe 후보 (수정 없음)** |
| Refine ⑧ | `/refactor-safe` | Budget 내 리팩터 · PASS 유지 |

---

## 참조

| SSOT | 경로 |
|------|------|
| TDD · ECB | `.cursorrules` |
| 에러 코드 | `.cursor/commands/red-test-plan.md` |
| GREEN | `.cursor/commands/green-minimal.md` |
| Golden | `.cursor/commands/golden-master.md` |
| Skill | `magic-square-tdd` — 있으면 자동 따름 |
