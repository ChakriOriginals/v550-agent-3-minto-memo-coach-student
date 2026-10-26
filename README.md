# V550 Agent 3: Minto Memo Coach

This Codex coach helps you turn **your** charter, WBS, and timeline into **your own memo of no more than two pages** for the fictional *Allocating the Waldron* scenario. It explains Minto ideas, asks one question at a time, and gives specific feedback. A rough draft or a missing file is fine.

Plan for about 45–60 minutes if you can. You can pause, skip ahead, or stop at any point.

## Start in this folder — no installation needed

1. Get this folder with **Code → Download ZIP** on [GitHub](https://github.com/ChakriOriginals/v550-agent-3-minto-memo-coach-student), then unzip it. If you use Git, run:

   ```sh
   git clone https://github.com/ChakriOriginals/v550-agent-3-minto-memo-coach-student.git
   ```

2. Open the `v550-agent-3-minto-memo-coach-student` folder as a local project in Codex Desktop. For Codex CLI on Mac or Linux, run `./start-v550.sh` from the folder. On Windows, open a terminal in the folder and run `codex --sandbox read-only -c web_search=disabled`.

3. Start a new chat with this command so Codex selects the coach reliably:

   ```text
   Use $v550-agent-3-minto-memo-coach-student to coach me through my memo. I have my charter, WBS, and timeline.
   ```

Attach the files or paste what you have. No special filename, prior-agent transcript, review ZIP, Living Project File, key, PIN, or course account is needed. If one item is missing, the coach asks once and continues.

### Other ways to start

- `Use $v550-agent-3-minto-memo-coach-student. I'm not sure who my memo is for.`
- `Use $v550-agent-3-minto-memo-coach-student. I have a draft. Can you review it?`
- `Use $v550-agent-3-minto-memo-coach-student. What's the difference between a Main Idea and a topic?`

If you are tired, say so and ask for the short path. If you are stuck, say “I'm stuck.” You may explain why you disagree with a suggestion. To pause, ask for a short note you can bring to your next chat.

## Your memo and chat

You write the memo; the coach does not create or submit it. Copy your own memo and chat transcript through the course's normal submission method **if the course requires them**. Check your syllabus or ask your instructor about format.

## Optional installation for other folders

You can use the coach from this folder without Python. To make it available in other Codex projects, install it with Python 3.11 or newer:

```sh
python3 tools/verify_package.py
python3 install.py
```

On Windows, use `py` instead of `python3`. The installer copies the skill to `~/.agents/skills/v550-agent-3-minto-memo-coach-student` and stops if that folder already exists. Reopen Codex afterward. If both copies are visible while this folder is open, choose the repository copy.

For an update, run `git pull` in this folder or download a fresh ZIP. If you installed a copy, quit Codex, move that installed folder aside, rerun `python3 install.py`, and reopen Codex. The installer never overwrites a copy silently.

## Privacy and local tools

This package contains no analytics, roster access, reporting service, or automatic transcript collection. It does not contact a course service. Codex uses its normal chat and account behavior, so share only material you are comfortable putting in a Codex chat.

The Mac/Linux CLI launcher starts Codex with a read-only sandbox and web search disabled. The Windows command above uses the same settings. These launch settings do not configure Codex Desktop or disable all local computation. The coach's instructions prohibit web research for this fictional scenario and limit file use to read-only inspection.

## Package checks

Maintainers can run `python3 tools/verify_package.py` and `python3 -m unittest discover -s tests -p 'test_*.py'`. [Conversation checks](tests/conversation_checks.md) provide synthetic student situations for manual coaching review.
