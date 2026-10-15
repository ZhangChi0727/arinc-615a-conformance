# CL-TAV Experiment Implementation Specification / CL-TAV 实验实施规格

**Identity:** `CLTAV-EXPERIMENT-DESIGN`, version `0.2-candidate`

**Parent authority:** `EXP-PLAN-2026-001`

**Machine source:** `configs/research/cltav_experiment_design.json`
**Status:** candidate design; **not** a registration, executable Configuration,
run approval, result, proof, or scientific approval.

## 1. Authority and snapshot discipline / 权威与快照纪律

The method report and ALG-CLTAV-01--07 define semantics; the interface registry
defines identifiers and record flow; development contracts define accepted
engineering records, scenarios, and acceptance cases; the experiment plan
defines three families and four arms. This specification only makes their
implementation-facing evaluation contract explicit.

Nine exact Git-blob bindings separate `ACCEPTED-AUTHORITY` inputs from
`SUCCESSOR-BASELINE` documents being revised by this change. The checker parses
accepted registry, development, CRS/model, method, and evidence-ledger bytes
from those verified blobs—not from mutable working-tree copies. A valid binding
therefore requires the declared path, role, base-commit OID, and SHA-256.

方法报告及 ALG-CLTAV-01--07 定义语义；接口登记定义标识与记录流；开发合同定义已
接受的工程记录、场景和验收用例；实验计划定义三个实验族和四个比较臂。本规格只
把面向实施的评价合同显式化。九项 Git blob 绑定区分“已接受权威”与本变更修改的
“后继基线”；检查器只解析经 OID 和 SHA-256 验证的 blob，不读取可变工作区副本。

## 2. Bounded C1/C2 argument / C1/C2 有界论证

| Claim / 主张 | Bounded proposition / 有界命题 | Assumptions / 假设 | Falsifier / 反证 | Allowed and prohibited wording / 可用与禁用措辞 |
|---|---|---|---|---|
| CL-C1 | For admitted histories, an accepted non-empty compatibility update is a subset of the preceding set and retains hypotheses compatible with the accumulated history. / 对已准入历史，非空相容更新是前一集合的子集，并保留与累计历史相容的假设。 | finite registered domain; qualified ownership and interval interpretation; accepted R1--R5 and `HISTORY-HANDLE` semantics | an update adds an absent hypothesis, changes the uncertainty identity, or removes a compatible truth hypothesis | say “bounded monotonicity and conditional retention”; do not claim universal convergence, completeness, or arbitrary-system certification |
| CL-C2 | `CL-LOOP` may condition a later admissible action on observations from its own earlier actions; `CL-T`, `CL-A`, and `CL-TA` may not. Any gain is empirical and pending. / `CL-LOOP` 可依据自身先前动作的观测选择后续动作；其余三臂不可；收益仍待实验。 | same registered initial information; no evaluator truth; issued-action charging; exclusive resource mode | comparator receives loop-only observations, truth leaks, an unaffordable action is issued, or registered parent metrics show no benefit | say “testable feedback distinction and candidate loop”; do not claim proven superiority or optimality |

Raw events, timestamp intervals, interpretation classes, the surviving set, and
compatible histories are distinct objects. `IF-EQUIV` is the accepted runtime
candidate-equivalence interface; injected-fault/mutant equivalence is a proposed
evaluator-only truth field and must not redefine `IF-EQUIV`.

原始事件、时间区间、解释类、候选集合与相容历史是不同对象。`IF-EQUIV` 只表示运行
期候选等价；注入故障／变异体等价属于评价者专用真值字段，不得重定义该接口。

## 3. Shared implementation tables / 共享实施表

The following bilingual tables are generated from one JSON source. Row order is
non-semantic; identifiers and references are semantic. The synchronization gate
normalizes line endings and rejects handwritten drift.

以下双语表由同一 JSON 源生成。行顺序不具语义，标识与引用具有语义；同步门规范化
换行并拒绝手工漂移。

<!-- experiment-design-shared:start -->

> Generated from `configs/research/cltav_experiment_design.json`; edit the JSON and run `python scripts/sync_experiment_design.py --write`. / 本区由结构化设计合同生成；请勿直接修改。

### Claim and arm boundary / 主张与实验臂边界

| Claim / 主张 | Bounded proposition / 有界命题 | Assumptions / 前提 | Falsifiers / 反证条件 | Gate / 门禁 |
|---|---|---|---|---|
| CL-C1 | For admitted histories and the accepted compatibility update, every non-empty update is a subset of the preceding hypothesis set and contains each hypothesis compatible with the accumulated history. | the initial set covers the registered hypothesis domain<br>observation compatibility is evaluated using the accepted interval rule | an accepted update adds a hypothesis absent from the preceding set<br>a compatible truth hypothesis is removed by the accepted update | DEC-MATH-REVIEW |
| CL-C2 | Under the registered arm contracts, CL-LOOP may condition a later admissible action on its own earlier observations while CL-T, CL-A, and CL-TA may not; any empirical gain remains pending execution. | all arms receive the same registered initial information<br>evaluator truth is never algorithm-visible<br>cost is charged on issued actions | a comparator receives later CL-LOOP observations<br>CL-LOOP sees evaluator truth<br>a reported gain disappears under the registered parent metric | DEC-MATH-REVIEW |

| Arm / 实验臂 | Visible inputs / 可见输入 | Actions / 动作 | Feedback / 反馈 | Prohibited / 禁止 |
|---|---|---|---|---|
| CL-A | IF-EXP-SCENE.algorithmVisibleFields (ALGORITHM-INITIAL / 算法初始可见) | analysis only | no / 否 | IF-EXP-TRUTH.truthRecord<br>invented acquisition<br>records acquired by another arm |
| CL-LOOP | IF-EXP-SCENE.algorithmVisibleFields (ALGORITHM-INITIAL / 算法初始可见)<br>IF-EXP-COLLECT.observationLog (ALGORITHM-OWN-ACTION / 算法自身动作所得)<br>IF-EXP-COLLECT.resourceLog (ALGORITHM-OWN-ACTION / 算法自身动作所得) | TEST<br>Prep<br>Recover<br>analysis-guided next action | yes / 是 | IF-EXP-TRUTH.truthRecord |
| CL-T | IF-EXP-SCENE.algorithmVisibleFields (ALGORITHM-INITIAL / 算法初始可见)<br>IF-EXP-COLLECT.observationLog (ALGORITHM-OWN-ACTION / 算法自身动作所得) | predetermined TEST<br>declared Prep/Recover when executed | no / 否 | IF-EXP-TRUTH.truthRecord<br>records acquired by another arm |
| CL-TA | IF-EXP-SCENE.algorithmVisibleFields (ALGORITHM-INITIAL / 算法初始可见)<br>IF-EXP-COLLECT.observationLog (ALGORITHM-OWN-ACTION / 算法自身动作所得) | frozen collection policy<br>analysis after frozen collection | no / 否 | IF-EXP-TRUTH.truthRecord<br>adaptive selection after analysis |

### Scenario contract / 场景合同

| Scenario / 场景 | Scope / 服务 | Development + CRS / 开发与需求 | Acceptance / 验收 | Perturbation / 扰动点 | Records / 记录 | Admission / 准入 |
|---|---|---|---|---|---|---|
| SC-ABORT | UPLOAD | SC-ABORT<br>APPLICABLE<br>CRS-M1-00104<br>CRS-M1-00108 | AC-EXP-SCENE<br>AC-EXP-CAUSAL<br>AC-SYN-TRANSFER<br>AM-OWNERSHIP<br>AM-TIMING | owned abort event during active transfer | TRANSFER-RECORD<br>PROTOCOL-EVENT<br>OWNERSHIP-RESULT | admit only when the abort is causally linked to one request instance |
| SC-INVALID-OBS | INFORMATION | SC-INVALID-OBS<br>TOOL-OR-EXPERIMENT-N/A | AC-EXP-SCENE<br>AC-EXP-CAUSAL<br>AC-SYN-OBSERVATION<br>AM-LABEL<br>AM-TIMING<br>AM-EXPERIMENT | capture timestamp, coverage, or ownership evidence | CAPTURE-IDENTITY<br>PACKET-REF<br>OBSERVATION-ASSESSMENT<br>FINDING-RECORD | retain in all-attempt accounting but exclude from IUT PASS/FAIL denominators |
| SC-NO-RESPONSE | INFORMATION | SC-NO-RESPONSE<br>APPLICABLE<br>CRS-M1-00101 | AC-EXP-SCENE<br>AC-EXP-CAUSAL<br>AC-SYN-OBSERVATION<br>AM-OWNERSHIP<br>AM-TIMING | owned response suppression after the CRS-M1-00101 request trigger; evaluator tracks exception delay and abort cancellation | PACKET-REF<br>PROTOCOL-EVENT<br>OWNERSHIP-RESULT<br>OBSERVATION-ASSESSMENT | admit only confirmed, non-equivalent suppression with a complete qualified horizon |
| SC-NORMAL-UPLOAD | UPLOAD | SC-NORMAL-UPLOAD<br>APPLICABLE<br>CRS-M1-00077 | AC-EXP-SCENE<br>AC-EXP-CAUSAL<br>AM-EXPERIMENT<br>AM-STATE | no perturbation; qualified upload completion control | TRANSFER-RECORD<br>PROTOCOL-EVENT<br>OBSERVATION-ASSESSMENT<br>HISTORY-HANDLE | admit only after scene identity, reset, and observation qualification pass |
| SC-RESOURCE-ERROR | INFORMATION | SC-RESOURCE-ERROR<br>TOOL-OR-EXPERIMENT-N/A | AC-EXP-SCENE<br>AC-EXP-CAUSAL<br>AC-SYN-RESOURCE-STOP<br>AM-RESOURCE<br>AM-STATE | declared resource controller or tool-error path | INTAKE-METADATA<br>FINDING-RECORD<br>HISTORY-HANDLE | retain every registered attempt and distinguish budget exhaustion from tool error |
| SC-SAME-KEY | INFORMATION | SC-SAME-KEY<br>TOOL-OR-EXPERIMENT-N/A | AC-EXP-SCENE<br>AC-EXP-CAUSAL<br>AC-SYN-HISTORY<br>AM-OWNERSHIP<br>AM-HISTORY | concurrent requests sharing a correlation key | PROTOCOL-EVENT<br>OWNERSHIP-RESULT<br>HISTORY-HANDLE | admit only when ambiguity is represented rather than silently resolved |
| SC-SINGLE-BATCH | UPLOAD | SC-SINGLE-BATCH<br>TOOL-OR-EXPERIMENT-N/A | AC-EXP-SCENE<br>AC-EXP-CAUSAL<br>AC-SYN-SELECT<br>AM-EXPERIMENT<br>AM-HISTORY | registered single-versus-batch selection policy | TRANSFER-RECORD<br>PROTOCOL-EVENT<br>HISTORY-HANDLE | admit paired units only when configuration differs solely at the registered perturbation |
| SC-WAIT-CONTINUE | UPLOAD | SC-WAIT-CONTINUE<br>APPLICABLE<br>CRS-M1-00106<br>CRS-M1-00107 | AC-EXP-SCENE<br>AC-EXP-CAUSAL<br>AC-SYN-HISTORY<br>AM-TIMING<br>AM-STATE | WAIT/continuation event timing and state transition | PROTOCOL-EVENT<br>OBSERVATION-ASSESSMENT<br>HISTORY-HANDLE | admit only when event ownership and both measurement intervals are reconstructable |

### Acceptance-matrix disposition / 验收矩阵处置

| AM id / 编号 | Disposition / 处置 | Consumers / 使用方 | Rationale / 理由 |
|---|---|---|---|
| AM-ADMIT | CONTROL-GATE | EXP-CLTAV-DETECT<br>EXP-CLTAV-LOCATE<br>EXP-CLTAV-ABLATION | applies algorithm action admission A1-A5: affordable distinguishing TEST, minimax/cost/id ordering, and declared Prep/Recover |
| AM-DRIFT | CONTROL-GATE | DEP-REGISTRATION | authority drift invalidates the registered design |
| AM-EXPERIMENT | CONTROL-GATE | DEP-REGISTRATION<br>SC-NORMAL-UPLOAD<br>SC-INVALID-OBS<br>SC-SINGLE-BATCH | experiment identity and pairing are control-plane gates |
| AM-FIELDS | SCENARIO-EVIDENCE | SC-NORMAL-UPLOAD<br>SC-ABORT | field evidence is collected by protocol scenarios |
| AM-FORMAT | PRE-RUN-CONTRACT | DEP-IUT | format preconditions belong to the selected environment |
| AM-HISTORY | SCENARIO-EVIDENCE | SC-SAME-KEY<br>SC-SINGLE-BATCH | history state is reconstructed per run |
| AM-IDENTITY | PRE-RUN-CONTRACT | DEP-REGISTRATION | binds capture manifest, path, hash and byte-length identity before evidence use |
| AM-IP | SCENARIO-EVIDENCE | SC-NORMAL-UPLOAD<br>SC-WAIT-CONTINUE<br>SC-NO-RESPONSE<br>SC-ABORT<br>SC-SAME-KEY | records IP reconstruction as COMPLETE, GAPPED or CONFLICT with overlap and epoch handling |
| AM-LABEL | SCENARIO-EVIDENCE | SC-INVALID-OBS | separates tool/capture anomalies from IUT findings |
| AM-OWNERSHIP | SCENARIO-EVIDENCE | SC-NO-RESPONSE<br>SC-ABORT<br>SC-SAME-KEY | ownership is a per-attempt causal fact |
| AM-RESOURCE | CONTROL-GATE | DEP-RESOURCE<br>SC-RESOURCE-ERROR | budget and charge modes are frozen before execution |
| AM-STATE | SCENARIO-EVIDENCE | SC-NORMAL-UPLOAD<br>SC-WAIT-CONTINUE<br>SC-RESOURCE-ERROR | state transitions support outcome and stop attribution |
| AM-TFTP | SCENARIO-EVIDENCE | SC-NORMAL-UPLOAD<br>SC-WAIT-CONTINUE<br>SC-NO-RESPONSE<br>SC-ABORT<br>SC-SINGLE-BATCH | records TID, option, retransmission, wrap and final-block reconstruction semantics |
| AM-TIMING | SCENARIO-EVIDENCE | SC-WAIT-CONTINUE<br>SC-NO-RESPONSE<br>SC-ABORT<br>SC-INVALID-OBS | timing intervals are per-attempt evidence |

### Metric dictionary / 指标字典

| Metric / 指标 | Population / 分母总体 | Numerator / 分子总体 | Calculation / 计算 | Missing + censoring / 缺失与删失 | Analysis / 分析 | Primary / 主要 |
|---|---|---|---|---|---|---|
| MET-ABLATION-DELTA | POP-PAIRED-ELIGIBLE | — | within-pair arm difference for each named parent metric | unmatched pairs are reported and not imputed<br>inherits each parent metric censoring rule<br>zero=N/A | AN-PAIRED | no / 否 |
| MET-ABSTAIN | POP-ATTEMPTS | POP-ABSTAIN | abstentions / all attempts | missing validity invalidates row<br>none<br>zero=N/A | AN-FLOW | no / 否 |
| MET-ANSWERED-COVERAGE | POP-ATTEMPTS | POP-ANSWERED | answered attempts / all attempts | missing validity or outcome invalidates the row<br>no censoring; budget and error exits remain in denominator<br>zero=N/A | AN-PROPORTION | yes / 是 |
| MET-ATTEMPTS | POP-ATTEMPTS | — | cardinality | missing attemptId invalidates the row<br>none; retain every registered attempt<br>zero=N/A | AN-FLOW | no / 否 |
| MET-CONDITIONAL-DETECTION-ERROR | POP-ANSWERED | POP-CONDITIONAL-ERROR | wrong answered decisions / answered attempts | missing evaluator truth invalidates error classification<br>defined only for answered attempts<br>zero=N/A | AN-PROPORTION | yes / 是 |
| MET-COST-VECTOR | POP-ATTEMPTS | — | project detail costs to (acquisition, computation, preparation, retry), folding recovery into preparation once | missing charge field invalidates row<br>include spent cost for incomplete and error exits<br>zero=N/A | AN-DISTRIBUTION | yes / 是 |
| MET-ERROR | POP-ATTEMPTS | POP-ERROR | errors / all attempts | missing outcome or validity invalidates row<br>none<br>zero=N/A | AN-FLOW | no / 否 |
| MET-FALSE-FAIL | POP-QUALIFIED-NORMAL | POP-FALSE-FAILS | valid FAIL / qualified normal controls | unqualified normal controls stay outside this denominator<br>tool errors are not false failures<br>zero=N/A | AN-PROPORTION | yes / 是 |
| MET-FINAL-CANDIDATES | POP-LOCALIZATION-ELIGIBLE | — | distribution of len(finalHypotheses) | missing finalHypotheses invalidates row<br>include incomplete and empty exits with stop class<br>zero=N/A | AN-DISTRIBUTION | yes / 是 |
| MET-INCOMPLETE | POP-ATTEMPTS | POP-INCOMPLETE | incomplete or budget-exhausted attempts / all attempts | missing resourceStatus invalidates row<br>right-censored runtime/cost remains visible<br>zero=N/A | AN-FLOW | no / 否 |
| MET-INCONCLUSIVE | POP-ATTEMPTS | POP-INCONCLUSIVE | inconclusive attempts / all attempts | missing outcome invalidates row<br>interval overlap is retained as inconclusive<br>zero=N/A | AN-FLOW | no / 否 |
| MET-LOCALIZATION-COVERAGE | POP-LOCALIZATION-ELIGIBLE | POP-LOCALIZATION-DECISION | issued localization decisions / eligible localization attempts | missing decision flag invalidates row<br>empty/error stops remain in eligible denominator<br>zero=N/A | AN-PROPORTION | yes / 是 |
| MET-MISS | POP-CONFIRMED-FAULT | POP-MISSES | valid PASS / confirmed in-domain non-equivalent fault attempts | unconfirmed or unresolved injection is retained outside this denominator<br>budget/error exits remain in fault denominator and are reported separately<br>zero=N/A | AN-PROPORTION | yes / 是 |
| MET-ROUNDS | POP-ROUNDS | — | issued actions per ROUNDS-policy run | non-ROUNDS policy is not applicable<br>right-censor at the registered round limit<br>zero=N/A | AN-DISTRIBUTION | no / 否 |
| MET-SINGLETON-CORRECT | POP-SINGLETON-DECISION | POP-SINGLETON-CORRECT | correct singletons / issued singleton decisions | missing truth invalidates row<br>Stop-645 and budget stops cannot create singleton decisions<br>zero=N/A | AN-PROPORTION | no / 否 |
| MET-TRUE-EXCLUDED | POP-LOCALIZATION-DECISION | POP-TRUE-EXCLUDED | decisions excluding truth / issued localization decisions | missing truth or final set invalidates row<br>no-decision attempts are not truth exclusions<br>zero=N/A | AN-PROPORTION | no / 否 |
| MET-TRUE-RETAINED | POP-LOCALIZATION-DECISION | POP-TRUE-RETAINED | decisions retaining truth / issued localization decisions | missing truth or final set invalidates row<br>no-decision attempts are reported by coverage, not silently removed<br>zero=N/A | AN-PROPORTION | yes / 是 |

### Analysis decisions / 分析决定

| Plan / 方案 | Estimand / 估计目标 | Unit + pairing / 单位与配对 | Estimator + interval / 估计量与区间 | Applicability / 适用性 | Evidence / 方法证据 | Freeze / 冻结决定 |
|---|---|---|---|---|---|---|
| AN-DISTRIBUTION | distribution of survivor count, cost, or rounds | registered scene attempt or independently reset run as explicitly registered<br>use paired/clustered branch when scenes or seeds are shared; never infer independence from row count | finite empirical distribution for exhaustive domain; paired or cluster-aware descriptive contrast when dependence is registered<br>no resampling interval until randomness and resampling unit are established; otherwise WAIT-DEC-SAMPLE<br>PAIRED-OR-CLUSTERED / 配对或聚类<br>WAIT-DEC-SAMPLE / 等待样本量决定 | count/cost metrics; no automatic large-sample or bootstrap assumption | EVID-2026-063<br>EVID-2026-064<br>EVID-2026-065<br>METHOD.md §6.2 lines 995-1023: conditional i.i.d. example and clustered-data warning | DEC-SAMPLE |
| AN-FLOW | finite attempt-flow proportion or count | attempt<br>none | finite count and empirical proportion<br>descriptive finite enumeration; no superpopulation interval unless DEC-SAMPLE selects an independent-random branch<br>FLOW-ONLY / 仅流程描述<br>WAIT-DEC-SAMPLE / 等待样本量决定 | flow and coverage metrics | EVID-2026-064<br>EVID-2026-065<br>METHOD.md §6.2 lines 995-1023: conditional i.i.d. example and clustered-data warning | DEC-SAMPLE |
| AN-PAIRED | within-scene ablation change in a named parent metric | registered pair<br>same base scene/seed, reciprocal registered arms, distinct independently confirmed resets, and parent eligibility | paired difference on the named parent metric scale<br>paired candidate only after pair independence/repeat structure and direct method source are frozen; otherwise WAIT-DEC-SAMPLE<br>PAIRED-OR-CLUSTERED / 配对或聚类<br>WAIT-DEC-SAMPLE / 等待样本量决定 | only when parent metric semantics and every pair-eligibility field hold | EVID-2026-063<br>EVID-2026-064<br>EVID-2026-065<br>METHOD.md §6.2 lines 995-1023: conditional i.i.d. example and clustered-data warning | DEC-SAMPLE |
| AN-PROPORTION | finite-population decision or error proportion | registered scene attempt<br>independent only after scene/seed and shared-run clustering are excluded | finite-domain proportion for a complete census, otherwise empirical proportion and registered risk difference<br>finite-domain enumeration for a census; independent-binomial candidate only with verified independent random assignment; otherwise WAIT-DEC-SAMPLE<br>INDEPENDENT-RANDOMIZED / 独立随机<br>WAIT-DEC-SAMPLE / 等待样本量决定 | binary metrics with nonzero denominator and branch inputs frozen before held-out access | EVID-2026-063<br>EVID-2026-064<br>EVID-2026-065<br>METHOD.md §6.2 lines 995-1023: conditional i.i.d. example and clustered-data warning | DEC-SAMPLE |

### Comparison families / 比较族

| Family / 比较族 | Class / 类别 | Metrics / 指标 | Contrasts / 对比 | Joint conclusion / 联合结论 | Multiplicity / 多重性 |
|---|---|---|---|---|---|
| CF-EXPLORATORY | EXPLORATORY / 探索性 | MET-ABLATION-DELTA | registered within-scene CL-LOOP versus comparator ablation pair | hypothesis-generating only unless parent estimand and family role are preregistered | label exploratory unless its parent estimand and multiplicity treatment are frozen before held-out access |
| CF-PRIMARY | PRIMARY / 主要 | MET-ANSWERED-COVERAGE<br>MET-CONDITIONAL-DETECTION-ERROR<br>MET-MISS<br>MET-FALSE-FAIL<br>MET-LOCALIZATION-COVERAGE<br>MET-TRUE-RETAINED<br>MET-FINAL-CANDIDATES<br>MET-COST-VECTOR | EXP-CLTAV-DETECT: CL-LOOP versus CL-T<br>EXP-CLTAV-LOCATE: CL-LOOP versus CL-T<br>EXP-CLTAV-LOCATE: CL-LOOP versus CL-TA | no primary superiority conclusion unless the registered detection/localization benefit and cost/coverage safeguards jointly hold | DEC-SAMPLE must freeze one family-wise procedure before held-out access; until then report estimates and uncertainty without confirmatory rejection claims |
| CF-SECONDARY | SECONDARY / 次要 | MET-ABSTAIN<br>MET-INCONCLUSIVE<br>MET-ERROR<br>MET-INCOMPLETE<br>MET-TRUE-EXCLUDED<br>MET-SINGLETON-CORRECT<br>MET-ROUNDS | same registered arm contrasts as CF-PRIMARY where the metric applies | supports interpretation and failure-mode accounting but cannot replace a failed primary safeguard | descriptive with interval estimates; no confirmatory multiplicity claim |

### Engineering dependencies / 工程依赖

| Dependency / 依赖 | Consumers / 使用方 | Current ref / 当前引用 | Evidence + producer / 证据与产出方 | State + proposal / 状态与提议 | Decisions / 决定 | Closure + follow-up / 闭合与后续 | Milestone / 里程碑 |
|---|---|---|---|---|---|---|---|
| DEP-645-RUNTIME | EXP-CLTAV-ABLATION | kind=authority-binding; ref=ARINC-645 candidate source and semantic binding | implemented and independently checked CRC/check-value/naming oracle<br>future authorized engineering change | RUNTIME-PENDING<br>findingRecord.oracleRef [evaluator and audit] | DEC-IUT | independent vectors and oracle evidence; source presence alone is insufficient<br>separate engineering CR if this cell is retained | 645-specific-run |
| DEP-CLOCK | SC-WAIT-CONTINUE<br>SC-NO-RESPONSE<br>SC-INVALID-OBS | kind=record-field; ref=OBSERVATION-ASSESSMENT.measurementInterval | clock chain and error budget<br>test environment owner | RUNTIME-PENDING<br>observationAssessment.clockChainRef [algorithm and evaluator] | DEC-CLOCK | calibration evidence and interval reproduction<br>qualify clock and freeze the error budget | pilot |
| DEP-EQUIV | MET-MISS<br>MET-ABLATION-DELTA | kind=contrast-only-algorithm-interface; ref=IF-EQUIV.established | evaluator-side equivalenceDisposition distinct from runtime candidate equivalence<br>named fault adjudicator | PROPOSED-CONTRACT-DELTA<br>truthRecord.equivalenceDisposition [evaluator-only] | DEC-EQUIV | one evaluator field yields equivalent, non-equivalent or unresolved accounting without reusing runtime IF-EQUIV<br>approve evaluator adjudication procedure | confirmatory-registration |
| DEP-IUT | SC-NORMAL-UPLOAD<br>SC-WAIT-CONTINUE<br>SC-NO-RESPONSE<br>SC-ABORT<br>SC-SAME-KEY<br>SC-SINGLE-BATCH<br>SC-RESOURCE-ERROR | kind=experiment-plan-section; ref=EXP-PLAN-2026-001:prerequisites | interactive IUT identity, behavior boundary, and reviewed safe initial projection<br>project owner and later authorized implementer | PROPOSED-CONTRACT-DELTA<br>sceneRecord.iutIdentity [evaluator and audit]<br>IF-EXP-SCENE.algorithmVisibleFields [all arms; excludes faultPlan, truthSource, injection confirmation, validity and posthoc adjudication] | DEC-IUT | reviewed IUT/configuration identity resolves and leakage test proves only the safe projection is algorithm-visible<br>select IUT and approve the projected initial-field allowlist | pilot |
| DEP-OBS-QUAL | SC-INVALID-OBS<br>MET-ERROR | kind=record-field; ref=OBSERVATION-ASSESSMENT.verdict | qualification policy separating capture/tool error from IUT verdict<br>observation assessor | EXISTING-REFERENCE | DEC-CLOCK | invalid timestamp/ownership witness produces ERROR without IUT blame<br>retain accepted qualification semantics | design-review |
| DEP-REGISTRATION | EXP-CLTAV-DETECT<br>EXP-CLTAV-LOCATE<br>EXP-CLTAV-ABLATION | kind=experiment-plan; ref=EXP-PLAN-2026-001 | frozen confirmatory registration<br>experiment registrar and named scientific reviewer | HUMAN-PENDING | DEC-MATH-REVIEW<br>DEC-IUT<br>DEC-TRUTH<br>DEC-EQUIV<br>DEC-SAMPLE<br>DEC-RESOURCE<br>DEC-CLOCK | registration committed before confirmatory runs<br>freeze units, budgets, denominators, adjudication and analysis | confirmatory-run |
| DEP-RESET | SC-NORMAL-UPLOAD<br>SC-SINGLE-BATCH | kind=experiment-interface; ref=IF-EXP-SCENE.sceneRecord | reset identifier and success evidence<br>scene controller | PROPOSED-CONTRACT-DELTA<br>sceneRecord.resetId [all arms and evaluator]<br>sceneRecord.resetEvidenceRef [evaluator and audit] | DEC-IUT | paired run starts from independently confirmed reset<br>define reset evidence fields | pilot |
| DEP-RESOURCE | SC-RESOURCE-ERROR<br>MET-COST-VECTOR<br>MET-ROUNDS | kind=algorithm-interface; ref=IF-RESOURCE-STOP.trace | exclusive resource mode and actual charge log<br>runtime resource controller | RUNTIME-PENDING<br>resourceLog.mode [algorithm and evaluator]<br>resourceLog.detailCharges [evaluator and audit] | DEC-RESOURCE | one charge per issued action, recovery folded once into preparation, and named exhaustion<br>implement charge trace without changing accepted cost semantics | pilot |
| DEP-SAMPLE | MET-ANSWERED-COVERAGE<br>MET-MISS<br>MET-TRUE-RETAINED<br>MET-ABLATION-DELTA | kind=placeholder; ref=PH-STAT-N | precision/effect target or finite census basis plus pilot variance/prevalence<br>named scientific reviewer | HUMAN-PENDING | DEC-SAMPLE | sample size, repeat policy, comparison family, and multiplicity role frozen before held-out access<br>run non-confirmatory pilot then decide | confirmatory-registration |
| DEP-TRUTH | MET-MISS<br>MET-FALSE-FAIL<br>MET-TRUE-RETAINED<br>MET-SINGLETON-CORRECT | kind=experiment-interface; ref=IF-EXP-TRUTH.truthRecord | confirmed injection and evaluator-only adjudicated truth<br>independent evaluator | PROPOSED-CONTRACT-DELTA<br>truthRecord.confirmationRef [evaluator-only]<br>truthRecord.equivalenceDisposition [evaluator-only] | DEC-TRUTH<br>DEC-EQUIV | truth leakage review plus independent confirmation witness<br>approve generator/adjudicator separation | pilot |

### Hypothetical method-choice walkthroughs / 假设性方法选择见证

| Choice / 选择 | Label / 标签 | Inputs / 输入 | Branch / 分支 | Result / 结果 | Rationale / 理由 |
|---|---|---|---|---|---|
| CHOICE-CENSUS | HYPOTHETICAL-NOT-RESULT / 假设示例，非结果 | COMPLETE<br>UNKNOWN<br>NONE<br>no / 否 | DETERMINISTIC-EXHAUSTIVE / 确定性穷举 | CANDIDATE-METHOD / 候选方法 | A completely enumerated registered finite domain uses finite counts/proportions without a superpopulation claim. |
| CHOICE-INDEPENDENT | HYPOTHETICAL-NOT-RESULT / 假设示例，非结果 | INCOMPLETE<br>INDEPENDENT<br>NONE<br>no / 否 | INDEPENDENT-RANDOMIZED / 独立随机 | CANDIDATE-METHOD / 候选方法 | Independent randomized scene attempts permit the registered independent-sample candidate, subject to DEC-SAMPLE. |
| CHOICE-PAIRED | HYPOTHETICAL-NOT-RESULT / 假设示例，非结果 | INCOMPLETE<br>NOT-INDEPENDENT<br>PAIRED<br>yes / 是 | PAIRED-OR-CLUSTERED / 配对或聚类 | CANDIDATE-METHOD / 候选方法 | Shared scenes with reciprocal arms and reset evidence require a paired or cluster-aware candidate. |
| CHOICE-WAIT | HYPOTHETICAL-NOT-RESULT / 假设示例，非结果 | UNKNOWN<br>UNKNOWN<br>UNKNOWN<br>no / 否 | NONE | WAIT-DEC-SAMPLE / 等待样本量决定 | Missing domain, independence and pairing inputs stops method selection; this is not a power calculation or observed result. |

### Open decisions / 待定决定

| Decision / 决定 | Owner / 负责人 | Inputs / 输入 | Procedure / 程序 | Freeze / 冻结点 | Closure witness / 闭合证据 |
|---|---|---|---|---|---|
| DEC-CLOCK | test environment owner and metrology reviewer | clock accuracy, synchronization, timestamp path, and JCGM 100/106-informed error budget | construct and independently reproduce the interval; freeze endpoint inclusivity and overlap rule | pilot | clock-chain report, calibration reference, and interval replay |
| DEC-DISCLOSURE | corresponding author | author declarations | collect each declaration and reconcile it with the manuscript checklist | submission | completed disclosure checklist |
| DEC-EQUIV | named fault adjudicator | fault-specific evaluator record plus impact evidence | two-stage impact screen and named human adjudication with unresolved allowed | confirmatory registration | adjudication form and population-flow rule |
| DEC-IUT | project owner | identity, access, controllability, configuration and reset evidence | score candidates against scenario access and independent reset | pilot | versioned IUT/configuration identity plus reset demonstration |
| DEC-MATH-REVIEW | independent mathematical reviewer | argument table and minimum counterexample witnesses | record proposition-by-proposition disposition and any counterexample | design acceptance | signed review record naming accepted propositions |
| DEC-RESOURCE | experiment owner and runtime implementer | pilot charge traces, feasible resource envelope and retry-safety evidence | project detail charges to the accepted four-vector, test no-double-charge, select exactly one session mode, then register a separate retry cap that reports execution error without creating another Stop-Budget mode | confirmatory registration | versioned single-mode budget table, retry-cap rule and passing charge-accounting witness |
| DEC-SAMPLE | named scientific reviewer | estimand, precision/effect target, pilot information and dependence structure | select experimental unit and repeat policy first, then compute or justify N and comparison-family treatment | confirmatory registration | registered N/repeats table and statistical review sign-off |
| DEC-TRUTH | named evaluator | confirmation and common-error analysis | document independence and run a deliberate disagreement witness | pilot | truth-source protocol and leakage review |

### Synthetic accounting witness / 合成记账见证

| Attempts / 尝试 | Answered / 已回答 | Coverage / 覆盖 | Conditional error / 条件错误 | Localization coverage / 定位覆盖 | Projected cost / 投影成本 | Review/setup / 评审准备工作量 |
|---|---|---|---|---|---|---|
| 13 | 4 | 4/13 | 0/4 | 3/6 | acquisition=10; computation=9; preparation=3; retry=1 | 3.0 |

<!-- experiment-design-shared:end -->

## 4. Experimental unit, retention, and reset / 实验单位、保留与复位

One registered attempt on one base scene, arm, and fault/control construction is
the experimental unit. `attemptId` is the all-ledger de-duplication key; a
`runId` exists only after admission. Packets, events, timestamps, hypotheses,
and repeated fields are observations within an attempt, not independent samples.
Paired rows share a non-null `pairingId` and require an independently confirmed
reset. Unmatched pairs remain visible and are never imputed.

一个基础场景、一个比较臂及一种故障／控制构造上的一次登记尝试构成实验单位。
`attemptId` 用于全台账去重；只有通过准入后才有 `runId`。包、事件、时间戳、假设及
重复字段是尝试内观测，不是独立样本。配对行共享非空 `pairingId`，且必须各自完成
独立复位；缺失配对不插补并保持可见。

Every registered attempt remains in `POP-ATTEMPTS`. Unconfirmed injections,
confirmed equivalents, unresolved equivalence, abstentions, invalid observations,
budget exits, and errors have named states. They may be outside a scored
denominator, but they are never erased from flow or cost accounting.

所有登记尝试都保留在 `POP-ATTEMPTS`。未确认注入、确认等价、等价性未决、弃权、
无效观测、预算退出和错误均有具名状态；即使不进入某个计分分母，也不得从流量或
成本记账中删除。

## 5. Arm visibility and truth boundary / 比较臂可见性与真值边界

Visible inputs are typed as either `ALGORITHM-INITIAL` or
`ALGORITHM-OWN-ACTION`. `IF-EXP-TRUTH.truthRecord` is always
`EVALUATOR-ONLY`; a field name, prose alias, or working-tree-only interface
member cannot make it algorithm-visible. Non-loop arms have no feedback.
`CL-A` cannot receive records from actions it did not execute.

可见输入只允许 `ALGORITHM-INITIAL` 或 `ALGORITHM-OWN-ACTION` 两种类型。
`IF-EXP-TRUTH.truthRecord` 始终为 `EVALUATOR-ONLY`；改名、文本别名或仅存在于工作区
的接口成员均不能使其成为算法输入。非闭环臂不得接收反馈，`CL-A` 不得接收自身未
执行动作产生的记录。

Truth confirmation and mutation-equivalence adjudication must be independent of
the parser whose result is being scored, or must use a documented dual-evidence
procedure with disagreement retained. Confirmed equivalents are excluded only
from the scored mutation/fault denominator; equivalent and unresolved counts and
review cost remain reportable. This follows the bounded accounting use of
`EVID-2026-077` and `EVID-2026-079`, not a historical prevalence prior.

## 6. Finite populations, stops, and interval witness / 有限总体、停止与区间见证

Metric populations are derived from row fields, not handwritten denominator
tags. A valid answered decision is exactly `validity == VALID` with outcome
`PASS` or `FAIL`; `ERROR`, `INCONCLUSIVE`, and `NOT-ANSWERED` are not answered.
Thus zero answers among twelve attempts gives answered coverage `0/12`, while
conditional detection error is `N/A` because its denominator is empty.

指标总体由行字段推导，不使用手填分母标签。只有 `validity == VALID` 且结果为
`PASS` 或 `FAIL` 才算已回答；`ERROR`、`INCONCLUSIVE` 与 `NOT-ANSWERED` 均不算。
因此十三次尝试中零次回答时，回答覆盖率为 `0/13`，而条件检测错误率因分母为空为
`N/A`。

Stop processing is stage-sensitive. `Stop-Empty` is a post-update `ERROR` with
an empty survivor set and no localization decision. `Stop-645` is a post-update
abstention and cannot become a singleton merely because one candidate remains.
`Stop-Budget` preserves the partial set and spent cost but does not issue a
singleton decision. Pre-action admission failure issues no action and charges no
action cost.

停止处理与阶段相关：`Stop-Empty` 是更新后、候选集为空且不产生定位决定的 `ERROR`；
`Stop-645` 是更新后弃权，不能因只剩一个候选而变成单点决定；`Stop-Budget` 保留部分
集合和已花成本但不产生单点决定。动作前准入失败不得发出动作或计动作成本。

The T5 synthetic witness uses closed measured interval `[5.0, 5.2] s` and requirement
interval `[4.0, 5.1] s`. They overlap without containment, so the outcome is
`INCONCLUSIVE`; full containment is `PASS`, disjointness is `FAIL`, and closed
endpoint contact is overlap. Endpoint order, unit mismatch, or a wrong class is rejected.

## 7. Cost and statistical boundary / 成本与统计边界

The accepted comparison vector is `(acquisition, computation, preparation,
retry)`. Runtime detail may retain `recovery`, but projection folds it into
`preparation` exactly once. Charges attach only to issued actions. Incomplete,
budget, abstention, and error attempts retain all spent cost.
Pre-run review/setup effort is retained in a separate audit total and is never
charged to an unissued arm action.

接受的比较向量为 `(acquisition, computation, preparation, retry)`。运行细节可保留
`recovery`，但投影时只合并到 `preparation` 一次；只有实际发出的动作才计费。未完成、
预算、弃权及错误尝试均保留全部已花成本。

Primary, secondary, and exploratory families name the existing arm contrasts
and their joint conclusion rule. Every primary metric
has a finite population, missing/censoring rule, analysis plan, and freeze
decision. The current statistical procedures are candidates only. Experimental
unit, pairing/repeat policy, randomness, target precision/effect, resource budget,
and clock/error budget must be frozen by their named decisions before held-out or
confirmatory access. The finite choice table selects deterministic exhaustive,
independent-randomized, or paired/clustered candidates only when their inputs are
present; otherwise it returns `WAIT-DEC-SAMPLE`. Its examples are hypothetical,
not power calculations, pilots, or results. `EVID-2026-063`--`065` support conditional use of independent
runs, censoring-aware reporting, effect sizes, and transparent raw results; they
do not prescribe a universal repeat count. JCGM 100/106 guide the open clock and
measurement-error decision but do not themselves validate this apparatus.

## 8. Synthetic witness and admission limit / 合成见证与准入限制

The thirteen walkthrough rows are synthetic design/accounting witnesses only.
They exercise normal PASS, non-singleton fault FAIL, wrong singleton, unconfirmed
injection, invalid observation, interval overlap, `Stop-Empty`, confirmed
equivalent, unresolved equivalence, `Stop-645`, spent-cost budget exit, and
pre-action admission failure, and a reciprocal same-scene paired comparator.
They are not observed experiment results and must
not appear in a confirmatory result table.

十三行走查只用于合成设计与记账核对，覆盖正常 PASS、非单点故障 FAIL、错误单点、
未确认注入、无效观测、区间重叠、`Stop-Empty`、确认等价、等价性未决、`Stop-645`、
保留成本的预算退出、动作前准入失败及同场景互为对照的有效配对。它们不是观测实验结果，不得进入确认性结果表。

Historical captures remain `EXPLORATORY-OFFLINE-ONLY`. Confirmatory execution is
`BLOCKED` until the seven listed scientific/runtime decisions close. Disclosure
remains separately blocking for submission. This candidate neither selects an
IUT nor authorizes implementation, execution, claim promotion, or submission.

历史抓包仅可用于离线探索。七项科学／运行决定闭合前，确认性执行保持 `BLOCKED`；
披露决定另行阻塞投稿。本候选不选择 IUT，也不授权实现、执行、主张升级或投稿。
