판정: **FAIL — Pages 읽기 권한 수정 필요**. 이번 배포 설정에 한정한 판정이며 전체 Phase gate 또는 실제 배포 판정은 아니다. 파일은 수정하지 않았다.

발견 사항:

- **P2 · `.github/workflows/pages.yml:16`**: build job은 `contents:read`만 받지만 `configure-pages@v5`가 Pages 조회 API를 호출한다. 비공개 저장소에서는 필요한 `pages:read`가 없어 구성 단계가 실패할 수 있다. build job에 `permissions: {contents: read, pages: read}`를 추가하고 재검토해야 한다. 공개 리소스 조회에는 권한 예외가 있으므로 공개 저장소에서 반드시 실패한다는 의미는 아니다. 근거: [configure-pages 구현](https://raw.githubusercontent.com/actions/configure-pages/v5/src/api-client.js), [GitHub Pages API 권한](https://docs.github.com/en/rest/pages/pages#get-a-github-pages-site).

나머지 확인 사항은 충족했다. main push가 PR 병합을 포함하고 수동 실행은 main으로 제한된다. 테스트·빌드 실패 시 배포하지 않으며 artifact 경로와 deploy 의존성이 일치한다. Pages 전용 HashRouter와 base 경로, 로컬 BrowserRouter 보존, 최초 Pages 설정 안내, ADR의 대안·복구 설명을 확인했다.

실행한 읽기 검사와 결과:

| 명령·검사 | 종료 코드 | 결과 |
|---|---:|---|
| `cat`으로 규칙·원본 명세·대상·보고서·manifest 읽기 | 0 | 요구사항 및 범위 대조 |
| Python SHA-256·snapshot·before 대조 | 0 | 출력 5파일 일치, 입력 보관본 일치, 기존 계약/package/config 불변 |
| Python 빌드 HTML asset 참조·파일 존재 검사 | 0 | local/pages 각각 4개 참조 정상 |
| Python `results.json`·로그 검사 | 0 | 단위 테스트 12개 및 두 빌드 종료0 증거 확인 |
| `ruby -rpsych` YAML 읽기 | 0 | YAML 구문 정상 |
| `nl`, `cat frontend/package.json`, `git remote -v` | 0 | 행 위치·build 스크립트·기본 URL 대조 |

검토 출력 SHA-256:

```text
.github/workflows/pages.yml
6146384a05ecb4d03c0d4b30799a2e3452e5f7be337895817850e3c40476e62b
frontend/src/main.tsx
3bfed077d6515441f960602651570f4f3bffb82dfd03c22f7b294b3ba9a758e8
README.md
f3e8f50c8b9fbeb8f54f95c1d604095f59690be6899f9bb4fe98e56dc1d686db
docs/adr/010-github-pages-demo.md
9856887ab01a63b58153d617e6a1172716632ea6600a991053f9970827b6152c
harness/reports/phase-1/PAGES-20261109-main.md
9a1354ced4fa0553562f1685e13bbb2c7c21e4aac53c69ab171a3ba135518844
```

입력 해시는 `PAGES-20261109-attempt-1/input-manifest.json`의 8개 항목 모두 보관본과 대조했다. 수정 대상으로 지정된 main.tsx와 README를 제외한 현재 파일도 입력 해시와 일치했다.

테스트 재실행·서비스 기동·설치·원격 설정·Actions 실행·Pages 게시·브라우저 접속은 **NOT_RUN**이다. 기존 로그는 Node20 로컬 결과이고 CI의 Node22 실행 증거는 없다. 기존 Phase0 차단과 phase-1 gate 미충족은 보존해야 한다.
