# Scripts

Automation scripts should support one of:

- schema and traceability validation;
- controlled execution and evidence capture;
- mutation/fault generation with registered seeds;
- raw-to-derived analysis reproduction;
- report/table generation;
- repository link and baseline consistency checks.

Each research script records its inputs, outputs, version, and deterministic
settings. Historical one-off PR/review scripts beginning with `_` are not part
of the frozen research pipeline unless promoted through review.

Current controlled check:

```bash
python scripts/check_repo_baseline.py
```

It validates required baseline files, local document links, appended Chinese
versions and structural parity in controlled documents, mathematical delimiters,
numeric and timed equation numbering, the methodology-directory migration, and
required architecture/traceability contract terms. Ignored local research
sources are outside the public-baseline link graph.

---

# 中文版

脚本用于 schema/追踪验证、受控执行和证据采集、故障生成、原始到派生复现、报告生成及仓库一致性检查。`check_repo_baseline.py` 检查关键文档末尾附有中文版、报告中英文结构一致、普通公式 1–14 和时序公式 T1–T5 完整、数学/代码块闭合、本地链接有效，并禁止遗留或平行中文报告文件。以下划线开头的一次性历史脚本不属于冻结研究管线。

当前受控检查：

```bash
python scripts/check_repo_baseline.py
```

它还验证全部双语受控文档使用统一 H1 边界，并对中英文 H2/H3、数学块、公式标签和代码围栏执行结构对等检查，同时检查方法论目录迁移以及架构/追踪契约的关键字段。本地忽略的研究素材不进入公开基线链接图。结构门禁不能证明翻译语义正确，语义对等仍必须记录在逐文件人工评审清单中。
