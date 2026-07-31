# Evidence Manifest Contract

Every execution and derived analysis package records at least:

```json
{
  "manifestVersion": "1.2",
  "manifestId": "EVM-...",
  "baselineId": "RB-2026-001-v4.2",
  "standardEdition": "",
  "applicabilityId": "",
  "crsVersion": "",
  "modelVersion": "",
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
      "boundNs": null,
      "components": []
    }
  },
  "timingObservations": [
    {
      "obligationId": "",
      "triggerTimestampNs": null,
      "responseTimestampNs": null,
      "observedIntervalNs": [null, null],
      "allowedIntervalNs": [null, null],
      "verdict": "PASS|FAIL|INCONCLUSIVE|ERROR"
    }
  ],
  "verdict": "PASS|FAIL|INCONCLUSIVE|ERROR",
  "artifacts": [
    {
      "path": "",
      "sha256": "",
      "mediaType": "",
      "role": "raw|derived"
    }
  ],
  "deviations": [],
  "reviewRecord": ""
}
```

## Integrity rules

- manifests and raw artifacts are append-only after run closure;
- derived artifacts reference all raw inputs and the generating script version;
- clock, reset, configuration, and tool failures cannot be hidden as PASS;
- missing mandatory provenance makes the run ERROR or evidence INCOMPLETE;
- external/private artifacts retain checksums and controlled location IDs.
- every manifest has a stable `manifestId`; cross-domain consumers cite that ID
  and the applicable upstream artifact/gate references rather than “latest”;
- timing PASS/FAIL/INCONCLUSIVE is reproducible from raw timestamps, pairing
  rules, allowed bounds, and the recorded error budget;
- a missing/invalid clock or error budget invalidates timing evidence and cannot
  be hidden by a case-level PASS.

---

# 中文版

每个执行/分析包至少记录 manifest、基线、标准、适用性、CRS、模型、VCS、VC、IUT、工具、环境、实验、运行、种子、开始/结束、判定和带 hash 的产物。v1.2 在 v1.1 时序字段基础上增加稳定 `manifestId`、上游产物/版本/门禁引用和下游主张 ID，以支持跨领域追踪。时序结论必须能由原始时间戳、配对规则、界限和误差预算重算；无效时间链不能被总体 PASS 掩盖。

```json
{
  "manifestVersion": "1.2",
  "manifestId": "EVM-...",
  "baselineId": "RB-2026-001-v4.2",
  "standardEdition": "",
  "applicabilityId": "",
  "crsVersion": "",
  "modelVersion": "",
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
      "boundNs": null,
      "components": []
    }
  },
  "timingObservations": [
    {
      "obligationId": "",
      "triggerTimestampNs": null,
      "responseTimestampNs": null,
      "observedIntervalNs": [null, null],
      "allowedIntervalNs": [null, null],
      "verdict": "PASS|FAIL|INCONCLUSIVE|ERROR"
    }
  ],
  "verdict": "PASS|FAIL|INCONCLUSIVE|ERROR",
  "artifacts": [
    {
      "path": "",
      "sha256": "",
      "mediaType": "",
      "role": "raw|derived"
    }
  ],
  "deviations": [],
  "reviewRecord": ""
}
```

## 完整性规则

运行关闭后 manifest 和原始产物只可追加；派生产物必须引用全部原始输入和生成脚本版本；时钟、重置、配置或工具故障不得隐藏为 PASS；缺少强制来源信息时运行应为 ERROR 或证据应为 INCOMPLETE；私有产物也必须保存校验和和受控位置。每份清单具有稳定 `manifestId`，跨领域消费者必须引用该 ID 及适用上游产物/门禁记录，不得引用“最新”。时序判定必须可由原始时间戳、配对规则、允许界限和误差预算重算，无效时钟或误差预算使时序证据无效。
