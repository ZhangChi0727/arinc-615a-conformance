# Experiment Plan

| Field | Value |
|---|---|
| **Plan ID** | EXP-PLAN-2026-001 |
| **Version** | 2.0 |
| **Status** | Active CL-TAV protocol; confirmatory runs are not executed in this PR |
| **Governing method** | CL-TAV / CR-2026-012 / DD-029; RR-2026-001 successor text |

This is the **active** experiment protocol for the CL-TAV increment. Historical
EXP-001–007 under RR-2026-001 v4.2 remain a frozen registry; they are not the
current comparison design.

No confirmatory numbers are filled here. Formal sample size and effect
thresholds are frozen only after a declared pilot or external justification.
Passing unit tests does not show that CL-TAV outperforms any arm.

## Fair comparison arms

All arms use the same information pool, action pool, basic verdicts and declared
fault domain. Costs are charged as specified; Analysis-only is not forced to
invent a sampling cost it does not spend.

| Arm | Fair definition | Cost reporting |
|---|---|---|
| CL-T (Test-only) | Same test pool and fault domain; predetermined selection; no analysis feedback into the next test | acquisition budget only |
| CL-A (Analysis-only) | Same prior and pre-allowed input records; no hidden extra tests | prior-input and compute budgets only |
| CL-TA (fixed Test→Analysis) | Same total budget: collect first with a frozen policy, then analyse; selection does not close the loop | acquisition then compute, separately |
| CL-LOOP (CL-TAV) | Same information and action pool; analysis update chooses the next action; Prep / Recover / failed retry costs are charged | acquisition, compute, prep/recover, retries |

Direct numeric comparison is allowed only where the same denominator and the
same charged resource apply. Otherwise report the budgets side by side and say
which conclusions are comparable.

## Three experiment groups

Each group states hypothesis, experimental unit, normal and fault construction,
development/held-out isolation, pairing or randomization, reset, invalid or
equivalent-fault handling, stopping rule and metrics. INCONCLUSIVE and ERROR
are first-class outcomes, not silent misses.

### EXP-CLTAV-DETECT — detection and error judgement

- **Hypothesis:** Under the same detection budget, CL-LOOP does not increase
  missed detections relative to CL-T, and does not convert equality-timing
  uncertainty into PASS by rewriting source constants.
- **Unit:** one IUT session / one declared fault or normal instance.
- **Construction:** normal instances plus injected protocol faults that the
  declared domain can name; invalid and equivalent faults are classified and
  excluded from the detection denominator.
- **Isolation:** development instances never enter the confirmatory held-out
  set after any selector or oracle change.
- **Metrics:** miss rate, false alarm, INCONCLUSIVE, ERROR; denominators exclude
  abstentions from PASS/FAIL rates.
- **Timing:** FIND abort does not waive the 2 s host answer deadline or the 3 s
  registration window. Equality timing under nonzero measurement error may only
  return INCONCLUSIVE.

### EXP-CLTAV-LOCATE — finite-domain localization / candidate reduction

- **Hypothesis:** Under the same localization budget, CL-LOOP reduces the
  surviving candidate set more than CL-T or CL-TA without excluding the true
  in-domain fault when the compatibility update is applied.
- **Unit:** one diagnosis episode over the declared \(H_0=\{h_{\mathrm{normal}}\}\cup H_{\mathrm{single}}\).
- **Construction:** single-fault instances inside the declared domain; out-of-domain
  faults are reported separately and cannot refute in-domain localization.
- **Metrics:** true-fault exclusion rate, localization accuracy or surviving-set
  size, diagnostic rounds, resource consumed. A singleton normal hypothesis is
  not protocol PASS.
- **Stopping:** P1–P5 remain exclusive; `ERROR` spends the same resource.

### EXP-CLTAV-ABLATION — feedback, timing uncertainty and cost

- **Hypothesis:** Removing analysis feedback, ignoring Prep/Recover cost, or
  collapsing the two FIND clocks each changes detection or localization relative
  to the specified CL-LOOP.
- **Unit:** same as DETECT/LOCATE, with one factor disabled per cell.
- **Factors:** no feedback (CL-T or CL-TA); Prep/Recover uncharged; FIND abort
  treated as a clock waiver (negative control; the specified method forbids it).
- **Metrics:** same primary metrics as the parent group, plus charged cost and
  rounds.

## Registration, statistics and release

Create one directory per registered experiment:

```text
artifacts/experiments/EXP-YYYY-NNN/
  registration.yaml
  environment.json
  cases.json
  raw/
  derived/
  scripts/
  results.md
  deviations.md
  review/
```

Required registration fields remain: ID, owner, date, hypothesis, RQ/CL-RQ,
baseline/CRS/model/VCS/IUT/tool/environment versions, experimental and sampling
units, inclusion/exclusion, development/held-out split, primary outcomes,
stopping rationale, randomization/reset/isolation/seeds, time source and error
budget where timing is observed, planned statistical model, deviations and
gates.

Keep exploratory pilot analysis separate from pre-registered confirmation.
An experiment result may enter a thesis, paper, or release claim only when
registration and deviations are complete, provenance is reproducible, wording
matches the earned claim status, and negative or inconclusive results remain
visible.

## Historical v4.2 registry (not the active design)

EXP-001–007 (requirement-extraction reproducibility, B0–B3 coverage comparison,
finite-fault-domain adequacy, deterministic timed conformance, operational
repeatability, calibration/HMM, failure diagnosis) remain historical under
RR-2026-001 v4.2. They may be cited as prior protocol. They do not define the
CL-TAV arms or the three groups above. HMM/Bayesian calibration stays a
non-default comparison model.

---

# 中文版

本文件是 CL-TAV 增量的**活动**实验方案。RR-2026-001 v4.2 下的 EXP-001～007 只作为冻结登记保留，不再作为当前对照设计。本 PR 不填确认性数字；正式样本量与效应阈值须在声明的 pilot 或外部依据之后冻结。单元测试通过不表示 CL-TAV 优于任一对照臂。

## 公平对照臂

四臂共用同一信息池、动作池、基本判定与声明故障域。Analysis-only 不承担其未花费的采集成本。

| 对照臂 | 公平定义 | 成本报告 |
|---|---|---|
| CL-T（仅测试） | 同一测试池与故障域，预定选择，分析不反馈到下一测试 | 只报告采集预算 |
| CL-A（仅分析） | 同等先验与预先允许的输入记录，不靠隐藏额外测试获信息 | 只报告先验输入与计算预算 |
| CL-TA（固定先测后析） | 同一总预算下先按冻结策略采集再分析，选择不闭环 | 采集与计算分开报告 |
| CL-LOOP（CL-TAV） | 同一信息与动作池，分析更新后选择下一动作，计入 Prep／Recover／失败重试 | 采集、计算、准备／恢复、重试 |

仅在同一分母且同一计费资源下做直接数值比较；否则并列报告预算并说明哪些结论可公平比较。

## 三组实验

### EXP-CLTAV-DETECT——检测与错误判定

假设：同一检测预算下，CL-LOOP 相对 CL-T 不增加漏检，且不以改写来源常数把等式时序不确定性变成 PASS。单位为一会话／一声明故障或正常实例。指标含漏检、误报、INCONCLUSIVE、ERROR；拒答不进入 PASS／FAIL 分母。FIND 中止不豁免 2 秒主机期限与 3 秒登记窗口。

### EXP-CLTAV-LOCATE——有限域定位／候选缩减

假设：同一定位预算下，CL-LOOP 比 CL-T 或 CL-TA 更能缩小幸存候选集，且在相容更新下不误排除域内真故障。域为 \(H_0=\{h_{\mathrm{normal}}\}\cup H_{\mathrm{single}}\)。正常单候选不是协议 PASS。停止条件 P1～P5 互斥；`ERROR` 消耗同一资源。

### EXP-CLTAV-ABLATION——反馈、时序不确定性与成本

假设：去掉分析反馈、不计 Prep／Recover 成本、或把 FIND 中止当作时钟豁免，都会相对既定 CL-LOOP 改变检测或定位。后一因素是反例对照，规格禁止该豁免。

## 登记、统计与发布

每项实验一个目录：

```text
artifacts/experiments/EXP-YYYY-NNN/
  registration.yaml
  environment.json
  cases.json
  raw/
  derived/
  scripts/
  results.md
  deviations.md
  review/
```

确认实验前登记。探索性 pilot 与预注册确认实验分开。结果进入论文或发布主张前，登记／偏差、溯源、措辞与否定／不确定结果均须可见。

## 历史 v4.2 登记（非活动设计）

EXP-001～007 仍按 RR-2026-001 v4.2 保留为历史方案，可被引用，但不定义上述四臂与三组。HMM／贝叶斯校准保持非默认比较模型。
