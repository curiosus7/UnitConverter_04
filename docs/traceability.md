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
| FR-03 | TD-04 | **U-IN-05** | A | `cubit:1` (미등록) | E-UNIT |
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
| EXT-01 | TD-07 | **D-CFG-03** | B | JSON 배열 | ConfigError |
| EXT-01 | TD-07 | **D-CFG-04** | B | 비율 비숫자 | ConfigError |
| EXT-01 | TD-07 | **U-CFG-01** | A | --units-file 깨진 JSON | ConfigError |
| EXT-01 | TD-07 | **U-CFG-02** | A | --units-file 유효 | 변환 성공 |
| EXT-01 | TD-07 | **U-CFG-03** | A | --units-file 없는 경로 | ConfigError |
| EXT-01 | TD-07 | **U-CFG-04** | A | --units-file 값 없음 | 기본 registry |
| EXT-01 | TD-07 | **U-CFG-05** | A | 루트 units.json | 변환 성공 |
| EXT-02 | TD-08 | **D-REG-03** | B | cubit=0.4572 m 등록 | cubit:1 변환 가능 |
| EXT-02 | TD-08 | **D-REG-04** | B | register 문자열 유효 | cubit, 0.4572 |
| EXT-02 | TD-08 | **D-REG-05** | B | register 문자열 무효 | RegisterParseError |
| EXT-02 | TD-08 | **U-REG-01** | A | --register + cubit:1 | 변환 성공 |
| EXT-02 | TD-08 | **U-REG-02** | A | --register 잘못된 형식 | E-REG |
| EXT-02 | TD-08 | **U-REG-03** | A | --register 값 없음 | 등록 생략 |
| EXT-02 | TD-08 | **U-REG-04** | A | units-file + register | cubit 변환 |
| EXT-03 | TD-09 | **U-FMT-01** | A | --format json | 유효 JSON |
| EXT-03 | TD-09 | **U-FMT-02** | A | --format csv | CSV 헤더·행 |
| EXT-03 | TD-09 | **U-FMT-03** | A | --format table | box table 출력 |
| EXT-03 | TD-09 | **D-FMT-01** | B | format_table_output | lecture 부록 box table |
| EXT-03 | TD-09 | **U-FMT-04** | A | --format 생략 | table 기본 |
| EXT-03 | TD-09 | **U-FMT-05** | A | --format xml | E-FMT-OPT |
| EXT-03 | TD-09 | **U-FMT-06** | A | --format 값 없음 | table 기본 |
| EXT-04 | TD-10 | **U-GUI-01** | A | unit=meter, value=2.5, table | 3줄 이상, 4자리 |
| EXT-04 | TD-10 | **U-GUI-02** | A | format=json | 유효 JSON |
| EXT-04 | TD-10 | **U-GUI-03** | A | value=-1 | E-NEG |
| EXT-04 | TD-10 | **U-GUI-04** | A | value=abc | E-NUM |
| EXT-04 | TD-10 | **U-GUI-05** | A | format=csv | CSV 헤더·행 |
| EXT-04 | TD-10 | **U-GUI-06** | A | format 미변경 | table 기본 |
| EXT-04 | TD-10 | **U-GUI-07** | A | value='' | E-FMT |
| EXT-04 | TD-10 | **U-GUI-08** | A | unit=feet, value=10 | I-02 환산 |

---

## 오류 메시지 계약 (SSOT)

| 코드 | 메시지 (정확 문자열) | Test ID |
|------|----------------------|---------|
| E-FMT | `Invalid format. Use unit:value (ex: meter:2.5)` | U-IN-01, U-IN-02, U-IN-04 |
| E-NUM | `Invalid number: {value_str}` | D-PAR-03 |
| E-NEG | `Negative value not allowed` | U-IN-03, D-PAR-02, U-GUI-03 |
| E-UNIT | `Unknown unit: {unit}` | D-REG-01, U-IN-05 |
| E-REG | `Invalid register format. Use: 1 cubit = 0.4572 meter` | U-REG-02, D-REG-05 |
| E-FMT-OPT | `Invalid format option. Use: csv, json, table` | U-FMT-05 |

---

## Golden Master (Approval Test)

| Golden ID | 연결 Test | Given | Then | 파일 |
|-----------|-----------|-------|------|------|
| **GM-METER-25** | GM test, U-FMT-04/06, U-CFG-02/04, U-REG-03 | `meter:2.5` (format 생략) | table stdout | `tests/golden/GM-METER-25.approved.txt` |
| **GM-METER-NEG** | GM test, U-GUI-03 | `meter:-1` | E-NEG 한 줄 | `tests/golden/GM-METER-NEG.approved.txt` |
| **GM-FMT-TABLE** | U-FMT-03, U-GUI-01/06 | `meter:2.5 --format table` | table stdout | `tests/golden/GM-FMT-TABLE.approved.txt` |
| **GM-FMT-JSON** | U-FMT-01, U-GUI-02 | `meter:2.5 --format json` | JSON 전체 | `tests/golden/GM-FMT-JSON.approved.txt` |
| **GM-FMT-CSV** | U-FMT-02, U-GUI-05 | `meter:2.5 --format csv` | CSV 전체 | `tests/golden/GM-FMT-CSV.approved.txt` |
| **GM-FEET-10** | GM test, U-GUI-08 | `feet:10` table | I-02 stdout | `tests/golden/GM-FEET-10.approved.txt` |
| **GM-REG-CUBIT-1** | U-REG-01 | `--register` + `cubit:1` | 4단위 table | `tests/golden/GM-REG-CUBIT-1.approved.txt` |
| **GM-REG-CUBIT-2** | U-REG-04 | units-file + register + `cubit:2` | 3단위 table | `tests/golden/GM-REG-CUBIT-2.approved.txt` |
| **GM-FMT-OPT-ERR** | U-FMT-05 | `--format xml` | E-FMT-OPT | `tests/golden/GM-FMT-OPT-ERR.approved.txt` |
| **GM-REG-ERR** | U-REG-02 | `--register bad` | E-REG | `tests/golden/GM-REG-ERR.approved.txt` |
| **GM-UNIT-CUBIT-ERR** | U-IN-05 | `cubit:1` 미등록 | E-UNIT | `tests/golden/GM-UNIT-CUBIT-ERR.approved.txt` |

갱신: `UPDATE_GOLDEN=1 pytest tests/ -v` (수동 `.approved.txt` 편집 금지)

---

## 변경 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| 0.1 | 2026-06-11 | spec 3단계 — 1:1 매핑 정리 |
| 0.2 | 2026-06-11 | REFACTOR — D-STR-01~04·Golden Master TC 추가 (세션 04) |
| 0.3 | 2026-06-11 | new_features — EXT-04 U-GUI-01~04·D-CFG·D-REG-03·U-FMT (세션 05) |
| 0.4 | 2026-06-11 | Golden Master — `tests/golden/*.approved.txt` + `_approval.py` |
| 0.5 | 2026-06-11 | P1 Boundary TC — U-CFG/U-REG/U-FMT 옵션·생략·오류 + U-IN-05 |
| 0.6 | 2026-06-11 | Golden Master 확장 — 옵션별 10건 `.approved.txt` |
