# Evidence Manifest Contract

Every execution and derived analysis package records at least:

```json
{
  "manifestVersion": "1.1",
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
- timing PASS/FAIL/INCONCLUSIVE is reproducible from raw timestamps, pairing
  rules, allowed bounds, and the recorded error budget;
- a missing/invalid clock or error budget invalidates timing evidence and cannot
  be hidden by a case-level PASS.

---

## 中文版

每个执行/分析包至少记录 manifest、基线、标准、适用性、CRS、模型、VCS、VC、IUT、工具、环境、实验、运行、种子、开始/结束、判定和带 hash 的产物。v1.1 新增单调时钟类型/来源/分辨率、时间戳位置、同步假设、误差预算分量，以及逐时序义务的触发/响应时间戳、观测区间、允许区间和判定。时序结论必须能由原始时间戳、配对规则、界限和误差预算重算；无效时间链不能被总体 PASS 掩盖。
