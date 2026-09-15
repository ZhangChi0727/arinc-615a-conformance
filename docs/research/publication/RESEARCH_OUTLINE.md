# Research and Publication Outline

| Field | Value |
|---|---|
| **Version** | 3.0-candidate under CR-2026-012 |
| **Status** | CL-TAV thesis plan; design direction accepted 2026-09-14; not independent mathematical or RG approval |
| **Method** | [`../methodology/RR-2026-001_test_analysis_conformance_methodology.md`](../methodology/RR-2026-001_test_analysis_conformance_methodology.md), DD-028, DD-029, DD-030 |
| **Reader entry** | [`../../../artifacts/publications/cltav/CLTAV_RESEARCH_PLAN.md`](../../../artifacts/publications/cltav/CLTAV_RESEARCH_PLAN.md) |

## Working title

**English:** CL-TAV: Closed-Loop Test–Analysis Verification for Protocol Conformance and Fault Localization—An ARINC 615A Case Study

**Chinese:** CL-TAV：面向协议符合性验证与故障定位的闭环测试—分析协同方法——以 ARINC 615A 为例

## Central question

> How can test observations, constraint verdicts, fault hypotheses and next-test selection form a consistent closed loop for protocol conformance verification and fault localization, using ARINC 615A as a bounded case?

CL-RQ1 (loop consistency), CL-RQ2 (comparative effect under the same budget), and CL-RQ3 (uncertainty and stopping) are the primary questions. Historical RQ1–RQ6 remain mapped in the method report and are not completed by deletion.

## Contributions to evaluate

These are propositions, not established results, and not a claim to have invented Test or Analysis:

1. a first-version CL-TAV loop with set-valued compatibility, one-step minimax selection, preparatory actions, and three-way cannot-shrink stopping (DD-029);
2. a system-engineering architecture that separates the **verification-session** machine from the **protocol-operation** machine and joins them only by interfaces and observations;
3. a comparative experiment protocol (fixed Test, Analysis, non-feedback T+A, full CL-TAV) with no unrun results filled here;
4. an expanded protocol CRS, generated only after source-unit audit, covering INFORMATION, UPLOAD, both DOWNLOAD modes, FIND, and conditional network variants.

Review gates, timed EFSM supporting math, and held-out mutation remain supporting material. Equation (14) stays a non-default comparison model.

## Chapter plan

Each chapter below states the claim it must carry, the CL-RQ it answers, the algorithm or architecture it uses, the experiment or evidence it needs, planned figures, what already exists, and the remaining gap. Titles alone are not a plan.

### Chapter 1 Introduction

- **Claim:** Protocol conformance work that only executes a fixed suite, or only analyses a model without feeding the next test, leaves detection and localization under a finite budget incomplete.
- **Answers:** motivates CL-RQ1–CL-RQ3; does not answer them.
- **Uses:** problem framing only; no algorithm yet.
- **Needs:** no confirmatory data; cites engineering ICD practice and the bounded M2 UPLOAD/INFORMATION merge as the case starting point.
- **Figures:** none required; may reuse FIG-CL-TAV-01 context.
- **Have / gap:** method report §1 exists; introduction prose may start later. Must not claim CL-TAV superiority.

### Chapter 2 Related work and problem definition

- **Claim:** Requirements-based testing, ioco-style conformance, mutation adequacy and diagnostic classifiers each supply part of detection or localization. Whether a cited method already forms an observation→update→select loop with explicit finite termination, preparatory actions and unknown-effect `ERROR` remains a literature question to check against feedback mechanism, fault domain, timing uncertainty, cost objective and stopping guarantee. It is not a proved absence and not a first-invention claim for CL-TAV.
- **Answers:** positions CL-RQ1 against related work; keeps RQ6 (transfer) explicitly unanswered.
- **Uses:** no CL-TAV equations; defines the three comparison arms used later (CL-T, CL-A, CL-TA vs CL-LOOP).
- **Needs:** literature already cited in RR-2026-001; no new “first invention” wording.
- **Figures:** optional related-work map, not SysML.
- **Have / gap:** §1.6 novelty boundary exists. Gap is a method-by-method comparison of those five attributes, not a blanket “not a closed loop” verdict.

### Chapter 3 System-engineering design and CL-TAV architecture

- **Claim:** CL-TAV is realized by layered SysML views in which protocol CRS, tool functions and method goals stay distinct, and two state machines stay distinct.
- **Answers:** CL-RQ1 (structure of the loop); supports CL-RQ3 (where uncertainty and ERROR live).
- **Uses:** SysML 1.6 notation views FIG-CL-TAV-01..08; DD-030 isolation of bound M2; protocol CRS vs tool requirements split.
- **Needs:** no execution evidence. Architecture review, not implementation.
- **Figures:** FIG-CL-TAV-01 context, 02 requirement layers, 03 BDD, 04 IBD, 07 two machines.
- **Have / gap:** DD-030 and this outline. Gap is that views are notation-based, not an executable SysML metamodel.

### Chapter 4 CL-TAV closed-loop algorithm

- **Claim:** First-version objects \(H_0=\{h_{\mathrm{normal}}\}\cup H_{\mathrm{single}}\), observable \(q_k\), compatibility update, one-step minimax \(s(t)\), preparatory actions, and stop classes are specified and internally consistent.
- **Answers:** CL-RQ1 (definitions) and CL-RQ3 (uncertainty partitions, cannot-shrink, termination).
- **Uses:** DD-029; method report §3.9 and §4.11. Termination is \(c_{\min}>0\) plus finite \(B\), or finite \(K_{\max}\); `ERROR` spends the same resource.
- **Needs:** worked examples (already in DD-029), not confirmatory runs. Independent math review still open.
- **Figures:** FIG-CL-TAV-05 activity, 06 diagnostic sequence, 08 parametric constraints.
- **Have / gap:** algorithm text exists. Gap is proof of properties; remaining-set minimax is not claimed globally optimal.

### Chapter 5 Instrument plan and experiment design

- **Claim:** A later development-ready PR can implement the loop; this chapter only plans modules, oracles, comparison arms, isolation and metrics.
- **Answers:** CL-RQ2 (what will be compared) and the engineering half of CL-RQ1.
- **Uses:** four arms CL-T / CL-A / CL-TA / CL-LOOP; detection, localization and ablation families from the work order; no shared secretly-stronger oracle.
- **Needs:** registered experiment protocol before any confirmatory run. No Configuration, no live load.
- **Figures:** reuse FIG-CL-TAV-04 ports as the future tool boundary.
- **Have / gap:** method report §8.1 lists arms. Gap is executable experiment configuration, which belongs to a later PR.

### Chapter 6 Results

- **Claim:** none in this increment. The chapter layout is reserved for later registered experiments.
- **Answers:** will answer CL-RQ2 and CL-RQ3 only after data exist.
- **Uses:** the same stop classes, budgets and \(H_k\) traces specified in Chapter 4.
- **Needs:** detection / false-alarm / pending, localization set accuracy, true-fault exclusion, cost/interaction counts; intervals; held-out isolation.
- **Figures:** planned result templates only; no filled charts.
- **Have / gap:** empty on purpose. Filling numbers now would be a false result claim.

### Chapter 7 Discussion, limitations and further work

- **Claim:** first-version CL-TAV is bounded by single-fault \(H_0\), one-step selection, missing ARINC 645 algorithms, and notation-only SysML.
- **Answers:** interprets CL-RQ3 limitations; does not close RQ6.
- **Uses:** threats already in method report §11; 645 `BLOCKED-SOURCE-645`; out-of-domain faults may mimic in-domain hypotheses.
- **Needs:** no new experiment.
- **Figures:** none.
- **Have / gap:** limitation list exists in DD-029. Discussion prose waits for results.

### Chapter 8 Conclusion

- **Claim:** only restates questions, the first-version design direction, and what remains unapproved.
- **Answers:** none beyond “the loop is specified; it is not independently approved; it is not development-ready.”
- **Uses:** no extra algorithm.
- **Needs:** independent RG0/RG1 and method/math/architecture review on a later Head.
- **Figures:** none.
- **Have / gap:** must not convert design-direction acceptance into independent approval.

## Two state machines

CL-TAV models **two** machines. They must not be merged into one protocol EFSM.

| Machine | States (first version) | Alphabet / interface | Must not |
|---|---|---|---|
| Verification session \(M_{\mathrm{sess}}\) | Idle, Admit, Select, Execute, Update, ErrorHandle, Recover, Prep, and the stop classes | selects from \(S\subseteq A(q_k)\) through FIG-CL-TAV-04 ports; one resource mode | copy UPLOAD/FIND protocol states as its own |
| Protocol operation \(M_{\mathrm{prot}}\) | bound M2 INFORMATION/UPLOAD black box; DOWNLOAD/FIND listed as planned scope without behavior edges | messages, files, timers on the observation port | silently update \(H_k\) or spend verification budget; unaudited Information→other-operation edges |

Association: an Execute step of \(M_{\mathrm{sess}}\) applies a stimulus to \(M_{\mathrm{prot}}\) through FIG-CL-TAV-04 ports and reads \(I_{z_k}\). That association is not a cross-machine state transition. Preparatory actions are session steps in \(A(q_k)\). Bound M2 remains an UPLOAD/INFORMATION protocol model; it is not \(M_{\mathrm{sess}}\) and does not cover new CRS services.

## SysML views

Editable sources live in [`models/`](models/). They are **SysML 1.6 notation-based views**; executable or complete metamodel conformance is not claimed. `satisfy`/`verify` are model relations, not executed verification. Each view is a declared subset.

| ID | View | Algorithm / architecture content that must appear |
|---|---|---|
| FIG-CL-TAV-01 | Context | IUT, adapter, operator, network/clock, 645 integrity boundary |
| FIG-CL-TAV-02 | Requirement layers | method goals ≠ protocol CRS ≠ tool requirements; representative source→CRS→constraint trace with real IDs |
| FIG-CL-TAV-03 | BDD | Test, Observation, Analysis, Diagnosis, Selection, Evidence as separate blocks |
| FIG-CL-TAV-04 | IBD | trace, constraint, candidate-set, test-selection, budget ports |
| FIG-CL-TAV-05 | Closed-loop activity | \(A\) then \(S\), Admit A1–A5, currently valid strictly-reducing minimax then Prep, selected-mode XOR, charge once, exclusive P1–P5 stops, `ERROR` split |
| FIG-CL-TAV-06 | Diagnostic sequence | overlapping observation, preparatory action, later distinguishing test, second \(I_{z_k}\) into Analysis |
| FIG-CL-TAV-07 | Two state machines | \(M_{\mathrm{sess}}\) vs bound-M2 black box; Admit A1–A5; P1–P5 stops; ports not cross-machine transitions |
| FIG-CL-TAV-08 | Parametric | \(I\), \(\varepsilon\), \(J\), \(c_{\min}\), \(B\) or \(K_{\max}\), remaining-set score |

## Source audit before CRS generation

FIND, DOWNLOAD and AFDX-appendix bilingual CRS are corrected in `M1-CANDIDATE-5` after RR-CLTAV-2026-006 REWORK (currently 2796 coverage / 523 requirements; FIND 34 + DOWNLOAD 102 + AFDX 3 after splits and one revocation). Remaining 665/664/RFC body audits are **not** produced by renaming deferred labels. The ledger [`../../../configs/research/cltav_protocol_source_audit.json`](../../../configs/research/cltav_protocol_source_audit.json) keeps FIND 78/78, DOWNLOAD 365/365 and AFDX appendix 13/13 reread records. `profileScope.instanceBoundOperations` stay UPLOAD/INFORMATION; `researchExpandedOperations` are DOWNLOAD/FIND. Media Defined and Operator Defined DOWNLOAD stay separate. AFDX stays a conditional deployment and does not activate the current Compliant instance. Bound M2 does not execute FIND, DOWNLOAD or AFDX; FIND timing is observational catalog only. Batch template fill is forbidden. Tool software requirements stay out of this PR.

## Historical versus successor evidence

The check that the freeze commit still hashes to 94 display-math blocks proves **only** that historical objects were not rewritten. It does **not** prove that successor CL-TAV mathematics is correct. `rr_2026_001_revision_identity.json` keeps `independentMathematicalApproval` and `independentReviewApproval` false, and `historicalMathCheckDoesNotProveSuccessorMath` true. Design-direction acceptance on 2026-09-14 is not an independent Gate.

## Writing order

1. Keep the method and DD-029 objects stable except for explicit tightenings such as finite termination.
2. Finish source-unit audit, then write CRS rows from sources, never from deferred-status labels.
3. Draft Chapters 1–5 against this outline and the SysML views.
4. Register experiments before any confirmatory run; leave Chapter 6 empty until then.
5. Write Chapters 7–8 only after claim/evidence review of actual results.

# 中文版

| 字段 | 值 |
|---|---|
| **版本** | CR-2026-012 下的 3.0-candidate |
| **状态** | CL-TAV 论文计划；2026-09-14 接受设计方向；不是独立数学或 RG 批准 |
| **方法** | [`../methodology/RR-2026-001_test_analysis_conformance_methodology.md`](../methodology/RR-2026-001_test_analysis_conformance_methodology.md)，DD-028、DD-029、DD-030 |
| **读者入口** | [`../../../artifacts/publications/cltav/CLTAV_RESEARCH_PLAN.md`](../../../artifacts/publications/cltav/CLTAV_RESEARCH_PLAN.md) |

## 工作题目

英文题目为 *CL-TAV: Closed-Loop Test–Analysis Verification for Protocol Conformance and Fault Localization—An ARINC 615A Case Study*；中文题目为《CL-TAV：面向协议符合性验证与故障定位的闭环测试—分析协同方法——以 ARINC 615A 为例》。

## 核心问题

测试观测、约束判定、故障假设与后续测试选择如何形成一致闭环，用于协议符合性验证与故障定位，并以 ARINC 615A 作为有界案例？主问题为 CL-RQ1、CL-RQ2、CL-RQ3。历史 RQ1–RQ6 在方法报告中映射，不因删除而完成。

## 待评价贡献

这些是命题，不是既成结果，也不声称发明了 Test 或 Analysis：

1. 首版 CL-TAV 闭环：集合式相容、一步 minimax、准备性动作、三分“不能缩小”停止（DD-029）；
2. 把**验证会话**状态机与**协议操作**状态机分开、只通过接口和观测关联的系统工程架构；
3. 固定 Test、Analysis、非反馈 T+A 与完整 CL-TAV 的比较实验协议（此处不填未跑结果）；
4. 仅在来源单元审计之后生成的扩大协议 CRS（INFORMATION、UPLOAD、两种 DOWNLOAD、FIND 及条件化网络变体）。

评审门、时序 EFSM 支撑数学和留出变异仍是支撑材料。方程 (14) 仍为非默认比较模型。

## 章节计划

以下每章都写明必须承载的论点、回答的 CL-RQ、所用算法或架构、所需实验或证据、计划图、已有材料和缺口。只有标题不算计划。

### 第1章 引言

- **论点：** 只执行固定套件、或只分析模型而不把结果送入下一测试，会在有限预算下把检测与定位做不完整。
- **回答：** 提出 CL-RQ1–CL-RQ3，并不回答它们。
- **使用：** 只做问题界定，尚无算法。
- **需要：** 无确认性数据；以工程 ICD 实践和已合并的有界 M2 UPLOAD／INFORMATION 为案例起点。
- **图：** 不强制；可复用 FIG-CL-TAV-01。
- **已有／缺口：** 方法报告 §1 已有；引言正文可后写。不得声称 CL-TAV 优越。

### 第2章 相关工作与问题定义

- **论点：** 基于需求的测试、ioco 符合、变异充分性和诊断分类器各自提供检测或定位的一部分。某一被引方法是否已经构成带显式有限终止、准备性动作和效果未知 `ERROR` 的观测→更新→选择闭环，仍须按反馈机制、故障域、时序不确定性、成本目标和停止保证对照文献，不能由术语分类得出“已有工作都不是闭环”，也不得据此声称 CL-TAV 首次发明。
- **回答：** 把 CL-RQ1 放到相关工作中；RQ6 明确未回答。
- **使用：** 不用 CL-TAV 方程；定义后文比较臂 CL-T、CL-A、CL-TA 与 CL-LOOP。
- **需要：** RR-2026-001 已引用文献；不得新写“首次发明”。
- **图：** 可选相关工作图，不是 SysML。
- **已有／缺口：** §1.6 创新边界已有。缺口是按上述五个属性做方法对方法比较，而不是总括“不是闭环”。

### 第3章 系统工程设计与 CL-TAV 架构

- **论点：** CL-TAV 由分层 SysML 视图实现：协议 CRS、工具功能、方法目标分离；两套状态机分离。
- **回答：** CL-RQ1（闭环结构）；支撑 CL-RQ3（不确定性和 ERROR 的位置）。
- **使用：** SysML 1.6 记法视图 FIG-CL-TAV-01..08；DD-030 对绑定 M2 的隔离；协议 CRS 与工具需求分离。
- **需要：** 无执行证据。这是架构评审，不是实现。
- **图：** FIG-CL-TAV-01 上下文、02 需求层次、03 BDD、04 IBD、07 两套机器。
- **已有／缺口：** DD-030 与本大纲。缺口是视图仅为记法，不是可执行 SysML 元模型。

### 第4章 CL-TAV 闭环算法

- **论点：** 首版对象 \(H_0=\{h_{\mathrm{normal}}\}\cup H_{\mathrm{single}}\)、可观测 \(q_k\)、相容更新、一步 minimax \(s(t)\)、准备性动作和停止类已规定且内部一致。
- **回答：** CL-RQ1（定义）与 CL-RQ3（不确定性分区、不能缩小、终止）。
- **使用：** DD-029；方法报告 §3.9 与 §4.11。终止为 \(c_{\min}>0\) 加有限 \(B\)，或有限 \(K_{\max}\)；`ERROR` 消耗同一资源。
- **需要：** DD-029 已有走查，不是确认性运行。独立数学审查仍开放。
- **图：** FIG-CL-TAV-05 活动、06 诊断序列、08 参数约束。
- **已有／缺口：** 算法正文已有。缺口是性质证明；剩余集 minimax 不声称全局最优。

### 第5章 工具实现计划与实验设计

- **论点：** 后继开发就绪 PR 才能实现该闭环；本章只规划模块、oracle、比较臂、隔离和指标。
- **回答：** CL-RQ2（将比较什么）以及 CL-RQ1 的工程一半。
- **使用：** 四臂 CL-T／CL-A／CL-TA／CL-LOOP；工作单中的检测、定位、消融；不得共用暗中更强的 oracle。
- **需要：** 确认性运行前先登记实验协议。无 Configuration，无实网加载。
- **图：** 复用 FIG-CL-TAV-04 端口作为未来工具边界。
- **已有／缺口：** 方法报告 §8.1 已列比较臂。缺口是可执行实验配置，属于后继 PR。

### 第6章 结果

- **论点：** 本增量无结果。本章只保留布局。
- **回答：** 有数据后才回答 CL-RQ2 与 CL-RQ3。
- **使用：** 第4章规定的同一停止类、预算和 \(H_k\) 迹。
- **需要：** 检测／误报／未决、定位集合正确率、真实故障误排除、成本／交互次数；区间；留出隔离。
- **图：** 只计划结果模板，不填数。
- **已有／缺口：** 刻意留空。现在填数就是虚假结果主张。

### 第7章 讨论、局限与后续工作

- **论点：** 首版 CL-TAV 受单故障 \(H_0\)、一步选择、缺失 645 算法和仅记法 SysML 约束。
- **回答：** 解释 CL-RQ3 的局限；不关闭 RQ6。
- **使用：** 方法报告 §11 的威胁；645 `BLOCKED-SOURCE-645`；域外故障可能与域内假设相同。
- **需要：** 无新实验。
- **图：** 无。
- **已有／缺口：** DD-029 已有局限清单。讨论正文等结果。

### 第8章 结论

- **论点：** 只重述问题、首版设计方向，以及尚未批准的事项。
- **回答：** 仅“闭环已规定；尚未独立批准；不是开发就绪”。
- **使用：** 无额外算法。
- **需要：** 后继 Head 上的独立 RG0／RG1 与方法／数学／架构评审。
- **图：** 无。
- **已有／缺口：** 不得把设计方向接受改写成独立批准。

## 两套状态机

CL-TAV 建**两套**机器，不得并成一个协议 EFSM。

| 机器 | 首版状态 | 字母表／接口 | 禁止 |
|---|---|---|---|
| 验证会话 \(M_{\mathrm{sess}}\) | Idle、Admit、Select、Execute、Update、ErrorHandle、Recover、Prep 及停止类 | 经 FIG-CL-TAV-04 端口从 \(S\subseteq A(q_k)\) 选择；一种资源模式 | 把 UPLOAD／FIND 协议状态当成自己的状态 |
| 协议操作 \(M_{\mathrm{prot}}\) | 已绑定 M2 的 INFORMATION／UPLOAD 黑箱；DOWNLOAD／FIND 仅作计划范围、无行为边 | 观测端口上的消息、文件、计时器 | 静默更新 \(H_k\) 或消耗验证预算；无依据的 Information→其他操作边 |

关联：\(M_{\mathrm{sess}}\) 的 Execute 经 FIG-CL-TAV-04 端口对 \(M_{\mathrm{prot}}\) 施加刺激并读取 \(I_{z_k}\)。该关联不是跨机状态迁移。准备性动作是 \(A(q_k)\) 中的会话步骤。已绑定 M2 仍是 UPLOAD／INFORMATION 协议模型；它不是 \(M_{\mathrm{sess}}\)，也不覆盖新 CRS 服务。

## SysML 视图

可编辑源在 [`models/`](models/)。它们是 **SysML 1.6 记法视图**；不声称可执行或完整元模型符合性。`satisfy`／`verify` 是模型关系，不是已执行验证。每图都是声明的子集。

| ID | 视图 | 必须出现的算法／架构内容 |
|---|---|---|
| FIG-CL-TAV-01 | 上下文 | IUT、适配器、操作者、网络／时钟、645 完整性边界 |
| FIG-CL-TAV-02 | 需求层次 | 方法目标 ≠ 协议 CRS ≠ 工具需求；带真实 ID 的来源→CRS→约束代表追踪 |
| FIG-CL-TAV-03 | BDD | Test、Observation、Analysis、Diagnosis、Selection、Evidence 分块 |
| FIG-CL-TAV-04 | IBD | trace、constraint、候选集、测试选择、预算端口 |
| FIG-CL-TAV-05 | 闭环活动 | 先 \(A\) 再 \(S\)、Admit A1–A5、当前有效严格缩小再 Prep、所选模式 XOR、一次计费、互斥 P1–P5 停止、拆分 `ERROR` |
| FIG-CL-TAV-06 | 诊断序列 | 重叠观测、准备性动作、随后的区分测试、第二次 \(I_{z_k}\) 进入 Analysis |
| FIG-CL-TAV-07 | 两套状态机 | \(M_{\mathrm{sess}}\) 对已绑定 M2 黑箱；Admit A1–A5；P1–P5 停止；端口而非跨机状态迁移 |
| FIG-CL-TAV-08 | 参数 | \(I\)、\(\varepsilon\)、\(J\)、\(c_{\min}\)、\(B\) 或 \(K_{\max}\)、剩余集评分 |

## 来源审计先于 CRS 生成

FIND、DOWNLOAD 与 AFDX 附录双语 CRS 已按 RR-CLTAV-2026-006 REWORK 纠正为 `M1-CANDIDATE-5`（当前 2796 条 coverage／523 条需求；拆分与一项撤销后为 FIND 34＋DOWNLOAD 102＋AFDX 3）。其余 665／664／RFC 正文审计**不**靠改名延期标签产生。清单 [`../../../configs/research/cltav_protocol_source_audit.json`](../../../configs/research/cltav_protocol_source_audit.json) 仍保存 FIND 78/78、DOWNLOAD 365/365 与 AFDX 附录 13/13 条重读记录。`profileScope.instanceBoundOperations` 仍为 UPLOAD／INFORMATION；`researchExpandedOperations` 为 DOWNLOAD／FIND。Media Defined 与 Operator Defined DOWNLOAD 保持分开。AFDX 仍为条件化部署，不激活当前 Compliant 实例。绑定 M2 不执行 FIND、DOWNLOAD 或 AFDX；FIND 时序只进入观察目录。禁止批量套模板。工具软件需求不属于本 PR。

## 历史与后继证据

冻结提交上 94 块显示数学的核验**只**证明历史对象未被改写，**不**证明后继 CL-TAV 数学正确。`rr_2026_001_revision_identity.json` 保持 `independentMathematicalApproval` 与 `independentReviewApproval` 为 false，且 `historicalMathCheckDoesNotProveSuccessorMath` 为 true。2026-09-14 的设计方向接受不是独立 Gate。

## 写作顺序

1. 除有限终止等已明确收紧外，保持方法与 DD-029 对象稳定。
2. 先完成来源单元审计，再按原文写 CRS 行，绝不按延期状态词生成。
3. 按本大纲和 SysML 视图起草第1–5章。
4. 任何确认性运行前登记实验；第6章在有数据前留空。
5. 主张—证据评审实际结果后再写第7–8章。
