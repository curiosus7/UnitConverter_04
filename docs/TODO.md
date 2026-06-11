# To-Do — PRD → 구현 작업 목록

| 항목 | 내용 |
|------|------|
| 문서 ID | TODO-UC-001 |
| 기준 PRD | `docs/PRD.md` v0.2 |
| 추적 | `docs/traceability.md` |
| 작성일 | 2026-06-11 |

**규칙 (C2C):** 1 To-Do : 1+ Test Case · RED 먼저 · 1 RED 묶음 = 1 커밋

---

## P0 — 필수 (red / green / refactoring)

| To-Do ID | 작업 | 모듈/브랜치 | PRD | Test ID | 상태 |
|----------|------|-------------|-----|---------|------|
| **TD-01** | 입력 파싱·검증 (`unit:value`) | `unit_converter/app/input_parser.py` · `red` | FR-01, FR-04, FR-05 | D-PAR-01, U-IN-01~04 | pending |
| **TD-02** | meter 기준 환산 (전 단위) | `unit_converter/domain/converter.py` · `red` | FR-02, NFR-03 | D-CNV-01~03, U-OUT-01 | pending |
| **TD-03** | 단위 등록·조회 (OCP) | `unit_converter/domain/unit_registry.py` · `red` | FR-03, NFR-01 | D-REG-01, D-REG-02 | pending |
| **TD-04** | CLI 경계 (입력·출력 계약) | `unit_converter/cli.py` · `red` | FR-02~05 | U-IN-*, U-OUT-01 | pending |
| **TD-05** | SRP 패키지 분리 | `refactoring` | NFR-02 | D-STR-01~04 | pending |
| **TD-06** | 출력 포맷터 분리 | `unit_converter/app/output_formatter.py` · `refactoring` | NFR-02 | D-STR-04 | pending |

---

## P1 — 확장 (new_features)

| To-Do ID | 작업 | 모듈/브랜치 | PRD | Test ID | 상태 |
|----------|------|-------------|-----|---------|------|
| **TD-07** | `units.json` 로드 | `infrastructure/config_loader.py` | EXT-01 | D-CFG-01, D-CFG-02 | pending |
| **TD-08** | 동적 단위 등록 CLI | registry 확장 | EXT-02 | D-REG-03 | pending |
| **TD-09** | `--format json\|csv\|table` | `output_formatter.py` · CLI | EXT-03 | U-FMT-01~03 | pending |

---

## TD-01 상세 (RED 1차 묶음 후보)

| 항목 | 내용 |
|------|------|
| Goal | `parse("meter:2.5")` → `(unit="meter", value=2.5)` |
| 거부 | `""`, `meter`, `meter:-1`, `abc`, `meter:abc` |
| 완료 조건 | D-PAR-01, U-IN-01~04 RED→GREEN |

---

## TD-02 상세

| 항목 | 내용 |
|------|------|
| Goal | 2.5 m → feet 8.2021 (소수 4자리 반올림) |
| 불변 | feet↔yard는 meter 경유 |
| 완료 조건 | D-CNV-01~03, U-OUT-01 |

---

## 브랜치 매핑

| 브랜치 | To-Do |
|--------|-------|
| `spec` | 문서·Harness (본 단계) |
| `red` | TD-01 ~ TD-04 테스트 스켈레톤 |
| `green` | TD-01 ~ TD-04 최소 구현 |
| `refactoring` | TD-05, TD-06 |
| `new_features` | TD-07 ~ TD-09 |

---

## 변경 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| 0.1 | 2026-06-11 | spec 4단계 — PRD v0.2 기반 |
