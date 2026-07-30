# Traceability Schema

Traceability is relational and many-to-many.

## Required relations

| Relation | Source | Target | Required metadata |
|---|---|---|---|
| `rho_RT` | CRS requirement | Test Purpose | obligation, rationale, reviewer |
| `rho_TV` | Test Purpose | Verification Case | coverage role, polarity, reviewer |
| `rho_RM` | CRS obligation | EFSM/model target | state/transition/data guard/clock guard/invariant/reset/timing target |
| `rho_VF` | Verification Case | fault class/operator | expected detection mechanism |
| `rho_VE` | Verification Case execution | evidence record | run and manifest IDs |

## Integrity checks

- every applicable requirement has at least one `rho_RT`;
- every requirement obligation has an adequate reviewed VC;
- every TP has at least one executable VC;
- every VC references controlled requirements and model targets;
- every timing obligation traces to its trigger/response semantics, bounds,
  clock start/reset targets, timing partitions, robust oracle, and evidence fields;
- dangling, retired, or version-mismatched IDs fail validation;
- base and extended relations are distinguishable;
- coverage reports show missing links rather than dropping them.

## Export

Use machine-readable CSV or JSON plus a human-readable generated matrix. The
machine-readable relation set is authoritative; generated views identify the
source version and generation command.

---

# 中文版

追踪关系是多对多关系：`rho_RT` 连接 CRS 与 TP，`rho_TV` 连接 TP 与 VC，`rho_RM` 连接义务与状态、转移、数据/时钟守卫、不变量、复位和时序目标，`rho_VF` 连接 VC 与故障算子，`rho_VE` 连接执行与证据。每条时序义务必须追踪到触发/响应语义、界限、时钟启动/复位、时序分区、稳健 oracle 和证据字段。缺失、悬空、退役或版本不匹配关系必须显式失败。

## 必需关系

`rho_RT` 从 CRS 到 TP 并保存义务、理由和评审者；`rho_TV` 从 TP 到 VC 并保存覆盖角色和极性；`rho_RM` 从 CRS 义务到 EFSM/模型目标；`rho_VF` 从 VC 到故障类别/算子；`rho_VE` 从 VC 执行到证据记录。

## 完整性检查

每个适用需求至少有一个 `rho_RT`，每个需求义务有充分且已评审的 VC，每个 TP 至少有一个可执行 VC，每个 VC 引用受控需求和模型目标。时序义务还必须连接触发/响应、界限、时钟启动/复位、时序分区、稳健 oracle 和证据字段。悬空、退役或版本不匹配 ID 失败；基础/扩展关系可区分；覆盖报告不得删除缺失链接。

## 导出

同时提供机器可读 CSV/JSON 和生成人可读矩阵。机器可读关系集是权威源，生成视图必须记录源版本和生成命令。
