# Traceability Schema

Traceability is relational and many-to-many. Under the `RB-2026-001-v4.3`
migration candidate, all `rho_*` relations below are local ARINC/Profile trace
relations. They are not Generic GVS Core relations. Their direction is fixed,
but cardinalities and external GVS correspondence remain open to independent
review. Relations are split into local assurance and engineering/research groups.

## ARINC/Profile assurance relations

| Relation | Source | Target | Required metadata |
|---|---|---|---|
| `rho_BR` | higher-level requirement / basis | protocol requirement | basis ref, rationale, reviewer |
| `rho_RA` | protocol requirement | applicable CRS item | obligation, applicability, reviewer |
| `rho_RO` | CRS requirement / obligation | Verification Objective | objective type, acceptance criteria, reviewer |
| `rho_OM` | Verification Objective | verification method / test purpose / analysis / review | method role, reviewer |
| `rho_TV` | test purpose | verification case | coverage role, polarity, reviewer |
| `rho_VE` | verification case execution | evidence record / execution evidence manifest | run and manifest IDs |
| `rho_EO` | evidence / verification record | objective satisfaction record | closure rationale, reviewer |
| `rho_OC` | verification objective | compliance claim | claim ID, scope, reviewer |

`rho_BR` may remain `NOT_INSTANTIATED_IN_PROTOCOL_ONLY_STUDY` when no
aircraft-level certification requirement is instantiated. Do not fabricate
aircraft-level certification requirements in the protocol-only study.

This chain is a local trace view. A link records a candidate relation; it does
not automatically establish a Verification Basis Element, Verification
Obligation, Evidence Item, Objective Satisfaction, Claim support, compliance,
or authority acceptance. External correspondence is `NOT-DETERMINED` unless a
reviewed mapping record states otherwise.

## Engineering and research extension relations

| Relation | Source | Target | Required metadata |
|---|---|---|---|
| `rho_RM` | requirement obligation | EFSM / model target | state/transition/data/clock guard/invariant/reset/timing target |
| `rho_VF` | verification case | fault class / mutation operator | expected detection mechanism |
| `rho_EA` | evidence | calibration / diagnosis / research analysis | analysis model, dataset |

These relations must not be presented as certification-mandatory trace links.

## Integrity checks

- every applicable requirement has at least one `rho_RA` to a CRS item;
- every applicable CRS obligation traces to at least one Verification Objective
  via `rho_RO`;
- every objective has acceptance criteria and at least one `rho_OM` to a
  verification method;
- every test purpose has at least one executable `rho_TV`;
- every verification case references controlled requirements and model targets;
- every execution traces via `rho_VE` to a controlled evidence manifest;
- every objective satisfaction record traces via `rho_EO` to supporting
  evidence;
- every compliance claim traces via `rho_OC` to objective satisfaction;
- every timing obligation traces to its trigger/response/cancellation/
  supersession predicates, correlation key, pairing/concurrency policy,
  endpoint inclusivity, bounds, clock start/reset targets, error-budget
  ID/version, timing partitions, robust oracle, and evidence fields;
- dangling, retired, or version-mismatched IDs fail validation;
- core and extension relations are distinguishable;
- coverage reports show missing links rather than dropping them.

## Export

Use machine-readable CSV or JSON plus a human-readable generated matrix. The
machine-readable relation set is authoritative; generated views identify the
source version and generation command.

---

# 中文版

追踪关系是多对多关系。在 `RB-2026-001-v4.3` 迁移候选下，下列全部 `rho_*` 都是本地
ARINC/Profile 追踪关系，不是 Generic GVS Core 关系。方向已固定，但基数和外部 GVS 对应
仍待独立评审。关系分为本地保证关系与工程/研究关系。

## ARINC/Profile 保证关系

`rho_BR` 从更高层需求/基础到协议需求；`rho_RA` 从协议需求到适用 CRS 项；`rho_RO` 从 CRS 需求/义务到验证目标；`rho_OM` 从验证目标到验证方法/测试目的/分析/评审；`rho_TV` 从测试目的到验证用例；`rho_VE` 从验证用例执行到证据记录/执行证据清单；`rho_EO` 从证据/验证记录到目标满足记录；`rho_OC` 从验证目标到合规主张。

当未实例化航空器级认证需求时，`rho_BR` 可保留为 `NOT_INSTANTIATED_IN_PROTOCOL_ONLY_STUDY`。在仅协议研究中不得编造航空器级认证需求。

该链只是本地追踪视图。存在链接不会自动建立 Verification Basis Element、Verification
Obligation、Evidence Item、Objective Satisfaction、Claim support、compliance 或 authority
acceptance。除非受评审映射另有规定，外部对应状态为 `NOT-DETERMINED`。

## 工程与研究扩展关系

`rho_RM` 从需求义务到 EFSM/模型目标；`rho_VF` 从验证用例到故障类别/变异算子；`rho_EA` 从证据到校准/诊断/研究分析。这些关系不得被表述为认证强制链接。

## 完整性检查

每个适用需求至少有一个 `rho_RA`；每个适用 CRS 义务经 `rho_RO` 追踪到至少一个验证目标；每个目标有验收准则和至少一个 `rho_OM`；每个 TP 至少有一个可执行 `rho_TV`；每个 VC 引用受控需求和模型目标；每次执行经 `rho_VE` 追踪到受控证据清单；每个目标满足记录经 `rho_EO` 追踪到支持证据；每个合规主张经 `rho_OC` 追踪到目标满足；时序义务必须追踪到触发/响应/取消/替代、关联键、配对/并发、端点包含性、界限、时钟启动/复位、误差预算 ID/版本、时序分区、稳健 oracle 和证据字段；悬空、退役或版本不匹配 ID 失败；核心与扩展关系可区分；覆盖报告不得删除缺失链接。

## 导出

同时提供机器可读 CSV/JSON 和生成人可读矩阵。机器可读关系集是权威源，生成视图必须记录源版本和生成命令。
