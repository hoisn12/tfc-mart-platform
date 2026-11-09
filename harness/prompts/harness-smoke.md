# 하네스 실제 호출 스모크

활성화 후 새 프로젝트 세션에서 실행한다. 비용이 발생하는 실제 모델 위임이며 정적 설정 검증과 별개다.

```text
하네스 호출만 검증하고 Phase 0과 앱 구현은 시작하지 마라.
AGENTS.md와 harness/README.md를 읽고 python3 harness/scripts/validate.py --active를 실행하라.
메인 Codex가 정확한 custom agent 이름 architect, backend, frontend, reliability, reviewer를 한 개씩 순차 호출하라. 각각 새 읽기 전용 작업에서 자신의 역할, 허용/금지 파일, 실행 시점, 계약 전 구현 금지, 실SMS/운영/기존 데이터 삭제 금지 규칙을 응답으로 반환하게 하라. 어떤 Agent도 파일을 수정하거나 서비스/외부 API를 실행하지 않게 하라.
각 세션의 실제 선택된 Agent 이름과 thread/task ID, 역할 규칙을 메인이 대조하라. generic agent에게 역할을 말로 부여한 것은 custom agent 로딩 검증으로 인정하지 마라. 역할 선택이 노출되지 않거나 이름을 호출할 수 없으면 NOT_RUN/BLOCKED로 기록하라.
reviewer에게 앞 네 응답과 준비/활성 파일 동일성·호출 기록을 읽기 검토하게 하라. 실패 시 중단하고 대체 Agent로 숨기지 마라.
메인만 harness/reports/setup/runtime-smoke.md에 명령·종료 코드·Agent/thread ID·각 결과·독립 판정을 저장하라. --active 성공이면 setup.activation을 ACTIVE로, 다섯 custom 역할 호출 및 reviewer 검증 모두 성공이면 setup.runtime_smoke를 PASS로 기록하라. runtime-smoke.md를 확정한 뒤 setup.runtime_evidence에 {"path":"harness/reports/setup/runtime-smoke.md","sha256":"해당 파일의 실제 SHA-256"}를 등록하라. 보고서를 바꾸면 해시도 다시 검증하라.
runtime_smoke PASS, --active 검사 PASS와 독립 구축 리뷰까지 충족한 경우에만 setup.status를 PASS로 바꿔라. 실패면 BLOCKED를 유지한다. setup.config_location도 .codex로 바꿔라. 이 결과는 실제 앱 기능 검증이나 Phase 0 완료가 아니다. 한국어로 보고하라.
```
