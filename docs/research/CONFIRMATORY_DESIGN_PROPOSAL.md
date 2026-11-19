# Confirmatory design proposal (SIMULATED-IUT, no run)

| Field | Value |
|---|---|
| Artifact | CONFIRMATORY_DESIGN_PROPOSAL |
| Status | DRAFT / HYPOTHETICAL-NOT-RESULT |
| IUT | local simulated 615A bound model (DEC-IUT closed, CR-2026-027 / DD-051) |
| Authority | WO-CLTAV-CONFIRMATORY-DESIGN-2026-011; user rulings U2–U4 (2026-11-18); user decision S1 (RR-PR29-2026-001) |
| Machine grid | `configs/research/cltav_confirmatory_design_draft_v1.json` |
| Hypothesis model | v1 unchanged; confirmatory matching uses `configs/research/cltav_confirmatory_hypothesis_model_v2.json` |
| Not | census, confirmatory run, `registration.yaml` freeze, manuscript fill |

This document proposes a confirmatory *design*. No cell in this file is an
observed result. Every statement about discrimination, error rates, cost, or
arm ranking is a **hypothesis**. The R1 rule is retained: a mixed VALID set
that still contains `h_normal` and has no T5 interval is `INCONCLUSIVE`.

## User decision S1 (visible intervals)

S1 is a user decision on the algorithm-visible interface. It does **not**
close DEC-CLOCK. The proposal implements option **C1** as a subset rule on
the already-accepted simulated T5 instrument:

- Arms see only the measured `observationInterval` (`tick ± ε`, plus
  `observationJitterS`). Exact simulator ticks are evaluator-only.
- LATE / in-window / INCONCLUSIVE follow T5 (`clock.t5_interval_verdict`,
  EXP-PLAN-2026-001): `I_obs ⊆ I_r` is in-window; disjoint is LATE;
  overlap-not-subset is INCONCLUSIVE.
- For FIND-ANSWER versus CRS-M1-00391 closed `[0, 2]`, those three T5
  topologies map to observation classes `FIND-ANSWER`, `FIND-ANSWER-LATE`,
  and `FIND-ANSWER-BOUNDARY`. The last is **not** a protocol event name.
- N4 timing metrics still use evaluator exact ticks or the observation
  endpoint.
- Pilot census artefacts were produced under the pre-S1 tick-visible
  interface and are **not** regenerated here.

DEC-CLOCK remains OPEN. C2 and C3 stay listed. Simulated `ε` is still not a
laboratory error budget.

Variation is **not** N identity repeats and **not** unseeded randomness. The
pilot census (PR #28, Head `cd0ca25c28adfe42eb22622116af66ab2a0e9010`) showed
zero outcome variance at N=3 on a deterministic simulated IUT. Confirmatory
variation, if ever run, would come from parameterised faults and multiple base
scenes (U2).

## Variation axes and grids

Each timing axis names a requirement interval and an observation end. Endpoint
inclusivity is not frozen (DEC-CLOCK remains OPEN).

| Axis | Kind | Parent / key | Requirement interval | Observation end | Grid |
|---|---|---|---|---|---|
| AX-BASE-SCENE | base scene | public scene ids | n/a | n/a | SC-NORMAL-UPLOAD, SC-WAIT-CONTINUE, SC-ABORT, SC-SINGLE-BATCH, SC-NO-RESPONSE, SC-SAME-KEY, SC-RESOURCE-ERROR, SC-INVALID-OBS |
| AX-FIND-ANSWER-TICK | timing | F-FIND-ANSWER-LATE / `findAnswerAtS` | CRS-M1-00391 closed `[0, 2]` s | FIND family `2201/1000` s (`2 + ε + margin`) so a late FIND-ANSWER in `(2, end)` stays a FIND-ANSWER, not an absence | `2002/1000` (just outside), `41/20` (pilot default late), `21/10` (mid), `11/5` (near end) |
| AX-STATUS-SILENCE-UNTIL | timing | F-STATUS-SILENCE / `statusSilenceUntilS` | CRS-M1-00106 `exceptionDelaySeconds=10` | INFORMATION family `10201/1000` s | `10`, `10002/1000`, `10201/1000` (pilot default) |
| AX-LUR-ACK-TICK | timing | H-NORMAL / `lurAckAtS` | CRS-M1-00366 matching ACK **presence** after LUR WRQ; numeric ACK deadline is **not** frozen | none declared | `1/50`, `1/5`, `1` (ACK still present; kind `LUR-ACK`) — normal timing perturbation, truth h_normal (CR-2026-029) |
| AX-OBS-JITTER | observation perturbation | `observationJitterS` | declared simulated `ε = 1/1000` s | n/a | `±1/500` (`±2ε`) applied only to algorithm-visible `observationInterval` |
| AX-FIND-OBS-END | observation end | F-FIND-ANSWER-ABSENT / `findObservationEndS` | CRS-M1-00391 `[0, 2]` | short window `2` s vs default `2201/1000` s | `FIND-END-DEADLINE`, `FIND-END-DEFAULT` |

Faults still change only timing, presence, or order. Visible kinds remain in
the existing protocol whitelist. Truth access is unchanged (evaluator store +
capability; arms never receive truth).

## Harder in-domain cases (hypotheses)

Declared in the catalogue (`harderCases`) and visible to arms only through
protocol events.

| Id | Construction | Hypothesized stress |
|---|---|---|
| HC-FIND-ENDPOINT | LATE with `findAnswerAtS = 2` (requirement endpoint) | Under S1/C1 it is **hypothesized** that the unshifted interval overlaps `[0, 2]` and classifies as `FIND-ANSWER-BOUNDARY` / T5 INCONCLUSIVE, not FAIL. CL-A: mixed candidate set without a T5 interval is hypothesized INCONCLUSIVE under retained R1. CL-TA: hypothesized to inherit the TEST interval verdict. CL-LOOP: hypothesized not to match `h_find_answer_late` (grid default LATE) nor a unique in-window singleton until a later distinguishing event. |
| HC-FIND-NEAR-EQUIV | LATE near FIND observation end (`11/5`) paired with ABSENT | CL-T: hypothesized to confuse late-near-end with absence. CL-A: order/presence features are hypothesized to still separate the pair. CL-TA: hypothesized to follow TEST. CL-LOOP: hypothesized to retain both LATE and ABSENT until stop. |
| HC-LATE-ABSENT-SHORT-WINDOW | ABSENT with observation end at `2` s, paired with LATE | All arms: hypothesized observationally equivalent when the window ends at or before the deadline; DEC-EQUIV remains OPEN. |
| HC-OBS-PERTURB-EPS | LATE plus `+2ε` observationInterval shift | It is **hypothesized** that jitter now changes the arm-visible interval and, near endpoints, the observation class. CL-T: hypothesized more sensitive to interval shift. CL-A: hypothesized insensitive if it ignores endpoints. CL-TA: hypothesized to inherit TEST. CL-LOOP: hypothesized partial sensitivity through T5 members. |
| HC-LUR-ACK-DELAY-VS-MISSING | delayed but present LUR-ACK versus F-LUR-ACK-MISSING | CL-T: if no numeric ACK interval is frozen, delay is hypothesized indistinguishable from H-NORMAL on T5. CL-A: presence is hypothesized to separate delay from missing. CL-TA: hypothesized to follow presence. CL-LOOP: hypothesized to drop `h_lur_ack_missing` once LUR-ACK is observed. Truth for delayed-ACK units is h_normal (CR-2026-029); any FAIL on them is a false fail. |
| HC-INVALID-OBS-JITTER | H-INVALID-OBS plus `−2ε` interval shift | All arms: hypothesized ERROR / INVALID-OBS rather than IUT FAIL; DETECT/ABLATION accounting only. |

These constructions are intended so that accuracy metrics *can* separate arms.
The pilot ceiling (MISS 0, FALSE-FAIL 0, TRUE-RETAINED 228/228) is a fact about
the non-confirmatory census of model-built default faults, not a confirmatory
result for this grid.

## Open decisions (options and recommendations; none closed)

DEC-IUT is already closed. The items below stay OPEN.

### DEC-CLOCK

- **Option C1.** Keep the simulated T5 rule (`I_obs ⊆ I_r` PASS; disjoint FAIL;
  overlap-not-subset INCONCLUSIVE) with closed CRS intervals, and treat
  simulated `ε` as a declared bound only.
- **Option C2.** Score every endpoint equality as INCONCLUSIVE until a
  laboratory error budget exists.
- **Option C3.** Change the FIND host-answer contract to a half-open interval
  so `t = 2` is strictly outside or inside by definition.
- **Recommendation (not a close):** C1 for this simulated design, because it
  matches the already-accepted instrument; C2 remains available for any future
  physical clock. Simulated `ε` is not calibration. S1 implements C1 on the
  visible interface only; DEC-CLOCK stays OPEN.

### DEC-EQUIV

- **Option E1.** Adjudge LATE vs ABSENT as non-equivalent whenever FIND-ANSWER
  is present under the default FIND observation end.
- **Option E2.** Adjudge them equivalent when the observation end is moved to
  the requirement deadline (HC-LATE-ABSENT-SHORT-WINDOW).
- **Option E3.** Leave the pair `unresolved` until a named adjudicator records
  impact evidence; equivalent cells stay outside scored detection denominators.
- **Recommendation (not a close):** E3 as the default flow, with E1 as a
  candidate for the default-end pair only. Do not silently score short-window
  pairs.

### DEC-SAMPLE

- **Option S1.** Independent unit = `(base scene × fault × parameter vector)`;
  N = 1 identity attempt per unit because the IUT is deterministic; arms are
  paired on that unit.
- **Option S2.** Census a declared subset (harder cases + one default per
  parent fault) rather than the full Cartesian product.
- **Option S3.** Keep N > 1 identity repeats (pilot style). The pilot showed
  those repeats carry no information.
- **Recommendation (not a close):** S1 for the registered grid, with S2 as a
  resource fallback if DEC-RESOURCE later bounds wall time. Inferential
  intervals stay `WAIT-DEC-SAMPLE` until a named reviewer freezes multiplicity.

### DEC-RESOURCE

- **Option R1.** Exclusive ROUNDS mode, remaining = 8, matching the pilot
  session envelope.
- **Option R2.** Exclusive BUDGET mode with a four-vector projection.
- **Option R3.** Per-family envelopes (FIND vs INFORMATION) still exclusive
  within a session.
- **Recommendation (not a close):** R1 until charge traces from any future
  confirmatory run exist. Mode remains exclusive; retry cap stays a safety
  constraint, not a second Stop-Budget.

### DEC-TRUTH

- **Option T1.** Keep confirmed-injection tokens and the fail-closed evaluator
  store (Phase A instrument).
- **Option T2.** Require a second human adjudication for every harder pair
  before truth is scorable.
- **Option T3.** Dual protocol: token confirmation for presence/order faults;
  unresolved truth for endpoint/equivalence candidates until DEC-EQUIV moves.
- **Recommendation (not a close):** T3. Truth access paths stay unchanged;
  unconfirmed injection still cannot become truth.

## Sample-size logic

1. The **independent experimental unit** is one `(base scene × fault ×
   parameter vector)` on a reset simulated IUT. Arms are not additional
   independent units; they are paired treatments of the same unit.
2. Because the IUT is deterministic and consumes no PRNG, repeating the same
   unit with distinct seeds is hypothesized to add **zero** outcome
   information (as observed in the non-confirmatory pilot). Therefore the
   design sets **N = 1 per unit** unless DEC-SAMPLE later requires identity
   repeats for audit.
3. The draft expander in `a615a_sim.faults.parameters` enumerates units; it is
   not a runner. Cell count is a planning quantity, not a result.
4. Family-wise error control, Clopper-Pearson, and superiority tests remain
   unauthorized until DEC-SAMPLE names a procedure **before** any held-out
   confirmatory access.

## Draft analysis plan

| Layer | Content | Status |
|---|---|---|
| Primary metrics | MET-MISS, MET-FALSE-FAIL, MET-TRUE-RETAINED, MET-ANSWERED-COVERAGE, MET-CONDITIONAL-DETECTION-ERROR, MET-LOCALIZATION-COVERAGE | descriptive until DEC-SAMPLE |
| Secondary | MET-COST-VECTOR, MET-ROUNDS, MET-INCONCLUSIVE, MET-TRUTH-MISSING, MET-ERROR, MET-FINAL-CANDIDATES | descriptive; MET-ROUNDS `issued=1` in the pilot is a known counting question, not changed here |
| Contrasts | CL-LOOP vs CL-T (DETECT); CL-LOOP vs CL-TA (LOCATE); CL-A vs CL-T on presence-only faults | paired on the independent unit |
| Multiplicity | one family-wise procedure must be named before confirmatory rejection claims | OPEN / WAIT-DEC-SAMPLE |
| Decision rule | No PASS/FAIL superiority. A contrast is reportable only on a shared denominator. Mixed `h_normal` without T5 → INCONCLUSIVE (U4 / R1). Ceiling metrics on default model-built faults are hypothesized *not* to be the confirmatory headline; harder cases are hypothesized to supply the discriminating rows. | not executed |
| Forbidden | inferential claims from this proposal; filling PH-RES-* / PH-ABS-RESULT / PH-STAT-N; reusing pilot rows as confirmatory data | — |

## Threats to validity (simulated IUT)

- **Model-built faults.** The injector and the IUT share the same bound model.
  Discrimination on this grid would not automatically transfer to a physical
  TH / FIND-HOST.
- **Clock.** Simulated `ε` is not a JCGM error budget. Endpoint hypotheses
  (HC-FIND-ENDPOINT) are especially sensitive to this threat.
- **Confirmation circularity.** Injection confirmation uses the same event
  kinds it injects. Independent physical observation does not exist.
- **R1 / mixed-set INCONCLUSIVE.** Coverage numerators remain sensitive to the
  outcome rule; the pilot’s 156/360 INCONCLUSIVE rows illustrate the
  mechanism, not a confirmatory rate.
- **LOCATE unused in pilot.** Confirmatory design still lists locate scenes;
  whether they enter the scored locate population is DEC-SAMPLE / plan
  registration.
- **Observation jitter** is an algorithm-visible interval shift, not a
  physical timestamp attack. It tests algorithm sensitivity, not metrology.

## Design ambiguities (not resolved here)

1. Resolved by CR-2026-029: the standard gives no numeric LUR-ACK deadline and none is invented; delayed ACK is a normal timing perturbation (truth h_normal).
2. Whether `findAnswerAtS = 2` is LATE, in-interval normal, or INCONCLUSIVE
   still depends on DEC-CLOCK inclusivity. S1/C1 **hypothesizes** overlap
   INCONCLUSIVE / `FIND-ANSWER-BOUNDARY` on the unshifted simulated interval;
   that is not a close of DEC-CLOCK.
3. Whether a FIND observation end at `2` s makes LATE and ABSENT equivalent
   depends on DEC-EQUIV (HC-LATE-ABSENT-SHORT-WINDOW).
4. Cartesian expansion vs harder-case subsample is a DEC-SAMPLE / DEC-RESOURCE
   trade; this draft enumerates both default parameter ticks and harder cases
   without authorizing a run.

# 中文版

本文件是确认性**设计提案**，不是普查或确认性运行。IUT 为已关闭 DEC-IUT 的
本地模拟 615A。变异轴为参数化故障与多基准场景（U2），不是 N 次重复或无种子
随机。困难情形见目录 `harderCases`，仅通过既有协议事件对臂可见（U3）。保留
R1：含 `h_normal` 且无 T5 区间的混合 VALID 集为 INCONCLUSIVE（U4）。用户裁决
S1：臂只见 `observationInterval`，按 T5／C1 子集规则判定在窗内／迟到／
INCONCLUSIVE；`FIND-ANSWER-BOUNDARY` 是观测类而非协议事件名。DEC-CLOCK 仍
OPEN；本提案按 C1 实现可见接口，不关闭该决策。试点产物在旧（精确 tick）
接口下产生，本次不重跑。DEC-EQUIV、DEC-SAMPLE、DEC-RESOURCE、DEC-TRUTH 均
给出选项与建议，一律不关闭。关于臂间可分性、错误率或成本的陈述均为假设。
