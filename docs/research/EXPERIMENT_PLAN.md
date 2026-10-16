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

## Controlled experiment interface contract

The seven interfaces `IF-EXP-SCENE`, `IF-EXP-INJECT`, `IF-EXP-TRUTH`,
`IF-EXP-COLLECT`, `IF-EXP-RUN`, `IF-EXP-FILTER`, and `IF-EXP-EVAL` are bound
in `configs/engineering/cltav_development_contracts.json` to exact registry
inputs/outputs, ownership, failure, resource, acceptance and successor
implementation locations. Historical captures are exploratory offline inputs,
not runnable scenes or independent truth. No interactive IUT, confirmed
injection, qualified reset/clock chain or confirmatory execution is claimed.

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

Keep one all-attempt ledger for every arm. It retains confirmed runs and the
named unconfirmed-injection, invalid-observation, equivalent-fault,
undecided-fault, abstain, INCONCLUSIVE, ERROR and unconcluded flows; these names
need not be treated as a single mutually exclusive taxonomy when the registered
workflow permits layered labels.

Report separately:

- attempt coverage and each named flow on all registered attempts;
- refusal / no-answer among attempts;
- detection PASS/FAIL conditional error on the valid detection answered subset;
- miss rate on the registered detection denominator after declared exclusions;
- localization decision coverage on confirmed in-domain injections;
- true-fault retention/exclusion, singleton correctness and final candidate-set
  size on the registered localization subset.

A valid detection FAIL with (H=\{h_1,h_2\}) is an answered detection outcome,
not completed singleton localization. A singleton normal hypothesis is not
protocol PASS. Confirmed equivalents may be excluded from a mutation-score
denominator, but equivalent and undecided counts, the adjudicator and review
cost remain visible. A large refusal rate cannot be read as a better conditional
error rate.

#### Literature-comparator disposition

No cited method is added as a fifth arm in this increment. Köhl--Hermanns and
Fränzle et al. are C1 concept comparators because the task, active policy and
observation premises differ. Hu et al. and Miao et al. are C2 concept comparators
because controllable-event authority, objectives, observables, lifecycle and
cost projections differ. F-LAS, IMA and cockpit-display studies are scenario or
evaluation context. A direct implementation arm requires a later decision that
freezes a faithful task mapping, information and action pools, stops, budget and
observable outputs.

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

#### Decisions that must be frozen before confirmatory registration

The registration must name the experimental and sampling units, fault-domain
construction, injection-confirmation method, equivalence/undecided adjudicator
and review procedure, reset and pairing/randomization rule, time source and
clock-error calibration, oracle independence/shared components, budget
projection, stopping rule, primary denominators, and interval/effect-size method.
If any stage is stochastic, it must also freeze seeds or seed generation and
independent repetition. Literature workload, precision or equivalent-mutant
percentages are not sample-size inputs. This list refines the existing
registration authority; it does not create a second experiment plan.

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
| IF-EXP-FILTER | run-completed: runId, truthRecord, observationLog; pre-run-exclusion: sceneId, attemptId, injectionUnconfirmed; pre-run-equivalent: sceneId, attemptId, truthRecord | validityClass, filterReason | unconfirmed, invalid, equivalent, or abstain are not detection PASS/FAIL | evaluator labels; not a select input | not a second charge |
| IF-EXP-EVAL | run-completed: runId, validityClass, denominators, truthRecord, algorithmResultRef, chargedCost; pre-run-exclusion: sceneId, attemptId, validityClass, denominators. Evaluator store keyed by runId/sceneId/attemptId; missing ref is EVAL failure | metricCells, attemptDenominator, answeredSubsetDenominator | missing denominator or missing declared record/ref is not a result | evaluator-only metrics | report Prep/Recover/retry cost |

Denominators: attempt, answered-subset, abstain, invalid-observation, equivalent-fault, unconfirmed-injection.

Shared parsers, clocks or models used by both truth and the method must be named as common-error risk at registration. Numeric sample size, seeds and thresholds freeze at confirmatory registration; this PR does not choose them.

Record-flow walkthroughs (truth never enters IF-SELECT-ADMIT / IF-PRED-OBS / IF-HIST-UPDATE / IF-EXECUTE-RECORD). Each walk is a synthetic record instance in `cltav_interface_registry.json`; they do not report performance.

| Walk | Path | Filter / eval variant | Denominators | Records produced |
|---|---|---|---|---|
| WF-NORMAL | IF-EXP-SCENE → IF-EXP-INJECT → IF-EXP-TRUTH → IF-EXP-RUN → IF-EXP-COLLECT → IF-EXP-FILTER → IF-EXP-EVAL | run-completed / run-completed | attempt, answered-subset | S-N1 / A-N1 / R-N1; confirmed injection; valid observation |
| WF-UNCONFIRMED-INJECT | IF-EXP-SCENE → IF-EXP-INJECT → IF-EXP-FILTER → IF-EXP-EVAL | pre-run-exclusion / pre-run-exclusion | attempt, unconfirmed-injection | S-U1 / A-U1; injectionUnconfirmed; no runId |
| WF-INVALID-OBS | IF-EXP-SCENE → IF-EXP-INJECT → IF-EXP-TRUTH → IF-EXP-RUN → IF-EXP-COLLECT → IF-EXP-FILTER → IF-EXP-EVAL | run-completed / run-completed | attempt, invalid-observation | R-I1 missing correlation id |
| WF-ABSTAIN | IF-EXP-SCENE → IF-EXP-INJECT → IF-EXP-TRUTH → IF-EXP-RUN → IF-EXP-COLLECT → IF-EXP-FILTER → IF-EXP-EVAL | run-completed / run-completed | attempt, abstain | R-A1 Stop-645 abstain with charged cost |
| WF-EQUIVALENT | IF-EXP-SCENE → IF-EXP-INJECT → IF-EXP-TRUTH → IF-EXP-FILTER → IF-EXP-EVAL | pre-run-equivalent / pre-run-exclusion | attempt, equivalent-fault | confirmed injection; truth.equivalentFault; no run |

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

## CR-2026-019 implementation-design attachment

`EXPERIMENT_IMPLEMENTATION_SPEC.md` refines this plan without replacing it.
It reuses the three experiment families, four arms, eight scenario IDs, seven
experiment interfaces and fourteen acceptance-matrix classes. Its closed JSON
index v0.2 binds nine exact base-commit blobs by role, derives finite metric
populations from attempt fields, disposes every AM class, and maps any recovery
detail into the accepted four-component cost vector exactly once. It also
names missing/censoring rules, comparison families, analysis plans, dependency
fields, and separate sample/repeat, resource, and clock decisions. The
bilingual shared tables are generated from that index and checked for drift.
Algorithm arms receive only the proposed safe projection
`IF-EXP-SCENE.algorithmVisibleFields`, whose typed member allowlist is exactly
`sceneId`, `serviceScope`, `registeredArm`, `resourceMode`, and
`publicConfigurationRef`; fault plan, truth source, injection confirmation,
validity, equivalence, and post-hoc adjudication remain explicitly forbidden.
A pair is derived separately for each parent metric and requires reciprocal
registered arms on the same base scene, seed, construction, and registered
contrast with distinct confirmed resets. Loss of truth-scoring eligibility does
not erase a still-valid cost pair.
Pre-run review/setup effort is audited separately from issued-action cost.
Design-check success is not
confirmatory registration or run admission. Interactive IUT/reset evidence,
truth and injection confirmation, equivalent-fault adjudication, independent
mathematical review, justified sample/repeat policy, resource budget, and clock
error budget remain named blockers. A zero answered count is reported as
coverage `0/N`, while answered-conditional error is `N/A`; missing truth remains
in coverage and an explicit truth-missing flow but leaves only truth-scored
denominators. A scenario-independent interpretation/update relation distinguishes
accepted current interpretations, rejected current steps, and no-current-update
exits. Rejected steps preserve the preceding `H` and spent cost and issue no
current localization decision; valid empty and singleton updates still force
`Stop-Empty` and `Stop-Singleton` before later stops. Every metric input is also
bound to a record/interface field, producer role, dependency and closure milestone;
truth confirmation remains an evaluator-only pilot prerequisite. The bounded statistical routine derives a
complete-census, independent, paired, clustered, or wait branch from explicit
randomization, dependence, evidence, and independent-unit inputs. Only the
independent Bernoulli branch currently names Clopper--Pearson; paired and
clustered inference remain `WAIT-DEC-SAMPLE` until a direct method is frozen.
For CRS-M1-00101, the scored trigger is the data loader receiving a status file
that carries an exception delay for the active operation.  A new status strictly
before the unresolved expiry endpoint or an observed required abort fallback
after expiry passes only the observed fallback-action proposition. Equality stays
unscored until DEC-CLOCK freezes endpoint inclusivity. This candidate admits no
abort-completion constant: the field remains null, arbitrary numeric bounds are
rejected, and finite absence of both events remains `NOT-SCORED`. Generic request suppression is
method-only and is not scored against that requirement.
Exactly one `BUDGET` or `ROUNDS` resource mode is selected per session; a retry
cap is a separate execution-safety bound, not a second resource stop mode.
Historical captures stay exploratory and synthetic fixtures are not results.

# 中文版

本文件是 CL-TAV 增量的**活动**实验方案。RR-2026-001 v4.2 下的 EXP-001～007 只作为冻结登记保留，不再作为当前对照设计。本 PR 不填确认性数字；正式样本量与效应阈值须在声明的 pilot 或外部依据之后冻结。单元测试通过不表示 CL-TAV 优于任一对照臂。

## 受控实验接口合同

七个接口 `IF-EXP-SCENE`、`IF-EXP-INJECT`、`IF-EXP-TRUTH`、
`IF-EXP-COLLECT`、`IF-EXP-RUN`、`IF-EXP-FILTER` 和 `IF-EXP-EVAL`
在 `configs/engineering/cltav_development_contracts.json` 中绑定到注册表的
精确输入／输出、所有权、失败、资源、验收和后继实现位置。历史捕获仅是
探索性离线输入，不是可运行场景或独立真值。本增量不声称已有交互 IUT、
已确认注入、合格复位／时钟链或确认性执行。

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

每一对照臂保留同一份全部尝试总账。已确认运行以及具名的未确认注入、无效观测、等价故障、未决故障、弃权、INCONCLUSIVE、ERROR 和未结束流均保留；若登记工作流允许分层标签，不强称这些名称构成单一互斥穷尽分类。

分开报告：全部登记尝试上的覆盖与各具名流；尝试中的拒答／无答案；检测有效回答子集上的 PASS／FAIL 条件错误；按登记排除后的检测分母漏检率；已确认域内注入上的定位决策覆盖；以及登记定位子集上的真故障保留／排除、单例正确性和最终候选集大小。有效检测 FAIL 且 (H=\{h_1,h_2\}) 是已回答检测结果，不是完成单例定位；正常单例不是协议 PASS。已确认等价体可从变异分数分母排除，但等价／未决计数、裁定人和评审成本保持可见。大量拒答不得被读成更优的条件错误率。

#### 文献比较器处置

本增量不把任何被引方法新增为第五实验臂。Köhl--Hermanns 与 Fränzle 等因任务、主动策略和观测前提不同，只作 C1 概念比较；Hu 等与 Miao 等因可控事件权限、目标、可观测、生命周期和成本投影不同，只作 C2 概念比较；F-LAS、IMA 与座舱显示研究只作场景或评价语境。建立直接实现臂须由后继决定冻结忠实任务映射、信息／动作池、停止、预算和可观测输出。

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

#### 确认性登记前必须冻结的决定

登记须具名：实验单位与抽样单位、故障域构造、注入确认方法、等价／未决裁定人与评审过程、复位与配对／随机规则、时间源与钟差校准、oracle 独立性／共享组件、预算投影、停止规则、主分母及区间／效应量方法。若任一阶段具有随机性，还须冻结种子或种子生成和独立重复。文献中的工作量、precision 或等价变异比例不得作为样本量输入。本清单细化既有登记权威，不建立第二份实验方案。

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
| IF-EXP-FILTER | 已运行：runId、truthRecord、observationLog；运行前排除：sceneId、attemptId、injectionUnconfirmed；运行前等价：sceneId、attemptId、truthRecord | validityClass、filterReason | 未确认、无效、等价或弃权不是检测 PASS／FAIL | 评价器标签；不是选择输入 | 不二次计费 |
| IF-EXP-EVAL | 已运行：runId、validityClass、denominators、truthRecord、algorithmResultRef、chargedCost；运行前排除：sceneId、attemptId、validityClass、denominators。评价器库以 runId／sceneId／attemptId 为键；缺引用是 EVAL 失败 | metricCells、attemptDenominator、answeredSubsetDenominator | 缺分母或缺声明记录／引用不是结果 | 仅评价器指标 | 报告 Prep／Recover／重试成本 |

分母：attempt、answered-subset、abstain、invalid-observation、equivalent-fault、unconfirmed-injection。

真值与方法共用的解析器、时钟或模型须在登记中具名为共同错误风险。样本量、种子与阈值在确认性登记时冻结；本 PR 不定这些数。

记录流走查（真值不进入 IF-SELECT-ADMIT／IF-PRED-OBS／IF-HIST-UPDATE／IF-EXECUTE-RECORD）。每条走查是 `cltav_interface_registry.json` 中的合成记录实例，不报告性能。

| 走查 | 路径 | 过滤／评价变体 | 分母 | 记录 |
|---|---|---|---|---|
| WF-NORMAL | IF-EXP-SCENE → IF-EXP-INJECT → IF-EXP-TRUTH → IF-EXP-RUN → IF-EXP-COLLECT → IF-EXP-FILTER → IF-EXP-EVAL | 已运行／已运行 | attempt、answered-subset | S-N1／A-N1／R-N1；注入已确认；有效观测 |
| WF-UNCONFIRMED-INJECT | IF-EXP-SCENE → IF-EXP-INJECT → IF-EXP-FILTER → IF-EXP-EVAL | 运行前排除／运行前排除 | attempt、unconfirmed-injection | S-U1／A-U1；injectionUnconfirmed；无 runId |
| WF-INVALID-OBS | IF-EXP-SCENE → IF-EXP-INJECT → IF-EXP-TRUTH → IF-EXP-RUN → IF-EXP-COLLECT → IF-EXP-FILTER → IF-EXP-EVAL | 已运行／已运行 | attempt、invalid-observation | R-I1 缺关联标识 |
| WF-ABSTAIN | IF-EXP-SCENE → IF-EXP-INJECT → IF-EXP-TRUTH → IF-EXP-RUN → IF-EXP-COLLECT → IF-EXP-FILTER → IF-EXP-EVAL | 已运行／已运行 | attempt、abstain | R-A1 Stop-645 弃权并带计费成本 |
| WF-EQUIVALENT | IF-EXP-SCENE → IF-EXP-INJECT → IF-EXP-TRUTH → IF-EXP-FILTER → IF-EXP-EVAL | 运行前等价／运行前排除 | attempt、equivalent-fault | 注入已确认；truth.equivalentFault；无运行 |

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

## CR-2026-019 实施设计附件

`EXPERIMENT_IMPLEMENTATION_SPEC.md` 是本计划的下属细化，不取代本计划。它
复用三实验族、四臂、八场景、七实验接口和十四类 AM。v0.2 封闭 JSON 按角色绑定
九个基线 Git blob，由尝试字段推导有限总体，逐项处置全部 AM，并把 recovery 明细
恰好一次并入接受的四维成本向量；同时规定缺失／删失、比较族、分析方案、依赖字段，
并把样本／重复、资源预算和时钟误差预算分开决策。双语共享表由该 JSON 生成并检查
漂移。设计检查通过不等于确认性登记或运行准入。交互 IUT／复位、真值与注入确认、
等价裁定、独立数学审查、有依据的样本／重复、资源和时钟决定继续阻塞运行。零回答
时回答覆盖率写作 `0/N`，以回答为条件的错误率写作 `N/A`；`ERROR` 或停止类不得虚构
回答或单点定位决定。算法可见投影固定为五个类型化初始成员，并显式禁止真值、注入、
有效性、等价性和事后裁定字段。配对按父指标分别从场景、种子、构造、注册对比和互异
确认复位证据推导。真值缺失保留在覆盖率与显式缺失流中，只退出真值计分分母。统一的
解释／更新关系区分已接受解释、被拒绝当前步骤和无当前更新；被拒绝步骤保留此前 `H`、
历史及已花成本，不产生当前定位决定。有效空集与单例仍分别优先触发 `Stop-Empty` 与
`Stop-Singleton`。每个指标输入均绑定记录／接口字段、生产者角色、依赖和闭合里程碑，
真值确认必须由独立评估者在试点前提供。统计分支由随机化、依赖、配对／聚类证据及独立单位推导；当前仅独立
伯努利分支列出 Clopper--Pearson，配对和聚类推断继续等待决定。CRS-M1-00101 的计分
触发是数据加载器收到携带异常延迟的当前操作状态文件；在 DEC-CLOCK 冻结端点前，
恰逢到期的事件保持不计分；到期后的规定中止是后备义务而非取消豁免，观察到该中止的
PASS 只覆盖后备动作命题。本候选不接纳中止完成常数，字段保持为空，任意注入数字均被
拒绝，因此有限缺失迹继续为 `NOT-SCORED`。通用请求抑制不按该条计分。
历史捕获只属探索，合成 fixture 不是结果。
