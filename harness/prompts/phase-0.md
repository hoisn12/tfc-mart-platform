# Phase 0 실행 프롬프트

아래 전체를 프로젝트 루트의 새 Codex 세션에 전달한다. 하네스 활성화·스모크가 선행돼야 한다.

```text
메인 Codex가 Orchestrator로 Phase 0만 수행하라. AGENTS.md, 두 MART 원본 명세, 기존 docs 설계, docs/PROGRESS.md, harness/README.md·OWNERSHIP.md·PROTOCOL.md·PHASES.md·state.json·TASKS.md를 읽어라. 기존 설계는 초안이며 Discovery 승인 완료로 간주하지 마라.

먼저 python3 harness/scripts/validate.py --active를 실행하고 실제 Custom Agent 스모크 PASS 증거를 확인하라. 준비본만 있거나 정확한 이름의 역할을 호출할 수 없으면 BLOCKED로 기록하고 중단하라. 일반 Agent로 조용히 대체하지 마라.

Phase 0 범위에서 architect, backend, frontend, reliability, reviewer를 명시적으로 사용하라. 메인만 task·파일 잠금·상태·진행 원장·최종 gate를 관리한다. 동시 슬롯 3 이하로 순차/교대 배정하고 재위임은 금지한다. 계약 전 backend/frontend는 읽기 검토만 한다.

1. architect에게 기존 분석/기능 대응/요구/가정/architecture/ERD/API/전환 계획과 ADR 초안을 재검토하게 하라. 사실·제안·UNKNOWN을 분리하고 U/L/K ID를 유지하라. 필요한 정확한 docs 파일만 잠금 배정하라.
2. Foundation에 필요한 API 범위의 OpenAPI와 behavior 계약을 docs/contracts/에 작성하게 하라. 요청/응답/상태/오류/권한·mart 격리/멱등성·버전 충돌·재시도/fake 경계를 포함하라. 중요한 변경은 ADR 009 이후 별도 문서로 기록하라.
3. backend와 frontend에게 순차 또는 읽기 병렬 계약 검토를 맡겨 구현/소비 가능성과 UI 실패 상태 누락을 반환받아라. 앱/빌드/의존성을 생성하지 마라.
4. reliability에게 docs/test-plan.md와 안전한 실행/장애 주입/복구·복원/앱 롤백·운영 안전성 계획을 검토하게 하라. 해당 docs 파일만 배정하라. 운영·외부 서비스·SQL·실제 SMS는 실행하지 마라.
5. 작성 종료와 잠금 해제를 확인해 산출물 파일별 SHA-256을 고정한 뒤, 작성에 참여하지 않은 새 reviewer 검증 작업으로 독립 검토하라. reviewer는 읽기 검사만 하고 직접 수정하지 않는다. 실패는 원소유자가 수정하고 새 스냅샷으로 재검증한다.
6. 메인은 보고서·원문·해시를 harness/reports/phase-0/에 저장하라. 필수 항목을 충족할 때만 계약을 동결하고 gate.json을 작성한 뒤 python3 harness/scripts/check_gate.py --phase 0을 실행하라. 통과 시 state/PROGRESS를 갱신한다.

레거시 코드·DB·한글 화면·인증·물량·예산 등 필수 결정이 없으면 안전한 설계 범위만 진행하고 해당 gate는 BLOCKED로 남겨라. 문서가 있다는 이유로 승인·테스트 완료로 보고하지 마라. Phase 0 테스트 증거는 계획 검증이며 실행 테스트로 표현하지 마라.

이번 실행에서 Phase 1 또는 비즈니스 기능 구현을 시작하지 마라. Production 직접 변경·실SMS·기존 데이터 삭제 금지다. 최종 보고는 한국어로 변경/계약/독립 판정/실행 명령·결과/미완료·차단/다음 조건을 정리하라.
```
