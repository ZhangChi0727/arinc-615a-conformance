# External Generic Verification Suite Binding

| Field | Value |
|---|---|
| **Binding ID** | TMP-XRB-ARINC615A-01 |
| **Candidate baseline** | RB-2026-001-v4.3 |
| **Status** | MIGRATION CANDIDATE — PENDING INDEPENDENT REVIEW |
| **Method repository** | `ZhangChi0727/complex-system-verification-assurance` |
| **MethodDefinitionCommit** | `48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b` |
| **Compatibility** | NOT-DETERMINED |
| **Instance evaluation** | NOT-EXERCISED |

## 1. Purpose and authority boundary

This record binds the ARINC 615A migration candidate to one immutable Candidate
Generic Verification Suite (GVS) Core definition. The external method repository
is authoritative for generic method definitions. This repository is authoritative
only for the ARINC 615A Profile, Product Binding, Project Configuration, instance
engineering, instance research, and instance evidence.

The binding does not copy generic ownership into this repository, certify the
ARINC 615A instance, establish compatibility, or report an exercised evaluation.
Method material is consumed as **EXTERNAL / READ-ONLY / OPEN-CANDIDATE**.

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

## 3. Instance identity tuple

| Identity element | Controlled value |
|---|---|
| Method instance | `TMP-ARINC615A-01` |
| Conformance target profile | `TMP-CTP-ARINC615A-01`, version `0.1-candidate` |
| Product binding | `TMP-PB-ARINC615A-01`, version `0.1-candidate` |
| Project configuration | `TMP-PC-ARINC615A-01`, status `NOT YET ESTABLISHED` |
| Cross-repository binding | `TMP-XRB-ARINC615A-01` |
| Effective ARINC release | `RB-2026-001-v4.2.1` |
| Effective ARINC tag commit | `3299e6dae83424862f75a4c1d09b91b80d9d8b00` |
| Candidate starting head | `53a98447bcfa862f082ce443d69115067d3ff2f1` |
| Candidate PR | [PR #9](https://github.com/ZhangChi0727/arinc-615a-conformance/pull/9) |

The effective release, candidate starting head, and eventual candidate release
commit are distinct provenance fields and must not be substituted for one
another.

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
profile/binding/configuration and instance-mapping contracts. Until those
candidate contracts pass independent review, no migration claim is earned.

## 5. Status, limitations, and rollback

Compatibility remains **NOT-DETERMINED** and evaluation remains
**NOT-EXERCISED**. The record establishes referential identity only. It neither
asserts that the current artifacts satisfy the external contract nor upgrades
historical evidence, assurance, research maturity, or authority acceptance.

If any immutable locator, repository identity, temporary identifier, ownership
boundary, or migration mapping is found inconsistent, stop migration, retain
PR #9 as Draft, revert the correction commit that introduced the inconsistency,
and open a controlled change before proceeding. Proprietary ARINC text and
employer-only material must not be copied into either repository.

---

# 中文版

# 外部通用验证套件绑定

| 字段 | 值 |
|---|---|
| **绑定 ID** | TMP-XRB-ARINC615A-01 |
| **候选基线** | RB-2026-001-v4.3 |
| **状态** | 迁移候选——等待独立评审 |
| **方法仓库** | `ZhangChi0727/complex-system-verification-assurance` |
| **MethodDefinitionCommit** | `48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b` |
| **兼容性** | NOT-DETERMINED（未确定） |
| **实例评价** | NOT-EXERCISED（未执行） |

## 1. 目的与权威边界

本记录把 ARINC 615A 迁移候选绑定到唯一、不可变的 Candidate GVS Core
定义。外部方法仓库对通用方法定义负责；本仓库只对 ARINC 615A Profile、
Product Binding、Project Configuration、实例工程、实例研究和实例证据负责。

该绑定不把通用对象的所有权复制到本仓库，不证明实例兼容，不取得认证信用，也不声称
完成了实例评价。方法材料以“外部、只读、开放候选”状态使用。

## 2. 不可变方法定位符

| 方法对象 | 版本 | 提交绑定定位符 |
|---|---:|---|
| Candidate GVS Core | 0.3 | [generic_verification_suite_core.md](https://github.com/ZhangChi0727/complex-system-verification-assurance/blob/48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b/docs/02_verification_framework/generic_verification_suite_core.md) |
| 跨仓库实例契约 | 0.2 | [cross_repository_instance_contract.md](https://github.com/ZhangChi0727/complex-system-verification-assurance/blob/48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b/docs/08_validation/cross_repository_instance_contract.md) |
| ARINC 615A 对象映射登记册 | 0.2 | [arinc_615a_object_mapping_register.md](https://github.com/ZhangChi0727/complex-system-verification-assurance/blob/48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b/docs/08_validation/arinc_615a_object_mapping_register.md) |
| ARINC 615A 实例评价协议 | 0.2 | [arinc_615a_instance_evaluation_protocol.md](https://github.com/ZhangChi0727/complex-system-verification-assurance/blob/48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b/docs/08_validation/arinc_615a_instance_evaluation_protocol.md) |
| 实例登记册 | 0.2 | [instance_registry.md](https://github.com/ZhangChi0727/complex-system-verification-assurance/blob/48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b/docs/08_validation/instance_registry.md) |

分支名和 `main` 链接仅供发现，不构成绑定身份。改用其它方法提交必须经过显式基线变更。

## 3. 实例身份元组

| 身份要素 | 受控值 |
|---|---|
| 方法实例 | `TMP-ARINC615A-01` |
| 符合性目标 Profile | `TMP-CTP-ARINC615A-01`，版本 `0.1-candidate` |
| Product Binding | `TMP-PB-ARINC615A-01`，版本 `0.1-candidate` |
| Project Configuration | `TMP-PC-ARINC615A-01`，状态 `NOT YET ESTABLISHED` |
| 跨仓库绑定 | `TMP-XRB-ARINC615A-01` |
| 当前有效 ARINC 发布 | `RB-2026-001-v4.2.1` |
| 当前有效 ARINC 标签提交 | `3299e6dae83424862f75a4c1d09b91b80d9d8b00` |
| 候选起始 head | `53a98447bcfa862f082ce443d69115067d3ff2f1` |
| 候选 PR | [PR #9](https://github.com/ZhangChi0727/arinc-615a-conformance/pull/9) |

当前有效发布、候选起始 head 和未来候选发布提交是三个不同的来源字段，不得相互替代。

## 4. 迁移语义

- L0–L7 是 ARINC 615A Profile 分解标签，除非未来被正式接受的通用方法修订明确采纳；
- A0–A4、R0–R5、RG 和 G 是候选 ARINC Profile/项目生命周期状态或门，不是 Generic GVS Core 语义；
- VO 针对绑定产品和配置细化 Profile 义务；OSR 记录实例处置，但不重定义通用方法对象；
- CEI 是实例追踪索引，Evidence Manifest 保留执行来源；二者均不构成兼容性证明或认证信用；
- Test Conformity 与 Problem Closure 记录属于项目保证控制。

详细对象映射和所有权规则由配套的 Profile/Binding/Configuration 及实例映射契约规定。
这些候选契约通过独立评审前，不获得迁移主张。

## 5. 状态、限制与回滚

兼容性保持 **NOT-DETERMINED**，评价保持 **NOT-EXERCISED**。本记录只建立引用身份，
不声称当前产物已经满足外部契约，也不晋级历史证据、保证状态、研究成熟度或权威接受状态。

如不可变定位符、仓库身份、临时 ID、所有权边界或迁移映射存在不一致，应停止迁移、保持
PR #9 为 Draft、回退引入不一致的 correction commit，并在继续前发起受控变更。不得向任一
仓库复制专有 ARINC 原文或雇主内部材料。
