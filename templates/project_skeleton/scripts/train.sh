# Minimal shell script examples. Makefile targets call these.
# scripts/train.sh — launch training with a given experiment override.
python src/train.py "${@}"
