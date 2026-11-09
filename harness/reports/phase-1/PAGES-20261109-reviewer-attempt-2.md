판정: **PASS — Pages 배포 설정의 독립 정적 검토 통과**. 실제 원격 배포나 전체 Phase gate의 PASS를 의미하지 않는다. 파일 수정은 하지 않았다.

시도 1의 권한 결함은 해결됐다. build job에 `contents: read`, `pages: read`가 명시돼 `configure-pages@v5`의 Pages 조회 요구와 일치한다. 배포 쓰기 권한과 OIDC 권한은 deploy job에만 있다. [configure-pages 구현](https://raw.githubusercontent.com/actions/configure-pages/v5/src/api-client.js), [Pages 조회 API 권한](https://docs.github.com/en/rest/pages/pages#get-a-github-pages-site).

추가 결함은 발견하지 못했다.

- `main` push가 직접 push와 PR 병합을 처리하며 수동 실행도 `main`으로 제한한다.
- 설치→단위 테스트→타입 검사 포함 빌드→artifact 업로드→배포의 의존성이 맞다.
- Pages base 경로와 전용 HashRouter를 적용하고 기본 로컬 BrowserRouter를 유지한다.
- 최초 Pages 설정, 접속 URL, 배포 전제와 복구 방법을 문서화했다.
- 기존 계약·package·lockfile·Vite 설정 해시가 입력과 같다. 시도 2의 현재 파일과 고정 스냅샷 5개도 일치한다.

| 실행한 읽기 검사 | 종료 코드 | 결과 |
|---|---:|---|
| `cat`·`sed`로 규칙·명세·대상·보고서 읽기 | 0 | 범위·요구사항 대조 |
| Python SHA-256·snapshot·before 비교 | 0 | 출력 5파일 및 입력 보관본 일치 |
| Python 시도 1→2 diff | 0 | 권한과 문서 수정 확인 |
| Python `results.json`·로그 검사 | 0 | 단위 테스트 12개, 일반·Pages 빌드 종료0 증거 확인 |
| Python 빌드 asset 참조·파일 존재 검사 | 0 | 두 모드 각각 4개 참조 정상 |
| Ruby Psych YAML 구조 검사 | 0 | 이벤트·main 조건·권한·배포 의존성·concurrency 정상 |
| `cat frontend/package.json`, `git remote -v` | 0 | build 스크립트·접속 주소 대조 |

검토 출력 SHA-256:

```text
.github/workflows/pages.yml
01e2234b095166876f6bde6cbf4ea5451080b96a63239a4dd3d92219b33a8045

frontend/src/main.tsx
3bfed077d6515441f960602651570f4f3bffb82dfd03c22f7b294b3ba9a758e8

README.md
f3e8f50c8b9fbeb8f54f95c1d604095f59690be6899f9bb4fe98e56dc1d686db

docs/adr/010-github-pages-demo.md
58130c059e332a8930feb1fe061f93cbab87b75fb352d28344391c8c3ab457b2

harness/reports/phase-1/PAGES-20261109-main.md
ac42b1a445d3d94cf40577659a7525a83c7c4a874f94a9f4ff551515aab23869
```

입력 해시는 `PAGES-20261109-attempt-1/input-manifest.json`의 8개 항목을 보관본과 대조했다. 현재 수정 대상인 main.tsx와 README를 제외한 입력 파일도 일치한다.

테스트 재실행·설치·서비스 기동·GitHub 설정 변경·실제 Actions/Node22 실행·Pages 게시·브라우저 접속은 **NOT_RUN**이다. 확인한 실행 증거는 지원 Node20의 로컬 결과다. 저장소에서 Pages source를 GitHub Actions로 설정하고 변경을 main에 반영한 후 원격 실행을 확인해야 한다. 기존 Phase0 차단과 전체 Phase gate 미충족 상태는 유지해야 한다.
