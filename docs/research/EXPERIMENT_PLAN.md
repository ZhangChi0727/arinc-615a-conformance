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
fault domain. Direct numeric comparison is allowed only where the same
denominator and the same charged resource apply. Otherwise report the budgets
side by side and say which conclusions are comparable.

#### Cost vector and resource projection

Charge a common cost vector \(c=(c_{\mathrm{acq}},c_{\mathrm{comp}},c_{\mathrm{prep}},c_{\mathrm{retry}})\).
Every executed action of the same type has the same price on every arm.
An action that is not executed is not charged. Comparison uses an explicit
resource projection of that vector (for example acquisition-only, or
acquisition+compute). Inventing a cost that the arm did not spend is forbidden.

| Arm | Fair definition | Projection of the common vector |
|---|---|---|
| CL-T (Test-only) | Same test pool and fault domain; predetermined selection; no analysis feedback into the next test | \(c_{\mathrm{acq}}\) for tests that actually run; prep/recover/retry only if those actions run |
| CL-A (Analysis-only) | Same prior and pre-allowed input records; no hidden extra tests | prior-input and \(c_{\mathrm{comp}}\) only; no invented sampling cost |
| CL-TA (fixed Test→Analysis) | Same total budget: collect first with a frozen policy, then analyse; selection does not close the loop | \(c_{\mathrm{acq}}\) then \(c_{\mathrm{comp}}\), reported separately |
| CL-LOOP (CL-TAV) | Same information and action pool; analysis update chooses the next action | \(c_{\mathrm{acq}}+c_{\mathrm{comp}}+c_{\mathrm{prep}}+c_{\mathrm{retry}}\) for actions that actually run |

#### Refusal, coverage and miss denominators

Report, for every arm:

- attempt coverage (all registered attempts);
- refusal / no-answer rate (abstentions among attempts);
- conditional error rate on the answered subset;
- miss rate on the detection denominator after invalid and equivalent faults are removed.

Abstentions are excluded from PASS/FAIL rates and must still appear as a
first-class refusal rate. A large refusal rate cannot be read as a better
conditional error rate. INCONCLUSIVE and ERROR stay visible. Unconcluded
attempts are counted in coverage and refusal, not converted into PASS or miss.

## Three experiment groups

Each group states hypothesis, experimental unit, normal and fault construction,
development/held-out isolation, pairing or randomization, reset, invalid or
equivalent-fault handling, stopping rule, metrics and the statistical
estimation target. No sample size or confirmatory number is filled here.

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
- **Pairing / reset:** pair arms on the same held-out instance where the
  instance permits it; otherwise randomize instance order. Reset the IUT and
  session budget between arms.
- **Metrics:** miss rate, false alarm, INCONCLUSIVE, ERROR, refusal rate,
  attempt coverage, and conditional error rate. Denominators exclude
  abstentions from PASS/FAIL rates but still report them.
- **Timing:** FIND abort does not waive the 2 s host answer deadline or the 3 s
  registration window. Equality timing uses the same robust oracle as
  RR-2026-001 (T5): \(I_{\mathrm{obs}}\subseteq I_r\) is PASS; disjoint
  \(I_{\mathrm{obs}}\cap I_r=\varnothing\) is FAIL; intersect-but-not-contained
  is INCONCLUSIVE. Example: \(I_r=[3,3]\) with \(I_{\mathrm{obs}}=[2.9,3.1]\)
  is INCONCLUSIVE; \(I_{\mathrm{obs}}=[3.9,4.1]\) is FAIL. A nonzero-width
  measurement interval usually cannot support PASS on a point equality, but it
  can support FAIL. Do not rewrite the specified 2 s / 3 s clocks.
- **Estimation target:** held-out miss rate and refusal rate with an interval
  after a declared pilot; not estimated in this PR.

### EXP-CLTAV-LOCATE — finite-domain localization / candidate reduction

- **Hypothesis:** Under the same localization budget, CL-LOOP reduces the
  surviving candidate set more than CL-T or CL-TA without excluding the true
  in-domain fault when the compatibility update is applied.
- **Unit:** one diagnosis episode over the declared \(H_0=\{h_{\mathrm{normal}}\}\cup H_{\mathrm{single}}\).
- **Construction:** single-fault instances inside the declared domain; out-of-domain
  faults are reported separately and cannot refute in-domain localization.
- **Pairing / reset:** same as DETECT; candidate set and budget reset between arms.
- **Metrics:** true-fault exclusion rate, localization accuracy or surviving-set
  size, diagnostic rounds, resource consumed, refusal rate. A singleton normal
  hypothesis is not protocol PASS.
- **Stopping:** P1–P5 remain exclusive; `ERROR` spends the same resource.
- **Estimation target:** held-out surviving-set size and true-fault exclusion
  rate; not estimated in this PR.

### EXP-CLTAV-ABLATION — feedback, timing uncertainty and cost

- **Hypothesis:** Removing analysis feedback, ignoring Prep/Recover cost, or
  replacing robust interval judgement with a point timestamp each changes
  detection or localization relative to the specified CL-LOOP. Treating FIND
  abort as a clock waiver is a separate negative control that the specified
  method forbids.
- **Unit:** same as DETECT/LOCATE, with one factor disabled per cell.
- **Factors:**
  1. no feedback (CL-T or CL-TA);
  2. Prep/Recover uncharged;
  3. timing-uncertainty ablation: keep the specified FIND 2 s / 3 s clocks
     unchanged; compare robust interval judgement with \(\varepsilon\) against
     a point-timestamp verdict on the same traces;
  4. FIND abort treated as a clock waiver (negative control; forbidden).
- **Metrics:** same primary metrics as the parent group, plus charged cost,
  rounds, refusal rate and the timing-uncertainty disagreement count.
- **Estimation target:** ablation contrast on the same held-out set; not
  estimated in this PR.

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

四臂共用同一信息池、动作池、基本判定与声明故障域。仅在同一分母且同一计费资源下做直接数值比较；否则并列报告预算并说明哪些结论可公平比较。

#### 成本向量与资源投影

计费使用通用成本向量 \(c=(c_{\mathrm{acq}},c_{\mathrm{comp}},c_{\mathrm{prep}},c_{\mathrm{retry}})\)。
各臂对同一实际动作同价；未执行的动作不虚构收费。比较使用该向量的显式资源投影（例如只计采集，或采集加计算）。禁止为未花费的动作编造成本。

| 对照臂 | 公平定义 | 通用向量的投影 |
|---|---|---|
| CL-T（仅测试） | 同一测试池与故障域，预定选择，分析不反馈到下一测试 | 实际运行测试计 \(c_{\mathrm{acq}}\)；仅当确实执行时才计准备／恢复／重试 |
| CL-A（仅分析） | 同等先验与预先允许的输入记录，不靠隐藏额外测试获信息 | 只计先验输入与 \(c_{\mathrm{comp}}\)；不编造采集成本 |
| CL-TA（固定先测后析） | 同一总预算下先按冻结策略采集再分析，选择不闭环 | \(c_{\mathrm{acq}}\) 与 \(c_{\mathrm{comp}}\) 分开报告 |
| CL-LOOP（CL-TAV） | 同一信息与动作池，分析更新后选择下一动作 | 对实际执行的动作计 \(c_{\mathrm{acq}}+c_{\mathrm{comp}}+c_{\mathrm{prep}}+c_{\mathrm{retry}}\) |

#### 拒答、覆盖与漏检分母

每一对照臂都报告：全登记尝试覆盖；拒答／无答案率（尝试中的弃权）；已作答子集上的条件错误率；剔除无效与等价故障后的检测分母上的漏检率。拒答不进入 PASS／FAIL 分母，但仍作为一等拒答率报告。大量拒答不得被读成更优的条件错误率。INCONCLUSIVE 与 ERROR 保持可见。未作结论的尝试计入覆盖与拒答，不改写成 PASS 或漏检。

## 三组实验

每组写明假设、实验单位、正常与故障构造、开发／留出隔离、配对或随机、重置、无效或等价故障处理、停止规则、指标与统计估计目标。此处不填样本量或确认性数字。

### EXP-CLTAV-DETECT——检测与错误判定

- **假设：** 同一检测预算下，CL-LOOP 相对 CL-T 不增加漏检，且不以改写来源常数把等式时序不确定性变成 PASS。
- **单位：** 一会话／一声明故障或正常实例。
- **构造：** 正常实例加上声明域可命名的注入协议故障；无效与等价故障分类后排除出检测分母。
- **隔离：** 选择器或判定器变更后，开发实例永不进入确认性留出集。
- **配对／重置：** 实例允许时在同一留出实例上配对各臂；否则随机化实例顺序。臂间重置 IUT 与会话预算。
- **指标：** 漏检、误报、INCONCLUSIVE、ERROR、拒答率、尝试覆盖与条件错误率。拒答不进入 PASS／FAIL 分母，但仍报告。
- **时序：** FIND 中止不豁免 2 秒主机期限与 3 秒登记窗口。等式时序使用与 RR-2026-001（T5）相同的稳健判定：\(I_{\mathrm{obs}}\subseteq I_r\) 为 PASS；不相交 \(I_{\mathrm{obs}}\cap I_r=\varnothing\) 为 FAIL；相交但不包含为 INCONCLUSIVE。例如 \(I_r=[3,3]\) 且 \(I_{\mathrm{obs}}=[2.9,3.1]\) 为 INCONCLUSIVE；\(I_{\mathrm{obs}}=[3.9,4.1]\) 为 FAIL。非零宽度测量区间通常不能对点等式给出稳健 PASS，但仍可给出 FAIL。不改写既定 2 秒／3 秒时钟。
- **估计目标：** 声明 pilot 之后的留出漏检率与拒答率区间；本 PR 不估计。

### EXP-CLTAV-LOCATE——有限域定位／候选缩减

- **假设：** 同一定位预算下，CL-LOOP 比 CL-T 或 CL-TA 更能缩小幸存候选集，且在相容更新下不误排除域内真故障。
- **单位：** 声明域 \(H_0=\{h_{\mathrm{normal}}\}\cup H_{\mathrm{single}}\) 上的一次诊断情节。
- **构造：** 域内单故障实例；域外故障另行报告，不能反驳域内定位。
- **配对／重置：** 与 DETECT 相同；臂间重置候选集与预算。
- **指标：** 真故障排除率、定位准确率或幸存集大小、诊断轮次、资源消耗、拒答率。正常单候选不是协议 PASS。
- **停止：** P1～P5 互斥；`ERROR` 消耗同一资源。
- **估计目标：** 留出幸存集大小与真故障排除率；本 PR 不估计。

### EXP-CLTAV-ABLATION——反馈、时序不确定性与成本

- **假设：** 去掉分析反馈、不计 Prep／Recover 成本、或用点时间判定替换稳健区间判定，都会相对既定 CL-LOOP 改变检测或定位。把 FIND 中止当作时钟豁免是另一项反例对照，规格禁止该豁免。
- **单位：** 与 DETECT／LOCATE 相同，每格只关闭一个因素。
- **因素：**
  1. 无反馈（CL-T 或 CL-TA）；
  2. 不计 Prep／Recover；
  3. 时序不确定性消融：保持既定 FIND 2 秒／3 秒时钟不变，在同一轨迹上比较带 \(\varepsilon\) 的稳健区间判定与点时间判定；
  4. 把 FIND 中止当作时钟豁免（反例对照；禁止）。
- **指标：** 与父组相同的主指标，外加计费成本、轮次、拒答率及时序不确定性分歧计数。
- **估计目标：** 同一留出集上的消融对照；本 PR 不估计。

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

必需登记字段仍为：ID、责任人、日期、假设、RQ／CL-RQ、基线／CRS／模型／VCS／IUT／工具／环境版本、实验与抽样单位、纳入／排除、开发／留出划分、主结局、停止理由、随机化／重置／隔离／种子、时序观测时的时间源与误差预算、计划统计模型、偏差与门禁。

## 历史 v4.2 登记（非活动设计）

EXP-001～007 仍按 RR-2026-001 v4.2 保留为历史方案，可被引用，但不定义上述四臂与三组。HMM／贝叶斯校准保持非默认比较模型。
