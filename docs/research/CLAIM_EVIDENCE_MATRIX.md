# Claim–Evidence Matrix

This matrix controls what may be stated in reports, releases, and thesis text.
Status is earned by evidence; implementation progress alone cannot promote it.
The active research method is **CL-TAV**. Unit tests, walk-throughs and CI do
not show that CL-TAV outperforms any comparison arm. Historical
`RB-2026-001-v4.2` T0–T3 labels remain valid only under their frozen baseline
wording. The v4.3 ARINC/Profile claim categories are retained as local
assurance vocabulary; they are not Generic GVS Core claims, and external
correspondence stays `NOT-DETERMINED`.

## ARINC/Profile certification-oriented claim candidates

| Claim ID | Permitted claim | Required evidence | Assurance state |
|---|---|---|---|
| A-BASIS | A controlled normative, applicability, and configuration basis exists | controlled standard edition, applicability declaration, CRS identity/version, configuration authority | A0 |
| A-TRACE | Applicable requirements and obligations are traceable to reviewed verification objectives and activities | CRS, `rho_RA`, `rho_RO`, `rho_OM`, `rho_TV` matrices | A1 |
| A-EXEC | Named verification executions are valid and evidence-complete under controlled configuration | test article/setup/procedure conformity, execution validity, raw/derived provenance, evidence integrity | A2 |
| A-OBJ | Named verification objectives are satisfied by reviewed evidence | objective satisfaction records, required evidence classes, reviewed closure | A3 |
| A-COMP | Named protocol-level compliance claims are supported by a complete controlled evidence package | compliance evidence index, objective satisfaction records, limitations and non-claims | A4 |

`A4` does not depend on research maturity `R4` or `R5`.

## CL-TAV contribution claims (this increment)

These map proposed contributions onto theory, the experiment plan, or
system-engineering artefacts. Status is **Specified** or **To be verified**.
Passing tests is not Result, Evidence, or a superiority Claim.

| Claim ID | Permitted claim | Required evidence | Status |
|---|---|---|---|
| CL-C1 | In the declared finite domain, interpretation, timing verdict and whole-history update are specified to be consistent; true-hypothesis retention is conditional on R1--R5 | method conditional argument, ALG-CLTAV-06/07, independent math review, later controlled executions | Specified proposition; no universal drift/loss/reordering theorem; empirical verification open |
| CL-C2 | Current feasible affordable tests are ranked by prior-free one-step worst residual cardinality, then cost and identifier, within existing lifecycle exits | ALG-CLTAV-05, fair four-arm registration, later controlled comparisons | Specified proposition; not first active loop or global optimum; empirical verification open |
| CL-SPEC | First-version CL-TAV objects, update, one-step minimax, Prep/Recover/ERROR and exclusive stops are specified | method report §3.9–§3.9.1, DD-029, loop walk-throughs | Specified; author arguments present; independent math review open |
| CL-ARCH | Verification-session and protocol-operation machines join only by declared interfaces | SysML FIG-CL-TAV-01..08, DD-030 | Specified; notation views, not executable metamodel |
| CL-DETECT | Detection and error-judgement comparison of CL-T / CL-A / CL-TA / CL-LOOP | EXP-CLTAV-DETECT registration and later held-out runs | To be verified; no numbers in this PR |
| CL-LOCATE | In-domain localization / candidate reduction under the same budget | EXP-CLTAV-LOCATE | To be verified |
| CL-ABLATION | Feedback, FIND-clock non-waiver and Prep/Recover cost change outcomes | EXP-CLTAV-ABLATION, including the forbidden abort-waiver negative control | To be verified |
| CL-CRS | Expanded protocol CRS is reviewable for INFORMATION, UPLOAD, both DOWNLOAD modes, FIND, bounded 665/664/RFC support and 615A-triggered 645 semantic leaves | M1 package, source audit, bilingual review view | Specified as candidate; 645 SOURCE/SEMANTIC bound; capabilities NOT-ESTABLISHED; not independently approved |
| CL-ALG | Top-level CL-TAV process and abstract interfaces are specified | ALG-CLTAV-01, method §3.9.2, DD-033 | Specified; not implemented; independent math review open |
| CL-DEV | A bounded finite-path kernel, eight algorithm bindings, seven experiment bindings and synthetic contract witnesses are development-specified | `CLTAV-DEVELOPMENT-CONTRACTS` and generated bilingual review view | Specification candidate only; no parser, solver, IUT, integrity capability or experiment executed |

Observation → Result → Evidence → Argument/Decision → Claim stays the control
boundary. ARINC 645-1 2021 is identity-bound for 615A-triggered CRC, check-value
and naming leaves; CRC/check-value/naming/complete-integrity capabilities stay
not established.

## Engineering claims

| Claim ID | Permitted claim | Required evidence |
|---|---|---|
| E-TIME | Named timing obligations are satisfied for specified executions under the declared measurement-error budget | approved timing catalog, clock-augmented model, raw timestamps, clock/error metadata, robust verdict reproduction |
| E-REPRO | A named evidence package can be reproduced from controlled source, tool, and environment configuration | CI, manifests, checksums, runbook, reproducibility record |

## Research claims

| Claim ID | Permitted claim | Required evidence | Maturity state |
|---|---|---|---|
| R-MUT | The VCS detected a declared evaluated set of valid non-equivalent mutants or faults | T1 equivalence decisions, mutant catalog, results | R2 |
| R-HOLDOUT | Held-out fault detection performance was measured | held-out split, detection rates with intervals | R3 |
| R-CAL | Evidence interpretation was calibrated under a declared observation model | independent calibration, prior and dependence sensitivity | R4 |
| R-DIAG | Declared fault classes were localized with reported held-out performance | held-out diagnosis instances, baselines, abstention results | R4 |
| R-XFER | Specified method elements were replicated on a second protocol instance | completed second-protocol instance and comparative analysis | R5 |

Research maturity does not grant certification status. Failure to reach `R4` or
`R5` does not block `A4`.

## Historical claims

These claims were defined under `RB-2026-001-v4.2`. The v4.3 vocabulary below is
a retained mapping, not a silent relabel and not a second active research
main-line. They remain valid only under their historical baseline wording.

| Historical claim | v4.3 replacement | Note |
|---|---|---|
| C-T0 | A-TRACE | traceability now traces to reviewed objectives |
| C-T1 | A-EXEC, A-OBJ | execution validity and reviewed satisfaction are separated |
| C-TIME | E-TIME | engineering claim, now distinct from assurance status |
| C-T2 | R-MUT, R-HOLDOUT | research-only, not a higher assurance tier |
| C-T3 | R-CAL | research-only; does not block A4 |
| C-DIAG | R-DIAG | research-only |
| C-XFER | R-XFER | research-only, second-protocol replication |
| C-ENG | E-REPRO | engineering claim

## Wording rules

Use:

- “traceability-complete for CRS version …”;
- “PASS was observed under configuration …”;
- “the observation interval was contained in the requirement interval under
  error budget …”;
- “objective OSR-… was satisfied by reviewed evidence …”;
- “detected \(k/n\) evaluated valid non-equivalent mutants”.

Avoid:

- “the finite suite proves all protocol behavior”;
- “100% coverage proves conformance”;
- “mutation score is diagnostic coverage” without a population argument;
- “PASS frequency is the probability the IUT conforms”;
- “the measured point timestamp exactly satisfies the bound” when nonzero
  measurement uncertainty applies;
- “protocol-independent” before R-XFER is supported;
- any wording that implies mutation, Bayesian calibration, diagnosis, or
  cross-protocol replication is required for certification-oriented assurance.

## Literature-qualified publication wording (CR-2026-018 / DD-042)

| Publication proposition | Permitted wording now | Literature qualification | Evidence needed to advance |
|---|---|---|---|
| C1 consistency | Interpretation, timing verdict and whole-history update are specified to be mutually consistent under the declared finite model, ownership, pairing and conservative-observation assumptions | Compatible-run diagnosis under latency, clock mapping and out-of-order observation already exists; exact-once and source liveness premises are not inherited (`EVID-2026-040`--`045`) | independent mathematical review plus controlled executions; a stronger loss/drift/reordering theorem needs a separate method decision |
| C2 selection | The current feasible affordable test set is ranked by one-step worst residual cardinality, then cost and identifier, with existing lifecycle exits | Diagnostic-state feedback, conditional active plans and time-interval control are prior art (`EVID-2026-001`--`015`, `028`--`030`, `038`) | fair arm mapping and registered results; no first-loop or global-optimum wording |
| Aviation relevance | 615A supplies the legal action, observation and evidence context; F-LAS/IMA/CDS motivate scenarios, traceability and threats | Those works address different standards/tasks; F-LAS procedures were not executed and CDS precision shares the OCL oracle (`EVID-2026-053`--`060`, `067`--`075`) | independent 615A execution and truth evidence |
| Evaluation | Report all attempts, detection answered cases, localization decisions/correctness/candidate size and named excluded/unresolved flows separately | Equivalent/undecided mutants and selective answering can bias denominators (`EVID-2026-061`--`065`, `076`--`080`) | frozen registration, adjudicator, units, dependence and interval/effect-size method |

These rows qualify prose; they do not promote any claim status or create a new
claim authority. Manuscript bibliography keys are bound to source/evidence IDs
in `manuscript_manifest.json` and mechanically checked against the evidence
ledger.

## Status transitions

Certification-oriented: `Planned → Evidence Collected → In Review → Supported / Not Supported / Open`.
Research: `Planned → Reproduced → Evaluated → Held-Out / Calibrated / Replicated`.

Every transition must name an artifact version and a gate record. `Not
Supported` and `Incomplete` are valid outcomes and must not be erased by editing
the claim after observing results. No automatic promotion from execution
verdict to objective status, or from objective status to compliance status, is
permitted.

---

## CR-2026-019 implementation-design obligations

This attachment does not promote any claim. `CL-C1` remains conditional on the
finite domain, ownership/pairing, conservative interpretation, R1--R5 and a
versioned whole-history handle. Its minimum falsifiers include uncertainty
identity drift, treating an observation class as H, exclusion of a valid true
hypothesis, or unconditional FAIL from insufficient evidence. `CL-C2` separates
implementation conformance from measured benefit; prediction gaps, truth
leakage, omitted cost, TEST-scoring of Prep/Recover, or global-optimality wording
falsify the implementation/wording obligation. Independent mathematical and
scientific review remain open. The full argument and witnesses are in
`EXPERIMENT_IMPLEMENTATION_SPEC.md`; finite references and synthetic accounting
are indexed by `configs/research/cltav_experiment_design.json`.

# 中文版

本矩阵控制报告、发布和论文允许使用的主张。状态由证据获得，实现进度本身不能晋级。
活动研究方法是 **CL-TAV**。单元测试、走查和 CI 不表示 CL-TAV 优于任一对照臂。
历史 `RB-2026-001-v4.2` 的 T0–T3 仅在冻结基线措辞下有效。v4.3 的 ARINC/Profile
主张类别作为本地保证词汇保留，不是 Generic GVS Core 主张，外部对应为 `NOT-DETERMINED`。

## CL-TAV 贡献主张（本增量）

这些主张把拟议贡献映射到理论、实验方案或系统工程制品。状态为 **Specified** 或 **To be verified**。
通过测试不是 Result、Evidence 或优越性 Claim。

| 主张 ID | 允许主张 | 所需证据 | 状态 |
|---|---|---|---|
| CL-C1 | 在声明有限域中，解释、时序判定与全历史更新被规格为一致；真实假设保留以 R1～R5 为条件 | 方法条件性论证、ALG-CLTAV-06／07、独立数学评审、后续受控执行 | 已规格化命题；不是漂移／丢失／乱序的普遍定理；实证仍开放 |
| CL-C2 | 当前有限可行、可负担测试按无默认先验的一步最坏剩余数、成本和标识排序，并服从既有生命周期退出 | ALG-CLTAV-05、公平四臂登记、后续受控比较 | 已规格化命题；不是首次主动闭环或全局最优；实证仍开放 |
| CL-SPEC | 首版 CL-TAV 对象、更新、一步 minimax、Prep／Recover／ERROR 与互斥停止已规格化 | 方法报告 §3.9–§3.9.1、DD-029、闭环走查 | Specified；作者论证已给出；独立数学评审仍开放 |
| CL-ARCH | 验证会话机与协议操作机仅经声明接口连接 | SysML FIG-CL-TAV-01..08、DD-030 | Specified；记法视图，不是可执行元模型 |
| CL-DETECT | CL-T／CL-A／CL-TA／CL-LOOP 的检测与错误判定比较 | EXP-CLTAV-DETECT 登记及随后留出运行 | To be verified；本 PR 不填数字 |
| CL-LOCATE | 同一预算下的域内定位／候选缩减 | EXP-CLTAV-LOCATE | To be verified |
| CL-ABLATION | 反馈、FIND 时钟不豁免与 Prep／Recover 成本改变结局 | EXP-CLTAV-ABLATION，含禁止的中止豁免反例对照 | To be verified |
| CL-CRS | 扩大协议 CRS 对 INFORMATION、UPLOAD、两种 DOWNLOAD、FIND、有界 665／664／RFC 支持及 615A 触发的 645 语义叶可评审 | M1 包、来源审计、双语评审视图 | Specified 为候选；645 来源／语义已绑定；能力未建立；未经独立批准 |
| CL-ALG | CL-TAV 总体过程与抽象接口已规格化 | ALG-CLTAV-01、方法报告 §3.9.2、DD-033 | Specified；未实现；独立数学评审仍开放 |

观察→结果→证据→论证／决策→主张边界保持。ARINC 645-1 2021 已按 615A 触发的 CRC、校验值与命名叶完成身份绑定；CRC／校验值／命名／完整完整性能力仍未建立。

## ARINC/Profile 面向认证候选主张

| 主张 ID | 允许主张 | 所需证据 | 保证状态 |
|---|---|---|---|
| A-BASIS | 受控的规范、适用性与配置基础存在 | 受控标准版本、适用性声明、CRS 身份／版本、配置权威 | A0 |
| A-TRACE | 适用需求与义务可追踪至已评审验证目标与活动 | CRS、`rho_RA`、`rho_RO`、`rho_OM`、`rho_TV` 矩阵 | A1 |
| A-EXEC | 命名验证执行在受控配置下有效且证据完整 | 被试／装置／程序符合性、执行有效性、原始／派生溯源、证据完整性 | A2 |
| A-OBJ | 命名验证目标由受评审证据满足 | 目标满足记录、所需证据类、受评审闭合 | A3 |
| A-COMP | 命名协议级合规主张由完整受控证据包支持 | 合规证据索引、目标满足记录、限制与非主张 | A4 |

`A4` 不依赖研究成熟度 `R4` 或 `R5`。

## 工程主张

| 主张 ID | 允许主张 | 所需证据 |
|---|---|---|
| E-TIME | 在声明测量误差预算下，命名时序义务对指定执行得到满足 | 已批准时序目录、时钟增强模型、原始时间戳、时钟／误差元数据、稳健判定复现 |
| E-REPRO | 命名证据包可由受控源、工具与环境配置复现 | CI、清单、校验和、运行手册、可复现记录 |

## 研究主张

| 主张 ID | 允许主张 | 所需证据 | 成熟度状态 |
|---|---|---|---|
| R-MUT | VCS 检测到声明评价的有效非等价变异体或故障集 | T1 等价判定、变异体目录、结果 | R2 |
| R-HOLDOUT | 留出故障检测性能已测量 | 留出划分、带区间的检测率 | R3 |
| R-CAL | 证据解释在声明观测模型下已校准 | 独立校准、先验与依赖敏感性 | R4 |
| R-DIAG | 声明故障类在留出性能下定位 | 留出诊断实例、对照、弃权结果 | R4 |
| R-XFER | 指定方法要素在第二协议实例上复现 | 已完成的第二协议实例与比较分析 | R5 |

研究成熟度不授予认证状态；未达 `R4`/`R5` 不阻塞 `A4`。

## 历史主张

下列主张定义于 `RB-2026-001-v4.2`。下表 v4.3 词汇是保留映射，不是静默重标，也不是第二条活动研究主线。它们仅在历史基线措辞下有效。

| 历史主张 | v4.3 替代 | 说明 |
|---|---|---|
| C-T0 | A-TRACE | 追踪性现追踪到已评审目标 |
| C-T1 | A-EXEC、A-OBJ | 执行有效性与受评审满足分离 |
| C-TIME | E-TIME | 工程主张，现与保证状态分离 |
| C-T2 | R-MUT、R-HOLDOUT | 仅研究，非更高保证层级 |
| C-T3 | R-CAL | 仅研究；不阻塞 A4 |
| C-DIAG | R-DIAG | 仅研究 |
| C-XFER | R-XFER | 仅研究，第二协议复现 |
| C-ENG | E-REPRO | 工程主张

## 措辞规则

允许：

- “对 CRS 版本……而言追踪性完整”；
- “在配置……下观察到 PASS”；
- “在误差预算……下，观测区间包含于需求区间”；
- “目标 OSR-… 经受评审证据满足……”；
- “检出 \(k/n\) 个评价有效非等价变异体”。

禁止：

- “有限套件证明全部协议行为”；
- “100% 覆盖即符合”；
- 无总体论证时把“突变分数当作诊断覆盖”；
- “PASS 频率即 IUT 符合概率”；
- 在非零测量不确定性下说“测得点时间精确满足边界”；
- 在 R-XFER 成立前使用“与协议无关”；
- 任何暗示突变、贝叶斯校准、诊断或跨协议复现为面向认证保证所必需的措辞。

## 文献限定的出版措辞（CR-2026-018／DD-042）

| 出版命题 | 当前允许措辞 | 文献限定 | 晋级所需证据 |
|---|---|---|---|
| C1 一致性 | 在声明有限模型、所有权、配对与保守观测假设下，解释、时序判定和全历史更新被规格为相互一致 | 已有工作覆盖时延、时钟映射和乱序观测下的相容运行诊断；不继承 exact-once 与来源活性前提（`EVID-2026-040`～`045`） | 独立数学评审与受控执行；更强的丢失／漂移／乱序定理须另开方法决定 |
| C2 选择 | 当前有限可行、可负担测试集按一步最坏剩余数、成本、标识排序，并保留既有生命周期退出 | 按诊断状态反馈、条件主动计划和时区间控制均为先例（`EVID-2026-001`～`015`、`028`～`030`、`038`） | 公平实验臂映射与登记结果；不得写“首次闭环”或“全局最优” |
| 航空相关性 | 615A 提供合法动作、观测与证据语境；F-LAS／IMA／CDS 用于场景、追踪与威胁 | 这些工作对象／标准不同；F-LAS 规程未执行，CDS precision 与比较器共享 OCL oracle（`EVID-2026-053`～`060`、`067`～`075`） | 独立 615A 执行与真值证据 |
| 评价 | 分开报告全部尝试、检测回答、定位决策／正确性／候选集大小及具名排除／未决流 | 等价／未决变异体和选择性回答会偏置分母（`EVID-2026-061`～`065`、`076`～`080`） | 冻结登记、裁定人、实验单位、依赖和区间／效应量方法 |

这些行只限定措辞，不晋级任何主张状态，也不建立第二套主张权威。
稿件 manifest 将参考文献键绑定到 source／evidence ID，并对证据台账机械校验。

## 状态转换

认证向：`Planned → Evidence Collected → In Review → Supported / Not Supported / Open`；研究向：`Planned → Reproduced → Evaluated → Held-Out / Calibrated / Replicated`。每次转换必须记录证据版本与门禁记录；否定和不完整结果不得通过事后改写主张删除。禁止从执行判定自动晋级到目标状态，或从目标状态自动晋级到合规状态。

## CR-2026-019 实施设计义务

本附件不提升主张状态。`CL-C1` 仍依赖有限域、所有权／配对、保守解释、R1--R5
与版本化全历史；不确定性身份漂移、把观测类当 H、排除有效真实假设、把证据不足
一律判 FAIL 均构成最小反例。`CL-C2` 把实现遵循规格与实测收益分开；预测 gap
计零、truth 泄漏、漏计成本、把 Prep／Recover 当 TEST 评分或全局最优措辞均不合格。
独立数学／科学评审仍开放；完整论证与走查位置见上述实施规格和有限 JSON 索引。
