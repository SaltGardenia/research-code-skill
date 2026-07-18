# Reference: Research Code Comment Standard

Source of truth for **code-comment discipline in research (ML/DL) code**.
This is a distinct concern from *general* Python style: research code is not
commercial software — the point of a comment is **not** "explain every
line", it is to record **research intent, mathematical logic, design
decisions, and experimental constraints** so the code transmits research
thinking, not just runs. Fused into the **Engineering Process** cluster
(`engineering_process.md`) because comment/docstring discipline is the
"interface discipline" half of that cluster, and it extends `RC-ENG-001`
(doc on every public symbol) and `RC-ENG-007` (interface docs never drift)
with *what* a research comment must say.

Endorsed reference systems (these shape the rules below):
- Google Python Style Guide (comment section)
- NumPy/SciPy Docstring Standard
- PEP 257 Docstring Convention
- Google Engineering Practices (code review: comments)
- Clean Code (Robert C. Martin) — intent-revealing names over comments
- PyTorch official code style
- scikit-learn API Documentation Style

## Core principle

### COMMENT001: comments explain "Why", not "What"

Code already says what it does.

**Not recommended**
```python
# Add one to x
x += 1
```

**Recommended**
```python
# Offset the index by one because the dataset annotation
# follows 1-based indexing while PyTorch uses 0-based indexing.
x += 1
```
Explain: *why* it is done, and the *assumption* behind it.

## Comment taxonomy (6 types)

```
Comment Types
├── API Documentation      # what the public symbol does
├── Algorithm Explanation  # how a non-trivial algorithm proceeds
├── Mathematical Explanation # the formula behind the math
├── Design Decision      # why this approach was chosen
├── Experiment Note       # observed empirical behavior / constraint
└── Warning / Limitation  # danger, instability, known limit
```

## Function docstring (COMMENT002)

Every public function needs a docstring. Recommended style: **NumPy docstring**
(PEP 257 compatible). It must state Parameters / Returns / Notes:
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

## Class comment (COMMENT003)

Every core module must state: function, I/O, and design source:
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

## Mathematical formula comment (COMMENT004)

Research code routinely encodes formulas — show the formula, cite the source:
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
Do **not** write `# calculate attention` — that states nothing.

## Algorithm block comment (COMMENT005)

Complex algorithms must explain their staged logic (Transformer, optimization,
numerical methods, simulation):
```python
# ----------------------------------------------------
# Stage 1:
#   Estimate token importance using CLS attention.
#
# Stage 2:
#   Select top-k tokens according to importance scores.
#
# Stage 3:
#   Preserve selected tokens for subsequent transformer blocks.
# ----------------------------------------------------
tokens = select_tokens(x)
```

## Design decision comment (COMMENT006) — high priority

Research code constantly needs to justify *why this design*:
```python
# We detach the importance score here.
#
# Reason:
#   The pruning decision should not directly affect
#   the attention learning objective.
#
# This follows the two-stage optimization strategy.
score = score.detach()
```

## TODO comment (COMMENT007)

Forbidden: `# TODO fix this`. Recommended — owner + action + reason + issue:
```python
# TODO(username): Replace heuristic threshold with
# adaptive calibration after collecting validation statistics.
#
# Issue:
# https://github.com/project/issues/12
```
Format: `TODO(owner): action + reason`.

## FIXME comment (COMMENT008)

For known problems / temporary workarounds:
```python
# FIXME:
#   Numerical instability occurs when variance approaches zero.
#
# Temporary solution:
#   Add epsilon=1e-6.
```

## WARNING comment (COMMENT009)

For dangerous code:
```python
# WARNING:
#   This operation changes tensor layout.
#   Do not remove contiguous() before view().
x = x.contiguous()
```

## Experiment-related comment (COMMENT010)

Research code especially needs to record empirical constraints:
```python
# Experiment Note:
#
#   Removing this normalization decreases ImageNet accuracy
#   by approximately 0.5%.
#
#   Keep this behavior consistent with the paper setting.
x = self.norm(x)
```

## Disallowed comments

### COMMENT011: no code restatement
```python
# convolution
conv = nn.Conv2d(...)   # forbidden
```

### COMMENT012: no meaningless comment
```python
# model
model = Model()          # forbidden
```

### COMMENT013: no stale comment
```python
# use ResNet
model = ViT()            # forbidden — comment lies about the code
```

## Comment language (COMMENT014)

- **Open-source research: English only** — international collaboration, GitHub
  audience, paper reproduction.
- **Chinese: allowed** only for temporary experimental notes
  (`# 实验临时记录`), never for core code logic
  (`# 这里进行注意力计算` is forbidden in core code).

## Comment density standard (COMMENT015)

More is not better. Recommended ratio:

| Code type | Comment ratio |
|-----------|---------------|
| Simple utility | ~10% |
| Algorithm module | 20–30% |
| Math implementation | 30–40% |
| Paper-core method | 40%+ |

## Research-code special requirement (COMMENT016)

Every **paper-core module** must contain a module-level doc block:
```
Module Documentation
├── Purpose
├── Mathematical formulation
├── Reference paper
├── Input shape
├── Output shape
├── Complexity
└── Design choice
```
Example:
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

## AI-agent code-modification rule (COMMENT017)

Embed in the agent workflow:
```
COMMENT_RULES
Before adding code:
  1. Identify algorithmic complexity.
  2. Check whether mathematical logic exists.
  3. Add explanation for non-obvious decisions.
After modifying:
  1. Update outdated comments.
  2. Remove misleading comments.
  3. Add docstring for new public APIs.
```

## Rule cards (machine-executable)

| Code | Rule | Severity |
|------|------|----------|
| COMMENT001 | Comment explains **why**, not **what** (states assumption/intent). | MAJOR |
| COMMENT002 | Every public function/class carries a docstring (NumPy/PEP257 style). | MAJOR |
| COMMENT003 | Core module docstring states function, I/O, and design source/reference. | MAJOR |
| COMMENT004 | Mathematical algorithms carry the formula + citation as a comment. | MAJOR |
| COMMENT005 | Complex algorithms carry a staged (Stage 1/2/3) block comment. | MINOR |
| COMMENT006 | Non-obvious design decisions carry a `Reason:` comment. | MAJOR |
| COMMENT007 | `TODO(owner): action + reason` (+ issue link); no bare `TODO`. | MINOR |
| COMMENT008 | Known problems use `FIXME:` with temporary-solution note. | MINOR |
| COMMENT009 | Dangerous code uses `WARNING:` explaining the hazard. | MINOR |
| COMMENT010 | Empirical constraints use `Experiment Note:` (observed delta). | MINOR |
| COMMENT011 | No code-restatement comments (`# convolution`). | MINOR |
| COMMENT012 | No meaningless comments (`# model`). | MINOR |
| COMMENT013 | No stale comments that contradict the code (`# use ResNet` + `ViT()`). | MAJOR |
| COMMENT014 | Core code comments in English; Chinese only for temp experimental notes. | MINOR |
| COMMENT015 | Comment density matches code type (util ~10% … paper-core 40%+). | MINOR |
| COMMENT016 | Every paper-core module has a Purpose/Formula/Reference/IO/Complexity/Design doc block. | MAJOR |
| COMMENT017 | On modify, update/remove stale comments and docstring new public APIs. | MAJOR |

## How to apply with the rest of the skill

- `COMMENT002`/`COMMENT003` **are** `RC-ENG-001` (doc on every public
  symbol) made concrete for research code; `COMMENT017` **is** `RC-ENG-007`
  (interface docs never drift) applied to comments.
- `COMMENT001` (why not what) is the research-grade restatement of the
  Google comment rule; it overrides the urge to narrate every line.
- Pair with `RC-SP-002` (docstrings + types) and `PL-DOC` (public-method
  docstrings): the *presence* is owned by those codes; the *content* (intent,
  math, design, experiment) is owned by `COMMENT-*`.
- When tidying (Scenario B), the agent must **not** preserve stale comments
  (`COMMENT013`): if it renames `ResNet` → `ViT`, it deletes the
  `# use ResNet` line in the same pass.
