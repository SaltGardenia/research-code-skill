# 参考：科研代码注释规范（中文版 · 供开发者阅读）

> 本文件是 `references/code_comments.md` 的中文对照版。智能体运行时仍应加载英文原版。

本参考是 **科研（ML/DL）代码中的注释纪律** 的事实来源。这是与一般 Python 风格不同的独立关注点：
科研代码不是商业软件——注释的意义**不是**“解释每一行”，而是记录**科研意图、数学逻辑、设计决策、
实验约束**，使代码传递科研思考，而非仅仅能跑。它被融合进**工程过程**集群（`engineering_process.md`），
因为注释/docstring 纪律是该集群“接口纪律”的一半，并以注释*必须说什么* 扩展了
`RC-ENG-001`（每个公共符号有文档）与 `RC-ENG-007`（接口文档永不漂移）。

背书参考体系（它们塑造下述规则）：

- Google Python Style Guide（注释节）
- NumPy/SciPy Docstring Standard
- PEP 257 Docstring Convention
- Google Engineering Practices（code review：注释）
- Clean Code（Robert C. Martin）——意图揭示命名优于注释
- PyTorch 官方代码风格
- scikit-learn API Documentation Style

## 核心原则

### COMMENT001：注释解释“为什么”，而非“什么”

代码已经说了它在做什么。

**不推荐**
```python
# 给 x 加一
x += 1
```
**推荐**
```python
# 索引偏移 1，因为数据集标注使用 1-based 索引，
# 而 PyTorch 使用 0-based 索引。
x += 1
```
解释：*为什么*这样做，以及背后的*假设*。

## 注释分类（6 类）

```text
注释类型
├── API 文档            # 公共符号做什么
├── 算法解释            # 非平凡算法如何推进
├── 数学解释            # 数学背后的公式
├── 设计决策            # 为什么选这个方法
├── 实验注记            # 观测到的经验行为 / 约束
└── 警告 / 限制         # 危险、不稳定、已知限制
```

## 函数 docstring（COMMENT002）

每个公共函数都需要 docstring。推荐风格：**NumPy docstring**（兼容 PEP 257）。
必须陈述 Parameters / Returns / Notes：

```python
def compute_attention(
    query,
    key,
    value,
    temperature=1.0,
):
    """
    Compute scaled dot-product attention.

    This implementation follows the formulation introduced
    in "Attention Is All You Need".

    Parameters
    ----------
    query : torch.Tensor
        Query embeddings with shape (B, N, C).
    key : torch.Tensor
        Key embeddings with shape (B, N, C).
    value : torch.Tensor
        Value embeddings with shape (B, N, C).
    temperature : float
        Scaling factor for attention logits.

    Returns
    -------
    torch.Tensor
        Attention output with shape (B, N, C).

    Notes
    -----
    The temperature term is introduced to stabilize
    training when using low-dimensional embeddings.
    """
```

## 类注释（COMMENT003）

每个核心模块必须说明：功能、I/O、设计来源：

```python
class TokenPruner(nn.Module):
    """
    Dynamic token pruning module.

    The module estimates token importance scores and removes
    redundant tokens during inference.

    Reference:
        DynamicViT:
            Dynamic Vision Transformer with Attention-Based
            Token Sparsification.

    Attributes
    ----------
    keep_ratio : float
        Percentage of tokens retained.
    """
```

## 数学公式注释（COMMENT004）

科研代码例行编码公式——展示公式，引用来源：

```python
# Attention computation:
#
#        QK^T
# A = softmax(-----)
#        sqrt(d)
#
# Following Vaswani et al. (2017).
attention = torch.softmax(
    q @ k.transpose(-2, -1)
    / math.sqrt(dim),
    dim=-1,
)
```
绝不要写 `# calculate attention`——那什么也没说。

## 算法块注释（COMMENT005）

复杂算法必须解释其分阶段逻辑（Transformer、优化、数值方法、仿真）：

```python
# ----------------------------------------------------
# Stage 1:
#   用 CLS attention 估计 token 重要性。
#
# Stage 2:
#   按重要性分数选择 top-k token。
#
# Stage 3:
#   为后续 transformer 块保留所选 token。
# ----------------------------------------------------
tokens = select_tokens(x)
```

## 设计决策注释（COMMENT006）——高优先级

科研代码不断需要论证*为什么这样设计*：

```python
# 此处把重要性分数 detach。
#
# 原因：
#   剪枝决策不应直接影响 attention 的学习目标。
#
# 这遵循两阶段优化策略。
score = score.detach()
```

## TODO 注释（COMMENT007）

禁止：`# TODO fix this`。推荐——owner + 动作 + 原因 + issue：

```python
# TODO(username): 收集验证统计后，用自适应校准替换启发式阈值。
#
# Issue:
# https://github.com/project/issues/12
```
格式：`TODO(owner): action + reason`。

## FIXME 注释（COMMENT008）

用于已知问题 / 临时 workaround：

```python
# FIXME:
#   当方差趋近零时出现数值不稳定。
#
# 临时方案：
#   加 epsilon=1e-6。
```

## WARNING 注释（COMMENT009）

用于危险代码：

```python
# WARNING:
#   此操作改变 tensor 布局。
#   在 view() 前不要移除 contiguous()。
x = x.contiguous()
```

## 实验相关注释（COMMENT010）

科研代码尤其需要记录经验约束：

```python
# Experiment Note:
#
#   移除该归一化会使 ImageNet 精度下降约 0.5%。
#
#   保持该行为与论文设置一致。
x = self.norm(x)
```

## 禁止的注释

### COMMENT011：无代码重述
```python
# convolution
conv = nn.Conv2d(...)   # 禁止
```

### COMMENT012：无无意义注释
```python
# model
model = Model()          # 禁止
```

### COMMENT013：无陈旧注释
```python
# use ResNet
model = ViT()            # 禁止——注释对代码说谎
```

## 注释语言（COMMENT014）

- **开源科研：仅英文**——国际协作、GitHub 受众、论文复现。
- **中文：仅允许**用于临时实验笔记（`# 实验临时记录`），绝不用于核心代码逻辑。

## 注释密度标准（COMMENT015）

越多越好是错的。推荐比例：

| 代码类型 | 注释比例 |
|----------|----------|
| 简单工具 | ~10% |
| 算法模块 | 20–30% |
| 数学实现 | 30–40% |
| 论文核心方法 | 40%+ |

## 科研代码特殊要求（COMMENT016）

每个**论文核心模块**必须含一个模块级文档块：

```text
模块文档
├── Purpose（目的）
├── Mathematical formulation（数学形式）
├── Reference paper（参考论文）
├── Input shape（输入形状）
├── Output shape（输出形状）
├── Complexity（复杂度）
└── Design choice（设计选择）
```

示例：
```python
class SparseAttention(nn.Module):
    """
    Sparse multi-head attention.

    Paper:
        Efficient Transformer XXX

    Complexity:
        Dense:  O(N^2)
        Sparse: O(kN)

    Input:  x: [B, N, C]
    Output: y: [B, N, C]
    """
```

## AI 智能体代码修改规则（COMMENT017）

嵌入智能体工作流：
```text
COMMENT_RULES
添加代码前：
  1. 识别算法复杂度。
  2. 检查是否存在数学逻辑。
  3. 为非显然决策加解释。
修改后：
  1. 更新过时的注释。
  2. 删除误导性的注释。
  3. 为新公共 API 加 docstring。
```

## Rule Card（机器可执行）

| 代码 | 规则 | 严重度 |
|------|------|--------|
| COMMENT001 | 注释解释**为什么**，而非**什么**（说明假设/意图）。 | MAJOR |
| COMMENT002 | 每个公共函数/类带 docstring（NumPy/PEP257 风格）。 | MAJOR |
| COMMENT003 | 核心模块 docstring 说明功能、I/O、设计来源/参考。 | MAJOR |
| COMMENT004 | 数学算法以注释形式带公式 + 引文。 | MAJOR |
| COMMENT005 | 复杂算法带阶段性（Stage 1/2/3）块注释。 | MINOR |
| COMMENT006 | 非显然的设计决策带 `Reason:` 注释。 | MAJOR |
| COMMENT007 | `TODO(owner): action + reason`（+ issue 链接）；无裸 `TODO`。 | MINOR |
| COMMENT008 | 已知问题用 `FIXME:` 并附临时解决方案说明。 | MINOR |
| COMMENT009 | 危险代码用 `WARNING:` 说明危害。 | MINOR |
| COMMENT010 | 经验约束用 `Experiment Note:`（观测到的差异）。 | MINOR |
| COMMENT011 | 无代码重述注释（`# convolution`）。 | MINOR |
| COMMENT012 | 无无意义注释（`# model`）。 | MINOR |
| COMMENT013 | 无与代码矛盾的陈旧注释（`# use ResNet` + `ViT()`）。 | MAJOR |
| COMMENT014 | 核心代码注释用英文；中文仅用于临时实验笔记。 | MINOR |
| COMMENT015 | 注释密度匹配代码类型（工具 ~10% —— 论文核心 40%+）。 | MINOR |
| COMMENT016 | 每个论文核心模块都有 Purpose/Formula/Reference/IO/Complexity/Design 文档块。 | MAJOR |
| COMMENT017 | 修改时更新/删除陈旧注释，并为新公共 API 写 docstring。 | MAJOR |

## 如何与本技能其余部分协同

- `COMMENT002`/`COMMENT003` **就是** `RC-ENG-001`（每个公共符号有文档）在科研代码上的具体化；
  `COMMENT017` **就是** `RC-ENG-007`（接口文档永不漂移）在注释上的应用。
- `COMMENT001`（为什么而非什么）是 Google 注释规则的科研级重述；它压倒逐行叙述的冲动。
- 与 `RC-SP-002`（docstring + 类型）和 `PL-DOC`（公共方法 docstring）配对：
  *存在性*由这些代码拥有；*内容*（意图、数学、设计、实验）由 `COMMENT-*` 拥有。
- 整理（场景 B）时，智能体**绝不能**保留陈旧注释（`COMMENT013`）：
  若它把 `ResNet` 重命名为 `ViT`，它要在同一遍中删除 `# use ResNet` 那行。
