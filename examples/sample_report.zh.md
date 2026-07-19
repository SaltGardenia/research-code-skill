# 示例：合规报告（校验门输出）

> 本文件是 `examples/sample_report.md` 的中文对照版。智能体运行时仍应加载英文原版。

当 `scripts/audit_style.py` 作为确认门运行（而非本技能的主要目的）时，它输出 SKILL.md 中固定的
Markdown 表格。这是 `examples/review_request.md` 中的触发在智能体已把合规代码写入 `./my_project`
之后的预期结果。

```markdown
# Research Code Conformance: ./my_project

## Summary
- Files scanned: 14
- Findings: 1 (BLOCKER: 0, MAJOR: 0, MINOR: 1)

## Findings
| ID | Category | Severity | File:Line | Rule | Suggestion |
|----|----------|----------|-----------|------|------------|
| F1 | PYSTYLE | MINOR | src/models/cifar_module.py:88 | GP-LEN | 第 84 行 > 80 字符；请换行（或在 pyproject 中设为 99）。 |

## Next Steps
- 要么换行，要么把项目行宽覆盖设为 99。
```

## 如何复现

```bash
pip install -r requirements.txt
python scripts/audit_style.py ./my_project
```

退出码 `0` 表示无 BLOCKER（规范足够成立，可继续）；`1` 表示至少一处 BLOCKER 必须先修复，
变更才能被接受。
