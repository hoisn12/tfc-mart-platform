# 작업·파일 잠금 원장

유일한 편집자: 메인 Codex. 정확한 파일이 겹치면 동시 RUNNING 금지. reviewer는 쓰기 잠금을 받지 않는다.

| task ID | Phase | 소유자 | 상태 | 정확한 쓰기 파일 | 입력/계약 해시 | 보고서 | 잠금 |
|---|---|---|---|---|---|---|---|
| HARNESS-SETUP | 구축 | 메인 | BLOCKED | validation.md의 생성·수정 파일 목록 | review-manifest.json 참조 | harness/reports/setup/validation.md | 코드·규칙 작성 종료, 활성화는 보호 경로로 차단 |

아직 Phase 작업을 배정하지 않았다. 준비본 검증을 마쳤으며 활성화·실제 Custom Agent 호출은 미완료다. Phase 0은 활성화/스모크 후 별도 지시로 시작한다. 구체적인 task는 templates/task.md 양식을 함께 보존한다.

## UI 프로토타입 — 2026-11-05 사용자 별도 실행 지시

기존 Running Foundation/Phase 0 gate는 승인하지 않는다. 이번 작업은 외부 연동 없는 UI 전용 실행 트랙이다. .codex 없음; 준비 TOML을 명시적으로 읽어 세션 collaboration 역할로 적용한다. Custom Agent 런타임 활성화와 구분한다. 원본 gate 검사기는 변경하지 않는다.

| task ID | Phase | 소유자 | 상태 | 정확한 쓰기 파일 | 입력/계약 해시 | 보고서 | 잠금 |
|---|---|---|---|---|---|---|---|
| UI1-CONTRACT | 1 UI | architect | DONE | docs/contracts/ui-prototype.behavior.md, docs/contracts/ui-prototype.openapi.yaml, docs/adr/009-ui-prototype.md, harness/reports/phase-1/UI1-CONTRACT-architect.md | input-manifest.json | harness/reports/phase-1/UI1-CONTRACT-architect.md | RELEASED |

검증: 계약에 상품/문자/이미지/회원/설정, LocalStorage 오류/복구, 합성자료, UNKNOWN 재발송 금지, integer KRW/string barcode/UTC-KST, UI demo 권한 한계, 이후 API 교체점과 명시적 제외 포함. frontend 읽기 → reliability 읽기 → 독립 reviewer 읽기 → 메인 SHA-256 동결 후 구현한다. 패키지 매니저 기존 없음: npm 선택.

| UI1-SETUP | 1 UI | main | RUNNING | frontend/package.json, frontend/package-lock.json, frontend/index.html, frontend/tsconfig.json, frontend/vite.config.ts, frontend/postcss.config.js, frontend/components.json, frontend/playwright.config.ts, frontend/.gitignore, README.md | input-manifest.json | harness/reports/phase-1/UI1-SETUP-main.md | ACTIVE |

| UI1-CONTRACT-READ-FE | 1 UI | frontend | DONE | 없음(읽기) | behavior 914bb804… / openapi fcb89bbb… | UI1-CONTRACT-read-reviews.md | NONE |
| UI1-CONTRACT-READ-BE | 1 UI | backend | DONE | 없음(읽기) | behavior 914bb804… / openapi fcb89bbb… | UI1-CONTRACT-read-reviews.md | NONE |
| UI1-CONTRACT-SAFETY | 1 UI | reliability | DONE | 없음(읽기) | behavior 914bb804… / openapi fcb89bbb… | UI1-CONTRACT-read-reviews.md | NONE |

| UI1-CONTRACT-REVIEW | 1 UI | reviewer_contract | DONE | 없음(읽기) | contract-freeze.json | UI1-CONTRACT-reviewer.md | NONE |
| UI1-IMPLEMENT | 1 UI | frontend | RUNNING | frontend/src/main.tsx, frontend/src/app/App.tsx, frontend/src/app/AppShell.tsx, frontend/src/app/PrototypeProvider.tsx, frontend/src/styles.css, frontend/src/types/index.ts, frontend/src/lib/utils.ts, frontend/src/lib/format.ts, frontend/src/services/repository.ts, frontend/src/services/localRepository.ts, frontend/src/mocks/seed.ts, frontend/src/hooks/useRepository.ts, frontend/src/components/ui/button.tsx, frontend/src/components/ui/dialog.tsx, frontend/src/components/ui/input.tsx, frontend/src/components/ui/badge.tsx, frontend/src/components/ui/table.tsx, frontend/src/components/shared.tsx, frontend/src/components/ProductImage.tsx, frontend/src/features/dashboard/DashboardPage.tsx, frontend/src/features/products/ProductsPage.tsx, frontend/src/features/products/ProductForm.tsx, frontend/src/features/messaging/MessagingPage.tsx, frontend/src/features/images/ImagesPage.tsx, frontend/src/features/members/MembersPage.tsx, frontend/src/features/settings/SettingsPage.tsx, frontend/src/services/localRepository.test.ts, frontend/tests/prototype.spec.ts, harness/reports/phase-1/UI1-IMPLEMENT-frontend.md | contract-freeze.json SHA-256 기준 | harness/reports/phase-1/UI1-IMPLEMENT-frontend.md | ACTIVE |

UI1-IMPLEMENT 완료 조건: 여섯 화면 실제 동작, 서비스/저장소 오류와 안전상태 구현, typecheck/build/unit/E2E 실행, 한국어 보고. 검증 명령 frontend에서 npm run typecheck, npm test, npm run build, npm run test:e2e. package/config/lock/README 메인 소유.

## 2026-11-06 — 사용자 지시: 전체 붉은 테마

기존 UI 메인 thread `01a1aa49-23eb-7ad0-81f1-6333ea52dc70`는 `wait_threads`로 systemError / turn failed / completedAt 존재를 확인했다. 완료 승격은 하지 않는다. 색상 변경 범위는 아래 두 파일뿐이며 기존 UI1-IMPLEMENT의 이 두 파일 쓰기 잠금을 회수·해제하고 새 작업에 이전한다. 기존 행의 ACTIVE는 이 인계 이후 이 두 파일에 적용되지 않는다. 다른 앱 파일/기능 구현은 재개하지 않는다.

최종 인계 SHA-256: `frontend/src/styles.css` = `45f2d0cc8cdaf22ede79350b4b24f48a38d305b71a0e03845110294fe035f00e`; `frontend/src/features/dashboard/DashboardPage.tsx` = `933c8106a0d716c4e0bf9151b92d52ad83e88093bd69d5b5b16f4b0bb4e6767b`.
기존 FROZEN 계약의 behavior/OpenAPI/ADR 세 파일 해시가 승인본과 일치한다. 밝은 중립 팔레트+한 가지 강조색 계약 내 스타일 변경으로 API·상태·오류·권한·멱등성 계약은 변경하지 않는다.

| task ID | Phase | 소유자 | 상태 | 정확한 쓰기 파일 | 입력/계약 해시 | 보고서 | 잠금 |
|---|---|---|---|---|---|---|---|
| UI-RED-20261106-FE | 1 UI 색상 수정 | frontend | DONE | frontend/src/styles.css, frontend/src/features/dashboard/DashboardPage.tsx, harness/reports/phase-1/UI-RED-20261106-frontend.md | 기존 contract-freeze.json 및 위 인계 해시; /tmp/tfc-mart-red-theme/manifest.json | harness/reports/phase-1/UI-RED-20261106-frontend.md | RELEASED — 독립 읽기 검토 PASS |

완료 조건: 전체 UI의 녹색 브랜드·선택·hover/focus·배경·차트를 붉은 계열로 변경, 성공/경고/실패 의미 구분 유지, 기능·데이터 불변. 검증: `npm run build` (frontend cwd), 색상 외 변경 없음 읽기 대조. 새 테스트 작성·서비스·외부 API·DB·실SMS·운영 변경·기존 데이터 삭제 금지. main은 상태/원장/최종 보고만 취합한다. 쓰기 종료 후 새 reviewer가 읽기 검토한다.

frontend 실제 custom task `/root/ui_red_theme_frontend`, thread `01a1b118-c0b0-7f40-96e9-e087fdd6a61f`, 종료·잠금 반환 확인. 최종 입력: styles.css `98b09c56caf8732db6cca706c2c56d2d6d16085c864029b9c63905333a451b18`, DashboardPage.tsx `11dd406b5e689ecd0b929da0389da98094e5ee5b1716253bfee1154762d4303e`. `npm run build` 종료 0; 기존 Node 18/Vite 지원 버전 경고 기록. 검토 중 대상 쓰기 없음.

| UI-RED-20261106-REV | 1 UI 색상 수정 | reviewer | DONE | 없음(읽기만, 응답 반환) | 위 최종 2파일 SHA-256 및 frontend 보고서 | harness/reports/phase-1/UI-RED-20261106-reviewer.md (메인 저장) | NONE |

독립 custom reviewer `/root/ui_red_theme_reviewer`, thread `01a1b11b-16fc-72b0-af54-4ff0bc699563`: 색상 변경 정적 검토 PASS. 첫 정적 비교 종료1은 성공 범례 설명 주석 차이로 확인됐고 주석 제외 재검사 종료0 PASS; 실패 이력은 reviewer 원문에 보존했다. 메인 최종 해시 대조 종료0 PASS. 브라우저 시각 QA/E2E/단위 테스트 NOT_RUN, Node18 지원 버전 경고 유지. 이 task DONE은 색상 수정만 의미하며 전체 UI/Phase gate 완료가 아니다. 기존 Phase 및 setup 상태는 변경하지 않는다.

| UI1-VERIFY-MAIN | 1 UI | main | RUNNING | harness/reports/phase-1/UI1-tests-main.md, harness/reports/phase-1/UI1-test-attempt-1.log, harness/reports/phase-1/UI1-test-attempt-2.log, harness/reports/phase-1/UI1-test-attempt-3.log, harness/reports/phase-1/UI1-test-attempt-4.log, harness/reports/phase-1/UI1-test-attempt-5.log | contract-freeze.json | UI1-tests-main.md | ACTIVE |

## 2026-11-09 — 참고 이미지처럼 중립 배경 + 빨간 포인트

이번 사용자 요청은 기존 UI 전용 트랙의 스타일 수정으로 한정한다. 전체 Phase 진입/승격 없음. 현재 협업 트리는 메인만 실행 중임을 확인했다. 과거 UI1-IMPLEMENT의 styles.css 쓰기 잠금은 종료된 과거 세션 기록이며 현재 대상 파일에 대한 잠금을 회수해 아래 task에 이전한다. 현재 styles.css 해시는 이전 붉은 테마 보고서와 다르므로 작업 시작 시 실제 파일을 별도로 보관했다. 기존 자료를 되돌리지 않고 현재 입력을 기준으로 수정한다. 계약 세 파일은 동결 해시와 일치한다.

| task ID | Phase | 소유자 | 상태 | 정확한 쓰기 파일 | 입력/계약 해시 | 보고서 | 잠금 |
|---|---|---|---|---|---|---|---|
| UI-ACCENT-20261109-FE | 1 UI 색상 수정 | frontend | DONE | frontend/src/styles.css, harness/reports/phase-1/UI-ACCENT-20261109-frontend.md | UI-ACCENT-20261109-attempt-1/input-manifest.json, 기존 contract-freeze.json | harness/reports/phase-1/UI-ACCENT-20261109-frontend.md | RELEASED |

완료 조건: 첨부 이미지의 밝은 중립 UI, 흰색/회색 배경·사이드바·테이블·글자, 빨간 주요 액션/체크/선택 포인트, 의미별 상태색 유지, 레이아웃/동작/계약 불변. 정확한 앱 쓰기는 styles.css만 허용한다. CSS 선언의 색상만 수정하고 build는 메인이 격리 출력 경로로 수행한다. 검증: TypeScript 검사와 Vite build, CSS 색상 외 변경 대조, 새 독립 reviewer 읽기 검증. 브라우저/서비스 기동·설치·외부 연동·DB·실발송·배포 없음.

추가 사용자 지시: 파비콘도 같은 빨간색으로 변경한다. index.html의 기존 녹색 SVG data favicon과 theme-color만 #b52c3d로 교체한다. UI1-SETUP의 index.html 잠금은 과거 종료 세션 기록에서 회수해 아래 메인 task로 이전한다. 원본/해시는 위 attempt의 before 및 input-manifest에 보존했다.

| UI-ACCENT-20261109-ICON | 1 UI 색상 수정 | main | DONE | frontend/index.html, harness/reports/phase-1/UI-ACCENT-20261109-main.md | UI-ACCENT-20261109-attempt-1/input-manifest.json | harness/reports/phase-1/UI-ACCENT-20261109-main.md | RELEASED |

2026-11-09 대상 쓰기 종료 및 frontend 잠금 반환 확인. FE/ICON ACTIVE 잠금은 RELEASED로 전환하며 위 두 파일은 독립 검토 중 동결한다. 산출물 스냅샷: UI-ACCENT-20261109-attempt-1/snapshot, output-manifest.json.

| UI-ACCENT-20261109-REV | 1 UI 색상 수정 | reviewer | DONE | 없음(읽기 전용) | UI-ACCENT-20261109-attempt-1/output-manifest.json | harness/reports/phase-1/UI-ACCENT-20261109-reviewer.md (메인 저장) | NONE |

독립 reviewer /root/ui_red_accent_reviewer: 색상·파비콘 정적 검증 PASS, 결함 없음. reviewer 검사 스크립트 첫 실패(공백 CSS 조각 ValueError)는 보고서 원문에 보존했고 수정한 검사 종료0. TypeScript 및 지원 Node20 Vite build 종료0, 산출물 favicon 색상 일치. 브라우저/E2E/운영 검증 NOT_RUN. 세 task DONE은 이번 색상 범위만 의미하며 Phase/state/gate는 승격하지 않는다.

## 2026-11-09 — GitHub Pages 자동 배포

최신 사용자 요청은 main push/PR merge 후 GitHub Pages로 UI 정적 데모를 빌드·게시하는 Actions 추가다. 전체 시스템 Phase 실행/승격과 분리한다. 현재 세션의 전문 Agent는 없고 과거 UI1-SETUP/IMPLEMENT의 아래 중복 파일 잠금은 종료된 세션의 기록이므로 이번 작업으로 회수한다. 기존 미커밋 파일은 보존한다. 원격 push/배포/설정 변경은 수행하지 않는다.

| task ID | Phase | 소유자 | 상태 | 정확한 쓰기 파일 | 입력/계약 해시 | 보고서 | 잠금 |
|---|---|---|---|---|---|---|---|
| PAGES-20261109-MAIN | 1 UI 배포 설정 | main | DONE | .github/workflows/pages.yml, frontend/src/main.tsx, README.md, docs/adr/010-github-pages-demo.md, harness/reports/phase-1/PAGES-20261109-main.md, harness/reports/phase-1/PAGES-20261109-attempt-1/input-manifest.json, harness/reports/phase-1/PAGES-20261109-attempt-1/output-manifest.json 및 그 manifest에 명시한 before/snapshot 파일 | PAGES-20261109-attempt-1/input-manifest.json; 기존 contract-freeze.json | harness/reports/phase-1/PAGES-20261109-main.md | RELEASED — 산출물 동결 |

완료 조건: main push(병합 포함)와 main 수동 실행 시 npm ci→단위 테스트→타입 검사/Pages base 빌드→Pages artifact→의존 deploy. 최소 권한·직렬 배포, Pages 전용 hash router로 새로고침 지원, 기본 로컬 URL 보존, 최초 Pages 설정/접속 URL 문서화. 검증: 두 라우터 모드 TypeScript/Vite build, 단위 테스트, 산출물 base 경로/라우터 정적 검사, harness validate 및 기존 phase-1 gate 결과 기록, 새 독립 reviewer 읽기 검증. 배포 성공은 원격 실행 전 NOT_RUN.

| PAGES-20261109-REV | 1 UI 배포 설정 | reviewer | FAILED | 없음(읽기 전용, 응답 반환) | PAGES-20261109-attempt-1/output-manifest.json | harness/reports/phase-1/PAGES-20261109-reviewer-attempt-1.md (메인 저장) | NONE |

메인 쓰기 종료. 출력 manifest와 snapshot 동결 후 새 독립 reviewer에게 main/merge 트리거, 권한, base/hash, 최초 설정 안내, 증거·한계를 읽기 검증 요청한다.

시도1 권한 결함으로 FAIL: build configure-pages API 조회에 pages:read가 누락됐다. main 잠금을 재취득해 .github/workflows/pages.yml, docs/adr/010-github-pages-demo.md, PAGES-20261109-main.md를 수정했다. build에 contents:read/pages:read 명시, ADR·메인 보고서 정정. attempt-1은 보존하며 attempt-2/output-manifest.json 및 명시한 snapshot 파일 생성 후 쓰기를 종료하고 잠금을 반환한다. main 관리 파일과 두 독립 판정 보고서는 메인만 저장한다.

| PAGES-20261109-REV2 | 1 UI 배포 설정 | reviewer | DONE | 없음(읽기 전용, 응답 반환) | PAGES-20261109-attempt-2/output-manifest.json | harness/reports/phase-1/PAGES-20261109-reviewer-attempt-2.md (메인 저장) | NONE |

최종: 새 독립 reviewer /root/pages_reviewer_attempt_2가 설정 정적 검토 PASS. 메인 최종 현재/스냅샷 SHA-256 재대조 종료0. 시도1 FAIL과 시도2 PASS 원문을 각각 보존했다. 단위12개/타입·두 빌드/YAML/asset 경로 PASS. 원격 Actions/Pages/Node22 및 브라우저 검증 NOT_RUN. 설정 추가 task만 DONE이며 실제 배포 완료나 전체 Phase PASS가 아니다. state/기존 gate는 변경하지 않는다.
