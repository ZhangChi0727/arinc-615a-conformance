# ARINC 615A Conformance Verification

This repository owns the ARINC 615A **Profile, Product Binding, Project
Configuration, instance engineering, execution records and instance evidence**
used to apply a separately controlled generic verification methodology. It
develops an auditable Test-and-Analysis approach, with Review and Inspection
gates controlling artifacts and claims.

The root README is the sole human-readable current-status surface. Atomic
baselines, change requests, reviews and historical evidence remain immutable
records at commit-bound locations.

## Project architecture

```mermaid
flowchart TD
    C["Method repository<br/>Candidate GVS Core"] --> P["ARINC Conformance Profile"]
    P --> B["Product Binding"]
    B --> G["Project Configuration<br/>NOT YET ESTABLISHED"]
    G --> V["Cases · Procedures · Oracles<br/>not yet executed"]
    V --> E["Observations · Results · Evidence · Claims<br/>NOT-EXERCISED"]
    E -. "controlled instance findings" .-> F["Framework Change Proposal"]
    F -. "method review; no direct redefinition" .-> C
```

The method repository owns the Generic Core. This repository owns the ARINC
refinement and all configuration- and execution-specific artifacts. Instance
findings may support, qualify or challenge candidate method claims, but cannot
silently redefine the Core.

<!-- project-status:start -->
## Current development picture

| Dimension | Controlled state |
|---|---|
| Repository role | ARINC 615A Profile / Binding / Configuration / instance engineering and evidence owner |
| Current release | [`RB-2026-001-v4.3.1`](docs/control/baselines/RB-2026-001-v4.3.1.md) / annotated [`v4.3.1`](https://github.com/ZhangChi0727/arinc-615a-conformance/tree/v4.3.1) |
| Method input | Candidate GVS Core 0.3 at [`48dd8232b7ef`](https://github.com/ZhangChi0727/complex-system-verification-assurance/commit/48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b) |
| Protocol source | `ARINC-615A-3` / edition `615A-3` / wire version `A4` |
| Bounded source and open dependency | `ARINC-665-5`, `ARINC-664-2`, `ARINC-664-3`, `ARINC-645` (BOUNDED-ACTIVE); `ARINC-664-4`, `ARINC-664-7` (CONDITIONAL-DEPLOYMENT); ARINC-645 `OPEN-DEPENDENCY`, ARINC-664-3 `OPEN-DEPENDENCY`, ARINC-664-4 `OPEN-DEPENDENCY`, ARINC-664-7 `OPEN-DEPENDENCY`, RFC-768 `OPEN-DEPENDENCY`, RFC-791 `OPEN-DEPENDENCY`, RFC-1123 `OPEN-DEPENDENCY`, RFC-1350 `OPEN-DEPENDENCY`, RFC-1785 `OPEN-DEPENDENCY`, RFC-2347 `OPEN-DEPENDENCY`, RFC-2348 `OPEN-DEPENDENCY`, RFC-2349 `OPEN-DEPENDENCY`, RFC-1122 `OPEN-DEPENDENCY` |
| Technical direction | `LIGHTWEIGHT-OBSERVABLE-TIMED-EFSM` / `CL-TAV` / platform `deferred: TTCN-3` |
| Delivery position | current `M2` / next `M3` / disposition `ADOPT` |
| Activation boundary | merge evidence `EXTERNAL-VERIFICATION-REQUIRED` / approval `NOT-AUTOMATED` |
| Technical controls | [`source register`](configs/research/controlled_sources.json), [`activation control`](docs/control/changes/CR-2026-012.md), [`technical decisions`](docs/control/decisions/DESIGN_DECISIONS.md), [`M1 package`](configs/requirements/arinc_615a3_m1_crs.json), [`generated M1 review view`](docs/control/requirements/ARINC615A3_M1_CRS_REVIEW_VIEW.md), [`M2 package`](configs/models/arinc_615a3_m2_model.json), [`generated M2 review view`](docs/control/models/ARINC615A3_M2_MODEL_REVIEW_VIEW.md) |
| Third handshake | `COMPLETE` |
| Compatibility | `REVIEWED-COMPATIBLE-WITH-QUALIFICATION` under Q-01–Q-09 |
| Project Configuration | `NOT YET ESTABLISHED` |
| Instance evaluation | `NOT-EXERCISED` |
| RQ8 | `OPEN` |

## Current increment

**CL-TAV algorithm decomposition, authority-derived status inventory and persisted source-disposition regression**

- Execute the two closure actions registered at the PR #16 acceptance. F-A derives the current CRS inventory in the status surface from the authoritative controlled package instead of a second hand-filled copy. F-B persists the PDF-30 adjacent-CRC source-disposition negatives and positive cases through the production checker.
- Decompose the approved CL-TAV process into a readable top-level algorithm (ALG-CLTAV-01) plus ALG-CLTAV-02/03/04 and one contract appendix (F-C), with a split-versus-merged equivalence witness matrix over the frozen abstract backends. No candidate-update, stop, resource, retry or successor-summary semantics change.
- Keep protocol CRS and M2 semantics unchanged: the CRS stays M1-CANDIDATE-25 with its declared inventory, the bound M2 stays UPLOAD/INFORMATION with 65 transitions and 30 observational timing rows, and the M2 input pin stays its recorded ancestor. No M3, no capability establishment, no Project Configuration, no baseline or tag.

State changes:

- F-A, F-B and F-C are delivered on one Draft PR under CR-2026-014 / DD-035 and DD-036; M3 remains blocked.
- currentStop remains EXECUTABLE-FOUNDATION-GATE for M3 implementation.

Unchanged boundaries:

- Candidate GVS Core and compatibility-disposition identities remain separate and unchanged.
- The 18 source mapping rows, 7 instance-only rows and Q-01 through Q-09 remain unchanged.
- Project Configuration is NOT YET ESTABLISHED; instance evaluation is NOT-EXERCISED; RQ8 remains OPEN.
- Protocol conformance, certification readiness and authority acceptance remain false; no baseline or tag is created.
- This increment creates no codec, executable EFSM engine, verification case, procedure, execution evidence or Project Configuration.

## Current stop

`EXECUTABLE-FOUNDATION-GATE` — **NOT YET ESTABLISHED**: This stop still blocks M3 implementation. The bounded M2 ordinary merge is recorded; that approval is not transplanted onto expanded CRS. The CL-TAV Draft candidate is M1-CANDIDATE-25 with 615A-triggered 645 SOURCE/SEMANTIC bind, FIND abort non-waiver, bound RFC 1123/791, 664-7 latency/jitter/MAC and remaining P7 switch/Attachment-2 contracts including the VL-sum max_jitter equation, source-owned 4.7.3.2 filtering-table members, 664P4-1 address-rule leaves for the first 00519 alternative, and combined TFTP end conditions; it is not method/paper/capability/expanded-CRS approval. Independent review must pass, and merge requires explicit authorization. Do not Ready, merge or tag on this increment. The 2026-09-14 DD-029 design-direction acceptance is not independent approval.

## Next development steps

- Request complete-range RG0/RG1 and method/math/architecture/experiment review on the unique Draft PR. Keep independentMathematicalApproval and independentReviewApproval false. Do not Ready, merge, tag or start M3.
- Keep 665 section 2.3 emitted-not-closed in this PR. ARINC 645 SOURCE/SEMANTIC bind stays capability-open. Bound M2 stays UPLOAD/INFORMATION. FIND clock limited approval stays closed. Do not auto-select Part 4 or activate AFDX.

## 当前开发图景

| 维度 | 受控状态 |
|---|---|
| 仓库角色 | ARINC 615A Profile、Binding、Configuration、实例工程与证据的权威仓库 |
| 当前发布 | [`RB-2026-001-v4.3.1`](docs/control/baselines/RB-2026-001-v4.3.1.md) / annotated [`v4.3.1`](https://github.com/ZhangChi0727/arinc-615a-conformance/tree/v4.3.1) |
| 方法输入 | Candidate GVS Core 0.3 @ [`48dd8232b7ef`](https://github.com/ZhangChi0727/complex-system-verification-assurance/commit/48dd8232b7efe6b0dba3fcb75dfc154d034d2b0b) |
| 协议来源 | `ARINC-615A-3` / 版次 `615A-3` / 线版本 `A4` |
| 有边界来源与开放依赖 | `ARINC-665-5`, `ARINC-664-2`, `ARINC-664-3`, `ARINC-645` (BOUNDED-ACTIVE); `ARINC-664-4`, `ARINC-664-7` (CONDITIONAL-DEPLOYMENT)；ARINC-645 `OPEN-DEPENDENCY`, ARINC-664-3 `OPEN-DEPENDENCY`, ARINC-664-4 `OPEN-DEPENDENCY`, ARINC-664-7 `OPEN-DEPENDENCY`, RFC-768 `OPEN-DEPENDENCY`, RFC-791 `OPEN-DEPENDENCY`, RFC-1123 `OPEN-DEPENDENCY`, RFC-1350 `OPEN-DEPENDENCY`, RFC-1785 `OPEN-DEPENDENCY`, RFC-2347 `OPEN-DEPENDENCY`, RFC-2348 `OPEN-DEPENDENCY`, RFC-2349 `OPEN-DEPENDENCY`, RFC-1122 `OPEN-DEPENDENCY` |
| 技术方向 | `LIGHTWEIGHT-OBSERVABLE-TIMED-EFSM` / `CL-TAV` / 平台 `deferred: TTCN-3` |
| 交付位置 | 当前 `M2` / 下一 `M3` / 处置 `ADOPT` |
| 激活边界 | 合并证据 `EXTERNAL-VERIFICATION-REQUIRED` / 批准 `NOT-AUTOMATED` |
| 技术控制入口 | [`source register`](configs/research/controlled_sources.json), [`activation control`](docs/control/changes/CR-2026-012.md), [`technical decisions`](docs/control/decisions/DESIGN_DECISIONS.md), [`M1 package`](configs/requirements/arinc_615a3_m1_crs.json), [`generated M1 review view`](docs/control/requirements/ARINC615A3_M1_CRS_REVIEW_VIEW.md), [`M2 package`](configs/models/arinc_615a3_m2_model.json), [`generated M2 review view`](docs/control/models/ARINC615A3_M2_MODEL_REVIEW_VIEW.md) |
| 第三次握手 | `COMPLETE` |
| 兼容性 | 受 Q-01～Q-09 限定的 `REVIEWED-COMPATIBLE-WITH-QUALIFICATION` |
| Project Configuration | `NOT YET ESTABLISHED` |
| 实例评价 | `NOT-EXERCISED` |
| RQ8 | `OPEN` |

## 本次集成增量

**CL-TAV 算法分解、权威派生状态清单与来源处置回归持久化**

- 执行 PR #16 接受时登记的两项收尾动作。F-A 从权威受控包派生状态面的当前 CRS 清单，而不是第二份手填副本。F-B 经生产检查路径持久化 PDF 30 邻接 CRC 的来源处置负例与正例。
- 把已批准的 CL-TAV 过程分解为可读的总体算法（ALG-CLTAV-01）加 ALG-CLTAV-02/03/04 与一个契约附录（F-C），并在冻结抽象后端上给出拆分／合并等价性见证矩阵。候选更新、停止、资源、重试与后继摘要语义均不变。
- 协议 CRS 与 M2 语义不变：CRS 保持 M1-CANDIDATE-25 及其声明清单，绑定 M2 保持 UPLOAD／INFORMATION、65 迁移与 30 条观察时序，M2 输入钉保持既有祖先。不启动 M3，不建立能力，不建立 Project Configuration，不创建 baseline 或 tag。

状态变化：

- F-A、F-B、F-C 在唯一 Draft PR 上以 CR-2026-014／DD-035、DD-036 交付；M3 保持阻塞。
- 对 M3 实现而言 currentStop 仍为 EXECUTABLE-FOUNDATION-GATE。

保持不变的边界：

- Candidate GVS Core 与兼容性处置身份保持分离且不变。
- 18 个来源映射行、7 个实例专用行及 Q-01～Q-09 保持不变。
- Project Configuration 保持 NOT YET ESTABLISHED；实例评价保持 NOT-EXERCISED；RQ8 保持 OPEN。
- 协议符合性、认证准备度和权威接受保持 false；不创建 baseline 或 tag。
- 本增量不创建 codec、可执行 EFSM 引擎、验证用例、规程、执行证据或 Project Configuration。

## 当前停点

`EXECUTABLE-FOUNDATION-GATE` — **NOT YET ESTABLISHED**：本停点仍禁止 M3 实现。有界 M2 普通合并已记录；该批准不移植到扩大 CRS。CL-TAV Draft 候选为 M1-CANDIDATE-25，含 615A 触发的 645 来源／语义绑定、FIND 中止不豁免、已绑定的 RFC 1123／791、含 VL 求和 max_jitter 方程的 664-7 时延／抖动／MAC 及剩余交换机／附件 2 合同、4.7.3.2 过滤表来源成员、00519 第一条替代路径的 664P4-1 地址规则叶及组合后的 TFTP 结束条件，不是方法／论文／能力／扩大 CRS 批准。须通过独立评审，合并须明确授权。本增量不转 Ready、不合并、不打标签。2026-09-14 对 DD-029 的设计方向接受不是独立批准。

## 下一步开发计划

- 在唯一 Draft PR 上请求完整范围 RG0／RG1 以及方法／数学／架构／实验评审。保持 independentMathematicalApproval 与 independentReviewApproval 为 false。不转 Ready、不合并、不打标签、不启动 M3。
- 665 §2.3 在本 PR 保持已发出未闭合。ARINC 645 来源／语义绑定保持能力未建立。绑定 M2 仍为 UPLOAD／INFORMATION。FIND 时钟有限批准保持关闭。不自动选定第 4 部分，也不激活 AFDX。
<!-- project-status:end -->

## Read by role / 按角色继续阅读

| Reader | Entry | Purpose |
|---|---|---|
| General reader / 普通读者 | This README and the [current release](https://github.com/ZhangChi0727/arinc-615a-conformance/tree/v4.3.1) | purpose, achieved state and unearned claims |
| Researcher / 研究人员 | [`RESEARCH_CONTROL.md`](docs/research/RESEARCH_CONTROL.md) | method inputs, ARINC refinement, experiments and claims |
| Developer / 开发者 | [`ENGINEERING_CONTROL.md`](docs/engineering/ENGINEERING_CONTROL.md) | implementation, tests, configuration and evidence production |
| Agent | [`project-status.json`](project-status.json) | machine state, stop point, next steps and prohibited actions |
| Tutorial reader / 教程读者 | [`TUTORIAL_CONTROL.md`](docs/tutorial/TUTORIAL_CONTROL.md) | common and ARINC-specific tutorial products |
| Maintainer / 维护者 | [`PROJECT_CONTROL.md`](docs/control/PROJECT_CONTROL.md), [`CHANGE_CONTROL.md`](docs/control/CHANGE_CONTROL.md) | workflow, gates, PR and release discipline |

## Repository structure

```text
README.md                 sole human-readable current-status surface
project-status.json       machine-readable lifecycle and cross-repository state
pyproject.toml             Python package/build/test metadata
.github/                  CI and repository configuration
src/                       verification instrument source
tests/                     executable engineering and governance checks
configs/                   controlled machine-readable inputs and templates
scripts/                   synchronization and validation automation
docs/                      developer control plane and atomic records
artifacts/reports/current/ legacy report path retained for immutable references; not current status
artifacts/reports/archive/ other historical reader reports
artifacts/tutorials/       published tutorial outputs
artifacts/releases/        distributable release packages
artifacts/evidence/        generated evidence packages, normally untracked
local-references/          ignored local research inputs, never published
```

`pyproject.toml` remains at the root because packaging, editable installation,
test discovery and development tools locate it there by convention. It is
machine-facing executable configuration, not a reader report.

## Quick start

```bash
python -m pip install -e ".[dev]"
python scripts/sync_project_overview.py --check
python scripts/check_repo_baseline.py
python -m pytest tests/ -q
```

Do not commit proprietary ARINC or employer-only ICD text. A passing test suite
is engineering evidence, not by itself a conformance proof, certification
finding or scientific result.

不得提交专有 ARINC 或雇主内部 ICD 原文。测试通过属于工程证据，本身不是符合性证明、
认证结论或科学研究结果。
