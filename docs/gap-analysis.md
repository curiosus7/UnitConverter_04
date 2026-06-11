# Gap Analysis — 시드 코드 vs PRD

| 항목 | 내용 |
|------|------|
| 문서 ID | GAP-UC-001 |
| 기준 PRD | `docs/PRD.md` v0.2 |
| 대상 시드 | `UnitConverter.py` (37 lines) |
| 작성일 | 2026-06-11 |

---

## 1. 요약

| 구분 | 건수 |
|------|------|
| P0 갭 (미구현·위반) | 12 |
| P1 갭 (확장 요구) | 3 |
| 부분 구현 | 4 |
| 코드 스멜 (NFR) | 5 |

시드는 **데모 수준의 단일 파일 CLI**이며, PRD가 요구하는 **모듈 분리·검증·추적 가능한 테스트 구조**와 거리가 있다.

---

## 2. PRD ID별 갭 상세

| PRD ID | 시드 현황 | 갭 | 심각도 |
|--------|-----------|-----|--------|
| **FR-01** | `split(':', 1)` + `float()` 로 파싱 | 전용 `input_parser` 모듈 없음; 파싱 로직 테스트 불가 | P0 |
| **FR-02** | 3단위 출력함 | 소수 **4자리** 고정 없음(가변 float 표시); `python -m unit_converter` 미지원 | P0 |
| **FR-03** | `Unknown unit: {unit}` 출력 후 return | E-UNIT 메시지는 v0.2 확정; 예외 타입·exit code는 RED에서 TC 고정 | P0 |
| **FR-04** | 음수 검증 **없음** | `-1` 등 음수 그대로 변환됨 | P0 |
| **FR-05** | 콜론 없음만 검사 | 빈 문자열 `""` 미검증; `abc` 전체 비정상 입력 미검증; `meter:abc`는 ValueError만 | P0 |
| **FR-05** | `meter:2.5:extra` | `value_str="2.5:extra"` → float 실패 → `Invalid number` (형식 오류로 통일) | P0 |
| **NFR-01** | `if/elif` 단위 분기 | 단위 추가 시 `main()` 수정 필요 — **OCP 위반** | P0 |
| **NFR-02** | 파싱·변환·출력이 `main()`에 혼재 | Parser/Registry/Converter/Formatter **미분리** | P0 |
| **NFR-03** | 하드코딩 비율 | 상수 일관성은 있으나 외부 설정·테스트 고정 자릿수 없음 | P0 |
| **NFR-04** | 테스트 없음 | PRD↔TC 추적 불가 | P0 |
| **NFR-05** | 단일 파일 | Dual-Track `tests/` 구조 없음 | P0 |
| **EXT-01** | 비율 하드코딩 | `units.json` / YAML 로드 없음 | P1 |
| **EXT-02** | 고정 3단위만 | 동적 단위 등록 없음 | P1 |
| **EXT-03** | `print`만 | `--format json\|csv\|table` 없음 | P1 |

---

## 3. 코드 스멜 목록

| # | 스멜 | 위치 | PRD 연계 | 조치 방향 |
|---|------|------|----------|-----------|
| S-01 | Long Method / God `main()` | L1–L32 | NFR-02 | Parser·Converter·Formatter 추출 |
| S-02 | Duplicated Magic Numbers | L19–L28 | NFR-03, EXT-01 | Registry + 설정 파일 |
| S-03 | Switch on type (if/elif unit) | L16–L24 | NFR-01 | `unit_registry` |
| S-04 | No negative validation | L10–L14 | FR-04 | parser 검증 |
| S-05 | Mixed abstraction (input+logic+IO) | 전체 | NFR-02, SRP | 패키지 구조 |

---

## 4. 부분 구현 (재사용 가능)

| 항목 | 시드 동작 | PRD와의 차이 |
|------|-----------|--------------|
| 콜론 구분 파싱 | `split(':', 1)` | FR-01 기초 — 모듈화 필요 |
| 기본 비율 | 3.28084, 1.09361 | PRD §4.2와 일치 |
| 미지 단위 메시지 | `Unknown unit: {unit}` | 문구 SSOT 확정 후 유지 가능 |
| 형식 오류 1종 | `Invalid format...` | U-IN-01~02 계약에 편입 |

---

## 5. 아키텍처 갭

| PRD §6.1 모듈 | 시드 | 상태 |
|---------------|------|------|
| `input_parser.py` | `main()` L4–L14 | ❌ 없음 |
| `unit_registry.py` | if/elif L16–24 | ❌ 없음 |
| `converter.py` | L26–28 인라인 | ❌ 없음 |
| `output_formatter.py` | print L30–32 | ❌ 없음 |
| `config_loader.py` | — | ❌ 없음 |
| `cli.py` | `main()` + input | ❌ 패키지 CLI 없음 |
| `tests/test_converter.py` | — | ❌ 없음 |
| `tests/test_cli.py` | — | ❌ 없음 |

---

## 6. RED 우선순위 (갭 → To-Do 연계)

1. **TD-01** input_parser — FR-01, FR-04, FR-05  
2. **TD-02** converter — FR-02, NFR-03  
3. **TD-03** unit_registry — FR-03, NFR-01  
4. **TD-04** CLI boundary — U-IN-*, U-OUT-01  
5. **TD-05~06** SRP 패키지 분리 — NFR-02 (`refactoring`)  
6. **TD-07~09** EXT-01~03 (`new_features`)

---

## 변경 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| 0.1 | 2026-06-11 | 초안 — spec 1단계 |
