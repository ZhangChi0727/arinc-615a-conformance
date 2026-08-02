# Review and Gate Guideline

| Field | Value |
|---|---|
| **Version** | 2.1 |
| **Status** | Baseline-aligned |
| **Source** | RR-2026-001 v4.2 §4.10 |

## Review types

| Type | Focus |
|---|---|
| Repository | placement, naming, links, confidentiality, baseline references |
| Engineering | behavior, interfaces, tests, reproducibility, tool failure modes |
| Methodology | requirements, models, oracles, fault domain, mathematical semantics |
| Research | questions, hypotheses, baselines, validity, citations, claim strength |
| Evidence | provenance, exclusions, calculations, raw-to-derived reproduction |
| Claim release | correspondence between wording, achieved tier, risks, and gates |

One PR or gate may require several review types.

## RG0–RG6

| Gate | Entry | Required reviewers | Approval focus |
|---|---|---|---|
| RG0 Scope | standard, roles, services, applicability, observation draft | method + engineering | feasible, bounded scope |
| RG1 CRS | dual extraction and adjudication | requirements + independent method | source, atomicity, applicability |
| RG2 Model/trace | clock-augmented EFSM, timing catalog, mappings | protocol + timing/method | discrete/timed observability, consistency, completeness |
| RG3 VC/oracle | cases, robust oracles, clock/reset/error schemas | test + independent protocol | executability, timing uncertainty, verdict validity |
| RG4 Execution | IUT/tool/clock/timestamp/environment configuration | engineering + test | control, timing error budget, dry run, tool validity |
| RG5 Evidence | timestamped raw and derived packages | evidence + timing/analysis | provenance, clock metadata, exclusions, reproduction |
| RG6 Claim | assurance argument and proposed wording | independent research + engineering authority | achieved gates and residual risk |

Independence means the reviewer did not solely author the judgment being
approved. A small team may use role separation and a recorded second pass.

## Outcomes

Use exactly:

- `APPROVE`;
- `APPROVE WITH ACTIONS`;
- `REWORK`.

`APPROVE WITH ACTIONS` must identify owners and deadlines and cannot be used for
an unresolved mathematical error, invalid oracle, missing provenance, or
overstated claim. It also cannot be used when an applicable timing obligation
lacks trigger, response, bound, clock-reset, observation, or defensible
error-budget semantics.

## Finding severity

| Severity | Meaning |
|---|---|
| Must | Blocks the gate or merge |
| Should | Required follow-up with named owner |
| Nice | Optional improvement |

## Gate record

Store durable records as `docs/review/gates/GR-<gate>-<date>-<artifact>.md`:

```text
artifact and version
baseline and applicable claim IDs
reviewers and independence statement
entry criteria
findings and dispositions
residual risks
decision
sign-off date
```

## Theory debt

Theory debt is permitted only when:

- it does not contradict the frozen baseline;
- it is irrelevant to the current released claim;
- it has an owner, trigger, and destination;
- claim wording excludes the unresolved theory.

DTMC edge-confidence, first-order path products, and HMM-based localization are
not active baseline mechanisms. They may re-enter only through baseline change
control supported by appropriate data and validation.

---

# 中文版

评审类型包括仓库、工程、方法、研究、证据和主张发布。RG0 固定范围；RG1 裁决 CRS；RG2 评审带时钟 EFSM、时序目录和追踪；RG3 评审 VC、稳健 oracle、时钟/复位/误差 schema；RG4 检查 IUT、工具、时钟、时间戳链、环境和试运行；RG5 检查带时戳原始/派生证据及可复现性；RG6 控制主张发布。

## 评审类型

仓库、工程、方法、研究、证据和主张发布评审各自声明对象、评审者独立性和允许决定。

## RG0–RG6

RG0 固定范围；RG1 裁决 CRS；RG2 评审模型和追踪；RG3 评审 VC/oracle；RG4 检查执行就绪；RG5 检查证据完整性；RG6 独立控制主张发布。

## 结果

结果只能是 `APPROVE`、`APPROVE WITH ACTIONS` 或 `REWORK`。数学错误、无效 oracle、缺失来源、过度主张，或适用时序义务缺少触发、响应、界限、时钟复位、观测点或可辩护误差预算时，不得使用“带行动批准”。Must 阻塞门禁/合并，Should 需要负责人和期限，Nice 为可选改进。

## 发现严重度

Must 阻塞门禁/合并；Should 必须有负责人和期限；Nice 为不影响批准的可选改进。

## 门禁记录

使用 `GATE_RECORD_TEMPLATE.md` 保存产物版本、基线、主张、评审者独立性、进入条件、发现、剩余风险、决定、理由和签字。

```text
产物及版本
基线和适用主张 ID
评审者及独立性声明
进入条件
发现及处理
剩余风险
决定
签字日期
```

## 理论债务

DTMC 边置信度、一阶路径乘积和 HMM 定位仍不是基线机制。只有经过正式基线变更，并证明物理状态含义、可识别性、数据量和比较性能后才能重新进入。
