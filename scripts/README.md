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
versions in key documents, per-language report structure, mathematical
delimiters, numeric and timed equation numbering, and legacy/parallel filenames.

---

## 中文版

脚本用于 schema/追踪验证、受控执行和证据采集、故障生成、原始到派生复现、报告生成及仓库一致性检查。`check_repo_baseline.py` 检查关键文档末尾附有中文版、报告中英文结构一致、普通公式 1–14 和时序公式 T1–T5 完整、数学/代码块闭合、本地链接有效，并禁止遗留或平行中文报告文件。以下划线开头的一次性历史脚本不属于冻结研究管线。
