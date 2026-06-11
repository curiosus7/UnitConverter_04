# Command: UC Export Session — UnitConverter

ARRR 사이클(RED/GREEN/REFACTOR) 종료 시 **Report 8섹션** + **Transcript** Export.

---

## 실행

```
/uc-export-session
```

세션 번호 미지정 시 `Report/`·`Prompting/` 최대 NN + 1.

---

## 출력 (2파일만)

| 경로 | 예 |
|------|-----|
| `Report/NN.REPORT.md` | `Report/02.REPORT.md` |
| `Prompting/NN.Export-Transcript.md` | `Prompting/02.Export-Transcript.md` |

---

## Report 8섹션 (UnitConverter)

1. **요약** — Phase, pytest 결과, 커밋
2. **산출물** — 변경 파일 표
3. **RED** — Test ID, FAIL 건수 (해당 Phase일 때)
4. **GREEN** — PASS Test ID (해당 Phase일 때)
5. **REFACTOR** — 스멜·추출 (해당 Phase일 때)
6. **커버리지** — `pytest tests/ -v` 요약
7. **다음 단계** — 다음 TD / 브랜치
8. **이슈** — Harness·팀 리뷰 등

---

## README 갱신 (같은 세션)

- `## 프로젝트 진행 현황` — 브랜치·단계·pytest
- `## 세션 문서` 표에 NN 행 추가
- `docs/TODO.md` TD 상태 (해당 시)

---

## SSOT

- `docs/PRD.md`, `docs/traceability.md`, `docs/TODO.md`
- lecture: Report = README 요약 대시보드
