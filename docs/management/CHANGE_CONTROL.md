# Baseline and Change Control

| Field | Value |
|---|---|
| **Process ID** | CMP-2026-001 |
| **Applies to** | RB-2026-001-v4.2 and controlled descendants |
| **Owner** | Research lead |

## Change classes

| Class | Examples | Approval |
|---|---|---|
| **Editorial** | spelling, formatting, link repair with no semantic effect | document owner |
| **Artifact** | new CRS item, VC, mutant, result, or implementation conforming to baseline | applicable gate owner |
| **Interpretive** | changed standard interpretation, oracle, applicability, or equivalence decision | independent methodology review |
| **Baseline** | changed RQ, scope, formal semantics, assurance tier, gate rule, domain ownership, or cross-domain contract | formal CR and RG6-style independent approval |

## Baseline change request

Create `docs/management/changes/CR-YYYY-NNN.md` containing:

- problem and triggering evidence;
- affected baseline clauses and downstream artifacts;
- scientific and engineering impact;
- alternatives considered;
- migration and re-evaluation plan;
- review findings and disposition;
- new version and effective date if approved.

## Rules

1. Do not silently edit a frozen claim after seeing experimental results.
2. Corrections to mathematical errors are mandatory baseline changes, not
   editorial changes.
3. Scope expansion requires applicability, observation, fault-model, schedule,
   and confidentiality impact analysis.
4. Superseded documents remain in history and link to the replacing baseline.
5. Every released evidence package records the exact baseline identifier.
6. A baseline version is immutable after its release commit/tag; subsequent
   changes create a new version.
7. A cross-domain interface change identifies affected producers, consumers,
   trace fields, migrations, and tutorial/publication references.

## Git and PR policy

- branch new work from an up-to-date `main`;
- use `codex/` for Codex-created branches unless a project branch is specified;
- keep methodology, engineering, and evidence changes separable where practical;
- PR descriptions identify affected RQs, gates, claims, and baseline;
- methodology changes require a methodology reviewer independent of the author;
- raw evidence changes require provenance and reproduction checks;
- squash only when the resulting commit preserves useful baseline and gate IDs.

Recommended baseline tag after approval: `research-baseline/RB-2026-001-v4.2`.

---

# 中文版

变更分为：不改变语义的编辑变更；符合基线的新 CRS/VC/变异体/结果等产物变更；改变标准解释、oracle、适用性或等价判断的解释变更；改变 RQ、范围、形式语义、保证层级、门禁、领域所有权或跨领域契约的基线变更。数学修正和时序语义变化必须作为基线变更，不得伪装成编辑修订。

## 变更类别

编辑、产物、解释和基线四类变更按上述语义划分；以影响而非文件类型决定类别。

## 基线变更请求

基线变更请求必须记录触发问题、受影响条款和下游产物、科学/工程影响、备选方案、迁移/重评计划、评审处理以及批准后的版本和日期。发布后的基线不可原地修改；每个证据包记录精确基线 ID。

## 规则

数学修正、时序语义、oracle、适用性和保证层级变化不得伪装成编辑；既有证据不得仅通过改标签迁移；解释冲突必须进入裁决和风险记录。跨领域接口变化必须标明受影响生产者、消费者、追踪字段、迁移以及教程/出版引用。

## Git 与 PR 政策

基线变更使用专用分支和 PR，保持 Draft 直至独立评审完成；PR 必须链接 CR、DD、验证结果和迁移影响，合并后才建立冻结标签。
