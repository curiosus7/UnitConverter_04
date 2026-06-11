# Unit Converter (Python)

![unit-converter](./unit-converter.jpg)

## Overview

길이 단위 변환 CLI를 **PRD와 테스트로부터 추적 가능하게(C2C)** 재구현하는 프로젝트입니다.

- 입력: `단위:값` (예: `meter:2.5`)
- 출력: 지원 단위 전체로 환산 (기본 줄 단위; 확장 시 JSON / CSV / 표)
- 개발 방식: ARRR (RED → GREEN → REFACTOR) · Dual-Track TDD

> **스테이크홀더 안내:** 아래 [프로젝트 진행 현황](#프로젝트-진행-현황)에서 완료·진행·예정 항목을 한눈에 확인할 수 있습니다.  
> (lecture: Report 8섹션 중 §1 작업 개요 · §2 완료 To-Do · §7 미완료 & 다음 단계를 README에 요약 반영)

---

## 프로젝트 진행 현황

| 항목 | 내용 |
|------|------|
| 최종 갱신 | 2026-06-11 |
| 현재 브랜치 | `spec` |
| 현재 단계 | **spec 완료** (세션 01 Export) → 다음: **`red`** |
| 최신 Report | [Report/01.REPORT.md](Report/01.REPORT.md) |
| PRD 버전 | [v0.2](docs/PRD.md) |
| pytest | 환경 구성 완료 · `tests/` 미작성 |

### 7단계 · ARRR 로드맵

| 단계 | 내용 | 상태 | 비고 |
|------|------|------|------|
| ① 주제 | Mom Test → 문제 한 문장 | ✅ 완료 | PRD §1 |
| ② R-G-I-O | Role·Goal·Input·Output | ✅ 완료 | PRD §2 |
| spec | PRD·갭·추적·Harness·환경·Export | ✅ 완료 | Report/01 |
| ③ Ask (RED) | Dual-Track 실패 테스트 | ⏳ 예정 | `red` 브랜치 |
| ④ Respond (GREEN) | 최소 구현 | ⏳ 예정 | `green` 브랜치 |
| ⑤ Refine (REFACTOR) | SRP 분리·Golden Master | ⏳ 예정 | `refactoring` 브랜치 |
| ⑥ Repeat | 추가 FR RED 반복 | ⏳ 예정 | |
| ⑦ 확장 | EXT-01~03 | ⏳ 예정 | `new_features` 브랜치 |

### 완료된 산출물 (§2 완료 To-Do 요약)

| 구분 | 산출물 | 링크 |
|------|--------|------|
| 요구사항 | PRD v0.2 (SSOT) | [docs/PRD.md](docs/PRD.md) |
| 분석 | 시드 vs PRD 갭 분석 | [docs/gap-analysis.md](docs/gap-analysis.md) |
| 설계 | 추적표 · To-Do | [docs/traceability.md](docs/traceability.md) · [docs/TODO.md](docs/TODO.md) |
| 환경 | venv · pytest · requirements.txt | `requirements.txt` |
| Harness | Cursor Rules · Skill | `.cursor/rules/` · `.cursor/skills/unit-converter-tdd/` |
| Git | `staging` · `spec` 브랜치 | — |
| 문서 | README (진입·현황) | 본 파일 |
| Export | 세션 01 Report·Transcript | [Report/01](Report/01.REPORT.md) · [Prompting/01](Prompting/01.Export-Transcript.md) |

### 구현 To-Do 진행 (P0)

| ID | 작업 | 브랜치 | 상태 |
|----|------|--------|------|
| TD-01 | 입력 파싱·검증 | `red` | ⏳ pending |
| TD-02 | meter 기준 환산 | `red` | ⏳ pending |
| TD-03 | 단위 Registry (OCP) | `red` | ⏳ pending |
| TD-04 | CLI 경계 테스트 | `red` | ⏳ pending |
| TD-05 | SRP 패키지 분리 | `refactoring` | ⏳ pending |
| TD-06 | 출력 포맷터 분리 | `refactoring` | ⏳ pending |

상세: [docs/TODO.md](docs/TODO.md)

### 다음 단계 (§7 미완료 & 다음 단계)

1. **`red` 브랜치** 생성 — TD-01 입력 파싱 RED 스켈레톤 (`D-PAR-01`, `U-IN-01~04`)
2. **Dual-Track** — `tests/test_converter.py` (B) · `tests/test_cli.py` (A)
3. **팀 리뷰** — PRD → TC 설계 C2C 추적성 확인 (Ground Rules PDF)
4. **GREEN** — TD-01~04 최소 구현 (`green` 브랜치)
5. **KPT 회고** — 실습 종료 시 (발표: A팀 권용환)

### 실습 Activities 진행 (6시간)

| # | 활동 | 계획 | 상태 |
|---|------|------|------|
| 1 | 문제 코드·요구사항 분석 | 0.5h | ✅ 갭 분석 완료 |
| 2 | 기본·품질 요구사항 구현 | 2h | ⏳ RED→GREEN 대기 |
| 3 | TC 구현 | 0.5h | ⏳ `tests/` 대기 |
| 4 | 추가 요구사항 구현 | 2h | ⏳ P1 (EXT) 대기 |
| 5 | 회고 및 발표 | 1h | ⏳ KPT 예정 |

### 품질 게이트 (수용 기준)

| 게이트 | 조건 | 상태 |
|--------|------|------|
| P0 | FR-01~05, NFR-01~02 + Domain TC | ⏳ |
| P1 | EXT-01~03 + Boundary TC | ⏳ |
| 팀 리뷰 | PRD→TC→코드 C2C · AI 코드 설명 | ⏳ |
| main 병합 | 위 게이트 통과 후 | ⏳ |

---

## 문서 (SSOT)

| 문서 | 경로 | 설명 |
|------|------|------|
| **PRD (요구사항 SSOT)** | [docs/PRD.md](docs/PRD.md) | §1~§8 요구·수용 기준 |
| Gap Analysis | [docs/gap-analysis.md](docs/gap-analysis.md) | 시드 vs PRD 갭 |
| To-Do | [docs/TODO.md](docs/TODO.md) | PRD → 구현 작업 |
| Traceability | [docs/traceability.md](docs/traceability.md) | PRD ↔ Test ID 매핑 |

> 상세 요구사항·오류 메시지·추적표는 **PRD 및 traceability**를 따릅니다. README는 진입·요약용입니다.

---

## 빠른 시작

### 가상환경 및 의존성

```bash
# 가상환경 생성
python -m venv venv

# 활성화 (Windows)
venv\Scripts\activate

# 활성화 (macOS/Linux / Git Bash)
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 시드 코드 실행 (레거시)

```bash
python UnitConverter.py
# 입력 예: meter:2.5
```

### 테스트 (목표 구조 — RED 단계에서 추가)

```bash
pytest tests/ -v
pytest tests/test_converter.py -v   # Track B (Domain)
pytest tests/test_cli.py -v       # Track A (Boundary)
```

### 목표 CLI (구현 후)

```bash
python -m unit_converter "meter:2.5"
python -m unit_converter "meter:2.5" --format json
```

---

## 요구사항 요약

상세: [docs/PRD.md](docs/PRD.md) §5~§7

### P0 — 필수

| ID | 요약 |
|----|------|
| FR-01 | `unit:value` 파싱 |
| FR-02 | 전 단위 환산 출력 (4자리 반올림) |
| FR-03 | 미지 단위 오류 |
| FR-04 | 음수 거부 |
| FR-05 | 잘못된 형식 거부 |
| NFR-01 | OCP — 단위 추가 시 변환기 핵심 비수정 |
| NFR-02 | SRP — Parser / Registry / Converter / Formatter 분리 |

### P1 — 확장

| ID | 요약 |
|----|------|
| EXT-01 | `units.json` / YAML 비율 로드 |
| EXT-02 | 동적 단위 등록 (`1 cubit = 0.4572 meter`) |
| EXT-03 | `--format json \| csv \| table` |

### 비즈니스 로직

- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet ↔ yard는 **meter 경유** 계산

---

## 예시 입출력

입력:

```
meter:2.5
```

출력 (소수 4자리 반올림):

```
2.5 meter = 2.5000 meter
2.5 meter = 8.2021 feet
2.5 meter = 2.7340 yard
```

기본 지원 단위: `meter`, `feet`, `yard`

---

## 목표 프로젝트 구조

상세: [docs/PRD.md](docs/PRD.md) §6.1

```
unit_converter/
├─ domain/          # registry, converter (OCP)
├─ infrastructure/  # config_loader
├─ app/             # input_parser, output_formatter
├─ cli.py
└─ tests/
    ├─ test_converter.py   # Track B
    └─ test_cli.py         # Track A
```

현재 시드: 루트 `UnitConverter.py` (37 lines, 리팩터링 대상)

---

## Git 브랜치

```
main → staging → spec → red → green → refactoring → new_features
                  ▲ spec 완료 · ⏳ red 다음
```

| 브랜치 | 목적 | 상태 |
|--------|------|------|
| `staging` | 작업 기준점 | ✅ |
| `spec` | 문서·설계·Harness | ✅ **현재·완료** |
| `red` | RED 테스트 스켈레톤 | ⏳ **다음** |
| `green` | 최소 구현 | ⏳ |
| `refactoring` | SRP 패키지 분리 | ⏳ |
| `new_features` | EXT-01~03 | ⏳ |

---

## Cursor Harness

| 요소 | 경로 |
|------|------|
| Rules | `.cursor/rules/unit-converter.mdc` |
| Skill | `.cursor/skills/unit-converter-tdd/SKILL.md` |
| Commands | `.cursor/commands/` (`/red-test-plan`, `/red-skeleton`, …) |

---

## 세션 문서 (ARRR 후 갱신)

lecture: ARRR 한 사이클마다 Report(8섹션) + Transcript 저장 · README 표에 1행 추가

| NN | 주제 | Phase | Report | Transcript |
|----|------|-------|--------|------------|
| 01 | spec — PRD·갭·Harness·정합성 | spec | [Report/01.REPORT.md](Report/01.REPORT.md) | [Prompting/01.Export-Transcript.md](Prompting/01.Export-Transcript.md) |
| — | RED TD-01 파싱 | red | ⏳ | ⏳ |

Report 8섹션: §1 개요 · §2 완료 To-Do · §3 RED · §4 GREEN · §5 REFACTOR · §6 커버리지 · §7 다음 단계 · §8 이슈

---

## 생성형AI를 활용한 Activities (6시간)

상세 진행률은 [프로젝트 진행 현황](#프로젝트-진행-현황) 참조.

1. **문제 코드 및 기본 요구사항 분석** (0.5h) — ✅ 시드 구조, PRD 갭
2. **기본·품질 요구사항 구현** (2h) — ⏳ OCP/SRP, 입력 검증
3. **TC 구현** (0.5h) — ⏳ Dual-Track 테스트
4. **추가 요구사항 구현** (2h) — ⏳ EXT-01~03 + TC
5. **회고 및 발표** (1h) — ⏳ KPT, AI 활용 회고
