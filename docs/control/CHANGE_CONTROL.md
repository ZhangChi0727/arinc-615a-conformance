# Change Control

This document defines stable change classes, pull-request discipline and
release rules. Current state is owned by the [root README](../../README.md) and
[`project-status.json`](../../project-status.json).

## 1. Change classes

| Class | Examples | Minimum control |
|---|---|---|
| Editorial | wording or navigation without semantic effect | review and automated checks |
| Engineering | implementation, tests, schemas or evidence production | tests, impact statement and engineering review |
| Research | model, experiment, analysis or claim change | registration/traceability and research review |
| Baseline | scope, formal semantics, assurance tier, gate or ownership change | formal CR and independent approval |
| Release | approved state made externally identifiable | release checks and annotated tag when authorized |

Changes to standard interpretation, applicability, mathematical/timing or
oracle/verdict semantics, method binding, compatibility/evaluation state,
ownership or migration semantics are baseline changes requiring independent
review.

Registering or migrating a standards source, closing an open source dependency,
or changing L1/L2/L3 open-source reuse permission is also a baseline change. It
requires a CR, immutable source/license identity, applicability impact and
independent review; proprietary material and unreviewed L3 reuse stay outside
Git.

## 2. Pull-request rules

Every pull request must:

1. update `README.md` and `project-status.json` together;
2. summarize the increment, current stop, next step and unchanged boundaries;
3. identify affected method inputs and ARINC-owned artifacts;
4. run deterministic local checks and Python 3.10–3.12 CI;
5. preserve atomic baselines, CRs, reviews and historical evidence;
6. keep detailed review transfer in the PR description rather than a new
   HANDOFF or current-status Markdown file.

The comparison base comes from the pull-request event or base ref. It is never
hardcoded as a lifecycle identity.

## 3. Lifecycle identity rules

Mutable SHA, PR, tag, branch and current-state facts live in
`project-status.json`. Executable governance code may contain stable schema,
enumerations and semantic invariants only, each identified as
`STABLE_INVARIANT`. Temporary controls include `temporary`, `owner`,
`introducedBy` and `retireWhen`; validation rejects a control after its
retirement condition is met.

Controlled external semantics use immutable commit-bound locators. A mutable
`main`, `latest` or equivalent ref is navigation only, never semantic identity.

## 4. Review and release

Approval binds the final unchanged head. No commit is added after final
approval. A requested release uses a normal merge commit, waits for post-merge
CI, verifies any authorized annotated tag and removes the temporary branch.
Baseline or tag creation requires explicit scope and authority; ordinary
management or navigation changes create neither.

# 中文版

本文档规定稳定的变更类别、PR 纪律和发布规则。当前状态由
[根 README](../../README.md)与 [`project-status.json`](../../project-status.json) 管理。

## 1. 变更类别

| 类别 | 示例 | 最低控制 |
|---|---|---|
| 编辑性 | 不影响语义的文字或导航 | 评审与自动检查 |
| 工程 | 实现、测试、schema 或证据生产 | 测试、影响声明、工程评审 |
| 研究 | 模型、实验、分析或主张变化 | 注册／追踪与研究评审 |
| 基线 | 范围、形式语义、保证层级、门禁或所有权变化 | 正式 CR 与独立批准 |
| 发布 | 使已批准状态可由外部识别 | 发布检查及经授权的 annotated tag |

对标准解释、适用性、数学／时序或 oracle／verdict 语义、方法绑定、兼容性／评价状态、
所有权或迁移语义的修改均属于 baseline change，必须接受独立评审。

登记或迁移标准来源、关闭开放来源依赖、改变 L1/L2/L3 开源复用许可同样属于 baseline
change，必须具有 CR、不可变来源/许可证身份、适用性影响和独立评审；专有材料及未经评审的
L3 复用不得进入 Git。

## 2. PR 规则

每个 PR 必须：

1. 同时更新 `README.md` 与 `project-status.json`；
2. 概述本次增量、当前停点、下一步和保持不变的边界；
3. 识别受影响的方法输入与 ARINC 所有产物；
4. 运行确定性本地检查和 Python 3.10–3.12 CI；
5. 保持原子 baseline、CR、Review 和历史证据不变；
6. 将详细评审移交写入 PR 描述，而不是新建 HANDOFF 或 current-status Markdown。

比较基点来自 PR 事件或 base ref，绝不硬编码为生命周期身份。

## 3. 生命周期身份规则

可变 SHA、PR、tag、branch 和当前状态事实存放在 `project-status.json`。可执行治理代码只能
包含稳定 schema、枚举和语义不变量，并标记为 `STABLE_INVARIANT`。临时控制包含
`temporary`、`owner`、`introducedBy` 与 `retireWhen`；退役条件满足后校验必须拒绝残留。

受控外部语义使用不可变 commit-bound locator。可变 `main`、`latest` 等只能导航，不能作为
语义身份。

## 4. 评审与发布

批准绑定最终不变 Head；最终批准后不得新增提交。发布按要求使用普通 merge commit，等待
合并后 CI，核验经授权的 annotated tag，并删除临时分支。创建 baseline 或 tag 必须有明确
范围与授权；普通管理或导航变更均不创建二者。
