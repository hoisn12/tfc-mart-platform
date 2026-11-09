#!/usr/bin/env python3
"""필수 증거·독립 판정·파일 해시·선행 Phase를 검사한다. 상태 변경/모델 호출 없음."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
CATEGORIES = {"requirements", "contract", "tests", "recovery", "rollback",
              "operations", "independent_review"}
PHASE0_OUTPUTS = {
    "docs/legacy-feature-matrix.md", "docs/requirements.md", "docs/assumptions.md",
    "docs/architecture.md", "docs/data-model.md", "docs/api-spec.md",
    "docs/migration-plan.md", "docs/test-plan.md",
    "docs/contracts/phase-1.openapi.yaml", "docs/contracts/phase-1.behavior.md",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def artifact(root, name, digest):
    require(isinstance(name, str) and name and not Path(name).is_absolute(),
            "증거 경로는 프로젝트 상대 파일이어야 함")
    path = root / name
    require(".." not in Path(name).parts and path.is_file(), f"파일 누락/경로 오류: {name}")
    require(path.resolve().is_relative_to(root.resolve()), f"프로젝트 밖 증거 금지: {name}")
    require(isinstance(digest, str) and len(digest) == 64, f"SHA-256 형식 오류: {name}")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    require(actual == digest, f"증거/산출물 변경 감지: {name}")
    return path


def check(root, phase):
    require(type(phase) is int and 0 <= phase <= 6, "Phase는 0~6")
    state = json.loads((root / "harness/state.json").read_text())
    setup = state["setup"]
    require(setup["status"] == "PASS" and setup["activation"] == "ACTIVE"
            and setup["runtime_smoke"] == "PASS", "하네스 활성화/실제 호출 검증 미완료")
    active = root / ".codex"
    source = root / "harness/codex"
    require(active.is_dir() and not active.is_symlink(), "활성 .codex 디렉터리 없음/금지 symlink")
    configs = [source / "config.toml", *sorted((source / "agents").glob("*.toml"))]
    require(len(configs) == 6, "준비 설정 6개 필요")
    for config in configs:
        target = active / config.relative_to(source)
        require(target.is_file() and not target.is_symlink()
                and target.resolve().is_relative_to(active.resolve())
                and target.read_bytes() == config.read_bytes(), "활성 설정 누락/불일치")
    receipt = setup["runtime_evidence"]
    artifact(root, receipt["path"], receipt["sha256"])
    phases = state["phases"]
    require([p["phase"] for p in phases] == list(range(7)), "Phase 상태 목록 오류")
    for number in range(phase + 1):
        record = phases[number]
        require(record["status"] in ({"PASS"} if number < phase else {"VERIFYING", "PASS"}),
                f"Phase {number} 상태가 gate 검사 조건을 충족하지 않음")
        require(record["gate"] == f"harness/reports/phase-{number}/gate.json",
                "gate 경로 불일치")
        gate = json.loads((root / record["gate"]).read_text())
        require(type(gate["phase"]) is int and gate["phase"] == number, "gate Phase 불일치")
        require(gate["status"] == "PASS", f"Phase {number} gate PASS 아님")
        attempt = gate["attempt"]
        require(type(attempt) is int and attempt >= 1, "검증 시도 번호 필요")
        require(gate["reviewer"] == "reviewer" and gate["reviewer_independent"] is True
                and gate["reviewer_verdict"] == "PASS"
                and bool(gate["reviewer_task_id"]), "독립 reviewer PASS 필요")
        require(gate["unresolved"] == [], "미해결 필수 항목 존재")
        snapshot = gate["snapshot"]
        require(isinstance(snapshot, dict) and bool(snapshot), "산출물 스냅샷 누락")
        require(not any(name.endswith("/gate.json") for name in snapshot),
                "gate 자체를 산출물로 검증할 수 없음")
        archive = gate["archive"]
        require(set(archive) == set(snapshot), "스냅샷과 보관본 목록 불일치")
        for name, digest in snapshot.items():
            require(archive[name] == f"harness/reports/phase-{number}/attempt-{attempt}/snapshot/{name}",
                    "스냅샷 보관 경로 불일치")
            artifact(root, archive[name], digest)
            # 선행 gate는 그 시점 보관본을 검증한다. 현재 Phase는 작업 파일도 일치해야 한다.
            if number == phase:
                artifact(root, name, digest)
        if number == 0:
            require(PHASE0_OUTPUTS <= set(snapshot), "Phase 0 필수 설계/계약 스냅샷 누락")
        if 1 <= number <= 5:
            require(any(name.startswith("backend/") for name in snapshot)
                    and any(name.startswith("frontend/") for name in snapshot),
                    "구현 Phase의 backend/frontend 실제 산출물 스냅샷 필요")
        if number == 6:
            require("docs/migration-plan.md" in snapshot, "전환 계획 스냅샷 필요")
        contract = gate["contract"]
        require(contract["status"] == "FROZEN" and contract["approved_by"] == "main-codex"
                and contract["reviewer_verdict"] == "PASS"
                and contract["reviewer_independent"] is True
                and bool(contract["reviewer_task_id"]), "독립 검토와 메인 계약 동결 필요")
        contracts = contract["files"]
        require(isinstance(contracts, dict) and len(contracts) >= 2
                and all(name.startswith("docs/contracts/") for name in contracts)
                and any(name.endswith(".openapi.yaml") for name in contracts)
                and any(name.endswith(".behavior.md") for name in contracts),
                "OpenAPI와 behavior 계약 해시 필요")
        require(all(snapshot.get(name) == digest for name, digest in contracts.items()),
                "동결 계약과 산출물 스냅샷 불일치")
        approval = contract["approval"]
        require(approval["path"].startswith(f"harness/reports/phase-{number}/")
                and approval["path"].endswith(".md"), "해당 Phase 계약 승인 보고서 필요")
        artifact(root, approval["path"], approval["sha256"])
        evidence = gate["evidence"]
        require(set(evidence) == CATEGORIES, "필수 증거 7종 필요")
        for category, item in evidence.items():
            require(item["status"] == "PASS", f"{category} 실패/미실행/차단")
            require(item["path"].startswith(f"harness/reports/phase-{number}/")
                    and item["path"].endswith(".md"), "해당 Phase의 Markdown 보고서 필요")
            report = artifact(root, item["path"], item["sha256"])
            require(report.stat().st_size > 0, f"빈 보고서: {category}")
        independent = evidence["independent_review"]["path"]
        require(independent != approval["path"], "계약 승인과 최종 독립 리뷰는 별도 보고서 필요")
        require(independent not in {v["path"] for k, v in evidence.items()
                                    if k != "independent_review"},
                "독립 리뷰는 작성자 증거와 다른 보고서여야 함")
    return f"PASS: Phase 0~{phase} 증거/독립 판정/해시 일치. 상태 전이는 메인이 수행."


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", required=True, type=int, choices=range(7))
    args = parser.parse_args()
    print(check(ROOT, args.phase))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        sys.exit(1)
