from __future__ import annotations

import argparse
import json
import os
import platform
import shlex
import socket
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone


def post_event(api_url: str, agent_key: str, payload: dict) -> dict:
    request = urllib.request.Request(
        f"{api_url.rstrip('/')}/api/telemetry/events",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "X-Agent-Key": agent_key},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Send authorized local command telemetry to the CTI dashboard.")
    parser.add_argument("--api-url", default=os.getenv("CTI_API_URL", "http://127.0.0.1:8000"))
    parser.add_argument("--agent-key", default=os.getenv("TELEMETRY_AGENT_KEY", "change-me-agent-key"))
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to execute after --")
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("provide an authorized command after --, for example: python telemetry_agent.py -- whoami")

    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    payload = {
        "command": shlex.join(command),
        "device_name": socket.gethostname(),
        "username": os.getenv("USER") or os.getenv("USERNAME") or "unknown",
        "shell": os.getenv("SHELL") or os.getenv("ComSpec") or "unknown",
        "platform": platform.platform(),
        "source_address": socket.gethostbyname(socket.gethostname()),
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "exit_code": completed.returncode,
        "event_type": "command",
    }
    result = post_event(args.api_url, args.agent_key, payload)
    print(json.dumps({"telemetry": result, "stdout": completed.stdout, "stderr": completed.stderr}, indent=2))
    return completed.returncode


if __name__ == "__main__":
    sys.exit(main())