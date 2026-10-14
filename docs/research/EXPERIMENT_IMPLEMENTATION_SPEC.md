# CL-TAV Experiment Implementation Specification / CL-TAV 实验实施规格

**Identity:** `CLTAV-EXPERIMENT-DESIGN`, version `0.1-candidate`

**Parent authority:** `EXP-PLAN-2026-001`

**Machine index:** `configs/research/cltav_experiment_design.json`
**Status:** candidate design; **not** a registration, executable Configuration,
run approval, result, proof or scientific approval.

## 1. Authority and maturity / 权威与成熟度

The method report and ALG-CLTAV-01--07 define semantics; the interface registry
defines identifiers and record flow; development contracts define current
engineering fields; the experiment plan defines the three families and four
arms. This attachment specifies how those accepted objects would be evaluated.
It has three maturity classes: (1) existing semantic contract, (2) proposed
research implementation awaiting review, and (3) runtime value/decision that
must be frozen from evidence. Machine checks cover identity and accounting only.

方法报告与 ALG-CLTAV-01--07 定义语义，接口登记定义身份与记录流，开发合同定义
现有工程字段，实验计划定义三实验族与四臂。本附件只规定如何评价这些对象。成熟度
分为：已有语义合同、待审研究实施提案、须据证据冻结的运行值／决定。机器检查只
覆盖身份与记账。

## 2. Bounded C1/C2 argument / C1/C2 有界论证

| Claim | Bounded proposition and locator | Assumptions and author argument | Falsifier / independent obligation | Engineering evidence | Allowed / prohibited wording |
|---|---|---|---|---|---|
| CL-C1 | One uncertainty identity is used by prediction, frozen snapshot, interpretation and whole-history update; true-hypothesis retention is conditional. RR-2026-001 §3.9–3.9.1; ALG-CLTAV-06/07. | Finite declared domain, qualified ownership/pairing, conservative observation class, R1–R5 and versioned HistoryHandle. Intersection gives monotone H; R1–R5, not monotonicity alone, support retention. | Minimum counterexample: the same `uncertaintyRef` changes meaning, H is replaced by an observation class, a valid in-domain true hypothesis is excluded, or insufficient evidence becomes unconditional FAIL. Independent mathematical review remains open. | snapshot/history version, uncertainty reference, ownership and qualified evidence; complete history or declared sufficient summary. | “conditional consistency/retention in the declared model”; never universal soundness/completeness under arbitrary loss, drift, duplication or reordering. |
| CL-C2 | Eligible, feasible and affordable TEST actions are ranked by one-step worst residual cardinality, charged cost and stable ID; Prep/Recover use their existing coordination rules. RR-2026-001 §3.9–3.9.1; ALG-CLTAV-05. | Current finite nonempty H; valid prediction classes; exclusive BUDGET/ROUNDS; positive finite costs; retry cap. A is not S, a gap is not score zero, and partial distinction can exist when worst-case size does not shrink. | Minimum counterexample: truth/future evidence leaks into selection, unaffordable action is selected, cost is omitted, or Prep/Recover is scored as TEST. Separately test whether the compliant implementation yields benefit; conformance does not imply gain. | action eligibility, prediction status/classes, budget mode/balance, attempt and charged-cost records. | “one-step prior-free minimax implementation; empirical benefit to be estimated”; never first active loop, Bayesian optimum or global multi-step optimum. |

Raw events/timestamps, interpretation classes, H and compatible histories are
different objects. Equal H does not imply equal compatible histories. A
qualified expired no-response may be FAIL; missing qualification is not thereby
FAIL. Stop-Empty remains visible. An out-of-domain fault can still match an
in-domain survivor. Köhl–Hermanns is a strong passive-history neighbour, but
its exact-once, clock/A4 and bounded-history conclusions are not imported.

原始事件／时间戳、解释类、H 与相容历史是不同对象；H 相同不等于历史相同。证据
合格且义务到期的无响应可以为 FAIL，证据不足不能据此判 FAIL。Stop-Empty 保留。
域外故障仍可能与域内候选相容。Köhl–Hermanns 是强近邻，但其 exact-once、时钟／
A4 和有界历史结论不移植。

## 3. Scenario matrix / 场景矩阵

All rows reuse existing IDs and applicable AM references. “Fault” is typed as
protocol, configuration, observation or tool condition; a malformed tool record
does not prove IUT nonconformance.

| Scenario | Family; scope | Control, perturbation and observable | Truth/reset/admission | Arms; dependencies |
|---|---|---|---|---|
| SC-NORMAL-UPLOAD | DETECT, LOCATE; UPLOAD | qualified normal completion; normal singleton is not protocol PASS | controlled scene + terminal evidence; fresh session/IUT reset | all; AM-EXPERIMENT/STATE; IUT, reset, registration |
| SC-WAIT-CONTINUE | DETECT, ABLATION; UPLOAD | WAIT preserves obligation until continuation | confirmed event script; loader/session reset | all; AM-TIMING/STATE; IUT, clock, registration |
| SC-NO-RESPONSE | DETECT, LOCATE; INFORMATION | valid uncancelled expiry may FAIL; insufficient evidence stays non-FAIL | confirmed suppression + complete qualified horizon; endpoint/horizon reset | all; AM-OWNERSHIP/TIMING; IUT, clock, truth |
| SC-ABORT | DETECT, ABLATION; UPLOAD | owned obligation cancelled; unrelated clocks remain | independent controller log; transfer/session reset | all; AM-OWNERSHIP/TIMING; IUT, truth |
| SC-INVALID-OBS | DETECT, ABLATION; INFORMATION | observation anomaly → ERROR/qualification outcome, not IUT blame | evaluator construction only; fresh capture/session identity | all; AM-LABEL/TIMING/EXPERIMENT; clock, observation qualification |
| SC-SAME-KEY | LOCATE, ABLATION; INFORMATION | one owner or explicit ambiguity; no response reuse | independent request schedule; correlation reset | all; AM-OWNERSHIP/HISTORY; IUT, truth |
| SC-SINGLE-BATCH | LOCATE, ABLATION; UPLOAD | controlled configuration difference | paired scenes; full independent resetId | all; AM-EXPERIMENT/HISTORY; IUT, reset |
| SC-RESOURCE-ERROR | DETECT, LOCATE, ABLATION; UPLOAD | ERROR, Stop-Budget and Stop-645 retain spent cost | controlled capability/resource condition; resource reset | all; AM-RESOURCE/EXPERIMENT; capability, registration |

The design references every AM class: IDENTITY, LABEL, FORMAT, IP, TFTP,
FIELDS, OWNERSHIP, TIMING, ADMIT, HISTORY, STATE, RESOURCE, EXPERIMENT and
DRIFT. This is specification coverage, not achieved fault coverage. FIND 2 s/
3 s and abort-does-not-waive remain synthetic contract checks because active M2
does not execute FIND. DOWNLOAD, AFDX and 645 runtime integrity remain outside
first-run admission.

八场景和 14 类 AM 的逐项引用只表示规格覆盖，不表示已获得故障覆盖。FIND 的 2 s／
3 s 与 abort 不豁免仍是合成合同核对；当前 M2 不执行 FIND。DOWNLOAD、AFDX 与 645
运行完整性能力不进入首轮运行。

## 4. Units, split and reset / 单位、分割与复位

The experimental unit is one registered attempt on one base scene, arm and
fault/control construction. `attemptId` is the all-ledger de-duplication key;
a `runId` exists only after run admission. Packets, events, time points,
hypotheses and repeated fields are observations within an attempt, not
independent samples. The sampling unit is the independently constructed base
scene; repeated-measure and paired units share that base scene but require
separate reset evidence. Scenario, fault ID, generator template, seed, attempt
and run remain separate fields.

Development/debug, calibration/pilot and confirmatory holdout are disjoint by
base-scene/fault-template lineage, not merely filename. Pilot data may estimate
feasibility, variance and cost; after algorithm tuning it cannot become held-out
performance. Pair arms on the same base instance with independent reset; randomize
order only where order is genuinely stochastic. Historical captures remain an
offline exploratory branch with unknown truth and population frequency.

实验单位是一个基础场景、臂、故障／控制构造上的一次登记 attempt；`attemptId` 是
总账去重键，只有运行准入后才有 `runId`。packet、event、时间点、假设和重复字段都
不是独立样本。开发、pilot 与确认性留出按场景／故障模板谱系隔离。配对使用相同
基础实例但独立复位；历史捕获只属未知真值的离线探索。

## 5. Four-arm contract / 四臂合同

| Arm | Visible information and action | Feedback / exit | Cost and fair comparison |
|---|---|---|---|
| CL-T | frozen test pool; predetermined TEST and actually executed Prep/Recover | no adaptive feedback | acquisition, prep/recover/retry actually incurred; frozen policy needs reproducible rationale |
| CL-A | frozen prior records; analysis only | no future acquired record | computation only; no invented acquisition cost |
| CL-TA | records from a frozen collect policy, then analysis | no post-analysis selection | acquisition and computation separate; no hidden adaptive step |
| CL-LOOP | same initial pool plus records produced by its own prior actions | analysis-guided next TEST/Prep/Recover | all actually incurred components; same price vector for same action type |

The same initial pool does not give another arm CL-LOOP's future observations.
All arms retain ERROR, abstain, inconclusive and resource exits. External methods
remain conceptual comparators; no new direct baseline or fifth arm is authorized.

## 6. Truth and oracle boundary / 真值与 oracle 边界

IF-EXP-SCENE registers the control/fault construction; IF-EXP-INJECT records
planned versus confirmed injection; IF-EXP-TRUTH produces evaluator-only truth;
IF-EXP-COLLECT preserves causal records; IF-EXP-RUN executes an arm without
truth; IF-EXP-FILTER classifies validity/equivalence; IF-EXP-EVAL joins truth
only for scoring. Fault labels never enter IF-PRED-OBS, IF-SELECT-ADMIT,
IF-HIST-UPDATE or IF-EXECUTE-RECORD.

Four oracles remain distinct: protocol conformance, observation qualification,
injection confirmation and evaluation truth. Separate files alone do not make
them independent. Shared parsers, models, clocks or generators are declared as
common-error risks. Unconfirmed injections retain attempts without valid effect
scores. Equivalent faults require a named adjudication; unresolved cases stay
visible. Reset success requires an independently recorded reset identity.

四类 oracle——协议、观测资格、注入确认、评价真值——必须分开。另存文件不构成
独立；共享解析器、模型、时钟或生成器均须披露共同错误。未确认注入保留 attempt
但不产生有效效果成绩；等价需具名裁定，未决不能删除；复位需独立 reset 身份。

## 7. Metric dictionary and accounting / 指标与记账

The JSON index is the finite metric dictionary and field-link source. Primary
metrics cover all-attempt flow, answered coverage, detection miss/false-FAIL,
true-hypothesis retention and charged cost. Secondary metrics cover validity,
abstain/inconclusive/error/incomplete/budget exits, localization decision,
singleton correctness, final |H|, rounds and cost components. Every metric names
its target subset, numerator, denominator, unit, direction, missing rule,
zero-denominator `N/A`, censoring rule, fields and planned panel. Labels can
overlap; they are never summed as mutually exclusive unless the metric declares
a partition.

FAIL with non-singleton H answers detection but not singleton localization.
Normal singleton is not protocol PASS. Equivalent faults leave a visible ledger
and may leave a mutation denominator only after confirmed adjudication;
unresolved cases cannot disappear. Budget exhaustion is not success. Cost is
reported with success/coverage and censoring, never only among successful runs.

JSON 中的 12 个指标给出总体／子集、分子、分母、单位、方向、缺失、零分母 N/A、
预算删失、主次身份、字段和面板。标签允许重叠，不能无声明地相加。FAIL 且 H 非
单例不是完成定位；正常单例不是协议 PASS；等价／未决、预算退出和已花成本可见。

## 8. Statistical and sample decision procedure / 统计与样本决定程序

First classify each estimand as finite-domain census or population inference,
paired or independent, discrete or continuous, and deterministic or stochastic.
For paired binary outcomes, propose paired contrasts with confidence intervals;
for counts/cardinality/cost, report paired effect distributions and robust
intervals appropriate to the observed dependence; for hierarchical repeated
attempts, estimate at the independent base-scene unit. Effect size and interval
come before multiplicity-adjusted confirmatory tests. No universal t-test and no
p-value-only conclusion are permitted.

`DEC-SAMPLE` remains open. Pilot/calibration must supply target population,
eligible-unit count, baseline/effect or desired precision, variability,
dependence, attrition/abstention and cost. The named scientific reviewer chooses
finite census, precision-based or effect-based paired sampling before
confirmatory registration. Clock/error budgets and repeat counts follow the same
evidence-first procedure. No rule may be tuned after learning which arm wins.

先把 estimand 区分为有限域穷举／总体推断、配对／独立、离散／连续、确定／随机，
再选效应量、区间与必要的多重比较；依赖单位是独立基础场景。样本量、时钟／误差
预算、重复数须由 pilot 或外部依据提供总体、精度／效应、变异、依赖、流失和成本，
由具名科学审查者在确认性登记前冻结，不能按哪一臂获胜事后调整。

## 9. Synthetic walkthrough / 合成记账走查

The 12 `SYNTHETIC-DESIGN-WALKTHROUGH` entries exercise: qualified normal;
FAIL with nonsingleton H; true-hypothesis exclusion; unconfirmed injection;
invalid observation; T5 overlap; Stop-Empty; confirmed equivalent; unresolved;
Stop-645; budget/incomplete; and a denominator-overlap/empty-cell case. Hand
accounting from the ledger gives 12 unique attempts, 3 PASS/FAIL answered, 2
FAIL, 1 PASS, 1 singleton localization decision, 1 abstain, 1 equivalent, 1
unconfirmed and 1 invalid-observation entry. Thus answered coverage is 3/12;
an empty requested cell is `N/A`, never 0%. The checker recalculates these
counts and rejects duplicate attempts, forged observed/confirmatory labels,
run IDs on unconfirmed/equivalent cases and omitted spent cost.

这 12 条均是设计走查而非实验结果。手算为 12 个唯一 attempt、3 个 PASS/FAIL
answered、2 FAIL、1 PASS、1 个单例定位决定，并分别保留弃权、等价、未确认和
无效观测；answered coverage 为 3/12，空单元输出 N/A 而非 0%。至少正常路径由
attempt／run、终态证据和最终 H 追踪，负面路径由 truthClass、Stop-Empty／排除 H
与 FINDING-RECORD／HISTORY-HANDLE 类字段追踪。

## 10. Engineering dependency and decision handoff / 工程依赖与决定交接

The JSON dependency matrix contains ten actionable entries. Existing references
resolve CAPTURE-IDENTITY, PACKET-REF, DATAGRAM-RECORD, TRANSFER-RECORD,
PROTOCOL-EVENT, OWNERSHIP-RESULT, OBSERVATION-ASSESSMENT, INTAKE-METADATA,
FINDING-RECORD, HISTORY-HANDLE and registered experiment outputs down to named
fields. Proposed deltas are explicitly `PROPOSED-CONTRACT-DELTA`, with producer,
type intent, truth visibility, compatibility, closure test and milestone. They
are requests for Decision Maker routing, not changes to engineering contracts.

| Decision | Recommendation; evidence | Owner / freeze / blocks |
|---|---|---|
| DEC-MATH-REVIEW | Review bounded C1/C2 and minimum counterexamples; do not enlarge theorem | independent mathematical reviewer / design acceptance / claim advancement |
| DEC-IUT | smallest interactive target preserving protocol/reset contract; identity, access, controllability | project owner / pilot / interactive runs |
| DEC-TRUTH | independent generator or dual evidence + adjudication; common-error analysis | named evaluator / pilot / effect metrics |
| DEC-EQUIV | confirmed equivalent/non-equivalent/unresolved with retained ledger | fault adjudicator / registration / mutation denominators |
| DEC-SAMPLE | choose census, precision or paired-effect design from estimand and pilot | scientific reviewer / registration / confirmatory execution |
| DEC-DISCLOSURE | author, affiliation, funding, permission and AI declarations | corresponding author / submission / submission only |

Milestones are ordered: design review → engineering feasibility → pilot/
calibration → frozen confirmatory registration → run → result acceptance.
Research design can be accepted while run admission remains blocked. PR #22 is
not required to implement these proposals and its offline chain does not close
prediction, timing, ownership, history, selection or active-execution evidence.

里程碑依次为设计评审、工程可行性、pilot／校准、冻结确认性登记、运行、结果接纳。
研究设计可先接受，而运行继续阻塞。依赖矩阵不向 PR #22 新增任务；其离线链也不
关闭预测、时序、所有权、历史、选择或主动执行证据。
