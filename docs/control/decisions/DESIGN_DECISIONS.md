# Design Decisions

Log of important research/engineering decisions and their rationale.

Append new entries; do not rewrite history—add superseding entries instead.

---

## DD-001 — Verification Point as primary unit

**Decision:** Use *Verification Point* (and verification cases derived from it) as the primary auditable unit linking standards to execution.

**Why:** Auditable traceability for conformance arguments; aligns with requirements-based verification practice and ISO 9646-style derivation.

**Date:** 2026-07

**Status:** Active

---

## DD-002 — Layered quantitative model (as stated in RR-2026-001)

**Decision:** RR-2026-001 introduces a layered quantitative confidence story (reported there using DTMC/HMM vocabulary) on top of the VCS methodology.

**Why:** Move from binary Pass/Fail alone toward scoped assurance metrics and diagnostic hooks.

**Date:** 2026-07

**Status:** Active in research docs; **formalization under methodology review** (see PR #2 review notes). Future PRs may refine mathematical presentation without abandoning the goal of quantified confidence.

---

## DD-003 — Bayesian / evidence-based confidence language

**Decision:** Treat quantitative “confidence” as **epistemic / evidence-based** assurance given tests, not as an unexplained intrinsic randomness of the IUT.

**Why:** Protocol specs are largely deterministic; uncertainty is about our knowledge of the IUT under a fault/observation model.

**Date:** 2026-07

**Status:** Active

---

## DD-004 — Mutation analysis for adequacy

**Decision:** Use mutation / fault injection to support detection-capability claims for the base VCS.

**Why:** Requirement coverage alone does not prove detection power; mutation provides an explicit finite fault model bound.

**Date:** 2026-07

**Status:** Active

---

## DD-005 — Base vs extended VCS separation

**Decision:** Keep a stable, standard-derived **base** VCS separate from project-specific **extended** cases.

**Why:** Preserve a reusable conformance claim while remaining compatible with customer ICD extras.

**Date:** 2026-07

**Status:** Active

---

## DD-006 — Dual-role simulator as instrument, not the claimed innovation

**Decision:** Position the dual-role software as the experimental / engineering instrument; academic novelty centers on the verification method.

**Why:** Matches the project’s academic-thesis framing (engineer perspective).

**Date:** 2026-07

**Status:** Active

---

## DD-007 — Freeze RR-2026-001 v4.1 as the methodology baseline

**Decision:** Adopt `RB-2026-001-v4.1` as the normative research-method
baseline for subsequent requirements, engineering, experiments, analysis, and
publication work.

**Why:** The report now separates analytical objects, bounds every assurance
tier, resolves the blocking probability and fault-domain errors, and defines
operational review/evidence gates.

**Date:** 2026-07-26
**Status:** Active; supersedes any inconsistent methodology language in earlier
outlines and proposals.

---

## DD-008 — Test and Analysis are complementary primary paths

**Decision:** Test produces controlled observations and verdict evidence;
Analysis evaluates coverage, adequacy, uncertainty, and diagnosis. Neither is
treated as sufficient alone.

**Why:** This architecture creates both scientific evaluability and an
engineering feedback loop.

**Date:** 2026-07-26
**Status:** Active

---

## DD-009 — Review and Inspection are cross-cutting gates

**Decision:** Implement RG0–RG6 as independent static controls across the
Test-and-Analysis loop. Demonstration remains optional and cannot replace
detailed protocol evidence.

**Why:** Artifact defects and overstated claims need prevention before they
propagate into execution or release.

**Date:** 2026-07-26
**Status:** Active

---

## DD-010 — Retire DTMC/HMM as baseline conformance machinery

**Decision:** Protocol behavior remains an EFSM/IOLTS; calibrated inference and
diagnosis use separately defined models. DTMC edge labels, weakest-link
“probabilities,” path products, and HMM/Viterbi localization are not baseline
claims.

**Why:** Protocol topology, evidence, and stochastic inference are different
mathematical objects. Temporal models require independently demonstrated state
meaning, identifiability, data sufficiency, and comparative performance.

**Date:** 2026-07-26
**Status:** Active; supersedes DD-002 where it described DTMC/HMM vocabulary as
the active quantitative story.

---

## DD-011 — Gate-earned claim release

**Decision:** All research and engineering claim wording is controlled by
`docs/research/CLAIM_EVIDENCE_MATRIX.md`. T0–T3, diagnosis, engineering
reproducibility, and transferability are promoted only by their required
evidence and gates.

**Why:** Repository progress and passing tests are not substitutes for an
assurance argument.

**Date:** 2026-07-26
**Status:** Active

---

## DD-012 — Add deterministic timed conformance without restoring stochastic protocol semantics

**Decision:** Adopt `RB-2026-001-v4.2`. Extend the observable EFSM with clocks,
clock guards, invariants, and resets; represent executions as timestamped
traces; and use an interval-based robust timing oracle with an explicit
measurement-error budget. Co-locate the Chinese translation after each key
English document rather than maintaining parallel language files.

**Why:** Timing obligations are already in scope, but v4.1 did not give them a
complete mathematical or measurement semantics. A point-threshold oracle can
create false precision near a boundary. Co-located translations reduce
structural drift. Protocol topology remains deterministic/nondeterministic as
declared and is not converted into a DTMC or HMM.

**Date:** 2026-07-30

**Status:** Active. Approved by `GR-PR6-RB-2026-001-v4.2` and made effective by
the merge of PR #6. v4.2 supersedes v4.1 as the current methodology baseline
identifier, while DD-010 remains active. v4.1 evidence is not automatically
relabelled as v4.2 evidence.

### 中文

采用 `RB-2026-001-v4.2`：在可观测 EFSM 中加入时钟、时钟守卫、不变量和复位；将执行表示为带时戳迹；以显式测量误差预算驱动区间式稳健时序 oracle；关键英文文档末尾直接附中文译本。原因是 v4.1 已将时序义务纳入范围，却没有完整数学和测量语义，点阈值会在边界制造虚假精度。该决定不恢复 DTMC/HMM 协议语义。

---

## DD-013 — Separate product domains through controlled, traceable contracts

**Decision:** Treat methodology research/publication, engineering
implementation, and verification tutorials as distinct product domains. Keep
governance and controlled requirements as their shared contract layer. Move the
authoritative report from `docs/study/` to `docs/methodology/`; separate common
and ARINC 615A tutorial entry points; and require cross-domain dependencies to
identify upstream artifact versions and applicable gate records. Publication
and tutorials remain downstream. Evidence-driven feedback changes an upstream
contract only through CR/DD and Review control.

**Why:** Complete independence is neither possible nor useful: research needs
engineering evidence, engineering implements method semantics, and tutorials
explain both. Explicit direction and trace records reduce accidental coupling
without breaking the integrated verification loop.

**Date:** 2026-07-31

**Status:** Active. Approved by `GR-PR6-RB-2026-001-v4.2` and made effective by
the merge of PR #6. Product domains are coupled only through controlled contracts;
tutorials are non-normative, publication cannot modify methodology, and
upstream-changing feedback enters through CR/DD and Review control.

The locations established by this decision were reorganized by active
DD-014/CR-2026-003 through PR #7, without changing the dependency semantics.

---

## DD-014 — Separate the reader release surface from the developer control plane

**Decision:** Adopt the information architecture and reporting contract in
CR-2026-003. Keep only the reader-oriented README at the repository root; keep
machine-discovered configuration at its conventional root paths; place all
reader deliverables under `artifacts/`; and give project, research,
engineering, and tutorial work one control entry each. Preserve evidence and
governance records as separate traceable artifacts. Release every reader update
as one self-contained report directly linked from the root README.

**Why:** Readers need one coherent release narrative, whereas developers need
atomic records, ownership, and audit history. Treating those needs as separate
surfaces reduces navigation noise without flattening the assurance argument or
weakening traceability.

**Date:** 2026-08-02

**Status:** Active. Approved by `GR-PR7-RB-2026-001-v4.2.1` and made effective
by the merge of PR #7. The review confirmed relocation completeness, link integrity,
bilingual parity, validator coverage, and no change to RR-2026-001 v4.2
mathematical or methodological semantics.

---

# 中文版

本决策日志只追加、不重写历史。有效决策包括：以可审计验证点/用例为主单位；把“置信”解释为有条件的认识性证据；用有限故障域和变异评价检测能力；分离基础与扩展 VCS；把双角色模拟器定位为仪器而非学术创新；以测试和分析为互补主路径；以评审和检查作为横向门禁；停用 DTMC 边概率、最弱链路、路径乘积和默认 HMM 定位；所有主张由证据门晋级。

## DD-001——以验证点为主要单位

以可审计的需求义务、TP 和 VC 为主要推理与追踪单位。

## DD-002——分层定量模型（历史）

保留原 RR-2026-001 的历史陈述，但其 DTMC/HMM 核心已由 DD-010 取代。

## DD-003——贝叶斯/证据置信语言

“置信”仅表示满足校准、先验和模型条件时的认识性证据。

## DD-004——用变异分析评价充分性

在声明的有限故障域内，以有效、非等价变异体评价检测能力。

## DD-005——基础与扩展 VCS 分离

扩展实验不得修改基础用例的规范性 oracle。

## DD-006——双角色模拟器是仪器

模拟器用于受控刺激、观测和故障注入，不被单独宣称为学术创新。

## DD-007——冻结 RR-2026-001 v4.1

保留历史决定；若 v4.2 获批，其当前基线标识由 DD-012 取代。

## DD-008——测试与分析互补

测试产生受控观察，分析评价证据范围和强度，二者均不可单独完成方法论。

## DD-009——评审和检查是横向门禁

Review 与 Inspection 控制静态产物和主张，而非被强行并入动态 Test。

## DD-010——停用 DTMC/HMM 基线机制

协议保持 EFSM/IOLTS；概率推断和诊断使用独立定义并验证的模型。

## DD-011——主张由门禁获得

所有研究和工程措辞由主张—证据矩阵及相应门禁晋级。

## DD-012——加入确定性时序符合性而不恢复随机协议语义

DD-012 已由 `GR-PR6-RB-2026-001-v4.2` 批准，并已在 PR #6 合并时生效：v4.2 取代 v4.1 作为当前方法论基线标识，同时保持 DD-010 有效；加入确定性时序语义和误差感知 oracle，但不把协议图变成随机过程。v4.1 证据不得自动改标为 v4.2 证据。

### 中文

本节是英文 DD-012 内嵌中文说明的对应结构；独立评审结论已记录，但合并前不得提前改为 Active。

## DD-013——通过受控可追踪契约分离产品领域

把方法论研究/出版、工程实现和验证教程视为不同产品领域，以治理和受控需求作为共享契约层。权威报告从 `docs/study/` 迁移至 `docs/methodology/`；通用教程和 ARINC 615A 教程使用不同入口；跨领域依赖必须标明上游产物版本和适用门禁记录。出版和教程保持下游地位；证据反馈只有通过 CR/DD 与评审控制才能修改上游契约。

完全独立既不可能也无益：研究需要工程证据，工程实现方法语义，教程解释二者。明确依赖方向与追踪记录能够在不破坏综合验证闭环的情况下减少偶然耦合。本决定已由 `GR-PR6-RB-2026-001-v4.2` 批准，并已在 PR #6 合并时与 DD-012 同时生效。产品域通过受控契约耦合；教程不具规范性，出版不得反向修改方法论，改变上游契约的反馈必须通过 CR/DD 和评审控制进入。该决定建立的路径已由生效的 DD-014/CR-2026-003 经 PR #7 重组，但依赖语义不变。

## DD-014——分离读者发布面与开发者控制平面

采用 CR-2026-003 的信息架构和报告契约：根目录只保留面向读者的 README；工具按约定发现的
机器配置继续位于根目录；全部读者交付物置于 `artifacts/`；项目、研究、工程和教程各有一个
控制入口；证据与治理记录继续作为独立可追踪产物保存；每次读者更新以一份自包含报告发布，
并由根 README 直接链接。

读者需要连贯的发布叙述，开发者则需要原子记录、所有权和审计历史。分离两个界面可以减少
导航噪声，同时不压平保证论证或削弱追踪。本决定已由 `GR-PR7-RB-2026-001-v4.2.1`
批准，并已随 PR #7 合并生效。独立评审已确认迁移完整、链接有效、中英文对等、校验器覆盖充分，且
RR-2026-001 v4.2 的数学与方法论语义未改变。
