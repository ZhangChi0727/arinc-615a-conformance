# Evidence Manifest Contract

Every execution and derived analysis package records at least:

```json
{
  "manifestVersion": "1.2",
  "manifestId": "EVM-...",
  "baselineId": "RB-2026-001-v4.2",
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
  be hidden by a case-level PASS.

---

# 中文版

每个执行/分析包至少记录 manifest、基线、源提交、标准、适用性、需求/CRS、模型、VCS/VC 集、IUT、工具、环境、实验、运行、执行状态、种子、开始/结束、判定、门禁记录和带 hash 的原始/派生证据。v1.2 在 v1.1 时序字段基础上增加稳定 `manifestId`、上游产物/版本/门禁引用和下游主张 ID，以支持跨领域追踪。时序结论必须能由原始时间戳、配对规则、义务处置、界限和具名版本误差预算重算；无效时间链不能被总体 PASS 掩盖。

```json
{
  "manifestVersion": "1.2",
  "manifestId": "EVM-...",
  "baselineId": "RB-2026-001-v4.2",
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
