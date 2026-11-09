# 마트 리뉴얼 공통 작업 규칙

## 목적과 현재 범위

Java 21 / Spring Boot + React / TypeScript 마트 통합관리 시스템을 리뉴얼한다. 기능 호환성, 데이터 정합성, 무인 운영 안정성을 우선한다. 기본 명세는 `MART_RENEWAL_PRD.md`, `MART_CODING_AGENT_PROMPT.md`이며 기존 docs 설계를 함께 읽는다. 최신 사용자 지시가 우선한다.

현재 허용 범위는 **하네스·에이전트 설정·규칙·Phase 계획**이다. 앱 구현, 의존성 설치, 서비스 기동, DB 변경, 인프라 적용은 시작하지 않는다. 별도 Phase 실행 지시가 있어야 해당 범위를 연다. 기존 Phase 0 문서는 승인·검증 완료가 아니다.

## 필수 안전 규칙

- Production 직접 변경 금지. 운영 배포·SQL·클라우드 적용·실계정/유료 리소스 생성 금지. Phase 6도 계획과 비운영 리허설까지만 허용한다.
- 실제 SMS 발송 금지. FAKE provider와 합성 수신자만 사용한다. UNKNOWN 접수 결과는 조회·대사 전 재발송/타 발송사 failover하지 않는다.
- 기존 데이터 삭제 금지. 파괴적 migration·기존 이미지 GC·볼륨 삭제·이력 유실 금지. 출처를 입증한 격리된 일회용 테스트 자료만 정리할 수 있다.
- 비밀값/PII/운영 덤프를 코드·프롬프트·로그·보고서에 넣지 않는다. 실행 대상이 local/test이고 가짜 자격증명인지 확인한다. 대상 불명이면 실행하지 않는다.
- 중요 구조·DB·트랜잭션·외부 연동·인증·테넌트·API 호환 변경은 `docs/adr/`에 대안/근거/영향/복구 방안을 담은 ADR부터 작성한다. 기존 architecture.md의 ADR 001~008은 초안으로 보존하고 새 번호는 009부터 사용한다.
- 검증 실패/미실행/증거 부족이면 다음 Phase 진입 금지. 미완료 기능, FAKE/local 검증을 기능 완료나 운영 검증으로 보고하지 않는다.
- Agent 간 동일 파일 동시 수정 금지. 소유 경로 안에서도 메인이 배정한 정확한 파일 목록과 활성 잠금이 있어야 수정한다.

## 공통 기술 기준

모듈러 모놀리스+헥사고날 구조, 순수 domain, 외부 Port/Adapter와 local fake를 유지한다. 초기 MSA/Kafka/Kubernetes/자체 이미지 서버/근거 없는 Redis 금지. 기존 DB 조사 우선, 신규 DB 허용 시 PostgreSQL 검토. 금액 부동소수점 금지, 바코드 문자열·선행 0 보존, UTC 저장/KST 표시, 서버 측 mart 권한, 낙관적 잠금, 감사 이력 필수.

SMS는 업무+Outbox 단일 DB TX, 내구 큐, 멱등 소비, 접수/전달/UNKNOWN 구분과 대사를 요구한다. 이미지는 private 원본+CDN 변형+불변키이며 새 READY까지 기존 정상 이미지를 유지한다. 대량/엑셀은 검증→미리보기→확정→비동기 처리→부분 실패/재개를 따른다. 미확인 규칙은 `docs/assumptions.md`에 영향·확인 방법과 함께 기록한다.

## 메인 Orchestrator와 전문 Agent

메인 Codex만 Orchestrator를 맡고 여섯 번째 Custom Agent를 만들지 않는다. Phase 실행 시 `.codex/agents/`의 architect/backend/frontend/reliability/reviewer를 명시적으로 골라 위임한다. 상세 책임은 각 TOML과 `harness/OWNERSHIP.md`를 따른다. 전문 Agent의 재위임은 금지한다. 동시 슬롯이 부족하면 순차 실행한다.

메인만 `docs/PROGRESS.md`, `harness/state.json`, `harness/TASKS.md`, 최종 gate를 수정한다. 공통 설정·원본 명세·루트 파일도 메인이 취합한다. 전문 Agent는 자기 보고서만 작성한다. reviewer는 모든 대상에 읽기 검증만 하고 판정을 응답으로 반환하며 메인이 원문을 보고서에 저장한다.

## Phase 실행과 독립 검증

1. PROGRESS/state/TASKS/PHASES와 이전 gate·입력 해시를 확인한다. 재개 시 실행 중 작업과 변경 파일부터 대사한다.
2. 메인은 task ID, Phase, 입력/계약 해시, 정확한 쓰기 파일, 완료 조건, 검증 명령, 고유 보고서 경로를 기록하고 잠금을 배정한다.
3. 각 구현 Phase마다 architect 계약 작성→backend/frontend 읽기 검토→reliability 안전 검토→독립 reviewer 검토→메인 동결 순서다. 승인된 OpenAPI·UI 상태·오류·권한·멱등성 계약 SHA-256을 task에 고정한 후에만 Backend와 Frontend를 병렬 구현한다. 기존 API 초안은 승인 계약이 아니다.
4. 계약 변경 시 두 구현자의 작업/잠금을 멈추고 architect에게 변경 요청한다. 수정→독립 재검증→해시 갱신 후 재배정한다.
5. 작업자는 자기 테스트와 실제 명령·종료 코드·증거를 보고한다. 모든 쓰기를 멈추고 스냅샷을 고정한 뒤 작성에 참여하지 않은 reviewer의 새 검증 작업에서 독립 판정을 받는다. reliability는 자기 산출물을 독립 승인하지 않는다.
6. 메인이 `python3 harness/scripts/validate.py`, `python3 harness/scripts/check_gate.py --phase N`을 실행한다. 독립 PASS와 필수 증거를 모두 충족할 때만 해당 Phase를 PASS로 기록한다. 이후 Phase 시작도 사용자가 허용한 실행 범위 안에서만 가능하다.

상태·인계·충돌·재개는 `harness/PROTOCOL.md`, 계획과 게이트는 `harness/PHASES.md`, 프롬프트는 `harness/prompts/`를 따른다. 이들은 저장소 작업 규약이다. Codex의 자동 스케줄러/파일 ACL이 아니다. Agent TOML로 독립 sandbox/approval 권한을 만든다고 가정하지 않는다. 부모 세션·관리 정책과 연결 도구 권한을 상속하며 이를 확대하지 않는다.

## 품질과 한국어 보고

각 Phase에서 요구사항 추적, 계약·단위·통합·E2E 테스트, 장애 복구, 롤백, 보안·운영 안전성을 검증한다. Phase 0은 실행 환경 대신 검증 계획의 완전성·안전성·추적성을 평가한다. 이후 실행 테스트를 계획서로 대체하지 않는다. 성능/SLO/RTO/RPO는 목표와 조건부 실측을 구분한다.

진행 원장은 `docs/PROGRESS.md` 하나다(원본 프롬프트 소문자 경로보다 최신 사용자 지시 우선). 모든 보고는 한국어. `harness/reports/phase-N/<task-id>-<agent>.md`에 PASS/FAIL/BLOCKED/NOT_RUN, 변경·명령·종료 코드·로그·입력 해시·미완료·가정·위험을 기록한다. gate.json은 메인이 작성한다. 실패 이력은 덮어쓰지 않고 새 시도 보고서를 추가한다.
