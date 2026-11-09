# TFC 마트 통합관리 · UI 프로토타입

React/TypeScript 기반의 로컬 관리자 데모입니다. 상품관리, 대시보드, 문자 발송, 이미지, 회원, 설정을 조작할 수 있습니다. 화면의 수치·마트·회원·상품은 모두 합성 샘플이며 실제 운영 자료가 아닙니다.

## 실행

Node.js 20.19 이상(20 LTS) 또는 22.12 이상과 npm이 필요합니다. 백엔드·DB·자격증명 없이 실행합니다.

```sh
cd frontend
npm ci
npm run dev
```

브라우저에서 <http://127.0.0.1:5173>을 엽니다. 개발 서버는 loopback에만 바인딩합니다.

```sh
cd frontend
npm run typecheck
npm test
npm run build
```

`npm test`는 서비스 테스트와 Playwright E2E를 함께 실행합니다. 개별 실행은 `npm run test:unit`, `npm run test:e2e`입니다. 브라우저 테스트 결과는 실행별 임시 폴더에 보존합니다.

Playwright Chromium이 설치되지 않은 개발 환경에서는 `npx playwright install chromium`을 한 번 실행합니다. 테스트는 격리된 브라우저 컨텍스트의 합성 데모 자료만 변경합니다.

## GitHub Pages 자동 배포

[Pages workflow](.github/workflows/pages.yml)는 `main` push 때 실행됩니다. PR을 `main`에 merge해도 push 이벤트로 한 번 실행됩니다. Actions에서 수동 실행할 때도 `main`을 선택합니다.

1. 저장소 **Settings → Pages → Build and deployment → Source**를 **GitHub Actions**로 설정합니다([GitHub 공식 안내](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)).
2. 프런트엔드 소스와 workflow를 함께 `main`에 반영합니다.
3. **Actions → Deploy UI demo to GitHub Pages**의 성공을 확인하고 배포 환경의 URL을 엽니다.

기본 접속 주소: <https://hoisn12.github.io/tfc-mart-platform/>. Pages 설정에 커스텀 도메인이 있으면 Actions에 표시되는 URL을 사용합니다. 최초 설정 전에는 배포가 실패할 수 있습니다.

Node 22에서 `npm ci` → 단위 테스트 → 타입 검사와 빌드 → Pages 업로드·배포 순서로 실행합니다. 테스트나 빌드가 실패하면 배포하지 않습니다. 별도 토큰/비밀값 등록은 필요하지 않습니다. Pages 배포본만 해시 라우팅을 사용해 `/tfc-mart-platform/#/products`처럼 메뉴 이동·직접 접속·새로고침을 지원합니다. 로컬 개발 URL은 기존과 같습니다. [ADR 010](docs/adr/010-github-pages-demo.md)에 배포·복구 결정을 기록했습니다.

공개되는 화면은 합성자료 UI 데모입니다. 서버·실제 SMS·DB 기능은 포함하지 않습니다.

## 화면과 데이터

- 대시보드: 상품·주문·매출·문자 요약과 샘플 차트, 최근 변경.
- 상품관리: 검색/마트/분류/상태 필터, 정렬/페이지 이동, 컬럼 설정, 상세·등록·수정·보관, 선택 일괄 변경.
- 문자 관리: 합성 대상만 사용하는 로컬 상태 시뮬레이션. 요청 접수와 전달 결과를 구분하고 UNKNOWN 재발송을 제공하지 않습니다.
- 이미지 관리: 로컬 업로드·검증·미리보기·교체 상태와 fallback. S3/CDN 업로드가 아닙니다.
- 회원/설정: 합성 회원 검색·상세, 마트 정보·운영 설정.

브라우저 LocalStorage에 데모 상태를 보존합니다. 초기화는 설정 화면에서 확인 후 실행하며 이 앱의 데모 키만 대상으로 합니다. 실제 정보·비밀값을 입력하지 마세요. 브라우저 저장소 한도/접근 실패·파손은 오류로 안내합니다.

UI는 Repository 인터페이스를 통해 데이터에 접근하고, LocalStorage 어댑터만 Mock seed를 참조합니다. 향후 REST 어댑터로 교체할 때 서버 인증·마트 권한·검증·감사·동시성 통제를 별도로 구현해야 합니다. 현재 마트 선택은 데모 필터이며 보안 경계가 아닙니다.

## 범위와 검증 기록

이번 작업은 사용자가 별도로 허용한 **Phase 1 프론트엔드 UI 프로토타입**입니다. Java/Spring Boot, DB, AWS/SQS/S3/CDN, 실제 SMS/주문/결제, 운영 배포는 구현하지 않습니다. 실제 레거시 기능 동등성 및 운영 안정성도 검증하지 않았습니다.

- [UI 계약](docs/contracts/ui-prototype.behavior.md), [향후 API 연결점](docs/contracts/ui-prototype.openapi.yaml), [ADR 009](docs/adr/009-ui-prototype.md)
- [진행 원장](docs/PROGRESS.md), [작업과 잠금](harness/TASKS.md), [UI 검증 보고서](harness/reports/phase-1/)

`.codex/` Custom Agent는 활성화되지 않았습니다. 이번 협업은 `harness/codex/agents/` 준비 TOML의 역할 지침을 일반 collaboration Agent에 적용합니다. 기존 전체 시스템 Discovery/Running Foundation gate는 UI 데모 결과와 별개로 차단 상태를 보존하며, 이를 승인·활성화 완료로 해석하면 안 됩니다.
