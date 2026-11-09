#!/usr/bin/env python3
"""준비/활성 Codex 설정 검증. Python 3.11+, Codex CLI 필요. 모델 호출 없음."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[2]
ROLES = {"architect", "backend", "frontend", "reliability", "reviewer"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--active", action="store_true", help="실제 .codex 활성 파일도 확인")
    args = parser.parse_args()
    source = ROOT / "harness/codex"
    config = tomllib.loads((source / "config.toml").read_text())
    require(set(config) == {"approval_policy", "sandbox_mode", "sandbox_workspace_write", "agents"},
            "메인 설정의 지원/허용 키가 아님")
    require(config["approval_policy"] == "never", "승인 확대 금지 정책 불일치")
    require(config["sandbox_mode"] == "workspace-write", "sandbox 불일치")
    require(config["sandbox_workspace_write"] == {"network_access": False}, "network 정책 불일치")
    require(config["agents"] == {"enabled": True, "max_concurrent_threads_per_session": 3},
            "agents 설정 불일치")
    agents = list((source / "agents").glob("*.toml"))
    require({p.stem for p in agents} == ROLES, "정확히 5개의 전문 Agent 필요")
    for path in agents:
        data = tomllib.loads(path.read_text())
        require(set(data) == {"name", "description", "developer_instructions"},
                f"{path.name}: 공식 최소 standalone 키 외 설정")
        require(data["name"] == path.stem, f"{path.name}: 이름 불일치")
        require(all(isinstance(v, str) and v.strip() for v in data.values()),
                f"{path.name}: 필수 문자열 누락")
        for marker in ("AGENTS.md", "산출물", "완료 기준", "실제 SMS", "재위임"):
            require(marker in data["developer_instructions"], f"{path.name}: 규칙 누락 {marker}")
    required = ["AGENTS.md", "docs/PROGRESS.md", "harness/README.md",
                "harness/OWNERSHIP.md", "harness/PROTOCOL.md", "harness/PHASES.md",
                "harness/TASKS.md", "harness/GATE_RECORDS.md", "harness/prompts/phase-0.md",
                "harness/prompts/harness-smoke.md", "harness/templates/gate.json"]
    for name in required:
        require((ROOT / name).is_file(), f"필수 파일 누락: {name}")
    state = json.loads((ROOT / "harness/state.json").read_text())
    require(state["schema_version"] == 1, "state 버전 불일치")
    require([p["phase"] for p in state["phases"]] == list(range(7)), "Phase 0~6 필요")
    require(all(p["status"] in {"NOT_STARTED", "IN_PROGRESS", "VERIFYING", "PASS", "FAIL", "BLOCKED"}
                for p in state["phases"]), "잘못된 Phase 상태")
    if args.active:
        active = ROOT / ".codex"
        require(not active.is_symlink(), ".codex symlink 금지")
        for path in [source / "config.toml", *agents]:
            target = active / path.relative_to(source)
            require(target.is_file() and not target.is_symlink(),
                    f"활성 파일 없음/금지 symlink: {target.relative_to(ROOT)}")
            require(target.read_bytes() == path.read_bytes(), f"준비/활성 불일치: {target.name}")
        require({p.stem for p in (active / "agents").glob("*.toml")} == ROLES,
                "활성 custom 역할이 준비본 5개와 다름")
    binary = shutil.which("codex")
    require(binary is not None, "Codex CLI 없음: 네이티브 설정 검증 미실행")
    # 전역 인증·신뢰·MCP 설정을 복사하지 않는다. 프로젝트 설정을 검증용 HOME 최상위로 복사한다.
    with tempfile.TemporaryDirectory(prefix="mart-codex-validate-") as tmp:
        sandbox = Path(tmp)
        shutil.copyfile(source / "config.toml", sandbox / "config.toml")
        shutil.copytree(source / "agents", sandbox / "agents")
        env = dict(os.environ, CODEX_HOME=tmp)
        result = subprocess.run(
            [binary, "app-server", "--strict-config", "--print-startup-config"],
            cwd=tmp, env=env, text=True, capture_output=True, timeout=30)
        require(result.returncode == 0,
                f"네이티브 strict config 실패(exit={result.returncode}): {result.stderr[-2000:]}")
        startup = json.loads(result.stdout)
        version = startup.get("appServerVersion", "미확인")
    print(json.dumps({
        "status": "PASS", "scope": "active-files" if args.active else "staged-files",
        "toml": 6, "standalone_minimal_schema": "PASS",
        "native_main_config_strict": "PASS", "codex_version": version,
        "active_config": "FILES_MATCH_RUNTIME_UNVERIFIED" if args.active else "NOT_CHECKED",
        "custom_agent_spawn": "NOT_RUN",
        "note": "파일 검증은 프로젝트 신뢰/역할 로딩/실제 spawn 성공을 증명하지 않음"
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
