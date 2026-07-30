# Claim–Evidence Matrix

This matrix controls what may be stated in reports, releases, and thesis text.
Status is earned by evidence; implementation progress alone cannot promote it.

| Claim ID | Permitted claim | Required evidence | Gate | Initial status |
|---|---|---|---|---|
| C-T0 | Every applicable obligation is linked to reviewed executable cases | Controlled CRS, \(\rho_{RT}\), \(\rho_{TV}\), obligation matrix | RG1–RG3, G1 | Planned |
| C-T1 | The IUT exhibited accepted behavior for named valid executions | T0 plus raw traces, configuration, oracle records, verdicts | RG4–RG5, G2 | Planned |
| C-TIME | The IUT satisfied named timing obligations for specified executions under the declared measurement-error budget | Approved timing catalog, clock-augmented model, raw timestamps, clock/error metadata, robust verdict reproduction | RG2–RG5, G1–G2 | Planned |
| C-T2 | The VCS detected all claimed members of the named evaluated fault set | T1 plus mutant catalog, equivalence decisions, held-out results | G3 | Planned |
| C-T3 | Evidence updates belief in named conformance propositions under a calibrated model | T2 plus independent calibration, prior and dependence sensitivity | G4–G5 | Optional |
| C-DIAG | The diagnostic model localizes declared fault classes at reported performance | Held-out fault instances, baselines, calibration/abstention results | G6 | Optional |
| C-XFER | Specified method elements transfer beyond ARINC 615A | Completed second-protocol instance | G7 | Future |
| C-ENG | The verification pipeline is reproducible for a named release | CI, manifests, checksums, runbook, reproducibility record | RG4–RG5 | Planned |

## Wording rules

Use:

- “traceability-complete for CRS version …”;
- “PASS was observed under configuration …”;
- “the observation interval was contained in the requirement interval under
  error budget …”;
- “detected \(k/n\) evaluated valid non-equivalent mutants”;
- “posterior under the stated prior and calibrated observation model …”.

Avoid:

- “the finite suite proves all protocol behavior”;
- “100% coverage proves conformance”;
- “mutation score is diagnostic coverage” without a population argument;
- “PASS frequency is the probability the IUT conforms”;
- “the measured point timestamp exactly satisfies the bound” when nonzero
  measurement uncertainty applies;
- “protocol-independent” before C-XFER is supported.

## Status transitions

`Planned → Evidence Collected → In Review → Supported/Not Supported/Incomplete`

Every transition must name an artifact version and gate record. `Not Supported`
and `Incomplete` are valid research outcomes and must not be erased by editing
the claim after observing results.

---

## 中文版

本矩阵控制报告、发布和论文允许使用的主张。C-T0 要求全部适用义务追踪到已评审可执行用例；C-T1 只说明命名有效执行中观测到可接受行为；C-TIME 只说明在声明误差预算下，观测区间满足命名时序义务；C-T2 限于声明评价故障集；C-T3 依赖独立校准、先验和依赖敏感性；诊断、迁移和工程复现各有独立证据与门禁。

时序允许措辞为“在误差预算……下，观测区间包含于需求区间……”。存在非零测量不确定性时，不得说“测得点时间精确满足边界”。状态只能按 `Planned → Evidence Collected → In Review → Supported/Not Supported/Incomplete` 转移；否定和不完整结果不得通过事后改写主张删除。
