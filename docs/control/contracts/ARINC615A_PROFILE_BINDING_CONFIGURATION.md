# ARINC 615A Profile, Binding, and Configuration Contract

| Field | Value |
|---|---|
| **Contract ID** | PBC-ARINC615A-2026-001 |
| **Version** | 0.2-candidate |
| **Baseline** | RB-2026-001-v4.3.1 acknowledgement candidate |
| **External method binding** | `TMP-XRB-ARINC615A-01` |
| **MethodCompatibilityDispositionCommit** | `c02330d21fe2d3e89e7e2d6352872d52461a6dda` |
| **Compatibility** | REVIEWED-COMPATIBLE-WITH-QUALIFICATION — Q-01–Q-09 |
| **Instance evaluation** | NOT-EXERCISED |
| **Project Configuration** | NOT YET ESTABLISHED |
| **Review status** | PENDING INDEPENDENT REVIEW |

## 1. Four-layer ownership model

| Layer | Identity and status | Owns | Must not own |
|---|---|---|---|
| Candidate GVS Core | external commit `48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b`; EXTERNAL / READ-ONLY / OPEN-CANDIDATE | generic object roles, relations, constraints, extension points, and method contract | ARINC messages, project values, or this repository's local taxonomies |
| Conformance-Testing Profile candidate | `TMP-CTP-ARINC615A-01`; `0.1-candidate` | applicability/CRS formation policy; conformance-testing roles; review, evidence, and closure policy; local A/R and RG/G taxonomies; selected extension-point policies | concrete ARINC messages, IUT values, or claims of generic authority |
| ARINC 615A Product Binding candidate | `TMP-PB-ARINC615A-01`; `0.1-candidate` | ARINC applicability locators, observable objects/interactions, timed model, Test Purpose/VC/procedure realization, Oracle interfaces, adapters, local trace relations, VCS, and diagnostics | generic Core definitions or executed project values |
| Project Configuration | `TMP-PC-ARINC615A-01`; NOT YET ESTABLISHED | selected method/Profile/Binding versions; standard/applicability/IUT/setup/procedure/tool/environment values; clock and error budget; run parameters, evidence destination, reviewers, and access boundary | method semantics, Profile policy, or fabricated execution history |

The dependency direction is Core → Profile → Binding → Configuration. A lower
layer may select or realize an upstream extension point, but may not silently
redefine it. Findings travel upstream only through controlled change proposals.

## 2. Candidate Profile policy

The Profile candidate may define how an applicability/PICS-like declaration
forms an applicable CRS population and how Test Purposes, Verification Cases,
procedures, results/verdicts, review, evidence admission, and closure participate
in this conformance-testing instance. It may select candidate policies for
coverage, sufficiency, independence, assumptions, A0–A4, R0–R5, and RG/G.

These terms remain local candidates. ISO/IEC 9646 correspondence has not been
established clause by clause; PICS, Test Purpose, ATS, and PIXIT must not be
presented as adopted Generic GVS Core or source-native conclusions.

## 3. Product Binding policy

The Product Binding realizes the Profile for the scoped ARINC 615A subject. It
may reference controlled standard locators without copying proprietary text;
define observable protocol objects, roles, states, timing, and boundaries; bind
the clock-augmented EFSM/timed IOLTS; and provide executable cases, procedures,
Oracle implementations, adapters, and evidence mappings.

An Oracle specifies an evaluation rule; applying it to controlled
Observation(s) produces a Result/verdict. A Result is not an Observation. A PASS
does not automatically close a Verification Objective,
support a claim, establish compliance, or obtain authority acceptance.

### Controlled source boundary

The current Product Binding source authority is ARINC 615A-3 as identified in
[`controlled_sources.json`](../../../configs/research/controlled_sources.json).
Its ASCII wire-version value `A4` is not an edition label. ARINC 665-5 is only a
bounded data-format reference and is not an equivalent substitute for 665-3.
ARINC 645 is an open dependency, so affected complete-integrity capabilities
remain unearned. Historical 615A-4 wording has no current technical authority.
M0 creates no CRS item, model, operation or execution qualification.

## 4. Project Configuration policy

No actual configuration has yet been established or exercised for this
migration. `TMP-PC-ARINC615A-01` is a temporary registry key for a future
configuration record, not evidence of one. Before execution, a controlled
configuration must fix all selected versions and values, including the IUT,
test setup, procedure, tool, environment, clock source, measurement-error
budget, timeout, seeds, logging, storage, reviewers, approvals, and access rules.

Configuration identity is required for repeatability but does not itself prove
that the Profile/Binding is compatible with the external method.

## 5. Change and finding route

Instance defects remain local. Binding defects change the ARINC realization.
Profile-contract ambiguities change Profile policy. Suspected Core insufficiency
or overconstraint, evaluation-protocol defects, and candidate generalizations
are Framework Change Proposal inputs for the method repository; this repository
must not directly edit or shadow the Core.

Compatibility is `REVIEWED-COMPATIBLE-WITH-QUALIFICATION` under Q-01–Q-09;
instance evaluation remains `NOT-EXERCISED` and Project Configuration remains
`NOT YET ESTABLISHED`. This acknowledgement candidate becomes effective only
after its own independent review, ordinary merge, and identified v4.3.1 tag.

---

# 中文版

# ARINC 615A Profile、Binding 与 Configuration 契约

| 字段 | 值 |
|---|---|
| **契约 ID** | PBC-ARINC615A-2026-001 |
| **版本** | 0.2-candidate |
| **基线** | RB-2026-001-v4.3.1 确认候选 |
| **外部方法绑定** | `TMP-XRB-ARINC615A-01` |
| **兼容性** | REVIEWED-COMPATIBLE-WITH-QUALIFICATION——受 Q-01–Q-09 限定 |
| **实例评价** | NOT-EXERCISED |
| **Project Configuration** | NOT YET ESTABLISHED |
| **评审状态** | 等待独立评审 |

## 1. 四层所有权模型

| 层 | 身份与状态 | 拥有 | 不得拥有 |
|---|---|---|---|
| Candidate GVS Core | 外部提交 `48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b`；外部/只读/开放候选 | 通用对象角色、关系、约束、扩展点和方法契约 | ARINC 报文、项目值或本仓库本地 taxonomy |
| Conformance-Testing Profile candidate | `TMP-CTP-ARINC615A-01`；`0.1-candidate` | 适用性/CRS 形成政策、符合性测试角色、评审/证据/关闭政策、本地 A/R 与 RG/G taxonomy、扩展点选择 | 具体 ARINC 报文、IUT 值或通用定义权主张 |
| ARINC 615A Product Binding candidate | `TMP-PB-ARINC615A-01`；`0.1-candidate` | ARINC 适用性定位、可观测对象/交互、时序模型、TP/VC/规程实现、Oracle 接口、适配器、本地追踪、VCS 和诊断 | 通用 Core 定义或已执行项目值 |
| Project Configuration | `TMP-PC-ARINC615A-01`；尚未建立 | 选定版本以及标准/适用性/IUT/装置/规程/工具/环境、时钟/误差预算、运行参数、证据目的地、评审者与访问边界 | 方法语义、Profile 政策或虚构的执行历史 |

依赖方向为 Core → Profile → Binding → Configuration。下游可以选择或实现上游扩展点，
但不得静默重定义；finding 只能通过受控变更提案反馈上游。

## 2. 候选 Profile 政策

Profile 候选可以规定适用性/PICS-like 声明如何形成适用 CRS 总体，以及 Test Purpose、
Verification Case、规程、结果/判定、评审、证据准入和关闭如何参与该符合性测试实例；也可以
为 coverage、sufficiency、independence、assumption、A0–A4、R0–R5 和 RG/G 选择候选政策。

这些术语仍是本地候选。ISO/IEC 9646 对应尚未逐条建立，不得把 PICS、Test Purpose、
ATS 或 PIXIT 表述成已被 Generic GVS Core 采纳或已确立的源生结论。

## 3. Product Binding 政策

Product Binding 为限定范围的 ARINC 615A 对象实现 Profile。它可以在不复制专有原文的
前提下引用受控标准定位符，定义可观测协议对象、角色、状态、时序与边界，绑定带时钟 EFSM/
timed IOLTS，并提供可执行用例、规程、Oracle 实现、适配器及证据映射。

Oracle 规定评价规则；将其应用于受控 Observation 后产生 Result/verdict。Result 不是
Observation。PASS 不自动关闭 VO、支持主张、建立合规或取得权威接受。

### 受控来源边界

当前 Product Binding 的来源权威是
[`controlled_sources.json`](../../../configs/research/controlled_sources.json) 登记的 ARINC
615A-3。其 ASCII 线版本值 `A4` 不是版次标签。ARINC 665-5 只是有边界的数据格式参考，
不等价替代 665-3。ARINC 645 是开放依赖，因此受影响的完整完整性能力仍未取得。历史
615A-4 文字不再具有当前技术权威。M0 不创建 CRS 条目、模型、操作或执行资格。

## 4. Project Configuration 政策

此次迁移尚未建立或执行实际配置。`TMP-PC-ARINC615A-01` 只是未来配置记录的临时登记键，
不是配置证据。执行前必须以受控配置固定全部选定版本和值，包括 IUT、测试装置、规程、工具、
环境、时钟源、测量误差预算、timeout、seed、日志、存储、评审/批准身份和访问规则。

配置身份是复现的必要条件，但本身不能证明 Profile/Binding 与外部方法兼容。

## 5. 变更与 finding 路由

实例缺陷留在本地；Binding 缺陷改变 ARINC 实现；Profile-contract ambiguity 改变 Profile
政策。疑似 Core insufficiency/overconstraint、评价协议缺陷和候选泛化只能形成提交方法仓库的
Framework Change Proposal 输入；本仓库不得直接编辑或复制遮蔽 Core。

兼容性为受 Q-01–Q-09 限定的 `REVIEWED-COMPATIBLE-WITH-QUALIFICATION`；实例评价保持
`NOT-EXERCISED`，Project Configuration 保持 `NOT YET ESTABLISHED`。本确认候选仅在
自身独立评审、普通合并并确定 v4.3.1 标签后生效。
