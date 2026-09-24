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
| CL-SPEC | First-version CL-TAV objects, update, one-step minimax, Prep/Recover/ERROR and exclusive stops are specified | method report §3.9–§3.9.1, DD-029, loop walk-throughs | Specified; author arguments present; independent math review open |
| CL-ARCH | Verification-session and protocol-operation machines join only by declared interfaces | SysML FIG-CL-TAV-01..08, DD-030 | Specified; notation views, not executable metamodel |
| CL-DETECT | Detection and error-judgement comparison of CL-T / CL-A / CL-TA / CL-LOOP | EXP-CLTAV-DETECT registration and later held-out runs | To be verified; no numbers in this PR |
| CL-LOCATE | In-domain localization / candidate reduction under the same budget | EXP-CLTAV-LOCATE | To be verified |
| CL-ABLATION | Feedback, FIND-clock non-waiver and Prep/Recover cost change outcomes | EXP-CLTAV-ABLATION, including the forbidden abort-waiver negative control | To be verified |
| CL-CRS | Expanded protocol CRS is reviewable for INFORMATION, UPLOAD, both DOWNLOAD modes, FIND, bounded 665/664/RFC support and 615A-triggered 645 semantic leaves | M1 package, source audit, bilingual review view | Specified as candidate; 645 SOURCE/SEMANTIC bound; capabilities NOT-ESTABLISHED; not independently approved |
| CL-ALG | Top-level CL-TAV process and abstract interfaces are specified | ALG-CLTAV-01, method §3.9.2, DD-033 | Specified; not implemented; independent math review open |

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

## Status transitions

Certification-oriented: `Planned → Evidence Collected → In Review → Supported / Not Supported / Open`.
Research: `Planned → Reproduced → Evaluated → Held-Out / Calibrated / Replicated`.

Every transition must name an artifact version and a gate record. `Not
Supported` and `Incomplete` are valid outcomes and must not be erased by editing
the claim after observing results. No automatic promotion from execution
verdict to objective status, or from objective status to compliance status, is
permitted.

---

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

## 状态转换

认证向：`Planned → Evidence Collected → In Review → Supported / Not Supported / Open`；研究向：`Planned → Reproduced → Evaluated → Held-Out / Calibrated / Replicated`。每次转换必须记录证据版本与门禁记录；否定和不完整结果不得通过事后改写主张删除。禁止从执行判定自动晋级到目标状态，或从目标状态自动晋级到合规状态。
