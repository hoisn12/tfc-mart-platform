# UI1-SETUP 메인 보고

상태: 설정·의존성 준비 PASS, 앱 검증 진행 중. npm 신규 선택(기존 package/lock 없음). 루트 명세/이미지/기존 설계 보존. package/config/lockfile/README 메인 소유.

명령과 실제 결과:
- 기존 npm view 조회: DNS ENOTFOUND(실행 환경의 기본 network 제한). UI 구현 차단으로 해석하지 않고 허용된 npm install 경로로 진행.
- 최초 npm install React/Tailwind/...: vite metadata 조회에서 진행이 멈춰 세션 SIGINT 종료130. 파일 완료를 주장하지 않음.
- npm install React19.2.8/Vite7.3.6 명시 + 요청 의존성 --prefer-offline: 종료0, 71 packages.
- nvm20 source 후 dev dependencies install: network ENOTFOUND 종료1.
- npm install -D TS5.9.3/plugin-react5.2/Vitest3.2.7/Playwright1.62 등 허용 명령: 종료0, 89 packages. npm 실행 호스트 Node18.18.0의 EBADENGINE 경고 발생. 실제 실행·검사는 Node20.20.2에서 수행. 설치 경고를 실행 호환 검증으로 대체하지 않는다.
- python3 harness/scripts/validate.py: 종료0, staged-files strict config PASS(Codex0.166.0). native custom spawn NOT_RUN.
- python3 harness/scripts/check_gate.py --phase 1: 종료1, 하네스 활성화/실제 호출 검증 미완료. 기존 전체 gate 차단 유지, 검사기 변경 없음.

Native .codex 보호 경로는 수정/우회하지 않았다. 백엔드/DB/인프라/실발송/배포 없음. UI 자체 인수 판정은 별도 독립 검증으로 수행한다.

추가 확인:
- 최초 Vite 시작은 Tailwind native binding 누락으로 종료1. Node25.9.0에서 npm install 재실행으로 platform optional deps 3개 설치 종료0, 이후 Node20.20.2 Vite 시작 성공.
- 최초 npx playwright screenshot은 호스트 기본 Node18로 실행되어 >=20 필요 메시지 종료1. default sandbox Node20 Chromium launch는 MachPort 권한 거절로 종료1. 앱/브라우저 기능 실패와 구분하며 승인된 실행 환경에서 npm test 재검증 예정.
- 설치 감사가 Vite7.3.6/Vitest3.2.7/router6 관련 6개 취약점(3 moderate,1 high,2 critical)을 보고. 의존성 캐시의 실제 advisory 범위를 확인하고 Vite^7.3.7/Vitest^4.1.12/router-dom^7.18.0로 갱신. Node25 npm install 종료0, 4 추가/11 제거/16 갱신, 163 audited, found 0 vulnerabilities. offline npm audit의 0건은 온라인 감사 대체 증거로 사용하지 않음.
- Node20.20.2 Vite7.3.7 재기동 성공, Local http://127.0.0.1:5173/.

- 중간 npm run typecheck(Node20): 종료2, 아직 작성 중인 ImagesPage/MembersPage/SettingsPage import 3개만 누락. 나머지 작성된 소스 타입 오류 없음. 최종 완료 검증이 아니며 페이지 작성 후 재검증 예정.

- 이후 Node20 build에서 tsc 누락 종료127을 확인. 일부 dev dependency 디렉터리가 없고 symlink만 남은 설치 상태였다. frontend는 설치/정리를 실행하지 않았다고 확인. Node25 npm install 재실행 종료0(24개 추가/1개 갱신), audited163 취약점0. 원인은 확정하지 않는다.
- Node20 npm run build 재실행 종료0: Vite7.3.7 production build 성공. 초기 JS616.89kB chunk 경고를 확인하여 main 소유 Vite 설정에서 React/data 라이브러리를 분리한다. Zod 배포 소스의 PURE 주석 위치 경고2건은 기능 실패가 아닌 Rollup 주석 제거 안내다.
