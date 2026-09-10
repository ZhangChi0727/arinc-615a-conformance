# Model Schema

The M2 candidate uses one authoritative package,
`configs/models/arinc_615a3_m2_model.json`, one closed schema, and one generated
bilingual review view. M1 remains the immutable CRS input. M2 does not copy the
requirement list and does not implement a protocol engine.

## Form

The machine is M = (S, s0, V, C, P, E, T, Inv).

- S is the finite set of control states; s0 is the unique initial state.
- V is typed variables; C is clocks; P is parameters; E is events.
- T is transitions (source, event, guard, updates, resets, outputs, target)
  plus source/obligation references.
- Inv is a state invariant that holds during delay in that state.
- Roles, locators and review metadata are controlled fields; they are not
  implicit.

Delay lets clocks in C grow while variables in V stay unchanged. A discrete
step evaluates guard, then updates, then clock resets, then outputs, then the
target. Outputs are instantaneous on the named channel.

## Observation and composition

UPLOAD and INFORMATION share one machine. Data Loader and Target Hardware are
observation projections of the same variables and clocks, not two unsynchronized
swimlanes. Send and receive of the same message cannot be swapped. Local
evaluation is not claimed as network-visible. Absence of a captured packet is
not protocol silence unless the observation window, correlation key and clock
are declared.

## Time, clocks and concurrency

Each in-scope timing obligation records trigger, response, cancel, supersede,
correlation key, clock and resets, bound kind, endpoint inclusivity, unit,
source evidence, observation window and error-budget class. Fixed constants,
message parameters, configuration parameters, symbolic equations and examples
remain distinct. Missing, unresolved and unbounded bounds are not collapsed to
null. Timeout events compete with packet events without a forged priority.
Simultaneous same-channel events are environment nondeterminism. Closed
endpoints include equality.

Measurement error is a parameterized M6 instance budget. Network delay is not
instrument error. No unsourced independent clock-sync assumption is adopted.
This candidate does not ship an execution oracle.

## Expressions

Guards, updates, invariants and timing expressions use a restricted AST:
TRUE, COMPARE, AND, VAR, CLOCK, SYMBOL, LITERAL, ENUM, ASSIGN, PAYLOAD and
BINARY with ADD, SUB, MUL and DIV. APPLICATION payload fields are typed on the
stimulating event and evaluated in the guard before variable updates. Arbitrary
strings are not evaluated. Timeout and WAIT-elapsed events are enabled only by
COMPARE(enablingCompare) between enablingClock and enablingBound. Unresolved
symbolic bounds remain NOT-CHECKED or UNRESOLVED; they are not PASS. Source
equations keep the source comparison operator and the ordered source expression
structure, including retry and network-transmission terms. Same-operator ADD and
MUL may be flattened and reordered; comparison direction, SUB/DIV order, mixed
grouping and literals stay fixed. WAIT retry is a not-before lower bound.
LUR WRQ requires a session-local list-ready flag established only by LUS 0001.

## Automatic checks

Automation checks the nested closed schema, fail-closed git object identity,
M1-bound field/status axes, RFC atomic-part locators, discrete-step witnesses
including list-offered-not-ready, source-equation structure against the M1
relation, partition, polarity, graph connectivity, sequence constraints, restricted
expressions, capability guards and fingerprint refresh.
It cannot prove proprietary source fidelity, timed reachability or
implementation conformance. Static untimed connectivity is limited to the
declared graph. OPEN-M1-CORRECTION keeps blocksFinalApproval true. After a
successor M1 delta authorized by CR-2026-009 and executed under CR-2026-011,
those identities may be CLOSED-BY-SUCCESSOR-M1-DELTA; reviewControl still
blocks final approval until independent RG1 accepts. Successor inputAcceptance
does not transplant the frozen merge approval.

## Non-claims

M2 does not establish Project Configuration, behavior capabilities, AFDX,
FIND, integrity algorithms or IUT PASS/FAIL. RG0, incremental RG1 and RG2 remain
external. reviewHead stays UNBOUND-DRAFT on the candidate.

# 中文版

# 模型 Schema

M2 候选使用一个权威数据包 `configs/models/arinc_615a3_m2_model.json`、一个封闭
schema 和一个生成的双语评审视图。M1 仍为不可变 CRS 输入。M2 不复制需求清单，
也不实现协议引擎。

## 形式

机器为 M = (S, s0, V, C, P, E, T, Inv)。

- S 为有限控制状态；s0 为唯一初态。
- V 为有类型变量；C 为时钟；P 为参数；E 为事件。
- T 为迁移（源、事件、守卫、更新、复位、输出、目标）并附来源／义务引用。
- Inv 为该状态下延时成立的不变量。
- 角色、定位和评审元数据是受控字段，不得隐式省略。

延时时 C 中时钟增长而 V 中变量不变。离散步骤依次求值守卫、更新、时钟复位、
输出，然后进入目标。输出在具名通道上瞬时发生。

## 观测与组合

UPLOAD 与 INFORMATION 共享一台机器。数据加载器与目标硬件是同一组变量和时钟
的观测投影，不是两张互不同步的泳道。同一消息的发送与接收不能互换。本地评价
不声称网络可见。未采到报文不是协议静默，除非已声明观测窗口、关联键和时钟。

## 时间、时钟与并发

每项范围内时序义务记录触发、响应、取消、替代、关联键、时钟与复位、边界种类、
端点包含性、单位、来源证据、观测窗口和误差预算类别。固定常量、消息参数、配置
参数、符号方程与示例保持区分。缺失、未解析与无界不得都写成 null。超时事件与
报文事件竞争，不伪造优先级。同一通道同时事件视为环境非确定性。闭端点包含相等。

测量误差是参数化的 M6 实例预算。网络时延不是仪表误差。不采用无来源的独立时钟
同步假设。本候选不交付执行 oracle。

## 表达式

守卫、更新、不变量和时序表达式使用受限 AST：TRUE、COMPARE、AND、VAR、CLOCK、
SYMBOL、LITERAL、ENUM、ASSIGN、PAYLOAD 以及 ADD/SUB/MUL/DIV 的 BINARY。
APPLICATION 的 payload 字段在刺激事件上有类型，并在变量更新之前参与守卫求值。
禁止对任意字符串求值。超时与 WAIT 到期事件仅由 enablingClock 与 enablingBound
之间的 COMPARE(enablingCompare) 使能。未解析符号边界保持 NOT-CHECKED 或
UNRESOLVED，不是 PASS。来源方程保留来源比较算子及有序来源表达式结构，包括重试与网络传输项。同一算子
的 ADD／MUL 可扁平化并重排；比较方向、SUB／DIV 次序、混合分组与常量保持固定。
WAIT 重试是不得早于的下界。LUR WRQ 要求仅由 LUS 0001 建立的会话内列表就绪标志。

## 自动检查

自动化检查完整嵌套封闭 schema、fail-closed 的 Git 对象身份、与 M1 绑定的字段／
状态轴、RFC 原子片段定位、离散步见证（含列表已提交但未就绪）、按 M1 关系检查
来源方程结构、分区、极性、图连通、顺序约束、受限
表达式、能力守卫和指纹刷新。不能证明专有来源忠实度、定时可达或实现符合性。
静态无时时连通仅限于已声明图。OPEN-M1-CORRECTION 使 blocksFinalApproval 保持
为真。CR-2026-009 授权并由 CR-2026-011 执行的后继 M1 增量可将这些身份记为
CLOSED-BY-SUCCESSOR-M1-DELTA；reviewControl 在独立 RG1 接受前仍阻止最终批准。
后继 inputAcceptance 不移植冻结合并批准。

## 非主张

M2 不建立 Project Configuration、行为能力、AFDX、FIND、完整性算法或 IUT
PASS/FAIL。RG0、增量 RG1 与 RG2 仍为外部评审。候选上 reviewHead 保持
UNBOUND-DRAFT。
