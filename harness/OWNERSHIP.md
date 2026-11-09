# 책임·파일 소유권·산출물

경로는 쓰기 후보일 뿐이다. 정확한 파일별 task와 잠금 없이는 쓰지 않는다. 현재 생성되지 않은 앱 경로는 미래 담당 영역이다.

| 담당 | 실행 시점 | 쓰기 후보 | 산출물·완료 조건 |
|---|---|---|---|
| 메인 Codex | 모든 배정·계약 동결·gate·재개 | AGENTS.md, .codex/**, harness 공통파일/스크립트/state/TASKS/최종 gate, docs/PROGRESS.md, 루트 README/빌드/Compose, 공통 lockfile | 실행 범위·잠금·해시·계약 승인 기록, 독립 판정 취합, gate 검사 통과 후만 상태 전이 |
| architect | Phase 0 및 매 Phase 구현 전/계약 변경 시 | docs/{architecture,data-model,api-spec,requirements,legacy-feature-matrix,assumptions,migration-plan}.md, docs/contracts/**, docs/adr/** | 근거/UNKNOWN·설계·OpenAPI·상태 계약·ADR, 구현자 읽기 검토와 독립 승인 가능한 계약 |
| backend | 계약 전 읽기 검토; 동결 후 Phase 1~5 구현 | backend/** (Gradle/Flyway/내부 테스트/worker 포함) | 구현·계약/단위/통합 테스트·호환 migration·앱 원복 증거, 자기 테스트 통과 |
| frontend | 계약 전 읽기 검토; 동결 후 backend와 병렬 가능 | frontend/** (lockfile/생성 client/브라우저 테스트 포함) | UI/실API 통합·오류/409/접근성/E2E 증거, fixture 완료와 실통합 완료 분리 |
| reliability | 각 Phase 계획·통합/장애 검증; Phase 0은 계획만 | infra/**, .github/workflows/**, tests/system/**, docs/test-plan.md, docs/runbooks/** | local/fake 환경·CI·주입/복구·백업/롤백·안전성 증거, 자기 작성물은 reviewer에게 인계 |
| reviewer | 계약 동결 직전·Phase 종료·수정 후 재검증 | 없음; 판정은 응답 반환, 메인이 보존 | 작성자와 독립된 PASS/FAIL/BLOCKED 및 파일/행·재현·증거·누락, 직접 수정 금지 |

모든 작성 Agent는 메인이 배정한 고유 `harness/reports/phase-N/<task-id>-<agent>.md`만 추가로 쓸 수 있다. 다른 보고서 수정 금지. reviewer 원문 저장은 메인 담당이다.

공통 파일은 두 Agent에 배정하지 않는다. backend 내부 application.yml·테스트는 backend 소유이며 reliability는 제안만 반환한다. frontend 내부 테스트도 frontend 소유다. 공통 Compose/CI 의존 경로 변경은 메인에게 요청한다. 경로를 이동하거나 reviewer에게 수정 권한을 줘서 규칙을 회피하지 않는다.

소유권 이전은 기존 작업 종료/중단 확인→최종 해시·변경 인계→잠금 해제→새 task/소유자 배정 순서다. 충돌 시 어느 쪽도 강제 덮어쓰기/자동 충돌 해결하지 않는다. .codex는 현재 환경에서 보호돼 있으므로 준비본 경로 harness/codex만 편집하며 활성 상태를 거짓 보고하지 않는다.
