# V550 Agent 3: Minto Memo Coach

A local Codex skill for turning **your** charter, WBS, and timeline into **your own memo of no more than two pages** for the fictional *Allocating the Waldron* scenario. The coach explains Minto ideas, asks one question at a time, and gives concise feedback. You can keep going even if a file is missing or a draft is rough.

## Install

You need Git, Python 3.11 or newer, and Codex Desktop or Codex CLI. Get the package and run:

```sh
git clone https://github.com/ChakriOriginals/v550-agent-3-minto-memo-coach-student.git
cd v550-agent-3-minto-memo-coach-student
python3 tools/verify_package.py
python3 install.py
```

The installer copies the skill to `~/.agents/skills/v550-agent-3-minto-memo-coach-student`. It stops if that folder exists; it never replaces an installation silently. Quit and reopen Codex after installing.

## Start

Open a **local Codex chat** with this folder as the workspace. In Codex Desktop, select Codex and open this folder. For the CLI, you can run `./start-v550.sh` from this folder. Then send:

```text
Use $v550-agent-3-minto-memo-coach-student to coach me through my Minto memo. I have my charter, WBS, and timeline.
```

Attach or paste whatever you have. No special filename, Agent 1 or 2 transcript, review ZIP, Living Project File, key, PIN, or course account is needed. The coach reads your work but does not write your memo or submit anything. If your course asks for a memo and chat transcript, copy and submit your own through its normal method.

## Other ways to start

- `Use $v550-agent-3-minto-memo-coach-student. I'm not sure who my memo is for.`
- `Use $v550-agent-3-minto-memo-coach-student. I have a draft. Can you help me review it?`
- `Use $v550-agent-3-minto-memo-coach-student. What's the difference between a Main Idea and a topic?`

## Update or reinstall

Run `python3 tools/verify_package.py` on the new package. Quit Codex, then move the existing installed folder aside to keep a backup, or remove it if you no longer need it. Run `python3 install.py` again and reopen Codex. The installer will stop until the old destination has been moved or removed. To test without touching your installed copy, set `V550_SKILLS_HOME` to an empty temporary skills folder before running the installer.

## Local data boundary

This package has no reporting, analytics, roster access, or automatic transcript collection. It does not call a course service. Codex itself uses its normal chat and account behavior, so the package does not make Codex offline or telemetry-free. Share only the course files you are comfortable putting in your Codex chat.
