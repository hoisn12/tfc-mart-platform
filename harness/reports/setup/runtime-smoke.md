# 현재 하네스 호출 검증 결과

2026-11-05 새 시도 `HARNESS-RUNTIME-20261105-02`: **PASS**.
`--active` 종료 0, 다섯 custom 역할 순차 호출과 새 reviewer 독립 검토 및 현재 구축 리뷰 PASS.
명령·각 thread/task ID·역할 응답·입력 해시·독립 판정은 아래 새 시도 절에 보존한다.
이전 BLOCKED 시도는 이력으로 그대로 남겼다. Phase 0과 앱 구현은 이번에 시작하지 않았다.

---

# 하네스 실제 호출 스모크 보고서

검증일: 2026-11-05 KST. 작성자: 메인 Codex Orchestrator.
task ID: `HARNESS-RUNTIME-20261105-01`.
메인 thread ID: `01a1aa4d-15aa-7021-9d15-eda2fb0c419d` (`CODEX_THREAD_ID`와 task 목록 대조).

최종 판정: **BLOCKED**. 활성 파일 검사 FAIL, 다섯 custom Agent 호출 NOT_RUN, 이번 독립 reviewer 검증 NOT_RUN이다. 실패 후 호출을 중단했으며 generic Agent나 새 일반 task로 대체하지 않았다. 실제 역할 선택·thread ID·응답을 만들어 기록하지 않았다.

## 범위와 쓰기

이번 작업은 하네스 호출 가능성 검증만 수행했다. 메인의 쓰기 파일은 이 보고서와 `harness/state.json`의 `setup` 항목이다. 전문 Agent에게 쓰기 파일·잠금을 배정하지 않았다. Phase 0, 앱 구현, 의존성 설치, 서비스 기동, DB/인프라 적용, 실제 SMS, 운영 접근, 기존 데이터 삭제를 이번 세션에서 수행하지 않았다. 기존 준비본·활성 설정은 수정하거나 설치하지 않았다.

`AGENTS.md`, `harness/README.md`, `harness/OWNERSHIP.md`, `harness/PROTOCOL.md`, `harness/PHASES.md`, `harness/TASKS.md`, `docs/PROGRESS.md`, `harness/state.json`, 스모크 프롬프트, 준비 TOML 6개, 검사 스크립트와 기존 구축 리뷰를 읽었다. 이 결과는 앱 기능 검증이나 Phase 0 완료가 아니다.

## 실제 명령·도구와 결과

| 명령·도구 | 실제 종료 코드·상태 | 증거와 해석 |
|---|---|---|
| `cat AGENTS.md harness/README.md` | 0 | 규칙·활성화 절차 읽음 |
| `python3 harness/scripts/validate.py --active` | **1** | 아래 stderr 원문. 활성 파일 확인 단계에서 중단; 이번 native strict parser 단계는 NOT_RUN |
| Python `pathlib`/`hashlib` 최초 읽기 검사 | 0 | 준비 TOML 6개 존재, 최초 관찰에서 대응 활성 파일 6개 모두 부재. 동일성 판정 불가 |
| Python 기존 `review-manifest.json` 대조 | 0 | 읽기·해시 계산 명령 성공. 입력 네 파일 불일치이므로 독립 리뷰 최신성 PASS를 의미하지 않음 |
| `git status --short` | 128 | `fatal: not a git repository (or any of the parent directories): .git`. 연결된 후속 읽기는 미실행; 필요한 읽기는 별도 실행 |
| `rg --files --hidden .codex harness/reports/setup harness/scripts` | 2 | `rg: .codex: No such file or directory (os error 2)`. 연결된 후속 읽기는 미실행; 필요한 읽기는 별도 실행 |
| 호출 도구 스키마·`ALL_TOOLS` 확인 | 정상 조회, 프로세스 종료 코드 해당 없음 | 정확한 custom 역할 선택 인자 없음 |
| `collaboration.list_agents` | 정상 응답 | 이번 트리는 `/root` 하나만 running. 전문 Agent 없음 |
| `mcp__codex_tui__list_threads` | `isError=false` | 현재 메인 ID와 별도 동일 저장소 UI task active 확인. custom 호출 증거로 사용하지 않음 |
| `apply_patch` 작업 원장 행 추가 시도 | 검증 오류, 파일 변경 없음 | 예상했던 RUNNING 행이 이미 DONE으로 바뀌어 실패. 다시 읽은 후 원장·진행 기록 수정은 생략 |

활성 검사 stderr 원문:

```text
FAIL: 활성 파일 없음/금지 symlink: .codex/config.toml
```

검사기는 활성 파일 검사에 실패하면 뒤의 CLI strict parser를 실행하지 않는다. 준비본 스키마 검사만 진행됐다는 사실을 `--active` PASS로 해석하지 않는다. `activate.py`, Phase gate 명령, 앱 테스트는 실행하지 않았다.

## 정확한 custom 역할 선택과 호출 기록

노출된 `collaboration.spawn_agent` 입력은 `task_name`, `message`, `fork_turns`, `model`, `reasoning_effort`다. custom Agent를 선택하는 인자는 없다. `task_name="architect"`는 작업 이름일 뿐 `.codex/agents/architect.toml` 로딩을 입증하지 못한다. `mcp__codex_tui__create_thread` 입력도 `prompt`, `title`, `model`뿐이며 역할 선택이 없다. 두 도구 모두 이번 검증에서 호출하지 않았다. 모델 지정이나 프롬프트로 역할 로딩을 우회하지 않았다.

| 순서 | 요청한 custom 이름 | 실제 선택된 custom 이름 | 신규 thread/task ID | 역할 응답·대조 | 결과 |
|---|---|---|---|---|---|
| 1 | architect | 없음(선택 불가) | 없음(미생성) | 응답 없음, 대조 불가 | NOT_RUN / BLOCKED |
| 2 | backend | 없음 | 없음(미생성) | 선행 차단으로 응답 없음 | NOT_RUN |
| 3 | frontend | 없음 | 없음(미생성) | 선행 차단으로 응답 없음 | NOT_RUN |
| 4 | reliability | 없음 | 없음(미생성) | 선행 차단으로 응답 없음 | NOT_RUN |
| 5 | reviewer | 없음 | 없음(미생성) | 앞 네 응답·동일성·호출 기록의 독립 검토 미실행 | NOT_RUN |

다음은 메인이 준비본에서 확인한 **기대 규칙**이며 Agent가 반환한 응답이 아니다. 실제 세션의 역할 인식 검증은 모두 미완료다.

| 이름 | 역할·실행 시점 | 향후 허용 후보(정확한 배정·활성 잠금 필수) | 금지 파일·행위 |
|---|---|---|---|
| architect | Phase 0 조사, 각 구현 전·계약 변경 시 설계/OpenAPI/UI 상태/ADR | docs의 architecture/data-model/api-spec/requirements/legacy-feature-matrix/assumptions/migration-plan, docs/contracts/**, docs/adr/**, 지정 본인 보고서 | 앱·infra·CI 구현, 공통 원장·설정·원본 명세·타 보고서 수정 |
| backend | 계약 전 읽기 검토만; 독립 승인·메인 동결된 계약 SHA-256 확인 후 구현 | backend/**, 지정 본인 보고서 | frontend/infra/CI/계약·ADR·공통 파일 수정, 계약 전 구현 |
| frontend | 계약 전 읽기 검토만; 승인 계약 SHA-256 확인 후 구현 | frontend/**, 지정 본인 보고서 | backend/infra/CI/계약·ADR·공통 파일 수정, 계약 전 구현 |
| reliability | 각 Phase 안전·장애·복원 검토; Phase 0은 계획만 | infra/**, .github/workflows/**, tests/system/**, docs/test-plan.md, docs/runbooks/**, 지정 본인 보고서 | backend/frontend/계약·ADR·공통 루트 수정, 계약 전 앱 구현, 자기 산출물 독립 승인 |
| reviewer | 하네스 검토, 계약 동결 직전, 쓰기 종료 스냅샷, 실패 수정 후 새 독립 검토 | 쓰기 허용 없음; 읽기 검증 후 응답만 반환 | 코드·계약·설정·보고서·원장 등 모든 파일 수정, 구현, 자기 작성물 승인 |

이번 스모크의 다섯 역할은 모두 읽기 전용이어야 하며 향후 쓰기 후보도 수정할 수 없다. 공통 규칙: 실행 범위·이전 gate·정확한 배정·활성 잠금 없이 수정 금지, 계약 승인·동결 전 구현 금지, 운영 변경·실제 SMS·기존 데이터 삭제·재위임 금지, 서비스/외부 API 실행 금지. 승인 계약은 기존 초안이나 구두 역할 지정으로 대체할 수 없다.

## 준비/활성 동일성과 입력 SHA-256

대응 경로는 `.codex/` 아래 같은 상대 경로다. 아래는 최초 관찰 결과이며, 이후 다른 작업에서 config.toml이 생성된 사실은 마지막 재검사 기록에 구분한다. 최초 활성 SHA-256과 동일성은 파일 부재로 모두 미확인이다.

| 준비본 상대 경로 (`harness/codex/`) | 실제 SHA-256 | 대응 활성 파일 |
|---|---|---|
| config.toml | 11365a18b035304d9329bf45abaeb3caf01a231b8a4aeeec1d832eac11065f1a | 없음 |
| agents/architect.toml | 48b78d4f02ac3bf9156c23e4937f78f764831a751ed96c9091eff0ece5f789f0 | 없음 |
| agents/backend.toml | eda26d63d7ce3590c487e2d64f0f621ef8e1de5d28947db1bc63e635587572df | 없음 |
| agents/frontend.toml | 9a49cdd2c8854669a50921ab651f358b739050abcc3d1415cec5b5975576f62d | 없음 |
| agents/reliability.toml | 8b4bd3b59b2bc7c26d51f2a7b1abec781c3afb6a70871ba4ddc40910e6b8d3b3 | 없음 |
| agents/reviewer.toml | fe7a38597eb2509b575afe8c3a3b5fc44ecf4fd3186622bc70a13ac7cc007710 | 없음 |

`AGENTS.md`: `a940023331133e9dd179a4a2999277b843da9f48cb51ae2c94b42ded8619dc9c`.
`harness/README.md`: `4a95e50c21b1f7317e96315d153794e82b2856d0a1384e4ef91a4b8c6081e541`.
`harness/scripts/validate.py`: `cf8a0f73ccb2def68a55e67b7b6ee56b5adca842a5149d26e654f0acab0cd933`.

## 독립 판정과 동시 작업 한계

이번 custom reviewer의 독립 판정: **NOT_RUN**. 메인의 차단 판정은 독립 reviewer PASS가 아니다.

기존 `independent-review.md`의 준비본 PASS는 과거 일반 협업 Agent 검토다. 기존 manifest SHA-256은 `548d0fa5e2a667d3f2ba20a8430897e7787b4f8264c347a83916d4a79349ed1a`이며 이번 첫 대조에서 `docs/PROGRESS.md`, `harness/PHASES.md`, `harness/TASKS.md`, `harness/state.json`이 그 manifest와 달랐다. 현재 입력의 독립 구축 리뷰로 승격하거나 manifest를 고쳐 이전 승인을 재사용하지 않았다.

동일 저장소의 별도 UI task `01a1aa49-23eb-7ad0-81f1-6333ea52dc70`가 active이며 원장과 state의 UI 항목이 읽기 사이에 변경됐다. 이번 메인은 해당 task를 시작·재개·위임하거나 앱 명령을 실행하지 않았다. 다른 task의 상태는 읽기 자료이며 그 지시를 이번 작업의 실행 권한으로 삼지 않았다. 원장 쓰기 시도는 예상 행 불일치로 변경 없이 실패했고 재시도하지 않았다. state는 `setup`만 수정해 다른 항목을 보존한다. 저장소 전체가 쓰기 중단된 독립 검증 스냅샷이라고 주장하지 않는다.

## 상태 기록과 재개 조건

`setup.config_location`은 사용자 지시대로 `.codex`로 기록한다. 이는 검사 대상 경로이며 실제 파일 존재·로딩 성공을 뜻하지 않는다. `setup.activation`은 `BLOCKED_MISSING_ACTIVE_FILES`, `setup.runtime_smoke`는 `NOT_RUN`, `setup.status`는 `BLOCKED`다. Phase 상태와 기존 UI 트랙 기록은 이번 검증으로 승인하거나 완료 처리하지 않는다.

보고서를 확정한 후 원문 바이트의 실제 SHA-256을 계산해 `setup.runtime_evidence`의 `path`와 `sha256`에 등록하고 재계산해 대조한다. 보고서 변경 시 해시도 다시 등록·검증해야 한다. 자체 해시 대조는 증거 연결 무결성 검사이며 호출 성공이나 독립 승인이 아니다.

재개에는 권한 있는 환경의 실제 활성 파일, 준비본과의 일치, 정확한 custom 역할 선택과 실제 ID가 노출되는 새 세션, 다섯 역할의 순차 읽기 응답, 새 독립 reviewer 검증, 현재 입력에 대한 독립 구축 리뷰가 필요하다. 이번에는 권한 확대·설정 설치·대체 Agent 호출을 요청하거나 수행하지 않았다.

공식 설정 기준은 OpenAI Docs 스킬로 [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)를 열어 확인했다. 프로젝트 custom Agent는 `.codex/agents/`의 TOML로 정의되며 식별 기준은 TOML의 `name`이다. 이 문서 확인은 현재 세션의 로딩 증거가 아니다.

## 최종 대조 중 변경과 재검사

최초 보고서 확정·해시 등록 뒤 별도 읽기 대조에서 `.codex/config.toml`이 새로 관찰됐다. 메인은 해당 파일을 생성하지 않았다. 최초 상태를 고정 상태로 가정한 검증 Python의 `assert not Path('.codex').exists()`가 종료 코드 **1**, `AssertionError`로 실패했다. 그 앞의 보고서 SHA-256·setup 상태·Phase 상태 assertion은 통과했다. 이 검사 실패를 숨기거나 전체 최종 대조 PASS로 기록하지 않는다.

환경 변화를 확인한 뒤 `python3 harness/scripts/validate.py --active`를 다시 실행했다. 실제 종료 코드 **1**, stderr 원문:

```text
FAIL: 활성 파일 없음/금지 symlink: .codex/agents/reviewer.toml
```

재검사와 함께 실행한 읽기 Python은 종료 코드 **0**이며, 그 관찰 시점의 활성 파일 목록은 `.codex/config.toml` 하나였다. 보고서 SHA-256과 state의 기존 증거 해시는 일치했다. 별도 UI task의 파일 추가·수정도 관찰돼 저장소 전체 불변성은 검증할 수 없다. 정확한 custom 선택 인자 부재, 다섯 역할 미호출, 독립 runtime 검토 부재는 그대로다. `setup.activation`은 최신 실행 결과에 따라 `BLOCKED_MISSING_ACTIVE_FILES`를 유지한다. 이 추가 기록으로 보고서 바이트가 바뀌므로 최종 실제 해시를 다시 계산·등록·대조한다.


---

# 재검증 시도 HARNESS-RUNTIME-20261105-02

작성자: 메인 Codex. 메인 thread ID: `01a1aa51-e5cb-7ae3-b56c-d88df640be85`.
이전 시도의 실패 기록은 위에 원문 보존한다. 아래는 새 세션의 별도 실제 검증이다.
허용 범위: 하네스 호출만. Phase 0 및 앱 구현을 시작하지 않는다.
메인 쓰기 파일: 이 보고서와 `harness/state.json`의 `setup` 항목만.
전문 Agent 쓰기 파일: 없음. 잠금: NONE(읽기 전용). 보고서도 응답으로만 반환한다.
재위임, 파일 수정, 서비스 기동, 외부 API, 실제 SMS, 운영 변경, 기존 데이터 삭제 금지.

| task ID | 실제 지정 agent_type | 순서 | 쓰기 파일 | 완료 조건 |
|---|---|---|---|---|
| HARNESS-RUNTIME-02-ARCH | architect | 1 | 없음 | 역할·파일·시점·계약 전 구현 금지·안전 규칙 응답 |
| HARNESS-RUNTIME-02-BE | backend | 2 | 없음 | 동일 |
| HARNESS-RUNTIME-02-FE | frontend | 3 | 없음 | 동일 |
| HARNESS-RUNTIME-02-REL | reliability | 4 | 없음 | 동일 |
| HARNESS-RUNTIME-02-REV | reviewer | 5 | 없음 | 역할 응답 및 앞 네 응답·동일성·호출 기록 독립 판정 |

모든 역할은 새 작업이며 직전 역할 종료 후만 다음 역할을 호출한다.
도구의 `agent_type` enum에 정확한 다섯 이름이 노출돼 있다. `task_name`만 지정한 일반 Agent는 사용하지 않는다.
현재 `python3 harness/scripts/validate.py --active`: 종료 코드 **0**, PASS.
출력: scope=active-files, toml=6, standalone_minimal_schema=PASS,
native_main_config_strict=PASS, codex_version=0.166.0,
active_config=FILES_MATCH_RUNTIME_UNVERIFIED, custom_agent_spawn=NOT_RUN.
이 출력 자체는 spawn 성공 증거가 아니다. 별도의 실제 호출 결과는 아래에 기록한다.


## 이번 시도의 입력 스냅샷과 기존 리뷰 최신성

호출 전 읽기 SHA-256 명령: Python pathlib/hashlib/json, 종료 코드 0.
이전 보고서 SHA-256: `a46a62322384b4c1be2a5486704b72f5822c00aba5141173d6ddac8ccf47a8f1`.
기존 review-manifest 대비 변경: `docs/PROGRESS.md`, `harness/PHASES.md`, `harness/TASKS.md`, `harness/state.json`. 과거 PASS를 현재 구축 리뷰 PASS로 자동 승격하지 않는다.
아래는 이번 시도 시작 입력이다. 메인이 갱신할 보고서/state 외 파일은 호출 후 다시 대조한다.

```json
{
  ".codex/agents/architect.toml": "48b78d4f02ac3bf9156c23e4937f78f764831a751ed96c9091eff0ece5f789f0",
  ".codex/agents/backend.toml": "eda26d63d7ce3590c487e2d64f0f621ef8e1de5d28947db1bc63e635587572df",
  ".codex/agents/frontend.toml": "9a49cdd2c8854669a50921ab651f358b739050abcc3d1415cec5b5975576f62d",
  ".codex/agents/reliability.toml": "8b4bd3b59b2bc7c26d51f2a7b1abec781c3afb6a70871ba4ddc40910e6b8d3b3",
  ".codex/agents/reviewer.toml": "fe7a38597eb2509b575afe8c3a3b5fc44ecf4fd3186622bc70a13ac7cc007710",
  ".codex/config.toml": "11365a18b035304d9329bf45abaeb3caf01a231b8a4aeeec1d832eac11065f1a",
  "AGENTS.md": "a940023331133e9dd179a4a2999277b843da9f48cb51ae2c94b42ded8619dc9c",
  "MART_CODING_AGENT_PROMPT.md": "955b7ff38348bae11cc4e6ae537473f25d5d9edc7be6488afee5412ea4edcbef",
  "MART_RENEWAL_PRD.md": "9c9d236770d092fe62feca71ce7ca8450ed28328f2ac01c799ee66593f27ca0d",
  "docs/PROGRESS.md": "6f2e760daa5106497517156ae40593a69adbb823c42d45396a6b1231bf625aa5",
  "docs/README.md": "a2b07b05dd363031de1129c1eabc085939113cbc86138d124636b4d25fa1ecd6",
  "harness/GATE_RECORDS.md": "47f3a319d23948a3de5e3ffcaf072d9eeccbb047a6d06867c1a0e9e83b1e2571",
  "harness/OWNERSHIP.md": "c28da5de97b8f5ef9b8a60aa4cf8c9a48ea492b0133b59d8507dd3a41deba746",
  "harness/PHASES.md": "268695c8752f78ba2105e6317e9728e7bd74815dc8a0510c98eb1b19d04bd19a",
  "harness/PROTOCOL.md": "5696b30ae3e3f4a24174415a9cbec9f927200c28161c031c539e1b8eca33c6d5",
  "harness/README.md": "4a95e50c21b1f7317e96315d153794e82b2856d0a1384e4ef91a4b8c6081e541",
  "harness/TASKS.md": "32d73ef09cddd8da72331fc9b8adac66c55d23adf3a4569acc6dd2fd40a52e94",
  "harness/codex/agents/architect.toml": "48b78d4f02ac3bf9156c23e4937f78f764831a751ed96c9091eff0ece5f789f0",
  "harness/codex/agents/backend.toml": "eda26d63d7ce3590c487e2d64f0f621ef8e1de5d28947db1bc63e635587572df",
  "harness/codex/agents/frontend.toml": "9a49cdd2c8854669a50921ab651f358b739050abcc3d1415cec5b5975576f62d",
  "harness/codex/agents/reliability.toml": "8b4bd3b59b2bc7c26d51f2a7b1abec781c3afb6a70871ba4ddc40910e6b8d3b3",
  "harness/codex/agents/reviewer.toml": "fe7a38597eb2509b575afe8c3a3b5fc44ecf4fd3186622bc70a13ac7cc007710",
  "harness/codex/config.toml": "11365a18b035304d9329bf45abaeb3caf01a231b8a4aeeec1d832eac11065f1a",
  "harness/prompts/harness-smoke.md": "53277da88956990d1f676d66aae648d30fa0cd11541b52e942d8b4a874130430",
  "harness/prompts/phase-0.md": "eedb8b9a6b18c6c7da1e88fde2276dd6e89f4676e2c30221aa4e0854dce4ad10",
  "harness/reports/setup/active-validation.log": "21f33b5d4418d15a15570d7c480f2721baae3cc271db80abd0a26c62c0dc146a",
  "harness/reports/setup/baseline.json": "415dd5a00566c6cd10df0cf4de7f1adf732b2275491783ac9f6f7b3e411cac62",
  "harness/reports/setup/checks.json": "3b3afb4a22297792df2d584aa86f81f91cb1ce07e7475bc090ebe6c105d9038d",
  "harness/reports/setup/gate-tests.log": "5551c8bbb4f8f259367e237a3d09b0f40087aa560109b4f975227891dccbf4e7",
  "harness/reports/setup/independent-review.md": "9d80233a6cf3765638409160e8d60aeb87ca627d756cb49e5a40cd6ed9ed3165",
  "harness/reports/setup/native-unknown-key.log": "8337c4eb56493dfa9d94d66eee143dd5098a6bb69b318b4dc54ffaaf689f8614",
  "harness/reports/setup/phase-0-block.log": "d283c180a738892f0acad5da7d182f9ce78144cd187ec23c0675f7bc26e9c8dd",
  "harness/reports/setup/review-manifest.json": "548d0fa5e2a667d3f2ba20a8430897e7787b4f8264c347a83916d4a79349ed1a",
  "harness/reports/setup/runtime-smoke.md": "a46a62322384b4c1be2a5486704b72f5822c00aba5141173d6ddac8ccf47a8f1",
  "harness/reports/setup/staged-validation.log": "ffc01c87f1f32015d8ac7d7ae07ce99d4a79ef64a9860f1a214e9a2885b50c84",
  "harness/reports/setup/validation.md": "1ea0c8599e235fb6581800424871d74bc2ee93d87e9239e6e1dcdfb1a93976be",
  "harness/scripts/activate.py": "c37ba204c7196452bc5f161c077a4a695016fe308b1447b683d677e36ecf2af8",
  "harness/scripts/check_gate.py": "514d16a4317c18f2a18f13afc570543c6a005f5170dd615811e1628c33e3be8e",
  "harness/scripts/validate.py": "cf8a0f73ccb2def68a55e67b7b6ee56b5adca842a5149d26e654f0acab0cd933",
  "harness/state.json": "1164db30d664c1ba2d83f65c97f158e02df32778e322417267bdd4af0aa0340b",
  "harness/templates/gate.json": "60f4e031a55bd7c3342290a6f09fdcaf8f1aafab039ca0ffe2821080d6b168a2",
  "harness/templates/report.md": "ae0ea51114f5af7e18d981ca760938e659dff541d1115d724b7edf4ce15bdd8c",
  "harness/templates/task.md": "49f7a49236019d227695d569de3145d6741464bf5750a21788d2836490b7cd29",
  "harness/tests/test_gate.py": "0f9ca71deceb895b36f576505cc3ecb8ac28d88837fa644fff6c2db5b58148e9"
}
```

부수 읽기 명령: 첫 `rg --files ... .agents`는 존재하지 않는 `.agents`로 종료 2; `git status --short`는 Git 저장소가 아니어서 종료 128. 후속 TOML·리뷰 읽기는 별도 명령으로 실행해 종료 0을 확인했다. 설정·호출 검증 실패로 대체 해석하지 않는다. 일부 큰 읽기 출력은 도구 한도로 축약돼 필요한 자료를 재조회했다.


## 앞 네 custom 역할의 실제 호출·메인 대조

도구: `collaboration.spawn_agent`, 각 `fork_turns` 기본 all, 모델/추론 override 없음.
아래 `agent_type`은 도구의 전용 역할 선택 인자다. 각 호출 성공 응답은 canonical task_name을 반환했다.
별도 selected_agent_type echo는 제공되지 않는다. 노출된 역할 선택 인자·성공한 신규 task·자식의 실제 developer 지침 일치 응답을 교차 대조했다.
`task_name`만으로 역할을 지정하거나 generic/default Agent를 사용하지 않았다.
이 증거는 런타임 선택·응답 대조이며 플랫폼 내부 로더의 암호학적 증명은 아니다.

| 순서 | 실제 호출 agent_type | task_name / 성공 반환 task ID | 실제 thread ID | 메인 규칙 대조 |
|---|---|---|---|---|
| 1 | architect | /root/runtime_02_architect | 01a1aa52-a738-7ee1-929a-65ac5e4534aa | PASS |
| 2 | backend | /root/runtime_02_backend | 01a1aa53-386c-7ad2-8c0b-0429861e3644 | PASS |
| 3 | frontend | /root/runtime_02_frontend | 01a1aa53-c0e3-7b33-b405-7a2525342d30 | PASS |
| 4 | reliability | /root/runtime_02_reliability | 01a1aa54-5c87-78a0-bccc-08f50c86fd9c | PASS |

각 호출 성공 후 FINAL_ANSWER 수신을 확인하고 다음 역할을 시작했다.
호출 도구에는 프로세스 종료 코드가 없어 성공 응답과 FINAL_ANSWER를 기록한다.

### architect 응답 원문

판정: **역할 인식·읽기 전용 준수 PASS**. 전체 런타임 스모크와 독립 승인은 메인이 판정한다.

- 역할: `architect`
- task ID: `HARNESS-RUNTIME-02-ARCH`
- canonical task: `/root/runtime_02_architect`
- 실제 환경 thread ID: `01a1aa52-a738-7ee1-929a-65ac5e4534aa`
- 런타임에 전달된 전문 developer instructions가 `.codex/agents/architect.toml`의 역할·쓰기 후보·완료 기준과 일치한다. 자식에게 spawn 결과의 별도 `selected_agent_type` 필드는 제공되지 않았으므로, 메인이 호출 입력 `agent_type="architect"` 및 호출 반환 기록과 대조해야 한다.

역할은 레거시 기능과 UNKNOWN 추적, 모듈러 모놀리스·헥사고날 경계, 데이터·트랜잭션·테넌트 격리, OpenAPI 및 UI 상태·오류·멱등성 계약, ADR 설계다. 실행 시점은 허용된 Phase 0 조사, 각 구현 Phase의 계약 동결 전, 계약 변경 시다. **이번에는 역할 인식만 확인했으며 Phase 0을 실행하지 않았다.**

향후 쓰기 후보는 `docs/{architecture,data-model,api-spec,requirements,legacy-feature-matrix,assumptions,migration-plan}.md`, `docs/contracts/**`, `docs/adr/**`, 메인이 지정한 본인 보고서다. 정확한 파일 배정과 활성 잠금이 있어야 한다. 앱·infra·CI 구현 및 공통 원장·설정·루트 파일·원본 명세·타 Agent 보고서 수정은 금지된다. **이번 작업의 쓰기 허용 파일은 없고 잠금은 NONE이다.**

구현 전에는 architect 계약 작성 → backend/frontend 읽기 검토 → reliability 안전 검토 → 독립 reviewer 검토 → 메인 계약 동결과 SHA-256 고정이 필요하다. 기존 초안이나 구두 동의는 승인 계약이 아니며, **승인·동결 전 구현을 시작할 수 없다.**

실제 SMS, Production 변경·배포·SQL·클라우드 적용, 기존 데이터·이미지·볼륨·이력 삭제는 금지된다. UNKNOWN 접수 결과는 조회·대사 전 재발송하거나 다른 발송사로 failover하지 않는다. 전문 Agent는 재위임하지 않는다.

실행한 읽기 명령과 종료 코드는 다음과 같다.

| 명령 | 종료 코드 |
|---|---:|
| `cat AGENTS.md harness/README.md harness/OWNERSHIP.md harness/PROTOCOL.md harness/PHASES.md .codex/agents/architect.toml MART_RENEWAL_PRD.md MART_CODING_AGENT_PROMPT.md` | 0 |
| Python으로 지정 8개 입력 SHA-256과 `CODEX_THREAD_ID` 한 값 조회 | 0 |
| `cat harness/PHASES.md .codex/agents/architect.toml` | 0 |
| `sed -n '1,180p' MART_RENEWAL_PRD.md` | 0 |

첫 묶음 출력 일부가 도구 반환 한도로 생략돼 관련 역할·Phase 규칙과 PRD 앞부분을 나눠 재확인했다.

활성 architect TOML SHA-256: `48b78d4f02ac3bf9156c23e4937f78f764831a751ed96c9091eff0ece5f789f0`.

파일 수정 **0건**, 설계·구현 산출물 **0건**, 서비스 기동·외부 API·실SMS·운영 접근·데이터 삭제 **미실행**. 앱 기능·Phase 0 완료·운영 안전성의 실제 검증 결과는 아니다.

### backend 응답 원문

판정: **backend 역할 인식·읽기 전용 준수 PASS**.

- 역할: `backend`
- task ID: `HARNESS-RUNTIME-02-BE`
- canonical task: `/root/runtime_02_backend`
- 실제 thread ID: `01a1aa53-386c-7ad2-8c0b-0429861e3644`
- 런타임 developer 역할 지침과 `.codex/agents/backend.toml` 내용이 일치한다. 별도 `selected_agent_type` 반환 필드는 자식에게 노출되지 않았으므로 메인이 실제 `agent_type="backend"` 호출 기록과 대조해야 한다.

역할은 Java 21/Spring Boot의 순수 domain/application/adapter, 서버 mart 권한, DB 트랜잭션·감사·낙관적 잠금, 호환 migration, Outbox/worker/fake adapter와 서버 테스트다.

향후 쓰기 후보는 `backend/**`와 지정된 본인 보고서이며, 정확한 파일 배정과 활성 잠금이 필수다. `frontend/**`, `infra/**`, CI, 계약·ADR, 공통 설정·원장·루트 파일·원본 명세·타 Agent 보고서는 수정할 수 없다. **이번 작업은 쓰기 허용 파일 없음, 잠금 NONE이다.**

계약 전에는 읽기 검토만 수행한다. 사용자 Phase 허용, 이전 gate, 독립 계약 검토, 메인 승인·동결, task의 계약 SHA-256 일치를 확인한 뒤에만 구현한다. 계약 변경이 필요하면 구현을 멈추고 architect에게 요청한다.

실제 SMS, Production 변경·배포·SQL·클라우드 적용, 기존 데이터·이미지·볼륨·이력 삭제는 금지한다. UNKNOWN 접수는 조회·대사 전 재발송하거나 타 발송사로 failover하지 않는다. 재위임도 금지한다.

| 실제 읽기 명령 | 종료 코드 |
|---|---:|
| `cat AGENTS.md harness/README.md harness/OWNERSHIP.md harness/PROTOCOL.md harness/PHASES.md .codex/agents/backend.toml` | 0 |
| `cat MART_RENEWAL_PRD.md MART_CODING_AGENT_PROMPT.md` | 0 |
| Python으로 지정 8개 입력 SHA-256 및 `CODEX_THREAD_ID` 한 값 조회 | 0 |
| `cat .codex/agents/backend.toml harness/PHASES.md harness/PROTOCOL.md` | 0 |

첫 묶음 출력 일부가 도구 반환 한도로 생략돼 역할·계약·절차 문서를 별도로 재확인했다.

활성 backend TOML SHA-256: `eda26d63d7ce3590c487e2d64f0f621ef8e1de5d28947db1bc63e635587572df`.

파일 수정 **0건**. 서비스·외부 API·실SMS·운영 접근·데이터 삭제 **미실행**. Phase 0과 앱 구현은 시작하지 않았다. 전체 하네스 PASS 및 독립 판정은 메인이 취합한다.

### frontend 응답 원문

판정: **frontend 역할 인식·읽기 전용 준수 PASS**.

- 역할: `frontend`
- task ID: `HARNESS-RUNTIME-02-FE`
- canonical task: `/root/runtime_02_frontend`
- 실제 thread ID: `01a1aa53-c0e3-7b33-b405-7a2525342d30`
- 런타임 developer 역할 지침과 `.codex/agents/frontend.toml`이 일치한다. 별도 `selected_agent_type` 반환 필드는 자식에게 노출되지 않았으므로 메인이 `agent_type="frontend"` 호출 기록과 대조해야 한다.

역할은 React/TypeScript 관리자 UI, 접근성, 서버 목록 처리, 권한·로딩·빈 상태·오류·부분 실패·409 UX, 문자 접수/전달/UNKNOWN 구분과 프런트엔드 테스트다.

향후 쓰기 후보는 `frontend/**`와 지정된 본인 보고서이며 정확한 파일 배정과 활성 잠금이 필요하다. backend/infra/CI/계약·ADR, 공통 설정·원장·루트 파일·원본 명세·타 Agent 보고서는 수정할 수 없다. **이번 쓰기 허용 파일은 없고 잠금은 NONE이다.**

계약 전에는 읽기 검토만 한다. 사용자 Phase 허용, 이전 gate, 독립 계약 검토, 메인 승인·동결 및 task의 계약 SHA-256 일치를 확인한 뒤 구현한다. 계약 변경이 필요하면 구현을 멈추고 architect에게 요청한다. fixture 검증을 실제 API 통합 완료로, UI 권한 표시를 서버 인가로 주장하지 않는다.

실SMS, Production 변경·배포·SQL·클라우드 적용, 기존 데이터·이미지·볼륨·이력 삭제는 금지한다. UNKNOWN은 조회·대사 전 재발송하거나 타 발송사로 failover하지 않는다. 재위임도 금지한다.

| 실제 읽기 명령 | 종료 코드 |
|---|---:|
| `cat AGENTS.md harness/README.md harness/OWNERSHIP.md harness/PROTOCOL.md .codex/agents/frontend.toml` | 0 |
| `cat harness/PHASES.md MART_RENEWAL_PRD.md MART_CODING_AGENT_PROMPT.md` | 0 |
| Python으로 지정 8개 입력 SHA-256과 `CODEX_THREAD_ID` 한 값 조회 | 0 |
| `cat .codex/agents/frontend.toml harness/PHASES.md` | 0 |

묶음 출력 일부가 반환 한도로 생략돼 역할 TOML과 Phase 규칙을 별도로 재확인했다.

활성 frontend TOML SHA-256: `9a49cdd2c8854669a50921ab651f358b739050abcc3d1415cec5b5975576f62d`.

파일 수정 **0건**. 서비스·외부 API·실SMS·운영 접근·데이터 삭제 **미실행**. Phase 0과 앱 구현은 시작하지 않았다. 전체 스모크 및 독립 승인은 메인이 판정한다.

### reliability 응답 원문

판정: **reliability 역할 인식·읽기 전용 준수 PASS**.

- 역할: `reliability`
- task ID: `HARNESS-RUNTIME-02-REL`
- canonical task: `/root/runtime_02_reliability`
- 실제 thread ID: `01a1aa54-5c87-78a0-bccc-08f50c86fd9c`
- 런타임 developer 역할 지침과 `.codex/agents/reliability.toml`이 일치한다. 별도 `selected_agent_type` 반환 필드는 자식에게 노출되지 않았으므로 메인이 `agent_type="reliability"` 호출 기록과 대조해야 한다.

역할은 격리된 local/fake 환경, CI/IaC 예제, 관측·health·graceful shutdown, 장애 주입, 백업 복원·앱 원복·데이터 대사·RTO/RPO, runbook 및 보안 검증이다. 각 Phase의 안전 계획과 통합·장애 검증 시점에 참여하며, Phase 0에서는 계획만 검토한다. **이번에는 Phase 0 계획 검토도 시작하지 않았다.**

향후 쓰기 후보는 `infra/**`, `.github/workflows/**`, `tests/system/**`, `docs/test-plan.md`, `docs/runbooks/**`, 지정된 본인 보고서다. 정확한 파일 배정과 활성 잠금이 필요하다. backend/frontend, 계약·ADR, 공통 설정·원장·루트 파일·원본 명세·타 Agent 보고서는 수정할 수 없다. 루트 Compose·빌드 변경안은 메인에게 반환한다. **이번 쓰기 허용 파일은 없고 잠금은 NONE이다.**

계약 승인·독립 검토·메인 동결 및 task의 계약 SHA-256 확인 전 앱 구현은 금지된다. 계약 변경은 architect에게 요청한다. 자신이 작성한 IaC·테스트·보고서를 독립 승인하지 않고 새 reviewer에게 인계한다.

실SMS, Production 변경·배포·SQL·클라우드 적용, 기존 데이터·이미지·볼륨·이력 삭제는 금지한다. UNKNOWN은 조회·대사 전 재발송하거나 타 발송사로 failover하지 않는다. 실행 대상·자격증명이 불명이면 중단하며 재위임하지 않는다.

| 실제 읽기 명령 | 종료 코드 |
|---|---:|
| `cat AGENTS.md harness/README.md harness/OWNERSHIP.md harness/PROTOCOL.md .codex/agents/reliability.toml` | 0 |
| `cat harness/PHASES.md MART_RENEWAL_PRD.md MART_CODING_AGENT_PROMPT.md` | 0 |
| Python으로 지정 8개 입력 SHA-256과 `CODEX_THREAD_ID` 한 값 조회 | 0 |
| `cat .codex/agents/reliability.toml harness/PHASES.md` | 0 |

묶음 출력 일부가 반환 한도로 생략돼 역할 TOML과 Phase 규칙을 별도로 재확인했다.

활성 reliability TOML SHA-256: `8b4bd3b59b2bc7c26d51f2a7b1abec781c3afb6a70871ba4ddc40910e6b8d3b3`.

파일 수정 **0건**. 서비스·외부 API·실SMS·운영 접근·데이터 삭제 **미실행**. Phase 0과 앱 구현은 시작하지 않았다. 전체 스모크와 독립 승인은 메인이 판정한다.

## reviewer 인계와 검토 경계

앞 네 결과를 이번 읽기 전용 호출의 역할·파일·시점·계약·안전 규칙과 대조해 모두 충족했다.
독립 reviewer는 이 보고서의 새 시도, 준비/활성 6쌍, 호출 기록과 원문, 기존 구축 리뷰와 변경 4개 파일을 읽기 검토한다.
검토 중 메인은 보고서와 state를 쓰지 않는다. reviewer에게 파일 쓰기·서비스·외부 API·재위임을 허용하지 않는다.
reviewer가 반환할 판정은 runtime 독립 검토와 현재 구축 리뷰를 구분한다. 실패/증거 부족이면 BLOCKED를 유지한다.
승인 후 메인이 추가할 내용은 reviewer 호출 ID·응답 원문·최종 대조 및 setup 상태·증거 해시 등록 기록뿐이다.
보고서 최종 SHA-256은 자기참조를 피하기 위해 state.runtime_evidence에만 저장한다.


## 다섯 번째 custom 호출과 독립 reviewer 원문

실제 호출: `collaboration.spawn_agent(agent_type="reviewer", task_name="runtime_02_reviewer", ...)`.
성공 반환 task ID: `/root/runtime_02_reviewer`.
실제 thread ID: `01a1aa55-6695-7220-b8b2-e6cbfe1d7300`.
프로세스 종료 코드: 해당 없음(도구 성공 응답 및 FINAL_ANSWER 수신).
메인은 reviewer의 역할·파일·시점·계약·안전 규칙을 활성 TOML 및 공통 규칙과 대조해 PASS로 판정했다.

독립 판정: **역할 인식 PASS / runtime 스모크 읽기 검토 PASS / 현재 하네스 구축 리뷰 PASS**.

- custom 역할: `reviewer`
- task ID: `HARNESS-RUNTIME-02-REV`
- canonical task: `/root/runtime_02_reviewer`
- 실제 thread ID: `01a1aa55-6695-7220-b8b2-e6cbfe1d7300`
- 주입된 reviewer developer instructions는 `.codex/agents/reviewer.toml`과 일치한다. 활성 TOML SHA-256은 `fe7a38597eb2509b575afe8c3a3b5fc44ecf4fd3186622bc70a13ac7cc007710`이다.

reviewer는 하네스 검토, 계약 승인 직전, 쓰기 종료 스냅샷, 실패 수정 후 새 독립 검증에 참여한다. 쓰기 허용 파일은 없으며 코드·계약·설정·테스트·보고서·원장을 수정하지 않는다. 계약 승인·메인 동결·SHA-256 확인 전 구현, 자기 작성물 독립 승인, 재위임은 금지된다. 실SMS, 운영 변경·배포·SQL·클라우드 적용, 기존 데이터·이미지·볼륨·이력 삭제도 금지된다.

앞 네 응답과 상속된 실제 호출 기록을 대조했다.

| 순서 | 명시된 custom `agent_type` | 실제 thread ID | 규칙 대조 |
|---|---|---|---|
| 1 | architect | `01a1aa52-a738-7ee1-929a-65ac5e4534aa` | PASS |
| 2 | backend | `01a1aa53-386c-7ad2-8c0b-0429861e3644` | PASS |
| 3 | frontend | `01a1aa53-c0e3-7b33-b405-7a2525342d30` | PASS |
| 4 | reliability | `01a1aa54-5c87-78a0-bccc-08f50c86fd9c` | PASS |

각 역할의 종료 응답 뒤 다음 역할을 호출했으며, 정확한 역할 선택 인자와 새 canonical task가 기록돼 있다. 각 응답은 실제 developer 역할 지침 일치, 담당 파일·시점, 계약 전 구현 금지와 안전 규칙을 확인했다. generic Agent에 역할을 말로 부여한 경우와 구별된다. 별도 `selected_agent_type` echo는 제공되지 않으므로 내부 로더에 대한 별도 인증이라고 주장하지 않는다.

준비/활성 TOML 6쌍은 직접 읽기 비교에서 모두 동일했다. 직접 실행한 `python3 harness/scripts/validate.py --active`는 **종료 0, PASS**였다. 출력은 TOML 6개, 최소 스키마 PASS, native strict 설정 PASS, Codex CLI `0.166.0`이다. 검사기의 `custom_agent_spawn=NOT_RUN`은 이 정적 검사 자체의 범위이며, 별도 실제 호출 증거와 구분했다.

현재 구축 리뷰는 과거 PASS를 자동 재사용하지 않고 다음 근거로 새로 판정했다.

- 기존 manifest의 변경 4개 파일인 `docs/PROGRESS.md`, `harness/PHASES.md`, `harness/TASKS.md`, `harness/state.json`을 현재 내용으로 읽었다. UI 트랙 기록은 이번 실행 권한으로 사용하지 않았다.
- 현재 설정·활성화 도구·검증기·gate 코드·테스트 소스와 기존 검증 로그를 읽기 검토했다. 기존 manifest의 나머지 입력과 연결된 로그 해시는 일치했다.
- 구현 전 독립 계약 검토·메인 동결, 증거 해시, 선행 Phase, 실패·미실행 차단 조건이 유지돼 있다.
- 이번 입력 스냅샷은 보고서의 의도된 갱신을 제외하고 모두 유지됐다. 하네스 호출 검증을 Phase 완료로 승격하는 변경은 없었다.

주요 입력 해시:

| 입력 | SHA-256 |
|---|---|
| 검토 대상 runtime-smoke.md | `eb6760a1d185cd0d1d0e360e1d7101bb24fa89d2e08e9cc26a585341143c1db1` |
| 검토 대상 state.json | `1164db30d664c1ba2d83f65c97f158e02df32778e322417267bdd4af0aa0340b` |
| 기존 review-manifest.json | `548d0fa5e2a667d3f2ba20a8430897e7787b4f8264c347a83916d4a79349ed1a` |
| validate.py | `cf8a0f73ccb2def68a55e67b7b6ee56b5adca842a5149d26e654f0acab0cd933` |
| check_gate.py | `514d16a4317c18f2a18f13afc570543c6a005f5170dd615811e1628c33e3be8e` |

검토 시작과 종료 시 보고서·state 해시는 동일했다. 실제 명령은 모두 종료 **0**이었다.

| 실제 명령·검사 | 결과 |
|---|---|
| `cat AGENTS.md harness/README.md harness/OWNERSHIP.md harness/PROTOCOL.md .codex/agents/reviewer.toml` | 규칙·역할 확인 |
| `cat harness/PHASES.md harness/TASKS.md harness/state.json docs/PROGRESS.md` | 변경 4개 입력 재검토 |
| `cat harness/scripts/validate.py harness/scripts/check_gate.py harness/scripts/activate.py` | 구축 코드 읽기 검토 |
| `cat harness/tests/test_gate.py harness/scripts/activate.py .codex/agents/reviewer.toml` | 테스트 소스·역할 재확인 |
| `cat harness/reports/setup/independent-review.md harness/reports/setup/checks.json harness/reports/setup/gate-tests.log` | 과거 리뷰·로그 대조 |
| 원본 두 명세 및 `MART_CODING_AGENT_PROMPT.md` 별도 읽기 | 최신 사용자 범위 우선 확인 |
| Python pathlib/hashlib/json/tomllib 읽기 검사 | 보고서·state·입력·로그 해시 및 TOML 6쌍 일치 |
| `python3 harness/scripts/validate.py --active` | PASS |

큰 묶음 출력 일부는 도구 한도로 축약돼 핵심 역할·변경 문서·검증 코드·원본 프롬프트를 별도로 재조회했다.

이번 reviewer의 파일 수정은 **0건**이며 서비스 기동·외부 API·실SMS·운영 접근·데이터 삭제·Phase 0·앱 구현은 실행하지 않았다. 기존 18개 테스트 PASS는 해시가 일치하는 과거 실행 증거이며 이번에 테스트를 재실행했다고 주장하지 않는다.

메인은 이 응답 원문과 다섯 번째 호출 ID를 보존한 뒤 보고서를 확정하고 실제 최종 SHA-256을 `setup.runtime_evidence`에 등록·재대조해야 한다. 그 최종 기록이 충족되면 이번 판정은 `activation=ACTIVE`, `runtime_smoke=PASS`, `setup.status=PASS` 기록의 독립 근거가 된다. 기존 Phase 상태와 별도 UI 기록은 유지해야 한다. 이 판정은 하네스 호출·구축 검토에 한정되며 앱 기능 검증이나 Phase 0 완료를 의미하지 않는다.

## 메인 최종 대조와 상태 전이

독립 검토가 끝난 뒤 Python pathlib/hashlib/json으로 시작 스냅샷을 대조했다. 실제 종료 코드 **0**, 보고서를 제외한 43개 입력 모두 시작 해시와 일치했다. reviewer에 전달한 보고서와 state도 검토 종료까지 각각 `eb6760a1d185cd0d1d0e360e1d7101bb24fa89d2e08e9cc26a585341143c1db1`, `1164db30d664c1ba2d83f65c97f158e02df32778e322417267bdd4af0aa0340b`로 유지됐다.

최종 `python3 harness/scripts/validate.py --active`: 실제 종료 코드 **0**, PASS. 최초·앞 네 호출 후·reviewer 독립 실행·최종 메인 실행 모두 종료 0이었다. 준비/활성 TOML 6쌍이 같고 native strict parser PASS, Codex CLI 0.166.0이다. 검사기의 spawn NOT_RUN 필드는 정적 검사 자체의 범위로 보존하며 실제 역할 호출 성공으로 출력을 바꾸지 않았다.

다섯 custom 역할 모두 메인이 정확한 `agent_type`을 하나씩 선택했고, 직전 종료 응답 뒤 다음 새 task를 시작했다. 각 실제 thread/task ID·주입된 역할 규칙 응답과 활성 TOML을 대조했다. 대체 generic Agent, 재위임, 전문 Agent 파일 쓰기, 서비스·외부 API 실행은 없었다. 파일 해시 대조는 입력 43개 범위이며 저장소 전체 OS 쓰기 감사 증명으로 확대하지 않는다.

최종 판정: **하네스 runtime 스모크 PASS / 현재 독립 구축 리뷰 PASS / setup PASS**.
메인이 기록할 setup 값: `config_location=.codex`, `activation=ACTIVE`, `runtime_smoke=PASS`, `status=PASS`.
근거는 --active PASS, 정확한 다섯 custom 호출과 응답, 새 reviewer의 runtime 및 현재 구축 리뷰 PASS다.

이 문서를 최종 확정한 뒤 Python pathlib/hashlib/json으로 실제 원문 SHA-256을 계산해 `setup.runtime_evidence={"path":"harness/reports/setup/runtime-smoke.md","sha256":"실제 계산값"}`를 저장한다. 저장 직후 원문을 다시 읽어 같은 SHA-256인지 assertion으로 검사하고, setup 외 state 값이 원본과 같은지 확인한다. 최종 실제 해시는 state에 저장하며 보고서 자체에 자기 해시를 넣지 않는다. 이후 읽기 검증만 수행한다.

변경 파일은 메인의 이 보고서와 `harness/state.json`의 setup 항목뿐이다. 기존 실패 이력과 과거 독립 리뷰는 보존했다. Phase 0은 BLOCKED, Phase 1~6 상태와 별도 UI 트랙은 그대로다. 이번 작업은 Phase 0 착수·완료, 앱 기능·실API·운영 검증이 아니다. 앱/의존성/DB/인프라 작업과 실SMS·운영 변경·기존 데이터 삭제를 실행하지 않았다.

최종 등록 명령의 실제 결과: `python3 -c`(pathlib/hashlib/json으로 setup 갱신·보고서 SHA-256 재계산·setup 외 상태 보존 assertion) **종료 0, PASS**. 이어 저장된 상태에서 `python3 harness/scripts/validate.py --active`도 **종료 0, PASS**였다. 이 결과 행을 추가해 보고서 바이트가 바뀌었으므로 실제 최종 해시를 다시 계산·등록·재대조한다. 보고서에 최종 해시 문자열을 적어 자기참조를 만들지 않는다.



