# Evidence Manifest Contract

Every execution and derived analysis package records at least:

```json
{
  "manifestVersion": "1.0",
  "baselineId": "RB-2026-001-v4.1",
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
