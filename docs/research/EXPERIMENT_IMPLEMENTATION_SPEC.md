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

| Claim / 主张 | Bounded proposition | Assumptions | Falsifiers | Controlled Chinese / 受控中文 | Gate / 门禁 |
|---|---|---|---|---|---|
| CL-C1 | For admitted histories and the accepted compatibility update, every non-empty update is a subset of the preceding hypothesis set and contains each hypothesis compatible with the accumulated history. | the initial set covers the registered hypothesis domain<br>observation compatibility is evaluated using the accepted interval rule | an accepted update adds a hypothesis absent from the preceding set<br>a compatible truth hypothesis is removed by the accepted update | 在已登记模型与合格观测下，有效历史更新只能缩小假设集并保留所有与累积历史相容的假设；新增假设或删除相容真值均构成反证。 | DEC-MATH-REVIEW |
| CL-C2 | Under the registered arm contracts, CL-LOOP may condition a later admissible action on its own earlier observations while CL-T, CL-A, and CL-TA may not; any empirical gain remains pending execution. | all arms receive the same registered initial information<br>evaluator truth is never algorithm-visible<br>cost is charged on issued actions | a comparator receives later CL-LOOP observations<br>CL-LOOP sees evaluator truth<br>a reported gain disappears under the registered parent metric | 仅 CL-LOOP 可依据自身先前观测选择后续合格动作；比较臂不得获得该反馈或评估真值，任何性能增益须待实验验证。 | DEC-MATH-REVIEW |

| Arm / 实验臂 | Visible inputs / 可见输入 | Actions | Feedback / 反馈 | Prohibited | Controlled Chinese / 受控中文 |
|---|---|---|---|---|---|
| CL-A | IF-EXP-SCENE.algorithmVisibleFields (ALGORITHM-INITIAL / 算法初始可见) | analysis only | no / 否 | IF-EXP-TRUTH.truthRecord<br>invented acquisition<br>records acquired by another arm | CL-A 仅执行分析计算，只读取初始安全投影，不得虚构采集、读取评估真值或使用其他臂记录。 |
| CL-LOOP | IF-EXP-SCENE.algorithmVisibleFields (ALGORITHM-INITIAL / 算法初始可见)<br>IF-EXP-COLLECT.observationLog (ALGORITHM-OWN-ACTION / 算法自身动作所得)<br>IF-EXP-COLLECT.resourceLog (ALGORITHM-OWN-ACTION / 算法自身动作所得) | TEST<br>Prep<br>Recover<br>analysis-guided next action | yes / 是 | IF-EXP-TRUTH.truthRecord | CL-LOOP 可依据自身动作的观测与资源日志选择下一动作，但始终不得读取评估真值。 |
| CL-T | IF-EXP-SCENE.algorithmVisibleFields (ALGORITHM-INITIAL / 算法初始可见)<br>IF-EXP-COLLECT.observationLog (ALGORITHM-OWN-ACTION / 算法自身动作所得) | predetermined TEST<br>declared Prep/Recover when executed | no / 否 | IF-EXP-TRUTH.truthRecord<br>records acquired by another arm | CL-T 执行预定测试及必要准备或恢复，只读取初始安全投影与自身动作产生的观测，不得读取真值或其他臂记录。 |
| CL-TA | IF-EXP-SCENE.algorithmVisibleFields (ALGORITHM-INITIAL / 算法初始可见)<br>IF-EXP-COLLECT.observationLog (ALGORITHM-OWN-ACTION / 算法自身动作所得) | frozen collection policy<br>analysis after frozen collection | no / 否 | IF-EXP-TRUTH.truthRecord<br>adaptive selection after analysis | CL-TA 按冻结策略采集后分析，不得在分析后自适应选测，也不得读取评估真值。 |

| Registered contrast / 注册对比 | Family / 实验族 | Arms / 实验臂 | Parent metrics / 父指标 |
|---|---|---|---|
| CONTRAST-DETECT-LOOP-T | EXP-CLTAV-DETECT | CL-LOOP<br>CL-T | MET-ANSWERED-COVERAGE<br>MET-COST-VECTOR |
| CONTRAST-LOCATE-LOOP-T | EXP-CLTAV-LOCATE | CL-LOOP<br>CL-T | MET-ANSWERED-COVERAGE<br>MET-TRUE-RETAINED<br>MET-COST-VECTOR |
| CONTRAST-LOCATE-LOOP-TA | EXP-CLTAV-LOCATE | CL-LOOP<br>CL-TA | MET-ANSWERED-COVERAGE<br>MET-TRUE-RETAINED<br>MET-COST-VECTOR |

### Scenario contract / 场景合同

| Scenario / 场景 | Scope / 服务 | Development + CRS / 开发与需求 | Acceptance / 验收 | Perturbation | Records / 记录 | Admission | Controlled Chinese / 受控中文 |
|---|---|---|---|---|---|---|---|
| SC-ABORT | UPLOAD | SC-ABORT<br>APPLICABLE<br>CRS-M1-00104<br>CRS-M1-00108 | AC-EXP-SCENE<br>AC-EXP-CAUSAL<br>AC-SYN-TRANSFER<br>AM-OWNERSHIP<br>AM-TIMING | owned abort event during active transfer<br>independent controller log<br>abort cancels only the owned obligation and does not waive unrelated clocks | TRANSFER-RECORD<br>PROTOCOL-EVENT<br>OWNERSHIP-RESULT | admit only when the abort is causally linked to one request instance | 中止仅取消与其因果归属的特定义务，不豁免其他时钟；须以独立控制器记录确认。 |
| SC-INVALID-OBS | INFORMATION | SC-INVALID-OBS<br>TOOL-OR-EXPERIMENT-N/A | AC-EXP-SCENE<br>AC-EXP-CAUSAL<br>AC-SYN-OBSERVATION<br>AM-LABEL<br>AM-TIMING<br>AM-EXPERIMENT | capture timestamp, coverage, or ownership evidence<br>evaluator construction record, not an IUT-fault label<br>ERROR or existing qualification result; never direct IUT blame | CAPTURE-IDENTITY<br>PACKET-REF<br>OBSERVATION-ASSESSMENT<br>FINDING-RECORD | retain in all-attempt accounting but exclude from IUT PASS/FAIL denominators | 无效观测归为工具或捕获错误并保留在全尝试流中，不直接归责 IUT，也不进入 PASS/FAIL 分母。 |
| SC-NO-RESPONSE | INFORMATION | SC-NO-RESPONSE<br>APPLICABLE<br>CRS-M1-00101 | AC-EXP-SCENE<br>AC-EXP-CAUSAL<br>AC-SYN-OBSERVATION<br>AM-OWNERSHIP<br>AM-TIMING | after the data loader receives a status file carrying an exception delay for the active operation, suppress both the next status file within that delay and the required data-loader abort fallback after expiry<br>evaluator confirms the received status-file delay and active-operation key, records the unresolved expiry endpoint, and observes to a finite qualified endpoint for either a new status file or the required data-loader abort fallback<br>PASS when a new status file is strictly before the unresolved expiry endpoint or when the prescribed data-loader abort fallback is actually observed after expiry; equality remains NOT-SCORED until DEC-CLOCK freezes the endpoint, and this candidate keeps the unreviewed abort-completion bound null so finite absence remains NOT-SCORED; generic request/response suppression is method-only and not scored against CRS-M1-00101 | PACKET-REF<br>PROTOCOL-EVENT<br>OWNERSHIP-RESULT<br>OBSERVATION-ASSESSMENT | score CRS-M1-00101 only when the trigger is a received status file carrying the delay for the same active operation; the abort remains a required fallback rather than a cancellation waiver, an observed abort PASS covers only that fallback-action proposition, and no absence FAIL is admitted while the completion bound is unreviewed and null | CRS-M1-00101 从数据加载器收到携带异常延迟的状态文件开始；到期端点在 DEC-CLOCK 前保持未决，规定中止是无及时新状态时的后备义务而非取消豁免；本候选把未审定的中止完成界限保持为空，因此有限缺失迹继续不计分，已观察中止的 PASS 仅覆盖后备动作命题。 |
| SC-NORMAL-UPLOAD | UPLOAD | SC-NORMAL-UPLOAD<br>APPLICABLE<br>CRS-M1-00077 | AC-EXP-SCENE<br>AC-EXP-CAUSAL<br>AM-EXPERIMENT<br>AM-STATE | no perturbation; qualified upload completion control<br>controlled scene definition plus terminal-status evidence<br>qualified completion evidence; normal singleton does not by itself establish protocol PASS | TRANSFER-RECORD<br>PROTOCOL-EVENT<br>OBSERVATION-ASSESSMENT<br>HISTORY-HANDLE | admit only after scene identity, reset, and observation qualification pass | 正常上传对照仅在场景身份、复位和观测资格齐备时纳入；正常单例本身不等于协议通过。 |
| SC-RESOURCE-ERROR | INFORMATION | SC-RESOURCE-ERROR<br>TOOL-OR-EXPERIMENT-N/A | AC-EXP-SCENE<br>AC-EXP-CAUSAL<br>AC-SYN-RESOURCE-STOP<br>AM-RESOURCE<br>AM-STATE | declared resource controller or tool-error path<br>configuration plus controller record<br>named ERROR/budget exit with all spent cost retained; not IUT nonconformance | INTAKE-METADATA<br>FINDING-RECORD<br>HISTORY-HANDLE | retain every registered attempt and distinguish budget exhaustion from tool error | 资源或工具错误以具名 ERROR 或预算停止退出，保留已花费成本，不归为 IUT 不符合。 |
| SC-SAME-KEY | INFORMATION | SC-SAME-KEY<br>TOOL-OR-EXPERIMENT-N/A | AC-EXP-SCENE<br>AC-EXP-CAUSAL<br>AC-SYN-HISTORY<br>AM-OWNERSHIP<br>AM-HISTORY | concurrent requests sharing a correlation key<br>independent request schedule<br>one owner or explicit ambiguity; no response reuse | PROTOCOL-EVENT<br>OWNERSHIP-RESULT<br>HISTORY-HANDLE | admit only when ambiguity is represented rather than silently resolved | 同键并发请求必须保留唯一归属或显式歧义，不得静默复用响应。 |
| SC-SINGLE-BATCH | UPLOAD | SC-SINGLE-BATCH<br>TOOL-OR-EXPERIMENT-N/A | AC-EXP-SCENE<br>AC-EXP-CAUSAL<br>AC-SYN-SELECT<br>AM-EXPERIMENT<br>AM-HISTORY | registered single-versus-batch selection policy<br>paired controlled scene definitions<br>paired comparison only after independent full reset | TRANSFER-RECORD<br>PROTOCOL-EVENT<br>HISTORY-HANDLE | admit paired units only when configuration differs solely at the registered perturbation | 单项与批量策略只在独立完整复位且除登记扰动外配置相同时进行配对比较。 |
| SC-WAIT-CONTINUE | UPLOAD | SC-WAIT-CONTINUE<br>APPLICABLE<br>CRS-M1-00106<br>CRS-M1-00107 | AC-EXP-SCENE<br>AC-EXP-CAUSAL<br>AC-SYN-HISTORY<br>AM-TIMING<br>AM-STATE | WAIT/continuation event timing and state transition<br>confirmed event script and evaluator timing record<br>WAIT preserves the active obligation until continuation | PROTOCOL-EVENT<br>OBSERVATION-ASSESSMENT<br>HISTORY-HANDLE | admit only when event ownership and both measurement intervals are reconstructable | WAIT 场景验证等待义务持续到继续事件；只有事件归属和两类时间区间可重建时才纳入。 |

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

| Metric / 指标 | Population / 分母总体 | Numerator / 分子总体 | Calculation | Missing + censoring | Required fields / 必需字段 | Controlled Chinese / 受控中文 | Analysis / 分析 | Primary / 主要 |
|---|---|---|---|---|---|---|---|---|
| MET-ABLATION-DELTA | POP-PAIRED-ELIGIBLE | — | within-pair arm difference for each named parent metric | unmatched pairs are reported and not imputed<br>inherits each parent metric censoring rule<br>zero=N/A | pairingId<br>outcome<br>chargedCost | 对每个父指标分别派生合格配对并计算臂内差异；未配对记录保留且不插补。 | AN-PAIRED | no / 否 |
| MET-ABSTAIN | POP-ATTEMPTS | POP-ABSTAIN | abstentions / all attempts | missing validity invalidates row<br>none<br>zero=N/A | validity | 报告全部尝试中的弃权比例，单例幸存者不能覆盖弃权停止。 | AN-FLOW | no / 否 |
| MET-ANSWERED-COVERAGE | POP-ATTEMPTS | POP-ANSWERED | answered attempts / all attempts | missing validity or outcome invalidates the row<br>no censoring; budget and error exits remain in denominator<br>zero=N/A | attemptId<br>validity<br>outcome | 以全部尝试为分母计算有效 PASS/FAIL 覆盖率；预算与错误退出仍在分母中。 | AN-PROPORTION | yes / 是 |
| MET-ATTEMPTS | POP-ATTEMPTS | — | cardinality | missing attemptId invalidates the row<br>none; retain every registered attempt<br>zero=N/A | attemptId | 统计全部唯一登记尝试；排除、未决、弃权、不完整和错误均不得删除。 | AN-FLOW | no / 否 |
| MET-CONDITIONAL-DETECTION-ERROR | POP-ANSWERED-TRUTH-SCORABLE | POP-CONDITIONAL-ERROR | wrong truth-scorable answered decisions / truth-scorable answered attempts | missing evaluator truth routes the answered attempt to MET-TRUTH-MISSING and excludes it only from this truth-scored denominator<br>answered coverage retains every answered attempt; truth scoring uses the explicit scorable subset<br>zero=N/A | validity<br>outcome<br>truthReference.truthHypothesis | 仅在真值可计分的已回答尝试内计算错误决策率；缺失真值转入显式缺失流。 | AN-PROPORTION | yes / 是 |
| MET-COST-VECTOR | POP-ATTEMPTS | — | project detail costs to (acquisition, computation, preparation, retry), folding recovery into preparation once | missing charge field invalidates row<br>include spent cost for incomplete and error exits<br>zero=N/A | chargedCost.acquisition<br>chargedCost.computation<br>chargedCost.preparation<br>chargedCost.recovery<br>chargedCost.retry | 把明细成本投影为采集、计算、准备和重试四维向量；恢复只并入准备一次。 | AN-DISTRIBUTION | yes / 是 |
| MET-ERROR | POP-ATTEMPTS | POP-ERROR | errors / all attempts | missing outcome or validity invalidates row<br>none<br>zero=N/A | validity<br>outcome | 报告错误或无效尝试比例并保留原因，不将其归为 IUT 失败。 | AN-FLOW | no / 否 |
| MET-FALSE-FAIL | POP-QUALIFIED-NORMAL | POP-FALSE-FAILS | valid FAIL / qualified normal controls | unqualified normal controls stay outside this denominator<br>tool errors are not false failures<br>zero=N/A | injectionStatus<br>faultDomain<br>validity<br>outcome | 在合格正常对照中统计有效 FAIL；工具错误不算误报。 | AN-PROPORTION | yes / 是 |
| MET-FINAL-CANDIDATES | POP-LOCALIZATION-ELIGIBLE | — | distribution of len(finalHypotheses) | missing finalHypotheses invalidates row<br>include incomplete and empty exits with stop class<br>zero=N/A | finalHypotheses<br>stopClass | 报告定位合格尝试的最终候选数分布，并连同不完整、空集和停止类别呈现。 | AN-DISTRIBUTION | yes / 是 |
| MET-INCOMPLETE | POP-ATTEMPTS | POP-INCOMPLETE | incomplete or budget-exhausted attempts / all attempts | missing resourceStatus invalidates row<br>right-censored runtime/cost remains visible<br>zero=N/A | validity<br>resourceStatus<br>chargedCost | 报告不完整或预算耗尽尝试，保留部分历史及已发生成本。 | AN-FLOW | no / 否 |
| MET-INCONCLUSIVE | POP-ATTEMPTS | POP-INCONCLUSIVE | inconclusive attempts / all attempts | missing outcome invalidates row<br>interval overlap is retained as inconclusive<br>zero=N/A | outcome<br>observationInterval<br>requirementInterval | 报告闭区间部分重叠导致的不确定结果，不强制归为通过或失败。 | AN-FLOW | no / 否 |
| MET-LOCALIZATION-COVERAGE | POP-LOCALIZATION-ELIGIBLE | POP-LOCALIZATION-DECISION | issued localization decisions / eligible localization attempts | missing decision flag invalidates row<br>empty/error stops remain in eligible denominator<br>zero=N/A | localizationDecisionIssued<br>injectionStatus<br>faultDomain | 在定位合格尝试中计算实际发出定位决策的比例；空集和错误停止留在分母。 | AN-PROPORTION | yes / 是 |
| MET-MISS | POP-CONFIRMED-FAULT | POP-MISSES | valid PASS / confirmed in-domain non-equivalent fault attempts | unconfirmed or unresolved injection is retained outside this denominator<br>budget/error exits remain in fault denominator and are reported separately<br>zero=N/A | injectionStatus<br>faultDomain<br>outcome<br>truthReference.truthHypothesis | 在已确认、域内且非等价故障尝试中统计错误 PASS；错误或预算退出另行报告。 | AN-PROPORTION | yes / 是 |
| MET-ROUNDS | POP-ROUNDS | — | issued actions per ROUNDS-policy run | non-ROUNDS policy is not applicable<br>right-censor at the registered round limit<br>zero=N/A | runId<br>actionIssued<br>resourcePolicy | 仅对按轮数控制且已运行的尝试统计实际发出动作数，并在登记上限处右删失。 | AN-DISTRIBUTION | no / 否 |
| MET-SINGLETON-CORRECT | POP-SINGLETON-TRUTH-SCORABLE | POP-SINGLETON-CORRECT | correct truth-scorable singletons / truth-scorable singleton decisions | missing truth routes the singleton decision to MET-TRUTH-MISSING<br>Stop-645 and budget stops cannot create singleton decisions<br>zero=N/A | singletonDecisionIssued<br>finalHypotheses<br>truthReference.truthHypothesis | 仅在真值可计分的单例决策中计算正确率；645 或预算停止不能制造单例决策。 | AN-PROPORTION | no / 否 |
| MET-TRUE-EXCLUDED | POP-LOCALIZATION-TRUTH-SCORABLE | POP-TRUE-EXCLUDED | truth-scorable decisions excluding truth / truth-scorable localization decisions | missing truth routes the decision to MET-TRUTH-MISSING<br>no-decision attempts are not truth exclusions<br>zero=N/A | truthReference.truthHypothesis<br>finalHypotheses<br>localizationDecisionIssued | 仅在有效且真值可计分的定位决策中计算排除真值比例，并与未决策区分。 | AN-PROPORTION | no / 否 |
| MET-TRUE-RETAINED | POP-LOCALIZATION-TRUTH-SCORABLE | POP-TRUE-RETAINED | truth-scorable decisions retaining truth / truth-scorable localization decisions | missing truth routes the decision to MET-TRUTH-MISSING<br>no-decision and missing-truth attempts remain visible in separate coverage/flow metrics<br>zero=N/A | truthReference.truthHypothesis<br>finalHypotheses<br>localizationDecisionIssued | 仅在有效且真值可计分的定位决策中计算保留真值比例。 | AN-PROPORTION | yes / 是 |
| MET-TRUTH-MISSING | POP-ATTEMPTS | POP-TRUTH-MISSING | truth-missing scored-decision candidates / all attempts | null truth is the event, not row deletion<br>retain attempts in flow and non-truth coverage<br>zero=N/A | truthReference.truthHypothesis<br>outcome<br>localizationDecisionIssued | 以全部尝试为分母显式报告本应计分但真值缺失的记录及原因。 | AN-FLOW | no / 否 |
| MET-TRUTH-SCORABLE-COVERAGE | POP-ANSWERED | POP-ANSWERED-TRUTH-SCORABLE | truth-scorable answered attempts / answered attempts | missing truth remains in the answered denominator<br>no silent removal from answered coverage<br>zero=N/A | outcome<br>validity<br>truthReference.truthHypothesis | 报告已回答尝试中具有可用评估真值的比例，防止真值缺失被静默删除。 | AN-FLOW | no / 否 |

### Metric-field handoff / 指标字段交接

| Field / 字段 | Kind + source / 类型与来源 | Inputs + rule / 输入与规则 | Proposal / 提议 | Producer / 生产者 | Visibility + compatibility / 可见性与兼容性 | Dependency + closure / 依赖与闭合 | Consumers / 使用指标 |
|---|---|---|---|---|---|---|---|
| actionIssued | DERIVED<br>IF-EXP-RUN.traceRef | IF-EXP-RUN.traceRef<br>true only for an admitted action recorded as issued in the run trace | proposal=None | run controller | evaluator and audit<br>existing derived field | DEP-RESOURCE<br>pilot | MET-ROUNDS |
| attemptId | DERIVED<br>IF-EXP-INJECT.injectionAttempt | IF-EXP-INJECT.injectionAttempt<br>extract the immutable registered attempt identity; never infer it from row order | proposal=None | experiment registrar | evaluator and audit<br>existing stable field | DEP-REGISTRATION<br>confirmatory-registration | MET-ANSWERED-COVERAGE<br>MET-ATTEMPTS |
| chargedCost | PROPOSED<br>IF-EXP-COLLECT.resourceLog | IF-EXP-COLLECT.resourceLog<br>project detail charges to acquisition, computation, preparation, recovery, and retry without double counting | proposal=resourceLog.detailCharges | resource controller | evaluator and audit<br>additive field projected to accepted four-vector | DEP-RESOURCE<br>pilot | MET-ABLATION-DELTA<br>MET-INCOMPLETE |
| chargedCost.acquisition | PROPOSED<br>IF-EXP-COLLECT.resourceLog | IF-EXP-COLLECT.resourceLog<br>sum registered acquisition charges once per admitted acquisition | proposal=resourceLog.detailCharges | resource controller | evaluator and audit<br>additive field projected to accepted four-vector | DEP-RESOURCE<br>pilot | MET-COST-VECTOR |
| chargedCost.computation | PROPOSED<br>IF-EXP-COLLECT.resourceLog | IF-EXP-COLLECT.resourceLog<br>sum registered computation charges once per admitted computation | proposal=resourceLog.detailCharges | resource controller | evaluator and audit<br>additive field projected to accepted four-vector | DEP-RESOURCE<br>pilot | MET-COST-VECTOR |
| chargedCost.preparation | PROPOSED<br>IF-EXP-COLLECT.resourceLog | IF-EXP-COLLECT.resourceLog<br>sum preparation charges; recovery is folded only by the metric projection rule | proposal=resourceLog.detailCharges | resource controller | evaluator and audit<br>additive field projected to accepted four-vector | DEP-RESOURCE<br>pilot | MET-COST-VECTOR |
| chargedCost.recovery | PROPOSED<br>IF-EXP-COLLECT.resourceLog | IF-EXP-COLLECT.resourceLog<br>sum registered recovery charges separately before the accepted projection folds them into preparation | proposal=resourceLog.detailCharges | resource controller | evaluator and audit<br>additive field projected to accepted four-vector | DEP-RESOURCE<br>pilot | MET-COST-VECTOR |
| chargedCost.retry | PROPOSED<br>IF-EXP-COLLECT.resourceLog | IF-EXP-COLLECT.resourceLog<br>sum registered retry charges once per charged retry | proposal=resourceLog.detailCharges | resource controller | evaluator and audit<br>additive field projected to accepted four-vector | DEP-RESOURCE<br>pilot | MET-COST-VECTOR |
| faultDomain | PROPOSED<br>IF-EXP-TRUTH.truthRecord | IF-EXP-TRUTH.truthRecord<br>map the independent equivalence disposition to the registered fault-domain class; never read runtime IF-EQUIV | proposal=truthRecord.equivalenceDisposition | fault adjudicator | evaluator-only<br>shared additive evaluator field; never substitutes for runtime IF-EQUIV | DEP-EQUIV<br>confirmatory-registration | MET-FALSE-FAIL<br>MET-LOCALIZATION-COVERAGE<br>MET-MISS |
| finalHypotheses | DERIVED<br>IF-EXP-RUN.traceRef | IF-EXP-RUN.traceRef<br>read the algorithm's terminal candidate set from the attempt trace; never use it as evaluator truth | proposal=None | algorithm under evaluation | evaluator and audit<br>existing algorithm output | DEP-IUT<br>pilot | MET-FINAL-CANDIDATES<br>MET-SINGLETON-CORRECT<br>MET-TRUE-EXCLUDED<br>MET-TRUE-RETAINED |
| injectionStatus | PROPOSED<br>IF-EXP-TRUTH.truthRecord | IF-EXP-TRUTH.truthRecord<br>copy the independently adjudicated injection status; confirmationRef remains a separate evidence reference | proposal=truthRecord.injectionStatus | independent evaluator | evaluator-only<br>additive evaluator field | DEP-TRUTH<br>pilot | MET-FALSE-FAIL<br>MET-LOCALIZATION-COVERAGE<br>MET-MISS |
| localizationDecisionIssued | DERIVED<br>IF-EXP-RUN.traceRef | IF-EXP-RUN.traceRef<br>true only when the trace records a current localization decision | proposal=None | run controller | evaluator and audit<br>existing derived field | DEP-IUT<br>pilot | MET-LOCALIZATION-COVERAGE<br>MET-TRUE-EXCLUDED<br>MET-TRUE-RETAINED<br>MET-TRUTH-MISSING |
| observationInterval | DIRECT<br>OBSERVATION-ASSESSMENT.measurementInterval | OBSERVATION-ASSESSMENT.measurementInterval<br>copy the closed measured interval with its recorded unit and endpoint semantics | proposal=None | observation assessor | algorithm and evaluator<br>existing measurement interval field | DEP-CLOCK<br>pilot | MET-INCONCLUSIVE |
| outcome | DERIVED<br>IF-EXP-RUN.traceRef | IF-EXP-RUN.traceRef<br>IF-EXP-FILTER.validityClass<br>OBSERVATION-ASSESSMENT.verdict<br>normalize each attempt's algorithm/observation verdict after validity filtering into PASS, FAIL, INCONCLUSIVE, ERROR, or NOT-ANSWERED before any metricCells aggregation | proposal=None | evaluation engine | evaluator and audit<br>existing derived attempt field; aggregate metricCells remain downstream | DEP-REGISTRATION<br>confirmatory-registration | MET-ABLATION-DELTA<br>MET-ANSWERED-COVERAGE<br>MET-CONDITIONAL-DETECTION-ERROR<br>MET-ERROR<br>MET-FALSE-FAIL<br>MET-INCONCLUSIVE<br>MET-MISS<br>MET-TRUTH-MISSING<br>MET-TRUTH-SCORABLE-COVERAGE |
| pairingId | PROPOSED<br>IF-EXP-SCENE.sceneRecord | IF-EXP-SCENE.sceneRecord<br>copy the shared registered pair identity; resetEvidenceRef is a distinct per-arm eligibility witness and never supplies this value | proposal=sceneRecord.pairingId | scene controller | evaluator and audit<br>additive field | DEP-RESET<br>pilot | MET-ABLATION-DELTA |
| requirementInterval | PROPOSED<br>IF-EXP-SCENE.sceneRecord | IF-EXP-SCENE.sceneRecord<br>resolve the cited requirement identity to its controlled timing interval, unit, and endpoint semantics; never copy the measured interval | proposal=sceneRecord.requirementInterval | requirements/configuration registrar | algorithm and evaluator<br>additive controlled requirement field | DEP-CLOCK<br>pilot | MET-INCONCLUSIVE |
| resourcePolicy | PROPOSED<br>IF-EXP-COLLECT.resourceLog | IF-EXP-COLLECT.resourceLog<br>copy the pre-registered resource mode for the attempt; never infer it from observed cost | proposal=resourceLog.mode | resource controller | algorithm and evaluator<br>additive field | DEP-RESOURCE<br>pilot | MET-ROUNDS |
| resourceStatus | PROPOSED<br>IF-EXP-COLLECT.resourceLog | IF-EXP-COLLECT.resourceLog<br>classify the attempt resource state from the registered resource log without erasing spent charges | proposal=resourceLog.detailCharges | resource controller | evaluator and audit<br>additive field projected to accepted four-vector | DEP-RESOURCE<br>pilot | MET-INCOMPLETE |
| runId | DIRECT<br>IF-EXP-RUN.runId | IF-EXP-RUN.runId<br>copy the immutable run identity | proposal=None | run controller | evaluator and audit<br>existing stable field | DEP-IUT<br>pilot | MET-ROUNDS |
| singletonDecisionIssued | DERIVED<br>IF-EXP-RUN.traceRef | IF-EXP-RUN.traceRef<br>true only when the trace records a current singleton localization decision | proposal=None | run controller | evaluator and audit<br>existing derived field | DEP-IUT<br>pilot | MET-SINGLETON-CORRECT |
| stopClass | DIRECT<br>IF-EXP-RUN.stopClass | IF-EXP-RUN.stopClass<br>copy the registered terminal stop class without recoding | proposal=None | run controller | evaluator and audit<br>existing stable field | DEP-IUT<br>pilot | MET-FINAL-CANDIDATES |
| truthReference.truthHypothesis | PROPOSED<br>IF-EXP-TRUTH.truthRecord | IF-EXP-TRUTH.truthRecord<br>copy the independently adjudicated hypothesis identity; confirmationRef is evidence only and finalHypotheses is never a truth input | proposal=truthRecord.truthHypothesis | independent evaluator | evaluator-only<br>additive evaluator field | DEP-TRUTH<br>pilot | MET-CONDITIONAL-DETECTION-ERROR<br>MET-MISS<br>MET-SINGLETON-CORRECT<br>MET-TRUE-EXCLUDED<br>MET-TRUE-RETAINED<br>MET-TRUTH-MISSING<br>MET-TRUTH-SCORABLE-COVERAGE |
| validity | DIRECT<br>IF-EXP-FILTER.validityClass | IF-EXP-FILTER.validityClass<br>copy the evaluator validity class without recoding | proposal=None | observation assessor | evaluator and audit<br>existing stable field | DEP-OBS-QUAL<br>design-review | MET-ABSTAIN<br>MET-ANSWERED-COVERAGE<br>MET-CONDITIONAL-DETECTION-ERROR<br>MET-ERROR<br>MET-FALSE-FAIL<br>MET-INCOMPLETE<br>MET-TRUTH-SCORABLE-COVERAGE |

### Analysis decisions / 分析决定

| Plan / 方案 | Estimand | Unit + pairing / 单位与配对 | Estimator + interval | Applicability | Controlled Chinese / 受控中文 | Method status / 方法状态 | Evidence / 方法证据 | Freeze / 冻结决定 |
|---|---|---|---|---|---|---|---|---|
| AN-DISTRIBUTION | distribution of survivor count, cost, or rounds | registered scene attempt or independently reset run as explicitly registered<br>use paired/clustered branch when scenes or seeds are shared; never infer independence from row count | finite empirical distribution and descriptive registered contrasts<br>WAIT-DEC-SAMPLE until randomness and the independent/resampling unit are established and a method is named<br>PAIRED-OR-CLUSTERED / 配对或聚类<br>WAIT-DEC-SAMPLE / 等待样本量决定 | count/cost metrics; no automatic large-sample, paired, or bootstrap assumption | 候选数、成本和轮数只给经验分布及描述性对比；随机性与独立单位未确定前不选区间法。 | METHOD-WAIT | EVID-2026-063<br>EVID-2026-064<br>EVID-2026-065<br>lineEnd=1023; lineStart=1021; path=docs/research/methodology/RR-2026-001_test_analysis_conformance_methodology.md; role=CONTEXT-ONLY | DEC-SAMPLE |
| AN-FLOW | finite attempt-flow proportion or count | attempt<br>none | finite count and empirical proportion<br>descriptive finite enumeration only; no inferential interval is selected<br>FLOW-ONLY / 仅流程描述<br>WAIT-DEC-SAMPLE / 等待样本量决定 | flow and coverage metrics | 流量指标只作有限集合计数与经验比例描述，不选择总体推断区间。 | DESCRIPTIVE-ONLY | EVID-2026-064<br>EVID-2026-065<br>lineEnd=1023; lineStart=1021; path=docs/research/methodology/RR-2026-001_test_analysis_conformance_methodology.md; role=CONTEXT-ONLY | DEC-SAMPLE |
| AN-PAIRED | within-scene ablation change in a named parent metric | registered pair-parent-metric unit<br>same base scene/seed/construction, one registered contrast, reciprocal arms, distinct confirmed resets, and derived parent-population membership | descriptive paired difference on the named parent metric scale<br>WAIT-DEC-SAMPLE until between-pair independence or clustering is established and a direct paired/clustered method source is named<br>PAIRED-OR-CLUSTERED / 配对或聚类<br>WAIT-DEC-SAMPLE / 等待样本量决定 | only when every structural and parent-specific eligibility field is derived from evidence | 按场景、种子、构造、注册对比、复位与父指标成员资格派生配对；推断方法与区间等待 DEC-SAMPLE。 | METHOD-WAIT | EVID-2026-063<br>EVID-2026-064<br>EVID-2026-065<br>lineEnd=1023; lineStart=1021; path=docs/research/methodology/RR-2026-001_test_analysis_conformance_methodology.md; role=CONTEXT-ONLY | DEC-SAMPLE |
| AN-PROPORTION | finite-population decision or error proportion | registered scene attempt<br>independent only after scene/seed and shared-run clustering are excluded | empirical proportion; Clopper-Pearson is the named candidate only for verified independent Bernoulli attempts<br>Clopper-Pearson only under the documented i.i.d. Bernoulli conditions; otherwise WAIT-DEC-SAMPLE<br>INDEPENDENT-RANDOMIZED / 独立随机<br>WAIT-DEC-SAMPLE / 等待样本量决定 | binary metrics with nonzero denominator, verified independent random assignment, and branch inputs frozen before held-out access | Clopper-Pearson 仅作为独立同分布伯努利尝试的具名候选；不满足独立性时等待 DEC-SAMPLE。 | NAMED-CANDIDATE | EVID-2026-063<br>EVID-2026-064<br>EVID-2026-065<br>anchorId=SRC-ANCHOR-BERNOULLI-EXACT-INTERVAL; excerptSha256=55215e23ca1ae18f01ed40dd8bc68c6c9e02cb0b3a521569c28368bf35e13dc2; lineEnd=1019; lineStart=995; path=docs/research/methodology/RR-2026-001_test_analysis_conformance_methodology.md; role=DIRECT | DEC-SAMPLE |

### Comparison families / 比较族

| Family / 比较族 | Class / 类别 | Metrics / 指标 | Contrasts | Joint conclusion | Multiplicity | Controlled Chinese / 受控中文 |
|---|---|---|---|---|---|---|
| CF-EXPLORATORY | EXPLORATORY / 探索性 | MET-ABLATION-DELTA | registered within-scene CL-LOOP versus comparator ablation pair | hypothesis-generating only unless parent estimand and family role are preregistered | label exploratory unless its parent estimand and multiplicity treatment are frozen before held-out access | 消融配对仅用于生成假设，除非其父估计目标和多重性处理在访问留出数据前完成登记。 |
| CF-PRIMARY | PRIMARY / 主要 | MET-ANSWERED-COVERAGE<br>MET-CONDITIONAL-DETECTION-ERROR<br>MET-MISS<br>MET-FALSE-FAIL<br>MET-LOCALIZATION-COVERAGE<br>MET-TRUE-RETAINED<br>MET-FINAL-CANDIDATES<br>MET-COST-VECTOR | EXP-CLTAV-DETECT: CL-LOOP versus CL-T<br>EXP-CLTAV-LOCATE: CL-LOOP versus CL-T<br>EXP-CLTAV-LOCATE: CL-LOOP versus CL-TA | no primary superiority conclusion unless the registered detection/localization benefit and cost/coverage safeguards jointly hold | DEC-SAMPLE must freeze one family-wise procedure before held-out access; until then report estimates and uncertainty without confirmatory rejection claims | 主要比较只有在登记的检测或定位收益与成本、覆盖率保障共同成立时才能支持优势结论；多重性方案须预先冻结。 |
| CF-SECONDARY | SECONDARY / 次要 | MET-ABSTAIN<br>MET-INCONCLUSIVE<br>MET-ERROR<br>MET-INCOMPLETE<br>MET-TRUE-EXCLUDED<br>MET-SINGLETON-CORRECT<br>MET-TRUTH-SCORABLE-COVERAGE<br>MET-TRUTH-MISSING<br>MET-ROUNDS | same registered arm contrasts as CF-PRIMARY where the metric applies | supports interpretation and failure-mode accounting but cannot replace a failed primary safeguard | descriptive with interval estimates; no confirmatory multiplicity claim | 次要指标用于解释失败模式和真值可用性，不能替代未通过的主要保障。 |

### Engineering dependencies / 工程依赖

| Dependency / 依赖 | Consumers / 使用方 | Current ref / 当前引用 | Evidence + producer | State + typed proposal / 状态与类型化提议 | Decisions / 决定 | Closure + follow-up | Controlled Chinese / 受控中文 | Milestone / 里程碑 |
|---|---|---|---|---|---|---|---|---|
| DEP-645-RUNTIME | EXP-CLTAV-ABLATION | kind=authority-binding; ref=ARINC-645 candidate source and semantic binding | implemented and independently checked CRC/check-value/naming oracle<br>future authorized engineering change | RUNTIME-PENDING<br>findingRecord.oracleRef (string; evaluator and audit) | DEC-IUT | independent vectors and oracle evidence; source presence alone is insufficient<br>separate engineering CR if this cell is retained | 需由后续授权工程变更实现并独立核验 ARINC 645-1 的 CRC、校验值与命名 oracle；仅有来源绑定不建立这些能力。 | 645-specific-run |
| DEP-CLOCK | SC-WAIT-CONTINUE<br>SC-NO-RESPONSE<br>SC-INVALID-OBS | kind=record-field; ref=OBSERVATION-ASSESSMENT.measurementInterval | clock chain, error budget, and independently registered requirement interval<br>test environment owner | RUNTIME-PENDING<br>observationAssessment.clockChainRef (string; algorithm and evaluator)<br>sceneRecord.requirementInterval (closed interval with requirement identity, unit, and endpoint semantics; algorithm and evaluator) | DEC-CLOCK | calibration evidence reproduces the observation interval and a distinct cited requirement contract reproduces the requirement interval<br>qualify the clock, freeze the error budget, and register requirement interval provenance | 需建立可复现的时钟链、区间和端点规则，并由计量审查者确认。 | pilot |
| DEP-EQUIV | MET-MISS<br>MET-ABLATION-DELTA | kind=contrast-only-algorithm-interface; ref=IF-EQUIV.established | evaluator-side equivalenceDisposition distinct from runtime candidate equivalence<br>named fault adjudicator | PROPOSED-CONTRACT-DELTA<br>truthRecord.equivalenceDisposition (enum[confirmed-equivalent,confirmed-non-equivalent,unresolved]; evaluator-only) | DEC-EQUIV | one evaluator field yields equivalent, non-equivalent or unresolved accounting without reusing runtime IF-EQUIV<br>approve evaluator adjudication procedure | 等价性由评估者按影响证据裁定，且不得改写运行时 IF-EQUIV 语义。 | confirmatory-registration |
| DEP-IUT | SC-NORMAL-UPLOAD<br>SC-WAIT-CONTINUE<br>SC-NO-RESPONSE<br>SC-ABORT<br>SC-SAME-KEY<br>SC-SINGLE-BATCH<br>SC-RESOURCE-ERROR | kind=experiment-plan-section; ref=EXP-PLAN-2026-001:prerequisites | interactive IUT identity, behavior boundary, and reviewed safe initial projection<br>project owner and later authorized implementer | PROPOSED-CONTRACT-DELTA<br>sceneRecord.iutIdentity (string; evaluator and audit)<br>IF-EXP-SCENE.algorithmVisibleFields (object; all arms through an exact member allowlist)<br>member sceneId:string [ALGORITHM-INITIAL]<br>member serviceScope:enum [ALGORITHM-INITIAL]<br>member registeredArm:enum [ALGORITHM-INITIAL]<br>member resourceMode:enum [ALGORITHM-INITIAL]<br>member publicConfigurationRef:reference [ALGORITHM-INITIAL]<br>forbidden faultPlan<br>forbidden truthSource<br>forbidden injectionConfirmed<br>forbidden validityClass<br>forbidden equivalenceDisposition<br>forbidden posthocAdjudication | DEC-IUT | reviewed IUT/configuration identity resolves and leakage test proves the exact typed projection contains no evaluator-only member<br>select IUT and approve the typed initial-field allowlist and denylist | 需确定交互式 IUT 身份与行为边界，并审核严格类型化的算法可见初始投影及禁入成员。 | pilot |
| DEP-OBS-QUAL | SC-INVALID-OBS<br>MET-ERROR | kind=record-field; ref=OBSERVATION-ASSESSMENT.verdict | qualification policy separating capture/tool error from IUT verdict<br>observation assessor | EXISTING-REFERENCE | DEC-CLOCK | invalid timestamp/ownership witness produces ERROR without IUT blame<br>retain accepted qualification semantics | 观测资格必须覆盖捕获完整性、时间、归属与重建状态，并能重放审计。 | design-review |
| DEP-REGISTRATION | EXP-CLTAV-DETECT<br>EXP-CLTAV-LOCATE<br>EXP-CLTAV-ABLATION | kind=experiment-plan; ref=EXP-PLAN-2026-001 | frozen confirmatory registration<br>experiment registrar and named scientific reviewer | HUMAN-PENDING | DEC-MATH-REVIEW<br>DEC-IUT<br>DEC-TRUTH<br>DEC-EQUIV<br>DEC-SAMPLE<br>DEC-RESOURCE<br>DEC-CLOCK | registration committed before confirmatory runs<br>freeze units, budgets, denominators, adjudication and analysis | 运行前冻结身份、臂、场景、指标、分析和权威输入，漂移即阻止确认性使用。 | confirmatory-run |
| DEP-RESET | SC-NORMAL-UPLOAD<br>SC-SINGLE-BATCH | kind=experiment-interface; ref=IF-EXP-SCENE.sceneRecord | shared pair identity plus distinct per-arm reset identifier and success evidence<br>scene controller | PROPOSED-CONTRACT-DELTA<br>sceneRecord.pairingId (string; evaluator and audit)<br>sceneRecord.resetId (string; all arms and evaluator)<br>sceneRecord.resetEvidenceRef (string; evaluator and audit) | DEC-IUT | paired rows share pairingId while each arm has a distinct independently confirmed resetEvidenceRef<br>define pair identity and separate reset evidence fields | 每次配对运行须有独立、可确认且互异的完整复位证据。 | pilot |
| DEP-RESOURCE | SC-RESOURCE-ERROR<br>MET-COST-VECTOR<br>MET-ROUNDS | kind=algorithm-interface; ref=IF-RESOURCE-STOP.trace | exclusive resource mode and actual charge log<br>runtime resource controller | RUNTIME-PENDING<br>resourceLog.mode (enum; algorithm and evaluator)<br>resourceLog.detailCharges (cost-detail; evaluator and audit) | DEC-RESOURCE | one charge per issued action, recovery folded once into preparation, and named exhaustion<br>implement charge trace without changing accepted cost semantics | 每会话只登记 BUDGET 或 ROUNDS 一种资源模式，重试上限作为独立安全约束。 | pilot |
| DEP-SAMPLE | MET-ANSWERED-COVERAGE<br>MET-MISS<br>MET-TRUE-RETAINED<br>MET-ABLATION-DELTA | kind=placeholder; ref=PH-STAT-N | precision/effect target or finite census basis plus pilot variance/prevalence<br>named scientific reviewer | HUMAN-PENDING | DEC-SAMPLE | sample size, repeat policy, comparison family, and multiplicity role frozen before held-out access<br>run non-confirmatory pilot then decide | 须根据总体、随机化、重复政策、独立单位与试点变异确定样本和方法。 | confirmatory-registration |
| DEP-TRUTH | MET-MISS<br>MET-FALSE-FAIL<br>MET-CONDITIONAL-DETECTION-ERROR<br>MET-TRUE-RETAINED<br>MET-TRUE-EXCLUDED<br>MET-SINGLETON-CORRECT<br>MET-TRUTH-SCORABLE-COVERAGE<br>MET-TRUTH-MISSING | kind=experiment-interface; ref=IF-EXP-TRUTH.truthRecord | confirmed injection and evaluator-only adjudicated truth<br>independent evaluator | PROPOSED-CONTRACT-DELTA<br>truthRecord.confirmationRef (string; evaluator-only)<br>truthRecord.truthHypothesis (string\|null; evaluator-only)<br>truthRecord.injectionStatus (enum[confirmed,normal,equivalent,unconfirmed,unresolved]; evaluator-only)<br>truthRecord.equivalenceDisposition (enum[confirmed-equivalent,confirmed-non-equivalent,unresolved]; evaluator-only) | DEC-TRUTH<br>DEC-EQUIV | truth leakage review plus independent confirmation witness and explicit truth-scorable population audit<br>approve generator/adjudicator separation and missing-truth accounting | 独立评估者提供确认注入和仅评估者可见的裁定真值；试点前须完成泄漏与缺失真值审计。 | pilot |

### Interpretation/update decision relation / 解释与更新决定关系

| Interpretation / 解释 | Update source / 更新来源 | Update status / 更新状态 | Preserve history / 保留历史 | Current decision / 当前决定 |
|---|---|---|---|---|
| ACCEPTED | CURRENT-QUALIFIED-INTERPRETATION | VALID-UPDATE | no / 否 | yes / 是 |
| NOT-EVALUATED | NO-CURRENT-UPDATE | NO-UPDATE | yes / 是 | no / 否 |
| REJECTED | NO-CURRENT-UPDATE | NOT-APPLIED-ERROR | yes / 是 | no / 否 |

| Walkthrough / 走查 | Interpretation / 解释 | Update source / 更新来源 |
|---|---|---|
| SYN-BUDGET | ACCEPTED | CURRENT-QUALIFIED-INTERPRETATION |
| SYN-EQUIVALENT | NOT-EVALUATED | NO-CURRENT-UPDATE |
| SYN-FAIL-NONSINGLETON | ACCEPTED | CURRENT-QUALIFIED-INTERPRETATION |
| SYN-INVALID-OBS | REJECTED | NO-CURRENT-UPDATE |
| SYN-NORMAL | ACCEPTED | CURRENT-QUALIFIED-INTERPRETATION |
| SYN-PAIR-COMPARATOR | ACCEPTED | CURRENT-QUALIFIED-INTERPRETATION |
| SYN-PRE-ACTION | NOT-EVALUATED | NO-CURRENT-UPDATE |
| SYN-STOP-645 | ACCEPTED | CURRENT-QUALIFIED-INTERPRETATION |
| SYN-STOP-EMPTY | ACCEPTED | CURRENT-QUALIFIED-INTERPRETATION |
| SYN-T5-OVERLAP | ACCEPTED | CURRENT-QUALIFIED-INTERPRETATION |
| SYN-TRUE-EXCLUDED | ACCEPTED | CURRENT-QUALIFIED-INTERPRETATION |
| SYN-UNCONFIRMED | NOT-EVALUATED | NO-CURRENT-UPDATE |
| SYN-UNRESOLVED | NOT-EVALUATED | NO-CURRENT-UPDATE |

### Hypothetical method-choice walkthroughs / 假设性方法选择见证

| Choice / 选择 | Label / 标签 | Inputs / 输入 | Branch / 分支 | Result / 结果 | Rationale / 理由 |
|---|---|---|---|---|---|
| CHOICE-CENSUS | HYPOTHETICAL-NOT-RESULT / 假设示例，非结果 | COMPLETE<br>UNKNOWN<br>NONE<br>pair=False<br>cluster=False<br>unit=UNKNOWN | DETERMINISTIC-EXHAUSTIVE / 确定性穷举 | CANDIDATE-METHOD / 候选方法 | A completely enumerated registered finite domain uses finite counts/proportions without a superpopulation claim. |
| CHOICE-CLUSTERED | HYPOTHETICAL-NOT-RESULT / 假设示例，非结果 | INCOMPLETE<br>NOT-INDEPENDENT<br>CLUSTERED<br>pair=False<br>cluster=True<br>unit=CLUSTER | PAIRED-OR-CLUSTERED / 配对或聚类 | CANDIDATE-METHOD / 候选方法 | Repeated attempts within a registered cluster use the cluster as the independent unit; this does not manufacture pair evidence. |
| CHOICE-INDEPENDENT | HYPOTHETICAL-NOT-RESULT / 假设示例，非结果 | INCOMPLETE<br>INDEPENDENT<br>NONE<br>pair=False<br>cluster=False<br>unit=ATTEMPT | INDEPENDENT-RANDOMIZED / 独立随机 | CANDIDATE-METHOD / 候选方法 | Independent randomized scene attempts permit the registered independent-sample candidate, subject to DEC-SAMPLE. |
| CHOICE-PAIRED | HYPOTHETICAL-NOT-RESULT / 假设示例，非结果 | INCOMPLETE<br>NOT-INDEPENDENT<br>PAIRED<br>pair=True<br>cluster=False<br>unit=PAIR | PAIRED-OR-CLUSTERED / 配对或聚类 | CANDIDATE-METHOD / 候选方法 | Shared scenes with reciprocal arms and confirmed reset evidence establish a pair unit; DEC-SAMPLE must still name any inferential method. |
| CHOICE-WAIT | HYPOTHETICAL-NOT-RESULT / 假设示例，非结果 | UNKNOWN<br>UNKNOWN<br>UNKNOWN<br>pair=False<br>cluster=False<br>unit=UNKNOWN | NONE | WAIT-DEC-SAMPLE / 等待样本量决定 | Missing domain, independence and pairing inputs stops method selection; this is not a power calculation or observed result. |

### CRS-M1-00101 protocol timelines / CRS-M1-00101 协议时间线

| Timeline / 时间线 | Trigger / 触发 | Observed / 观测 | Elapsed / 经过时间 | Expiry / 到期端点 | Abort duty / 中止义务 | Finite observation / 有限观察终点 | Outcome / 结果 |
|---|---|---|---|---|---|---|---|
| TL-ABORT-AFTER-DELAY | actor=DATA-LOADER; event=RECEIVED-STATUS-WITH-EXCEPTION-DELAY; exceptionDelaySeconds=10; operationKey=OP-02 | event=ABORT; operationKey=OP-02; requiredFallback=yes / 是 | 11 | UNRESOLVED | REQUIRED-IF-NO-TIMELY-STATUS<br>completionBound=None | end=11<br>qualified=True | PASS |
| TL-GENERIC-SUPPRESSION | actor=GENERIC-REQUESTER; event=REQUEST-SENT; exceptionDelaySeconds=10; operationKey=OP-04 | event=NONE; operationKey=OP-04; requiredFallback=no / 否 | 11 | UNRESOLVED | NOT-APPLICABLE<br>completionBound=None | end=11<br>qualified=True | NOT-SCORED |
| TL-MISSING-BOTH | actor=DATA-LOADER; event=RECEIVED-STATUS-WITH-EXCEPTION-DELAY; exceptionDelaySeconds=10; operationKey=OP-03 | event=NONE; operationKey=OP-03; requiredFallback=no / 否 | 11 | UNRESOLVED | REQUIRED-IF-NO-TIMELY-STATUS<br>completionBound=None | end=11<br>qualified=True | NOT-SCORED |
| TL-STATUS-AT-EXPIRY | actor=DATA-LOADER; event=RECEIVED-STATUS-WITH-EXCEPTION-DELAY; exceptionDelaySeconds=10; operationKey=OP-05 | event=NEW-STATUS; operationKey=OP-05; requiredFallback=no / 否 | 10 | UNRESOLVED | REQUIRED-IF-NO-TIMELY-STATUS<br>completionBound=None | end=10<br>qualified=True | NOT-SCORED |
| TL-STATUS-WITHIN-DELAY | actor=DATA-LOADER; event=RECEIVED-STATUS-WITH-EXCEPTION-DELAY; exceptionDelaySeconds=10; operationKey=OP-01 | event=NEW-STATUS; operationKey=OP-01; requiredFallback=no / 否 | 8 | UNRESOLVED | REQUIRED-IF-NO-TIMELY-STATUS<br>completionBound=None | end=8<br>qualified=True | PASS |

### Open decisions / 待定决定

| Decision / 决定 | Owner / 负责人 | Inputs | Procedure | Freeze / 冻结点 | Closure witness | Controlled Chinese / 受控中文 |
|---|---|---|---|---|---|---|
| DEC-CLOCK | test environment owner and metrology reviewer | clock accuracy, synchronization, timestamp path, and JCGM 100/106-informed error budget | construct and independently reproduce the interval; freeze endpoint inclusivity and overlap rule | pilot | clock-chain report, calibration reference, and interval replay | 依据校准和误差预算冻结各合同的端点开闭性与重叠规则；校准不得改写规范端点，未审定的中止完成界限保持为空。 |
| DEC-DISCLOSURE | corresponding author | author declarations | collect each declaration and reconcile it with the manuscript checklist | submission | completed disclosure checklist | 通讯作者按期刊与机构要求核对作者、单位、经费、许可和 AI 披露。 |
| DEC-EQUIV | named fault adjudicator | fault-specific evaluator record plus impact evidence | two-stage impact screen and named human adjudication with unresolved allowed | confirmatory registration | adjudication form and population-flow rule | 指定裁定者按两阶段影响筛选给出等价、非等价或未决结论，并保留未决流。 |
| DEC-IUT | project owner | identity, access, controllability, configuration and reset evidence | score candidates against scenario access and independent reset | pilot | versioned IUT/configuration identity plus reset demonstration | 项目负责人选择 IUT、版本、配置与安全投影，并以可复现身份清单关闭。 |
| DEC-MATH-REVIEW | independent mathematical reviewer | argument table and minimum counterexample witnesses | record proposition-by-proposition disposition and any counterexample | design acceptance | signed review record naming accepted propositions | 数学审查者核对 C1、C2 的有界命题、假设和反证条件，并留下签署记录。 |
| DEC-RESOURCE | experiment owner and runtime implementer | pilot charge traces, feasible resource envelope and retry-safety evidence | project detail charges to the accepted four-vector, test no-double-charge, select exactly one session mode, then register a separate retry cap that reports execution error without creating another Stop-Budget mode | confirmatory registration | versioned single-mode budget table, retry-cap rule and passing charge-accounting witness | 依据试点收费轨迹选择唯一资源模式，并以成本核算见证和独立重试上限关闭。 |
| DEC-SAMPLE | named scientific reviewer | estimand, precision/effect target, pilot information and dependence structure | select experimental unit and repeat policy first, then compute or justify N and comparison-family treatment | confirmatory registration | registered N/repeats table and statistical review sign-off | 先冻结实验单位、随机性、重复和依赖结构，再确定样本量、比较族与统计方法。 |
| DEC-TRUTH | named evaluator | confirmation and common-error analysis | document independence and run a deliberate disagreement witness | pilot | truth-source protocol and leakage review | 指定评估者选择独立真值协议，通过故意分歧见证和泄漏审查关闭。 |

### Synthetic accounting witness / 合成记账见证

| Attempts / 尝试 | Answered / 已回答 | Coverage / 覆盖 | Conditional error / 条件错误 | Localization coverage / 定位覆盖 | Projected cost / 投影成本 | Review/setup / 评审准备工作量 |
|---|---|---|---|---|---|---|
| 13 | 4 | 4/13 | 0/4 | 3/6 | acquisition=9; computation=8; preparation=3; retry=1 | 3.0 |

<!-- experiment-design-shared:end -->

## 4. Experimental unit, retention, and reset / 实验单位、保留与复位

One registered attempt on one base scene, arm, and fault/control construction is
the experimental unit. `attemptId` is the all-ledger de-duplication key; a
`runId` exists only after admission. Packets, events, timestamps, hypotheses,
and repeated fields are observations within an attempt, not independent samples.
Paired rows share a non-null `pairingId`, base scene, seed, construction ID, and
registered contrast, and require distinct independently confirmed resets.
Eligibility is derived separately for each named parent metric; loss of a
truth-scored parent does not erase an otherwise valid cost pair. Unmatched pairs
remain visible and are never imputed.

一个基础场景、一个比较臂及一种故障／控制构造上的一次登记尝试构成实验单位。
`attemptId` 用于全台账去重；只有通过准入后才有 `runId`。包、事件、时间戳、假设及
重复字段是尝试内观测，不是独立样本。配对行必须共享非空 `pairingId`、基础场景、种子、
构造标识和注册对比，并具有互异且独立确认的复位证据。资格按每个父指标分别派生；
失去真值计分资格不能抹去仍然有效的成本配对。缺失配对不插补并保持可见。

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

The initial algorithm-visible projection is an exact typed member allowlist:
`sceneId`, `serviceScope`, `registeredArm`, `resourceMode`, and
`publicConfigurationRef`, all in role `ALGORITHM-INITIAL`. Evaluator fields such
as fault plan, truth source, injection confirmation, validity, equivalence, and
post-hoc adjudication remain explicitly forbidden inside the projection, not
merely hidden by an outer object name.

算法初始可见投影采用精确的成员级类型白名单，仅含 `sceneId`、`serviceScope`、
`registeredArm`、`resourceMode` 与 `publicConfigurationRef`，角色均为
`ALGORITHM-INITIAL`。故障计划、真值来源、注入确认、有效性、等价性和事后裁定在
投影内部也被显式禁止，不能只靠外层对象改名隔离。

## 6. Finite populations, stops, and interval witness / 有限总体、停止与区间见证

Metric populations are derived from row fields, not handwritten denominator
tags. A valid answered decision is exactly `validity == VALID` with outcome
`PASS` or `FAIL`; `ERROR`, `INCONCLUSIVE`, and `NOT-ANSWERED` are not answered.
Thus zero answers among thirteen attempts gives answered coverage `0/13`, while
conditional detection error is `N/A` because its denominator is empty.

Truth-bearing metrics use explicit scorable subsets. Missing truth leaves an
attempt in answered or localization-decision coverage, routes it to
`POP-TRUTH-MISSING`, and removes it only from the applicable truth-scored
denominator. It may never disappear silently.

指标总体由行字段推导，不使用手填分母标签。只有 `validity == VALID` 且结果为
`PASS` 或 `FAIL` 才算已回答；`ERROR`、`INCONCLUSIVE` 与 `NOT-ANSWERED` 均不算。
因此十三次尝试中零次回答时，回答覆盖率为 `0/13`，而条件检测错误率因分母为空为
`N/A`。

需要真值的指标使用显式可计分子集。真值缺失时，尝试仍保留在已回答覆盖率或定位决策
覆盖率中，同时进入 `POP-TRUTH-MISSING`，只从相应真值计分分母中移出，绝不能静默消失。

Update disposition is evaluated before the mutable stop label. A
`NOT-APPLIED-ERROR` preserves the preceding set `H` regardless of its stop tag.
A `VALID-UPDATE` must equal the registered compatibility intersection and be a
subset of `H`; an empty result forces post-update `Stop-Empty`, while a singleton
forces `Stop-Singleton`, before `Stop-645`, budget, or other exits are considered.
`Stop-Budget` preserves the valid partial set and spent cost but cannot manufacture
a singleton decision. Pre-action admission failure issues no action and charges no
action cost.

先判定更新处置，再读取可修改的停止标签。`NOT-APPLIED-ERROR` 无论标签为何都必须保留
更新前集合 `H`。`VALID-UPDATE` 必须等于登记的相容交集且为 `H` 的子集；空集先强制
`Stop-Empty`，单例先强制 `Stop-Singleton`，之后才考虑 `Stop-645`、预算等退出。
`Stop-Budget` 保留有效部分集合和已花成本，但不能制造单例决定；动作前准入失败不得
发出动作或计动作成本。

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
confirmatory access. The finite choice routine derives its branch from the
recorded inputs. Independent selection requires independent random assignment,
no dependence, and attempt as the independent unit. Paired selection requires
pair evidence and pair as the unit; clustered selection separately requires
cluster evidence and cluster as the unit. Missing or inconsistent inputs return
`WAIT-DEC-SAMPLE`. Only the independent Bernoulli branch currently names
Clopper--Pearson from an exact bound source range; paired and clustered inference
remain method-wait. Its examples are hypothetical,
not power calculations, pilots, or results. `EVID-2026-063`--`065` support conditional use of independent
runs, censoring-aware reporting, effect sizes, and transparent raw results; they
do not prescribe a universal repeat count. JCGM 100/106 guide the open clock and
measurement-error decision but do not themselves validate this apparatus.

有限选择程序根据已记录输入推导分支。独立分支要求独立随机分配、无依赖且独立单位为
尝试；配对分支要求配对证据且单位为配对；聚类分支另行要求聚类证据且单位为聚类。
输入缺失或不一致时返回 `WAIT-DEC-SAMPLE`。当前只有独立伯努利分支依据精确绑定行号
列出 Clopper--Pearson 候选；配对与聚类推断仍保持等待方法状态。

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
