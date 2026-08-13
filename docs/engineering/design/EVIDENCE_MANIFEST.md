# Execution Evidence Manifest Contract

Under `RB-2026-001-v4.3`, the Evidence Manifest is redefined as the
**Execution Evidence Manifest (EEM)**: an execution-level evidence artifact
that sits below the Objective Satisfaction Record and the Compliance Evidence
Index. An EEM alone does not satisfy an objective or support a compliance
claim; those are reviewed conclusions.

Every execution and derived analysis package records at least:

```json
{
  "manifestVersion": "1.3",
  "manifestId": "EVM-...",
  "baselineId": "RB-2026-001-v4.3",
  "sourceCommit": "40-character Git SHA",
  "standardEdition": "",
  "applicabilityId": "",
  "requirementSetId": "",
  "crsVersion": "",
  "modelId": "",
  "modelVersion": "",
  "verificationCaseSetId": "",
  "vcsVersion": "",
  "verificationCaseId": "",
  "iutVersion": "",
  "toolVersion": "",
  "environmentId": "",
  "experimentId": "",
  "upstreamArtifactRefs": [
    {
      "artifactId": "",
      "artifactVersion": "",
      "role": "requirement|model|vcs|configuration",
      "gateRecordId": ""
    }
  ],
  "claimIds": [],
  "verificationObjectiveRefs": [],
  "testArticleConformityRef": "",
  "testSetupConformityRef": "",
  "procedureConformityRef": "",
  "problemRefs": [],
  "deviationRefs": [],
  "tool": {
    "toolId": "",
    "toolVersion": "",
    "toolRole": "",
    "qualificationStatus": "NOT_CLAIMED|QUALIFICATION_REQUIRED|QUALIFIED|NOT_APPLICABLE",
    "qualificationBasisRef": ""
  },
  "runId": "",
  "executionStatus": "VALID|INCOMPLETE|ERROR",
  "seed": null,
  "startedAt": "",
  "endedAt": "",
  "clock": {
    "kind": "monotonic",
    "source": "",
    "resolutionNs": null,
    "timestampLocations": [],
    "synchronization": "",
    "errorBudget": {
      "id": "",
      "version": "",
      "environmentId": "",
      "boundNs": null,
      "combinationRule": "worst_case_sum|declared",
      "commonBiasTreatment": "",
      "components": [
        {
          "componentId": "",
          "category": "resolution|accuracy_drift|timestamp_insertion|scheduling|network_capture|software_processing|synchronization|common_bias|other",
          "source": "",
          "boundNs": null,
          "signModel": "",
          "correlationClass": "independent|shared|declared",
          "cancellationRationale": ""
        }
      ]
    }
  },
  "timingObservations": [
    {
      "obligationId": "",
      "pairingRuleRef": "",
      "obligationDisposition": "discharged|cancelled|superseded|expired",
      "triggerTimestampNs": null,
      "responseTimestampNs": null,
      "observedIntervalNs": [null, null],
      "allowedIntervalNs": [null, null],
      "verdict": "PASS|FAIL|INCONCLUSIVE|ERROR"
    }
  ],
  "verdict": "PASS|FAIL|INCONCLUSIVE|ERROR",
  "rawEvidenceRefs": [
    {
      "artifactId": "",
      "location": "repository-relative path or controlled URI",
      "sha256": "",
      "mediaType": ""
    }
  ],
  "derivedEvidenceRefs": [
    {
      "artifactId": "",
      "location": "repository-relative path or controlled URI",
      "sha256": "",
      "mediaType": "",
      "inputArtifactIds": [],
      "generatorToolVersion": ""
    }
  ],
  "deviations": [],
  "gateRecordRefs": [],
  "reviewRecord": ""
}
```

## Integrity rules

- manifests and raw artifacts are append-only after run closure;
- raw and derived evidence use stable artifact IDs, integrity hashes, and
  repository-relative paths or controlled URIs, never machine-specific absolute
  paths;
- derived artifacts reference every raw input artifact ID and the generating
  tool or script version;
- clock, reset, configuration, and tool failures cannot be hidden as PASS;
- missing mandatory provenance makes the run ERROR or evidence INCOMPLETE;
- external/private artifacts retain checksums and controlled location IDs;
- every manifest has a stable `manifestId`; cross-domain consumers cite that ID
  and the applicable upstream artifact/gate references rather than “latest”;
- timing PASS/FAIL/INCONCLUSIVE is reproducible from raw timestamps, pairing
  rules, obligation disposition, allowed bounds, and the recorded error-budget
  ID/version and components;
- a missing/invalid clock or error budget invalidates timing evidence and cannot
  be hidden by a case-level PASS;
- `NOT_CONFIRMED` test article, setup, or procedure conformity invalidates the
  execution evidence and cannot be hidden by a case-level PASS;
- open major problems referenced by `problemRefs` prevent objective satisfaction
  unless a controlled disposition explicitly allows otherwise;
- the EEM carries execution validity and case verdict only; objective status and
  compliance status belong to objective satisfaction and compliance claim
  records, and no field in the EEM promotes them automatically;
- tool qualification credit is not implied; `qualificationStatus` states the
  actual status and `NOT_CLAIMED` is the default unless an applicable
  qualification basis is established.

---

# 中文版

在 `RB-2026-001-v4.3` 下，证据清单被重定义为**执行证据清单（EEM）**：位于目标满足记录与合规证据索引之下的执行级证据产物。EEM 本身不满足目标、不支持合规主张；这些是受评审结论。

每个执行/分析包至少记录 manifest、基线、源提交、标准、适用性、需求/CRS、模型、VCS/VC 集、IUT、工具、环境、实验、运行、执行状态、种子、开始/结束、判定、门禁记录和带 hash 的原始/派生证据。v1.3 在 v1.2 基础上增加验证目标引用、测试件/装置/规程符合性引用、问题与偏差引用及工具鉴定状态，以支持面向认证的目标与关闭层。工具鉴定信用不隐含；默认 `qualificationStatus` 为 `NOT_CLAIMED`，除非在适用鉴定基础上建立。

```json
{
  "manifestVersion": "1.3",
  "manifestId": "EVM-...",
  "baselineId": "RB-2026-001-v4.3",
  "sourceCommit": "40-character Git SHA",
  "standardEdition": "",
  "applicabilityId": "",
  "requirementSetId": "",
  "crsVersion": "",
  "modelId": "",
  "modelVersion": "",
  "verificationCaseSetId": "",
  "vcsVersion": "",
  "verificationCaseId": "",
  "iutVersion": "",
  "toolVersion": "",
  "environmentId": "",
  "experimentId": "",
  "upstreamArtifactRefs": [
    {
      "artifactId": "",
      "artifactVersion": "",
      "role": "requirement|model|vcs|configuration",
      "gateRecordId": ""
    }
  ],
  "claimIds": [],
  "verificationObjectiveRefs": [],
  "testArticleConformityRef": "",
  "testSetupConformityRef": "",
  "procedureConformityRef": "",
  "problemRefs": [],
  "deviationRefs": [],
  "tool": {
    "toolId": "",
    "toolVersion": "",
    "toolRole": "",
    "qualificationStatus": "NOT_CLAIMED|QUALIFICATION_REQUIRED|QUALIFIED|NOT_APPLICABLE",
    "qualificationBasisRef": ""
  },
  "runId": "",
  "executionStatus": "VALID|INCOMPLETE|ERROR",
  "seed": null,
  "startedAt": "",
  "endedAt": "",
  "clock": {
    "kind": "monotonic",
    "source": "",
    "resolutionNs": null,
    "timestampLocations": [],
    "synchronization": "",
    "errorBudget": {
      "id": "",
      "version": "",
      "environmentId": "",
      "boundNs": null,
      "combinationRule": "worst_case_sum|declared",
      "commonBiasTreatment": "",
      "components": [
        {
          "componentId": "",
          "category": "resolution|accuracy_drift|timestamp_insertion|scheduling|network_capture|software_processing|synchronization|common_bias|other",
          "source": "",
          "boundNs": null,
          "signModel": "",
          "correlationClass": "independent|shared|declared",
          "cancellationRationale": ""
        }
      ]
    }
  },
  "timingObservations": [
    {
      "obligationId": "",
      "pairingRuleRef": "",
      "obligationDisposition": "discharged|cancelled|superseded|expired",
      "triggerTimestampNs": null,
      "responseTimestampNs": null,
      "observedIntervalNs": [null, null],
      "allowedIntervalNs": [null, null],
      "verdict": "PASS|FAIL|INCONCLUSIVE|ERROR"
    }
  ],
  "verdict": "PASS|FAIL|INCONCLUSIVE|ERROR",
  "rawEvidenceRefs": [
    {
      "artifactId": "",
      "location": "repository-relative path or controlled URI",
      "sha256": "",
      "mediaType": ""
    }
  ],
  "derivedEvidenceRefs": [
    {
      "artifactId": "",
      "location": "repository-relative path or controlled URI",
      "sha256": "",
      "mediaType": "",
      "inputArtifactIds": [],
      "generatorToolVersion": ""
    }
  ],
  "deviations": [],
  "gateRecordRefs": [],
  "reviewRecord": ""
}
```

## 完整性规则

运行关闭后 manifest 和原始产物只可追加；原始/派生证据必须使用稳定产物 ID、完整性 hash 及仓库相对路径或受控 URI，不得写机器相关绝对路径；派生产物必须引用全部原始输入 ID 和生成工具/脚本版本；时钟、重置、配置或工具故障不得隐藏为 PASS；缺少强制来源信息时运行应为 ERROR 或证据应为 INCOMPLETE；私有产物也必须保存校验和和受控位置。每份清单具有稳定 `manifestId`，跨领域消费者必须引用该 ID 及适用上游产物/门禁记录，不得引用“最新”。时序判定必须可由原始时间戳、配对规则、义务处置、允许界限和误差预算 ID/版本及分量重算，无效时钟或误差预算使时序证据无效。
