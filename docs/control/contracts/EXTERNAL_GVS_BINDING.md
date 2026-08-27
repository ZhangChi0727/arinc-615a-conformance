# External Generic Verification Suite Binding

| Field | Value |
|---|---|
| **Binding ID** | TMP-XRB-ARINC615A-01 |
| **Candidate baseline** | RB-2026-001-v4.3.1 |
| **Status** | THIRD-HANDSHAKE ACKNOWLEDGEMENT CANDIDATE — PENDING INDEPENDENT REVIEW |
| **Method repository** | `ZhangChi0727/complex-system-verification-assurance` |
| **MethodDefinitionCommit** | `48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b` |
| **MethodCompatibilityDispositionCommit** | `c02330d21fe2d3e89e7e2d6352872d52461a6dda` |
| **Compatibility** | REVIEWED-COMPATIBLE-WITH-QUALIFICATION — Q-01–Q-09 |
| **Instance evaluation** | NOT-EXERCISED |
| **Project Configuration** | NOT YET ESTABLISHED |

## 1. Purpose and authority boundary

This record binds the ARINC 615A acknowledgement candidate to the immutable
Candidate Generic Verification Suite (GVS) Core definition and, separately, to
the reviewed third-handshake disposition. The external method repository is
authoritative for generic method definitions and compatibility disposition.
This repository is authoritative only for the ARINC 615A Profile, Product
Binding, Project Configuration, instance engineering, instance research, and
instance evidence.

The binding does not copy generic ownership into this repository, certify the
ARINC instance, or report an exercised evaluation. It acknowledges only the
qualified compatibility disposition recorded by the method repository. Method
material remains **EXTERNAL / READ-ONLY / OPEN-CANDIDATE**.

## 2. Immutable method locators

| Method object | Version | Commit-bound locator |
|---|---:|---|
| Candidate GVS Core | 0.3 | [generic_verification_suite_core.md](https://github.com/ZhangChi0727/complex-system-verification-assurance/blob/48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b/docs/02_verification_framework/generic_verification_suite_core.md) |
| Cross-repository instance contract | 0.2 | [cross_repository_instance_contract.md](https://github.com/ZhangChi0727/complex-system-verification-assurance/blob/48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b/docs/08_validation/cross_repository_instance_contract.md) |
| ARINC 615A object mapping register | 0.2 | [arinc_615a_object_mapping_register.md](https://github.com/ZhangChi0727/complex-system-verification-assurance/blob/48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b/docs/08_validation/arinc_615a_object_mapping_register.md) |
| ARINC 615A instance evaluation protocol | 0.2 | [arinc_615a_instance_evaluation_protocol.md](https://github.com/ZhangChi0727/complex-system-verification-assurance/blob/48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b/docs/08_validation/arinc_615a_instance_evaluation_protocol.md) |
| Instance registry | 0.2 | [instance_registry.md](https://github.com/ZhangChi0727/complex-system-verification-assurance/blob/48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b/docs/08_validation/instance_registry.md) |

Branch names and `main` URLs are discovery aids only and are not binding
identities. A different method commit requires an explicit baseline change.

### 2.1 Reviewed disposition identity

The locators above remain bound to MethodDefinitionCommit
`48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b`. The separate reviewed disposition
is bound to MethodCompatibilityDispositionCommit
`c02330d21fe2d3e89e7e2d6352872d52461a6dda` and its
[commit-bound compatibility record](https://github.com/ZhangChi0727/complex-system-verification-assurance/blob/c02330d21fe2d3e89e7e2d6352872d52461a6dda/docs/08_validation/arinc_615a_third_handshake_compatibility_disposition.md).
The method merge is an ordinary two-parent merge whose second parent is the
approved head `37fb88329abaea8f7127da96a66c0ac5d7525543`. The associated named review
is recorded truthfully as GitHub platform state `COMMENTED` with body outcome
`APPROVE`; it is not represented as a platform-native `APPROVED` review.

## 3. Instance identity tuple

| Identity element | Controlled value |
|---|---|
| Method instance | `TMP-ARINC615A-01` |
| Conformance target profile | `TMP-CTP-ARINC615A-01`, version `0.1-candidate` |
| Product binding | `TMP-PB-ARINC615A-01`, version `0.1-candidate` |
| Project configuration | `TMP-PC-ARINC615A-01`, status `NOT YET ESTABLISHED` |
| Cross-repository binding | `TMP-XRB-ARINC615A-01` |
| Assessed ARINC release tag | `v4.3` |
| Assessed ARINC release commit | `523d42bf03a1135b3d63a00bfb47d3b879d3927e` |
| Candidate acknowledgement baseline | `RB-2026-001-v4.3.1` |
| Method disposition commit | `c02330d21fe2d3e89e7e2d6352872d52461a6dda` |
| Candidate acknowledgement PR | PR #10, assigned when published |

The assessed ARINC release, method definition, method disposition, and eventual
acknowledgement merge are distinct provenance fields and must not be substituted
for one another.

## 4. Migration semantics

- L0–L7 are ARINC 615A Profile decomposition labels unless a future accepted
  generic method revision explicitly adopts them.
- A0–A4, R0–R5, RG identifiers, and G identifiers are candidate ARINC
  Profile/project lifecycle states and gates; they are not Generic GVS Core
  semantics.
- Verification Objectives (VOs) refine profile obligations for a bound product
  and configuration; Objective Satisfaction Records (OSRs) record instance
  dispositions without redefining generic method objects.
- The Compliance Evidence Index (CEI) is an instance trace index. Evidence
  Manifests retain execution provenance. Neither is generic proof of
  compatibility or certification credit.
- Test Conformity and Problem Closure records are project assurance controls.

Detailed object mapping and ownership rules are established in the companion
profile/binding/configuration and instance-mapping contracts. The method review
confirmed the mapping only with Q-01–Q-09; this local acknowledgement remains a
Draft candidate until its own independent review and ordinary merge.

## 5. Status, limitations, and rollback

Compatibility is **REVIEWED-COMPATIBLE-WITH-QUALIFICATION**, subject to all
Q-01–Q-09 in [`CR-2026-005`](../changes/CR-2026-005.md#mandatory-qualifications).
Evaluation remains **NOT-EXERCISED** and Project Configuration remains
**NOT YET ESTABLISHED**. This disposition upgrades no historical evidence,
assurance, research maturity, protocol conclusion, certification, or authority
acceptance.

If any immutable locator, repository identity, temporary identifier, ownership
boundary, qualification, or migration mapping is inconsistent, stop the
acknowledgement and keep its PR Draft. Revert the correction that introduced the
inconsistency and open a controlled change. Proprietary ARINC text and
employer-only material must not be copied into either repository.

---

# 中文版

# 外部通用验证套件绑定

| 字段 | 值 |
|---|---|
| **绑定 ID** | TMP-XRB-ARINC615A-01 |
| **候选基线** | RB-2026-001-v4.3.1 |
| **状态** | 第三次握手确认候选——等待独立评审 |
| **方法仓库** | `ZhangChi0727/complex-system-verification-assurance` |
| **MethodDefinitionCommit** | `48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b` |
| **MethodCompatibilityDispositionCommit** | `c02330d21fe2d3e89e7e2d6352872d52461a6dda` |
| **兼容性** | REVIEWED-COMPATIBLE-WITH-QUALIFICATION——受 Q-01–Q-09 限定 |
| **实例评价** | NOT-EXERCISED（未执行） |
| **Project Configuration** | NOT YET ESTABLISHED（尚未建立） |

## 1. 目的与权威边界

本记录把 ARINC 615A 确认候选分别绑定到不可变 Candidate GVS Core 定义与受评审的第三次
握手处置。外部方法仓库对通用方法定义和兼容性处置负责；本仓库只对 ARINC 615A Profile、
Product Binding、Project Configuration、实例工程、实例研究和实例证据负责。

该绑定不把通用对象所有权复制到本仓库，不证明认证，也不声称完成实例评价；它只确认方法
仓库记录的限定兼容性处置。方法材料保持“外部、只读、开放候选”。

## 2. 不可变方法定位符

| 方法对象 | 版本 | 提交绑定定位符 |
|---|---:|---|
| Candidate GVS Core | 0.3 | [generic_verification_suite_core.md](https://github.com/ZhangChi0727/complex-system-verification-assurance/blob/48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b/docs/02_verification_framework/generic_verification_suite_core.md) |
| 跨仓库实例契约 | 0.2 | [cross_repository_instance_contract.md](https://github.com/ZhangChi0727/complex-system-verification-assurance/blob/48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b/docs/08_validation/cross_repository_instance_contract.md) |
| ARINC 615A 对象映射登记册 | 0.2 | [arinc_615a_object_mapping_register.md](https://github.com/ZhangChi0727/complex-system-verification-assurance/blob/48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b/docs/08_validation/arinc_615a_object_mapping_register.md) |
| ARINC 615A 实例评价协议 | 0.2 | [arinc_615a_instance_evaluation_protocol.md](https://github.com/ZhangChi0727/complex-system-verification-assurance/blob/48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b/docs/08_validation/arinc_615a_instance_evaluation_protocol.md) |
| 实例登记册 | 0.2 | [instance_registry.md](https://github.com/ZhangChi0727/complex-system-verification-assurance/blob/48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b/docs/08_validation/instance_registry.md) |

分支名和 `main` 链接仅供发现，不构成绑定身份。改用其它方法提交必须经过显式基线变更。

### 2.1 受评审处置身份

上述定义定位符保持绑定 MethodDefinitionCommit
`48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b`。独立的受评审处置绑定
MethodCompatibilityDispositionCommit `c02330d21fe2d3e89e7e2d6352872d52461a6dda` 及其
[提交绑定兼容性记录](https://github.com/ZhangChi0727/complex-system-verification-assurance/blob/c02330d21fe2d3e89e7e2d6352872d52461a6dda/docs/08_validation/arinc_615a_third_handshake_compatibility_disposition.md)。
方法合并是普通两父合并，第二父为已批准 head
`37fb88329abaea8f7127da96a66c0ac5d7525543`。关联的具名评审如实记录为 GitHub 平台状态
`COMMENTED`、Review 正文结论 `APPROVE`；不得将其表述为 GitHub 平台原生
`APPROVED` 评审。

## 3. 实例身份元组

| 身份要素 | 受控值 |
|---|---|
| 方法实例 | `TMP-ARINC615A-01` |
| 符合性目标 Profile | `TMP-CTP-ARINC615A-01`，版本 `0.1-candidate` |
| Product Binding | `TMP-PB-ARINC615A-01`，版本 `0.1-candidate` |
| Project Configuration | `TMP-PC-ARINC615A-01`，状态 `NOT YET ESTABLISHED` |
| 跨仓库绑定 | `TMP-XRB-ARINC615A-01` |
| 被评价 ARINC 发布标签 | `v4.3` |
| 被评价 ARINC 发布提交 | `523d42bf03a1135b3d63a00bfb47d3b879d3927e` |
| 候选确认基线 | `RB-2026-001-v4.3.1` |
| 方法处置提交 | `c02330d21fe2d3e89e7e2d6352872d52461a6dda` |
| 候选确认 PR | PR #10，发布时确定 |

被评价 ARINC 发布、方法定义、方法处置和未来确认合并是不同来源字段，不得相互替代。

## 4. 迁移语义

- L0–L7 是 ARINC 615A Profile 分解标签，除非未来被正式接受的通用方法修订明确采纳；
- A0–A4、R0–R5、RG 和 G 是候选 ARINC Profile/项目生命周期状态或门，不是 Generic GVS Core 语义；
- VO 针对绑定产品和配置细化 Profile 义务；OSR 记录实例处置，但不重定义通用方法对象；
- CEI 是实例追踪索引，Evidence Manifest 保留执行来源；二者均不构成兼容性证明或认证信用；
- Test Conformity 与 Problem Closure 记录属于项目保证控制。

详细对象映射和所有权规则由配套的 Profile/Binding/Configuration 及实例映射契约规定。
方法评审只在 Q-01–Q-09 限定下确认映射；本地确认在自身独立评审与普通合并前仍为 Draft 候选。

## 5. 状态、限制与回滚

兼容性为 **REVIEWED-COMPATIBLE-WITH-QUALIFICATION**，受
[`CR-2026-005`](../changes/CR-2026-005.md#强制限定) 的 Q-01–Q-09 全部限定。评价保持
**NOT-EXERCISED**，Project Configuration 保持 **NOT YET ESTABLISHED**。该处置不晋级
历史证据、保证状态、研究成熟度、协议结论、认证或权威接受。

如不可变定位符、仓库身份、临时 ID、所有权边界、限定或迁移映射不一致，应停止确认并保持
其 PR 为 Draft；回退引入不一致的修正并发起受控变更。不得向任一仓库复制专有 ARINC 原文
或雇主内部材料。
