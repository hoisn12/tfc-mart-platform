# UI 프로토타입 동작 계약 v1

상태: architect 검토안. 구현자·안전·독립 검토 후 메인이 SHA-256 동결한다.
근거: 2026-11-05 사용자 「Phase 1 — UI 프로토타입 구현」, PRD §1~3, §4.3, §5~6, `docs/architecture.md`. 이 계약은 브라우저의 합성자료 데모에만 적용한다. 기존 Running Foundation의 backend/DB/인증/운영 gate나 레거시 동등성을 승인하지 않는다. 실제 한글 레거시 화면은 제공 파일에서 확인되지 않았고 `example.png`는 영문 디자인 참고다.

## 경계와 구성

- `frontend/`에 독립 Vite + React + TypeScript 앱. 기존 패키지 매니저가 없어 npm과 lockfile을 사용한다. Tailwind, shadcn/ui 계열의 접근 가능한 기본 컴포넌트, TanStack Query/Table, React Router, Lucide를 사용한다. Zustand는 필요할 때만 추가한다.
- `features`는 `services`의 비동기 Repository/Service 인터페이스를 사용한다. `mocks`와 LocalStorage 접근은 local adapter 안에만 둔다. 컴포넌트가 fixture를 직접 import하지 않는다. 서비스 인터페이스를 REST adapter로 교체할 수 있도록 DTO와 UI 상태를 분리한다.
- 경로는 `/` 대시보드, `/products`, `/messaging`, `/images`, `/members`, `/settings`. 메뉴의 활성 상태, 접이식 사이드바, breadcrumb, 마트 선택, 사용자/알림 메뉴를 제공한다. 존재하지 않는 경로는 복귀 안내한다.
- 전체 페이지에 샘플/Demo 표시. 실제 주문/매출/문자 성과나 실제 관리자 인증이라고 표현하지 않는다. 외부 SMS/S3/AWS/DB/결제 요청과 프로덕션 배포는 없다. 브라우저에 실데이터/실수신번호/비밀값 입력을 요구하지 않는다.
- 데스크톱 최소 1280px에 맞춘 밝은 중립 팔레트와 한 가지 강조색. 페이지 제목·액션, 카드, 상태 badge, 검색·필터·table·빈 상태·로딩·오류·재시도·focus를 일관되게 제공한다. 좁은 화면과 많은 열은 표 영역 가로 스크롤로 처리한다. dialog/drawer는 이름·닫기·키보드 focus/ESC를 제공한다.

## 데이터 모델과 서비스 의미

구현의 실제 이름은 의미를 보존하는 범위에서 조정 가능하다. ID/코드/바코드는 문자열, 금액은 원 단위 안전 정수, 시각은 ISO 8601 UTC 문자열이다. 화면 시각은 `Asia/Seoul`로 표시하며 예약 입력에는 KST를 표기하고 UTC로 변환한다.

```ts
type Product = {
  id: string; code: string; barcode: string; name: string; martId: string;
  category: string; brand: string; specification: string;
  price: number; discountPrice: number | null; minOrder: number; maxOrder: number;
  saleStatus: 'ON_SALE' | 'STOPPED'; visible: boolean;
  stockStatus: 'IN_STOCK' | 'LOW_STOCK' | 'OUT_OF_STOCK';
  imageId?: string; imageUrl: string; version: number;
  updatedAt: string; deletedAt?: string;
};
type MessageStatus = 'PENDING' | 'PROCESSING' | 'ACCEPTED' | 'DELIVERED' | 'FAILED' | 'UNKNOWN';
type ImageStatus = 'PROCESSING' | 'READY' | 'FAILED';
type ServiceErrorCode = 'VALIDATION' | 'NOT_FOUND' | 'CONFLICT' | 'STORAGE_UNAVAILABLE' | 'STORAGE_CORRUPT';
```

최소 서비스 유스케이스는 다음과 같다. 정렬/필터/페이지네이션을 local adapter 또는 TanStack Table에서 수행해도 동일한 결과를 보장한다. Query 캐시 무효화 후 요약과 목록이 함께 갱신된다.

| 유스케이스 | 입력과 결과 | 실패·정합성 |
|---|---|---|
| 상품 목록/조회 | 검색·마트·카테고리·판매/노출/재고 필터·정렬·페이지 → 목록/전체 건수, ID → 상세 | 미삭제만 기본 표시; 코드/바코드의 선행 0 보존 |
| 상품 등록/수정 | DTO, 수정은 ID+기존 version → 저장 상품 | 필수값, 금액, 수량, 마트 참조 검증. version 다르면 CONFLICT와 새로고침 안내 |
| 상품 삭제 | ID+version → soft delete | 확인 dialog 뒤 deletedAt 저장, 데이터 물리 삭제 금지 |
| 일괄 변경 | 선택 ID+version들과 판매/노출/재고 변경값 → 미리보기 → 확정 결과 | 선택 수·전후값 확인. 취소 시 무변경. 처리 직전 version 확인, 충돌은 실패 건수로 명시 |
| 대시보드 | 선택 마트 → 상품 집계·합성 일별 주문/매출·문자 집계·최근 변경 | 삭제/일괄 변경/단건 저장과 집계 일관성, 샘플 명시 |
| 문자 목록/요청 | 마트·제목·본문·SMS/LMS·합성 대상 그룹·선택 예약일 → PENDING | 실제 번호 입력/외부 호출 없음. 예약 유효성 검증 |
| 문자 모의 처리 | 캠페인 ID → PROCESSING/ACCEPTED/DELIVERED/FAILED/UNKNOWN 중 데모 전이 | 접수≠전달. UNKNOWN 재발송·자동 failover 경로 없음 |
| 이미지 목록/등록/교체 | File+선택 상품 → metadata와 처리 결과 | 형식/크기/디코딩 검증, READY 전 기존 대표 유지 |
| 회원 목록/조회 | 검색·상태·마트 → 합성 회원과 상세 | 실제 연락처 없이 마스킹된 합성자료만 사용 |
| 설정 조회/저장 | 마트 기본정보·운영 설정 → 저장 결과 | 관리자 계정 목록은 합성자료. 인증·권한 변경으로 표현하지 않음 |
| 데모 초기화 | 확인 → 이 앱의 합성 저장소만 seed로 복원 | 다른 origin 키·기존 자료·파일 삭제 금지 |

서비스 facade는 아래 하나의 `AppRepository`로 묶어도 된다. `getState`의 snapshot은 marts/products/messages/images/members/settings/audit를 제공하고 UI는 Query의 snapshot을 구독한다. 단일 facade는 기능별 adapter 분리를 방해하지 않는다. 아래는 의미 계약이며 정확한 TS 인수의 객체 포장/이름은 구현 시 조정 가능하다.

```ts
interface AppRepository {
  getState(): Promise<AppSnapshot>;
  saveProduct(input: ProductInput, existing?: { id: string; version: number }): Promise<Product>;
  archiveProducts(items: Array<{ id: string; version: number }>): Promise<BulkResult>;
  bulkProducts(items: Array<{ id: string; version: number }>, changes: ProductStatusPatch): Promise<BulkResult>;
  requestMessage(input: DemoMessageRequest): Promise<Message>;
  advanceMessage(id: string): Promise<Message>;
  uploadImage(file: File, productId?: string): Promise<ImageAsset>;
  updateSettings(input: DemoSettings): Promise<DemoSettings>;
  reset(): Promise<AppSnapshot>;
}
```

`AppSnapshot`과 나머지 DTO는 위 모델/유스케이스 표의 의미에 따라 정의한다. 마트 선택/열설정은 별도 UI preference 계층에 두어도 된다. `advanceMessage`는 UNKNOWN에서 재발송하지 않고 현 상태를 유지하거나 거절한다. `archiveProducts`도 각 version을 검증해 부분 실패를 반환한다.

## 상품 업무 흐름

- 100개 이상(권장 120개)의 서로 다른 코드와 현실적인 식품·생활용품명/규격/브랜드/가격을 생성한다. 여러 마트/카테고리와 관계를 일관되게 생성한다. 초기 데이터에서 판매중·중지·품절·비노출 상태가 모두 관찰 가능해야 한다.
- 기본 열은 checkbox, 이미지, 코드, 상품명, 마트, 카테고리, 브랜드, 규격, 판매가, 할인가, 최소·최대 주문, 판매·노출·재고 상태, 수정일, 작업이다. 사용자가 열을 숨길 수 있고 핵심 선택/상품/작업 접근은 유지한다. 열 설정은 새로고침 후 복원한다.
- 검색은 상품명·코드·바코드·브랜드 대상으로 대소문자 무시 부분 일치. 필터는 AND 결합, 변경 시 첫 페이지로 이동한다. 상품명/가격/수정일 등 의미 있는 정렬, 페이지 크기 및 이전/다음 페이지 이동을 제공한다.
- 페이지 전체 checkbox는 현재 표시 행만 선택한다. 필터/마트 변경 시 선택은 해제하고, 페이지를 넘겨 선택을 유지하면 전체 선택 수를 표시한다. 숨은 행에 모호한 일괄 작업을 하지 않는다.
- Drawer에서 상세/이미지 미리보기와 수정, 등록 dialog, 저장/취소, 삭제 확인을 제공한다. 취소는 저장소를 변경하지 않는다. 행의 작업 메뉴에서 빠르게 편집할 수 있다.
- 이름/코드/바코드/마트/분류 등 필수값은 공백 불가. 가격은 0 이상 안전 정수, 할인가 null 또는 0~판매가, 주문량은 1 이상 정수이며 min≤max. 중복 코드와 같은 마트 내 바코드 중복은 거절한다. 이것은 데모 가정이며 레거시 규칙 확정이 아니다.
- 저장 성공 뒤 Toast, 실패/validation은 원인과 수정 안내. 저장 실패 상태를 성공 Toast로 표현하지 않는다. 최근 변경 이력을 합성 사용자·시각·상품·행위로 유지한다.

## 문자·이미지·회원·설정

문자는 SMS/LMS, 합성 발송대상 수, 즉시/예약, 접수/처리중/발송사 접수/전달성공/실패/미확정을 구분한다. 각 캠페인의 성공·실패·미확정·처리중 합은 총 대상 수와 일치해야 한다. 이력 상세에는 상태와 모의 결과를 표시한다. 생성 후 명시적 모의 처리 버튼 또는 결정적인 재계산으로 상태를 바꿀 수 있다. 예약은 브라우저가 닫힌 동안 실행되는 실제 scheduler가 아니며 그 한계를 설명한다. UNKNOWN은 조회/대사 대기 안내만 제공하고 재발송 기능을 만들지 않는다.

이미지는 JPEG/PNG/WebP, 최대 5 MiB를 허용하고 MIME/확장자 일치와 실제 이미지 디코딩을 확인한다. SVG/실행파일/손상 이미지/초과 크기는 거절한다. 썸네일·원본 미리보기, 파일명·형식·크기·상품/마트 연계·상태를 보여준다. URL 선택/해석은 서비스에 둔다. 데모 업로드는 브라우저에서만 처리하고 용량을 제한한 data URL 등을 로컬 저장할 수 있다(DB byte 저장 아님). PROCESSING/FAILED에서는 기존 대표 URL을 유지하고 READY 후 새 버전 ID와 함께 교체한다. 실패 예시/복구 동작을 제공한다. 깨진 이미지 URL은 고정 크기 fallback으로 바꾸며 다른 행의 레이아웃에 영향이 없다. 원본/기존 이미지 GC는 하지 않는다.

회원 목록은 이름/합성 회원 ID 검색, 활성/휴면/탈퇴 등 상태 필터와 상세를 제공한다. 연락처는 마스킹된 가짜 예시다. 설정은 마트 기본정보, 합성 관리자 목록, 주문 최소금액/재고알림 등 기본 운영설정의 로컬 저장을 제공한다. 적용 범위가 데모임을 명시한다.

## 저장·오류·복구·권한·멱등성

- LocalStorage는 `tfc-mart-ui` 등 앱 전용 versioned namespace와 JSON schemaVersion을 사용한다. 데이터·설정·열설정은 해당 namespace에만 저장한다. 최초 키 부재일 때만 seed를 생성한다.
- JSON parsing/shape/schema mismatch는 STORAGE_CORRUPT로 안내하고 기존 raw 값을 자동 삭제하거나 seed로 덮지 않는다. 복구 안내와 사용자가 명시적으로 확인하는 데모 초기화를 제공한다. 읽기 불가/용량초과/쓰기 거절은 STORAGE_UNAVAILABLE로 표시하고 저장 성공을 반환하지 않는다. 쓰기 성공 전에 UI의 authoritative 데이터를 변경하지 않는다.
- 초기화는 이 앱이 만든 합성자료만 대상으로 하며 취소 시 무변경. 타 키를 건드리지 않고 `localStorage.clear()`를 사용하지 않는다. 초기화 실패도 명시한다.
- 등록/저장/발송 요청의 처리 중 중복 클릭을 막는다. 업데이트는 version으로 오래된 상세 저장을 거절한다. bulk 재확정은 최신 version 불일치로 중복 적용을 거절한다. 이 메모리/브라우저 동작을 서버 멱등성이나 동시 TX 보장으로 주장하지 않는다.
- 선택 마트에 맞춰 표시·쓰기 대상을 검증하는 것은 데모 UX다. 브라우저 데이터는 사용자 수정 가능하며 서버 인가·테넌트 보안을 제공하지 않는다. 미래 API는 인증된 Principal의 mart 권한과 version, idempotency를 서버에서 강제해야 한다.
- 네트워크 없는 데모의 로딩 지연·실패 예시는 local fake로만 재현한다. 외부 인증/웹훅/내구 큐/운영 복구는 NOT_RUN이다.

## 인수 검증 대응

| 사용자 요구 | 실행 검증 |
|---|---|
| 1~3 실행·메뉴·목록 | Vite 실제 기동, 여섯 경로/활성 메뉴, 100+ 상품 목록/페이지 이동 |
| 4 검색·필터 | 코드/바코드/이름 검색, 마트+카테고리+상태 교차, empty/초기화, 정렬 |
| 5 수정 | Drawer 저장·취소·유효성, 중복 코드, version 충돌, soft delete |
| 6 일괄 | 현재 페이지 선택, 미리보기 취소/확정, 선택 수·전후값·부분 충돌 결과 |
| 7 지속성 | 편집→브라우저 새로고침, 열설정 복원, 초기화 취소/확정, 저장 거절/손상 JSON 복구 |
| 8 이미지 | 정상 미리보기, 형식/크기/손상 거절, PROCESSING/FAILED 기존 대표 유지, 깨진 URL fallback |
| 9 오류 | 실제 브라우저 콘솔/페이지 오류 수집, 외부 SMS/storage 요청 없음 |
| 10 정적 검사 | TypeScript 검사·production build·필수 서비스/브라우저 회귀 테스트 |
| 문자·회원·설정 | 상태별 집계/상세/요청 모의 동작, UNKNOWN 재발송 없음, 회원 검색·상세, 설정 저장·복원 |

계약 검토 PASS는 위 테스트 실행 PASS가 아니다. README에는 실행 명령, 데모 초기화, LocalStorage 한계, 미구현 외부 연동을 기록한다. 독립 reviewer가 고정 스냅샷에서 재현하고 메인이 결과를 저장한다.
