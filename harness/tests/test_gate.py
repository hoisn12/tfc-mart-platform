"""Phase 오진입 방지 검증. 합성 증거를 임시 폴더에만 만들고 종료 시 정리한다."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("gate", ROOT / "harness/scripts/check_gate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="mart-gate-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shutil.copytree(ROOT / "harness/codex", self.root / "harness/codex")
        # 사용자 프로젝트의 보호 경로를 건드리지 않고 테스트 전용 임시 root에만 만든다.
        shutil.copytree(ROOT / "harness/codex", self.root / ".codex")
        self.state = {"setup": {"status": "PASS", "activation": "ACTIVE",
                               "runtime_smoke": "PASS",
                               "runtime_evidence": self.make_artifact("harness/reports/setup/runtime.md")},
                      "phases": [{"phase": n, "status": "VERIFYING" if n == 0 else "NOT_STARTED",
                                  "gate": f"harness/reports/phase-{n}/gate.json"} for n in range(7)]}
        snapshot = {p: self.make_artifact(p)["sha256"] for p in gate.PHASE0_OUTPUTS}
        archive = {p: f"harness/reports/phase-0/attempt-1/snapshot/{p}" for p in snapshot}
        for name in archive.values():
            self.make_artifact(name)
        self.record = {"phase": 0, "attempt": 1, "status": "PASS", "reviewer": "reviewer",
                       "reviewer_task_id": "SYNTHETIC-REVIEW", "reviewer_independent": True,
                       "reviewer_verdict": "PASS", "unresolved": [], "snapshot": snapshot,
                       "archive": archive,
                       "contract": {"status": "FROZEN", "approved_by": "main-codex",
                                    "reviewer_verdict": "PASS", "reviewer_independent": True,
                                    "reviewer_task_id": "SYNTHETIC-CONTRACT-REVIEW",
                                    "files": {p: digest for p, digest in snapshot.items()
                                              if p.startswith("docs/contracts/")},
                                    "approval": self.make_artifact("harness/reports/phase-0/contract-approval.md")},
                       "evidence": {key: {"status": "PASS", **self.make_artifact(
                           f"harness/reports/phase-0/{key}.md")} for key in gate.CATEGORIES}}
        self.save()

    def make_artifact(self, name):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("합성 fixture / 테스트 전용 증거이며 실제 완료 기록 아님\n")
        return {"path": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

    def save(self):
        (self.root / "harness/state.json").write_text(json.dumps(self.state))
        path = self.root / "harness/reports/phase-0/gate.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.record))

    def blocked(self, message=None, phase=0):
        self.save()
        with self.assertRaises(ValueError) as error:
            gate.check(self.root, phase)
        if message:
            self.assertIn(message, str(error.exception))

    def test_complete_fixture_passes(self):
        self.assertTrue(gate.check(self.root, 0).startswith("PASS"))

    def test_inactive_harness_blocks(self):
        self.state["setup"]["activation"] = "BLOCKED_PROTECTED_PATH"
        self.blocked("활성화")

    def test_missing_active_config_blocks(self):
        (self.root / ".codex/config.toml").unlink()
        self.blocked("설정")

    def test_not_run_evidence_blocks(self):
        self.record["evidence"]["recovery"]["status"] = "NOT_RUN"
        self.blocked("recovery")

    def test_missing_category_blocks(self):
        del self.record["evidence"]["rollback"]
        self.blocked("7종")

    def test_non_independent_reviewer_blocks(self):
        self.record["reviewer_independent"] = False
        self.blocked("독립")

    def test_changed_output_blocks(self):
        (self.root / "docs/requirements.md").write_text("검증 후 변경")
        self.blocked("변경 감지")

    def test_changed_evidence_blocks(self):
        path = self.root / self.record["evidence"]["tests"]["path"]
        path.write_text("검증 후 변경")
        self.blocked("변경 감지")

    def test_missing_contract_blocks(self):
        del self.record["snapshot"]["docs/contracts/phase-1.openapi.yaml"]
        del self.record["archive"]["docs/contracts/phase-1.openapi.yaml"]
        self.blocked("계약")

    def test_unfrozen_contract_blocks(self):
        self.record["contract"]["status"] = "DRAFT"
        self.blocked("동결")

    def test_changed_archive_blocks(self):
        path = self.root / self.record["archive"]["docs/requirements.md"]
        path.write_text("보관본 변경")
        self.blocked("변경 감지")

    def test_failed_predecessor_blocks_next_phase(self):
        self.state["phases"][0]["status"] = "FAIL"
        self.blocked("Phase 0", phase=1)

    def test_self_review_report_reuse_blocks(self):
        self.record["evidence"]["independent_review"] = copy.deepcopy(self.record["evidence"]["tests"])
        self.blocked("다른 보고서")

    def test_outside_path_blocks(self):
        self.record["snapshot"]["../outside"] = "0" * 64
        self.record["archive"]["../outside"] = "harness/reports/phase-0/attempt-1/snapshot/../outside"
        self.blocked("경로")

    def test_unresolved_blocks(self):
        self.record["unresolved"] = ["복구 미검증"]
        self.blocked("미해결")

    def phase_one(self):
        self.state["phases"][0]["status"] = "PASS"
        self.state["phases"][1]["status"] = "VERIFYING"
        self.save()
        record = copy.deepcopy(self.record)
        record["phase"] = 1
        names = [*record["contract"]["files"], "backend/example.txt", "frontend/example.txt"]
        record["snapshot"] = {p: self.make_artifact(p)["sha256"] for p in names}
        record["archive"] = {p: f"harness/reports/phase-1/attempt-1/snapshot/{p}" for p in names}
        for path in record["archive"].values():
            self.make_artifact(path)
        record["contract"]["approval"] = self.make_artifact("harness/reports/phase-1/contract-approval.md")
        record["evidence"] = {key: {"status": "PASS", **self.make_artifact(
            f"harness/reports/phase-1/{key}.md")} for key in gate.CATEGORIES}
        return record

    def save_phase_one(self, record):
        path = self.root / "harness/reports/phase-1/gate.json"
        path.write_text(json.dumps(record))

    def test_later_phase_may_evolve_documents_with_old_archive_intact(self):
        record = self.phase_one()
        self.save_phase_one(record)
        (self.root / "docs/requirements.md").write_text("다음 Phase에서 승인된 문서 진화")
        self.assertTrue(gate.check(self.root, 1).startswith("PASS"))

    def test_implementation_phase_needs_real_outputs(self):
        record = self.phase_one()
        del record["snapshot"]["backend/example.txt"]
        del record["archive"]["backend/example.txt"]
        self.save_phase_one(record)
        with self.assertRaisesRegex(ValueError, "실제 산출물"):
            gate.check(self.root, 1)

    def test_later_phase_contract_still_required(self):
        record = self.phase_one()
        record["contract"]["files"] = {}
        self.save_phase_one(record)
        with self.assertRaisesRegex(ValueError, "계약 해시"):
            gate.check(self.root, 1)


if __name__ == "__main__":
    unittest.main()
