# Codex 마트 개발 하네스

메인 Codex가 Orchestrator이며 전문 역할 5개를 배정하는 저장소 작업 하네스다. 비즈니스 구현은 이번 범위 밖이다. 시작 문서는 [공통 규칙](../AGENTS.md), [Phase 계획](PHASES.md), [협업 절차](PROTOCOL.md), [파일 소유권](OWNERSHIP.md)이다.

## 활성화 상태와 설정 근거

현재 환경은 프로젝트 `.codex/`를 읽기 전용 보호 경로로 지정한다. 쓰기가 자동 승인 검토에서 거부되어 **설정 원본은 `harness/codex/`에 준비**했다. 아직 프로젝트 Custom Agent로 활성화된 상태가 아니다. 보호 경로를 우회하지 않는다.

사용자가 쓰기 가능한 터미널에서 프로젝트 루트 기준으로 아래를 실행한다. 기존 파일이 있으면 덮어쓰지 않고 중단하며 먼저 비교·병합한다.

```sh
python3 harness/scripts/activate.py
python3 harness/scripts/validate.py --active
```

activate.py는 권한 있는 사용자를 위한 복사 도구다. 현재 Agent는 이 환경에서 실행하지 않는다. `.codex/config.toml`과 `.codex/agents/{architect,backend,frontend,reliability,reviewer}.toml`을 만든다. 기존 파일을 자동 교체하거나 사용자 전역 설정/프로젝트 신뢰 설정을 수정하지 않는다.

프로젝트를 신뢰하고 프로젝트 설정이 실제 로드되는 Codex 세션을 새로 연다. 앱/조직 정책이 해당 설정을 지원하지 않거나 덮어쓰면 이를 기록하고 시작하지 않는다. 설정 복사만으로 현재 대화에 역할이 즉시 등록된다고 가정하지 않는다.

공식 자료(2026-11-05 확인):
- [Subagents: standalone TOML 스키마·상속·권한](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)

독립 Agent 파일은 공식 필수 키 `name`, `description`, `developer_instructions`만 사용한다. 모델/추론 수준은 메인 상속. 폐기된 기능 플래그나 가상의 tools/allowed_paths/phase/permissions 키는 넣지 않았다. 메인 설정은 sandbox/approval/network와 agents 활성화/동시수만 정의한다. 부모/관리 권한이 우선하며 Agent TOML은 독립 sandbox를 만들지 않는다.

동시 하위 스레드 상한은 3이다. 역할 5개를 전부 동시에 실행할 필요는 없다. Backend+Frontend 병렬 구현과 reviewer 독립 최종 검증은 시점을 분리한다. 파일 소유권·gate·잠금은 작업 규약 및 보조 검증기로 관리하며 OS 파일 ACL이나 자동 워크플로 엔진이 아니다. 부모 세션의 네트워크 차단도 연결 도구의 모든 원격 행위를 차단하는 보증이 아니므로 안전 규칙을 함께 적용한다.

## 검증 수준

```sh
python3 harness/scripts/validate.py
python3 harness/scripts/validate.py --active
python3 harness/scripts/check_gate.py --phase 0
python3 -B -m unittest discover -s harness/tests -v
```

기본 검증은 준비본 TOML과 규칙·문서·state 구조를 검사하고 설치된 Codex의 strict parser로 메인 설정을 격리 임시 경로에서 검증한다. 모델 호출·서비스 기동·운영 접근 없이 실행한다. Agent 파일은 공식 최소 스키마와 TOML 문법을 검사하며 **실제 spawn 성공은 별도 검증**이다. `--active`는 실제 `.codex/` 파일이 준비본과 같은지도 확인한다.

현재 Phase 0 gate가 없는 것은 정상이며 check_gate는 0이 아닌 종료 코드를 내야 한다. 실패를 PASS로 바꾸지 않는다. gate는 사람이 임의로 작성할 수 있는 로컬 기록으로 변조 방지 서명이 아니다. reviewer의 독립 실행과 원문/로그를 함께 대조한다.

[하네스 스모크 프롬프트](prompts/harness-smoke.md)는 활성화 후 정확한 이름의 5 Agent를 순차 호출해 역할 인식·쓰기 금지·결과 회수를 확인한다. 실패 시 일반 Agent로 조용히 대체하지 않는다. 실제 spawn/UI·정책·인증 확인 전까지 런타임 상태는 NOT_RUN이다.

## 파일 구성

- `codex/`: `.codex/`에 설치할 메인 설정과 5개 Agent.
- `scripts/`: 활성화(사용자 실행), 정적/네이티브 설정 검증, Phase gate 확인.
- `templates/`: 작업 인계, 결과 보고, gate JSON 양식.
- `prompts/`: 하네스 스모크 및 Phase 0 실행 프롬프트.
- `reports/`: 구축 검증·독립 리뷰 및 향후 Phase별 보고서.
- `state.json`: 메인만 기록하는 Phase 상태. `TASKS.md`: 단일 파일 잠금 원장.
- 진행 원장: [docs/PROGRESS.md](../docs/PROGRESS.md).

gate 작성·보관본 생성·상태 전이 방법은 [증거 기록 안내](GATE_RECORDS.md)를 따른다.

기존 소문자 progress.md는 기록을 보존해 대문자 이름으로 통합한다. PRD 0~6을 유지하고 마스터 프롬프트 Phase 5의 이행을 5 리허설/6 전환 계획으로 나눈다. 현재 사용자 지시가 원본의 “가능하면 Phase 1”보다 우선한다.
