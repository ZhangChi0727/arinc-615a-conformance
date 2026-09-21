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
  can support FAIL. Do not rewrite the specified 2 s / 3 s clocks. Exact-value checks of AFDX technological latency or max_jitter algebra are source-algebra contracts, not deployed measurement PASS. Deployed verdicts use this T5 interval treatment and a Configuration error budget; for example an observation interval [149,151] us against a strict open RX bound of 150 us is INCONCLUSIVE, not a point-estimate PASS. This PR does not activate a Configuration.
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

## Algorithm interface contracts

The experiment reuses the same session identity and the same abstract interfaces as ALG-CLTAV-01 / method §3.9.2. Implementation may remain pending; missing failure semantics is not allowed.

| Interface | Experiment use | Must not |
|---|---|---|
| IF-PRED-OBS | Current observable summary seen by every arm | Evaluator truth as a prediction input |
| IF-HIST-UPDATE | Compatibility update on answered valid classes | Exclude on ERROR or unknown effect |
| IF-OBS-INTERPRET | Map the recorded observation to a class | Invent a class from the hidden fault label |
| IF-SELECT-ADMIT | Form \(A\) then \(S\); empty \(S\) is Admit A2–A5 | Treat nonempty \(A\) as executable |
| IF-EXECUTE-RECORD | Charge once and record the issued action | Gift later CL-LOOP records to CL-T/CL-A/CL-TA |
| IF-PREP-RECOVER | Same resource rule as TEST | Confirm a Recover that was only sent |
| IF-EQUIV | Observational-equivalence stop | Use evaluator labels as equivalence evidence |
| IF-RESOURCE-STOP | Exclusive P1–P5 / resource stops | Hide Prep/Recover/retry cost |

Evaluator-only truth never enters IF-SELECT-ADMIT, IF-PRED-OBS, IF-HIST-UPDATE or IF-EXECUTE-RECORD (FIG-CL-TAV-09).

## Experiment execution and truth contracts

Bounded experiment interfaces. Implementation may remain pending; missing failure or denominator semantics is not allowed. Run/scene/config identity is required on every record. Injection planned is not injection confirmed. A separate store is not, by itself, independent truth.

| ID | Inputs | Outputs | Failure / unconfirmed | Visibility | Resource / time basis |
|---|---|---|---|---|---|
| IF-EXP-SCENE | sceneId, configId, IUT, faultPlan, resourceMode | sceneRecord | missing identity is not runnable | evaluator-and-operator | declared mode only |
| IF-EXP-INJECT | sceneId, injectionPlan | injectionAttempt, injectionConfirmed, injectionUnconfirmed | planned ≠ confirmed; unconfirmed is not valid truth | evaluator-only confirmation | evaluator metadata |
| IF-EXP-TRUTH | sceneId, injectionConfirmed, independentGeneratorId | truthRecord, sharedComponentRisk | unconfirmed injection cannot default to valid truth | evaluator-only; never an algorithm input | not charged to arms |
| IF-EXP-COLLECT | sceneId, armId, algorithmVisibleRecord | observationLog, resourceLog | missing correlation id is invalid-observation | algorithm-visible only | same charged vector as ALG-CLTAV-01 |
| IF-EXP-RUN | sceneId, armId, SessionContext | runId, stopClass, traceRef | arm abort is ERROR, not PASS | algorithm-visible plus evaluator run id | one declared mode |
| IF-EXP-FILTER | runId, truthRecord, observationLog | validityClass, filterReason | unconfirmed, invalid, equivalent, or abstain are not detection PASS/FAIL | evaluator labels; not a select input | not a second charge |
| IF-EXP-EVAL | runId, validityClass, denominators | metricCells, attemptDenominator, answeredSubsetDenominator | missing denominator is not a result | evaluator-only metrics | report Prep/Recover/retry cost |

Denominators: attempt, answered-subset, abstain, invalid-observation, equivalent-fault, unconfirmed-injection.

Shared parsers, clocks or models used by both truth and the method must be named as common-error risk at registration. Numeric sample size, seeds and thresholds freeze at confirmatory registration; this PR does not choose them.

Record-flow walkthroughs (truth never enters IF-SELECT-ADMIT / IF-PRED-OBS / IF-HIST-UPDATE / IF-EXECUTE-RECORD):

| Walk | Path | Denominator |
|---|---|---|
| WF-NORMAL | IF-EXP-SCENE → IF-EXP-INJECT → IF-EXP-TRUTH → IF-EXP-RUN → IF-EXP-COLLECT → IF-EXP-FILTER → IF-EXP-EVAL | answered-subset |
| WF-UNCONFIRMED-INJECT | IF-EXP-SCENE → IF-EXP-INJECT → IF-EXP-FILTER → IF-EXP-EVAL | unconfirmed-injection |
| WF-INVALID-OBS | IF-EXP-RUN → IF-EXP-COLLECT → IF-EXP-FILTER → IF-EXP-EVAL | invalid-observation |
| WF-ABSTAIN | IF-EXP-RUN → IF-EXP-FILTER → IF-EXP-EVAL | abstain |
| WF-EQUIVALENT | IF-EXP-SCENE → IF-EXP-TRUTH → IF-EXP-FILTER → IF-EXP-EVAL | equivalent-fault |

## Truth independence and common-error risk

Injection plans and execution confirmation stay in the evaluator record. Arms see only algorithm-visible \(I_{z_k}\), \(q\) and charged cost. Shared clock, adapter or file-parse defects are common-error risks and must be named in registration; they do not become a secretly stronger oracle for CL-LOOP.

## Successor implementation dependencies

These items stay specified, not implemented. Stage names are development-readiness stages; they are not an automatic M3 start.

| Dependency | Owner role | Input | Next stage | Delivery | Close-out evidence | Blocks |
|---|---|---|---|---|---|---|
| Core estimators for IF-PRED-OBS / IF-OBS-INTERPRET | later authorized implementer | ALG-CLTAV-01 contracts; measurement-uncertainty declaration | development-ready spec → unit/integration | named estimator with incomputable/unknown returns | review that empty current prediction is a spec error, not score 0 | EXP-CLTAV-DETECT timing cells; IF-PRED-OBS |
| Compatibility update IF-HIST-UPDATE | later authorized implementer | Admit A1–A5, Update P1–P5 | implementation and walk-through | executable intersection that never excludes on ERROR | loop-spec regression plus independent math review | EXP-CLTAV-LOCATE; IF-HIST-UPDATE |
| Selection IF-SELECT-ADMIT | later authorized implementer | currently valid nonempty classes | implementation | one-step minimax on \(S\), never on empty \(A\) | negative tests for empty-\(S\) argmin | EXP-CLTAV-LOCATE / ABLATION |
| Independent truth recorder | later authorized evaluator | injection plan, execution confirmation | pre-experiment | evaluator store isolated from arm inputs | FIG-CL-TAV-09 leakage review | all three experiment groups |
| Resource / stop IF-RESOURCE-STOP and IF-EQUIV | later authorized implementer | one resource mode, exclusive stops | implementation | charged vector and Stop-645 as named remaining 645-dependent capability | no hidden sampling charge; Stop-645 ≠ file missing | EXP-CLTAV-ABLATION cost cells |
| Confirmatory parameters | experiment registrar | pilot or external justification | confirmatory registration | frozen sample size, pairing, effect thresholds | registration committed before runs | numeric Chapter 6 claims |

Parameters that affect fairness (budget projection, pairing, invalid/equivalent-fault rules, clock error budget) must be frozen before the confirmatory gate. They cannot be deferred as “choose later.”

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
- **时序：** FIND 中止不豁免 2 秒主机期限与 3 秒登记窗口。等式时序使用与 RR-2026-001（T5）相同的稳健判定：\(I_{\mathrm{obs}}\subseteq I_r\) 为 PASS；不相交 \(I_{\mathrm{obs}}\cap I_r=\varnothing\) 为 FAIL；相交但不包含为 INCONCLUSIVE。例如 \(I_r=[3,3]\) 且 \(I_{\mathrm{obs}}=[2.9,3.1]\) 为 INCONCLUSIVE；\(I_{\mathrm{obs}}=[3.9,4.1]\) 为 FAIL。非零宽度测量区间通常不能对点等式给出稳健 PASS，但仍可给出 FAIL。不改写既定 2 秒／3 秒时钟。AFDX 技术时延或 max_jitter 代数的精确值检查是源代数合同，不是部署测量 PASS。部署判定使用上述 T5 区间处理与 Configuration 误差预算；例如观测区间 [149,151] 微秒对照 150 微秒严格开上界是 INCONCLUSIVE，不是点估计 PASS。本 PR 不激活 Configuration。
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

## 算法接口契约

实验复用 ALG-CLTAV-01／方法报告 §3.9.2 的同一会话身份与抽象接口。实现可以待定，但不能缺少失败语义。

| 接口 | 实验用途 | 禁止 |
|---|---|---|
| IF-PRED-OBS | 各臂可见的当前可观察摘要 | 把评价器真值当作预测输入 |
| IF-HIST-UPDATE | 对已作答有效类做相容更新 | 因 ERROR 或未知效果排除候选 |
| IF-OBS-INTERPRET | 把记录观测映射为类 | 用隐藏故障标签编造类 |
| IF-SELECT-ADMIT | 先形成 \(A\) 再形成 \(S\)；空 \(S\) 走 Admit A2–A5 | 把非空 \(A\) 当成可执行 |
| IF-EXECUTE-RECORD | 一次计费并记录已发出动作 | 把后继 CL-LOOP 记录赠给 CL-T／CL-A／CL-TA |
| IF-PREP-RECOVER | 与 TEST 同一资源规则 | 把“已发送”当成 Recover 已确认 |
| IF-EQUIV | 观测等价停止 | 用评价器标签当等价证据 |
| IF-RESOURCE-STOP | 互斥 P1–P5／资源停止 | 隐藏 Prep／Recover／重试成本 |

评价器真值不得进入 IF-SELECT-ADMIT、IF-PRED-OBS、IF-HIST-UPDATE 或 IF-EXECUTE-RECORD（FIG-CL-TAV-09）。

## 实验执行与真值契约

有界实验接口。实现可以待定，但不能缺少失败或分母语义。每条记录都要有运行／场景／配置身份。注入计划不是注入确认。仅分库存储本身不是独立真值。

| ID | 输入 | 输出 | 失败／未确认 | 可见性 | 资源／时间基准 |
|---|---|---|---|---|---|
| IF-EXP-SCENE | sceneId、configId、IUT、faultPlan、resourceMode | sceneRecord | 缺少身份不可运行 | 评价器与操作者 | 只使用已声明模式 |
| IF-EXP-INJECT | sceneId、injectionPlan | injectionAttempt、injectionConfirmed、injectionUnconfirmed | 计划 ≠ 确认；未确认不是有效真值 | 仅评价器确认 | 评价器元数据 |
| IF-EXP-TRUTH | sceneId、injectionConfirmed、independentGeneratorId | truthRecord、sharedComponentRisk | 未确认注入不得默认为有效真值 | 仅评价器；永不作为算法输入 | 不对各臂计费 |
| IF-EXP-COLLECT | sceneId、armId、algorithmVisibleRecord | observationLog、resourceLog | 缺关联标识为 invalid-observation | 仅算法可见 | 与 ALG-CLTAV-01 同一计费向量 |
| IF-EXP-RUN | sceneId、armId、SessionContext | runId、stopClass、traceRef | 臂中止是 ERROR，不是 PASS | 算法可见加评价器 run id | 一种已声明模式 |
| IF-EXP-FILTER | runId、truthRecord、observationLog | validityClass、filterReason | 未确认、无效、等价或弃权不是检测 PASS／FAIL | 评价器标签；不是选择输入 | 不二次计费 |
| IF-EXP-EVAL | runId、validityClass、denominators | metricCells、attemptDenominator、answeredSubsetDenominator | 缺分母不是结果 | 仅评价器指标 | 报告 Prep／Recover／重试成本 |

分母：attempt、answered-subset、abstain、invalid-observation、equivalent-fault、unconfirmed-injection。

真值与方法共用的解析器、时钟或模型须在登记中具名为共同错误风险。样本量、种子与阈值在确认性登记时冻结；本 PR 不定这些数。

记录流走查（真值不进入 IF-SELECT-ADMIT／IF-PRED-OBS／IF-HIST-UPDATE／IF-EXECUTE-RECORD）：

| 走查 | 路径 | 分母 |
|---|---|---|
| WF-NORMAL | IF-EXP-SCENE → IF-EXP-INJECT → IF-EXP-TRUTH → IF-EXP-RUN → IF-EXP-COLLECT → IF-EXP-FILTER → IF-EXP-EVAL | answered-subset |
| WF-UNCONFIRMED-INJECT | IF-EXP-SCENE → IF-EXP-INJECT → IF-EXP-FILTER → IF-EXP-EVAL | unconfirmed-injection |
| WF-INVALID-OBS | IF-EXP-RUN → IF-EXP-COLLECT → IF-EXP-FILTER → IF-EXP-EVAL | invalid-observation |
| WF-ABSTAIN | IF-EXP-RUN → IF-EXP-FILTER → IF-EXP-EVAL | abstain |
| WF-EQUIVALENT | IF-EXP-SCENE → IF-EXP-TRUTH → IF-EXP-FILTER → IF-EXP-EVAL | equivalent-fault |

## 真值独立性与共同错误风险

注入计划与执行确认留在评价器记录。各臂只看见算法可见的 \(I_{z_k}\)、\(q\) 与已计费成本。共享时钟、适配器或文件解析缺陷是共同错误风险，须在登记中具名；不得变成 CL-LOOP 暗中更强的 oracle。

## 后继实施依赖

这些项保持已规格、未实现。阶段名是开发就绪阶段，不是自动启动 M3。

| 依赖 | 责任角色 | 输入 | 后继阶段 | 交付 | 关闭证据 | 阻塞 |
|---|---|---|---|---|---|---|
| IF-PRED-OBS／IF-OBS-INTERPRET 核心估计器 | 后继获授权实现者 | ALG-CLTAV-01 契约；测量不确定性声明 | 开发就绪规格 → 单元／集成 | 具名估计器，含不可计算／未知返回 | 审查空当前预测是规格错误而非 score 0 | EXP-CLTAV-DETECT 时序格；IF-PRED-OBS |
| 相容更新 IF-HIST-UPDATE | 后继获授权实现者 | Admit A1–A5、Update P1–P5 | 实现与走查 | 可执行交集，ERROR 不排除 | 闭环规格回归加独立数学审查 | EXP-CLTAV-LOCATE；IF-HIST-UPDATE |
| 选择 IF-SELECT-ADMIT | 后继获授权实现者 | 当前有效非空类 | 实现 | 对 \(S\) 做一步 minimax，不对空 \(A\) | 空 \(S\) 上 \(\arg\min\) 的负例 | EXP-CLTAV-LOCATE／ABLATION |
| 独立真值记录器 | 后继获授权评价者 | 注入计划、执行确认 | 预实验 | 与臂输入隔离的评价器存储 | FIG-CL-TAV-09 泄漏审查 | 三组实验 |
| 资源／停止 IF-RESOURCE-STOP 与 IF-EQUIV | 后继获授权实现者 | 一种资源模式、互斥停止 | 实现 | 计费向量；Stop-645 为具名剩余 645 依赖能力 | 无隐藏采集费；Stop-645 ≠ 文件缺失 | EXP-CLTAV-ABLATION 成本格 |
| 确认性参数 | 实验登记人 | pilot 或外部依据 | 确认性登记 | 冻结样本量、配对、效应阈值 | 运行前已提交登记 | 第 6 章数字主张 |

影响公平性的参数（预算投影、配对、无效／等价故障规则、时钟误差预算）必须在确认性门前冻结，不能写成“以后再选”。

## 历史 v4.2 登记（非活动设计）

EXP-001～007 仍按 RR-2026-001 v4.2 保留为历史方案，可被引用，但不定义上述四臂与三组。HMM／贝叶斯校准保持非默认比较模型。
