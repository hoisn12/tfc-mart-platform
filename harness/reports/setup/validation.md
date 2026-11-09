# 하네스 구축 검증 보고

기준일: 2026-11-05. 담당: 메인 Codex Orchestrator. 범위: 하네스·설정·규칙·Phase 계획. 비즈니스 기능, Phase 0 재실행, 의존성 설치, SQL, 서비스/인프라 기동은 수행하지 않았다.

판정: **준비본 설정·하네스 검사 PASS / 프로젝트 활성화 BLOCKED / 실제 Custom Agent 호출 NOT_RUN**.

프로젝트의 .codex는 환경에서 읽기 전용 보호 경로로 지정됐다. 절대 경로로 설정 쓰기를 시도했으나 자동 승인 검토에서 “writing outside of the project; rejected by user approval settings”로 거부됐다. AGENTS.md 같은 일반 프로젝트 파일은 작성 가능했다. 보호 경로를 우회하지 않고 harness/codex에 실제 설치할 설정 6개를 준비했다. 사용자가 쓰기 가능한 환경에서 activate.py를 실행해야 요청한 .codex 경로가 생성된다. 현재 요구사항 중 **.codex 설치 및 실제 작동 검증은 미완료**다.

| 검증 | 명령/방법 | 결과·실제 종료 코드 |
|---|---|---|
| TOML/최소 standalone 스키마·규칙 구조 | python3 harness/scripts/validate.py | PASS, 0. 설정 1개+Agent 5개 |
| 메인 설정의 Codex 네이티브 strict 검증 | 위 스크립트가 격리 CODEX_HOME에서 codex app-server --strict-config --print-startup-config 실행 | PASS, CLI 0.166.0, 0. 모델 호출 없음 |
| 지원하지 않는 키 거부 | 일회용 설정에 unsupported_harness_phase 추가 후 strict parser 실행 | 의도한 거부 확인, 1. 실제 설정에 해당 키 없음 |
| 실제 프로젝트 활성 파일 검사 | python3 harness/scripts/validate.py --active | BLOCKED, 1. .codex 파일 없음 |
| Phase 0 조기 진입 차단 | python3 harness/scripts/check_gate.py --phase 0 | BLOCKED, 1. 활성화/실호출 미완료 |
| 게이트 안전성 테스트 | python3 -B -m unittest discover -s harness/tests -v | PASS, 18개, 0. 합성 fixture는 임시 경로만 사용 |
| Python/마크다운 | Python AST, 신규 Markdown 및 docs README 로컬 링크/코드 펜스 검사 | PASS. Python 구문과 로컬 문서 경로 검사 |
| 원본 보존/구현 범위 | baseline.json SHA-256 비교 및 경로 확인 | 원본 14개 중 12개 동일. 예정된 README 링크·progress 통합만 변경. backend/frontend/infra 미생성 |
| Custom Agent 등록·실제 spawn | 실행 안 함 | NOT_RUN. 현재 일반 협업 하위 Agent 독립 리뷰와 구분 |
| 앱 build/E2E/DB 복원·cloud/AZ/운영 테스트 | 실행 안 함 | NOT_RUN. 앱/실행 환경이 없고 현재 범위 밖 |

테스트는 미활성·실패 선행 Phase·NOT_RUN·범주 누락·자기 승인·계약 미동결/누락·구현물 누락·원본/증거/보관본 변경·경로 탈출·리뷰 재사용·미해결 항목의 차단을 확인했다. 다음 Phase의 승인된 문서 진화가 과거 보관본을 손상하지 않는 정상 경로도 확인했다. 실제 구현 성공을 뜻하는 테스트가 아니다.

구축 중 첫 13개 테스트 통과 후 계약/시도별 보관본 검사를 추가했다. 확대 검사에서 경로 탈출 테스트의 fixture 목록이 불완전해 다른 차단 분기에서 17 PASS/1 FAIL이 발생했다. fixture를 보완한 최종 검사에서 18개가 통과했다. 실패를 기능 완료로 보고하거나 Phase gate에 반영하지 않았다.

실행 로그·종료 코드·해시는 [checks.json](checks.json), 원본 해시는 [baseline.json](baseline.json)에 보존했다. 독립 리뷰의 원문은 independent-review.md에 별도 저장한다. 이 리뷰는 일반 협업 하위 Agent가 수행하는 준비본 검토이며 프로젝트 Custom Agent runtime 검증이 아니다. 최종 검토 입력은 review-manifest.json에 고정한다.

## 생성·수정 파일

```text
AGENTS.md
docs/PROGRESS.md                 # 기존 progress.md 이력 보존·통합
docs/README.md                   # 진행 기록 링크 갱신
harness/
  README.md
  OWNERSHIP.md
  PROTOCOL.md
  PHASES.md
  GATE_RECORDS.md
  TASKS.md
  state.json
  codex/                        # .codex 설치 준비본
    config.toml
    agents/{architect,backend,frontend,reliability,reviewer}.toml
  prompts/{phase-0,harness-smoke}.md
  templates/{task,report}.md
  templates/gate.json
  scripts/{activate,validate,check_gate}.py
  tests/test_gate.py
  reports/setup/
    baseline.json
    checks.json
    review-manifest.json
    validation.md
    independent-review.md
    staged-validation.log
    active-validation.log
    phase-0-block.log
    gate-tests.log
    native-unknown-key.log
```

Phase별 harness/reports/phase-N/은 해당 실행 때 생성한다. 가짜 완료 보고서나 gate는 만들지 않았다. 원본 PRD/마스터 프롬프트·이미지·다른 기존 설계는 수정하지 않았다. Git 저장소가 없어 커밋·브랜치·Git 롤백 검증은 수행하지 않았다.

## 책임·협업·품질 기준

메인만 실행 범위·task/잠금·계약 동결·최종 gate·원장을 관리한다. architect는 설계/계약/ADR, backend는 서버/DB/내부 테스트, frontend는 UI/client/E2E, reliability는 infra/CI/통합 장애·복원/runbook을 담당한다. reviewer는 작성에 참여하지 않은 새 작업에서 읽기 검증만 하며 판정을 반환한다.

정확한 파일 잠금→계약 작성/읽기 검토→독립 승인/해시 동결→Backend/Frontend 병렬 구현→모든 쓰기 종료→시도별 스냅샷/증거→독립 reviewer→gate 검사 순서다. 계약 변경 시 구현을 멈추고 재동결한다. 실패/미실행/필수 UNKNOWN은 다음 Phase를 차단한다.

모든 Phase는 요구·계약·테스트·장애 복구·롤백·운영 안전성·독립 리뷰 증거를 요구한다. 0 조사/계약, 1 기반, 2 상품, 3 이미지, 4 메시징, 5 엑셀/강화/리허설, 6 비운영 이행 준비로 구성했다. Production 직접 변경과 실제 SMS, 기존 데이터 삭제는 모든 Phase에서 금지다. 중요 변경은 ADR부터 작성한다.

## 실제 작동 확인과 다음 지시

1. 권한 있는 사용자 터미널에서 python3 harness/scripts/activate.py 실행(기존 파일 자동 덮어쓰기 금지).
2. python3 harness/scripts/validate.py --active로 파일 일치 확인 후 새 Codex 프로젝트 세션 열기.
3. harness/prompts/harness-smoke.md로 정확한 5개 Custom Agent 호출과 결과 회수·역할 규칙·독립 판정 확인. 성공한 경우에만 state.setup 활성화/런타임/증거 해시 갱신.
4. 별도 실행 지시로 [Phase 0 프롬프트](../../prompts/phase-0.md)를 사용. Phase 0 gate PASS 전 Phase 1 진입 금지.

공식 설정 근거는 [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)다. 작업 소유권과 gate는 저장소 규약이며 OS ACL/자동 스케줄러가 아니다. 네이티브 parser 통과만으로 프로젝트 신뢰·관리 정책·독립 Agent 파일 runtime 로딩을 보장하지 않는다.
