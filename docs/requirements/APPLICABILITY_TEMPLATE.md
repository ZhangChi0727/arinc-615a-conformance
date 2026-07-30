# Applicability and Observation Declaration Template

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

## 中文版

本模板用于固定 IUT 身份、角色、服务/选项、排除项、观测边界、环境和最强允许主张。时序观测必须声明来源/工具、分辨率和限制；环境假设必须记录时间源、单调时钟身份与分辨率、时间戳观测点、跨主机同步/路径假设、初始误差预算及重置能力。存在不可观测或误差界无法论证的适用义务时，应缩小主张或判为不可验证，而不是静默忽略。
