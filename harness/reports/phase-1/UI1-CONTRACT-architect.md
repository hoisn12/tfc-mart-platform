# UI1-CONTRACT architect 보고서

판정: PASS (계약 초안 작성 완료). 독립 승인·계약 동결·구현·실행 테스트는 NOT_RUN이며 메인과 별도 reviewer 책임이다.

## 범위와 변경

배정된 네 파일만 작성했다. 최신 사용자 허용에 따른 frontend-only local mock 트랙, UI 6경로, 상품 100+ 및 CRUD/soft delete/bulk/열설정, SMS 상태/UNKNOWN 차단, 이미지 안전 교체/검증, 회원/설정, persistence 오류/복구를 정의했다. DTO와 Service 경계 및 미래 OpenAPI 연결점을 마련하고 ADR 009에 대안/영향/복구를 기록했다. 기존 Foundation gate와 문서는 승인·수정하지 않았다.

## 명령과 결과

- `cat harness/codex/agents/architect.toml harness/OWNERSHIP.md harness/PROTOCOL.md harness/PHASES.md harness/TASKS.md AGENTS.md`: 종료 0, 역할·정확한 파일 잠금 확인.
- `cat MART_RENEWAL_PRD.md MART_CODING_AGENT_PROMPT.md docs/architecture.md docs/assumptions.md`: 종료 0, 기본 명세·초안·미확인 경계 확인.
- shell here-doc로 배정 계약/ADR 작성 및 Python SHA-256 산출: 종료 0.
- `ruby` YAML parse 및 OpenAPI 버전/경로수 smoke: 최초 예상 경로수를 8로 쓴 확인 명령은 종료 1 (`missing paths`). 실제 7개 경로를 확인하고 기대값을 정정한 재실행은 종료 0, `YAML parse PASS: 7 paths`. 파일 schema 완전성 검증 도구를 실행한 것으로 주장하지 않는다.
- 앱 실행/TypeScript/build/브라우저/실 API/운영 검증: NOT_RUN (본 계약 작성 task의 실행 범위 아님).

## 산출물 SHA-256

```json
{
  "docs/contracts/ui-prototype.behavior.md": "914bb8043bf2d7641316419c469e27c5b7cfd3f1a3bfdf3f9aef9aa02d5cc9b7",
  "docs/contracts/ui-prototype.openapi.yaml": "fcb89bbb0e5c96964e7868ed7021b0f98cf5a40819c8dc280f91d70e005c872c",
  "docs/adr/009-ui-prototype.md": "504beb38465b55401a5fb4b77de5287f3bbf2e1aff7c46393799dba8c903635a"
}
```

## 입력 해시

메인 생성 `input-manifest.json`의 원문을 확인했다.

```json
{
  "AGENTS.md": "a940023331133e9dd179a4a2999277b843da9f48cb51ae2c94b42ded8619dc9c",
  "MART_RENEWAL_PRD.md": "9c9d236770d092fe62feca71ce7ca8450ed28328f2ac01c799ee66593f27ca0d",
  "MART_CODING_AGENT_PROMPT.md": "955b7ff38348bae11cc4e6ae537473f25d5d9edc7be6488afee5412ea4edcbef",
  "example.png": "f3d0ed103039ecebc28bb127f9bc172d5f3fdbc40cb1e886d3f2443c68f684cb",
  "harness/codex/agents/architect.toml": "48b78d4f02ac3bf9156c23e4937f78f764831a751ed96c9091eff0ece5f789f0",
  "harness/codex/agents/frontend.toml": "9a49cdd2c8854669a50921ab651f358b739050abcc3d1415cec5b5975576f62d",
  "harness/codex/agents/reviewer.toml": "fe7a38597eb2509b575afe8c3a3b5fc44ecf4fd3186622bc70a13ac7cc007710",
  "harness/codex/agents/reliability.toml": "8b4bd3b59b2bc7c26d51f2a7b1abec781c3afb6a70871ba4ddc40910e6b8d3b3"
}
```

## 미완료·가정·위험

구현자 읽기 검토 → reliability 안전 검토 → 새 독립 reviewer 검토 → 메인 해시 동결을 기다린다. .codex Custom Agent 활성화는 확인되지 않았고 준비 TOML을 collaboration 역할에 적용한 실행이다. 실제 한글 레거시와 U01~U16은 여전히 미확인이다. LocalStorage는 서버 인증·테넌트·TX·내구성 보장이 아니며 바코드 중복/가격/수량 규칙은 데모 가정이다. OpenAPI는 서버 미구현 초안이고 이 단계에서 실호출하지 않는다. 이미지 로컬 data URL은 제한된 브라우저 데모이며 실제 private 원본/CDN 구현을 대체하지 않는다.
