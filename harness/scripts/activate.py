#!/usr/bin/env python3
"""사용자 터미널에서 준비본을 .codex로 설치. Agent는 보호 경로 환경에서 실행 금지."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]


def main():
    source = ROOT / "harness/codex"
    target = ROOT / ".codex"
    paths = [source / "config.toml", *sorted((source / "agents").glob("*.toml"))]
    if len(paths) != 6:
        raise ValueError("설정 1개와 Agent 5개 필요")
    if target.is_symlink() or (target / "agents").is_symlink():
        raise ValueError("대상 symlink 금지")
    targets = [(p, target / p.relative_to(source)) for p in paths]
    if any(dst.exists() or dst.is_symlink() for _, dst in targets):
        raise ValueError("기존 설정 발견: 자동 덮어쓰기 금지. 먼저 비교·병합 필요")
    target.mkdir(exist_ok=True)
    (target / "agents").mkdir(exist_ok=True)
    for src, dst in targets:
        with dst.open("xb") as stream:
            stream.write(src.read_bytes())
    print("설정 6개 복사 완료. validate.py --active 후 새 Codex 세션에서 스모크 실행 필요.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print(f"활성화 실패: {exc}. 새로 생성된 파일 유무를 확인하고 다시 실행 전 비교하세요.",
              file=sys.stderr)
        sys.exit(1)
