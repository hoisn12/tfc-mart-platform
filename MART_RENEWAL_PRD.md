# 마트 통합관리 시스템 리뉴얼 — PRD / 아키텍처 설계 초안

- 작성 기준: 2026-11-03
- 상태: 초안(레거시 기능/실제 트래픽/인프라/발송사 조사 후 확정)
- 제품 목표: **무인·소수 인력 운영 환경에서 안정성이 높은 마트 관리자 시스템**
- 참고 화면: 사용자가 제공한 '상품관리(마트)' 레거시 관리자 스크린샷
- 기술 기준: React + TypeScript / Java + Spring Boot / 관리형 클라우드(AWS 예시)

## 0. 의사결정 원칙

1. **기능 호환 + 안정성 > 화려한 기술 도입 > 디자인 디테일**. 그러나 핵심 사용 흐름은 최신 SaaS 관리자 UX로 재설계.
2. **모듈러 모놀리스 + 헥사고날 구조**. 초기 마이크로서비스/Kafka/Kubernetes/자체 이미지 서버/과도한 Redis 사용 금지.
3. 모든 외부 연동은 Port/Adapter로 교체 가능하게 구성.
4. 네트워크 장애/반복 호출/중복 메시지/작업 재실행을 정상적인 상황으로 취급.
5. DB에는 원본 데이터와 감사 추적을 남기고, 이미지에는 CDN, 대량/외부 작업에는 내구성 있는 큐 사용.
6. 기존 운영 시스템을 한 번에 교체하지 않고 검증·병행·점진적 전환.
7. 사용하지 않는 비즈니스 기능을 지어내지 않음. 불명확한 규칙은 명시적으로 가정/확인 대기 기록.

## 1. 레거시 화면 관찰 기반 기능 인벤토리

> 스크린샷에서 확인되는 UI 중심의 잠정 인벤토리. 실제 DB/프로그램 동작과 대조 필수.

- 전역/사이드바: 관리자, 통합관리, 마트, 상품관리, 결제/배송관리, 회원관리, 상품업로드결과, 미등록상품관리, 엑셀 업로드 설정, 이벤트관리, 혜택관리, 계좌유효성조회, 전산관리, 기타설정 등
- 상품 목록: 행 체크박스, 번호/코드, 마트명, 카테고리(1/2), 바코드, 상품명, 규격, 단가, 세일가, 최소/최대 주문수량, 묶음단위/묶음가격, 저장, 이미지, 변경, 노출, 품절, 무배제외, 인기, 재고관리, 재고/등록/수정 일시 등
- 상단: 검색/필터, 등록/삭제, 노출·품절·인기 일괄 변경, 엑셀 입출력/상품 관련 기능, 페이지네이션
- 특징/위험: 데이터 밀도가 지나치게 높고 항목별 직접 수정 및 저장이 혼재하며, 대량 작업 실패 여부/감사 이력/비동기 처리 상태가 불명확함
- 미확정: 재고관리/주문/결제/배송/이벤트/혜택/회원의 실제 업무 규칙, 문자 발송 목적/종류, 엑셀 포맷, 이미지 원본 위치, API 및 데이터 규모

## 2. 목표 사용자와 핵심 업무

- 시스템 관리자: 전체 마트/권한/설정/운영 상태 관리
- 마트 운영자: 자신에게 허용된 마트 상품·가격·재고·이미지·주문/회원 관리
- 고객지원/메시지 담당자: 승인 범위 내 발송 예약·결과·실패 재처리
- 감사/읽기 전용 관리자: 변경 이력·발송 이력·시스템 상태 조회

### 핵심 업무 시나리오

1. 상품 검색 → 필터/정렬 → 상세 편집 → 유효성 검사 → 저장 → 변경 이력 확인
2. 상품 다중 선택 → 노출/품절/카테고리/가격 등 명시적 일괄 변경 → 미리보기 → 확정 → 성공/실패 목록 확인
3. 엑셀 업로드 → 사전 검증 → 변경 요약 및 오류 행 확인 → 확정 → 비동기 처리 → 결과 파일 다운로드
4. 이미지 업로드 → 처리 중 → 썸네일/원본 변형 생성 → CDN 배포 → 기존 정상 이미지에서 안전하게 교체
5. 업무/광고 문자 발송 등록 → 발송 대상/동의/정책 검증 → 저장/큐잉 → 발송사 접수 → 전달 결과 추적 → 실패/미확정 처리
6. 장애 발생 → 알림 수신 → 자동 재시도/격리/복구 → 운영 대시보드에서 확인

## 3. 화면 구조(정보 아키텍처)

- 대시보드: 오늘 주문/매출/재고 경고/발송 대기/이미지 실패/시스템 상태(허용된 권한 범위)
- 상품관리: 상품 목록, 상품 등록·상세, 카테고리·브랜드, 가격/프로모션, 재고/노출, 이미지, 엑셀 작업
- 주문/배송: 기존 실제 기능 확인 후 상세 명세 수립(상태 변경 및 재처리의 멱등성 필수)
- 회원/고객: 개인정보 접근권한, 검색, 이력; 기존 규칙 유지
- 메시지센터: 템플릿, 단건/대량/예약 발송, 동의/수신거부, 발송이력/실패/미확정 건, 발송사 상태
- 운영관리: 작업 이력, 감사로그, DLQ 관리(안전한 재처리), 시스템 상태, 관리자/마트 권한, 환경 설정
- 리뉴얼 범위 밖의 미확인 메뉴는 '기능 조사 후 후속 단계'로 분리

### 디자인 가이드

- B2B SaaS Admin / 깔끔하고 밀도 높은 라이트 UI, 차분한 뉴트럴 팔레트 + 한 가지 브랜드 강조색; 다크모드 후순위
- 좌측 접이식 내비게이션, 상단 글로벌 검색/마트 전환/알림, 본문 페이지 제목과 주요 액션
- 상품 목록은 2단 툴바: (1) 검색·필터·필터칩, (2) 선택 시에만 표시되는 일괄작업 바
- 테이블은 서버 사이드 페이지네이션/정렬/필터, 고정 주요 열(상품/바코드), 열 표시 설정, 밀도 조절, 가상화(필요 시)
- 인라인 편집은 소수 안전 필드에만; 위험하거나 종속 필드가 많은 수정은 Drawer/상세 편집에서 검증 후 저장
- 일괄 작업은 미리보기(영향 건수/변경 전후) + 확인 + 처리상태/실패행 다운로드
- 반응형: 데스크톱(1280px 이상) 우선, 태블릿 최소 사용성; 모바일은 필수 운영작업 중심
- 키보드 탐색, 포커스 관리, 에러 접근성, 로딩/빈 상태/부분 실패/재시도 표시
- 핵심 디자인 시스템 컴포넌트: AppShell, PageHeader, FilterBar, DataGrid, BulkActionBar, DetailDrawer, StatusChip, ConfirmDialog, JobProgress, AuditTimeline, ImageUploader

## 4. 권장 아키텍처

### 4.1 논리 구조

```
[운영자 Browser: React/TS]
       | HTTPS
[CloudFront/WAF: 정적 FE 배포]              [CloudFront/OAC: 상품 이미지]
       |                                              ^
[ALB/API] -> [ECS Fargate Spring Boot API, 2+ task / Multi-AZ] | 
       |                                   [S3 processed/private originals]
       +--> [RDS PostgreSQL Multi-AZ]
       +--> [S3 presigned upload] ---> [Image Processing Lambda/queue] --+
       +--> [Transactional Outbox] -> [Outbox publisher] -> [SQS]
                                                   |          |
                                         [SMS Worker/Lambda] [Excel Worker]
                                                   |          |
                                           [SMS Provider]  [S3 result]
                                                   |
                                 [Webhook + status reconciliation]
                      
[CloudWatch alarms / centralized logs / backups / IaC / secrets]
```

AWS는 참조 구현. 기존 인프라 재사용 타당성 검증 후 최종 결정. FE CDN과 이미지 CDN은 별도 배포 또는 경로 분리 가능. 모든 운영 DB는 private subnet에 유지.

### 4.2 Java 패키지 구조(기존 대화와 정합)

```
backend/src/main/java/.../
  domain/
    product/ category/ brand/ pricing/ inventory/
    image/ messaging/ importjob/ admin/ audit/
  application/
    port/in/{domain}/...UseCase.java
    port/out/{domain}/...Repository.java
    port/out/messaging/MessageSenderPort.java
    port/out/image/ImageStoragePort.java
    service/{domain}/...Service.java
  adapter/
    in/web/admin/{domain}/...Controller.java
    in/web/webhook/...Controller.java
    out/persistence/{domain}/adapter/...PersistenceAdapter.java
    out/persistence/{domain}/jpa/...JpaRepository.java
    out/persistence/{domain}/entity/...Entity.java
    out/persistence/{domain}/mapper/...Mapper.java
    out/persistence/{domain}/query/...QueryRepository.java
    out/persistence/{domain}/projection/...Projection.java
    out/smsprovider/...MessageSenderAdapter.java
    out/storage/s3/...ImageStorageAdapter.java
  config/
```

- 도메인은 Spring, JPA, HTTP SDK에 의존하지 않음. 외부연동은 Port/Adapter.
- 특정 인터페이스를 불필요하게 중복 추상화하지 않음.
- 사용자별/마트별 범위는 DB 조회·수정·감사로그 모두에서 서버 측 강제.
- 조회 성능을 위해 조회 모델/Projection 사용; 복잡한 목록을 엔티티 전체 그래프로 로딩하지 않음.
- 멀티 모듈 Gradle은 실제 빌드/팀 규모상 필요할 때만; 초기 단일 Spring Boot 모듈 + 도메인별 패키지 권장.

### 4.3 데이터 원칙

- DB: 운영 중 기존 DBMS/스키마 우선 조사; 새 DB를 선택할 수 있으면 PostgreSQL 권장.
- 주요 테이블 후보: mart, admin_user, role/permission, product, product_price, inventory, category, brand, product_image, import_job/import_row, sms_campaign/sms_message/sms_attempt, message_consent, outbox_event, audit_log.
- 가격: 원 단위 정수 또는 금액 VO와 `NUMERIC`(사업 규칙 확인). 부동소수점 금지.
- 시각: UTC 저장, 한국시간 화면 표현/예약 기준 명시.
- 동시 수정: version 컬럼 기반 optimistic locking과 409 충돌 UX.
- 외래키/유니크 제약: `(mart_id, barcode)` 중복 정책 조사 후 제약; idempotency unique key; provider_id 등.
- 삭제: 무조건 물리삭제가 아니라 참조관계/정책 확인 후 soft delete 또는 보존 처리.
- Flyway forward migration, 롤백은 호환형 migration + 애플리케이션 롤백을 원칙으로 함.

## 5. 문자 발송: 안정성과 중복 방지를 동시에

### 5.1 목적과 기능

- 업무용(주문/배송/예약 안내)과 광고용(이벤트/프로모션)은 정책/권한/템플릿을 분리.
- 단건, 대량, 예약 발송; 검수/승인(필요 시), 대상 수·예상 비용 확인, 캠페인 중단/상태 확인.
- 수신거부·동의·야간 발송 규제(광고성 문자), 발신번호 등록·검증, 개인정보 마스킹/보관기간 정책.

### 5.2 기술적 흐름

1. `POST /api/admin/messages/campaigns`: 요청 Idempotency-Key, 권한/마트/법정동의/형식/예산/발송번호 확인.
2. DB 단일 트랜잭션에서 캠페인/수신자별 메시지(상태 PENDING)와 outbox row를 기록. API는 **접수/예약 상태**만 반환하며 전송 성공으로 표현하지 않음.
3. Outbox dispatcher는 아직 게시되지 않은 row를 안전하게 SQS로 전달. 중복 게시는 정상 케이스로 취급하고 컨슈머에서 멱등 처리.
4. Worker는 rate limit/동시성 제한, 재시도 정책, provider request/response 및 correlation ID 저장. 발송사의 idempotency 지원 여부를 조사하여 사용.
5. 상태 예: `PENDING → QUEUED → PROCESSING → ACCEPTED_BY_PROVIDER → DELIVERED | FAILED`; 네트워크 타임아웃 등 결과 불명은 `UNKNOWN`.
6. Webhook 검증(서명/공유비밀/허용 정책/재전송 방지) 및 조회 API를 통한 주기적 대사(reconciliation); 이벤트 중복·역순 도착 허용.
7. 실패는 원인별 분류: 영구 실패(번호/동의/템플릿 문제) 재시도 금지; 일시 오류(429/5xx) backoff+jitter, 한도 초과 후 DLQ+경고.
8. **접수 여부 불명인 타임아웃은 즉시 다른 발송사로 재전송하지 않음**. 먼저 발송사 결과 조회/대사 후 결정. 불확정 상태를 관리자에게 노출.
9. 발송사 교체는 `MessageSenderPort` 구현 교체로 대응; 자동 failover는 중복발송을 방지하는 증거가 확보될 때에만.

> 큐/컨슈머만으로 실제 '정확히 한 번 전송'을 보장할 수 없음. API idempotency + 로컬 중복방지 + 발송사 고유키/조회/대사를 결합하여 가능한 범위까지 중복을 최소화.

- 발송사: SOLAPI / NHN Cloud / 네이버클라우드 등 실제 계약·가격·기능/실패 응답·리포트/웹훅 대사 가능 여부 비교 후 선정.
- 현재 발송 제한은 미확정. 이전 별도 프로젝트의 초당 50건/15분 20,000건 수치는 본 시스템에 자동 적용하지 않음. **발송사 및 업무 정책을 설정값으로 관리**.
- 참조: https://solapi.com/developers/api/webhook / https://solapi.com/developers/api/msg-getList / https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html
- 광고성 발송 법적 검토: https://law.go.kr/LSW/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1025057501

## 6. 상품 이미지: '서빙 서버' 대신 '처리 파이프라인 + CDN'

1. 운영자 UI → API 인증/권한/파일 크기·형식·용도 검증 → 짧은 만료의 **고유 키 presigned upload URL** 생성.
2. 브라우저가 S3 임시/원본 버킷에 직접 업로드. 버킷 public access 차단, overwrite/재사용 키 방지, 업로드 후 서버가 실파일 재검증.
3. 업로드 완료 이벤트 또는 확정 API → SQS/Lambda 처리: magic bytes 검사, 크기/해상도/보안 검증, EXIF 회전·메타데이터 제거, 안전한 JPEG/WebP(필요하면 AVIF) variants 생성 (예: 120/360/800/1200px).
4. 가공 이미지가 완성되고 모든 필수 변형이 확인되면 product_image 상태 `READY`로 전환. 기존 대표 이미지는 새 이미지 `READY` 전까지 그대로 유지.
5. **변경 불가능한 버전 키** 사용: `products/{martId}/{productId}/{assetVersion}/w360.webp`. 수정 시 새 키 생성 + DB 참조 교체. CDN 경로는 이미지 전용 도메인.
6. CloudFront OAC로 private S3 origin 접근. `Cache-Control: public, max-age=31536000, immutable`은 버전 고정된 공개 이미지에만 적용. 개인정보/관리자 이미지에는 공개 캐싱 금지.
7. API는 이미지 byte를 직접 프록시하지 않고 이미지 URL/상태/alt 메타데이터만 제공.
8. React: srcset/sizes, lazy loading, 에러 fallback, 목록 썸네일, 미리보기 및 재처리 안내.
9. 이미지 배치 복구 작업: 기존 이미지 URL 유효성 검사, 누락·깨진 파일, 버전 재생성, 오류 상태/재처리, 캐시 hit/miss·404/403 비율 모니터링.
10. 오래된 이미지 제거는 보존기간·참조·CDN TTL 고려한 안전한 백그라운드 GC로 실행.

- 잘못된 MIME이나 SVG, 악성/초대형 이미지/압축폭탄에 대비한 검증·리소스 한도 필요.
- 이미지 처리 실패가 상품조회/상품수정 API 장애로 전파되면 안 됨.
- 참고: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/UpdatingExistingObjects.html / https://docs.aws.amazon.com/eu_en/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html

## 7. 대량 엑셀 입출력

- 업로드: 인증 URL → 저장소 → 비동기 검증/파싱 → 검증 결과 → 사용자 확정 → 배치 적용(부분 실패 전략 정의) → 작업 상태/결과 보고서.
- 형식 변경 버저닝, 한글/숫자/바코드 앞자리 0 보존, 단가·세일가·품절·재고 상호 검증, 수식/매크로/CSV Injection 방어.
- 대량 변경 이력은 작업 ID + 상품별 상세 기록으로 추적.
- 재요청 중복 처리 방지, 작업 중단/재개, 실패행 재다운로드.
- 외부 발송/이미지/엑셀 작업은 API 동기 요청에서 모두 처리하지 않음.

## 8. 운영 안정성 / 보안 / 관측성

### 초기 목표(SLO 후보 — 실제 규모와 비용 확인 후 확정)

| 대상 | 제안 운영 목표 |
|---|---|
| API 가용성 | 월 99.9% 목표(외부 시스템/계획 정비 범위 정의 필요) |
| API 응답 | 상품 검색 p95 500ms 이내(테스트 데이터 규모·쿼리 조건 확정 후) |
| 발송 요청 유실 | DB에서 '접수 완료' 응답한 유효 요청의 영구 유실 0을 설계·검증 목표로 함 |
| 발송 지연 | 정상 환경의 내부 큐 대기→발송사 접수 p95 60초 이내 목표(물량에 따라 조정) |
| 이미지 | 목록 썸네일 CDN 제공, 처리 실패 시 기존 정상 이미지 유지 |
| 복구 | RTO 1시간 / RPO 15분 이하를 초기 사업 목표로 검토(검증 전 보증 아님) |

### 필수 체크리스트

- 웹/API: 2개 이상의 ECS tasks 및 AZ, readiness/liveness, graceful shutdown, request timeout, connection pool, 재시도/서킷브레이커, 배포 자동 롤백 및 기능 플래그.
- DB: RDS Multi-AZ + 자동 백업/PITR + 복구 리허설, 마이그레이션 보수적 설계, 인덱스/slow query 분석.
- 네트워크/권한: HTTPS, 최소권한 IAM, WAF/레이트리밋, 사용자 세션 보안, RBAC, 관리자 고위험 작업 2차 확인, 비밀정보 Secrets Manager.
- 데이터: 테넌트(mart) 격리, 변경 감사로그(누가/언제/무엇을/기존·변경 값), 개인정보 최소 수집 및 마스킹, 보존/파기 정책.
- 모니터링: API 5xx/latency, ECS 재시작, DB CPU/connections/storage, SQS age/DLQ, SMS accepted vs delivered/failure/unknown, 이미지 처리 실패/403/404/원본 트래픽, 비용 이상 탐지.
- 알림: 운영 담당자 채널로 경고/심각도별 통보; 자동 재시도/복구가 우선이고 수동 작업은 문서화된 runbook으로 제한.
- 정기 보안패치/CI 의존성 검사, 취약 라이브러리 배포 방지, 릴리스별 rollback 테스트.
- RDS Multi-AZ도 장애 시 순간적인 중단이 가능하므로 100% 무중단 보장하지 않음.

## 9. API 초안

```http
GET    /api/admin/marts
GET    /api/admin/products?martId=&q=&barcode=&status=&page=&size=&sort=
POST   /api/admin/products
GET    /api/admin/products/{id}
PATCH  /api/admin/products/{id}        # If-Match/version
POST   /api/admin/products/bulk-jobs    # 미리보기/확정 단계 분리
GET    /api/admin/jobs/{jobId}
POST   /api/admin/import-jobs
POST   /api/admin/import-jobs/{id}/confirm
POST   /api/admin/images/upload-requests
POST   /api/admin/images/{id}/complete
GET    /api/admin/images/{id}/status
POST   /api/admin/messages/campaigns  # Idempotency-Key
GET    /api/admin/messages/campaigns/{id}
GET    /api/admin/messages/{id}/attempts
POST   /api/webhooks/message-provider/{provider}
GET    /api/admin/audit-logs
GET    /actuator/health/readiness
```

API 명세는 OpenAPI로 관리; 표준 오류 응답(필드·사유·traceId), 401/403/404/409/422/429, 명시적인 예외·재시도 가능 여부.

## 10. 구현 우선순위 / 마이그레이션

| 단계 | 내용 | 완료 기준 |
|---|---|---|
| 0. Discovery | 레거시 UI/DB/API/발송사/이미지/엑셀/권한 조사, 기능 대응표, 운영 리스크 | UNKNOWN 목록과 기술 제약/전환 계획 승인 |
| 1. Foundation | React AppShell/Design System, Spring Boot 구조, 인증/RBAC, DB migration, IaC/CI, 로깅/헬스체크 | 배포 가능하고 기본 보안/알림 동작 |
| 2. Product | 조회/필터/정렬, 상세 수정, 대량 작업, 감사 로그, 카테고리/가격/재고 | 레거시 핵심 시나리오 회귀 테스트 통과 |
| 3. Image | presign→처리→CDN, legacy 이미지 이관, 오류/재처리 | 대량 로딩/교체/원본 장애 시나리오 통과 |
| 4. Messaging | Outbox→SQS→발송사→webhook/대사, 예약/광고 동의, 실패 처리/대시보드 | 실패/중복/타임아웃/리포트 누락 주입 테스트 통과 |
| 5. Excel & remaining | 대량 업로드/다운로드, 나머지 확인된 업무 모듈, 성능/보안/운영 리허설 | 병행검증 및 rollback 시나리오 통과 |
| 6. Migration | 레거시 read-only shadow/부분 전환, 데이터 대사, 기능별 cutover, 일정 기간 rollback 가능 유지 | 목표 SLA/오류율/데이터 정합성 확인 |

메시지 발송이 최우선 업무라면 3~4단계의 실제 착수 순서를 앞당길 수 있으며, 안정성 기반(Outbox/Queue/Observability)은 1단계부터 구축.

### 배포/데이터 이행 원칙

- 기존 운영 데이터의 인덱스/업무 규칙/연계 의존성 목록화.
- DB 덤프 또는 CDC, 정합성 대사, 스키마·데이터 매핑 문서, 비가역 변환 금지.
- 병행 기간에는 단일 쓰기 주체 원칙 유지. dual-write가 필요하면 불일치 복구 절차 먼저.
- Feature flag로 마트별/기능별 단계적 개방, 원복 절차 준비, 신규 테이블의 후방 호환 유지.

## 11. Coding Agent 전달물·품질 기준

### 필수 산출물

- `docs/legacy-feature-matrix.md`
- `docs/architecture.md` + Mermaid 구성/시퀀스 + ADRs
- `docs/requirements.md` + API/UI 상태 정의
- `docs/data-model.md` + ERD/Flyway 스키마
- `docs/migration-plan.md` + 기능별 cutover/rollback
- `docs/runbooks/{sms,image,db,deploy}.md`
- `docs/test-plan.md` + 실패 주입 시나리오
- `frontend/`, `backend/`, `infra/` 및 CI workflow

### 인수 기준(최소)

1. 상품 조회/수정/일괄 수정과 관리 권한이 E2E 테스트로 검증된다.
2. 상품 이미지 갱신 시 새 버전은 생성되고, 이전 URL은 오류 없이 기존 이미지를 계속 제공한다(삭제 정책 전).
3. 이미지 처리 Lambda가 실패해도 API/기존 이미지는 정상이며, 재처리 및 알림이 가능하다.
4. DB commit 이후 SQS 게시 실패를 주입해도 Outbox 대기 작업이 추후 전달된다.
5. SQS 중복 배달, 웹훅 중복/역순, 발송사 타임아웃, 429, 5xx, DLQ 상태를 테스트한다.
6. 발송사 접수와 단말 전달을 분리해 UI/DB에 표현하고 미확정 상태를 대사한다.
7. RDS·API 가용 영역 장애, 이전 버전으로 배포 복구, 백업 복원을 적어도 테스트 환경에서 리허설한다.
8. 운영자가 실패 원인·재시도 정책·감사이력을 대시보드에서 확인할 수 있다.
9. 모든 CI 테스트, 정적 검사, 보안 검사, 빌드가 통과한다.

## 12. Discovery 단계에서 반드시 확인할 질문(답 없이도 설계 진행, 불명확하면 가정 명시)

1. 레거시 코드와 DB 접근 가능 여부/DB 종류/데이터량/스키마.
2. 마트 수·상품 수·동시 사용자 수·시간당 이미지 요청·엑셀 최대 행 수.
3. 기존 호스팅 환경, 장애 이력, 이미지 문제 유형(404/느림/깨짐/핫링크/중복 업로드/캐시 갱신 실패).
4. 문자 목적(SMS/LMS/MMS/알림톡/광고), 기존 발송사, 일/분당 전송량, 수신 거부와 동의 관리 방법.
5. 주문/배송/회원/정산/결제/재고 시스템과의 연동 여부.
6. 기존 스프레드시트 규격, 바코드·상품 코드·마트별 가격 정책.
7. 실제 운영 예산, 허용 정지시간, RTO/RPO 기대치, 알림을 받을 운영 담당자.

---

## 참조 링크

- Spring Boot system requirements: https://docs.spring.io/spring-boot/system-requirements.html
- React versions: https://react.dev/versions
- CloudFront OAC: https://docs.aws.amazon.com/eu_en/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html
- CloudFront file versioning: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/UpdatingExistingObjects.html
- SQS/Lambda idempotency: https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html
- SOLAPI webhook: https://solapi.com/developers/api/webhook
- 정보통신망법 제50조: https://law.go.kr/LSW/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1025057501
