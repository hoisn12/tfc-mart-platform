독립 검토 판정: **준비본 하네스의 문서·설정·검증 코드 PASS / 프로젝트 활성화 BLOCKED / 실제 Custom Agent 호출 NOT_RUN**.

이번 검토는 일반 협업 하위 Agent가 수행한 읽기 검토다. 프로젝트 Custom Agent의 로딩·호출 검증으로 간주하지 않는다. 파일을 수정하거나 비즈니스 기능을 구현하지 않았다.

검토 입력은 `harness/reports/setup/review-manifest.json`의 33개 파일이며, 전부 기록된 SHA-256과 일치했다.

- manifest SHA-256: `548d0fa5e2a667d3f2ba20a8430897e7787b4f8264c347a83916d4a79349ed1a`
- `checks.json`에 연결된 검증 로그 해시도 모두 일치했다.
- `backend/`, `frontend/`, `infra/`는 생성되지 않았다.
- 원본 명세·이미지·기존 설계는 보존됐으며 변경은 예정된 README 링크와 진행 기록 통합뿐이었다.

직접 재실행한 결과는 다음과 같다.

| 검사 | 결과 |
|---|---|
| `python3 harness/scripts/validate.py` | 종료 0, 준비본 TOML 6개 및 CLI 0.166.0 네이티브 strict 메인 설정 검사 PASS |
| `python3 -B -m unittest discover -s harness/tests -v` | 종료 0, 18개 모두 PASS |
| `python3 harness/scripts/validate.py --active` | 종료 1, `.codex/config.toml` 부재를 정상 감지 |
| `python3 harness/scripts/check_gate.py --phase 0` | 종료 1, 활성화·실제 호출 검증 미완료를 정상 차단 |

검토 중 발견했던 다음 항목은 수정본에서 해소됐다.

- 매 Phase의 OpenAPI·behavior 계약, 독립 계약 검토 및 메인 동결 증거를 gate 필수 조건으로 추가했다.
- Phase 1~5의 Backend·Frontend 산출물 스냅샷을 요구한다.
- 시도별 보관본으로 선행 검증 근거를 보존하면서 다음 Phase의 승인된 문서 변경을 허용한다.
- 스모크 프롬프트에 `activation=ACTIVE`, `runtime_evidence` 경로·해시 등록을 추가했다.
- 경로 탈출 테스트 fixture를 보완했고 최종 18개 테스트가 통과했다.

최종 입력에서 추가로 수정이 필요한 코드·문서 결함은 발견하지 못했다. 역할별 책임·쓰기 범위·산출물·완료 기준, 계약 이후 병렬 구현, 동일 파일 수정 금지, 독립 reviewer 판정, 실패·미실행 차단, 장애 복구·롤백·운영 안전성 기준이 구분돼 있다.

남은 차단 사항은 요청한 `.codex/` 설치와 실제 5개 Custom Agent 호출이다. 보호 경로 쓰기가 자동 승인 검토에서 거부돼 준비본만 존재한다. 사용자 권한으로 활성화하고 새 세션에서 정확한 역할 이름의 호출·결과 회수·독립 판정을 확인하기 전에는 전체 하네스 작동 완료나 Phase 0 착수 가능 상태로 보고하면 안 된다.

게이트 검사는 증거 구조·해시·선행 상태를 검증한다. 문서 의미, 명령 실행의 진실성, 검토자 신원, 파일 수정 규칙 준수를 강제하는 OS ACL이나 자동 스케줄러는 제공하지 않는다. 이 한계도 문서에 정확히 명시돼 있다.
