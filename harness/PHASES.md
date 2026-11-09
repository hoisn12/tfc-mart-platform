# Phase별 계획과 품질 게이트

이번 작업은 하네스 구축뿐이다. 아래는 **미래 실행 계획**이다. 기존 Phase 0 설계 초안을 활용하되 승인/실행 완료로 올리지 않는다. PRD §10의 0~6을 유지하고 마스터 프롬프트 §9의 Phase 5 전환은 5 리허설/6 전환 계획으로 분리한다. Product의 bulk는 5에서 완성하며 그 전에는 미완료 의존으로 표시한다.

## 모든 단계의 공통 게이트

- 진입: 사용자 허용 범위, 준비본의 실제 활성화와 runtime smoke, 이전 모든 Phase gate PASS, 입력·파일 잠금·검증 조건 기록.
- 구현 전: 해당 Phase 범위의 OpenAPI+behavior 계약, 구현자 읽기 검토, reliability 검토, 독립 reviewer PASS, 메인 동결·파일별 SHA-256. 그 후만 backend/frontend 병렬 쓰기.
- 종료: 요구사항 추적과 필수 증거 7종(requirements/contract/tests/recovery/rollback/operations/independent_review), 모든 작성 중단, 산출물 스냅샷, 독립 reviewer 판정, check_gate.py 종료0.
- 다음 Phase 배정 전 위 조건을 다시 확인한다. 변경/실패/미실행/증거 누락이면 진입하지 않는다. 중대한 미해결 결함을 “추후 수정”으로 넘기며 PASS하지 않는다.
- Phase 0 증거는 계획/설계의 완전성 검증이다. 실행 테스트를 수행했다고 기록하지 않는다. Phase 1 이후는 현재 범위에 해당하는 실행·실패 주입·복구·롤백 로그가 필요하다.
- 보안·의존성 검사·build/lint/test의 명령과 버전은 실제 저장소와 호환 버전을 확인한 Phase에서 고정한다. 현재 없는 Gradle/npm 명령을 이미 통과한 것으로 쓰지 않는다.

| Phase | 진입/범위 | 역할과 산출물 | 독립 품질 게이트 |
|---|---|---|---|
| 0 Discovery & Contract Baseline | 하네스 활성화/스모크 후, 설계만 수행. 기존 docs 11개 및 U/L/K ID 재검토 | architect: 기능 대응·요구·가정·architecture/ERD/API·ADR. backend/frontend: 읽기 검토. reliability: 테스트/복구/롤백/운영 계획. reviewer: 독립 검증 | 자료/추정/UNKNOWN 구분, U01/04/13/15 등 Foundation 차단 항목의 근거·담당·기한, 레거시 동등성 기준, Phase 1 범위의 OpenAPI+behavior 계약 동결, 장애/복원/원복 계획 추적. 사용자/업무 결정이 필요한 항목 미해결이면 BLOCKED |
| 1 Running Foundation | Phase 0 PASS. 기술 버전/기존 DB/인증·권한·local 경계 확정, Phase 1 계약 재확인 | backend: Java/Gradle/레이어/DB migration/인증·RBAC/health. frontend: AppShell·디자인 시스템·계약 fixture. reliability: local Compose, CI/IaC 예제·health·logging·runbook 초안 | local/fake 전체 기동·빌드/lint/test/CI/보안 검사, 미인증·타마트 거부, migration 재실행/호환성, graceful shutdown·재기동·경보, 이전 앱 원복 및 일회용 DB 백업/복원 스모크. 실발송/운영 연결 차단 |
| 2 Product Vertical Slice | 1 PASS, U05~07과 해당 상품 규칙/계약 확정 | backend: 조회/필터/수정/권한/감사/409. frontend: 목록/Drawer/오류·충돌. reliability: 회귀·부하/오류 주입 | 검색·정렬·서버 페이지네이션·선행0·금액 경계·mart 격리·동시 수정·감사 E2E, 레거시 승인 사례 대응, 네트워크/DB 중단 후 안전 재시도, 호환 schema로 이전 앱 원복. bulk/미확인 업무는 미완료 표시 |
| 3 Image Pipeline | 2 PASS, U08·원본/공개/보존 정책·계약 확정 | backend: storage port/presign/완료 검증/worker. frontend: 상태·fallback. reliability: 비운영 저장소/CDN IaC 예제·주입/runbook | 원본 private·권한·MIME/magic bytes/리소스 한도, 불변키·원본 고정/재업로드·역순 완료, 처리 실패에도 기존 이미지·상품 API 유지, 재처리/경보·대표 포인터 원복·대사. 기존 URL/원본 삭제 금지 |
| 4 Reliable Messaging | 3 PASS, U09/10/16의 정책/멱등/조회/보존·계약 확정. FAKE만 사용 | backend: Outbox/queue/worker/fake/webhook/대사. frontend: 캠페인·접수/전달/UNKNOWN. reliability: 장애 주입·queue/DLQ·sms runbook | DB commit 뒤 게시 중단→복구, 중복/역순 webhook·조기 receipt·worker 종료·429/5xx/timeout UNKNOWN·대사·동의 철회·예약/취소·DLQ 안전 재처리. 자동 타사 failover/즉시 재발송 차단. 중복/유실·로그/알림·앱 원복 증거. 실제 SMS 0건 |
| 5 Bulk/Excel/Hardening/Rehearsal | 4 PASS, U11/12와 실제 남은 업무/보존/부하 프로파일 확정 | architect: 확인 업무만 명세. backend/frontend: preview/confirm/job/부분실패·재개. reliability: 회귀·스캔·부하·복원/전환 리허설 | 선행0·수식/CSV injection·포맷 버전·미리보기 만료/변경 충돌·중복 확정·부분 실패/중단/재개, L-ID별 검증/명시적 범위 합의. 비운영 사본 이관·백업복원·앱 원복/정합성·RTO/RPO 실측. 실제 cloud/AZ/PITR 미실행을 local 결과로 대체하지 않음 |
| 6 Migration Readiness | 5 PASS, U14와 운영 담당자·단일 쓰기·관찰/중단 임계값 확정 | architect: 매핑/cutover/rollback 계획. reliability: 합성/비식별 사본 shadow/대사·리허설. backend/frontend: 결함 수정만 별도 task. reviewer: 운영 인계 검증 | 비운영 단일 쓰기/부수효과 차단·대사 차이0·원복 후 재대사·큐/UNKNOWN 연속성, 합의 SLO/관찰기간 증거, 운영 담당자 인계·미검증 명시. Production 직접 변경은 계속 금지. PASS는 운영 전환 완료가 아님 |

각 Phase의 세부 task는 해당 Phase 진입 시 실제 파일과 테스트 환경을 확인해 분해한다. 보이지 않는 레거시 메뉴/규칙을 만들어 범위를 채우지 않는다. Discovery의 기능 동등성 증거가 부족하면 문서 작성은 가능하지만 관련 기능 구현/후속 gate는 BLOCKED다.

## 필수 안전성 검증표

| 위험 | 검증 기준/증거 | 시점 |
|---|---|---|
| 유실/중복/UNKNOWN | TX·Outbox·재전달·worker 종료·외부 접수 불명·대사·DLQ 시나리오/로그 | 0 계획, 1 경계, 4 실행 |
| 이미지 장애 전파 | 기존 정상/URL 유지, 실패 격리·재처리·포인터 복귀·권한·불변캐시 | 0 계획, 3 실행 |
| 데이터·권한 유출 | mart/role 변조, PII 마스킹, 비밀 분리, private 파일·최소 권한 | 0 계획, 1~6 회귀 |
| 파괴/원복 불가 | migration 호환, 이전 앱 복귀, 비운영 백업 복원·대사·실측 RTO/RPO | 0 계획, 1 스모크, 5~6 종합 |
| 운영 발견 실패 | health/shutdown, 5xx/latency/queue age/DLQ/UNKNOWN/이미지 오류 경보 | 0 계획, 1 기초, 3~6 도메인별 |
| 불완전 완료 보고 | 요구사항↔계약↔테스트↔증거↔독립 판정, NOT_RUN 차단 | 모든 Phase |

## 2026-11-05 별도 허용: Phase 1 UI 프로토타입

사용자의 최신 구체 지시에 따라 frontend-only 로컬 데모 구현을 별도 트랙으로 수행한다. 위 전체 시스템 Phase 0~6의 정의/차단 상태는 변경하지 않는다. UI 트랙은 architect 계약→frontend 구현자 읽기→reliability 안전 읽기→독립 reviewer 계약 검토→메인 동결→frontend 구현→스냅샷→새 독립 reviewer 실제 실행→결과 기록 순서다. backend 구현과 운영 권한은 열리지 않는다. .codex 보호/부재를 우회하지 않고 준비본 지침 기반 collaboration 실행임을 명시한다. 기존 check_gate.py는 그대로 실행하며 실패를 숨기거나 전체 gate PASS로 바꾸지 않는다. UI 완료 판정과 원래 gate 차단은 별도 필드에 보존한다.
