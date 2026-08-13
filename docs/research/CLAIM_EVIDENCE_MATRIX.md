# Claim–Evidence Matrix

This matrix controls what may be stated in reports, releases, and thesis text.
Status is earned by evidence; implementation progress alone cannot promote it.
Under `RB-2026-001-v4.3`, the historical `C-T0…C-T3` ladder is superseded by
domain-specific claims split into certification-oriented assurance,
engineering, and research categories. Historical T0–T3 labels are not silently
converted; they remain valid only under their historical baseline wording.

## Certification-oriented assurance claims

| Claim ID | Permitted claim | Required evidence | Assurance state |
|---|---|---|---|
| A-BASIS | A controlled normative, applicability, and configuration basis exists | controlled standard edition, applicability declaration, CRS identity/version, configuration authority | A0 |
| A-TRACE | Applicable requirements and obligations are traceable to reviewed verification objectives and activities | CRS, `rho_RA`, `rho_RO`, `rho_OM`, `rho_TV` matrices | A1 |
| A-EXEC | Named verification executions are valid and evidence-complete under controlled configuration | test article/setup/procedure conformity, execution validity, raw/derived provenance, evidence integrity | A2 |
| A-OBJ | Named verification objectives are satisfied by reviewed evidence | objective satisfaction records, required evidence classes, reviewed closure | A3 |
| A-COMP | Named protocol-level compliance claims are supported by a complete controlled evidence package | compliance evidence index, objective satisfaction records, limitations and non-claims | A4 |

`A4` does not depend on research maturity `R4` or `R5`.

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

本矩阵控制报告、发布和论文允许使用的主张。状态由证据获得，实现进度本身不能晋级。在 `RB-2026-001-v4.3` 下，历史 `C-T0…C-T3` 阶梯由按领域拆分的主张替代：面向认证保证、工程与研究。历史 T0–T3 标签不静默转换，仅在其历史基线措辞下有效。

## 面向认证保证主张

A-BASIS：受控的标准、适用性与配置基础存在；A-TRACE：适用需求与义务可追踪至已评审验证目标与活动；A-EXEC：命名验证执行在受控配置下有效且证据完整；A-OBJ：命名验证目标由受评审证据满足；A-COMP：命名协议级合规主张由完整受控证据包支持。`A4` 不依赖研究成熟度 `R4` 或 `R5`。

## 工程主张

E-TIME：在声明测量误差预算下，命名时序义务对指定执行得到满足；E-REPRO：命名证据包可由受控源、工具与环境配置复现。

## 研究主张

R-MUT：VCS 检测到声明评价的有效非等价变异体或故障集；R-HOLDOUT：留出故障检测性能已测量；R-CAL：证据解释在声明观测模型下已校准；R-DIAG：声明故障类在留出性能下定位；R-XFER：指定方法要素在第二协议实例上复现。研究成熟度不授予认证状态；未达 `R4`/`R5` 不阻塞 `A4`。

## 措辞规则

时序允许“在误差预算……下，观测区间包含于需求区间……”；目标可用“目标 OSR-… 经受评审证据满足……”；突变可用“检出 \(k/n\) 个评价有效非等价变异体”。不得说“有限套件证明全部协议行为”“100% 覆盖即符合”“突变分数即诊断覆盖”“PASS 频率即 IUT 符合概率”“测得点时间精确满足边界”，也不得暗示突变、贝叶斯校准、诊断或跨协议复现为面向认证保证所必需。

## 状态转换

认证向：`Planned → Evidence Collected → In Review → Supported / Not Supported / Open`；研究向：`Planned → Reproduced → Evaluated → Held-Out / Calibrated / Replicated`。每次转换必须记录证据版本与门禁记录；否定和不完整结果不得通过事后改写主张删除。禁止从执行判定自动晋级到目标状态，或从目标状态自动晋级到合规状态。