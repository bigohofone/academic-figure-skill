#!/bin/bash
# Runs one headless Claude session per task folder, in parallel, with no user
# CLAUDE.md and no auto-memory, so a skill is tested the way a new user meets it.
#
# usage: examples/run-isolated.sh <prompt-file> <skill-dir or ""> <task-folder>...
# Each task folder (outside this repo) holds the *-task.md files and their data;
# the session's log goes to <task-folder>/run.log.
prompt=$(cat "$1")
skill=$2
shift 2
for dir in "$@"; do
  (
    cd "$dir" || exit 1
    claude -p --setting-sources project ${skill:+--add-dir "$skill"} \
      --allowedTools "Bash Read Write Edit Glob Grep" --permission-mode acceptEdits \
      "$prompt" < /dev/null > run.log 2>&1
    echo "$(basename "$dir") exit $?"
  ) &
done
wait
