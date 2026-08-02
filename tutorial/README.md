# Verification Tutorial Workspace

Tutorials translate controlled methodology and released engineering artifacts
into reproducible learning paths. They are downstream products: useful for
teaching and operation, but never authoritative for requirements, formal
semantics, verdicts, or research claims.

## Product lines

| Product | Entry | Purpose |
|---|---|---|
| Common verification tutorial | [`common/README.md`](common/README.md) | protocol-independent concepts, methods, evidence reasoning, and exercises |
| ARINC 615A instance tutorial | [`arinc615a/README.md`](arinc615a/README.md) | concrete conformance workflow using a named baseline, tool release, and examples |

The two lines may cross-reference common concepts, but ARINC-specific material
must not be presented as a universal verification rule.

## Dependency and traceability rule

Each controlled tutorial declares the applicable subset of:

```text
tutorial_id
tutorial_version
tutorial_type
explains_baseline
explains_tool_release
example_artifact_ids
evidence_manifest_ids
source_or_concept_references
normative: false
```

Executable ARINC 615A lessons must pin the baseline and tool release. Common
concept lessons may mark tool- and example-specific fields not applicable, but
must still identify the concept sources and project baseline used for wording.

## Promotion and feedback rule

Tutorial observations may open an issue, CR, or DD. They cannot directly change
the method or engineering release. Corrected upstream artifacts are reviewed and
versioned first; the tutorial then updates its references.

---

# 中文版

教程把受控方法论和已发布工程产物转化为可复现的学习路径。它们是下游产品：可用于教学与操作，但不对需求、形式语义、判定或研究主张拥有权威。

## 产品线

| 产品 | 入口 | 用途 |
|---|---|---|
| 通用验证教程 | [`common/README.md`](common/README.md) | 协议无关的概念、方法、证据推理和练习 |
| ARINC 615A 实例教程 | [`arinc615a/README.md`](arinc615a/README.md) | 使用具名基线、工具发布和示例讲解具体符合性流程 |

两条产品线可以交叉引用通用概念，但不得把 ARINC 专用材料表述为普遍验证规则。

## 依赖与追踪规则

每份受控教程声明以下字段的适用子集：

```text
tutorial_id
tutorial_version
tutorial_type
explains_baseline
explains_tool_release
example_artifact_ids
evidence_manifest_ids
source_or_concept_references
normative: false
```

可执行的 ARINC 615A 课程必须固定基线和工具发布。通用概念课程可以把工具和示例字段标为不适用，但仍须标明概念来源以及措辞采用的项目基线。

## 晋级与反馈规则

教程观察可以发起 issue、CR 或 DD，但不能直接改变方法或工程发布。上游产物必须先完成修正、评审和版本化，教程随后更新引用。
