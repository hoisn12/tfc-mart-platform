# API 명세 초안

신규 계약 제안이며 기존 API 호환은 미확인이다. 기본 경로 `/api/admin`, JSON, 인증 필수, 모든 리소스에서 마트 범위를 서버가 강제한다. 구현 시 OpenAPI와 계약 테스트로 관리한다.

## 공통 계약

- ID는 불투명 문자열(UUID 후보), 금액은 `{"amount":"1200","currency":"KRW"}`, 바코드는 문자열, 시각은 UTC RFC3339다. 예약 UI는 KST를 명시한다.
- 목록은 `items,page,size,totalElements`. page=0, 기본 size=20/최대100을 제안한다. 정렬은 허용 목록과 id 보조 정렬을 적용한다. 대용량 커서는 필요 시 별도 계약으로 추가한다.
- 수정은 version 필수, 충돌409, 누락422. 초기 계약은 body version을 사용하고 If-Match를 중복 요구하지 않는다.
- 부수효과가 있는 POST는 Idempotency-Key 필수. actor/mart/operation 범위와 request hash 저장. 같은 요청 재전송은 같은 리소스/결과, 다른 payload로 같은 키 재사용은409. 보존기간은 U16에서 확정한다.
- 오류: 401 미인증, 403 작업 권한 없음, 404 없음/범위 밖, 409 버전·상태·키 충돌, 422 입력·동의·정책 오류, 429 제한, 503 일시 불가. 가능하면 Retry-After 제공.
- 오류 본문 예: `{"code":"VERSION_CONFLICT","message":"다시 읽고 변경을 확인하세요","fieldErrors":[],"traceId":"opaque","retryable":false}`. SQL·개인정보는 반환하지 않는다.
- 비동기 접수는202+리소스/작업ID. 접수를 외부 전달 성공으로 표시하지 않는다. 결과 파일은 scope 재검증 뒤 짧은 만료 URL을 제공하며 공개 캐시 금지.

## API 목록

| Method/Path | 입력·행위 | 성공/권한 후보 |
|---|---|---|
| GET /marts | 허용 마트만 조회 | 200 / 인증 |
| GET /products | martId,q,barcode,categoryId,exposed,soldOut,popular,page,size,sort | 200 / product.read |
| POST /products | martId,barcode,name,확인된 속성·금액 | 201 / product.write+key |
| GET /products/{id} | 상세,version,이미지 상태 | 200 / product.read |
| PATCH /products/{id} | version,changes,변경 사유 | 200+새version / product.write |
| GET /categories | martId,계층 조회 | 200 / product.read; 계층 규칙 확인 필요 |
| POST /products/bulk-jobs | martId,명시적productIds,operation,changes | 202 VALIDATING / product.write+key |
| GET /jobs/{jobId} | 상태·건수·미리보기·행 오류 | 200 / job.read |
| POST /jobs/{jobId}/confirm | previewToken,version | 202 QUEUED / job.confirm+key |
| POST /jobs/{jobId}/cancel | version,reason | 202 CANCEL_REQUESTED / job.cancel+key |
| GET /jobs/{jobId}/results | 성공/실패/충돌행 다운로드 URL | 200 / job.read |
| POST /import-jobs | martId,templateVersion,fileName,size,checksum | 201 업로드 정보 / import.write+key |
| POST /import-jobs/{id}/complete | 파일 고정 후 비동기 검증 | 202 / import.write+key |
| POST /import-jobs/{id}/confirm | 공통job confirm과 같은 계약 | 202 / job.confirm+key |
| POST /export-jobs | martId,filters,columns | 202 / product.export+key |
| POST /images/upload-requests | martId,productId,fileName,contentType,size,checksum | 201 assetId/uploadURL/expiry / image.write+key |
| POST /images/{id}/complete | checksum,원본 고정,desired 이미지 갱신 | 202 / image.write+key |
| GET /images/{id}/status | state,variants,failure,active 여부 | 200 / product.read |
| POST /images/{id}/retry | version,reason | 202 / image.retry+key; 부적합 원본은 재업로드 |
| POST /messages/campaigns/preview | martId,purpose,sender,template,targetSnapshot,scheduledAt | 202 검증job / message.send+key |
| POST /messages/campaigns | previewToken,version | 202 캠페인ID/준비·예약 상태 / message.send+key |
| GET /messages/campaigns/{id} | 준비/접수/전달/실패/UNKNOWN 건수 | 200 / message.read |
| GET /messages | campaignId,state,page,size | 200 / message.read, 전화번호 마스킹 |
| POST /messages/campaigns/{id}/cancel | version,reason | 202 / message.cancel+key |
| GET /messages/{id}/attempts | 마스킹된 시도·상관ID | 200 / message.read |
| POST /messages/{id}/reconcile | reason; 조회만 수행, 즉시 재발송 금지 | 202 / message.reconcile+key |
| GET /audit-logs | martId,target,actor,from,to,page,size | 200 / audit.read |
| POST /operations/dlq-replay-previews | queueType,대상IDs,reason | 202 검증job / operations.replay+key |
| POST /operations/dlq-replays | queueType,대상IDs,reason,previewToken | 202 / operations.replay+key; 상태·접수 증거 재검증 |

import confirm은 PRD 경로를 유지하는 용도별 별칭이며 공통 job confirm 유스케이스에 위임한다. 초기 일괄 변경은 명시적 ID만 받는다. 검색 결과 전체 선택이 필요하면 대상 스냅샷 계약을 추가한다. DELETE, 재고 차감, 주문/회원/결제 API는 업무 확인 전 확정하지 않는다.

관리자 외 진입점: `POST /api/webhooks/message-provider/{provider}`는 발송사 인증과 영속 receipt 저장 뒤200, 저장 실패 시5xx로 재전송을 유도한다. 서명 오류401/403, 형식 오류400. `GET /actuator/health/readiness` 등은 내부 감시 경로로 제한한다.

## 대표 요청·응답

상품 수정 요청:

```json
{"version":7,"changes":{"name":"상품명","exposed":true},"reason":"표시 정보 정정"}
```

허용 필드만 받으며 미확인 필드는 거절한다. 상품·가격 일괄 수정 시 부모 product version으로 집계 전체 충돌을 판단한다.

작업 조회 응답:

```json
{"jobId":"job-opaque","state":"AWAITING_CONFIRMATION","preview":{"token":"opaque","expiresAt":"2026-11-05T04:00:00Z","matched":30,"changed":28,"invalid":2},"counts":{"succeeded":0,"failed":0}}
```

토큰은 actor/mart/job/payload hash/대상 version/유효기간에 묶는다. 만료·입력 변경은 재미리보기, 처리 직전 변경 행은 충돌 오류로 기록한다.

캠페인 접수 응답:

```json
{"campaignId":"campaign-opaque","state":"SCHEDULED","scheduledAt":"2026-11-06T00:00:00Z","counts":{"preparing":1000,"accepted":0,"delivered":0,"unknown":0}}
```

본문·수신자·발신번호·비용 추정 버전을 미리보기에 고정한다. 발송 직전 동의 철회/차단/잔여 예산을 다시 검사한다. 비용·승인·발송 상한은 미확인으로 고정 수치를 넣지 않는다.
