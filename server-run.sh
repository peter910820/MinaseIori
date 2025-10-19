#!/usr/bin/env zsh
set -euo pipefail

# 取得腳本所在目錄（不受工作目錄影響）
SCRIPT_DIR="${0:A:h}"

# 虛擬環境目錄
VENV_PATH="$SCRIPT_DIR/.venv"

# 檢查虛擬環境存在
if [[ ! -d "$VENV_PATH" ]]; then
  echo "找不到虛擬環境: $VENV_PATH"
  exit 1
fi

# 直接執行虛擬環境內的 Python，不需要額外 activate, deactivate
"$VENV_PATH/bin/python" "$SCRIPT_DIR/app.py"
