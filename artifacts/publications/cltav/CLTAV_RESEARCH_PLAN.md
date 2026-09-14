# CL-TAV Research Plan

Reader entry for CR-2026-012. Authoritative files remain the method report, DD-028/029/030, `RESEARCH_OUTLINE.md`, SysML sources, and the protocol source-audit ledger. This page does not copy the CRS database.

## Method change summary

Successor method: Closed-Loop Test–Analysis Verification (CL-TAV). First-version direction accepted 2026-09-14 in DD-029. Combination of Test and Analysis is not a first-invention claim. Finite termination uses uniform \(c_{\min}>0\) plus finite \(B\), or finite \(K_{\max}\); `ERROR` spends the same resource.

## Thesis outline

Eight chapters. Each chapter in `docs/research/publication/RESEARCH_OUTLINE.md` states claim, CL-RQ, algorithm or architecture, required experiment, figures, what exists, and the gap. Chapter 6 is layout and metrics only; no unrun results.

## System-engineering views

SysML 1.6 notation-based PlantUML sources: `docs/research/publication/models/FIG-CL-TAV-01` through `08`. Executable or complete metamodel conformance is not claimed. Two machines: verification session \(M_{\mathrm{sess}}\) and protocol operation \(M_{\mathrm{prot}}\), joined only by interfaces and observations.

## Experiment design

Four arms CL-T, CL-A, CL-TA, CL-LOOP; detection, localization and ablation families. Register before confirmatory runs. No Configuration and no live load in this increment. No filled result numbers here.

## Expanded CRS index and audit

Current bound package still has 2796 coverage units and 384 requirements. FIND (`DEFERRED-FIND-M9`), DOWNLOAD (`DEFERRED-DOWNLOAD-M9`) and AFDX appendix units stay deferred until each source unit is re-read. Ledger: `configs/research/cltav_protocol_source_audit.json`. Do not batch-rename deferred labels. Tool software requirements are out of this PR.

## Historical versus successor evidence

The freeze-commit 94-block math check proves only that historical objects were not rewritten. It does not prove successor mathematics. `independentMathematicalApproval` and `independentReviewApproval` remain false.

# 中文版

CR-2026-012 的读者入口。权威文件仍是方法报告、DD-028／029／030、`RESEARCH_OUTLINE.md`、SysML 源和协议来源审计清单。本页不另抄 CRS 数据库。

## 方法变更摘要

后继方法：闭环测试—分析协同验证方法（CL-TAV）。首版方向于 2026-09-14 在 DD-029 接受。Test 与 Analysis 的组合不是首次发明主张。有限终止采用统一 \(c_{\min}>0\) 加有限 \(B\)，或有限 \(K_{\max}\)；`ERROR` 消耗同一资源。

## 论文大纲

八章。`docs/research/publication/RESEARCH_OUTLINE.md` 中每章写明论点、CL-RQ、算法或架构、所需实验、图、已有材料和缺口。第6章只保留布局和指标，不填未跑结果。

## 系统工程视图

SysML 1.6 记法 PlantUML 源：`docs/research/publication/models/FIG-CL-TAV-01` 至 `08`。不声称可执行或完整元模型符合性。两套机器：验证会话 \(M_{\mathrm{sess}}\) 与协议操作 \(M_{\mathrm{prot}}\)，只通过接口和观测关联。

## 实验设计

四臂 CL-T、CL-A、CL-TA、CL-LOOP；检测、定位、消融。确认性运行前登记。本增量无 Configuration、无实网加载。此处不填结果数字。

## 扩大 CRS 索引与审计

当前绑定包仍为 2796 条 coverage、384 条需求。FIND（`DEFERRED-FIND-M9`）、DOWNLOAD（`DEFERRED-DOWNLOAD-M9`）和 AFDX 附录单元在逐条重读来源前保持延期。清单：`configs/research/cltav_protocol_source_audit.json`。不得批量改名延期标签。工具软件需求不属于本 PR。

## 历史与后继证据

冻结提交上 94 块数学核验只证明历史对象未被改写，不证明后继数学正确。`independentMathematicalApproval` 与 `independentReviewApproval` 保持 false。
