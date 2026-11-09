# ADR 010 — GitHub Pages UI 데모 자동 배포

상태: 2026-11-09 사용자 요청에 따른 배포 설정 결정. 원격 배포 검증 전.

## 배경과 대안

사용자가 main push 또는 PR merge 후 GitHub Pages에서 UI 데모를 볼 수 있도록 Actions 추가를 요청했다. 기존 UI 전용 범위에 정적 데모 게시만 추가하며 실제 운영 시스템 배포와 전체 Phase gate 승격을 의미하지 않는다. 기존 동결 계약 원본은 보존한다. 이 ADR은 Pages의 배포 경로와 URL 표현에 대한 추가 결정이다.

대안은 BrowserRouter + 서버 rewrite, 404.html 우회, Pages 전용 HashRouter다. Pages에는 SPA 서버 rewrite가 없고 404 우회는 오류 응답/리다이렉트에 의존하므로 Pages 빌드에서만 HashRouter를 선택한다. 내부 화면 경로는 기존 계약대로 유지한다.

## 결정

- `push.branches: [main]`으로 직접 push와 PR merge를 한 번씩 처리한다. 수동 실행도 main만 허용한다.
- Node 22, lockfile 기반 npm ci, 단위 테스트, TypeScript 포함 build 후 frontend/dist만 Pages artifact로 업로드한다.
- configure-pages의 base_path를 Vite CLI의 --base로 전달해 저장소 하위 경로와 루트/커스텀 도메인에 대응한다.
- 빌드 환경 `VITE_GITHUB_PAGES=true`에서만 HashRouter를 사용한다. Pages URL은 `/tfc-mart-platform/#/products` 형태며 로컬 BrowserRouter 동작은 보존한다.
- contents:read를 기본으로 하고 deploy job만 pages:write/id-token:write를 받는다. 배포는 github-pages 환경에서 직렬 처리하며 실행 중 배포를 취소하지 않는다.
- 별도 비밀값/백엔드/실제 SMS/DB 없이 기존 합성자료 데모만 게시한다. 저장소 Pages source는 GitHub Actions로 한 번 설정해야 한다.

## 영향·복구·검증

Pages에 게시되는 UI와 번들에는 비밀값/실데이터를 포함하지 않는다. UI의 LocalStorage와 데모 권한 한계는 기존과 같다. 로컬 개발과 일반 빌드는 기존 경로를 사용한다. 기존 BrowserRouter URL을 Pages의 직접 경로로 사용하면 404이므로 공유 링크는 hash 경로를 사용한다.

복구는 문제 변경을 되돌리는 후속 커밋을 main에 반영해 이전 정상 버전을 재배포한다. 자동 게시 중지는 workflow 비활성화로 수행한다. 기존 자료 삭제, git reset/clean, 운영 인프라 변경은 하지 않는다. 실제 복구/배포는 이번 로컬 설정 작업에서 실행하지 않는다.

검증은 로컬/Pages 두 빌드, 단위 테스트, Pages asset base 및 hash 모드 검사, 독립 읽기 리뷰다. 원격 Actions와 Pages HTTP 접속 성공은 main 반영·Pages 설정 후 별도 확인하며 로컬 성공으로 대체하지 않는다.

근거: [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), [Vite 정적 배포](https://vite.dev/guide/static-deploy.html#github-pages).
