# Gap Analysis — 시드 코드 vs PRD

| 항목 | 내용 |
|------|------|
| 문서 ID | GAP-UC-001 |
| 기준 PRD | `docs/PRD.md` v0.2 |
| 대상 시드 | `UnitConverter.py` (37 lines) |
| 작성일 | 2026-06-11 |

---

## 1. 요약

| 구분 | 건수 | 비고 |
|------|------|------|
| P0 갭 (패키지 `unit_converter/`) | **0** | GREEN+REFACTOR 완료 (세션 04) |
| P0 갭 (시드 `UnitConverter.py`만) | 12 | 레거시 — 수정 대상 아님 |
| P1 갭 (확장 요구) | **0** | new_features 완료 (세션 05) |
| P1 갭 (시드만) | 3 | EXT — 패키지에서 해소, 시드는 레거시 |
| 시드 코드 스멜 | 5 | 패키지에서 S-01·S-03~S-05 해소 |

`unit_converter/` 패키지는 P0·P1(EXT-01~04)을 충족한다. 시드 파일은 갭 분석·비교용으로만 유지한다.

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
| **EXT-01** | 비율 하드코딩 | ~~`units.json` 로드 없음~~ | ✅ 패키지 (TD-07) |
| **EXT-02** | 고정 3단위만 | ~~동적 단위 등록 없음~~ | ✅ 패키지 (TD-08) |
| **EXT-03** | `print`만 | ~~`--format` 없음~~ | ✅ 패키지 (TD-09) |
| **EXT-04** | GUI 없음 | ~~PyQt 없음~~ | ✅ 패키지 (TD-10) |

---

## 3. 코드 스멜 목록

| # | 스멜 | 위치 | PRD 연계 | 조치 방향 |
|---|------|------|----------|-----------|
| S-01 | Long Method / God `main()` | L1–L32 | NFR-02 | Parser·Converter·Formatter 추출 |
| S-02 | Duplicated Magic Numbers | L19–L28 | NFR-03, EXT-01 | ✅ Registry + `units.json` |
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

### 5.1 패키지 (`unit_converter/`) — P0+P1 (세션 05 갱신)

| PRD §6.1 모듈 | 경로 | 상태 |
|---------------|------|------|
| `input_parser.py` | `app/input_parser.py` | ✅ TD-01 |
| `unit_registry.py` | `domain/unit_registry.py` | ✅ TD-03 |
| `converter.py` | `domain/converter.py` | ✅ TD-02 |
| `output_formatter.py` | `app/output_formatter.py` | ✅ TD-06 · TD-09 (box table/json/csv) |
| `cli.py` | `cli.py` + `__main__.py` | ✅ orchestration (TD-04, P1 옵션) |
| `config_loader.py` | `infrastructure/config_loader.py` | ✅ TD-07 |
| `conversion_service.py` | `app/conversion_service.py` | ✅ CLI/GUI 공유 |
| `register_parser.py` | `app/register_parser.py` | ✅ TD-08 |
| `ui/main_window.py` | `ui/` + `__main__gui__.py` | ✅ TD-10 PyQt |
| `tests/test_converter.py` | `tests/` Track B | ✅ 21+ TC |
| `tests/test_cli.py` | `tests/` Track A | ✅ 24+ TC |
| `tests/test_gui.py` | `tests/` Track A (GUI) | ✅ 8 TC |
| `tests/golden/*.approved.txt` | `tests/golden/` | ✅ 11 Golden Master |
| `length_unit.py` | — | ⏳ 선택 (PRD 목표만) |

### 5.2 시드 (`UnitConverter.py`) — 레거시

| PRD §6.1 모듈 | 시드 | 상태 |
|---------------|------|------|
| 전 모듈 | 단일 `main()` | ❌ SRP/OCP 위반 (비교용 유지) |

---

## 6. RED 우선순위 (갭 → To-Do 연계)

1. **TD-01** input_parser — FR-01, FR-04, FR-05  
2. **TD-02** converter — FR-02, NFR-03  
3. **TD-03** unit_registry — FR-03, NFR-01  
4. **TD-04** CLI boundary — U-IN-*, U-OUT-01  
5. **TD-05~06** SRP 패키지 분리 — NFR-02 (`refactoring`)  
6. **TD-07~10** EXT-01~04 (`new_features`) — ✅ 완료

---

## 변경 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| 0.1 | 2026-06-11 | 초안 — spec 1단계 |
| 0.2 | 2026-06-11 | REFACTOR 완료 — §1·§5 패키지 P0 갭 클로즈 |
| 0.3 | 2026-06-11 | new_features 완료 — P1 갭 0 · EXT-01~04 · Golden Master 11건 |
