# Boss Reads This

한국어 업무 문서를 쓰고 고치는 Claude Code 스킬입니다. 독자부터 정합니다. 문서 종류와 작성자까지 정한 뒤 형식을 고르고, 번역투, AI 관용구, 피동 남발, 어려운 단어는 쓰는 단계에서 걸러 냅니다.

## 설치

Claude Code 세션에서 아래 두 줄을 실행합니다.

```
/plugin marketplace add jinieeee/boss-reads-this
/plugin install boss-reads-this@boss-reads-this
```

- 업데이트는 `/plugin marketplace update boss-reads-this`를 실행한 뒤 `/plugin update boss-reads-this`를 실행합니다.
- 제거는 `/plugin uninstall boss-reads-this`로 합니다.

플러그인 대신 저장소를 직접 쓰려면 클론한 뒤 `install.sh`를 실행합니다. `~/.claude/skills/writing`에 심볼릭 링크를 걸기 때문에 저장소를 고치면 바로 반영됩니다.

```bash
git clone https://github.com/jinieeee/boss-reads-this.git
cd boss-reads-this
./install.sh
```

두 방법 중 하나만 씁니다. 둘 다 설치하면 같은 스킬이 두 번 잡힙니다.

## 쓰는 법

"보고서 써줘", "이 메일 다듬어줘", "회의록 정리해줘"처럼 요청하면 스킬이 불립니다. 이름으로 부르려면 플러그인은 `/boss-reads-this:writing`, 직접 설치는 `/writing`을 입력합니다.

한국어 문서를 쓸 때마다 이 스킬을 먼저 부르게 하려면 `~/.claude/CLAUDE.md`에 아래 줄을 넣습니다.

```markdown
한국어 문서를 쓰거나 고칠 때는 항상 `writing` 스킬을 먼저 불러서 따른다.
```

## 다루는 문서

| 문서 | 기본 독자 |
|---|---|
| 기획서, 보고서, 제안서 | 임원·결정권자 |
| 장애 보고서 | 임원·결정권자, 같은 팀 개발자 |
| 회의록, 회고 | 다른 직군 동료 |
| 메일·공지 | 받는 사람 |
| 기술·스터디 문서 | 신규 입사자·학습자 |
| 사용 가이드·매뉴얼 | 고객·외부 |
| 인프라 문서, SB Description | 같은 팀 개발자 |

컨플루언스 페이지는 위 문서 중 하나로 보고 패널, 링크, 코드 블록 규칙을 더 적용합니다.

## 구성

| 파일 | 내용 |
|---|---|
| `skills/writing/SKILL.md` | 상황 파악, 형식 결정, 작성, 자가 점검의 네 단계 |
| `references/doc-types.md` | 문서 종류별 형식표와 기본 독자 |
| `references/readers.md` | 독자별 분량, 용어 수준, 결론 위치 |
| `references/roles.md` | 작성자 직군별 기준 |
| `references/style-rules.md` | 단어 선택, 문장 리듬, 기술 용어가 많은 글 |
| `references/banned-phrases.md` | 쓰지 않는 표현 |
| `scripts/check.py` | 금지 표현, 피동, 문장 길이, 줄표를 잡는 점검 스크립트 |

점검 스크립트는 Python 3 표준 라이브러리만 씁니다.

```bash
python3 skills/writing/scripts/check.py 초안.md
```

## 라이선스

MIT. 출처를 남기면 복사, 수정, 재배포, 상업적 사용 모두 할 수 있습니다. 자세한 조건은 [LICENSE](LICENSE)에 있습니다.
