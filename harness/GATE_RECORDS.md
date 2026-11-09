# gate 증거 기록 안내

메인 Codex만 기록한다. gate JSON은 프로젝트 자체 기록이며 Codex 설정이 아니다. 실제 근거 없는 PASS를 채우지 않는다.

1. 사용자 권한으로 준비본을 활성화하고 새 세션 스모크를 완료한다. state.setup에 status=PASS, activation=ACTIVE, config_location=.codex, runtime_smoke=PASS와 runtime_evidence(path/sha256)를 실제 결과로 기록한다. 보고서를 변경하면 해시도 재검증한다.
2. 해당 Phase를 IN_PROGRESS로 기록하고 정확한 파일별 task/잠금을 배정한다. architect 계약 작성→두 구현자 읽기 검토→reliability 검토→독립 reviewer 계약 PASS를 취합한다. 메인은 contract-approval.md에 계약 파일/해시·검토 task/thread ID·판정·동결 시각을 기록한다.
3. Backend/Frontend 병렬 구현은 이 동결 이후만 가능하다. 계약은 docs/contracts/의 OpenAPI(`.openapi.yaml`), behavior(`.behavior.md`)를 포함한다. Phase 0은 phase-1.openapi.yaml과 phase-1.behavior.md로 Foundation 범위를 고정한다. 변경 없는 API도 각 Phase의 승인 버전·해시를 기록한다.
4. 모든 쓰기를 종료하고 **변경한 모든 파일과 검증 입력·계약·실제 산출물**을 스냅샷에 포함한다. backend/frontend 코드·테스트·migration을 누락하지 않는다. 자동 검사는 최소 조건만 확인하며 완전한 변경 목록은 reviewer가 task/diff와 대조한다.
5. phase-N/attempt-A/에 시도별 보고서와 snapshot/원래경로 보관본을 만든다. 기존 보관본은 덮어쓰지 않는다. snapshot은 원래경로→원본 SHA-256, archive는 원래경로→보관본 경로 매핑이다. 다음은 생성 방법의 예시이며 paths는 실제 task 목록으로 채운다.

```python
from pathlib import Path
import hashlib
root = Path.cwd()
phase, attempt = 0, 1
paths = [...]  # 실제 모든 입력/계약/변경/산출물 상대 경로
snapshot, archive = {}, {}
for name in paths:
    src = root / name
    assert not Path(name).is_absolute() and ".." not in Path(name).parts
    assert src.is_file() and src.resolve().is_relative_to(root.resolve())
    dst = root / f"harness/reports/phase-{phase}/attempt-{attempt}/snapshot/{name}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = src.read_bytes()
    with dst.open("xb") as out:
        out.write(data)
    snapshot[name] = hashlib.sha256(data).hexdigest()
    archive[name] = str(dst.relative_to(root))
```

6. 작성에 관여하지 않은 새 reviewer에게 고정된 입력·보관본·로그를 전달한다. 메인은 반환 원문을 independent-review.md로 저장한다. 계약 승인과 최종 독립 리뷰는 별도 파일이며 작성자 보고서와도 분리한다. reviewer task ID와 작성 불참을 확인한다.
7. templates/gate.json을 복사해 phase/attempt/snapshot/archive/contract/evidence를 실제 값으로 채운다. evidence는 requirements, contract, tests, recovery, rollback, operations, independent_review 7종이며 각 상태/보고서 경로/실제 SHA-256이 필요하다. 하나의 작성자 보고서가 여러 범주를 다룰 수 있지만 독립 리뷰는 별도 파일이다.
8. Phase 0의 실제 실행 테스트는 NOT_RUN이라고 명시한다. 이 단계 tests/recovery/rollback/operations 증거 PASS는 **계획이 필수 시나리오와 재현·관측·복구·인수 기준을 담았다는 독립 검증**이다. Phase 1 이후는 해당 범위 실제 실행 로그·종료 코드가 필요하다.
9. 필수 미해결이 있으면 BLOCKED/FAIL을 유지한다. 모두 충족하면 gate.status=PASS를 제안하고 Phase를 VERIFYING으로 둔다. gate.json은 해당 Phase 최상위의 현재 판정이며 같은 내용을 attempt-A/gate.json에도 보존한다.
10. validate.py --active와 check_gate.py --phase N의 종료0을 확인한 뒤 Phase를 PASS로 기록한다. 실패면 새 시도 번호로 재검증하고 다음 Phase로 가지 않는다. 현재 gate는 작업 파일과 보관본 양쪽을, 선행 gate는 당시 보관본과 증거를 검증한다. 다음 Phase에서 승인 범위의 문서/코드 진화는 현재 Phase의 계약·회귀 증거로 증명한다.

check_gate는 문서 의미·명령 실행의 진실성·reviewer 신원·수동 정책 위반을 암호학적으로 증명하지 않는다. 메인이 세션 기록/원문/로그와 대조하며 자동 승인의 대체로 사용하지 않는다.
