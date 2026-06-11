# PRD — Unit Converter (길이 단위 변환 CLI)

| 항목 | 내용 |
|------|------|
| 문서 ID | PRD-UC-001 |
| 버전 | 0.2 (spec) |
| 작성일 | 2026-06-11 |
| 작성 | A팀 · 박교현 (Mom Test 기반) |
| SSOT | 본 문서 (`docs/PRD.md`) — 요구사항의 단일 출처 |
| 추적 원칙 | C2C: PRD → To-Do → Test Case → Code |

---

## §1. 배경 (Background)

### 1.1 Mom Test에서 도출한 문제

개발·검토 업무에서 **서로 다른 출처의 길이 단위와 비율을 사람이 매번 수동으로 맞추느라** 시간 낭비와 입력 오류가 반복된다.

### 1.2 사실 근거 (Mom Test, 2026-06-11)

1. **해외 PDF → 내부 BOM 환산**  
   3월 초, feet/inch로 된 설비 스펙 PDF 12칸을 mm 기준 BOM에 옮기는 데 **35~40분** 소요. PDF 뷰어 → 구글 검색 → 계산기 → 엑셀 순으로 반복.

2. **단위 착오로 인한 재작업**  
   inch를 cm로 잘못 검색해 **2건** 오입력 → 동료 슬랙 지적 → BOM 행 재입력·출력물 재인쇄 → 회의 전 **10분** 지연.

3. **반복 패턴**  
   분기 **2~3회** 유사 작업 발생. 레거시 코드·문서에 ft/yd/m 혼재, 환산 상수(`3.28084` 등)가 **파일마다 다르게** 존재하는 경우 확인.

### 1.3 프로젝트 한 문장 (주제)

> 서로 다른 출처의 길이 단위와 비율을 사람이 매번 수동으로 맞추느라 생기는 시간 낭비와 입력 오류 문제를, **동일한 기준으로 반복 확인·대조**할 수 있게 한다.

### 1.4 프로젝트 목표 (C2C)

길이 단위 변환 CLI를 **PRD와 테스트로부터 추적 가능하게** 재구현한다.  
모든 기능·비기능 요구는 테스트 ID와 1:1 매핑하며, RED → GREEN → REFACTOR(ARRR) 사이클로 검증한다.

---

## §2. 목표 및 성공 기준 (Goals)

### 2.1 R-G-I-O

| 요소 | 내용 |
|------|------|
| **Role** | 길이·단위가 섞인 자료를 동일 기준으로 대조·검증하는 개발자 |
| **Goal** | 출처가 달라도 한 기준 단위(meter)로 일관 환산·확인하고, 잘못된 입력·단위 혼동을 줄인다 |
| **Input** | `단위:값` 형식 문자열 (예: `meter:2.5`, `feet:10`) |
| **Output** | 지원 단위 전체로의 환산 결과 (기본: 줄 단위 텍스트; 확장: JSON/CSV/표) |
| **성공 기준** | FR/NFR 전항목에 테스트 통과; PRD → TC → 코드 역추적 가능 |

### 2.2 Input 예시 (3개 이상)

| # | 입력 | 기대 |
|---|------|------|
| I-01 | `meter:2.5` | 정상 파싱·전 단위 출력 |
| I-02 | `feet:10` | meter 경유 정확 환산 |
| I-03 | `meter:-1` | 음수 거부 |
| I-04 | `meter` (콜론 없음) | 형식 오류 |
| I-05 | `cubit:1` (미등록) | 명확한 오류 |

### 2.3 우선순위

| 우선순위 | 범위 | 설명 |
|----------|------|------|
| **P0** | FR-01 ~ FR-05, NFR-01 ~ NFR-05 | 필수 완료 (기본 + 품질 + C2C·테스트) |
| **P1** | EXT-01 ~ EXT-03 | 추가 요구 (설정 외부화, 동적 등록, 출력 포맷) |

---

## §3. 사용자 및 사용 시나리오 (Users & Scenarios)

### 3.1 사용자

| 페르소나 | 설명 |
|----------|------|
| 개발자 | 레거시 코드·README의 단위·비율을 검증하고 샘플 값을 대조 |
| 설계/검토 담당 | 해외 자료(ft/inch)를 내부 기준(m)으로 빠르게 환산·확인 |
| 교육 실습자 | C2C·TDD·ARRR 워크플로우로 CLI를 재구현 |

### 3.2 핵심 시나리오

**S-01 정상 변환**  
사용자가 `meter:2.5`를 입력하면 meter, feet, yard 등 지원 단위로 환산된 결과를 출력한다.

**S-02 오류 입력 처리**  
음수, 형식 오류, 미지 단위 입력 시 프로그램이 중단되지 않고 명확한 오류를 반환한다.

**S-03 단위 확장 (P1)**  
`1 cubit = 0.4572 meter`를 등록한 뒤 즉시 cubit 기준 변환에 사용한다.

**S-04 설정 기반 운영 (P1)**  
`units.json`(또는 YAML)에서 비율을 로드하고, 코드 수정 없이 단위를 추가한다.

---

## §4. 입력·출력 규격 (I/O Specification)

### 4.1 입력 형식

```
<unit>:<value>
```

- `unit`: 지원·등록된 단위 이름 (문자열, 공백 없음)
- `value`: **0 이상**의 실수 (`0` 허용, 음수 불가)
- 구분자: 콜론(`:`) 1개 — `split(':', 1)` 기준 파싱
- **추가 콜론:** `meter:2.5:extra` → `value_str="2.5:extra"` → `float` 실패 → **E-NUM** (`Invalid number`)
- **비숫자 값:** `meter:abc` → E-NUM · 전체 `abc` → **E-FMT**

### 4.2 기본 지원 단위 및 비율 (meter = 1.0 기준)

| 단위 | meter 대비 비율 |
|------|-----------------|
| meter | 1.0 |
| feet | 3.28084 |
| yard | 1.09361 |

- feet ↔ yard 환산은 **meter를 경유**하여 계산한다.

### 4.3 출력 형식

**`--format table` (lecture 부록)** — box-drawing 표, `input` 열은 입력값, `result`는 4자리 환산

```
┌────────┬─────────┬─────────┐
│ unit   │   input │  result │
├────────┼─────────┼─────────┤
│ meter  │     2.5 │     2.5 │
│ feet   │     2.5 │  8.2021 │
│ yard   │     2.5 │  2.7340 │
└────────┴─────────┴─────────┘
```

**line (내부·D-STR)** — `format_conversion_output` 줄 형식 (Golden Master 이전 P0)

**오류 메시지 (SSOT)** — `docs/traceability.md` 참조

| 코드 | 메시지 |
|------|--------|
| E-FMT | `Invalid format. Use unit:value (ex: meter:2.5)` |
| E-NUM | `Invalid number: {value_str}` |
| E-NEG | `Negative value not allowed` |
| E-UNIT | `Unknown unit: {unit}` |

**확장 (P1, `--format`)**

| 포맷 | 설명 |
|------|------|
| `table` | box-drawing 표 (`unit` / `input` / `result` 열) |
| `json` | 구조화 JSON |
| `csv` | CSV |

### 4.4 실행 예시

```bash
python -m unit_converter "meter:2.5"
python -m unit_converter "meter:2.5" --format json
```

---

## §5. 기능 요구사항 (Functional Requirements)

| ID | 요구사항 | Given | Then | P |
|----|----------|-------|------|---|
| **FR-01** | `단위:값` 파싱 | 유효 문자열 `meter:2.5` | `unit=meter`, `value=2.5` | P0 |
| **FR-02** | 전 단위 출력 | `meter` + `2.5` | feet≈8.2021, yard≈2.7340 등 전 단위 결과 | P0 |
| **FR-03** | 미지 단위 처리 | `cubit:1` (미등록) | 명확한 오류 메시지 또는 예외 | P0 |
| **FR-04** | 음수 거부 | `meter:-1` | 거부 / 예외 | P0 |
| **FR-05** | 잘못된 형식 거부 | `meter`, `abc` | 형식 오류 | P0 |
| **EXT-01** | 설정 파일 로드 | `units.json` 존재 | 파일의 비율로 단위 등록 | P1 |
| **EXT-02** | 동적 단위 등록 | `1 cubit = 0.4572 meter` 등록 | 등록 직후 cubit 변환 가능 | P1 |
| **EXT-03** | 출력 포맷 선택 | `--format json \| csv \| table` | 포맷별 출력 검증 | P1 |

---

## §6. 비기능 요구사항 (Non-Functional Requirements)

| ID | 요구사항 | 설명 | P |
|----|----------|------|---|
| **NFR-01** | OCP (개방-폐쇄) | 새 단위(예: inch) 추가 시 **기존 변환기 핵심 코드 수정 없이** 등록·확장 | P0 |
| **NFR-02** | SRP (단일 책임) | Parser · Registry · Converter · Formatter(Printer) **모듈 분리** | P0 |
| **NFR-03** | 정확성·일관성 | 동일 입력 → 동일 출력; meter 기준 비율 일관 | P0 |
| **NFR-04** | 추적성 (C2C) | 모든 FR/NFR에 테스트 ID 1:1 매핑 | P0 |
| **NFR-05** | 테스트 가능성 | Domain(Track B) + Boundary(Track A) Dual-Track TDD | P0 |

### 6.1 목표 아키텍처 (Python)

```
unit_converter/
├─ domain/
│   ├─ length_unit.py      # Protocol: name, to_meter()
│   ├─ unit_registry.py    # 등록·조회 (OCP)
│   └─ converter.py        # meter 기준 전 단위 변환
├─ infrastructure/
│   └─ config_loader.py    # JSON / YAML
├─ app/
│   ├─ input_parser.py     # "unit:value"
│   └─ output_formatter.py # json | csv | table
├─ cli.py
└─ tests/
    ├─ test_converter.py   # Track B (Domain)
    └─ test_cli.py         # Track A (Boundary)
```

### 6.2 레거시 시드(`UnitConverter.py`) 개선 대상

- if/elif 단위 분기 → OCP 위반
- 비율 하드코딩 → 설정 외부화 필요
- 파싱·변환·출력 혼재 → SRP 위반
- 음수·형식·미지 단위 검증 없음

---

## §7. 제약 및 가정 (Constraints & Assumptions)

### 7.1 기술 제약

| 항목 | 내용 |
|------|------|
| 언어 | Python 3.10+ (권장 3.11+) |
| 테스트 | pytest |
| VCS | Git — `main` → `staging` → `spec` → `red` / `green` / `refactoring` / `new_features` |
| 개발 방식 | ARRR (RED → GREEN → REFACTOR), 1 RED 묶음 = 1 커밋 |

### 7.2 RED 단계 규칙

- RED 단계에서 **구현 코드 작성 금지**
- `pytest.fail("RED: ...")` 허용; skip / xfail 금지
- 모든 FR/NFR은 실패하는 테스트로 먼저 표현

### 7.3 가정

- 초기 기준 단위는 **meter**
- 길이 단위만 다룸 (무게·온도 등 제외)
- CLI 인터페이스 (GUI 없음)

### 7.4 설정 파일 예시 (`units.json`, P1)

```json
{
  "meter": 1.0,
  "feet": 3.28084,
  "yard": 1.09361
}
```

---

## §8. 수용 기준 및 추적표 (Acceptance & Traceability)

### 8.1 수용 기준 요약

| 구분 | 완료 조건 |
|------|-----------|
| P0 | FR-01~05, NFR-01~02 구현 + Domain TC 통과 + 팀 리뷰 |
| P1 | EXT-01~03 구현 + Boundary TC 포함 |
| 품질 게이트 | PRD → TC → 코드 C2C 역추적 가능; AI 생성 코드 설명 가능 |

### 8.2 PRD → 테스트 추적표

상세 1:1 매핑은 **`docs/traceability.md`** (SSOT). 요약:

#### 기능·비기능 (P0)

| PRD ID | Test ID (Track) | Given | Then (Expected) |
|--------|-----------------|-------|-----------------|
| FR-01 | D-PAR-01 (B) | `meter:2.5` | unit=meter, value=2.5 |
| FR-02 | D-CNV-02 (B) | 2.5 m | feet=8.2021 (4자리) |
| FR-02 | D-CNV-03 (B) | feet→yard | meter 경유 일치 |
| FR-02 | U-OUT-01 (A) | `meter:2.5` | 3줄 이상 출력 |
| FR-03 | D-REG-01 (B) | cubit 미등록 | E-UNIT |
| FR-04 | U-IN-03 (A), D-PAR-02 (B) | `meter:-1` | E-NEG |
| FR-05 | U-IN-01~02,04 (A), D-PAR-03 (B) | `""`, `meter`, `abc`, `meter:abc` | E-FMT / E-NUM |
| NFR-01 | D-REG-02 (B) | inch 등록 | Converter 핵심 비수정 |
| NFR-02 | D-STR-01~04 (B) | 패키지 구조 | 4모듈 분리 |
| NFR-03 | D-CNV-01 (B) | 1 feet | 0.3048 m (±0.0001) |

#### 확장 (P1)

| PRD ID | Test ID | Given | Then |
|--------|---------|-------|------|
| EXT-01 | D-CFG-01, D-CFG-02 (B) | JSON | ConfigError / 로드 성공 |
| EXT-02 | D-REG-03 (B) | cubit 0.4572 m | 등록 후 변환 |
| EXT-03 | U-FMT-01~03 (A) | `--format` | json / csv / table |

### 8.3 Dual-Track RED 설계

**Track A — Boundary (`tests/test_cli.py`)**

| Test ID | Given | Then |
|---------|-------|------|
| U-IN-01 | `""` | E-FMT |
| U-IN-02 | `meter` | E-FMT |
| U-IN-03 | `meter:-1` | E-NEG |
| U-IN-04 | `abc` | E-FMT |
| U-OUT-01 | `meter:2.5` | 3줄 이상, 4자리 환산 |
| U-FMT-01 | `--format json` | 유효 JSON (P1) |
| U-FMT-02 | `--format csv` | CSV (P1) |
| U-FMT-03 | `--format table` | 표/줄 출력 (P1) |

**Track B — Domain (`tests/test_converter.py`)**

| Test ID | 함수/대상 | Given / Then |
|---------|-----------|--------------|
| D-PAR-01 | parse | `meter:2.5` → meter, 2.5 |
| D-PAR-02 | parse | `-1` → E-NEG |
| D-PAR-03 | parse | `meter:abc` → E-NUM |
| D-CNV-01 | to_meter | 1 feet → 0.3048 m |
| D-CNV-02 | convert_all | 2.5 m → feet 8.2021 |
| D-CNV-03 | convert_all | feet→yard meter 경유 |
| D-REG-01 | registry | cubit 미등록 → E-UNIT |
| D-REG-02 | registry | inch 추가, OCP |
| D-REG-03 | registry | cubit 등록 (P1) |
| D-CFG-01 | config_loader | 깨진 JSON (P1) |
| D-CFG-02 | config_loader | units.json (P1) |
| D-STR-01~04 | 구조 | parser/registry/converter/formatter |

### 8.4 문서·회고 연계

| 산출물 | 경로/시점 |
|--------|-----------|
| PRD (본 문서) | `docs/PRD.md` — SSOT |
| Gap Analysis | `docs/gap-analysis.md` |
| To-Do | `docs/TODO.md` |
| Traceability | `docs/traceability.md` |
| Test Case | RED 단계 (`tests/`) |
| Report | ARRR 사이클 완료 시 `Report/NN.REPORT.md` |
| KPT 회고 | 실습 종료 — Keep / Problem / Try |

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 | 작성 |
|------|------|-----------|------|
| 0.1 | 2026-06-11 | Mom Test + lecture + README 기반 초안 | 박교현 |
| 0.2 | 2026-06-11 | spec 완료: 미결 스펙·추적표·갭분석·To-Do | 박교현 |
