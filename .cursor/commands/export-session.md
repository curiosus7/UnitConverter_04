# Command: Export Session

> **UnitConverter_04:** Magic Square 템플릿 — **`/uc-export-session` 사용** (Report 8섹션 · UnitConverter).

세션 종료 시 **Report** 보고서 + **Prompting** Transcript를 한 번에 Export한다.

**Export 요청 시 magic-square-docs Skill 로드 후 checklist 수행** (`.cursor/skills/magic-square-docs/`).

---

## 실행 트리거

사용자가 아래와 같이 요청할 때 이 Command를 따른다:

```
Report 폴더에 보고서 생성하고, Prompting 폴더에 Transcript도 Export 해줘.
```

세션 번호가 없으면 **기존 `Report/`·`Prompting/`의 `NN.*` 파일 중 최대 NN+1**을 사용한다.  
사용자가 `03` 등 번호를 명시하면 그 번호를 쓴다.

---

## 파일명 규칙 (`NN.XXX` 형식)

| NN | 의미 | 예 |
|----|------|-----|
| 2자리 세션 번호 | STEP·세션 순번 | `01`, `03` |
| XXX | 문서 종류 (대문자·하이픈) | `REPORT`, `Export-Transcript` |

**필수 출력 (2개만 생성·갱신):**

| 경로 | 파일명 예 |
|------|-----------|
| `Report/` | `Report/03.REPORT.md` |
| `Prompting/` | `Prompting/03.Export-Transcript.md` |

- 기존 동일 파일이 있으면 **본 세션 내용으로 덮어쓴다** (사용자가 “추가만” 명시한 경우 제외).
- `STEP*`, `cursor_*` 등 **다른 Prompting 파일은 이 Command에서 만들지 않는다.**

---

## 절차

1. **세션 번호 NN 확정** — 사용자 지정 또는 폴더 스캔.
2. **대화·작업 내용 수집** — User/Cursor 메시지, TDD Phase, pytest 결과, 변경 파일.
3. **`Report/NN.REPORT.md` 작성** — 아래 보고서 템플릿.
4. **`Prompting/NN.Export-Transcript.md` 작성** — 아래 Transcript 템플릿.
5. **보고 형식**으로 완료 알림 (경로 2개 명시).

---

## Report 템플릿 (`Report/NN.REPORT.md`)

```markdown
# MagicSquare_00 — 세션 NN 보고서

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_00 |
| 세션 | NN — (세션 주제 한 줄) |
| 보고서 생성일 | YYYY-MM-DD |
| 범위 | (예: Harness · .cursorrules · TDD RED) |

---

## 1. 요약

(3~5줄: 이번 세션에서 한 일, 결과, 다음 단계)

---

## 2. 산출물

| 파일 | 설명 |
|------|------|
| ... | ... |

---

## 3. TDD / 작업 기록

| Phase | 내용 | pytest / 결과 |
|-------|------|----------------|
| RED | ... | FAILED — ... |
| GREEN | ... | PASSED — ... |
| REFACTOR | ... | ... |

*(TDD가 없는 세션이면 Mom Test·워크북 등 해당 섹션으로 대체)*

---

## 4. 결정·규칙

- API·도메인 변경 요약 (`.cursorrules` 기준)
- SSOT·10선·incomplete 등 핵심 규칙 한 줄씩

---

## 5. 다음 단계

- (예: GREEN — validate_lines incomplete 구현)

---

## 6. 관련 문서

| 문서 | 경로 |
|------|------|
| Transcript | `Prompting/NN.Export-Transcript.md` |
| 규칙 | `.cursorrules` |
```

---

## Transcript 템플릿 (`Prompting/NN.Export-Transcript.md`)

```markdown
# MagicSquare_00 — 세션 NN Transcript
_Exported on YYYY-MM-DD from Cursor_

---

**User**

(사용자 메시지 요약 또는 원문)

---

**Cursor**

(응답 요약 — Phase, 변경 파일, pytest 결과 포함)

---

**User**

...

---

**Cursor**

...

---

*본 문서는 `Prompting/NN.Export-Transcript.md` — MagicSquare_00 세션 NN 대화 Export입니다.*
```

- **User / Cursor** 블록을 시간순으로 반복.
- 코드·pytest 출력은 fenced block으로 보존.
- `/tdd-red` 등 Command 이름이 있으면 명시.

---

## 보고 형식 (Command 완료 시)

```
## Export 완료

| 종류 | 경로 |
|------|------|
| Report | Report/NN.REPORT.md |
| Transcript | Prompting/NN.Export-Transcript.md |

## 세션 NN 요약
- (한 줄)

## 다음
- (한 줄)
```

---

## 금지

| 금지 | 이유 |
|------|------|
| `NN.*` 형식이 아닌 임의 파일명 | 저장 규칙 위반 |
| Report만·Transcript만 하나만 생성 | Command는 **둘 다** 필수 |
| 대화에 없는 내용 **추측** 기록 | Export는 실제 세션 근거만 |
| git commit / push (명시 없을 때) | `.cursorrules` |

---

## 참조

- SSOT 형식: `Report/05.REPORT.md`, `Prompting/05.Export-Transcript.md`
- Skill: `.cursor/skills/magic-square-docs/SKILL.md` (checklist · templates)
- 기존 예: `Report/04.REPORT.md`, `Prompting/04.Export-Transcript.md`
- 규칙: `.cursorrules`
- TDD: `.cursor/skills/magic-square-tdd/SKILL.md`
