#!/bin/sh
# PostToolUse hook: redraw only what the edited file feeds, in the background. Builds run in parallel, and a
# newer edit stops the older run of the same build so runs never pile up.
file=$(jq -r '.tool_input.file_path // empty')
cd "$CLAUDE_PROJECT_DIR" || exit 0
case "$file" in
  */skills/paper-figure/assets/*) set -- examples/layouts/layouts.py examples/build_charts.py examples/papers/build.py ;;
  */examples/layouts/layouts.py) set -- examples/layouts/layouts.py ;;
  */examples/chart-types/*) set -- examples/build_charts.py ;;
  */examples/papers/build.py) set -- examples/papers/build.py ;;
  */examples/papers/*/*) set -- "examples/papers/build.py $(echo "$file" | sed -E 's|.*/examples/papers/([^/]+)/.*|\1|')" ;;
  *) exit 0 ;;
esac
for build in "$@"; do
  pkill -f "python $build"
  log="examples/layouts/last-run-$(basename "${build%% *}" .py).log"
  nohup uv run --no-project -p 3.12 --with 'matplotlib>=3.10' --with numpy --with pyyaml --with scipy --with pymupdf \
    python $build > "$log" 2>&1 &
done
exit 0
