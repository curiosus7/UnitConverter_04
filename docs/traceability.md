# Traceability — PRD ↔ To-Do ↔ Test Case

| 항목 | 내용 |
|------|------|
| 문서 ID | TRACE-UC-001 |
| 기준 PRD | `docs/PRD.md` v0.2 |
| 작성일 | 2026-06-11 |

---

## P0 기능 요구

| PRD ID | To-Do | Test ID | Track | Given | Then |
|--------|-------|---------|-------|-------|------|
| FR-01 | TD-01 | **D-PAR-01** | B | `meter:2.5` | unit=meter, value=2.5 |
| FR-02 | TD-02 | **D-CNV-02** | B | 2.5 m | feet=8.2021 (4자리) |
| FR-02 | TD-02 | **D-CNV-03** | B | feet→yard | meter 경유 일치 |
| FR-02 | TD-04 | **U-OUT-01** | A | `meter:2.5` | 3줄 이상 출력 |
| FR-03 | TD-03 | **D-REG-01** | B | cubit 미등록 | Unknown unit 오류 |
| FR-04 | TD-01 | **U-IN-03** | A | `meter:-1` | Negative value 오류 |
| FR-04 | TD-01 | **D-PAR-02** | B | `meter:-1` | E-NEG / ParseError |
| FR-05 | TD-01 | **U-IN-01** | A | `""` | Invalid format |
| FR-05 | TD-01 | **U-IN-02** | A | `meter` | Invalid format |
| FR-05 | TD-01 | **U-IN-04** | A | `abc` | Invalid format |
| FR-05 | TD-01 | **D-PAR-03** | B | `meter:abc` | Invalid number |

---

## P0 비기능 요구

| PRD ID | To-Do | Test ID | Track | Given | Then |
|--------|-------|---------|-------|-------|------|
| NFR-01 | TD-03 | **D-REG-02** | B | inch 등록 | Converter 파일 비수정으로 환산 |
| NFR-02 | TD-05 | **D-STR-01** | B | 패키지 구조 | input_parser 모듈 존재 |
| NFR-02 | TD-05 | **D-STR-02** | B | 패키지 구조 | unit_registry 모듈 존재 |
| NFR-02 | TD-05 | **D-STR-03** | B | 패키지 구조 | converter 모듈 존재 |
| NFR-02 | TD-05 | **D-STR-04** | B | 패키지 구조 | output_formatter 모듈 존재 |
| NFR-03 | TD-02 | **D-CNV-01** | B | 1 feet | 0.3048 m (±0.0001) |
| NFR-04 | — | (본 문서) | — | 전 FR/NFR | Test ID 1:1 |
| NFR-05 | TD-04 | U-*, D-* | A+B | Dual-Track | test_cli + test_converter |

---

## P1 확장 요구

| PRD ID | To-Do | Test ID | Track | Given | Then |
|--------|-------|---------|-------|-------|------|
| EXT-01 | TD-07 | **D-CFG-01** | B | 깨진 JSON | ConfigError |
| EXT-01 | TD-07 | **D-CFG-02** | B | valid units.json | 3단위 로드 |
| EXT-02 | TD-08 | **D-REG-03** | B | cubit=0.4572 m 등록 | cubit:1 변환 가능 |
| EXT-03 | TD-09 | **U-FMT-01** | A | --format json | 유효 JSON |
| EXT-03 | TD-09 | **U-FMT-02** | A | --format csv | CSV 헤더·행 |
| EXT-03 | TD-09 | **U-FMT-03** | A | --format table | 줄/표 출력 |

---

## 오류 메시지 계약 (SSOT)

| 코드 | 메시지 (정확 문자열) | Test ID |
|------|----------------------|---------|
| E-FMT | `Invalid format. Use unit:value (ex: meter:2.5)` | U-IN-01, U-IN-02, U-IN-04 |
| E-NUM | `Invalid number: {value_str}` | D-PAR-03 |
| E-NEG | `Negative value not allowed` | U-IN-03, D-PAR-02 |
| E-UNIT | `Unknown unit: {unit}` | D-REG-01 |

---

## 변경 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| 0.1 | 2026-06-11 | spec 3단계 — 1:1 매핑 정리 |
