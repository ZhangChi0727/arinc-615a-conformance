# Applicability and Observation Declaration Template

## M1 Profile-level declaration

M1 declares source identities, roles, services/operations, included, excluded
and deferred behavior, and observation classes without inventing an IUT. Every
registered source PDF page is either inside a controlled section span or an
explicit exclusion range. Each
requirement uses exactly one observation classification:
`OBSERVABLE-IN-PRINCIPLE`, `CONFIGURATION-DEPENDENT`,
`INTERNAL-NOT-OBSERVABLE`, `DEPENDENCY-BLOCKED`, or `UNRESOLVED`. The strongest
M1 conclusion is only that a CRS/applicability candidate has been formed.

## Future Project Configuration declaration

The fields below are retained for M6. They must not be instantiated during M1.

| Field | Value |
|---|---|
| **Artifact ID** | APP-YYYY-NNN |
| **Version** | |
| **Status** | Draft |
| **Standard edition** | |
| **Baseline** | RB-2026-001-v4.2 |
| **Owner** | |
| **RG0 record** | |

## IUT identity and configuration

- implementation/version:
- role(s):
- hardware/OS/runtime:
- configuration checksum:

## Included services and behavior

| Service/option | Role | Supported | Applicability rationale |
|---|---|---:|---|
| DOWNLOAD | | | |
| UPLOAD | | | |

## Declared exclusions

Record the exact exclusion, standard source, rationale, and effect on claims.

## Observation boundary

| Observable | Source/tool | Resolution | Limitation |
|---|---|---|---|
| Network packets | | | |
| Timing | | | |
| IUT logs | | | |
| Files/content | | | |
| External state | | | |

## Environment assumptions

- network topology and impairment controls:
- protocol peer/reference model:
- time source:
- monotonic clock identity and resolution:
- timestamp observation points:
- clock synchronization/path assumptions:
- preliminary measurement-error budget:
- reset/isolation capability:
- external standards/data constraints:

## Claim boundary

State the strongest claim this declaration permits and list unresolved
observability or applicability questions.

## Review

- reviewers:
- findings:
- residual risks:
- decision: `APPROVE` / `APPROVE WITH ACTIONS` / `REWORK`

---

# 中文版

## M1 Profile 层声明

M1 只声明来源身份、角色、服务／操作、纳入／排除／延期行为和观测分类，不虚构 IUT。登记来源的每一 PDF 页必须落入受控 section span 或明确排除区间。每项需求只能采用 `OBSERVABLE-IN-PRINCIPLE`、`CONFIGURATION-DEPENDENT`、`INTERNAL-NOT-OBSERVABLE`、`DEPENDENCY-BLOCKED` 或 `UNRESOLVED` 之一。M1 允许的最强结论仅为已形成 CRS／适用性候选。

## 未来 Project Configuration 声明

下列 IUT、平台、工具、时钟、拓扑和 checksum 字段保留到 M6；M1 不得实例化。

本模板用于固定 IUT 身份、角色、服务/选项、排除项、观测边界、环境和最强允许主张。时序观测必须声明来源/工具、分辨率和限制；环境假设必须记录时间源、单调时钟身份与分辨率、时间戳观测点、跨主机同步/路径假设、初始误差预算及重置能力。存在不可观测或误差界无法论证的适用义务时，应缩小主张或判为不可验证，而不是静默忽略。

## IUT 身份与配置

记录实现/版本、角色、硬件/操作系统/运行时和配置校验和。

## 纳入的服务与行为

逐项记录 DOWNLOAD、UPLOAD 等服务/选项、角色、是否支持以及适用性理由。

## 明确排除

记录确切排除项、标准来源、理由及其对主张的影响。

## 观测边界

对网络包、时序、IUT 日志、文件/内容和外部状态，记录观测来源/工具、分辨率和局限。

## 环境假设

记录网络拓扑与干扰控制、协议对端/参考模型、时间源、单调时钟身份和分辨率、时间戳位置、同步/路径假设、初步误差预算、重置/隔离能力及外部标准/数据约束。

## 主张边界

声明该适用性文件允许的最强主张，并列出尚未解决的可观测性或适用性问题。

## 评审

记录评审者、发现、剩余风险和 `APPROVE`、`APPROVE WITH ACTIONS` 或 `REWORK` 决定。
