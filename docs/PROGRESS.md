# 진행 기록

## 2026-11-05 — Phase 0

상태: **설계 문서 작성 완료, Discovery 확인·승인 대기**. Phase 1 이후는 미착수다.

기본 명세 두 파일을 전체 확인하고 example.png를 직접 열람했다. 초기 폴더에는 세 파일만 있고 소스/DB/API/인프라/테스트는 없었다. PNG는 영문 디자인 참고로 PRD의 한글 레거시 화면과 다르다. 기능 대응표·요구사항·구조/ADR/시퀀스·ERD·API·미확인/위험·개발/전환/검증 계획을 작성했다.

프롬프트의 ‘가능하면 Phase 1까지’와 ‘단계마다 코드 추가’보다 이번 사용자의 ‘Phase 0만, 구현 금지’를 우선했다. SQL/OpenAPI YAML/frontend/backend/infra/CI를 만들지 않았다. 문서 진입점은 docs/README.md이며 루트의 원본 자료를 수정하지 않았다.

## 확인 명령과 결과

| 확인 | 결과 |
|---|---|
| pwd / ls -la / rg --files | 대상 경로·초기 세 파일 확인 |
| cat 두 기본 명세 | 전체 읽음 |
| view_image example.png | 영문 Products 참고 확인 |
| 대상·상위 경로 AGENTS 확인 | 추가 지침 파일 없음 |
| git rev-parse --is-inside-work-tree | 종료128, Git 저장소 아님. 읽기 전용 환경의 보조 캐시 경고도 발생했으나 문서 작업에는 영향 없음 |
| docs 검사 | 통과: Markdown 11개, 로컬 링크 15개, 코드 펜스 닫힘, 한국어 표현, docs 외 신규 파일 없음. Mermaid 4개 존재 확인(렌더링 미실행) |

기능 테스트/build/lint/DB·큐 복원/Mermaid 렌더링은 실행하지 않았다. 앱과 실행 환경이 없고 범위는 문서뿐이다. 운영·성능 목표도 미검증이다.

## 다음 우선순위

1. U01/U02/U04 자료·담당자를 확보하고 L-ID별 동작과 권한을 대조한다.
2. U03/U13/U15 물량·예산·보존·알림 대상을 확정해 Foundation 착수 조건을 충족한다.
3. U09/U10/U16 발송사 계약·동의·조회 능력을 확인하고 UNKNOWN 해소 가능성을 우선 검증한다.
4. Phase 0 리뷰 뒤 별도 지시로 Phase 1에 착수한다.

검증 명령은 Python pathlib/re 정적 검사다. 읽기 전용 환경에서 heredoc 임시 파일 생성이 거부되어 같은 검사를 python3 -c로 실행했고 종료 코드 0을 확인했다. 실제 기능 구현 및 외부 서비스 호출은 없다.

## 2026-11-05 — Multi-Agent 하네스 구축

범위: 하네스·설정·공통 규칙·Phase 계획만 작성. 비즈니스 구현과 Phase 0 재실행은 미착수다. 기존 설계 작성 이력을 위에 보존했다. 진행 원장은 사용자 지시대로 docs/PROGRESS.md로 통합했다.

상태: **구축 준비본·검증 완료, 활성화 BLOCKED**. 프로젝트 .codex는 환경의 읽기 전용 보호 경로라 설정 쓰기가 자동 승인 검토에서 거부됐다. 준비본은 harness/codex/에 보존하고 권한 있는 사용자용 설치 절차를 harness/README.md에 기록했다. 실제 Custom Agent 로딩/spawn은 NOT_RUN이며 이를 완료라고 보고하지 않는다.

Phase 0: 기존 초안 존재, Discovery 승인·API 계약 동결·독립 gate 미완료로 BLOCKED. Phase 1~6: NOT_STARTED.

메인 Codex가 Orchestrator이며 architect/backend/frontend/reliability/reviewer 책임을 분리했다. 계약 해시 동결 후 Backend/Frontend 병렬 구현, 파일별 단일 소유자 잠금, 독립 reviewer 검증, 실패/미실행 다음 Phase 차단을 규칙화했다. 실제 SMS·운영 변경·기존 데이터 삭제를 계속 금지한다.

검증 결과와 한계는 harness/reports/setup/validation.md 및 independent-review.md에 기록한다. 다음 작업은 사용자 권한으로 설정 활성화→새 세션 스모크→별도 Phase 0 지시 순서다.

준비본 TOML 6개/공식 최소 필드 검사와 Codex CLI 0.166.0 native strict parser 종료0. 미지원 키는 native parser가 종료1로 거부했다. 게이트 테스트 최종 18개 통과, Python 구문/문서 링크/원본 보존 확인. --active와 Phase 0 gate는 각각 종료1로 차단돼 미설치 상태를 통과시키지 않았다. 일반 협업 하위 Agent의 준비본 독립 검토는 별도 보고서에 보존하며 실제 Custom Agent 로딩 검증과 구분한다. 앱 build/E2E·운영/실발송·DB복원/cloud 장애 테스트는 NOT_RUN이다.

## 2026-11-05 — Phase 1 UI 프로토타입 착수

최신 사용자 요청은 React 프론트엔드 구현·의존성 설치·로컬 Vite 기동·브라우저 검증을 허용한다. 백엔드/DB/AWS/실발송/배포 제외. 기존 Phase 0 Discovery와 전체 Running Foundation gate는 BLOCKED를 보존한다. UI 전용 계약/독립 검증을 별도로 기록한다. .codex 활성 경로가 없으므로 harness/codex 준비본 역할 지침을 collaboration Agent에 전달하여 수행하며 네이티브 Custom Agent 활성화를 주장하지 않는다.


## 2026-11-06 — 붉은 테마 색상 수정

사용자 지시로 기존 UI의 브랜드·내비게이션·버튼·선택/포커스·배경 강조·토글·매출 차트를 딥 레드(`#b52c3d`)와 연한 로즈 계열로 변경했다. 성공/경고/실패 의미색은 유지했다. 기능·데이터·API/상태 계약은 변경하지 않았다.

기존 UI 작업 thread의 오류 종료를 확인하고 두 대상 파일의 해시·잠금을 인계했다. custom frontend가 `frontend/src/styles.css`, `frontend/src/features/dashboard/DashboardPage.tsx`를 수정하고 쓰기를 종료했다. 기존 승인 계약 해시 유지, `npm run build` 종료0, 새 독립 custom reviewer 정적 검토 PASS, 메인 최종 해시 대조 종료0을 확인했다. 보고서는 `harness/reports/phase-1/UI-RED-20261106-frontend.md`와 `UI-RED-20261106-reviewer.md`다.

Node18/Vite 지원 버전 경고는 남아 있다. 브라우저 시각 QA·E2E·단위 테스트는 이번에 실행하지 않았다. 색상 수정만 완료했으며 기존 UI 전체 기능 검증·Phase 0/1 완료를 의미하지 않는다. Phase 및 state는 변경하지 않았다. 서비스·외부 API·DB/인프라·실SMS·운영 변경·기존 데이터 삭제를 실행하지 않았다.

## 2026-11-09 — 중립 UI와 빨간 포인트·파비콘

최신 사용자 요청에 따라 흰색/연회색 배경·사이드바·표·중립 텍스트에 빨간 포인트(#b52c3d)를 적용했다. frontend/src/styles.css의 색상 선언 48개와 frontend/index.html의 favicon/theme-color 두 색상만 바꿨다. 기존 레이아웃·동작·의미별 상태색·나머지 앱 소스26개·동결 계약3개는 유지했다. 이전 보고서 해시와 현재 입력이 다른 점을 기록하고 현재 원본을 별도 보관했으며 다른 변경을 되돌리지 않았다.

frontend 작성·메인 favicon 수정 후 쓰기를 종료하고 스냅샷을 고정했다. 새 독립 reviewer 정적 검증 PASS, TypeScript 검사 종료0, 하네스 validate.py 종료0, 지원 Node20.20.2를 명시한 Vite build 종료0. 첫 직접 Vite 실행은 Node18 지원 경고가 있어 새 격리 출력으로 지원 버전에서 재검증했다. reviewer 첫 검사 스크립트 실패와 원인/정정 이력도 보존했다. 상세 보고서: harness/reports/phase-1/UI-ACCENT-20261109-{frontend,main,reviewer}.md 및 같은 접두 attempt-1의 원본/스냅샷/manifest.

브라우저 시각 QA/E2E/단위 테스트/운영 검증 NOT_RUN. 기능 전체 완료나 Phase PASS로 승격하지 않는다. 기존 state·Phase gate는 유지한다. 서비스 기동·설치·DB·외부 연동·실SMS·배포·기존 자료 삭제 없음.

## 2026-11-09 — GitHub Pages 자동 빌드·배포 설정

최신 사용자 요청에 따라 `.github/workflows/pages.yml`을 추가했다. main 직접 push와 PR merge를 push 이벤트로 처리하고 main 수동 실행도 허용한다. Node22/npm ci→단위 테스트→타입 검사와 Pages base build→frontend/dist artifact→Pages deploy 순서다. build는 contents:read/pages:read, deploy만 pages:write/id-token:write를 가지며 배포 실행 중 취소를 막는다. Pages 배포본에만 HashRouter를 적용해 저장소 하위 URL의 새로고침을 지원하고 기존 로컬 BrowserRouter를 유지했다. README에 최초 Settings→Pages→Source=GitHub Actions 설정과 URL을 안내하고 ADR010에 대안/영향/복구를 기록했다.

지원 Node20.20.2 로컬 환경에서 단위12개, TypeScript 포함 일반·Pages 두 빌드 종료0. YAML 구문/구조·두 모드 asset 참조/존재·계약/package/config 해시 불변 검사를 통과했다. 첫 독립 reviewer는 Pages 조회 읽기 권한 누락으로 FAIL을 반환했고 이를 수정한 attempt-2에 새 reviewer가 PASS를 반환했다. 실패 원문과 두 스냅샷을 보존했고 메인 최종 해시 재대조 종료0. 상세: harness/reports/phase-1/PAGES-20261109-main.md 및 reviewer-attempt-{1,2}.md. validate.py 종료0; check_gate.py --phase 1 종료1은 기존 Phase0 미완료 차단이며 유지했다.

원격 push/저장소 설정 변경/Actions 실행/Pages 실제 게시/Node22 CI 실행/브라우저 E2E는 NOT_RUN. Pages source 설정과 main 반영 후 실제 URL 확인이 필요하다. 이번 설정 task만 완료했으며 기존 state/Phase gate를 승격하지 않는다. 신규 설치/서비스 기동/DB/실SMS/운영 시스템 변경/기존 자료 삭제 없음.
