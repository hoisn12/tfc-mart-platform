# PAGES-20261109 — 메인 검증

상태: 로컬 설정 검증 PASS. 독립 판정은 별도 reviewer 보고서. 실제 Actions 실행·Pages 게시/HTTP 접속은 NOT_RUN. 전체 Phase gate 승격 없음.

## 변경과 입력

사용자 요청에 따라 main push(직접 push 및 PR merge) 시 GitHub Pages 정적 데모 자동 게시 workflow를 추가했다. main 수동 실행도 지원한다. Node22/npm ci/단위 테스트/타입 검사 포함 build 후 frontend/dist artifact만 게시한다. 기본 contents:read, build는 메타데이터 조회용 pages:read, deploy에만 pages:write/id-token:write, 배포 concurrency 취소 없음, 비밀값 등록 없음.

configure-pages base_path를 Vite --base에 전달한다. VITE_GITHUB_PAGES=true에서만 HashRouter를 사용하며 기존 로컬 BrowserRouter 경로는 보존한다. README에 최초 Pages source 설정과 기본 URL/해시 URL을 안내했다. ADR010에 대안·영향·복구를 기록했다. 기존 계약과 package/lock/Vite config는 해시 동일하다. 입력/출력은 같은 접두 attempt-1의 manifest 및 before/snapshot에 보존한다.

## 실제 명령과 결과

지원 Node20.20.2 환경의 기존 설치 의존성으로 실행했다. CI는 Node22를 지정하며 CI 자체 실행은 NOT_RUN이다. 신규 설치/서비스 기동은 하지 않았다.

| 명령 | 종료 코드 | 결과 |
|---|---|---|
| npm run test:unit (frontend) | 0 | 1파일 12테스트 PASS |
| npm run build -- --outDir <temp>/local | 0 | TypeScript + 기본 Vite build PASS |
| VITE_GITHUB_PAGES=true npm run build -- --base /tfc-mart-platform/ --outDir <temp>/pages | 0 | TypeScript + Pages Vite build PASS |
| ruby -rpsych 로 workflow YAML parse | 0 | YAML 구문 PASS |
| Python 빌드 HTML asset 참조/파일 존재 및 입력 해시 검사 | 0 | 두 모드 경로·파일 존재 PASS, 계약/package/config 불변 |
| python3 harness/scripts/validate.py | 0 | staged-files PASS |
| python3 harness/scripts/check_gate.py --phase 1 | 1 | 기존 Phase0 미완료로 BLOCKED. 이번 변경의 배포 설정 검증과 구분 |

실행 로그와 명령별 종료 코드: `/var/folders/b7/qzhtg3355qx45cwnnrcb42880000gn/T/tfc-mart-pages-20261109-fltk0a28/{unit,local-build,pages-build}.log`, `results.json`. Vite의 기존 zod PURE 주석 경고 및 외부 outDir 안내가 있으나 지원 Node 경고나 build 실패는 없다. 새 임시 경로를 사용했고 기존 dist/데이터를 지우지 않았다.

## 미실행·위험·복구

실제 GitHub Actions/npm ci/Node22 런타임/원격 Pages 설정·배포/브라우저 E2E는 NOT_RUN이다. actionlint는 미설치여서 실행하지 않았고 설치 없이 Ruby Psych로 YAML 문법을 검사했다. 원격 Pages source=GitHub Actions 설정 및 main 반영 후 원격 검증이 필요하다. 외부 API/DB/실SMS/운영 리소스 변경 없음. 사이트는 합성자료 UI 데모이며 운영 기능을 완성했다고 주장하지 않는다.

실수한 README 문맥을 포함한 첫 apply_patch는 검증 실패로 파일 변경 없이 종료했고, 올바른 문맥으로 다시 적용했다.

복구는 before 원본과 이후 변경을 대조해 대상 설정만 되돌리는 후속 커밋을 main에 반영한다. 자동 게시 중지는 workflow 비활성화로 가능하다. 실제 rollback은 NOT_RUN. 기존 state/Phase gate는 보존한다.

## 독립 검토 실패와 시도 2

attempt-1 독립 검토에서 build job의 configure-pages가 호출하는 Pages API 읽기 권한 누락을 발견했다. 첫 판정 FAIL 원문은 PAGES-20261109-reviewer-attempt-1.md에 보존한다. 공개 저장소에서 성공할 수 있어도 비공개 저장소에서는 조회가 거부될 수 있으므로 build에 contents:read/pages:read를 명시했다. ADR의 권한 설명도 갱신했다. 동작 소스나 빌드 결과는 바뀌지 않아 테스트/빌드를 반복하지 않는다. 새 스냅샷 attempt-2를 동결하고 새 독립 reviewer 검토를 요청한다. 첫 YAML/asset/unit/build 성공이 원격 권한 검증을 의미하지 않는 점을 유지한다.
