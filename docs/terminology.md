# Controlled Terminology

| Field | Value |
|---|---|
| **Version** | 2.1 |
| **Status** | Baseline-controlled |
| **Authority** | RB-2026-001-v4.2 |

## Core verification terms

| Term | Definition |
|---|---|
| **IUT** | Implementation Under Test: the fixed protocol implementation and configuration being evaluated. |
| **Applicability declaration** | Controlled statement of supported roles, services, options, and exclusions used to derive applicable requirements. |
| **Observation boundary** | Packet, timing, state, log, file, and environment phenomena permitted for verification decisions. |
| **CRS** | Conformance Requirement Set: atomic, applicable normative requirement items with controlled source references and interpretations. |
| **Verification obligation** | A functional, state, transition, data, timing, negative, or sequence aspect that must be covered for a requirement. |
| **TP** | Test Purpose: focused statement of the behavior or obligation a test is intended to verify. |
| **VC** | Verification Case: executable preconditions, stimulus, oracle, references, targets, reset, and evidence schema. |
| **VCS** | Verification Case Set: a controlled collection of VCs. |
| **Base VCS** | Cases derived from the applicable standard CRS for the base scoped claim. |
| **Extended VCS** | Additive project/ICD-specific cases whose results remain distinguishable from the base VCS. |
| **Oracle** | Rule or procedure mapping valid observations to PASS/FAIL while preserving INCONCLUSIVE/ERROR conditions. |
| **Evidence** | Versioned raw or derived records supporting a named claim, including provenance and conditions. |
| **Coverage** | Degree to which a named target set is addressed; not itself a conformance probability. |
| **Conformance** | Agreement with the declared applicable requirements under the stated observation, environment, and claim scope. |
| **Timed trace** | Ordered observable events paired with timestamps from a declared monotonic time basis. |
| **Timing obligation** | Requirement-defined trigger, response, cancellation/silence, lower/upper bounds, units, and clock-reset semantics. |
| **Measurement-error budget** | Auditable bound on applicable clock, timestamp, scheduling, capture, and path uncertainty. |
| **Robust timing oracle** | Interval-based rule: PASS only when the observation interval is contained in the allowed interval; FAIL only when disjoint; overlap is INCONCLUSIVE. |
| **Run-order dependence** | Drift, clustering, warm-up, shared state, or another effect that makes repeated executions dependent. |

## Verification activities

| Term | Definition |
|---|---|
| **Test** | Dynamic interaction with the IUT under controlled conditions to produce observations, measurements, and verdicts. |
| **Analysis** | Evaluation of requirements, models, traces, coverage, faults, uncertainty, dependencies, or diagnosis to determine what evidence supports and what action follows. |
| **Inspection** | Checklist-driven examination of objective artifact properties and completeness. |
| **Review** | Independent evaluation of technical judgments and progression through a gate. |
| **Demonstration** | Stakeholder-visible operation used where detailed measurement is not the primary objective; optional in this methodology. |

## Assurance and quantitative terms

| Term | Definition |
|---|---|
| **T0 Traceability** | Every applicable obligation is linked to reviewed executable cases. |
| **T1 Observed conformance** | Accepted behavior was observed for named valid executions under recorded conditions. |
| **T2 Bounded detection adequacy** | The VCS distinguishes all claimed members of a declared evaluated fault set. |
| **T3 Calibrated evidence** | Evidence updates belief in named conformance propositions under a validated observation model. |
| **Finite fault domain** | Explicit finite set of candidate nonconforming implementations or mutants used to bound a detection claim. |
| **Equivalent mutant** | Executable mutant indistinguishable from the specification within the declared observation scope. |
| **Mutation score** | Fraction or justified weighted fraction of evaluated valid non-equivalent mutants killed by the VCS. |
| **Operational PASS probability** | PASS probability under a defined repeated-run regime; not automatically belief that a fixed IUT conforms. |
| **Calibration** | Independent estimation and validation of observation-model behavior such as true-PASS and false-PASS rates. |
| **Posterior conformance belief** | Conditional probability of a named fixed conformance proposition under declared prior, likelihood, calibration, and dependence assumptions. |
| **Diagnostic model** | Separately validated model ranking fault classes from failure features; severity is governed separately. |

## Protocol roles

| Term | Definition |
|---|---|
| **DLS** | Data Loader System: loader-side ARINC 615A peer. |
| **THW** | Target Hardware: target-side ARINC 615A peer. |
| **Clock-augmented EFSM** | EFSM extended with clocks, clock guards, state invariants, and clock resets for deterministic timed conformance. |
| **PICS-like declaration** | Project applicability artifact analogous in purpose to a Protocol Implementation Conformance Statement. |

## Usage rules

- Use PASS, FAIL, INCONCLUSIVE, and ERROR as distinct verdicts.
- Use “traceability-complete,” “observed,” or “bounded detection” instead of
  unrestricted “proved conformance.”
- Do not call mutation score FMEDA diagnostic coverage without a defensible
  target failure-mode population and mapping.
- Do not call protocol-edge labels transition probabilities unless they form a
  validated stochastic kernel.
- HMM is a candidate temporal diagnostic model, not a baseline synonym for the
  protocol model.
- Do not call a point timestamp an exact timing result when a nonzero
  measurement-error budget applies.

---

# 中文版

核心术语：IUT 是固定实现及配置；适用性声明确定角色、服务、选项和排除项；观测边界限定可用于判定的报文、时序、状态、日志和环境现象；CRS 是带受控来源和解释的原子适用需求；TP 描述待验证义务；VC 是可执行的前置条件、刺激、oracle、追踪、目标、重置、时序/误差 schema 和证据 schema；VCS 是受控 VC 集。

## 核心验证术语

IUT、适用性声明、观测边界、CRS、TP、VC 和 VCS 采用上述受控含义；“覆盖”必须指明需求、义务、状态、转移、守卫、数据分区或时序分区对象。

## 验证活动

Test 通过受控执行产生观察，Analysis 评价覆盖、充分性、不确定性和诊断，Review 对工作产品进行技术判断，Inspection 按准则检查静态产物，Demonstration 仅说明操作表现，不能替代 Test 或 Analysis。

## 保证与定量术语

时序术语：**时戳迹**是采用声明单调时间基准的事件—时间戳序列；**时序义务**必须定义触发、响应、取消/静默、上下界、单位和时钟复位；**测量误差预算**是时钟、时间戳、调度、捕获和路径不确定性的可审计界；**稳健时序 oracle**仅在观测区间完全包含于允许区间时判 PASS，二者不相交时判 FAIL，部分重叠时判 INCONCLUSIVE；无效时间链判 ERROR；**运行顺序依赖**包括漂移、聚类、预热和共享状态。

T0–T3 分别表示追踪/方法完备、有效执行证据、有限故障域检测充分性和经校准的概率解释；不得把变异分数、重复 PASS 率或后验概率互相替代。

## 协议角色

ARINC 615A 实例必须显式声明目标 IUT 角色、对端角色、DOWNLOAD/UPLOAD 等服务以及适用选项；角色名不能代替能力声明。

## 使用规则

带时钟 EFSM 是加入时钟、时钟守卫、状态不变量和时钟复位的 EFSM，用于确定性时序符合性。它不是 DTMC，也不是 HMM。HMM 只有在隐状态确实随物理时间演化且数据、可识别性和比较性能充分时才是可选诊断模型。
