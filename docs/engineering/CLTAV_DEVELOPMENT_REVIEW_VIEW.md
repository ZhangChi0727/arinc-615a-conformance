# CL-TAV Development Readiness Review View

> Generated from `configs/engineering/cltav_development_contracts.json`; do not edit.

- Control: `CR-2026-016`; decisions DD-038, DD-039, DD-040
- Bound M1 requirements: 863; disposition total: 863; readiness: `CANDIDATE`; claim: `SPECIFICATION-ONLY`

## Inputs

- `ARINC615A3-M1-CRS` — `configs/requirements/arinc_615a3_m1_crs.json` — SHA-256 `56e214f089e6563e53e3991e7a8e7892f163840bb2c1d7d39f4a9ce92fc16758` — Bound protocol requirement universe
- `CLTAV-INTERFACE-REGISTRY` — `configs/research/cltav_interface_registry.json` — SHA-256 `a65679b902cf51d31aa613c133919c3cd2c66dbc6c65eb3cc58d9bf3530d329d` — Accepted interface vocabulary
- `CLTAV-INTEGRITY-OBLIGATION-BASELINE` — `configs/engineering/cltav_integrity_obligation_baseline.json` — SHA-256 `85ec28689371bf557dfad5b9fc5ff80421198a896173ced603dc992e62a2dc57` — Independent required integrity-obligation set and contract identity
- `CLTAV-HISTORICAL-CAPTURE-MANIFEST` — `configs/research/cltav_historical_capture_manifest.json` — SHA-256 `80cc6076e65d2639bd332406412e8895ca7c43722005f70f73426ef15eb8f747` — Pins exploratory capture identities for matrix identity witnesses; not independent truth.

## Record contracts

| ID | Owner | Fields | Uncertainty |
|---|---|---|---|
| `CAPTURE-IDENTITY` | `MOD-CAPTURE` | `captureId`, `relativePath`, `sha256`, `byteSize`, `manifestVersion` | Exploratory use only; unknown metadata remains UNKNOWN. |
| `PACKET-REF` | `MOD-CAPTURE` | `captureId`, `sectionId`, `interfaceId`, `packetNumber`, `rawTicks`, `resolution`, `caplen`, `origlen`, `decodeStatus` | Clock accuracy is distinct from resolution. |
| `DATAGRAM-RECORD` | `MOD-REASSEMBLY` | `fragmentRefs`, `coverage`, `overlapStatus`, `reassemblyStatus` | Missing or conflicting fragments remain explicit. |
| `TRANSFER-RECORD` | `MOD-TRANSFER` | `direction`, `endpoints`, `tid`, `request`, `optionState`, `blockMap`, `completionEvidence` | Ambiguous TID or option state remains UNKNOWN. UNKNOWN carries no effective option values. DEFAULTED blksize, when present, is exactly 512; omission means blksize was not established, not an implicit value. ACCEPTED carries the confirmed negotiated value. |
| `PROTOCOL-EVENT` | `MOD-TRANSFER` | `eventLayer`, `role`, `payload`, `correlationKey`, `rawRefs`, `parseBoundary` | Application facts are not inferred from wire evidence. |
| `OWNERSHIP-RESULT` | `MOD-OWNERSHIP` | `requestInstance`, `policy`, `status`, `evidenceRefs` | Multiple possible owners remain AMBIGUOUS. |
| `OBSERVATION-ASSESSMENT` | `MOD-OBSERVATION` | `measurementInterval`, `domain`, `errorBasis`, `verdict`, `reason` | Invalid time chain is ERROR; boundary overlap is INCONCLUSIVE. |
| `INTAKE-METADATA` | `MOD-CAPTURE` | `operatorNote`, `topology`, `clockAccuracy`, `configuration`, `rootCause` | Unknown values are not algorithm priors. |
| `FINDING-RECORD` | `MOD-OBSERVATION` | `facts`, `judgmentBasis`, `scope`, `assumptions`, `evidenceRefs` | Finding is not a root-cause label. |
| `HISTORY-HANDLE` | `MOD-OBSERVATION` | `H`, `compatibleStateByHypothesis`, `statusByHypothesis`, `version` | UNKNOWN-EFFECT and unconfirmed Recover retain H and mark affected status CONSERVATIVE-UNKNOWN; CONFIRMED-NOT-SENT preserves history; equal H sets may retain different compatible histories. |

### `CAPTURE-IDENTITY` — Capture identity
- Ownership: The intake boundary owns immutable file identity.
- Uncertainty: Exploratory use only; unknown metadata remains UNKNOWN.
- Source requirements: None
- Error behavior: Return a named error or conservative unknown; do not emit IUT FAIL.
- Field definitions: `{"byteSize": {"constraintId": "RC-CAPTURE-BYTE-SIZE", "minimum": 0, "required": true, "type": "integer"}, "captureId": {"constraintId": "RC-CAPTURE-ID", "pattern": "^(?:cap-[a-z0-9][a-z0-9-]*|HC-[0-9]{2})$", "required": true, "type": "string"}, "manifestVersion": {"constraintId": "RC-CAPTURE-MANIFEST-VERSION", "pattern": "^[1-9][0-9]*\\.[0-9]+$", "required": true, "type": "string"}, "relativePath": {"constraintId": "RC-CAPTURE-PATH", "pattern": "^(?!/)(?![A-Za-z]:)(?!.*(?:^|/)\\.\\.(?:/|$))[^\\x00-\\x1f\\\\]+$", "required": true, "type": "string"}, "sha256": {"constraintId": "RC-CAPTURE-SHA256", "pattern": "^[0-9a-f]{64}$", "required": true, "type": "string"}}`
- Valid example: `{"byteSize": 128, "captureId": "cap-syn-001", "manifestVersion": "1.0", "relativePath": "synthetic/cap-syn-001.pcapng", "sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"}`
- Invalid example: `{"byteSize": 128, "captureId": "cap-syn-001", "manifestVersion": "1.0", "relativePath": "synthetic/cap-syn-001.pcapng", "sha256": "not-a-hash"}`
- Expected rejection: `{"constraintId": "RC-CAPTURE-SHA256", "path": ["sha256"]}`
- Rejection reason: sha256 must contain exactly 64 lowercase hexadecimal characters

### `PACKET-REF` — Packet reference
- Ownership: Capture module owns raw packet provenance.
- Uncertainty: Clock accuracy is distinct from resolution.
- Source requirements: None
- Error behavior: Return a named error or conservative unknown; do not emit IUT FAIL.
- Field definitions: `{"caplen": {"constraintId": "RC-PACKET-CAPLEN", "minimum": 0, "required": true, "type": "integer"}, "captureId": {"constraintId": "RC-PACKET-CAPTURE-ID", "pattern": "^(?:cap-[a-z0-9][a-z0-9-]*|HC-[0-9]{2})$", "required": true, "type": "string"}, "decodeStatus": {"constraintId": "RC-PACKET-DECODE-STATUS", "enum": ["FULL", "TRUNCATED", "UNDECODED"], "required": true, "type": "string"}, "interfaceId": {"constraintId": "RC-PACKET-INTERFACE", "minimum": 0, "required": true, "type": "integer"}, "origlen": {"constraintId": "RC-PACKET-ORIGLEN", "minimum": 0, "required": true, "type": "integer"}, "packetNumber": {"constraintId": "RC-PACKET-NUMBER", "minimum": 1, "required": true, "type": "integer"}, "rawTicks": {"constraintId": "RC-PACKET-TICKS", "minimum": 0, "required": true, "type": "integer"}, "resolution": {"additionalProperties": false, "constraintId": "RC-PACKET-RESOLUTION", "properties": {"ticksPerSecond": {"constraintId": "RC-PACKET-TICKS-PER-SECOND", "minimum": 1, "type": "integer"}}, "required": true, "requiredProperties": ["ticksPerSecond"], "type": "object"}, "sectionId": {"constraintId": "RC-PACKET-SECTION", "minimum": 0, "required": true, "type": "integer"}}`
- Valid example: `{"caplen": 96, "captureId": "cap-syn-001", "decodeStatus": "FULL", "interfaceId": 0, "origlen": 96, "packetNumber": 1, "rawTicks": 125000, "resolution": {"ticksPerSecond": 1000000}, "sectionId": 0}`
- Invalid example: `{"caplen": 96, "captureId": "cap-syn-001", "decodeStatus": "FULL", "interfaceId": 0, "origlen": 96, "packetNumber": 1, "rawTicks": 125000, "resolution": {"ticksPerSecond": 0}, "sectionId": 0}`
- Expected rejection: `{"constraintId": "RC-PACKET-TICKS-PER-SECOND", "path": ["resolution", "ticksPerSecond"]}`
- Rejection reason: resolution must contain a positive ticksPerSecond value

### `DATAGRAM-RECORD` — Datagram reconstruction
- Ownership: Reassembly owns derived coverage, never source packets.
- Uncertainty: Missing or conflicting fragments remain explicit.
- Source requirements: None
- Error behavior: Return a named error or conservative unknown; do not emit IUT FAIL.
- Field definitions: `{"coverage": {"constraintId": "RC-DATAGRAM-COVERAGE", "items": {"additionalProperties": false, "constraintId": "RC-DATAGRAM-RANGE", "properties": {"endExclusive": {"constraintId": "RC-DATAGRAM-RANGE-END", "minimum": 1, "type": "integer"}, "start": {"constraintId": "RC-DATAGRAM-RANGE-START", "minimum": 0, "type": "integer"}}, "requiredProperties": ["start", "endExclusive"], "type": "object"}, "minItems": 1, "required": true, "type": "array"}, "fragmentRefs": {"constraintId": "RC-DATAGRAM-FRAGMENTS", "items": {"constraintId": "RC-PACKET-REF-ID", "pattern": "^(?:cap-[a-z0-9][a-z0-9-]*|HC-[0-9]{2}):[0-9]+:[0-9]+:[1-9][0-9]*$", "type": "string"}, "minItems": 1, "required": true, "type": "array", "uniqueItems": true}, "overlapStatus": {"constraintId": "RC-DATAGRAM-OVERLAP", "enum": ["NONE", "DUPLICATE", "CONFLICT", "UNKNOWN"], "required": true, "type": "string"}, "reassemblyStatus": {"constraintId": "RC-DATAGRAM-STATUS", "enum": ["COMPLETE", "GAPPED", "CONFLICT", "UNKNOWN"], "required": true, "type": "string"}}`
- Valid example: `{"coverage": [{"endExclusive": 512, "start": 0}], "fragmentRefs": ["cap-syn-001:0:0:1", "cap-syn-001:0:0:2"], "overlapStatus": "NONE", "reassemblyStatus": "COMPLETE"}`
- Invalid example: `{"coverage": [{"endExclusive": 512, "start": 0}], "fragmentRefs": [], "overlapStatus": "NONE", "reassemblyStatus": "COMPLETE"}`
- Expected rejection: `{"constraintId": "RC-DATAGRAM-FRAGMENTS", "path": ["fragmentRefs"]}`
- Rejection reason: fragmentRefs must contain at least one scoped packet reference

### `TRANSFER-RECORD` — Transfer candidate
- Ownership: Transfer module owns candidate association.
- Uncertainty: Ambiguous TID or option state remains UNKNOWN. UNKNOWN carries no effective option values. DEFAULTED blksize, when present, is exactly 512; omission means blksize was not established, not an implicit value. ACCEPTED carries the confirmed negotiated value.
- Source requirements: `CRS-M1-00646`, `CRS-M1-00647`
- Error behavior: Reject a DEFAULTED blksize other than 512 and any UNKNOWN effective value; return a named error or conservative unknown without emitting IUT FAIL.
- Field definitions: `{"blockMap": {"additionalProperties": {"constraintId": "RC-PACKET-REF-ID", "pattern": "^(?:cap-[a-z0-9][a-z0-9-]*|HC-[0-9]{2}):[0-9]+:[0-9]+:[1-9][0-9]*$", "type": "string"}, "constraintId": "RC-TRANSFER-BLOCK-MAP", "required": true, "type": "object"}, "completionEvidence": {"constraintId": "RC-TRANSFER-COMPLETION", "items": {"constraintId": "RC-EVIDENCE-REF", "pattern": "^(cap|pkt|dgram|transfer|event)-[A-Za-z0-9._:-]+$", "type": "string"}, "required": true, "type": "array", "uniqueItems": true}, "direction": {"constraintId": "RC-TRANSFER-DIRECTION", "enum": ["CLIENT-TO-SERVER", "SERVER-TO-CLIENT"], "required": true, "type": "string"}, "endpoints": {"additionalProperties": false, "constraintId": "RC-TRANSFER-ENDPOINTS", "properties": {"client": {"constraintId": "RC-TRANSFER-CLIENT", "minLength": 1, "type": "string"}, "server": {"constraintId": "RC-TRANSFER-SERVER", "minLength": 1, "type": "string"}}, "required": true, "requiredProperties": ["client", "server"], "type": "object"}, "optionState": {"additionalProperties": false, "constraintId": "RC-TRANSFER-OPTION-STATE", "properties": {"mode": {"constraintId": "RC-OPTION-MODE", "enum": ["ACCEPTED", "DEFAULTED", "UNKNOWN"], "type": "string"}, "values": {"additionalProperties": false, "constraintId": "RC-OPTION-VALUES", "properties": {"blksize": {"constraintId": "RC-OPTION-BLKSIZE", "maximum": 65464, "minimum": 8, "type": "integer"}, "timeout": {"constraintId": "RC-OPTION-TIMEOUT", "maximum": 255, "minimum": 1, "type": "integer"}, "tsize": {"constraintId": "RC-OPTION-TSIZE", "minimum": 0, "type": "integer"}}, "type": "object"}}, "required": true, "requiredProperties": ["mode", "values"], "type": "object"}, "request": {"constraintId": "RC-TRANSFER-REQUEST", "pattern": "^event-[A-Za-z0-9._:-]+$", "required": true, "type": "string"}, "tid": {"additionalProperties": false, "constraintId": "RC-TRANSFER-TID", "properties": {"clientPort": {"constraintId": "RC-TID-CLIENT", "maximum": 65535, "minimum": 1, "type": "integer"}, "serverPort": {"constraintId": "RC-TID-SERVER", "maximum": 65535, "minimum": 1, "type": "integer"}}, "required": true, "requiredProperties": ["clientPort", "serverPort"], "type": "object"}}`
- Valid example: `{"blockMap": {"1": "cap-syn-001:0:0:2"}, "completionEvidence": ["pkt-cap-syn-001:2"], "direction": "SERVER-TO-CLIENT", "endpoints": {"client": "192.0.2.10", "server": "192.0.2.20"}, "optionState": {"mode": "DEFAULTED", "values": {"blksize": 512}}, "request": "event-rrq-001", "tid": {"clientPort": 40000, "serverPort": 69}}`
- Invalid example: `{"blockMap": {}, "completionEvidence": [], "direction": "SIDEWAYS", "endpoints": {"client": "192.0.2.10", "server": "192.0.2.20"}, "optionState": {"mode": "DEFAULTED", "values": {}}, "request": "event-rrq-001", "tid": {"clientPort": 40000, "serverPort": 69}}`
- Expected rejection: `{"constraintId": "RC-TRANSFER-DIRECTION", "path": ["direction"]}`
- Rejection reason: direction must use the controlled client/server vocabulary

### `PROTOCOL-EVENT` — Protocol event
- Ownership: Transfer module owns derived event identity.
- Uncertainty: Application facts are not inferred from wire evidence.
- Source requirements: None
- Error behavior: Return a named error or conservative unknown; do not emit IUT FAIL.
- Field definitions: `{"correlationKey": {"constraintId": "RC-EVENT-CORRELATION", "pattern": "^corr-[A-Za-z0-9._:-]+$", "required": true, "type": "string"}, "eventLayer": {"constraintId": "RC-EVENT-LAYER", "enum": ["WIRE", "PARSE-RESULT", "APPLICATION", "ENVIRONMENT"], "required": true, "type": "string"}, "parseBoundary": {"constraintId": "RC-EVENT-PARSE-BOUNDARY", "enum": ["COMPLETE", "PARTIAL", "OPAQUE", "ERROR"], "required": true, "type": "string"}, "payload": {"additionalProperties": false, "constraintId": "RC-EVENT-PAYLOAD", "properties": {"ref": {"constraintId": "RC-PAYLOAD-REF", "pattern": "^payload-[A-Za-z0-9._:-]+$", "type": "string"}, "type": {"constraintId": "RC-PAYLOAD-TYPE", "pattern": "^[A-Z][A-Z0-9-]*$", "type": "string"}}, "required": true, "requiredProperties": ["type", "ref"], "type": "object"}, "rawRefs": {"constraintId": "RC-EVENT-RAW-REFS", "items": {"constraintId": "RC-PACKET-REF-ID", "pattern": "^(?:cap-[a-z0-9][a-z0-9-]*|HC-[0-9]{2}):[0-9]+:[0-9]+:[1-9][0-9]*$", "type": "string"}, "minItems": 1, "required": true, "type": "array", "uniqueItems": true}, "role": {"constraintId": "RC-EVENT-ROLE", "enum": ["CLIENT", "SERVER", "UNKNOWN"], "required": true, "type": "string"}}`
- Valid example: `{"correlationKey": "corr-transfer-001", "eventLayer": "WIRE", "parseBoundary": "COMPLETE", "payload": {"ref": "payload-rrq-001", "type": "RRQ"}, "rawRefs": ["cap-syn-001:0:0:1"], "role": "CLIENT"}`
- Invalid example: `{"correlationKey": "corr-transfer-001", "eventLayer": "WIRE", "parseBoundary": "COMPLETE", "payload": {"ref": "payload-rrq-001", "type": "RRQ"}, "rawRefs": [], "role": "CLIENT"}`
- Expected rejection: `{"constraintId": "RC-EVENT-RAW-REFS", "path": ["rawRefs"]}`
- Rejection reason: rawRefs must retain at least one source packet

### `OWNERSHIP-RESULT` — Ownership result
- Ownership: Ownership module owns matching result.
- Uncertainty: Multiple possible owners remain AMBIGUOUS.
- Source requirements: None
- Error behavior: Return a named error or conservative unknown; do not emit IUT FAIL.
- Field definitions: `{"evidenceRefs": {"constraintId": "RC-OWNERSHIP-EVIDENCE", "items": {"constraintId": "RC-EVIDENCE-REF", "pattern": "^(cap|pkt|dgram|transfer|event)-[A-Za-z0-9._:-]+$", "type": "string"}, "required": true, "type": "array", "uniqueItems": true}, "policy": {"constraintId": "RC-OWNERSHIP-POLICY", "enum": ["UNIQUE-KEY", "FIFO", "MOST-RECENT"], "required": true, "type": "string"}, "requestInstance": {"constraintId": "RC-OWNERSHIP-REQUEST", "pattern": "^event-[A-Za-z0-9._:-]+$", "required": true, "type": "string"}, "status": {"constraintId": "RC-OWNERSHIP-STATUS", "enum": ["UNIQUE", "AMBIGUOUS", "UNMATCHED", "UNKNOWN"], "required": true, "type": "string"}}`
- Valid example: `{"evidenceRefs": ["pkt-cap-syn-001:1"], "policy": "UNIQUE-KEY", "requestInstance": "event-rrq-001", "status": "UNIQUE"}`
- Invalid example: `{"evidenceRefs": [], "policy": "UNIQUE-KEY", "requestInstance": "event-rrq-001", "status": "CERTAIN"}`
- Expected rejection: `{"constraintId": "RC-OWNERSHIP-STATUS", "path": ["status"]}`
- Rejection reason: status must use the controlled ownership vocabulary

### `OBSERVATION-ASSESSMENT` — Observation assessment
- Ownership: Observation module owns verdict interpretation.
- Uncertainty: Invalid time chain is ERROR; boundary overlap is INCONCLUSIVE.
- Source requirements: None
- Error behavior: Return a named error or conservative unknown; do not emit IUT FAIL.
- Field definitions: `{"domain": {"constraintId": "RC-OBS-DOMAIN", "enum": ["MONOTONIC-CAPTURE", "SYNCHRONIZED-UTC", "UNKNOWN"], "required": true, "type": "string"}, "errorBasis": {"constraintId": "RC-OBS-ERROR-BASIS", "pattern": "^EB-[A-Za-z0-9._-]+$", "required": true, "type": "string"}, "measurementInterval": {"constraintId": "RC-OBS-INTERVAL", "oneOf": [{"additionalProperties": false, "constraintId": "RC-OBS-INTERVAL-VALUE", "properties": {"lower": {"constraintId": "RC-OBS-LOWER", "type": "integer"}, "lowerClosed": {"constraintId": "RC-OBS-LOWER-CLOSED", "type": "boolean"}, "unit": {"constraintId": "RC-OBS-UNIT", "enum": ["tick", "ns", "us"], "type": "string"}, "upper": {"constraintId": "RC-OBS-UPPER", "type": "integer"}, "upperClosed": {"constraintId": "RC-OBS-UPPER-CLOSED", "type": "boolean"}}, "requiredProperties": ["lower", "upper", "lowerClosed", "upperClosed", "unit"], "type": "object"}, {"constraintId": "RC-OBS-INTERVAL-ABSENT", "type": "null"}], "required": true}, "reason": {"constraintId": "RC-OBS-REASON", "minLength": 1, "required": true, "type": "string"}, "verdict": {"constraintId": "RC-OBS-VERDICT", "enum": ["PASS", "FAIL", "INCONCLUSIVE", "ERROR"], "required": true, "type": "string"}}`
- Valid example: `{"domain": "MONOTONIC-CAPTURE", "errorBasis": "EB-SYN-001", "measurementInterval": {"lower": 100, "lowerClosed": true, "unit": "us", "upper": 104, "upperClosed": true}, "reason": "entire interval lies within the closed requirement interval", "verdict": "PASS"}`
- Invalid example: `{"domain": "MONOTONIC-CAPTURE", "errorBasis": "EB-SYN-001", "measurementInterval": {"lower": 100, "lowerClosed": true, "unit": "seconds", "upper": 104, "upperClosed": true}, "reason": "bad unit", "verdict": "PASS"}`
- Expected rejection: `{"constraintId": "RC-OBS-INTERVAL", "path": ["measurementInterval"]}`
- Rejection reason: measurement interval unit must use the controlled exact-time vocabulary

### `INTAKE-METADATA` — Intake metadata
- Ownership: Intake boundary owns declared context only.
- Uncertainty: Unknown values are not algorithm priors.
- Source requirements: None
- Error behavior: Return a named error or conservative unknown; do not emit IUT FAIL.
- Field definitions: `{"clockAccuracy": {"additionalProperties": false, "constraintId": "RC-INTAKE-CLOCK", "properties": {"boundNs": {"constraintId": "RC-INTAKE-CLOCK-BOUND", "minimum": 1, "type": "integer"}, "source": {"constraintId": "RC-INTAKE-CLOCK-SOURCE", "minLength": 1, "type": "string"}, "state": {"constraintId": "RC-INTAKE-CLOCK-STATE", "enum": ["DECLARED", "UNKNOWN"], "type": "string"}}, "required": true, "requiredProperties": ["state", "source"], "type": "object"}, "configuration": {"additionalProperties": false, "constraintId": "RC-INTAKE-CONFIG", "properties": {"source": {"constraintId": "RC-INTAKE-CONFIG-SOURCE", "minLength": 1, "type": "string"}, "state": {"constraintId": "RC-INTAKE-CONFIG-STATE", "enum": ["DECLARED", "UNKNOWN"], "type": "string"}}, "required": true, "requiredProperties": ["state", "source"], "type": "object"}, "operatorNote": {"constraintId": "RC-INTAKE-NOTE", "minLength": 1, "required": true, "type": "string"}, "rootCause": {"additionalProperties": false, "constraintId": "RC-INTAKE-ROOT-CAUSE", "properties": {"source": {"constraintId": "RC-INTAKE-ROOT-SOURCE", "minLength": 1, "type": "string"}, "state": {"constraintId": "RC-INTAKE-ROOT-STATE", "enum": ["DECLARED", "UNKNOWN"], "type": "string"}}, "required": true, "requiredProperties": ["state", "source"], "type": "object"}, "topology": {"additionalProperties": false, "constraintId": "RC-INTAKE-TOPOLOGY", "properties": {"source": {"constraintId": "RC-INTAKE-TOPOLOGY-SOURCE", "minLength": 1, "type": "string"}, "state": {"constraintId": "RC-INTAKE-TOPOLOGY-STATE", "enum": ["DECLARED", "UNKNOWN"], "type": "string"}}, "required": true, "requiredProperties": ["state", "source"], "type": "object"}}`
- Valid example: `{"clockAccuracy": {"source": "not supplied", "state": "UNKNOWN"}, "configuration": {"source": "synthetic fixture cfg-1", "state": "DECLARED"}, "operatorNote": "synthetic intake only", "rootCause": {"source": "not claimed", "state": "UNKNOWN"}, "topology": {"source": "not supplied", "state": "UNKNOWN"}}`
- Invalid example: `{"clockAccuracy": {"boundNs": 0, "source": "bad bound", "state": "DECLARED"}, "configuration": {"source": "synthetic fixture cfg-1", "state": "DECLARED"}, "operatorNote": "synthetic intake only", "rootCause": {"source": "not claimed", "state": "UNKNOWN"}, "topology": {"source": "not supplied", "state": "UNKNOWN"}}`
- Expected rejection: `{"constraintId": "RC-INTAKE-CLOCK-BOUND", "path": ["clockAccuracy", "boundNs"]}`
- Rejection reason: a declared clock bound must be positive; UNKNOWN does not use a zero bound

### `FINDING-RECORD` — Finding record
- Ownership: Reporting owns the bounded finding.
- Uncertainty: Finding is not a root-cause label.
- Source requirements: None
- Error behavior: Return a named error or conservative unknown; do not emit IUT FAIL.
- Field definitions: `{"assumptions": {"constraintId": "RC-FINDING-ASSUMPTIONS", "items": {"constraintId": "RC-FINDING-ASSUMPTION", "minLength": 1, "type": "string"}, "required": true, "type": "array"}, "evidenceRefs": {"constraintId": "RC-FINDING-EVIDENCE", "items": {"constraintId": "RC-EVIDENCE-REF", "pattern": "^(cap|pkt|dgram|transfer|event)-[A-Za-z0-9._:-]+$", "type": "string"}, "minItems": 1, "required": true, "type": "array", "uniqueItems": true}, "facts": {"constraintId": "RC-FINDING-FACTS", "items": {"constraintId": "RC-FINDING-FACT", "minLength": 1, "type": "string"}, "minItems": 1, "required": true, "type": "array"}, "judgmentBasis": {"constraintId": "RC-FINDING-BASIS", "items": {"constraintId": "RC-EVIDENCE-REF", "pattern": "^(cap|pkt|dgram|transfer|event)-[A-Za-z0-9._:-]+$", "type": "string"}, "minItems": 1, "required": true, "type": "array"}, "scope": {"additionalProperties": false, "constraintId": "RC-FINDING-SCOPE", "properties": {"captureIds": {"constraintId": "RC-FINDING-CAPTURES", "items": {"constraintId": "RC-FINDING-CAPTURE", "pattern": "^(?:cap-[a-z0-9][a-z0-9-]*|HC-[0-9]{2})$", "type": "string"}, "minItems": 1, "type": "array"}, "requirementIds": {"constraintId": "RC-FINDING-REQUIREMENTS", "items": {"constraintId": "RC-FINDING-REQUIREMENT", "pattern": "^CRS-M1-[0-9]{5}$", "type": "string"}, "type": "array"}}, "required": true, "requiredProperties": ["captureIds", "requirementIds"], "type": "object"}}`
- Valid example: `{"assumptions": ["capture ordering preserved"], "evidenceRefs": ["pkt-cap-syn-001:2"], "facts": ["synthetic DATA block observed"], "judgmentBasis": ["pkt-cap-syn-001:2"], "scope": {"captureIds": ["cap-syn-001"], "requirementIds": ["CRS-M1-00021"]}}`
- Invalid example: `{"assumptions": [], "evidenceRefs": ["pkt-cap-syn-001:2"], "facts": [], "judgmentBasis": ["pkt-cap-syn-001:2"], "scope": {"captureIds": ["cap-syn-001"], "requirementIds": []}}`
- Expected rejection: `{"constraintId": "RC-FINDING-FACTS", "path": ["facts"]}`
- Rejection reason: a finding must contain at least one bounded fact and is not a root-cause assertion

### `HISTORY-HANDLE` — History handle
- Ownership: The session holds HistoryHandle; the observation/history-update module alone advances its versioned compatible histories.
- Uncertainty: UNKNOWN-EFFECT and unconfirmed Recover retain H and mark affected status CONSERVATIVE-UNKNOWN; CONFIRMED-NOT-SENT preserves history; equal H sets may retain different compatible histories.
- Source requirements: None
- Error behavior: Reject out-of-scope hypotheses and unknown status values; return a named error without converting it to IUT FAIL.
- Field definitions: `{"H": {"constraintId": "RC-HISTORY-H", "items": {"constraintId": "RC-HYPOTHESIS-ID", "pattern": "^h[A-Za-z0-9._-]+$", "type": "string"}, "minItems": 0, "required": true, "type": "array", "uniqueItems": true}, "compatibleStateByHypothesis": {"additionalProperties": {"constraintId": "RC-HISTORY-FRONTIER", "pattern": "^frontier-[A-Za-z0-9._:-]+$", "type": "string"}, "constraintId": "RC-HISTORY-COMPATIBLE", "required": true, "type": "object"}, "statusByHypothesis": {"additionalProperties": {"constraintId": "RC-HISTORY-STATUS-VALUE", "enum": ["KNOWN", "CONSERVATIVE-UNKNOWN"], "type": "string"}, "constraintId": "RC-HISTORY-STATUS", "required": false, "type": "object"}, "version": {"constraintId": "RC-HISTORY-VERSION", "minimum": 0, "required": true, "type": "integer"}}`
- Valid example: `{"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-syn-0"}, "statusByHypothesis": {"h0": "CONSERVATIVE-UNKNOWN"}, "version": 0}`
- Invalid example: `{"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-syn-0"}, "statusByHypothesis": {"h0": "BANANA"}, "version": 0}`
- Expected rejection: `{"constraintId": "RC-HISTORY-STATUS-VALUE", "path": ["statusByHypothesis", "h0"]}`
- Rejection reason: status must reuse KNOWN or CONSERVATIVE-UNKNOWN from the bound HistoryHandle

## Tool requirements

| ID | Owner | Source relation | Acceptance | Requirement |
|---|---|---|---|---|
| `TR-CAPTURE-INTAKE` | `MOD-CAPTURE` | `ENGINEERING-DECISION` | `AC-SYN-TRANSFER` | Preserve capture identity and clock scope |
| `TR-DATAGRAM-REASSEMBLY` | `MOD-REASSEMBLY` | `ENGINEERING-DECISION` | `AC-SYN-TRANSFER` | Reconstruct only provenance-consistent IPv4 datagrams |
| `TR-TRANSFER-RECONSTRUCTION` | `MOD-TRANSFER` | `PROTOCOL-DERIVED` | `AC-SYN-TRANSFER` | Reconstruct bounded TFTP transfer candidates |
| `TR-PROTOCOL-EVENT` | `MOD-TRANSFER` | `METHOD-DERIVED` | `AC-SYN-TRANSFER` | Derive typed protocol events without inventing application facts |
| `TR-OWNERSHIP` | `MOD-OWNERSHIP` | `METHOD-DERIVED` | `AC-SYN-TRANSFER` | Resolve response ownership conservatively |
| `TR-OBSERVATION-ASSESSMENT` | `MOD-OBSERVATION` | `METHOD-DERIVED` | `AC-SYN-TRANSFER` | Assess observations with explicit timing uncertainty |
| `TR-HISTORY-COMPATIBILITY` | `MOD-OBSERVATION` | `METHOD-DERIVED` | `AC-SYN-TRANSFER` | Update finite compatibility history conservatively |
| `TR-TRACEABLE-FINDING` | `MOD-OBSERVATION` | `ENGINEERING-DECISION` | `AC-SYN-TRANSFER` | Report bounded findings without fault-truth claims |

### `TR-CAPTURE-INTAKE` — Preserve capture identity and clock scope
- Trigger: A caller supplies one manifest-bound capture reference.
- Preconditions: The manifest audit has established a matching relative path, byte size and SHA-256.
- Inputs: `CAPTURE-IDENTITY`; outputs: `PACKET-REF`
- Action: Create a capture-scoped identity; retain section, interface and raw-tick provenance without inferring clock accuracy.
- Error/unknown: Unreadable blocks, unsupported link types and unknown clock accuracy are explicit decode or UNKNOWN metadata outcomes, never IUT FAIL.
- Evidence: CaptureIdentity and PacketRef raw provenance fields.
- Interfaces: `IF-EXECUTE-RECORD`; CRS: —; control/method: `DD-040`, `CR-2026-016 AC-03`

### `TR-DATAGRAM-REASSEMBLY` — Reconstruct only provenance-consistent IPv4 datagrams
- Trigger: PacketRef records contain IPv4 fragmentation metadata.
- Preconditions: All fragments retain capture, section and interface scope.
- Inputs: `PACKET-REF`; outputs: `DATAGRAM-RECORD`
- Action: Group fragments by scoped identity, retain every source reference, and classify missing or conflicting coverage without last-fragment overwrite.
- Error/unknown: Missing, truncated or overlapping fragments yield an incomplete or conflict record; they do not yield a complete UDP payload.
- Evidence: DatagramRecord fragment references and coverage classification.
- Interfaces: `IF-EXECUTE-RECORD`; CRS: —; control/method: `CR-2026-016 AC-03`

### `TR-TRANSFER-RECONSTRUCTION` — Reconstruct bounded TFTP transfer candidates
- Trigger: A complete or classified-incomplete UDP datagram is available.
- Preconditions: Initial request and dynamic TID evidence are distinguishable from ordinary UDP traffic.
- Inputs: `DATAGRAM-RECORD`; outputs: `TRANSFER-RECORD`
- Action: Associate request, option negotiation, DATA/ACK, WAIT, ERROR and ABORT evidence while preserving ambiguity and block-size confirmation state.
- Error/unknown: A confirmed accepted option uses its confirmed value. Sufficient, consistent evidence that an option was not accepted, including a complete basic transfer without option confirmation, uses the protocol default; missing, conflicting or uncorrelated evidence remains UNKNOWN; block-wrap beyond the declared bound is UNSUPPORTED.
- Evidence: TransferRecord endpoint, TID, option and completion evidence.
- Interfaces: `IF-EXECUTE-RECORD`; CRS: `CRS-M1-00021`, `CRS-M1-00025`, `CRS-M1-00032`, `CRS-M1-00620`, `CRS-M1-00635`, `CRS-M1-00646`, `CRS-M1-00647`; control/method: `CRS-M1-00021`, `CRS-M1-00025`, `CRS-M1-00032`

### `TR-PROTOCOL-EVENT` — Derive typed protocol events without inventing application facts
- Trigger: A TransferRecord has usable wire evidence.
- Preconditions: The event layer is explicitly WIRE, PARSE-RESULT, APPLICATION or ENVIRONMENT.
- Inputs: `TRANSFER-RECORD`; outputs: `PROTOCOL-EVENT`
- Action: Emit typed events with correlation keys, full raw references and a parse-confidence boundary.
- Error/unknown: Unobservable application decisions remain absent or UNKNOWN; they are not inferred from model state.
- Evidence: ProtocolEvent correlation key and raw PacketRef chain.
- Interfaces: `IF-OBS-INTERPRET`; CRS: —; control/method: `DD-039`, `CR-2026-016 AC-03`

### `TR-OWNERSHIP` — Resolve response ownership conservatively
- Trigger: A ProtocolEvent may answer a declared request instance.
- Preconditions: Matching policy and event order are available for the candidate instance set.
- Inputs: `PROTOCOL-EVENT`; outputs: `OWNERSHIP-RESULT`
- Action: Apply the declared UNIQUE-KEY, FIFO or MOST-RECENT policy and preserve cancellation, supersession and ambiguity evidence.
- Error/unknown: A response with incompatible possible owners is ambiguous and cannot be consumed as a unique response.
- Evidence: OwnershipResult policy, request instance and supporting event references.
- Interfaces: `IF-OBS-INTERPRET`; CRS: —; control/method: `IF-OBS-INTERPRET`, `CR-2026-016 AC-03`

### `TR-OBSERVATION-ASSESSMENT` — Assess observations with explicit timing uncertainty
- Trigger: A uniquely owned or explicitly incomplete observation is available.
- Preconditions: Measurement interval, declared domain and error basis are available or explicitly invalid.
- Inputs: `OWNERSHIP-RESULT`, `PROTOCOL-EVENT`; outputs: `OBSERVATION-ASSESSMENT`
- Action: Apply interval topology and the declared conformance domain to produce a four-valued assessment.
- Error/unknown: Empty measurement-domain intersection or invalid time chain is ERROR; boundary overlap is INCONCLUSIVE.
- Evidence: ObservationAssessment interval, domain and uncertainty references.
- Interfaces: `IF-OBS-INTERPRET`; CRS: —; control/method: `IF-OBS-INTERPRET`, `T5`

### `TR-HISTORY-COMPATIBILITY` — Update finite compatibility history conservatively
- Trigger: ObservationAssessment returns a normalized admissible outcome.
- Preconditions: The HistoryHandle belongs to the SessionContext and retains its versioned frontiers.
- Inputs: `OBSERVATION-ASSESSMENT`, `HISTORY-HANDLE`; outputs: `HISTORY-HANDLE`
- Action: Intersect only an accepted compatible set with the current hypothesis set and preserve per-hypothesis history.
- Error/unknown: ERROR, UNKNOWN-EFFECT and resource exhaustion do not exclude hypotheses or revive excluded hypotheses.
- Evidence: HistoryHandle version and compatible-state frontier references.
- Interfaces: `IF-HIST-UPDATE`; CRS: —; control/method: `DD-039`, `IF-OBS-INTERPRET`

### `TR-TRACEABLE-FINDING` — Report bounded findings without fault-truth claims
- Trigger: A completed assessment or a named blocked/unknown condition is available.
- Preconditions: All supporting records retain their capture and interpretation provenance.
- Inputs: `OBSERVATION-ASSESSMENT`, `INTAKE-METADATA`; outputs: `FINDING-RECORD`
- Action: Emit observation facts, judgment basis, scope and unresolved assumptions separately from root-cause labels.
- Error/unknown: Unknown topology, clock, configuration or root cause remains explicit and cannot become a fault label.
- Evidence: FindingRecord evidence links and applicability scope.
- Interfaces: `IF-OBS-INTERPRET`; CRS: —; control/method: `DD-040`, `CR-2026-016 AC-03`

## Module contracts

Upstream policy: every cross-module input producer must be directly or transitively reachable through `upstreamModuleIds`; external inputs and records produced by the consuming module itself require no upstream edge.

### `MOD-CAPTURE` — Capture intake and packet provenance
- Responsibility: Verify a manifest-bound capture identity and emit immutable packet references without inferring clock accuracy or field truth.
- Preconditions: CaptureIdentity matches the audited manifest bytes.; Intake metadata is explicitly declared or UNKNOWN.
- Inputs: `CAPTURE-IDENTITY`, `INTAKE-METADATA`; outputs: `PACKET-REF`
- Requirements: `TR-CAPTURE-INTAKE`; interfaces: `IF-EXECUTE-RECORD`
- Acceptance: `AC-SYN-TRANSFER`, `AC-EXP-SCENE`; runtime parameters: `RP-RESOURCE`; upstream: None
- Steps:
  - `S1`: Verify capture identity before parsing any block.
  - `S2`: Parse supported section and interface declarations while retaining their scope.
  - `S3`: Emit PacketRef values with exact raw ticks, resolution and length provenance.
- Invariants: Interface identity is scoped by capture and section.; Clock resolution never implies clock accuracy.; Unsupported blocks never produce an empty-success capture.
- Failure outcomes:
  - `IDENTITY-ERROR` — when Manifest identity does not match the supplied bytes. Result: Reject intake before block parsing and emit no PacketRef.
  - `UNSUPPORTED-CAPTURE` — when A required block or link type is unsupported. Result: Return a named unsupported outcome, not IUT FAIL.
- Output value mappings:
  - None
### `MOD-REASSEMBLY` — Provenance-preserving datagram reconstruction
- Responsibility: Build bounded datagram candidates from scoped packet fragments while preserving gaps, overlap conflicts and every source reference.
- Preconditions: Every fragment has a scoped PacketRef.; Resource bounds are available before buffering.
- Inputs: `PACKET-REF`; outputs: `DATAGRAM-RECORD`
- Requirements: `TR-DATAGRAM-REASSEMBLY`; interfaces: `IF-EXECUTE-RECORD`
- Acceptance: `AC-SYN-TRANSFER`; runtime parameters: `RP-RESOURCE`; upstream: `MOD-CAPTURE`
- Steps:
  - `S1`: Group fragments only by the declared scoped reconstruction identity.
  - `S2`: Compute coverage, missing ranges and overlaps without overwriting earlier bytes.
  - `S3`: Emit COMPLETE, GAPPED or CONFLICT reconstruction with all PacketRef values.
- Invariants: Fragments never cross capture, section or interface scope.; A first fragment is never treated as a complete datagram without complete coverage.
- Failure outcomes:
  - `INCOMPLETE-DATAGRAM` — when Coverage contains a gap or truncation. Result: Emit reassemblyStatus=GAPPED and no complete UDP payload.
  - `OVERLAP-CONFLICT` — when Overlapping ranges contain different bytes. Result: Preserve both sources and emit conflict, not last-write-wins data.
- Output value mappings:
  - `DATAGRAM-RECORD.reassemblyStatus` → `COMPLETE`, `GAPPED`, `CONFLICT`: A coverage gap maps to GAPPED; INCOMPLETE-DATAGRAM is a failure code, not a record-field value.
- Controlled non-overwrite reconstruction policy: `{"differentOverlap": "CONFLICT", "gapStatus": "GAPPED", "identicalOverlap": "DUPLICATE", "overlapPolicy": "IDENTICAL-ONLY", "overwriteEarlierBytes": false}`
### `MOD-TRANSFER` — TFTP transfer and protocol-event reconstruction
- Responsibility: Associate bounded TFTP transfer candidates and derive typed protocol events without inventing application-layer facts.
- Preconditions: Datagram completeness is classified.; Initial request and dynamic TID evidence remain distinguishable.
- Inputs: `DATAGRAM-RECORD`, `TRANSFER-RECORD`; outputs: `TRANSFER-RECORD`, `PROTOCOL-EVENT`
- Requirements: `TR-TRANSFER-RECONSTRUCTION`, `TR-PROTOCOL-EVENT`; interfaces: `IF-EXECUTE-RECORD`, `IF-OBS-INTERPRET`
- Acceptance: `AC-SYN-TRANSFER`, `AC-SYN-INTEGRITY`; runtime parameters: `RP-RESOURCE`; upstream: `MOD-REASSEMBLY`
- Steps:
  - `S1`: Open or retain transfer candidates from request and endpoint evidence.
  - `S2`: Apply option, block and terminal rules while retaining retransmission and ambiguity evidence.
  - `S3`: Emit typed wire or derived events with complete raw-reference chains.
- Invariants: Unknown option evidence never becomes an accepted or defaulted value.; Dynamic TID association is not replaced by a fixed port assumption.; Application facts are not inferred from wire-only evidence.
- Failure outcomes:
  - `AMBIGUOUS-TRANSFER` — when Evidence is compatible with multiple transfer candidates. Result: Retain ambiguity and withhold unique ownership claims.
  - `UNSUPPORTED-BLOCK-RANGE` — when Block progression exceeds the declared bounded range. Result: Return UNSUPPORTED without merging wrapped block identities.
- Output value mappings:
  - None
### `MOD-OWNERSHIP` — Request-instance ownership resolution
- Responsibility: Resolve response ownership under the declared matching policy while preserving cancellation, supersession and ambiguity.
- Preconditions: Candidate request instances and event order are explicit.; The matching policy is UNIQUE-KEY, FIFO or MOST-RECENT.
- Inputs: `PROTOCOL-EVENT`; outputs: `OWNERSHIP-RESULT`
- Requirements: `TR-OWNERSHIP`; interfaces: `IF-OBS-INTERPRET`
- Acceptance: `AC-SYN-TRANSFER`; runtime parameters: `RP-RESOURCE`; upstream: `MOD-TRANSFER`
- Steps:
  - `S1`: Discard candidates terminated by a valid cancellation or superseding trigger.
  - `S2`: Apply the declared policy to the remaining compatible candidates.
  - `S3`: Emit unique, unmatched or ambiguous ownership with supporting references.
- Invariants: One response is never silently consumed by two incompatible request instances.; Cancellation before a deadline prevents a later no-response failure for that obligation.
- Failure outcomes:
  - `AMBIGUOUS-OWNERSHIP` — when More than one incompatible owner remains. Result: Emit AMBIGUOUS and prohibit unique-response consumption.
- Output value mappings:
  - None
### `MOD-OBSERVATION` — Observation assessment, history update and bounded reporting
- Responsibility: Produce four-valued assessments, conservatively advance compatible histories and report bounded findings without root-cause claims.
- Preconditions: Ownership status and measurement provenance are explicit.; HistoryHandle belongs to the current session and version.
- Inputs: `OWNERSHIP-RESULT`, `PROTOCOL-EVENT`, `OBSERVATION-ASSESSMENT`, `HISTORY-HANDLE`, `INTAKE-METADATA`; outputs: `OBSERVATION-ASSESSMENT`, `HISTORY-HANDLE`, `FINDING-RECORD`
- Requirements: `TR-OBSERVATION-ASSESSMENT`, `TR-HISTORY-COMPATIBILITY`, `TR-TRACEABLE-FINDING`; interfaces: `IF-OBS-INTERPRET`, `IF-HIST-UPDATE`
- Acceptance: `AC-SYN-TRANSFER`, `AC-EXP-TRUTH`, `AC-EXP-CAUSAL`, `AC-EXP-DENOMINATOR`; runtime parameters: `RP-RESOURCE`; upstream: `MOD-TRANSFER`, `MOD-OWNERSHIP`
- Steps:
  - `S1`: Intersect measurement and requirement domains using exact interval topology.
  - `S2`: Produce PASS, FAIL, INCONCLUSIVE or ERROR without collapsing unknown evidence.
  - `S3`: Advance history only through IF-HIST-UPDATE and never revive excluded hypotheses.
  - `S4`: Emit a bounded finding with facts, scope, assumptions and evidence separated.
- Invariants: PASS requires every possible true value to satisfy the requirement.; FAIL requires every possible true value to violate the requirement.; ERROR and INCONCLUSIVE are never downgraded to FAIL.; Equal hypothesis sets may retain different compatible histories.
- Failure outcomes:
  - `INVALID-MEASUREMENT` — when The time chain, error budget or measurement-domain intersection is invalid. Result: Emit ERROR and do not exclude hypotheses.
  - `RESOURCE-UNKNOWN` — when The bounded history operation cannot complete within declared resources. Result: Retain the prior history with conservative-unknown status, not IUT FAIL.
- Output value mappings:
  - None

## Bounded algorithm refinement

### `AR-FINITE` — Bounded explicit CL-TAV reference kernel
- Boundary: No general solver, implicit discretization, completeness claim, or runtime implementation is specified. The kernel only propagates finite explicit paths over declared syntax and limits.
- Representation: A stable finite hypothesis-ID set maps each hypothesis to versioned explicit path frontiers. Guards use the existing restricted AST and exact rational interval constraints; updates are declared finite assignments. Frontiers may merge only when hypothesis, control state, clock constraints and whole-history provenance are identical.
- Conservative behavior: Unsupported syntax, a resource limit, or an undecidable feasible-path result returns the named interface UNKNOWN, GAP, SPEC-ERROR or controlled error path and never eliminates a hypothesis or proves equivalence.
- Complexity boundary: Work is bounded by the configured hypothesis count, actions, observation classes, path length and frontier states; no polynomial or completeness claim is made.
- Guard syntax: `TRUE`, `AND`, `STATE-EQUALS`, `RATIONAL-INTERVAL-CONTAINS`, `TYPED-FIELD-EQUALS`; update syntax: `STATE-ASSIGN`, `CLOCK-RESET-TO-ZERO`, `TYPED-FIELD-ASSIGN`
- Frontier: `hypothesisId`, `controlStateId`, `clockConstraint`, `typedStore`, `pathLength`, `historyProvenance`, `status`; merge key: `hypothesisId`, `controlStateId`, `clockConstraint`, `typedStore`, `historyProvenance`
- Propagation:
  - Validate the model and select-time snapshot.
  - Expand enabled transitions without dropping correlation constraints.
  - Intersect observation and timing constraints.
  - Retain each feasible successor with whole-history provenance.
  - Merge only entries with an identical merge key.
  - Reject unsupported syntax as SPEC-ERROR; return conservative unknown on a configured computation limit. Neither outcome deletes a hypothesis.
- Limit behavior: `{"actions": "ADMIT-REFUSED", "frontierStates": "CONSERVATIVE-UNKNOWN", "hypotheses": "SPEC-ERROR", "observationClasses": "PredictionGapError", "pathLength": "CONSERVATIVE-UNKNOWN"}`
- Result mapping: `{"IF-EQUIV": {"failure": ["UNKNOWN", "RESOURCE-UNKNOWN"], "success": ["established", "notEstablished", "unknown"]}, "IF-EXECUTE-RECORD": {"failure": ["CONFIRMED-NOT-SENT", "UNKNOWN-EFFECT"], "success": ["record", "effectClass", "correlationId"]}, "IF-HIST-UPDATE": {"failure": ["Stop-Empty", "RESOURCE-UNKNOWN", "CONSERVATIVE-UNKNOWN"], "success": ["HistoryHandlePrime", "Hprime", "Stop-Empty"]}, "IF-OBS-INTERPRET": {"failure": ["ERROR", "INCONCLUSIVE", "UNKNOWN-EFFECT"], "success": ["Iz", "effectClass", "summaryConfirmed", "postSummary", "ownershipResult", "measurementInterval"]}, "IF-PRED-OBS": {"failure": ["PredictionGapError", "RESOURCE-UNKNOWN"], "success": ["currentlyValidNonemptyClasses", "PredictionGapError"]}, "IF-PREP-RECOVER": {"failure": ["UNKNOWN-EFFECT", "PREP-ERROR", "CONFIRMED-NOT-SENT"], "success": ["targetConfirmed", "summaryConfirmed", "prepError", "ineligible", "declaredTarget", "evidence", "postSummary"]}, "IF-RESOURCE-STOP": {"failure": ["Stop-Budget", "Stop-Error", "Stop-645"], "success": ["stopClass", "finalH", "trace"]}, "IF-SELECT-ADMIT": {"failure": ["PredictionGapError", "SPEC-ERROR", "ADMIT-REFUSED"], "success": ["kind", "tStar", "S", "admitA2A5"]}}`
- Model instance schema: `{"clockConstraint": {"boundType": "rational", "feasibility": ["FEASIBLE", "INFEASIBLE", "COMPUTATION-UNKNOWN"], "finiteWitnessProjection": "one declared clock ID plus its rational interval; W1/W2 have exact one-clock semantics", "reset": "substitute exact zero before canonicalization", "timeAdvance": "one shared nonnegative rational delta", "type": "canonical-difference-bounds", "unsupportedProjection": "multi-clock or cross-clock relation without a named DBM projection is SPEC-ERROR, never a computed successor"}, "clockIds": ["x"], "guardAst": {"operandRepresentation": "RATIONAL-INTERVAL-CONTAINS uses a declared clock ID and one structured rational interval; strings are display-only", "supported": ["TRUE", "AND", "STATE-EQUALS", "RATIONAL-INTERVAL-CONTAINS", "TYPED-FIELD-EQUALS"], "type": "tagged-tree", "unsupported": ["OR", "NOT", "CALL"], "unsupportedBehavior": "SPEC-ERROR before expansion; preserve H, summary, and charge state"}, "rational": {"canonical": "gcd(abs(numerator),positiveDenominator)=1 and positiveDenominator>0", "required": ["numerator", "positiveDenominator"], "type": "object"}, "stateIds": ["q0", "q1", "q2", "q3"], "transition": {"additionalProperties": false, "required": ["id", "source", "target", "guardAst", "simultaneousUpdates"], "type": "object"}, "typedStore": {"keys": "declared variable IDs", "type": "finite-map", "values": "declared scalar-domain members"}, "typedVariables": {"mode": ["normal", "recovery"]}}`
- History backend → interface → S9 payload and sources: `{"backend": {"H_c": ["h0"], "eta_c": {"h0": "frontier-syn-1"}, "historyVersion": 1}, "branchWitnesses": [{"affectedHypothesisIds": [], "backend": {"H_c": ["h0"], "eta_c": {"h0": "frontier-next"}, "historyVersion": 1}, "effectKnowledge": "COMPATIBLE", "historyInputVersion": 0, "id": "HR-NO-COMMIT", "inputGamma": {"currentSummary": "q0", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "KNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "inputH": ["h0"], "inputHistoryHandle": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-old"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 0}, "interface": {"HistoryHandlePrime": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-next"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 1}, "Hprime": ["h0"], "status": "KNOWN"}, "outcome": {"postSummary": "q1", "summaryConfirmed": false}, "s9": {"GammaPrime": {"currentSummary": "q0", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "KNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "Hprime": ["h0"], "etaPrime": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-next"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 1}, "outerDisposition": "CONTINUE", "status": "OK", "summaryCommitted": false}, "snapshotVersion": 0}, {"affectedHypothesisIds": [], "backend": {"H_c": [], "eta_c": {}, "historyVersion": 1}, "effectKnowledge": "PROVEN-INCOMPATIBLE", "historyInputVersion": 0, "id": "HR-STOP-EMPTY", "inputGamma": {"currentSummary": "q0", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "KNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "inputH": ["h0"], "inputHistoryHandle": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-old"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 0}, "interface": {"HistoryHandlePrime": {"H": [], "compatibleStateByHypothesis": {}, "statusByHypothesis": {}, "version": 1}, "Hprime": [], "status": "Stop-Empty"}, "outcome": {"postSummary": null, "summaryConfirmed": false}, "s9": {"GammaPrime": {"currentSummary": "q0", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "KNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "Hprime": [], "etaPrime": {"H": [], "compatibleStateByHypothesis": {}, "statusByHypothesis": {}, "version": 1}, "outerDisposition": "Stop-Empty", "status": "OK", "summaryCommitted": false}, "snapshotVersion": 0}, {"affectedHypothesisIds": ["h0"], "backend": {"H_c": ["h0"], "eta_c": {"h0": "frontier-conservative"}, "historyVersion": 1}, "effectKnowledge": "UNKNOWN-EFFECT", "historyInputVersion": 0, "id": "HR-CONSERVATIVE", "inputGamma": {"currentSummary": "", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "UNKNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "inputH": ["h0"], "inputHistoryHandle": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-old"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 0}, "interface": {"HistoryHandlePrime": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-conservative"}, "statusByHypothesis": {"h0": "CONSERVATIVE-UNKNOWN"}, "version": 1}, "Hprime": ["h0"], "status": "CONSERVATIVE-UNKNOWN"}, "outcome": {"postSummary": null, "summaryConfirmed": false}, "s9": {"GammaPrime": {"currentSummary": "", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "UNKNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "Hprime": ["h0"], "etaPrime": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-conservative"}, "statusByHypothesis": {"h0": "CONSERVATIVE-UNKNOWN"}, "version": 1}, "outerDisposition": "CONTINUE", "status": "OK", "summaryCommitted": false}, "snapshotVersion": 0}, {"affectedHypothesisIds": [], "backend": null, "effectKnowledge": "VERSION-MISMATCH", "historyInputVersion": 0, "id": "HR-VERSION-MISMATCH", "inputGamma": {"currentSummary": "q0", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "KNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "inputH": ["h0"], "inputHistoryHandle": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-old"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 0}, "interface": null, "outcome": {"postSummary": "q1", "summaryConfirmed": true}, "s9": {"GammaPrime": {"currentSummary": "q0", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "KNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "Hprime": ["h0"], "etaPrime": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-old"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 0}, "outerDisposition": "Stop-Error", "reason": "history version mismatch", "status": "SPEC-ERROR", "summaryCommitted": false}, "snapshotVersion": 1}], "inputGamma": {"currentSummary": "q0", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "KNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "interface": {"HistoryHandlePrime": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-syn-1"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 1}, "Hprime": ["h0"], "status": "KNOWN"}, "normalizedOutcome": {"postSummary": "q1", "summaryConfirmed": true}, "s9": {"GammaPrime": {"currentSummary": "q1", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "KNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "Hprime": ["h0"], "etaPrime": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-syn-1"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 1}, "status": "OK", "summaryCommitted": true, "summaryConfirmed": true}, "sourceMap": {"interface.HistoryHandlePrime.compatibleStateByHypothesis": "backend.eta_c", "interface.HistoryHandlePrime.version": "backend.historyVersion", "interface.Hprime": "backend.H_c", "s9.GammaPrime.currentSummary": "normalizedOutcome.postSummary when the S9 guard holds; otherwise inputGamma.currentSummary", "s9.GammaPrime.otherSessionFields": "inputGamma unchanged; S7/S8 effects are upstream of S9", "s9.GammaPrime.qStatus": "inputGamma.qStatus", "s9.Hprime": "interface.Hprime", "s9.etaPrime": "interface.HistoryHandlePrime"}}`
- Internal results: `FEASIBLE`, `INFEASIBLE`, `COMPUTATION-UNKNOWN`, `UNSUPPORTED-SYNTAX`, `LIMIT-REACHED`, `EMPTY-HISTORY`
- Propagation rules: `[{"id": "FK-VALIDATE", "rule": "Reject unsupported AST nodes or ill-typed operands as SPEC-ERROR before expansion."}, {"id": "FK-ADVANCE", "rule": "Advance all clocks by one shared nonnegative rational delta and retain difference correlations."}, {"id": "FK-INTERSECT", "rule": "Conjoin transition guard, observation class, and timing interval; canonicalize before feasibility classification."}, {"id": "FK-UPDATE", "rule": "Apply state/clock/store updates simultaneously, then canonicalize the successor constraint."}, {"id": "FK-MERGE", "rule": "Merge only entries identical on hypothesisId, controlStateId, clockConstraint, typedStore, and historyProvenance."}, {"id": "FK-LIMIT", "rule": "Path/frontier limits return CONSERVATIVE-UNKNOWN without deleting hypotheses; they never produce Stop-Empty or equivalence."}]`
- Total return mapping: `[{"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-PRED-OBS", "internalResult": "FEASIBLE", "output": "currentlyValidNonemptyClasses", "reachable": true, "returnContract": {"adapter": "OK for FEASIBLE nonempty projection; all conservative failures become GAP with a named reason", "branchTag": "FEASIBLE", "fieldSources": {"classesByTest": "KERNEL", "historyVersionUsed": "KERNEL", "reason": "KERNEL", "status": "KERNEL", "uncertaintyRef": "KERNEL"}, "recordType": "PredictionResult", "requiredFields": ["status", "reason", "classesByTest", "historyVersionUsed", "uncertaintyRef"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-PRED-OBS", "internalResult": "INFEASIBLE", "output": "PredictionGapError", "reachable": true, "returnContract": {"adapter": "OK for FEASIBLE nonempty projection; all conservative failures become GAP with a named reason", "branchTag": "INFEASIBLE", "fieldSources": {"historyVersionUsed": "KERNEL", "reason": "KERNEL", "status": "KERNEL", "uncertaintyRef": "KERNEL"}, "recordType": "PredictionResult", "requiredFields": ["status", "reason", "historyVersionUsed", "uncertaintyRef"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-PRED-OBS", "internalResult": "COMPUTATION-UNKNOWN", "output": "RESOURCE-UNKNOWN", "reachable": true, "returnContract": {"adapter": "OK for FEASIBLE nonempty projection; all conservative failures become GAP with a named reason", "branchTag": "COMPUTATION-UNKNOWN", "fieldSources": {"historyVersionUsed": "KERNEL", "reason": "KERNEL", "status": "KERNEL", "uncertaintyRef": "KERNEL"}, "recordType": "PredictionResult", "requiredFields": ["status", "reason", "historyVersionUsed", "uncertaintyRef"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-PRED-OBS", "internalResult": "UNSUPPORTED-SYNTAX", "output": "PredictionGapError", "reachable": true, "returnContract": {"adapter": "OK for FEASIBLE nonempty projection; all conservative failures become GAP with a named reason", "branchTag": "UNSUPPORTED-SYNTAX", "fieldSources": {"historyVersionUsed": "KERNEL", "reason": "KERNEL", "status": "KERNEL", "uncertaintyRef": "KERNEL"}, "recordType": "PredictionResult", "requiredFields": ["status", "reason", "historyVersionUsed", "uncertaintyRef"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-PRED-OBS", "internalResult": "LIMIT-REACHED", "output": "RESOURCE-UNKNOWN", "reachable": true, "returnContract": {"adapter": "OK for FEASIBLE nonempty projection; all conservative failures become GAP with a named reason", "branchTag": "LIMIT-REACHED", "fieldSources": {"historyVersionUsed": "KERNEL", "reason": "KERNEL", "status": "KERNEL", "uncertaintyRef": "KERNEL"}, "recordType": "PredictionResult", "requiredFields": ["status", "reason", "historyVersionUsed", "uncertaintyRef"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-PRED-OBS", "internalResult": "EMPTY-HISTORY", "output": "PredictionGapError", "reachable": true, "returnContract": {"adapter": "OK for FEASIBLE nonempty projection; all conservative failures become GAP with a named reason", "branchTag": "EMPTY-HISTORY", "fieldSources": {"historyVersionUsed": "KERNEL", "reason": "KERNEL", "status": "KERNEL", "uncertaintyRef": "KERNEL"}, "recordType": "PredictionResult", "requiredFields": ["status", "reason", "historyVersionUsed", "uncertaintyRef"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-SELECT-ADMIT", "internalResult": "FEASIBLE", "output": "admitA2A5", "reachable": true, "returnContract": {"adapter": "Prediction GAP is TEST-scoped; eligible affordable Prep/Recover still pass A1-A5 admission", "branchTag": "FEASIBLE", "fieldSources": {"actionId": "KERNEL", "actionKind": "KERNEL", "classesUsed": "KERNEL", "kind": "KERNEL", "reason": "KERNEL"}, "recordType": "Decision", "requiredFields": ["kind", "actionKind", "actionId", "classesUsed", "reason"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-SELECT-ADMIT", "internalResult": "INFEASIBLE", "output": "PredictionGapError", "reachable": true, "returnContract": {"adapter": "Prediction GAP is TEST-scoped; eligible affordable Prep/Recover still pass A1-A5 admission", "branchTag": "INFEASIBLE", "fieldSources": {"actionId": "KERNEL", "actionKind": "KERNEL", "classesUsed": "KERNEL", "kind": "KERNEL", "reason": "KERNEL"}, "recordType": "Decision", "requiredFields": ["kind", "actionKind", "actionId", "classesUsed", "reason"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-SELECT-ADMIT", "internalResult": "COMPUTATION-UNKNOWN", "output": "ADMIT-REFUSED", "reachable": true, "returnContract": {"adapter": "Prediction GAP is TEST-scoped; eligible affordable Prep/Recover still pass A1-A5 admission", "branchTag": "COMPUTATION-UNKNOWN", "fieldSources": {"actionId": "KERNEL", "actionKind": "KERNEL", "classesUsed": "KERNEL", "kind": "KERNEL", "reason": "KERNEL"}, "recordType": "Decision", "requiredFields": ["kind", "actionKind", "actionId", "classesUsed", "reason"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-SELECT-ADMIT", "internalResult": "UNSUPPORTED-SYNTAX", "output": "SPEC-ERROR", "reachable": true, "returnContract": {"adapter": "Prediction GAP is TEST-scoped; eligible affordable Prep/Recover still pass A1-A5 admission", "branchTag": "UNSUPPORTED-SYNTAX", "fieldSources": {"actionId": "KERNEL", "actionKind": "KERNEL", "classesUsed": "KERNEL", "kind": "KERNEL", "reason": "KERNEL"}, "recordType": "Decision", "requiredFields": ["kind", "actionKind", "actionId", "classesUsed", "reason"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-SELECT-ADMIT", "internalResult": "LIMIT-REACHED", "output": "ADMIT-REFUSED", "reachable": true, "returnContract": {"adapter": "Prediction GAP is TEST-scoped; eligible affordable Prep/Recover still pass A1-A5 admission", "branchTag": "LIMIT-REACHED", "fieldSources": {"actionId": "KERNEL", "actionKind": "KERNEL", "classesUsed": "KERNEL", "kind": "KERNEL", "reason": "KERNEL"}, "recordType": "Decision", "requiredFields": ["kind", "actionKind", "actionId", "classesUsed", "reason"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-SELECT-ADMIT", "internalResult": "EMPTY-HISTORY", "output": "PredictionGapError", "reachable": true, "returnContract": {"adapter": "Prediction GAP is TEST-scoped; eligible affordable Prep/Recover still pass A1-A5 admission", "branchTag": "EMPTY-HISTORY", "fieldSources": {"actionId": "KERNEL", "actionKind": "KERNEL", "classesUsed": "KERNEL", "kind": "KERNEL", "reason": "KERNEL"}, "recordType": "Decision", "requiredFields": ["kind", "actionKind", "actionId", "classesUsed", "reason"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-EXECUTE-RECORD", "internalResult": "FEASIBLE", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "FEASIBLE", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-EXECUTE-RECORD", "internalResult": "INFEASIBLE", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "INFEASIBLE", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-EXECUTE-RECORD", "internalResult": "COMPUTATION-UNKNOWN", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "COMPUTATION-UNKNOWN", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-EXECUTE-RECORD", "internalResult": "UNSUPPORTED-SYNTAX", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "UNSUPPORTED-SYNTAX", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-EXECUTE-RECORD", "internalResult": "LIMIT-REACHED", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "LIMIT-REACHED", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-EXECUTE-RECORD", "internalResult": "EMPTY-HISTORY", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "EMPTY-HISTORY", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-OBS-INTERPRET", "internalResult": "FEASIBLE", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "FEASIBLE", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-OBS-INTERPRET", "internalResult": "INFEASIBLE", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "INFEASIBLE", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-OBS-INTERPRET", "internalResult": "COMPUTATION-UNKNOWN", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "COMPUTATION-UNKNOWN", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-OBS-INTERPRET", "internalResult": "UNSUPPORTED-SYNTAX", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "UNSUPPORTED-SYNTAX", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-OBS-INTERPRET", "internalResult": "LIMIT-REACHED", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "LIMIT-REACHED", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-OBS-INTERPRET", "internalResult": "EMPTY-HISTORY", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "EMPTY-HISTORY", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-PREP-RECOVER", "internalResult": "FEASIBLE", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "FEASIBLE", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-PREP-RECOVER", "internalResult": "INFEASIBLE", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "INFEASIBLE", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-PREP-RECOVER", "internalResult": "COMPUTATION-UNKNOWN", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "COMPUTATION-UNKNOWN", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-PREP-RECOVER", "internalResult": "UNSUPPORTED-SYNTAX", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "UNSUPPORTED-SYNTAX", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-PREP-RECOVER", "internalResult": "LIMIT-REACHED", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "LIMIT-REACHED", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-PREP-RECOVER", "internalResult": "EMPTY-HISTORY", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "EMPTY-HISTORY", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "INTERSECT-PROVEN", "interfaceId": "IF-HIST-UPDATE", "internalResult": "FEASIBLE", "output": "Hprime", "reachable": true, "returnContract": {"adapter": "Backend returns eta_c and H_c; IF-HIST-UPDATE exposes their typed aliases; S9 alone constructs GammaPrime and commits a confirmed summary.", "branchTag": "FEASIBLE", "fieldSources": {"HistoryHandlePrime": "INTERFACE-ADAPTER", "Hprime": "BACKEND-ALIAS", "compatibleStateByHypothesis": "KERNEL", "historyVersion": "KERNEL", "status": "KERNEL", "summaryEffect": "KERNEL"}, "recordType": "HistoryUpdateResult", "requiredFields": ["status", "compatibleStateByHypothesis", "Hprime", "HistoryHandlePrime", "historyVersion", "summaryEffect"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "INTERSECT-PROVEN", "interfaceId": "IF-HIST-UPDATE", "internalResult": "INFEASIBLE", "output": "Hprime", "reachable": true, "returnContract": {"adapter": "Backend returns eta_c and H_c; IF-HIST-UPDATE exposes their typed aliases; S9 alone constructs GammaPrime and commits a confirmed summary.", "branchTag": "INFEASIBLE", "fieldSources": {"HistoryHandlePrime": "INTERFACE-ADAPTER", "Hprime": "BACKEND-ALIAS", "compatibleStateByHypothesis": "KERNEL", "historyVersion": "KERNEL", "status": "KERNEL", "summaryEffect": "KERNEL"}, "recordType": "HistoryUpdateResult", "requiredFields": ["status", "compatibleStateByHypothesis", "Hprime", "HistoryHandlePrime", "historyVersion", "summaryEffect"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-HIST-UPDATE", "internalResult": "COMPUTATION-UNKNOWN", "output": "CONSERVATIVE-UNKNOWN", "reachable": true, "returnContract": {"adapter": "Backend returns eta_c and H_c; IF-HIST-UPDATE exposes their typed aliases; S9 alone constructs GammaPrime and commits a confirmed summary.", "branchTag": "COMPUTATION-UNKNOWN", "fieldSources": {"HistoryHandlePrime": "INTERFACE-ADAPTER", "Hprime": "BACKEND-ALIAS", "compatibleStateByHypothesis": "KERNEL", "historyVersion": "KERNEL", "status": "KERNEL", "summaryEffect": "KERNEL"}, "recordType": "HistoryUpdateResult", "requiredFields": ["status", "compatibleStateByHypothesis", "Hprime", "HistoryHandlePrime", "historyVersion", "summaryEffect"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-HIST-UPDATE", "internalResult": "UNSUPPORTED-SYNTAX", "output": "CONSERVATIVE-UNKNOWN", "reachable": true, "returnContract": {"adapter": "Backend returns eta_c and H_c; IF-HIST-UPDATE exposes their typed aliases; S9 alone constructs GammaPrime and commits a confirmed summary.", "branchTag": "UNSUPPORTED-SYNTAX", "fieldSources": {"HistoryHandlePrime": "INTERFACE-ADAPTER", "Hprime": "BACKEND-ALIAS", "compatibleStateByHypothesis": "KERNEL", "historyVersion": "KERNEL", "status": "KERNEL", "summaryEffect": "KERNEL"}, "recordType": "HistoryUpdateResult", "requiredFields": ["status", "compatibleStateByHypothesis", "Hprime", "HistoryHandlePrime", "historyVersion", "summaryEffect"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-HIST-UPDATE", "internalResult": "LIMIT-REACHED", "output": "CONSERVATIVE-UNKNOWN", "reachable": true, "returnContract": {"adapter": "Backend returns eta_c and H_c; IF-HIST-UPDATE exposes their typed aliases; S9 alone constructs GammaPrime and commits a confirmed summary.", "branchTag": "LIMIT-REACHED", "fieldSources": {"HistoryHandlePrime": "INTERFACE-ADAPTER", "Hprime": "BACKEND-ALIAS", "compatibleStateByHypothesis": "KERNEL", "historyVersion": "KERNEL", "status": "KERNEL", "summaryEffect": "KERNEL"}, "recordType": "HistoryUpdateResult", "requiredFields": ["status", "compatibleStateByHypothesis", "Hprime", "HistoryHandlePrime", "historyVersion", "summaryEffect"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "EMPTY-PROVEN", "interfaceId": "IF-HIST-UPDATE", "internalResult": "EMPTY-HISTORY", "output": "Stop-Empty", "reachable": true, "returnContract": {"adapter": "Backend returns eta_c and H_c; IF-HIST-UPDATE exposes their typed aliases; S9 alone constructs GammaPrime and commits a confirmed summary.", "branchTag": "EMPTY-HISTORY", "fieldSources": {"HistoryHandlePrime": "INTERFACE-ADAPTER", "Hprime": "BACKEND-ALIAS", "compatibleStateByHypothesis": "KERNEL", "historyVersion": "KERNEL", "status": "KERNEL", "summaryEffect": "KERNEL"}, "recordType": "HistoryUpdateResult", "requiredFields": ["status", "compatibleStateByHypothesis", "Hprime", "HistoryHandlePrime", "historyVersion", "summaryEffect"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-EQUIV", "internalResult": "FEASIBLE", "output": "notEstablished", "reachable": true, "returnContract": {"adapter": "FEASIBLE is notEstablished unless a declared equivalence proof exists", "branchTag": "FEASIBLE", "fieldSources": {"proofBasis": "KERNEL", "status": "KERNEL"}, "recordType": "EquivalenceResult", "requiredFields": ["status", "proofBasis"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-EQUIV", "internalResult": "INFEASIBLE", "output": "notEstablished", "reachable": true, "returnContract": {"adapter": "FEASIBLE is notEstablished unless a declared equivalence proof exists", "branchTag": "INFEASIBLE", "fieldSources": {"proofBasis": "KERNEL", "status": "KERNEL"}, "recordType": "EquivalenceResult", "requiredFields": ["status", "proofBasis"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-EQUIV", "internalResult": "COMPUTATION-UNKNOWN", "output": "unknown", "reachable": true, "returnContract": {"adapter": "FEASIBLE is notEstablished unless a declared equivalence proof exists", "branchTag": "COMPUTATION-UNKNOWN", "fieldSources": {"proofBasis": "KERNEL", "status": "KERNEL"}, "recordType": "EquivalenceResult", "requiredFields": ["status", "proofBasis"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-EQUIV", "internalResult": "UNSUPPORTED-SYNTAX", "output": "unknown", "reachable": true, "returnContract": {"adapter": "FEASIBLE is notEstablished unless a declared equivalence proof exists", "branchTag": "UNSUPPORTED-SYNTAX", "fieldSources": {"proofBasis": "KERNEL", "status": "KERNEL"}, "recordType": "EquivalenceResult", "requiredFields": ["status", "proofBasis"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-EQUIV", "internalResult": "LIMIT-REACHED", "output": "unknown", "reachable": true, "returnContract": {"adapter": "FEASIBLE is notEstablished unless a declared equivalence proof exists", "branchTag": "LIMIT-REACHED", "fieldSources": {"proofBasis": "KERNEL", "status": "KERNEL"}, "recordType": "EquivalenceResult", "requiredFields": ["status", "proofBasis"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-EQUIV", "internalResult": "EMPTY-HISTORY", "output": "notEstablished", "reachable": true, "returnContract": {"adapter": "FEASIBLE is notEstablished unless a declared equivalence proof exists", "branchTag": "EMPTY-HISTORY", "fieldSources": {"proofBasis": "KERNEL", "status": "KERNEL"}, "recordType": "EquivalenceResult", "requiredFields": ["status", "proofBasis"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-RESOURCE-STOP", "internalResult": "FEASIBLE", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "FEASIBLE", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-RESOURCE-STOP", "internalResult": "INFEASIBLE", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "INFEASIBLE", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-RESOURCE-STOP", "internalResult": "COMPUTATION-UNKNOWN", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "COMPUTATION-UNKNOWN", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-RESOURCE-STOP", "internalResult": "UNSUPPORTED-SYNTAX", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "UNSUPPORTED-SYNTAX", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-RESOURCE-STOP", "internalResult": "LIMIT-REACHED", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "LIMIT-REACHED", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-RESOURCE-STOP", "internalResult": "EMPTY-HISTORY", "output": "stopClass=Stop-Empty", "reachable": true, "returnContract": {"adapter": "Apply Empty, Singleton, 645, Equivalent, Budget ordering; retry exhaustion remains Stop-Error", "branchTag": "EMPTY-HISTORY", "fieldSources": {"finalH": "KERNEL", "stopClass": "KERNEL", "trace": "KERNEL"}, "recordType": "StopResult", "requiredFields": ["stopClass", "finalH", "trace"]}, "summaryEffect": "PRESERVE"}]`
- Witness vectors: `[{"expected": {"clockConstraint": {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 1, "positiveDenominator": 1}, "upperClosed": true}, "result": "FEASIBLE", "state": "q1", "typedStore": {"mode": "normal"}}, "id": "FK-W1-FEASIBLE", "input": {"clockConstraint": {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 1, "positiveDenominator": 1}, "upperClosed": true}, "delta": {"numerator": 0, "positiveDenominator": 1}, "guard": {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 2, "positiveDenominator": 1}, "upperClosed": true}, "observation": "response", "projectionClock": "x", "quantifier": "EXISTS-DELTA", "state": "q0", "transition": {"guardAst": {"clock": "x", "interval": {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 2, "positiveDenominator": 1}, "upperClosed": true}, "tag": "RATIONAL-INTERVAL-CONTAINS"}, "id": "t01", "simultaneousUpdates": [], "source": "q0", "target": "q1"}, "typedStore": {"mode": "normal"}}}, {"expected": {"result": "INFEASIBLE", "successorCount": 0}, "id": "FK-W2-INFEASIBLE", "input": {"clockConstraint": {"lower": {"numerator": 3, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 4, "positiveDenominator": 1}, "upperClosed": true}, "delta": {"numerator": 0, "positiveDenominator": 1}, "guard": {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 2, "positiveDenominator": 1}, "upperClosed": true}, "observation": "response", "projectionClock": "x", "quantifier": "EXISTS-DELTA", "state": "q0", "transition": {"guardAst": {"clock": "x", "interval": {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 2, "positiveDenominator": 1}, "upperClosed": true}, "tag": "RATIONAL-INTERVAL-CONTAINS"}, "id": "t02", "simultaneousUpdates": [], "source": "q0", "target": "q2"}, "typedStore": {"mode": "normal"}}}, {"expected": {"externalDisposition": "SPEC-ERROR", "preserveHypotheses": true, "result": "UNSUPPORTED-SYNTAX"}, "id": "FK-W3-UNKNOWN", "input": {"clockConstraint": {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 1, "positiveDenominator": 1}, "upperClosed": true}, "delta": {"numerator": 0, "positiveDenominator": 1}, "guard": {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 1, "positiveDenominator": 1}, "upperClosed": true}, "observation": "response", "quantifier": "EXISTS-DELTA", "state": "q0", "transition": {"guardAst": {"name": "unsupported", "tag": "CALL"}, "id": "t03", "simultaneousUpdates": [], "source": "q0", "target": "q3"}}}, {"expected": {"merge": false, "reason": "historyProvenance differs"}, "id": "FK-W4-HISTORY", "input": {"frontiers": ["frontier-a", "frontier-b"], "sameH": ["h0"]}}, {"expected": {"merge": false, "reason": "clockConstraint differs"}, "id": "FK-W5-CLOCK", "input": {"clockConstraints": [{"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 1, "positiveDenominator": 1}, "upperClosed": true}, {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 2, "positiveDenominator": 1}, "upperClosed": true}], "clockId": "x", "sameH": ["h0"]}}]`
- Interface bindings:
- Return relation: Γ and the versioned HistoryHandle η are separate. S9 preserves Γ.qStatus and all other session fields; only a KNOWN status, confirmed summary flag, and confirmed postSummary permit a currentSummary commit. A version mismatch returns SPEC-ERROR with the original η/H/Γ.
  - `IF-PRED-OBS` — inputs `SessionContext`, `HistoryHandle`, `H`, `measurementUncertainty`, `actionLibrary`; outputs `currentlyValidNonemptyClasses`, `PredictionGapError`; read: Reads the versioned HistoryHandle and current session only.; write: Read-only; does not charge or write Γ/η.; failures: `PredictionGapError`, `RESOURCE-UNKNOWN`; parameters: `RP-HYPOTHESIS-COUNT`, `RP-FRONTIER-STATE-COUNT`, `RP-OBSERVATION-CLASS-COUNT`; time: Uses the session U and declared measurement uncertainty without changing either.; acceptance: `AC-SYN-PREDICTION`; location: `future/reference_kernel/prediction.py`
  - `IF-SELECT-ADMIT` — inputs `A`, `q`, `currentlyValidNonemptyClasses`, `SessionContext`, `HistoryHandle`, `H`; outputs `kind`, `tStar`, `S`, `admitA2A5`; read: Reads select-time inputs and candidate actions.; write: Read-only; S3-SNAP constructs the immutable final SelectSnapshot after this interface returns.; failures: `PredictionGapError`, `SPEC-ERROR`, `ADMIT-REFUSED`; parameters: `RP-ACTION-COUNT`, `RP-OBSERVATION-CLASS-COUNT`, `RP-RESOURCE-MODE`; time: Uses the same U identity as prediction and later interpretation.; acceptance: `AC-SYN-SELECT`; location: `future/reference_kernel/selection.py`
  - `IF-EXECUTE-RECORD` — inputs `SessionContext`, `admitted tStar`; outputs `record`, `effectClass`, `correlationId`; read: Reads an admitted final snapshot only.; write: Writes one session-log execution record after the single charge.; failures: `CONFIRMED-NOT-SENT`, `UNKNOWN-EFFECT`; parameters: `RP-RESOURCE-MODE`, `RP-RETRY-CAP`; time: Execution cannot replace the select-time snapshot or U.; acceptance: `AC-SYN-TRANSFER`; location: `future/offline_adapter/execution_record.py`
  - `IF-OBS-INTERPRET` — inputs `SessionContext`, `executionRecord`, `clocks`, `epsilon`; outputs `Iz`, `effectClass`, `summaryConfirmed`, `postSummary`, `ownershipResult`, `measurementInterval`; read: Reads owned event evidence and declared clock/error sources.; write: Returns interpretation values only; does not exclude H.; failures: `ERROR`, `INCONCLUSIVE`, `UNKNOWN-EFFECT`; parameters: `RP-OBSERVATION-CLASS-COUNT`; time: Preserves interval topology and U identity; invalid timing evidence returns ERROR.; acceptance: `AC-SYN-OBSERVATION`; location: `future/reference_kernel/interpretation.py`
  - `IF-PREP-RECOVER` — inputs `SessionContext`, `HistoryHandle`, `tStar`, `record`; outputs `targetConfirmed`, `summaryConfirmed`, `prepError`, `ineligible`, `declaredTarget`, `evidence`, `postSummary`; read: Reads session, history and the admitted action record.; write: Returns values only; S8/S9 retain the sole Γ writers.; failures: `UNKNOWN-EFFECT`, `PREP-ERROR`, `CONFIRMED-NOT-SENT`; parameters: `RP-RETRY-CAP`, `RP-RESOURCE-MODE`; time: A confirmation is evaluated before retry accounting and does not rewrite U.; acceptance: `AC-SYN-PREP-RECOVER`; location: `future/reference_kernel/recovery.py`
  - `IF-HIST-UPDATE` — inputs `HistoryHandle`, `H`, `tStar`, `qUsedAtSelect`, `classesUsedAtSelect`, `historyVersion`, `valid Iz`, `postSummary`; outputs `HistoryHandlePrime`, `Hprime`, `Stop-Empty`; read: Reads the select-time snapshot and whole-history frontier.; write: Writes the next versioned HistoryHandle only through normalized outcomes.; failures: `Stop-Empty`, `RESOURCE-UNKNOWN`, `CONSERVATIVE-UNKNOWN`; parameters: `RP-HYPOTHESIS-COUNT`, `RP-PATH-LENGTH`, `RP-FRONTIER-STATE-COUNT`; time: Carries the select-time U identity and never substitutes post-effect summary for qUsedAtSelect.; acceptance: `AC-SYN-HISTORY`; location: `future/reference_kernel/history.py`
  - `IF-EQUIV` — inputs `SessionContext`, `H`, `HistoryHandle`, `remainingTests`; outputs `established`, `notEstablished`, `unknown`; read: Reads finite-domain state only.; write: Read-only; does not alter H or history.; failures: `UNKNOWN`, `RESOURCE-UNKNOWN`; parameters: `RP-HYPOTHESIS-COUNT`, `RP-PATH-LENGTH`, `RP-ACTION-COUNT`; time: Uses only declared bounded horizons; no available one-step test is not proof of equivalence.; acceptance: `AC-SYN-EQUIVALENCE`; location: `future/reference_kernel/equivalence.py`
  - `IF-RESOURCE-STOP` — inputs `SessionContext`, `H`, `HistoryHandle`, `named645Residuals`, `equivalenceStatus`; outputs `stopClass`, `finalH`, `trace`; read: Reads charged resources, retained history and named residuals.; write: Writes an auditable stop trace only.; failures: `Stop-Budget`, `Stop-Error`, `Stop-645`; parameters: `RP-RESOURCE-MODE`, `RP-RETRY-CAP`; time: Preserves exclusive stop order and never converts retry exhaustion into budget exhaustion.; acceptance: `AC-SYN-RESOURCE-STOP`; location: `future/reference_kernel/stopping.py`

## Experiment interface bindings

- `IF-EXP-SCENE` — inputs `sceneId`, `configId`, `IUT`, `faultPlan`, `resourceMode`; outputs `sceneRecord`, `unconfirmed`; read: evaluator-and-operator; write: Writes only the named experiment record in the evaluator or algorithm-visible store declared by visibility.; failure: missing identity is not a runnable scene; resource: declared mode only; acceptance: `AC-EXP-SCENE`; location: `future/experiment/scene.py`
- `IF-EXP-INJECT` — inputs `sceneId`, `injectionPlan`; outputs `injectionAttempt`, `injectionConfirmed`, `injectionUnconfirmed`; read: evaluator-only confirmation; write: Writes only the named experiment record in the evaluator or algorithm-visible store declared by visibility.; failure: planned is not confirmed; unconfirmed is not valid truth; resource: injection wall-clock is evaluator metadata; acceptance: `AC-EXP-TRUTH`; location: `future/experiment/inject.py`
- `IF-EXP-TRUTH` — inputs `sceneId`, `injectionConfirmed`, `independentGeneratorId`; outputs `truthRecord`, `sharedComponentRisk`; read: evaluator-only; never an algorithm input; write: Writes only the named experiment record in the evaluator or algorithm-visible store declared by visibility.; failure: unconfirmed injection cannot default to valid truth; separate store is not independence; resource: not charged to arms; acceptance: `AC-EXP-TRUTH`; location: `future/experiment/truth.py`
- `IF-EXP-COLLECT` — inputs `sceneId`, `armId`, `algorithmVisibleRecord`; outputs `observationLog`, `resourceLog`; read: algorithm-visible only; write: Writes only the named experiment record in the evaluator or algorithm-visible store declared by visibility.; failure: missing correlation id is invalid observation; resource: same charged vector as ALG-CLTAV-01; acceptance: `AC-EXP-CAUSAL`; location: `future/experiment/collect.py`
- `IF-EXP-RUN` — inputs `sceneId`, `armId`, `SessionContext`; outputs `runId`, `stopClass`, `traceRef`; read: algorithm-visible plus evaluator run id; write: Writes only the named experiment record in the evaluator or algorithm-visible store declared by visibility.; failure: arm abort is ERROR, not PASS; resource: one declared mode; no gifted CL-LOOP records; acceptance: `AC-EXP-SCENE`; location: `future/experiment/run.py`
- `IF-EXP-FILTER` — inputs `runId`, `truthRecord`, `observationLog`, `sceneId`, `attemptId`, `injectionUnconfirmed`; outputs `validityClass`, `filterReason`; read: evaluator-only labels; algorithm does not see the class name as a select input; write: Writes only the named experiment record in the evaluator or algorithm-visible store declared by visibility.; failure: unconfirmed, invalid, equivalent, or abstain are not detection PASS/FAIL; resource: not a second charge; acceptance: `AC-EXP-CAUSAL`; location: `future/experiment/filter.py`
- `IF-EXP-EVAL` — inputs `runId`, `validityClass`, `denominators`, `truthRecord`, `algorithmResultRef`, `chargedCost`, `sceneId`, `attemptId`; outputs `metricCells`, `attemptDenominator`, `answeredSubsetDenominator`; read: evaluator-only metrics; write: Writes only the named experiment record in the evaluator or algorithm-visible store declared by visibility.; failure: missing denominator definition or missing declared record/ref is not a result; resource: report charged cost; do not hide Prep/Recover/retry; acceptance: `AC-EXP-DENOMINATOR`; location: `future/experiment/eval.py`

## Runtime parameter contracts

### `RP-RESOURCE` — Offline buffering resource bound
- Unit/domain: bytes and records / `POSITIVE-INTEGER`
- Configuration: A concrete value is required before buffering; it is not inferred from a capture.
- Owner scope: offline capture and reconstruction modules
- Exhaustion: Return a bounded resource/decode outcome, retain provenance and do not report protocol PASS/FAIL.
- Acceptance: `AC-SYN-TRANSFER`
### `RP-HYPOTHESIS-COUNT` — Hypothesis count bound
- Unit/domain: hypotheses / `POSITIVE-INTEGER`
- Configuration: A finite H0 cardinality is configured for the declared model domain.
- Owner scope: bounded reference kernel
- Exhaustion: Return conservative unknown without eliminating a hypothesis.
- Acceptance: `AC-SYN-PREDICTION`, `AC-SYN-HISTORY`
### `RP-PATH-LENGTH` — Feasible path length bound
- Unit/domain: transitions / `POSITIVE-INTEGER`
- Configuration: The bounded horizon is declared per reference-kernel invocation.
- Owner scope: bounded reference kernel
- Exhaustion: Return unknown; exceeding the horizon is not proof of infeasibility.
- Acceptance: `AC-SYN-HISTORY`, `AC-SYN-EQUIVALENCE`
### `RP-FRONTIER-STATE-COUNT` — Per-hypothesis frontier bound
- Unit/domain: states per hypothesis / `POSITIVE-INTEGER`
- Configuration: A finite frontier capacity is configured before propagation.
- Owner scope: history propagation
- Exhaustion: Retain prior compatible history with conservative-unknown status.
- Acceptance: `AC-SYN-PREDICTION`, `AC-SYN-HISTORY`
### `RP-ACTION-COUNT` — Action-library bound
- Unit/domain: actions / `POSITIVE-INTEGER`
- Configuration: The admitted candidate action library is finite and identified.
- Owner scope: selection and equivalence
- Exhaustion: Refuse unenumerated actions; do not silently score them.
- Acceptance: `AC-SYN-SELECT`, `AC-SYN-EQUIVALENCE`
### `RP-OBSERVATION-CLASS-COUNT` — Observation-class bound
- Unit/domain: classes / `POSITIVE-INTEGER`
- Configuration: A finite current projection is declared before scoring.
- Owner scope: prediction, selection and interpretation
- Exhaustion: Return named GAP or conservative unknown, never a zero score.
- Acceptance: `AC-SYN-PREDICTION`, `AC-SYN-SELECT`, `AC-SYN-OBSERVATION`
### `RP-RETRY-CAP` — Retry cap
- Unit/domain: attempts / `POSITIVE-INTEGER`
- Configuration: The retry cap is an explicit positive integer and is separate from charged resource mode.
- Owner scope: recovery and stopping
- Exhaustion: Return Stop-Error; do not convert it to Stop-Budget.
- Acceptance: `AC-SYN-PREP-RECOVER`, `AC-SYN-RESOURCE-STOP`
### `RP-RESOURCE-MODE` — Exclusive resource mode
- Unit/domain: BUDGET or ROUNDS / `EXCLUSIVE-RESOURCE-MODE`
- Configuration: Exactly one declared mode is selected for a session.
- Owner scope: selection, execution, recovery and stopping
- Exhaustion: An unadmitted action is not issued or charged; inability to afford recovery differs from ineligibility.
- Acceptance: `AC-SYN-SELECT`, `AC-SYN-PREP-RECOVER`, `AC-SYN-RESOURCE-STOP`

## Acceptance cases

### `AC-SYN-TRANSFER` — Scoped transfer reconstruction witness
- Inputs: `CAPTURE-IDENTITY`, `PACKET-REF`, `DATAGRAM-RECORD`, `TRANSFER-RECORD`, `OWNERSHIP-RESULT`, `OBSERVATION-ASSESSMENT`, `HISTORY-HANDLE`, `FINDING-RECORD`
- Tools: `TR-CAPTURE-INTAKE`, `TR-DATAGRAM-REASSEMBLY`, `TR-TRANSFER-RECONSTRUCTION`, `TR-PROTOCOL-EVENT`, `TR-OWNERSHIP`, `TR-OBSERVATION-ASSESSMENT`, `TR-HISTORY-COMPATIBILITY`, `TR-TRACEABLE-FINDING`; modules: `MOD-CAPTURE`, `MOD-REASSEMBLY`, `MOD-TRANSFER`, `MOD-OWNERSHIP`, `MOD-OBSERVATION`; algorithm interfaces: `IF-EXECUTE-RECORD`, `IF-OBS-INTERPRET`, `IF-HIST-UPDATE`; experiment interfaces: None
- Input fixture: `{"caseId": "AC-SYN-TRANSFER", "recordIds": ["CAPTURE-IDENTITY", "PACKET-REF", "DATAGRAM-RECORD", "TRANSFER-RECORD", "OWNERSHIP-RESULT", "OBSERVATION-ASSESSMENT", "HISTORY-HANDLE", "FINDING-RECORD"], "values": {"acceptedBlockBytes": null, "blocks": [1, 2], "captureFormat": {"capturedLength": 64, "interfaceId": 0, "packetNumber": 1, "sectionId": 1}, "captureId": "HC-01", "fieldLayout": {"encodingRule": "ASCII-2", "fieldId": "FIELD-PROTOCOL-VERSION", "ordinal": 2, "protocolFile": "LCI", "sourceRequirementId": "CRS-M1-00283", "widthBits": 16}, "gaps": [], "ipFragments": {"coverageRanges": [[0, 15]], "datagramLengthBytes": 16, "fragmentOffsets": [0, 8], "fragments": [{"bytesHex": "0001020304050607", "offset": 0}, {"bytesHex": "08090a0b0c0d0e0f", "offset": 8}], "gapPolicy": "GAPPED", "overlapConflict": false, "overlapPolicy": "IDENTICAL-ONLY"}, "labelBoundary": {"annotation": "exploratory", "independentTruth": "not-claimed", "wireOutcome": "observed"}, "noResponseFixture": {"cancelled": false, "deadline": 5, "earliestElapsed": 6, "expectedDisposition": "FAIL-NO-RESPONSE", "requestId": "REQUEST-A", "upperClosed": true}, "optionState": "DEFAULTED", "ownershipFixture": {"expectedOwner": "REQUEST-B", "key": "k1", "ownershipEvents": [{"id": "REQUEST-A", "key": "k1", "kind": "REQUEST", "sequence": 1}, {"id": "REQUEST-B", "key": "k1", "kind": "REQUEST", "sequence": 2}, {"id": "RESPONSE-B", "key": "k1", "kind": "RESPONSE", "sequence": 3}], "policy": "MOST-RECENT", "responseId": "RESPONSE-B"}, "packetRefs": [1, 2, 3], "terminal": {"block": 2, "nextZeroBlock": null, "nextZeroPayloadBytes": null, "payloadBytes": 0}, "tid": {"client": 12000, "server": 69}}}`
- Expected fixture: `{"outcome": "CONTRACT-EXPECTED", "statement": "A provenance-preserving transfer candidate and typed event retain gaps, retransmissions and option evidence.", "values": {"datagramStatus": "COMPLETE", "orderedBlocks": [1, 2], "status": "COMPLETE", "terminalConfirmed": true}}`
- Expected: A provenance-preserving transfer candidate and typed event retain gaps, retransmissions and option evidence.
- Prohibited: No protocol PASS/FAIL, root-cause label or invented accepted option is emitted.; paths: `protocolVerdictWithoutMeasurement`, `independentTruthFromExploratoryInput`
- Negative variants: `[{"expectedRejection": "RC-TRANSFER-TERMINAL at inputFixture.values.terminal", "id": "AC-SYN-TRANSFER-NEG", "mutation": "remove terminal evidence", "operation": "remove", "path": ["inputFixture", "values", "terminal"]}]`
- Basis: Synthetic specification witness for the declared offline first slice; it is not historical truth or a parser execution.; witness: `SPECIFICATION-WITNESS`; runtime: `NOT-EXECUTED`
### `AC-SYN-PREDICTION` — Finite prediction boundary witness
- Inputs: `HISTORY-HANDLE`, `OBSERVATION-ASSESSMENT`
- Tools: `TR-HISTORY-COMPATIBILITY`; modules: `MOD-OBSERVATION`; algorithm interfaces: `IF-PRED-OBS`; experiment interfaces: None
- Input fixture: `{"caseId": "AC-SYN-PREDICTION", "recordIds": ["HISTORY-HANDLE", "OBSERVATION-ASSESSMENT"], "values": {"H": ["h0", "h1"], "actionId": "test-a", "eligibleActions": ["test-a"], "frontiers": [{"hypothesisId": "h0", "state": "q0"}, {"hypothesisId": "h1", "state": "q1"}], "model": {"transitions": [{"actionId": "test-a", "observationClass": "response-a", "source": "q0", "target": "q0"}, {"actionId": "test-a", "observationClass": "response-b", "source": "q1", "target": "q1"}]}, "resource": {"mode": "ROUNDS", "remaining": 1}}}`
- Expected fixture: `{"outcome": "CONTRACT-EXPECTED", "statement": "A finite current projection is tagged OK or GAP before any TEST score is read.", "values": {"classes": ["response-a", "response-b"], "predictionStatus": "OK"}}`
- Expected: A finite current projection is tagged OK or GAP before any TEST score is read.
- Prohibited: An empty projection is not scored as zero and no history is written.; paths: `protocolVerdictWithoutMeasurement`, `independentTruthFromExploratoryInput`
- Negative variants: `[{"expectedRejection": "RC-PREDICTION-NONEMPTY at expectedOutputFixture.values.classes", "id": "AC-SYN-PREDICTION-NEG", "mutation": "replace classes with an empty list while status is OK", "operation": "replace", "path": ["expectedOutputFixture", "values", "classes"], "value": []}]`
- Basis: Synthetic specification witness for finite current-class propagation.; witness: `SPECIFICATION-WITNESS`; runtime: `NOT-EXECUTED`
### `AC-SYN-SELECT` — Admitted action selection witness
- Inputs: `HISTORY-HANDLE`, `OBSERVATION-ASSESSMENT`
- Tools: `TR-HISTORY-COMPATIBILITY`; modules: `MOD-OBSERVATION`; algorithm interfaces: `IF-SELECT-ADMIT`; experiment interfaces: None
- Input fixture: `{"caseId": "AC-SYN-SELECT", "recordIds": ["HISTORY-HANDLE", "OBSERVATION-ASSESSMENT"], "values": {"H": ["h0", "h1"], "actions": [{"classesByHypothesis": {"h0": "response-a", "h1": "response-b"}, "cost": 1, "id": "test-b", "kind": "TEST", "worstClass": 1}, {"classesByHypothesis": {"h0": "response-a", "h1": "response-b"}, "cost": 1, "id": "test-a", "kind": "TEST", "worstClass": 1}], "distinguishingClasses": ["response-a", "response-b"], "eligibleActions": ["test-a", "test-b"], "resource": {"mode": "ROUNDS", "remaining": 1}}}`
- Expected fixture: `{"outcome": "CONTRACT-EXPECTED", "statement": "Only affordable distinguishing TEST actions are minimax-scored, then tie-broken by cost and stable action ID.", "values": {"selectedActionId": "test-a", "tieBreak": ["worstClass", "cost", "stable-id"]}}`
- Expected: Only affordable distinguishing TEST actions are minimax-scored, then tie-broken by cost and stable action ID.
- Prohibited: An uninformative TEST is not A2 and Prep/Recover are not TEST-scored.; paths: `protocolVerdictWithoutMeasurement`, `independentTruthFromExploratoryInput`
- Negative variants: `[{"expectedRejection": "RC-SELECT-STABLE-ID at expectedOutputFixture.values.selectedActionId", "id": "AC-SYN-SELECT-NEG", "mutation": "select test-b with equal score and cost", "operation": "replace", "path": ["expectedOutputFixture", "values", "selectedActionId"], "value": "test-b"}]`
- Basis: Synthetic specification witness for the declared one-step decision table.; witness: `SPECIFICATION-WITNESS`; runtime: `NOT-EXECUTED`
### `AC-SYN-OBSERVATION` — Four-valued timing interpretation witness
- Inputs: `OWNERSHIP-RESULT`, `PROTOCOL-EVENT`, `OBSERVATION-ASSESSMENT`
- Tools: `TR-OBSERVATION-ASSESSMENT`; modules: `MOD-OBSERVATION`; algorithm interfaces: `IF-OBS-INTERPRET`; experiment interfaces: None
- Input fixture: `{"caseId": "AC-SYN-OBSERVATION", "recordIds": ["OWNERSHIP-RESULT", "PROTOCOL-EVENT", "OBSERVATION-ASSESSMENT"], "values": {"clockValid": true, "interval": {"lower": 5.0, "lowerClosed": true, "upper": 5.2, "upperClosed": true}, "matrixTimingFixture": {"clockValid": true, "expectedVerdict": "INCONCLUSIVE", "interval": {"lower": 5.0, "lowerClosed": true, "upper": 5.2, "upperClosed": true}, "requirementWindow": {"lower": 4.0, "lowerClosed": true, "upper": 5.1, "upperClosed": true}}, "requirementWindow": {"lower": 4.0, "lowerClosed": true, "upper": 5.1, "upperClosed": true}}}`
- Expected fixture: `{"outcome": "CONTRACT-EXPECTED", "statement": "Valid intervals produce PASS, FAIL or INCONCLUSIVE; invalid timing evidence produces ERROR.", "values": {"verdict": "INCONCLUSIVE"}}`
- Expected: Valid intervals produce PASS, FAIL or INCONCLUSIVE; invalid timing evidence produces ERROR.
- Prohibited: ERROR or INCONCLUSIVE is not downgraded to FAIL.; paths: `protocolVerdictWithoutMeasurement`, `independentTruthFromExploratoryInput`
- Negative variants: `[{"expectedRejection": "RC-VERDICT-WHOLE-INTERVAL at expectedOutputFixture.values.verdict", "id": "AC-SYN-OBSERVATION-NEG", "mutation": "change verdict to PASS for a boundary-overlapping interval", "operation": "replace", "path": ["expectedOutputFixture", "values", "verdict"], "value": "PASS"}]`
- Basis: Synthetic specification witness for T5 interval and ownership preconditions.; witness: `SPECIFICATION-WITNESS`; runtime: `NOT-EXECUTED`
### `AC-SYN-PREP-RECOVER` — Confirmed recovery handoff witness
- Inputs: `HISTORY-HANDLE`, `OBSERVATION-ASSESSMENT`
- Tools: `TR-HISTORY-COMPATIBILITY`; modules: `MOD-OBSERVATION`; algorithm interfaces: `IF-PREP-RECOVER`; experiment interfaces: None
- Input fixture: `{"caseId": "AC-SYN-PREP-RECOVER", "recordIds": ["HISTORY-HANDLE", "OBSERVATION-ASSESSMENT"], "values": {"actionKind": "PREP", "postSummary": "q1", "summaryConfirmed": true, "targetConfirmed": true}}`
- Expected fixture: `{"outcome": "CONTRACT-EXPECTED", "statement": "Prep/Recover returns confirmation fields; only S8/S9 may commit known state or successor summary.", "values": {"commitSummary": "q1", "historyVersion": 1}}`
- Expected: Prep/Recover returns confirmation fields; only S8/S9 may commit known state or successor summary.
- Prohibited: An unconfirmed successor cannot retain stale known state or become a direct Γ write.; paths: `protocolVerdictWithoutMeasurement`, `independentTruthFromExploratoryInput`
- Negative variants: `[{"expectedRejection": "RC-SUMMARY-CONFIRMATION at inputFixture.values.summaryConfirmed", "id": "AC-SYN-PREP-RECOVER-NEG", "mutation": "set summaryConfirmed false while committing q1", "operation": "replace", "path": ["inputFixture", "values", "summaryConfirmed"], "value": false}]`
- Basis: Synthetic specification witness for S8/S9 ownership boundaries.; witness: `SPECIFICATION-WITNESS`; runtime: `NOT-EXECUTED`
### `AC-SYN-HISTORY` — Whole-history update witness
- Inputs: `HISTORY-HANDLE`, `OBSERVATION-ASSESSMENT`
- Tools: `TR-HISTORY-COMPATIBILITY`; modules: `MOD-OBSERVATION`; algorithm interfaces: `IF-HIST-UPDATE`; experiment interfaces: None
- Input fixture: `{"caseId": "AC-SYN-HISTORY", "recordIds": ["HISTORY-HANDLE", "OBSERVATION-ASSESSMENT"], "values": {"compatibleObservationHypotheses": [], "history": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-syn-0"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 0}, "summaryConfirmed": true}}`
- Expected fixture: `{"outcome": "CONTRACT-EXPECTED", "statement": "A normalized valid outcome advances a versioned whole-history frontier without resurrecting excluded hypotheses.", "values": {"history": {"H": [], "compatibleStateByHypothesis": {}, "statusByHypothesis": {}, "version": 1}, "stop": "Stop-Empty"}}`
- Expected: A normalized valid outcome advances a versioned whole-history frontier without resurrecting excluded hypotheses.
- Prohibited: H prime is never replaced by Iz and resource exhaustion is not incompatibility.; paths: `protocolVerdictWithoutMeasurement`, `independentTruthFromExploratoryInput`
- Negative variants: `[{"expectedRejection": "RC-HISTORY-NO-RESURRECTION at expectedOutputFixture.values.history.H", "id": "AC-SYN-HISTORY-NEG", "mutation": "return the old h0 after the empty intersection", "operation": "replace", "path": ["expectedOutputFixture", "values", "history", "H"], "value": ["h0"]}]`
- Basis: Synthetic specification witness for conservative history propagation.; witness: `SPECIFICATION-WITNESS`; runtime: `NOT-EXECUTED`
### `AC-SYN-EQUIVALENCE` — Bounded equivalence abstention witness
- Inputs: `HISTORY-HANDLE`
- Tools: `TR-HISTORY-COMPATIBILITY`; modules: `MOD-OBSERVATION`; algorithm interfaces: `IF-EQUIV`; experiment interfaces: None
- Input fixture: `{"caseId": "AC-SYN-EQUIVALENCE", "recordIds": ["HISTORY-HANDLE"], "values": {"H": ["h0", "h1"], "finiteDomainProof": "absent"}}`
- Expected fixture: `{"outcome": "CONTRACT-EXPECTED", "statement": "An established result requires declared finite-domain proof evidence; otherwise the result is unknown or notEstablished.", "values": {"result": "unknown"}}`
- Expected: An established result requires declared finite-domain proof evidence; otherwise the result is unknown or notEstablished.
- Prohibited: No immediately distinguishing TEST is not treated as proof of equivalence.; paths: `protocolVerdictWithoutMeasurement`, `independentTruthFromExploratoryInput`
- Negative variants: `[{"expectedRejection": "RC-EQUIV-EVIDENCE at expectedOutputFixture.values.result", "id": "AC-SYN-EQUIVALENCE-NEG", "mutation": "return established without finite-domain proof", "operation": "replace", "path": ["expectedOutputFixture", "values", "result"], "value": "established"}]`
- Basis: Synthetic specification witness for bounded equivalence semantics.; witness: `SPECIFICATION-WITNESS`; runtime: `NOT-EXECUTED`
### `AC-SYN-RESOURCE-STOP` — Resource and stop ordering witness
- Inputs: `HISTORY-HANDLE`, `FINDING-RECORD`
- Tools: `TR-HISTORY-COMPATIBILITY`, `TR-TRACEABLE-FINDING`; modules: `MOD-OBSERVATION`; algorithm interfaces: `IF-RESOURCE-STOP`; experiment interfaces: None
- Input fixture: `{"caseId": "AC-SYN-RESOURCE-STOP", "recordIds": ["HISTORY-HANDLE", "FINDING-RECORD"], "values": {"attemptsIssued": 1, "consecutiveErrorCount": 1, "lastOutcome": "ADAPTER-ERROR", "mode": "ROUNDS", "remaining": 0, "retryCap": 1}}`
- Expected fixture: `{"outcome": "CONTRACT-EXPECTED", "statement": "Exclusive stop ordering retains named 645 residuals and reports retry exhaustion as Stop-Error.", "values": {"charges": 1, "stop": "Stop-Error"}}`
- Expected: Exclusive stop ordering retains named 645 residuals and reports retry exhaustion as Stop-Error.
- Prohibited: Retry exhaustion is not Stop-Budget and a normal singleton is not protocol PASS.; paths: `protocolVerdictWithoutMeasurement`, `independentTruthFromExploratoryInput`
- Negative variants: `[{"expectedRejection": "RC-RESOURCE-ONCE at expectedOutputFixture.values.charges", "id": "AC-SYN-RESOURCE-STOP-NEG", "mutation": "charge the single issued attempt twice", "operation": "replace", "path": ["expectedOutputFixture", "values", "charges"], "value": 2}]`
- Basis: Synthetic specification witness for resource and stop contracts.; witness: `SPECIFICATION-WITNESS`; runtime: `NOT-EXECUTED`
### `AC-SYN-INTEGRITY` — Bounded integrity specification witness
- Inputs: `TRANSFER-RECORD`
- Tools: `TR-PROTOCOL-EVENT`; modules: `MOD-TRANSFER`; algorithm interfaces: `IF-OBS-INTERPRET`; experiment interfaces: None
- Input fixture: `{"caseId": "AC-SYN-INTEGRITY", "recordIds": ["TRANSFER-RECORD"], "values": {"requirementId": "CRS-M1-00076", "runtimeEvidence": "NOT-ESTABLISHED"}}`
- Expected fixture: `{"outcome": "CONTRACT-EXPECTED", "statement": "CRC-bearing inputs retain source parameters and yield NOT-EVALUATED until implementation, configuration and execution evidence exist.", "values": {"judgment": "NOT-EVALUATED"}}`
- Expected: CRC-bearing inputs retain source parameters and yield NOT-EVALUATED until implementation, configuration and execution evidence exist.
- Prohibited: No CRC PASS/FAIL or capability establishment is inferred from source binding.; paths: `runtimeResultClaim`, `truthLeakage`
- Negative variants: `[{"expectedRejection": "RC-INTEGRITY-RUNTIME at expectedOutputFixture.values.judgment", "id": "AC-SYN-INTEGRITY-NEG", "mutation": "return PASS without qualified runtime evidence", "operation": "replace", "path": ["expectedOutputFixture", "values", "judgment"], "value": "PASS"}]`
- Basis: Controlled specification witness; no parser, solver, IUT or experiment was executed.; witness: `SPECIFICATION-WITNESS`; runtime: `NOT-EXECUTED`
### `AC-EXP-SCENE` — Runnable scene identity witness
- Inputs: `INTAKE-METADATA`
- Tools: `TR-CAPTURE-INTAKE`; modules: `MOD-CAPTURE`; algorithm interfaces: `IF-EXECUTE-RECORD`; experiment interfaces: `IF-EXP-SCENE`, `IF-EXP-RUN`
- Input fixture: `{"caseId": "AC-EXP-SCENE", "recordIds": ["INTAKE-METADATA"], "values": {"algorithmVisibleFields": ["rawRecord"], "armId": "CL-T", "configurationId": "cfg-001", "faultPlan": "NONE", "iutId": "iut-001", "resetId": "reset-001", "resourceMode": "ROUNDS", "sceneId": "scene-001", "sessionContext": {"sessionId": "session-001", "state": "RESET"}, "truthSource": "evaluator-only"}}`
- Expected fixture: `{"outcome": "CONTRACT-EXPECTED", "statement": "A runnable scene has stable scene, configuration, IUT and resource identities.", "values": {"executionStatus": "NOT-EXECUTED", "registration": "ACCEPTED"}}`
- Expected: A runnable scene has stable scene, configuration, IUT and resource identities.
- Prohibited: A historical capture or missing identity is not promoted to a runnable scene.; paths: `runtimeResultClaim`, `truthLeakage`
- Negative variants: `[{"expectedRejection": "RC-SCENE-RESET-ID at inputFixture.values.resetId", "id": "AC-EXP-SCENE-NEG", "mutation": "remove resetId", "operation": "remove", "path": ["inputFixture", "values", "resetId"]}]`
- Basis: Controlled specification witness; no parser, solver, IUT or experiment was executed.; witness: `SPECIFICATION-WITNESS`; runtime: `NOT-EXECUTED`
### `AC-EXP-TRUTH` — Independent truth boundary witness
- Inputs: `FINDING-RECORD`
- Tools: `TR-TRACEABLE-FINDING`; modules: `MOD-OBSERVATION`; algorithm interfaces: `IF-OBS-INTERPRET`; experiment interfaces: `IF-EXP-INJECT`, `IF-EXP-TRUTH`
- Input fixture: `{"caseId": "AC-EXP-TRUTH", "recordIds": ["FINDING-RECORD"], "values": {"algorithmVisible": false, "generatorId": "truth-gen-001", "injectionConfirmed": true, "injectionId": "inj-001"}}`
- Expected fixture: `{"outcome": "CONTRACT-EXPECTED", "statement": "Only confirmed injection plus an independent generator creates truth, with shared-component risk named.", "values": {"sharedComponentRisk": "DECLARED", "truthStatus": "CONFIRMED"}}`
- Expected: Only confirmed injection plus an independent generator creates truth, with shared-component risk named.
- Prohibited: Planned or unconfirmed injection and field labels are not truth.; paths: `runtimeResultClaim`, `truthLeakage`
- Negative variants: `[{"expectedRejection": "RC-TRUTH-ISOLATION at inputFixture.values.algorithmVisible", "id": "AC-EXP-TRUTH-NEG", "mutation": "set algorithmVisible true", "operation": "replace", "path": ["inputFixture", "values", "algorithmVisible"], "value": true}]`
- Basis: Controlled specification witness; no parser, solver, IUT or experiment was executed.; witness: `SPECIFICATION-WITNESS`; runtime: `NOT-EXECUTED`
### `AC-EXP-CAUSAL` — Causal collection and arm fairness witness
- Inputs: `OBSERVATION-ASSESSMENT`
- Tools: `TR-OBSERVATION-ASSESSMENT`; modules: `MOD-OBSERVATION`; algorithm interfaces: `IF-EXECUTE-RECORD`; experiment interfaces: `IF-EXP-COLLECT`, `IF-EXP-FILTER`
- Input fixture: `{"caseId": "AC-EXP-CAUSAL", "recordIds": ["OBSERVATION-ASSESSMENT"], "values": {"arm": "CL-TA", "costVector": {"actions": 1, "bytes": 64}, "visiblePrefix": ["trigger", "response"]}}`
- Expected fixture: `{"outcome": "CONTRACT-EXPECTED", "statement": "Each arm sees only its causal prefix and pays the same declared cost vector.", "values": {"causalVisibility": "PREFIX-ONLY", "costComparable": true}}`
- Expected: Each arm sees only its causal prefix and pays the same declared cost vector.
- Prohibited: Future events, evaluator labels and gifted CL-LOOP records are prohibited.; paths: `runtimeResultClaim`, `truthLeakage`
- Negative variants: `[{"expectedRejection": "RC-CAUSAL-PREFIX at inputFixture.values.visiblePrefix", "id": "AC-EXP-CAUSAL-NEG", "mutation": "add evaluator truth to visiblePrefix", "operation": "replace", "path": ["inputFixture", "values", "visiblePrefix"], "value": ["trigger", "evaluator truth"]}]`
- Basis: Controlled specification witness; no parser, solver, IUT or experiment was executed.; witness: `SPECIFICATION-WITNESS`; runtime: `NOT-EXECUTED`
### `AC-EXP-DENOMINATOR` — Evaluation denominator witness
- Inputs: `FINDING-RECORD`
- Tools: `TR-TRACEABLE-FINDING`; modules: `MOD-OBSERVATION`; algorithm interfaces: `IF-RESOURCE-STOP`; experiment interfaces: `IF-EXP-EVAL`
- Input fixture: `{"caseId": "AC-EXP-DENOMINATOR", "recordIds": ["FINDING-RECORD"], "values": {"attempts": ["PASS", "INCONCLUSIVE", "ERROR", "UNCONFIRMED"]}}`
- Expected fixture: `{"outcome": "CONTRACT-EXPECTED", "statement": "Attempt and answered-subset denominators retain abstain, invalid, equivalent and unconfirmed membership.", "values": {"answeredDenominator": 1, "attemptDenominator": 4}}`
- Expected: Attempt and answered-subset denominators retain abstain, invalid, equivalent and unconfirmed membership.
- Prohibited: Excluded or unanswered cases are not silently removed from denominators.; paths: `runtimeResultClaim`, `truthLeakage`
- Negative variants: `[{"expectedRejection": "RC-DENOMINATOR-ATTEMPTS at expectedOutputFixture.values.attemptDenominator", "id": "AC-EXP-DENOMINATOR-NEG", "mutation": "drop abstentions from the attempt denominator", "operation": "replace", "path": ["expectedOutputFixture", "values", "attemptDenominator"], "value": 1}]`
- Basis: Controlled specification witness; no parser, solver, IUT or experiment was executed.; witness: `SPECIFICATION-WITNESS`; runtime: `NOT-EXECUTED`

## Cross-path acceptance matrix

| ID | Category | Positive input | Expected output | Negative mutation | Expected rejection |
|---|---|---|---|---|---|
| `AM-IDENTITY` | corpus identity | controlled manifest entry with unique externally inventoried file identity | identity accepted for exploratory intake | add/remove/hash/length/path/link/duplicate identity | `MANIFEST-ERROR`; cases `AC-SYN-TRANSFER`; test `case relation`; vector `{"byteCount": 214877828, "captureId": "HC-01", "relativePath": "OHMS数据加载CPM_L1_ACT40-FCPA-38AH,报fail,260820.pcapng", "resolvedFileIdentity": "externally-inventoried-regular-file", "sha256": "0e9c160dc28f59502730e7bd860a69d095ed32671d761843bbadb18199cf103c"}` |
| `AM-LABEL` | label boundary | wire record separated from operator annotation and evaluator truth | only protocol-visible fields reach algorithm input | copy filename outcome or evaluator label into algorithm-visible record | `LABEL-LEAKAGE`; cases `AC-SYN-TRANSFER`; test `case relation`; vector `{"annotation": "exploratory", "independentTruth": "not-claimed", "wireOutcome": "observed"}` |
| `AM-FORMAT` | capture format | bounded section/interface/ticks/caplen record | typed packet record preserving section and interface identity | truncate block, unknown link type, missing interface or mix section-local interface zero | `DECODE-ERROR`; cases `AC-SYN-TRANSFER`; test `case relation`; vector `{"capturedLength": 64, "interfaceId": 0, "packetNumber": 1, "sectionId": 1}` |
| `AM-IP` | IP reassembly | complete finite fragment set with PacketRef provenance | complete datagram or GAPPED/CONFLICT record | missing, reordered, overlapping or epoch-reused fragments treated as complete UDP | `REASSEMBLY-ERROR`; cases `AC-SYN-TRANSFER`; test `case relation`; vector `{"coverageRanges": [[0, 15]], "datagramLengthBytes": 16, "fragmentOffsets": [0, 8], "fragments": [{"bytesHex": "0001020304050607", "offset": 0}, {"bytesHex": "08090a0b0c0d0e0f", "offset": 8}], "gapPolicy": "GAPPED", "overlapConflict": false, "overlapPolicy": "IDENTICAL-ONLY"}` |
| `AM-TFTP` | TFTP reconstruction | dynamic TID and accepted/default option evidence with combined end condition | transfer record preserving repeats, wrap limit and terminal evidence | blind deduplication, fixed TID, invented option or wrong final block | `TRANSFER-ERROR`; cases `AC-SYN-TRANSFER`; test `case relation`; vector `{"blockNumbers": [1, 2], "optionState": "DEFAULTED", "terminalBlock": 2, "tidPair": [12000, 69]}` |
| `AM-FIELDS` | field contracts | typed conditional fields with declared counts and legal extension | record accepted with extension/provenance retained | ASCII/integer swap, count mismatch, sentinel misuse or unknown enum | `FIELD-ERROR`; cases `AC-SYN-TRANSFER`; test `case relation`; vector `{"encodingRule": "ASCII-2", "fieldId": "FIELD-PROTOCOL-VERSION", "ordinal": 2, "protocolFile": "LCI", "sourceRequirementId": "CRS-M1-00283", "widthBits": 16}` |
| `AM-OWNERSHIP` | matching and no response | active request instances with event order, cancellation and supersession | one owned response or explicit ambiguity/incomplete horizon | reuse response, wrong key, ignore cancellation or treat capture end as timeout | `OWNERSHIP-ERROR`; cases `AC-SYN-OBSERVATION, AC-SYN-TRANSFER`; test `case relation`; vector `{"deadline": 5, "earliestElapsed": 6, "expectedOwner": "REQUEST-B", "key": "k1", "policy": "MOST-RECENT", "responseId": "RESPONSE-B"}` |
| `AM-TIMING` | timing and U | interval, topology, clock chain, epsilon and immutable U identity | PASS/FAIL/INCONCLUSIVE/ERROR per T5 and no-response boundary | point-estimate rewrite, epsilon zero default or changed U commit | `TIMING-ERROR`; cases `AC-SYN-OBSERVATION`; test `case relation`; vector `{"boundaryClosure": "UPPER-CLOSED", "clockValidity": true, "measurementInterval": {"lower": 5.0, "lowerClosed": true, "upper": 5.2, "upperClosed": true}, "requirementWindow": {"lower": 4.0, "lowerClosed": true, "upper": 5.1, "upperClosed": true}}` |
| `AM-ADMIT` | prediction and admission | finite current classes plus eligible/affordable actions | TEST minimax cost/id tie or Prep/Recover/A2-A5 decision | score GAP as zero, classify uninformative TEST as A2 or score Prep | `SPEC-ERROR`; cases `AC-SYN-SELECT`; test `case relation`; vector `{"H": ["h0", "h1"], "distinguishingClasses": ["response-a", "response-b"], "eligibleActions": ["test-a", "test-b"], "resource": {"mode": "ROUNDS", "remaining": 1}}` |
| `AM-HISTORY` | history update | versioned whole-history frontier and normalized valid outcome | H prime equals H intersect Iz without resurrection | replace H by Iz, drop history correlation or treat frontier limit as incompatibility | `HISTORY-ERROR`; cases `AC-SYN-HISTORY`; test `case relation`; vector `{"H": ["h0"], "compatibleObservationHypotheses": [], "historyVersion": 0, "summaryConfirmed": true}` |
| `AM-STATE` | state and return | total Outcome/Resolution with S8/S9 confirmation fields | retry/commit/stop preserves adopted contexts and writer ownership | stale summary commit, missing confirmation or undefined returned context | `STATE-ERROR`; cases `AC-SYN-HISTORY`; test `case relation`; vector `{"interfaceId": "IF-RESOURCE-STOP", "internalResult": "EMPTY-HISTORY", "returnRecord": "StopResult", "sideEffects": "PRESERVE"}` |
| `AM-RESOURCE` | resource accounting | exclusive BUDGET/ROUNDS and positive finite costs/caps | one charge per issued attempt and named exhaustion | charge refused action twice or accept NaN/negative/noninteger | `RESOURCE-ERROR`; cases `AC-SYN-RESOURCE-STOP`; test `case relation`; vector `{"attemptsIssued": 1, "remaining": 0, "resourceMode": "ROUNDS", "retryCount": 1}` |
| `AM-EXPERIMENT` | experiment boundary | registered scene, confirmed injection and evaluator-only independent truth | causal four-arm record with explicit validity denominators | truth leakage, unconfirmed truth, hidden cost or exploratory capture as held-out | `EXPERIMENT-ERROR`; cases `AC-EXP-SCENE`; test `case relation`; vector `{"algorithmVisibleFields": ["rawRecord"], "armId": "CL-T", "resetId": "reset-001", "truthSource": "evaluator-only"}` |
| `AM-DRIFT` | controlled drift | authority plus generated view at same validated snapshot | checker and generator agree or fail without publishing | delete relation, forge reference, refresh count/hash or retain stale view | `CONTROL-ERROR`; cases ``; test `test_review_generator_refuses_invalid_authority_and_detects_stale_view`; vector `{"failurePreservesOldView": true, "publicationMode": "--write", "sourceMutation": "remove protocolInputDispositions[0].rationaleZh", "viewMarker": "preserve this failed-publication marker\n"}` |

The finite acceptance relations replay request-instance states: ACTIVE, DISCHARGED, CANCELLED, SUPERSEDED, or AMBIGUOUS. An ambiguous response is an ERROR premise, not proof of no response; discharge is not cancellation. BUDGET compares cost with remaining amount, while ROUNDS admits a positive remaining execution count before TEST-only scoring. IP coverage/conflict comes from fragment bytes, field width/encoding from the bound CRS fieldConstraint, and TFTP termination from effective block size and any required zero-length successor. Prep/Recover are never TEST-scored.
The owner and no-response consumers use the same event replay: ambiguous old instances leave the matchable set, while a later new request of the same key starts independently. UNKNOWN-EFFECT marks every declared affected HistoryHandle member CONSERVATIVE-UNKNOWN in the interface result and S9 etaPrime; unaffected member states are preserved for the next round. A computation limit alone does not change the session qStatus or charge a retry.

## First-batch experiment scenarios

- `SC-NORMAL-UPLOAD` — normal single upload; service `UPLOAD`; action normal operation; dependencies `EXP-PREQ-IUT, EXP-PREQ-REGISTRATION`; acceptance `AC-EXP-SCENE, AC-EXP-CAUSAL`; vector `{"eventSequence": ["LUI", "LUR", "DATA", "LUS"], "expectedBoundary": "normal completion only after declared terminal status", "sessionId": "s1", "terminalStatus": "COMPLETE"}`; truth confirmed controlled generator; reset reset IUT/session/budget; timing qualified monotonic clock and declared epsilon; resource same declared cost vector and one exclusive resource mode across arms; blocked by interactive IUT, confirmatory registration; `NOT-EXECUTED`
- `SC-WAIT-CONTINUE` — WAIT then continue; service `UPLOAD`; action controlled WAIT followed by continuation; dependencies `EXP-PREQ-IUT, EXP-PREQ-REGISTRATION`; acceptance `AC-EXP-SCENE, AC-EXP-CAUSAL`; vector `{"eventSequence": ["WAIT", "WAIT-END", "CONTINUE"], "expectedBoundary": "WAIT preserves the active obligation until continuation", "obligationId": "o1", "waitActive": true}`; truth confirmed event script; reset reset loader state and session; timing qualified monotonic clock and declared epsilon; resource same declared cost vector and one exclusive resource mode across arms; blocked by interactive IUT, confirmatory registration; `NOT-EXECUTED`
- `SC-NO-RESPONSE` — request without matching response; service `INFORMATION`; action controlled suppression with complete observation horizon; dependencies `EXP-PREQ-IUT, EXP-PREQ-REGISTRATION`; acceptance `AC-EXP-SCENE, AC-EXP-CAUSAL`; vector `{"cancelled": false, "deadline": 5, "earliestElapsed": 6, "eventSequence": ["TRIGGER", "SILENCE-HORIZON"], "expectedBoundary": "no-response only when earliest admissible elapsed horizon exceeds U", "triggerAt": 0, "upperClosed": true}`; truth confirmed suppression controller; reset reset endpoint and capture horizon; timing qualified clock, open/closed deadline recorded; resource same declared cost vector and one exclusive resource mode across arms; blocked by interactive IUT, confirmatory registration; `NOT-EXECUTED`
- `SC-ABORT` — explicit abort; service `UPLOAD`; action confirmed abort event; dependencies `EXP-PREQ-IUT, EXP-PREQ-REGISTRATION`; acceptance `AC-EXP-SCENE, AC-EXP-CAUSAL`; vector `{"cancelled": true, "eventSequence": ["TRIGGER", "ABORT"], "expectedBoundary": "abort cancels the active obligation", "obligationId": "o2"}`; truth independent controller log; reset reset transfer and session; timing qualified event order and clocks; resource same declared cost vector and one exclusive resource mode across arms; blocked by interactive IUT, confirmatory registration; `NOT-EXECUTED`
- `SC-INVALID-OBS` — invalid or missing observation; service `INFORMATION`; action capture/clock evidence deliberately incomplete; dependencies `EXP-PREQ-IUT, EXP-PREQ-REGISTRATION`; acceptance `AC-EXP-SCENE, AC-EXP-CAUSAL`; vector `{"clockValid": false, "eventSequence": ["TRIGGER", "INVALID-TIMESTAMP"], "expectedBoundary": "invalid timestamp chain yields ERROR", "expectedVerdict": "ERROR"}`; truth evaluator construction record; reset fresh capture and session; timing invalid chain remains ERROR; resource same declared cost vector and one exclusive resource mode across arms; blocked by interactive IUT, confirmatory registration; `NOT-EXECUTED`
- `SC-SAME-KEY` — multiple same-key requests; service `INFORMATION`; action controlled overlapping requests; dependencies `EXP-PREQ-IUT, EXP-PREQ-REGISTRATION`; acceptance `AC-EXP-SCENE, AC-EXP-CAUSAL`; vector `{"eventSequence": ["REQUEST-A", "REQUEST-B", "RESPONSE-B"], "expectedBoundary": "ownership policy identifies exactly one response owner", "expectedOwner": "REQUEST-B", "key": "k1", "ownershipEvents": [{"id": "REQUEST-A", "key": "k1", "kind": "REQUEST", "sequence": 1}, {"id": "REQUEST-B", "key": "k1", "kind": "REQUEST", "sequence": 2}, {"id": "RESPONSE-B", "key": "k1", "kind": "RESPONSE", "sequence": 3}], "policy": "MOST-RECENT", "responseId": "RESPONSE-B"}`; truth independent request schedule; reset reset correlation state; timing event order retained even for equal timestamps; resource same declared cost vector and one exclusive resource mode across arms; blocked by interactive IUT, confirmatory registration; `NOT-EXECUTED`
- `SC-SINGLE-BATCH` — single versus batch context; service `UPLOAD`; action paired declared contexts, not historical causal inference; dependencies `EXP-PREQ-IUT, EXP-PREQ-REGISTRATION`; acceptance `AC-EXP-SCENE, AC-EXP-CAUSAL`; vector `{"eventSequence": ["RESET", "SINGLE", "RESET", "BATCH"], "expectedBoundary": "full reset separates the two contexts", "firstContext": "single", "resetId": "reset-001", "secondContext": "batch"}`; truth controlled scene definitions; reset full IUT reset between scenes; timing same qualified clock/configuration; resource same declared cost vector and one exclusive resource mode across arms; blocked by interactive IUT, confirmatory registration; `NOT-EXECUTED`
- `SC-RESOURCE-ERROR` — resource exhaustion and consecutive error; service `INFORMATION`; action configured bound and injected adapter error; dependencies `EXP-PREQ-IUT, EXP-PREQ-REGISTRATION`; acceptance `AC-EXP-SCENE, AC-EXP-CAUSAL`; vector `{"consecutiveErrors": 2, "eventSequence": ["ACTION", "ADAPTER-ERROR", "RETRY", "ADAPTER-ERROR"], "expectedBoundary": "retry exhaustion is Stop-Error, not Stop-Budget", "expectedStop": "Stop-Error", "retryCap": 2}`; truth configuration plus controller record; reset reset resource/retry counters; timing clock evidence retained but not converted to verdict; resource same declared cost vector and one exclusive resource mode across arms; blocked by interactive IUT, confirmatory registration; `NOT-EXECUTED`
- Prerequisite `EXP-PREQ-IUT` — responsibility: Provide an interactive IUT with frozen identity and configuration.; closure: registered IUT/configuration plus operator availability; not established in this PR
- Prerequisite `EXP-PREQ-REGISTRATION` — responsibility: Register confirmatory scene, truth, reset, clock and cost contracts.; closure: independent confirmatory gate record; not established in this PR

## Slices and dependencies

A conservative unknown history effect preserves every input candidate; Stop-Empty requires a proven incompatible effect and cannot be inferred from an emptied output alone. Integrity variants validate service, symbolic object identity, and typed evidence before applicability and value comparison. Unknown option selection or part number is not evidence of NOT-APPLICABLE or VIOLATED. Missing check values, unknown comparison selection/result, or an unobserved FINAL-DATA premise are NOT-EVALUATED, never definitive VIOLATED. Explicit known non-applicability remains distinct; runtime capability remains NOT-ESTABLISHED.
- `SLICE-OFFLINE-UPLOAD-INFORMATION` — offline capture to traceable report — 176 requirement uses
### Dependency `DEP-INTEGRITY-RUNTIME` — ARINC 645 integrity runtime qualification
- Specification/runtime: `CLOSED` / `NOT-ESTABLISHED`; affects specification readiness: `False`
- Requirements: `CRS-M1-00076`, `CRS-M1-00082`, `CRS-M1-00085`, `CRS-M1-00086`, `CRS-M1-00087`, `CRS-M1-00109`; modules: `MOD-TRANSFER`; records: `TRANSFER-RECORD`; acceptance: `AC-SYN-INTEGRITY`
- Sources: `[{"contract": "information receiver: when declared integrity option selected and supported, retain option identity, receiver support and protected bytes; without qualified runtime evidence report NOT-EVALUATED.", "contractId": "INT-INFORMATION-RECEIVER-SUPPORT", "requirementId": "CRS-M1-00076", "sourceUnitId": "SU-ARINC-615A-3-5-4-2-P047-PROSE-SENTENCE-025-3CF28DC21423"}, {"contract": "upload receiver: when declared integrity option selected and supported, retain option identity, receiver support and protected bytes; without qualified runtime evidence report NOT-EVALUATED.", "contractId": "INT-UPLOAD-RECEIVER-SUPPORT", "requirementId": "CRS-M1-00082", "sourceUnitId": "SU-ARINC-615A-3-5-4-3-P048-PROSE-SENTENCE-026-F38D018C4499"}, {"contract": "final load image and LSP: when all load bytes and declared check-value fields are present, retain algorithm identity, ordered image bytes and LSP check value; without qualified runtime evidence report NOT-EVALUATED.", "contractId": "INT-FINAL-IMAGE-LSP-VALUE", "requirementId": "CRS-M1-00085", "sourceUnitId": "SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-007-F209ABE1376B"}, {"contract": "old and new target files: when optional comparison is selected and both file identities are evidenced, retain old/new file identities, bytes and comparison result; without qualified runtime evidence report NOT-EVALUATED.", "contractId": "INT-OPTIONAL-OLD-NEW-COMPARE", "requirementId": "CRS-M1-00086", "sourceUnitId": "SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-008-CDA43D6568CC"}, {"contract": "two files with the same part number: when two distinct file identities declare the same part number, retain both file identities, their common part number, CRC A, CRC B, and CRC-A-equals-CRC-B relation; without qualified runtime evidence report NOT-EVALUATED.", "contractId": "INT-SAME-PART-NUMBER-CRC-EQUALITY", "requirementId": "CRS-M1-00087", "sourceUnitId": "SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-010-F4624AC8DCB4"}, {"contract": "status-file stream after final DATA: when integrity calculation remains in progress after final DATA, retain final-DATA event, calculation interval and continued status-file events; without qualified runtime evidence report NOT-EVALUATED.", "contractId": "INT-POST-DATA-STATUS-CONTINUATION", "requirementId": "CRS-M1-00109", "sourceUnitId": "SU-ARINC-615A-3-6-3-2-P068-PROSE-SENTENCE-042-4C1D759A6B9A"}]`
- Obligation witnesses: `[{"expected": {"protectedBytesBound": true, "receiverSupportsSelectedOption": true}, "expectedRelation": "receiver supports selected INFORMATION integrity option", "inputs": {"optionIdentity": "integrity-option-information", "optionSelected": true, "protectedBytesRef": "symbolic-information-bytes", "receiverSupport": true, "service": "INFORMATION"}, "requirementId": "CRS-M1-00076"}, {"expected": {"protectedBytesBound": true, "receiverSupportsSelectedOption": true}, "expectedRelation": "receiver supports selected UPLOAD integrity option", "inputs": {"optionIdentity": "integrity-option-upload", "optionSelected": true, "protectedBytesRef": "symbolic-upload-bytes", "receiverSupport": true, "service": "UPLOAD"}, "requirementId": "CRS-M1-00082"}, {"expected": {"checkValueRelation": "EQUALS"}, "expectedRelation": "final-image check value equals the LSP check value", "inputs": {"checkValuePresent": true, "finalImageCheckValue": "0x1234", "finalImageId": "image-A", "lspCheckValue": "0x1234", "lspId": "lsp-A", "orderedBytesPresent": true, "relation": "EQUALS"}, "requirementId": "CRS-M1-00085"}, {"expected": {"comparisonResult": "DIFFERENT", "comparisonSelected": true}, "expectedRelation": "optional old/new comparison retains both identities and its declared result", "inputs": {"comparisonResult": "DIFFERENT", "comparisonSelected": true, "newCheckValue": "0x2222", "newFileId": "new-A", "oldCheckValue": "0x1111", "oldFileId": "old-A"}, "requirementId": "CRS-M1-00086"}, {"expected": {"samePartNumberCheckValueRelation": "EQUALS"}, "expectedRelation": "same part number implies crcA equals crcB", "inputs": {"crcA": "0x1234", "crcB": "0x1234", "fileAId": "file-A", "fileBId": "file-B", "partNumberA": "PN-1", "partNumberB": "PN-1"}, "requirementId": "CRS-M1-00087"}, {"expected": {"statusContinuation": "AT-EACH-OBSERVATION-POINT"}, "expectedRelation": "STATUS continues after FINAL-DATA while calculation is in progress", "inputs": {"calculationEndAt": 12, "calculationInProgress": true, "calculationStartAt": 10, "events": [{"at": 10, "kind": "FINAL-DATA"}, {"at": 11, "kind": "STATUS"}, {"at": 12, "kind": "STATUS"}], "finalDataSeen": true, "observationComplete": true, "requiredStatusObservationPoints": [11, 12]}, "requirementId": "CRS-M1-00109"}]`
- Derived obligation variants (specification only): `[{"branch": "VIOLATED", "changes": {"receiverSupport": false}, "requirementId": "CRS-M1-00076"}, {"branch": "NOT-EVALUATED", "changes": {"receiverSupport": null}, "requirementId": "CRS-M1-00076"}, {"branch": "NOT-APPLICABLE", "changes": {"optionSelected": false}, "requirementId": "CRS-M1-00076"}, {"branch": "VIOLATED", "changes": {"receiverSupport": false}, "requirementId": "CRS-M1-00082"}, {"branch": "NOT-EVALUATED", "changes": {"receiverSupport": null}, "requirementId": "CRS-M1-00082"}, {"branch": "NOT-APPLICABLE", "changes": {"optionSelected": false}, "requirementId": "CRS-M1-00082"}, {"branch": "VIOLATED", "changes": {"lspCheckValue": "0x5678"}, "requirementId": "CRS-M1-00085"}, {"branch": "NOT-EVALUATED", "changes": {"checkValuePresent": false, "finalImageCheckValue": null, "lspCheckValue": null}, "requirementId": "CRS-M1-00085"}, {"branch": "VIOLATED", "changes": {"comparisonResult": "EQUAL", "newCheckValue": "0x2222", "oldCheckValue": "0x1111"}, "requirementId": "CRS-M1-00086"}, {"branch": "NOT-EVALUATED", "changes": {"oldCheckValue": null}, "requirementId": "CRS-M1-00086"}, {"branch": "NOT-APPLICABLE", "changes": {"comparisonSelected": false}, "requirementId": "CRS-M1-00086"}, {"branch": "VIOLATED", "changes": {"crcA": "0x1234", "crcB": "0x5678"}, "requirementId": "CRS-M1-00087"}, {"branch": "NOT-EVALUATED", "changes": {"crcA": null}, "requirementId": "CRS-M1-00087"}, {"branch": "NOT-APPLICABLE", "changes": {"partNumberB": "PN-2"}, "requirementId": "CRS-M1-00087"}, {"branch": "VIOLATED", "changes": {"events": [{"at": 10, "kind": "FINAL-DATA"}, {"at": 11, "kind": "STATUS"}]}, "requirementId": "CRS-M1-00109"}, {"branch": "NOT-EVALUATED", "changes": {"observationComplete": false}, "requirementId": "CRS-M1-00109"}, {"branch": "NOT-APPLICABLE", "changes": {"calculationInProgress": false}, "requirementId": "CRS-M1-00109"}]`
- Contract: Use the bound ARINC 645 parameter leaves, occurrence-order byte stream and exact algorithm identity; emit NOT-EVALUATED unless all runtime qualification evidence is present.
- Affected judgments: CRC-dependent validation and equality judgments remain unavailable at runtime; transport/reconstruction may preserve bytes and provenance only.
- Runtime closure: implementation identity and tests; project-specific algorithm/configuration binding; execution evidence on controlled vectors; independent gate record
- Failure: Missing runtime evidence yields NOT-EVALUATED or named dependency status, never PASS, FAIL, or capability established.; evidence: `configs/engineering/cltav_integrity_obligation_baseline.json`, `configs/requirements/arinc_615a3_m1_crs.json`

## Paper trace

- `PT-ARCH` / III — `toolRequirements`, `moduleContracts`, `recordContracts`, `experimentInterfaceBindings`: Layered requirements and responsibility interfaces; no implementation claim.
- `PT-METHOD` / IV — `algorithmRefinements`, `runtimeParameterContracts`: Bounded reference-kernel specification; no general solver or completeness claim.
- `PT-EXPERIMENT` / V — `experimentInterfaceBindings`, `acceptanceCases`: Historical exploratory and future controlled evidence lines remain separate.
- `PT-RESULTS` / VI — `reviewBoundary`: No confirmatory result is reported.
- `PT-LIMITS` / VII — `implementationDependencies`: Runtime integrity, IUT, clock and independent-truth dependencies remain explicit.

## Slice membership relations

| Slice | Requirement |
|---|---|
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00021` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00025` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00032` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00071` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00072` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00073` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00074` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00075` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00076` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00077` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00078` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00079` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00080` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00081` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00082` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00083` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00084` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00085` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00086` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00087` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00088` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00089` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00090` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00091` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00093` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00094` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00095` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00096` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00097` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00098` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00099` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00100` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00101` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00102` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00103` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00104` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00105` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00106` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00107` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00108` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00109` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00124` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00125` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00126` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00127` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00128` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00129` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00130` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00131` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00132` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00133` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00134` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00135` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00136` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00137` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00138` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00139` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00140` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00141` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00142` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00143` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00144` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00145` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00146` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00147` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00148` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00149` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00150` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00151` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00152` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00153` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00154` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00155` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00156` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00157` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00158` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00159` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00160` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00161` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00162` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00163` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00164` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00165` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00166` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00186` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00282` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00283` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00284` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00285` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00286` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00287` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00288` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00289` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00290` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00291` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00292` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00293` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00294` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00295` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00296` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00297` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00298` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00299` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00300` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00301` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00302` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00303` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00304` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00305` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00306` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00307` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00308` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00309` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00310` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00311` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00312` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00313` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00314` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00315` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00316` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00317` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00318` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00319` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00320` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00321` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00322` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00323` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00324` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00325` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00326` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00327` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00328` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00329` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00330` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00331` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00332` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00333` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00346` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00347` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00348` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00349` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00350` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00351` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00352` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00353` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00354` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00355` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00356` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00357` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00358` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00359` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00360` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00361` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00362` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00363` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00364` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00365` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00366` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00367` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00368` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00369` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00370` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00371` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00372` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00373` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00374` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00375` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00376` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00378` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00618` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00620` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00622` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00632` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00645` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00646` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00647` |

## Disposition summary

| Disposition | Count |
|---|---:|
| `FIRST-SLICE-IMPLEMENTATION` | 176 |
| `LATER-SERVICE` | 137 |
| `NOT-TOOL-OBLIGATION` | 550 |

## All requirement dispositions

| Requirement | Disposition | First slice | Module | Record | Acceptance | Rationale |
|---|---|---|---|---|---|---|
| `CRS-M1-00001` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00002` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00003` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00004` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00005` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00006` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00007` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00008` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00009` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00010` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00011` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00012` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00013` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00014` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00015` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00016` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00017` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00018` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00019` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00020` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00021` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. Dependencies: none |
| `CRS-M1-00022` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00023` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00024` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00025` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. Dependencies: none |
| `CRS-M1-00026` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00027` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00028` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00029` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00030` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00031` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00032` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. Dependencies: none |
| `CRS-M1-00033` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00034` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00035` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00036` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00037` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00038` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00039` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00040` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00041` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00042` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00043` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00044` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00045` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00046` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00047` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00048` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00049` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00050` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00051` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00052` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00053` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00054` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00055` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00056` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00057` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00058` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00059` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00060` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00061` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00062` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00063` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00064` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00065` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00066` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00067` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00068` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00069` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00070` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00071` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00072` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00073` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00074` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00075` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00076` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `TRANSFER-RECORD` | `AC-SYN-INTEGRITY` | The first-slice specification preserves the CRC-bearing protocol obligation and source parameters; runtime validation remains explicitly not established pending implementation, configuration and execution evidence. Dependencies: `DEP-INTEGRITY-RUNTIME` |
| `CRS-M1-00077` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00078` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00079` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00080` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00081` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00082` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `TRANSFER-RECORD` | `AC-SYN-INTEGRITY` | The first-slice specification preserves the CRC-bearing protocol obligation and source parameters; runtime validation remains explicitly not established pending implementation, configuration and execution evidence. Dependencies: `DEP-INTEGRITY-RUNTIME` |
| `CRS-M1-00083` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00084` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00085` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `TRANSFER-RECORD` | `AC-SYN-INTEGRITY` | The first-slice specification preserves the CRC-bearing protocol obligation and source parameters; runtime validation remains explicitly not established pending implementation, configuration and execution evidence. Dependencies: `DEP-INTEGRITY-RUNTIME` |
| `CRS-M1-00086` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `TRANSFER-RECORD` | `AC-SYN-INTEGRITY` | The first-slice specification preserves the CRC-bearing protocol obligation and source parameters; runtime validation remains explicitly not established pending implementation, configuration and execution evidence. Dependencies: `DEP-INTEGRITY-RUNTIME` |
| `CRS-M1-00087` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `TRANSFER-RECORD` | `AC-SYN-INTEGRITY` | The first-slice specification preserves the CRC-bearing protocol obligation and source parameters; runtime validation remains explicitly not established pending implementation, configuration and execution evidence. Dependencies: `DEP-INTEGRITY-RUNTIME` |
| `CRS-M1-00088` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00089` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00090` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00091` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00092` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00093` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00094` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00095` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00096` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00097` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00098` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00099` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00100` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00101` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00102` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00103` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00104` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00105` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00106` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00107` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00108` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00109` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `TRANSFER-RECORD` | `AC-SYN-INTEGRITY` | The first-slice specification preserves the CRC-bearing protocol obligation and source parameters; runtime validation remains explicitly not established pending implementation, configuration and execution evidence. Dependencies: `DEP-INTEGRITY-RUNTIME` |
| `CRS-M1-00110` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00111` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00112` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00113` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00114` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00115` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00116` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00117` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00118` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00119` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00120` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00121` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00122` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00123` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00124` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00125` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00126` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00127` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00128` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00129` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00130` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00131` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00132` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00133` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00134` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00135` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00136` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00137` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00138` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00139` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00140` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00141` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00142` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00143` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00144` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00145` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00146` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00147` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00148` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00149` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00150` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00151` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00152` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00153` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00154` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00155` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00156` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00157` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00158` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00159` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00160` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00161` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00162` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00163` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00164` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00165` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00166` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00167` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00168` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00169` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00170` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00171` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00172` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00173` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00174` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00175` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00176` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00177` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00178` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00179` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00180` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00181` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00182` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00183` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00184` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00185` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00186` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. Dependencies: none |
| `CRS-M1-00187` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00188` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00189` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00190` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00191` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00192` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00193` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00194` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00195` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00196` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00197` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00198` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00199` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00200` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00201` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00202` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00203` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00204` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00205` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00206` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00207` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00208` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00209` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00210` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00211` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00212` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00213` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00214` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00215` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00216` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00217` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00218` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00219` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00220` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00221` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00222` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00223` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00224` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00225` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00226` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00227` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00228` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00229` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00230` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00231` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00232` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00233` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00234` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00235` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00236` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00237` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00238` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00239` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00240` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00241` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00242` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00243` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00244` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00245` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00246` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00247` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00248` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00249` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00250` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00251` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00252` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00253` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00254` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00255` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00256` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00257` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00258` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00259` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00260` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00261` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00262` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00263` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00264` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00265` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00266` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00267` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00268` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00269` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00270` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00271` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00272` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00273` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00274` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00275` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00276` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00277` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00278` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00279` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00280` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00281` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00282` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00283` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00284` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00285` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00286` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00287` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00288` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00289` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00290` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00291` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00292` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00293` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00294` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00295` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00296` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00297` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00298` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00299` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00300` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00301` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00302` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00303` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00304` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00305` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00306` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00307` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00308` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00309` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00310` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00311` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00312` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00313` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00314` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00315` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00316` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00317` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00318` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00319` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00320` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00321` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00322` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00323` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00324` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00325` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00326` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00327` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00328` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00329` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00330` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00331` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00332` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00333` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00334` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00335` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00336` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00337` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00338` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00339` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00340` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00341` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00342` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00343` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00344` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00345` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00346` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00347` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00348` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00349` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00350` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00351` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00352` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00353` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00354` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00355` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00356` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00357` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00358` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00359` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00360` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00361` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00362` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00363` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00364` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00365` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00366` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00367` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00368` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00369` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00370` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00371` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00372` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00373` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00374` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00375` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00376` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00377` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00378` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | Bounded offline UPLOAD/INFORMATION reconstruction, timing, ownership or transfer input. Dependencies: none |
| `CRS-M1-00379` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00380` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00381` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00382` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00383` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00384` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00385` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00386` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00387` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00388` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00389` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00390` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00391` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00392` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00393` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00394` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00395` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00396` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00397` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00398` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00399` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00400` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00401` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00402` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00403` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00404` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00405` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00406` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00407` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00408` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00409` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00410` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00411` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00412` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00413` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00414` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00415` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00416` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00417` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00418` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00419` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00420` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00421` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00422` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00423` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00424` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00426` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00427` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00428` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00429` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00430` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00431` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00432` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00433` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00434` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00435` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00436` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00437` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00438` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00439` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00440` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00441` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00442` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00443` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00444` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00445` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00446` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00447` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00448` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00449` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00450` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00451` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00452` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00453` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00454` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00455` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00456` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00457` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00458` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00459` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00460` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00461` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00462` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00463` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00464` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00465` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00466` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00467` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00468` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00469` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00470` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00471` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00472` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00473` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00474` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00475` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00476` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00477` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00478` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00479` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00480` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00481` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00482` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00483` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00484` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00485` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00486` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00487` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00488` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00489` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00490` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00491` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00492` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00493` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00494` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00495` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00496` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00497` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00498` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00499` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00500` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00501` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00502` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00503` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00504` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00505` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00506` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00507` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00508` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00509` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00510` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00511` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00512` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00513` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00514` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00515` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00516` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00517` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00518` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00519` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00520` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00521` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00522` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00523` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00524` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00525` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00526` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00527` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00528` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00529` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00530` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00531` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00532` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00533` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00534` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00535` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00536` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00537` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00538` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00539` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00540` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00541` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00542` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00543` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00544` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00545` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00546` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00547` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00548` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00549` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00550` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00551` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00552` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00553` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00554` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00555` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00556` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00557` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00558` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00559` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00560` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00561` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00562` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00563` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00564` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00565` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00566` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00567` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00568` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00569` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00570` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00571` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00572` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00573` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00574` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00575` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00576` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00577` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00578` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00579` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00580` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00581` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00582` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00583` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00584` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00585` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00586` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00587` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00588` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00589` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00590` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00591` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00592` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00593` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00594` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00595` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00596` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00597` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00598` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00599` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00600` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00601` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00602` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00603` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00604` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00605` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00606` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00607` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00608` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00609` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00610` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00611` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00612` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00613` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00614` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00615` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00616` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00617` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00618` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. Dependencies: none |
| `CRS-M1-00619` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00620` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice COMMON timing, TFTP transport, or final-block observation contract. Dependencies: none |
| `CRS-M1-00621` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00622` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. Dependencies: none |
| `CRS-M1-00623` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00624` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00625` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00626` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00627` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00628` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00629` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00630` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00631` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00632` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. Dependencies: none |
| `CRS-M1-00633` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00634` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00635` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00636` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00637` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00638` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00639` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00640` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00641` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00642` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00643` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00644` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00645` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. Dependencies: none |
| `CRS-M1-00646` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. Dependencies: none |
| `CRS-M1-00647` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | First-slice TFTP transport identity, option confirmation, request layout, or termination reconstruction. Dependencies: none |
| `CRS-M1-00648` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00649` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00650` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00651` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00652` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00653` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00654` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00655` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00656` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00657` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00658` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00659` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00660` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00661` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00662` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00663` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00664` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00665` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00666` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00667` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00668` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00669` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00670` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00671` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00672` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00673` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00674` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00675` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00676` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00677` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00678` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00679` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00680` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00681` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00682` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00683` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00684` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00685` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00686` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00687` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00688` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00689` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00690` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00691` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00692` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00693` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00694` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00695` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00696` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00697` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00698` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00699` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00700` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00701` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00702` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00703` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00704` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00705` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00706` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00707` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00708` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00709` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00710` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00711` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00712` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00713` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00714` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00715` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00716` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00717` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00718` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00719` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00720` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00721` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00722` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00723` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00724` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00725` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00726` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00727` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00728` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00729` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00730` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00731` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00732` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00733` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00734` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00735` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00736` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00737` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00738` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00739` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00740` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00741` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00742` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00743` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00744` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00745` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00746` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00747` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00748` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00749` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00750` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00751` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00752` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00753` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00754` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00755` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00756` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00757` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00758` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00759` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00760` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00761` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00762` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00763` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00764` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00765` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00766` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00767` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00768` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00769` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00770` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00771` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00772` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00773` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00774` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00775` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00776` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00777` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00778` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00779` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00780` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00781` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00782` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00783` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00784` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00785` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00786` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00787` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00788` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00789` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00790` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00791` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00792` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00793` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00794` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00795` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00796` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00797` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00798` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00799` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00800` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00801` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00802` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00803` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00804` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00805` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00806` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00807` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00808` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00809` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00810` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00811` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00812` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00813` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00814` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00815` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00816` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00817` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00818` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00819` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00820` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00821` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00822` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00823` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00824` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00825` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00826` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00827` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00828` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00829` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00830` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00831` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00832` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00833` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00834` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00835` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00836` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00837` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00838` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00839` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00840` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00841` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00842` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00843` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00844` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00845` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00846` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00847` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00848` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00849` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00850` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00851` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00852` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00853` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00854` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00855` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00856` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00857` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00858` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00859` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00860` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00861` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00862` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00863` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |
| `CRS-M1-00864` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | Outside the first offline UPLOAD/INFORMATION slice. Dependencies: none |

# 中文版

# CL-TAV 开发就绪评审视图

> 由同一权威 JSON 生成，禁止手工修改。

- 控制：`CR-2026-016`；设计决策：`DD-038`, `DD-039`, `DD-040`
- 绑定 M1 需求：863；处置合计：863；就绪状态：`CANDIDATE`；主张边界：`SPECIFICATION-ONLY`

## 输入身份

- `ARINC615A3-M1-CRS` — `configs/requirements/arinc_615a3_m1_crs.json` — SHA-256 `56e214f089e6563e53e3991e7a8e7892f163840bb2c1d7d39f4a9ce92fc16758` — 受控协议需求全集
- `CLTAV-INTERFACE-REGISTRY` — `configs/research/cltav_interface_registry.json` — SHA-256 `a65679b902cf51d31aa613c133919c3cd2c66dbc6c65eb3cc58d9bf3530d329d` — 已接受的接口词汇表
- `CLTAV-INTEGRITY-OBLIGATION-BASELINE` — `configs/engineering/cltav_integrity_obligation_baseline.json` — SHA-256 `85ec28689371bf557dfad5b9fc5ff80421198a896173ced603dc992e62a2dc57` — 独立的完整性必需义务集合与合同身份
- `CLTAV-HISTORICAL-CAPTURE-MANIFEST` — `configs/research/cltav_historical_capture_manifest.json` — SHA-256 `80cc6076e65d2639bd332406412e8895ca7c43722005f70f73426ef15eb8f747` — 固定矩阵身份见证的探索性捕获身份；不是独立真值。

## 记录合同

| ID | 责任模块 | 字段 | 不确定性 |
|---|---|---|---|
| `CAPTURE-IDENTITY` | `MOD-CAPTURE` | `captureId`, `relativePath`, `sha256`, `byteSize`, `manifestVersion` | 仅作探索用途；未知元数据保持 UNKNOWN。 |
| `PACKET-REF` | `MOD-CAPTURE` | `captureId`, `sectionId`, `interfaceId`, `packetNumber`, `rawTicks`, `resolution`, `caplen`, `origlen`, `decodeStatus` | 时钟精度与分辨率不同。 |
| `DATAGRAM-RECORD` | `MOD-REASSEMBLY` | `fragmentRefs`, `coverage`, `overlapStatus`, `reassemblyStatus` | 缺失或冲突分片保持显式。 |
| `TRANSFER-RECORD` | `MOD-TRANSFER` | `direction`, `endpoints`, `tid`, `request`, `optionState`, `blockMap`, `completionEvidence` | 歧义 TID 或选项状态保持 UNKNOWN。UNKNOWN 不携带生效选项值。DEFAULTED 的 blksize 若出现则必须恰为 512；省略表示尚未建立 blksize，而非隐含默认值。ACCEPTED 携带已确认的协商值。 |
| `PROTOCOL-EVENT` | `MOD-TRANSFER` | `eventLayer`, `role`, `payload`, `correlationKey`, `rawRefs`, `parseBoundary` | 不从线上证据推断应用事实。 |
| `OWNERSHIP-RESULT` | `MOD-OWNERSHIP` | `requestInstance`, `policy`, `status`, `evidenceRefs` | 多个可能所有者保持 AMBIGUOUS。 |
| `OBSERVATION-ASSESSMENT` | `MOD-OBSERVATION` | `measurementInterval`, `domain`, `errorBasis`, `verdict`, `reason` | 时间链无效为 ERROR，边界重叠为 INCONCLUSIVE。 |
| `INTAKE-METADATA` | `MOD-CAPTURE` | `operatorNote`, `topology`, `clockAccuracy`, `configuration`, `rootCause` | 未知值不能作为算法先验。 |
| `FINDING-RECORD` | `MOD-OBSERVATION` | `facts`, `judgmentBasis`, `scope`, `assumptions`, `evidenceRefs` | 发现记录不是根因标签。 |
| `HISTORY-HANDLE` | `MOD-OBSERVATION` | `H`, `compatibleStateByHypothesis`, `statusByHypothesis`, `version` | UNKNOWN-EFFECT 与未确认 Recover 保留 H，并将受影响状态标为 CONSERVATIVE-UNKNOWN；CONFIRMED-NOT-SENT 保留历史；相同 H 集合可以保留不同的相容历史。 |

### `CAPTURE-IDENTITY` — 捕获身份
- 所有权：捕获模块或接入边界拥有该记录。
- 不确定性：仅作探索用途；未知元数据保持 UNKNOWN。
- 来源需求：无
- 错误行为：返回具名错误或保守未知；不得输出 IUT FAIL。
- 字段定义：`{"byteSize": {"constraintId": "RC-CAPTURE-BYTE-SIZE", "minimum": 0, "required": true, "type": "integer"}, "captureId": {"constraintId": "RC-CAPTURE-ID", "pattern": "^(?:cap-[a-z0-9][a-z0-9-]*|HC-[0-9]{2})$", "required": true, "type": "string"}, "manifestVersion": {"constraintId": "RC-CAPTURE-MANIFEST-VERSION", "pattern": "^[1-9][0-9]*\\.[0-9]+$", "required": true, "type": "string"}, "relativePath": {"constraintId": "RC-CAPTURE-PATH", "pattern": "^(?!/)(?![A-Za-z]:)(?!.*(?:^|/)\\.\\.(?:/|$))[^\\x00-\\x1f\\\\]+$", "required": true, "type": "string"}, "sha256": {"constraintId": "RC-CAPTURE-SHA256", "pattern": "^[0-9a-f]{64}$", "required": true, "type": "string"}}`
- 有效示例：`{"byteSize": 128, "captureId": "cap-syn-001", "manifestVersion": "1.0", "relativePath": "synthetic/cap-syn-001.pcapng", "sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"}`
- 无效示例：`{"byteSize": 128, "captureId": "cap-syn-001", "manifestVersion": "1.0", "relativePath": "synthetic/cap-syn-001.pcapng", "sha256": "not-a-hash"}`
- 预期拒绝：`{"constraintId": "RC-CAPTURE-SHA256", "path": ["sha256"]}`
- 拒绝理由：sha256 必须为 64 个小写十六进制字符

### `PACKET-REF` — 数据包引用
- 所有权：捕获模块或接入边界拥有该记录。
- 不确定性：时钟精度与分辨率不同。
- 来源需求：无
- 错误行为：返回具名错误或保守未知；不得输出 IUT FAIL。
- 字段定义：`{"caplen": {"constraintId": "RC-PACKET-CAPLEN", "minimum": 0, "required": true, "type": "integer"}, "captureId": {"constraintId": "RC-PACKET-CAPTURE-ID", "pattern": "^(?:cap-[a-z0-9][a-z0-9-]*|HC-[0-9]{2})$", "required": true, "type": "string"}, "decodeStatus": {"constraintId": "RC-PACKET-DECODE-STATUS", "enum": ["FULL", "TRUNCATED", "UNDECODED"], "required": true, "type": "string"}, "interfaceId": {"constraintId": "RC-PACKET-INTERFACE", "minimum": 0, "required": true, "type": "integer"}, "origlen": {"constraintId": "RC-PACKET-ORIGLEN", "minimum": 0, "required": true, "type": "integer"}, "packetNumber": {"constraintId": "RC-PACKET-NUMBER", "minimum": 1, "required": true, "type": "integer"}, "rawTicks": {"constraintId": "RC-PACKET-TICKS", "minimum": 0, "required": true, "type": "integer"}, "resolution": {"additionalProperties": false, "constraintId": "RC-PACKET-RESOLUTION", "properties": {"ticksPerSecond": {"constraintId": "RC-PACKET-TICKS-PER-SECOND", "minimum": 1, "type": "integer"}}, "required": true, "requiredProperties": ["ticksPerSecond"], "type": "object"}, "sectionId": {"constraintId": "RC-PACKET-SECTION", "minimum": 0, "required": true, "type": "integer"}}`
- 有效示例：`{"caplen": 96, "captureId": "cap-syn-001", "decodeStatus": "FULL", "interfaceId": 0, "origlen": 96, "packetNumber": 1, "rawTicks": 125000, "resolution": {"ticksPerSecond": 1000000}, "sectionId": 0}`
- 无效示例：`{"caplen": 96, "captureId": "cap-syn-001", "decodeStatus": "FULL", "interfaceId": 0, "origlen": 96, "packetNumber": 1, "rawTicks": 125000, "resolution": {"ticksPerSecond": 0}, "sectionId": 0}`
- 预期拒绝：`{"constraintId": "RC-PACKET-TICKS-PER-SECOND", "path": ["resolution", "ticksPerSecond"]}`
- 拒绝理由：resolution 必须包含正数 ticksPerSecond

### `DATAGRAM-RECORD` — 数据报重组
- 所有权：重组模块拥有派生记录，原始包引用不可改写。
- 不确定性：缺失或冲突分片保持显式。
- 来源需求：无
- 错误行为：返回具名错误或保守未知；不得输出 IUT FAIL。
- 字段定义：`{"coverage": {"constraintId": "RC-DATAGRAM-COVERAGE", "items": {"additionalProperties": false, "constraintId": "RC-DATAGRAM-RANGE", "properties": {"endExclusive": {"constraintId": "RC-DATAGRAM-RANGE-END", "minimum": 1, "type": "integer"}, "start": {"constraintId": "RC-DATAGRAM-RANGE-START", "minimum": 0, "type": "integer"}}, "requiredProperties": ["start", "endExclusive"], "type": "object"}, "minItems": 1, "required": true, "type": "array"}, "fragmentRefs": {"constraintId": "RC-DATAGRAM-FRAGMENTS", "items": {"constraintId": "RC-PACKET-REF-ID", "pattern": "^(?:cap-[a-z0-9][a-z0-9-]*|HC-[0-9]{2}):[0-9]+:[0-9]+:[1-9][0-9]*$", "type": "string"}, "minItems": 1, "required": true, "type": "array", "uniqueItems": true}, "overlapStatus": {"constraintId": "RC-DATAGRAM-OVERLAP", "enum": ["NONE", "DUPLICATE", "CONFLICT", "UNKNOWN"], "required": true, "type": "string"}, "reassemblyStatus": {"constraintId": "RC-DATAGRAM-STATUS", "enum": ["COMPLETE", "GAPPED", "CONFLICT", "UNKNOWN"], "required": true, "type": "string"}}`
- 有效示例：`{"coverage": [{"endExclusive": 512, "start": 0}], "fragmentRefs": ["cap-syn-001:0:0:1", "cap-syn-001:0:0:2"], "overlapStatus": "NONE", "reassemblyStatus": "COMPLETE"}`
- 无效示例：`{"coverage": [{"endExclusive": 512, "start": 0}], "fragmentRefs": [], "overlapStatus": "NONE", "reassemblyStatus": "COMPLETE"}`
- 预期拒绝：`{"constraintId": "RC-DATAGRAM-FRAGMENTS", "path": ["fragmentRefs"]}`
- 拒绝理由：fragmentRefs 必须至少包含一个有作用域的数据包引用

### `TRANSFER-RECORD` — 传输候选
- 所有权：传输模块拥有派生的传输或事件记录。
- 不确定性：歧义 TID 或选项状态保持 UNKNOWN。UNKNOWN 不携带生效选项值。DEFAULTED 的 blksize 若出现则必须恰为 512；省略表示尚未建立 blksize，而非隐含默认值。ACCEPTED 携带已确认的协商值。
- 来源需求：`CRS-M1-00646`, `CRS-M1-00647`
- 错误行为：拒绝非 512 的 DEFAULTED blksize 和任何 UNKNOWN 生效值；返回具名错误或保守未知，且不得输出 IUT FAIL。
- 字段定义：`{"blockMap": {"additionalProperties": {"constraintId": "RC-PACKET-REF-ID", "pattern": "^(?:cap-[a-z0-9][a-z0-9-]*|HC-[0-9]{2}):[0-9]+:[0-9]+:[1-9][0-9]*$", "type": "string"}, "constraintId": "RC-TRANSFER-BLOCK-MAP", "required": true, "type": "object"}, "completionEvidence": {"constraintId": "RC-TRANSFER-COMPLETION", "items": {"constraintId": "RC-EVIDENCE-REF", "pattern": "^(cap|pkt|dgram|transfer|event)-[A-Za-z0-9._:-]+$", "type": "string"}, "required": true, "type": "array", "uniqueItems": true}, "direction": {"constraintId": "RC-TRANSFER-DIRECTION", "enum": ["CLIENT-TO-SERVER", "SERVER-TO-CLIENT"], "required": true, "type": "string"}, "endpoints": {"additionalProperties": false, "constraintId": "RC-TRANSFER-ENDPOINTS", "properties": {"client": {"constraintId": "RC-TRANSFER-CLIENT", "minLength": 1, "type": "string"}, "server": {"constraintId": "RC-TRANSFER-SERVER", "minLength": 1, "type": "string"}}, "required": true, "requiredProperties": ["client", "server"], "type": "object"}, "optionState": {"additionalProperties": false, "constraintId": "RC-TRANSFER-OPTION-STATE", "properties": {"mode": {"constraintId": "RC-OPTION-MODE", "enum": ["ACCEPTED", "DEFAULTED", "UNKNOWN"], "type": "string"}, "values": {"additionalProperties": false, "constraintId": "RC-OPTION-VALUES", "properties": {"blksize": {"constraintId": "RC-OPTION-BLKSIZE", "maximum": 65464, "minimum": 8, "type": "integer"}, "timeout": {"constraintId": "RC-OPTION-TIMEOUT", "maximum": 255, "minimum": 1, "type": "integer"}, "tsize": {"constraintId": "RC-OPTION-TSIZE", "minimum": 0, "type": "integer"}}, "type": "object"}}, "required": true, "requiredProperties": ["mode", "values"], "type": "object"}, "request": {"constraintId": "RC-TRANSFER-REQUEST", "pattern": "^event-[A-Za-z0-9._:-]+$", "required": true, "type": "string"}, "tid": {"additionalProperties": false, "constraintId": "RC-TRANSFER-TID", "properties": {"clientPort": {"constraintId": "RC-TID-CLIENT", "maximum": 65535, "minimum": 1, "type": "integer"}, "serverPort": {"constraintId": "RC-TID-SERVER", "maximum": 65535, "minimum": 1, "type": "integer"}}, "required": true, "requiredProperties": ["clientPort", "serverPort"], "type": "object"}}`
- 有效示例：`{"blockMap": {"1": "cap-syn-001:0:0:2"}, "completionEvidence": ["pkt-cap-syn-001:2"], "direction": "SERVER-TO-CLIENT", "endpoints": {"client": "192.0.2.10", "server": "192.0.2.20"}, "optionState": {"mode": "DEFAULTED", "values": {"blksize": 512}}, "request": "event-rrq-001", "tid": {"clientPort": 40000, "serverPort": 69}}`
- 无效示例：`{"blockMap": {}, "completionEvidence": [], "direction": "SIDEWAYS", "endpoints": {"client": "192.0.2.10", "server": "192.0.2.20"}, "optionState": {"mode": "DEFAULTED", "values": {}}, "request": "event-rrq-001", "tid": {"clientPort": 40000, "serverPort": 69}}`
- 预期拒绝：`{"constraintId": "RC-TRANSFER-DIRECTION", "path": ["direction"]}`
- 拒绝理由：direction 必须使用受控的客户端/服务器词汇

### `PROTOCOL-EVENT` — 协议事件
- 所有权：传输模块拥有派生的传输或事件记录。
- 不确定性：不从线上证据推断应用事实。
- 来源需求：无
- 错误行为：返回具名错误或保守未知；不得输出 IUT FAIL。
- 字段定义：`{"correlationKey": {"constraintId": "RC-EVENT-CORRELATION", "pattern": "^corr-[A-Za-z0-9._:-]+$", "required": true, "type": "string"}, "eventLayer": {"constraintId": "RC-EVENT-LAYER", "enum": ["WIRE", "PARSE-RESULT", "APPLICATION", "ENVIRONMENT"], "required": true, "type": "string"}, "parseBoundary": {"constraintId": "RC-EVENT-PARSE-BOUNDARY", "enum": ["COMPLETE", "PARTIAL", "OPAQUE", "ERROR"], "required": true, "type": "string"}, "payload": {"additionalProperties": false, "constraintId": "RC-EVENT-PAYLOAD", "properties": {"ref": {"constraintId": "RC-PAYLOAD-REF", "pattern": "^payload-[A-Za-z0-9._:-]+$", "type": "string"}, "type": {"constraintId": "RC-PAYLOAD-TYPE", "pattern": "^[A-Z][A-Z0-9-]*$", "type": "string"}}, "required": true, "requiredProperties": ["type", "ref"], "type": "object"}, "rawRefs": {"constraintId": "RC-EVENT-RAW-REFS", "items": {"constraintId": "RC-PACKET-REF-ID", "pattern": "^(?:cap-[a-z0-9][a-z0-9-]*|HC-[0-9]{2}):[0-9]+:[0-9]+:[1-9][0-9]*$", "type": "string"}, "minItems": 1, "required": true, "type": "array", "uniqueItems": true}, "role": {"constraintId": "RC-EVENT-ROLE", "enum": ["CLIENT", "SERVER", "UNKNOWN"], "required": true, "type": "string"}}`
- 有效示例：`{"correlationKey": "corr-transfer-001", "eventLayer": "WIRE", "parseBoundary": "COMPLETE", "payload": {"ref": "payload-rrq-001", "type": "RRQ"}, "rawRefs": ["cap-syn-001:0:0:1"], "role": "CLIENT"}`
- 无效示例：`{"correlationKey": "corr-transfer-001", "eventLayer": "WIRE", "parseBoundary": "COMPLETE", "payload": {"ref": "payload-rrq-001", "type": "RRQ"}, "rawRefs": [], "role": "CLIENT"}`
- 预期拒绝：`{"constraintId": "RC-EVENT-RAW-REFS", "path": ["rawRefs"]}`
- 拒绝理由：rawRefs 必须保留至少一个源数据包

### `OWNERSHIP-RESULT` — 所有权结果
- 所有权：所有权模块拥有匹配结果。
- 不确定性：多个可能所有者保持 AMBIGUOUS。
- 来源需求：无
- 错误行为：返回具名错误或保守未知；不得输出 IUT FAIL。
- 字段定义：`{"evidenceRefs": {"constraintId": "RC-OWNERSHIP-EVIDENCE", "items": {"constraintId": "RC-EVIDENCE-REF", "pattern": "^(cap|pkt|dgram|transfer|event)-[A-Za-z0-9._:-]+$", "type": "string"}, "required": true, "type": "array", "uniqueItems": true}, "policy": {"constraintId": "RC-OWNERSHIP-POLICY", "enum": ["UNIQUE-KEY", "FIFO", "MOST-RECENT"], "required": true, "type": "string"}, "requestInstance": {"constraintId": "RC-OWNERSHIP-REQUEST", "pattern": "^event-[A-Za-z0-9._:-]+$", "required": true, "type": "string"}, "status": {"constraintId": "RC-OWNERSHIP-STATUS", "enum": ["UNIQUE", "AMBIGUOUS", "UNMATCHED", "UNKNOWN"], "required": true, "type": "string"}}`
- 有效示例：`{"evidenceRefs": ["pkt-cap-syn-001:1"], "policy": "UNIQUE-KEY", "requestInstance": "event-rrq-001", "status": "UNIQUE"}`
- 无效示例：`{"evidenceRefs": [], "policy": "UNIQUE-KEY", "requestInstance": "event-rrq-001", "status": "CERTAIN"}`
- 预期拒绝：`{"constraintId": "RC-OWNERSHIP-STATUS", "path": ["status"]}`
- 拒绝理由：status 必须使用受控所有权词汇

### `OBSERVATION-ASSESSMENT` — 观测评估
- 所有权：观测模块拥有评估、发现或历史更新记录。
- 不确定性：时间链无效为 ERROR，边界重叠为 INCONCLUSIVE。
- 来源需求：无
- 错误行为：返回具名错误或保守未知；不得输出 IUT FAIL。
- 字段定义：`{"domain": {"constraintId": "RC-OBS-DOMAIN", "enum": ["MONOTONIC-CAPTURE", "SYNCHRONIZED-UTC", "UNKNOWN"], "required": true, "type": "string"}, "errorBasis": {"constraintId": "RC-OBS-ERROR-BASIS", "pattern": "^EB-[A-Za-z0-9._-]+$", "required": true, "type": "string"}, "measurementInterval": {"constraintId": "RC-OBS-INTERVAL", "oneOf": [{"additionalProperties": false, "constraintId": "RC-OBS-INTERVAL-VALUE", "properties": {"lower": {"constraintId": "RC-OBS-LOWER", "type": "integer"}, "lowerClosed": {"constraintId": "RC-OBS-LOWER-CLOSED", "type": "boolean"}, "unit": {"constraintId": "RC-OBS-UNIT", "enum": ["tick", "ns", "us"], "type": "string"}, "upper": {"constraintId": "RC-OBS-UPPER", "type": "integer"}, "upperClosed": {"constraintId": "RC-OBS-UPPER-CLOSED", "type": "boolean"}}, "requiredProperties": ["lower", "upper", "lowerClosed", "upperClosed", "unit"], "type": "object"}, {"constraintId": "RC-OBS-INTERVAL-ABSENT", "type": "null"}], "required": true}, "reason": {"constraintId": "RC-OBS-REASON", "minLength": 1, "required": true, "type": "string"}, "verdict": {"constraintId": "RC-OBS-VERDICT", "enum": ["PASS", "FAIL", "INCONCLUSIVE", "ERROR"], "required": true, "type": "string"}}`
- 有效示例：`{"domain": "MONOTONIC-CAPTURE", "errorBasis": "EB-SYN-001", "measurementInterval": {"lower": 100, "lowerClosed": true, "unit": "us", "upper": 104, "upperClosed": true}, "reason": "entire interval lies within the closed requirement interval", "verdict": "PASS"}`
- 无效示例：`{"domain": "MONOTONIC-CAPTURE", "errorBasis": "EB-SYN-001", "measurementInterval": {"lower": 100, "lowerClosed": true, "unit": "seconds", "upper": 104, "upperClosed": true}, "reason": "bad unit", "verdict": "PASS"}`
- 预期拒绝：`{"constraintId": "RC-OBS-INTERVAL", "path": ["measurementInterval"]}`
- 拒绝理由：测量区间单位必须使用受控的精确时间词汇

### `INTAKE-METADATA` — 接入元数据
- 所有权：捕获模块或接入边界拥有该记录。
- 不确定性：未知值不能作为算法先验。
- 来源需求：无
- 错误行为：返回具名错误或保守未知；不得输出 IUT FAIL。
- 字段定义：`{"clockAccuracy": {"additionalProperties": false, "constraintId": "RC-INTAKE-CLOCK", "properties": {"boundNs": {"constraintId": "RC-INTAKE-CLOCK-BOUND", "minimum": 1, "type": "integer"}, "source": {"constraintId": "RC-INTAKE-CLOCK-SOURCE", "minLength": 1, "type": "string"}, "state": {"constraintId": "RC-INTAKE-CLOCK-STATE", "enum": ["DECLARED", "UNKNOWN"], "type": "string"}}, "required": true, "requiredProperties": ["state", "source"], "type": "object"}, "configuration": {"additionalProperties": false, "constraintId": "RC-INTAKE-CONFIG", "properties": {"source": {"constraintId": "RC-INTAKE-CONFIG-SOURCE", "minLength": 1, "type": "string"}, "state": {"constraintId": "RC-INTAKE-CONFIG-STATE", "enum": ["DECLARED", "UNKNOWN"], "type": "string"}}, "required": true, "requiredProperties": ["state", "source"], "type": "object"}, "operatorNote": {"constraintId": "RC-INTAKE-NOTE", "minLength": 1, "required": true, "type": "string"}, "rootCause": {"additionalProperties": false, "constraintId": "RC-INTAKE-ROOT-CAUSE", "properties": {"source": {"constraintId": "RC-INTAKE-ROOT-SOURCE", "minLength": 1, "type": "string"}, "state": {"constraintId": "RC-INTAKE-ROOT-STATE", "enum": ["DECLARED", "UNKNOWN"], "type": "string"}}, "required": true, "requiredProperties": ["state", "source"], "type": "object"}, "topology": {"additionalProperties": false, "constraintId": "RC-INTAKE-TOPOLOGY", "properties": {"source": {"constraintId": "RC-INTAKE-TOPOLOGY-SOURCE", "minLength": 1, "type": "string"}, "state": {"constraintId": "RC-INTAKE-TOPOLOGY-STATE", "enum": ["DECLARED", "UNKNOWN"], "type": "string"}}, "required": true, "requiredProperties": ["state", "source"], "type": "object"}}`
- 有效示例：`{"clockAccuracy": {"source": "not supplied", "state": "UNKNOWN"}, "configuration": {"source": "synthetic fixture cfg-1", "state": "DECLARED"}, "operatorNote": "synthetic intake only", "rootCause": {"source": "not claimed", "state": "UNKNOWN"}, "topology": {"source": "not supplied", "state": "UNKNOWN"}}`
- 无效示例：`{"clockAccuracy": {"boundNs": 0, "source": "bad bound", "state": "DECLARED"}, "configuration": {"source": "synthetic fixture cfg-1", "state": "DECLARED"}, "operatorNote": "synthetic intake only", "rootCause": {"source": "not claimed", "state": "UNKNOWN"}, "topology": {"source": "not supplied", "state": "UNKNOWN"}}`
- 预期拒绝：`{"constraintId": "RC-INTAKE-CLOCK-BOUND", "path": ["clockAccuracy", "boundNs"]}`
- 拒绝理由：已声明的时钟界必须为正数；UNKNOWN 不得以零界表示

### `FINDING-RECORD` — 发现记录
- 所有权：观测模块拥有评估、发现或历史更新记录。
- 不确定性：发现记录不是根因标签。
- 来源需求：无
- 错误行为：返回具名错误或保守未知；不得输出 IUT FAIL。
- 字段定义：`{"assumptions": {"constraintId": "RC-FINDING-ASSUMPTIONS", "items": {"constraintId": "RC-FINDING-ASSUMPTION", "minLength": 1, "type": "string"}, "required": true, "type": "array"}, "evidenceRefs": {"constraintId": "RC-FINDING-EVIDENCE", "items": {"constraintId": "RC-EVIDENCE-REF", "pattern": "^(cap|pkt|dgram|transfer|event)-[A-Za-z0-9._:-]+$", "type": "string"}, "minItems": 1, "required": true, "type": "array", "uniqueItems": true}, "facts": {"constraintId": "RC-FINDING-FACTS", "items": {"constraintId": "RC-FINDING-FACT", "minLength": 1, "type": "string"}, "minItems": 1, "required": true, "type": "array"}, "judgmentBasis": {"constraintId": "RC-FINDING-BASIS", "items": {"constraintId": "RC-EVIDENCE-REF", "pattern": "^(cap|pkt|dgram|transfer|event)-[A-Za-z0-9._:-]+$", "type": "string"}, "minItems": 1, "required": true, "type": "array"}, "scope": {"additionalProperties": false, "constraintId": "RC-FINDING-SCOPE", "properties": {"captureIds": {"constraintId": "RC-FINDING-CAPTURES", "items": {"constraintId": "RC-FINDING-CAPTURE", "pattern": "^(?:cap-[a-z0-9][a-z0-9-]*|HC-[0-9]{2})$", "type": "string"}, "minItems": 1, "type": "array"}, "requirementIds": {"constraintId": "RC-FINDING-REQUIREMENTS", "items": {"constraintId": "RC-FINDING-REQUIREMENT", "pattern": "^CRS-M1-[0-9]{5}$", "type": "string"}, "type": "array"}}, "required": true, "requiredProperties": ["captureIds", "requirementIds"], "type": "object"}}`
- 有效示例：`{"assumptions": ["capture ordering preserved"], "evidenceRefs": ["pkt-cap-syn-001:2"], "facts": ["synthetic DATA block observed"], "judgmentBasis": ["pkt-cap-syn-001:2"], "scope": {"captureIds": ["cap-syn-001"], "requirementIds": ["CRS-M1-00021"]}}`
- 无效示例：`{"assumptions": [], "evidenceRefs": ["pkt-cap-syn-001:2"], "facts": [], "judgmentBasis": ["pkt-cap-syn-001:2"], "scope": {"captureIds": ["cap-syn-001"], "requirementIds": []}}`
- 预期拒绝：`{"constraintId": "RC-FINDING-FACTS", "path": ["facts"]}`
- 拒绝理由：发现必须至少包含一个有界事实，且不得冒充根因断言

### `HISTORY-HANDLE` — 历史句柄
- 所有权：会话持有 HistoryHandle；仅观测/历史更新模块推进其带版本的相容历史。
- 不确定性：UNKNOWN-EFFECT 与未确认 Recover 保留 H，并将受影响状态标为 CONSERVATIVE-UNKNOWN；CONFIRMED-NOT-SENT 保留历史；相同 H 集合可以保留不同的相容历史。
- 来源需求：无
- 错误行为：拒绝超出作用域的假设和未知状态值；返回具名错误且不得转换为 IUT FAIL。
- 字段定义：`{"H": {"constraintId": "RC-HISTORY-H", "items": {"constraintId": "RC-HYPOTHESIS-ID", "pattern": "^h[A-Za-z0-9._-]+$", "type": "string"}, "minItems": 0, "required": true, "type": "array", "uniqueItems": true}, "compatibleStateByHypothesis": {"additionalProperties": {"constraintId": "RC-HISTORY-FRONTIER", "pattern": "^frontier-[A-Za-z0-9._:-]+$", "type": "string"}, "constraintId": "RC-HISTORY-COMPATIBLE", "required": true, "type": "object"}, "statusByHypothesis": {"additionalProperties": {"constraintId": "RC-HISTORY-STATUS-VALUE", "enum": ["KNOWN", "CONSERVATIVE-UNKNOWN"], "type": "string"}, "constraintId": "RC-HISTORY-STATUS", "required": false, "type": "object"}, "version": {"constraintId": "RC-HISTORY-VERSION", "minimum": 0, "required": true, "type": "integer"}}`
- 有效示例：`{"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-syn-0"}, "statusByHypothesis": {"h0": "CONSERVATIVE-UNKNOWN"}, "version": 0}`
- 无效示例：`{"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-syn-0"}, "statusByHypothesis": {"h0": "BANANA"}, "version": 0}`
- 预期拒绝：`{"constraintId": "RC-HISTORY-STATUS-VALUE", "path": ["statusByHypothesis", "h0"]}`
- 拒绝理由：状态必须复用所绑定 HistoryHandle 的 KNOWN 或 CONSERVATIVE-UNKNOWN

## 工具需求

| ID | 责任模块 | 来源关系 | 验收 | 需求 |
|---|---|---|---|---|
| `TR-CAPTURE-INTAKE` | `MOD-CAPTURE` | `ENGINEERING-DECISION` | `AC-SYN-TRANSFER` | 保留捕获身份与时钟作用域 |
| `TR-DATAGRAM-REASSEMBLY` | `MOD-REASSEMBLY` | `ENGINEERING-DECISION` | `AC-SYN-TRANSFER` | 仅重组来源一致的 IPv4 数据报 |
| `TR-TRANSFER-RECONSTRUCTION` | `MOD-TRANSFER` | `PROTOCOL-DERIVED` | `AC-SYN-TRANSFER` | 重建有界 TFTP 传输候选 |
| `TR-PROTOCOL-EVENT` | `MOD-TRANSFER` | `METHOD-DERIVED` | `AC-SYN-TRANSFER` | 在不虚构应用事实的前提下派生带类型协议事件 |
| `TR-OWNERSHIP` | `MOD-OWNERSHIP` | `METHOD-DERIVED` | `AC-SYN-TRANSFER` | 保守解析响应所有权 |
| `TR-OBSERVATION-ASSESSMENT` | `MOD-OBSERVATION` | `METHOD-DERIVED` | `AC-SYN-TRANSFER` | 以显式时序不确定性评估观测 |
| `TR-HISTORY-COMPATIBILITY` | `MOD-OBSERVATION` | `METHOD-DERIVED` | `AC-SYN-TRANSFER` | 保守更新有限相容历史 |
| `TR-TRACEABLE-FINDING` | `MOD-OBSERVATION` | `ENGINEERING-DECISION` | `AC-SYN-TRANSFER` | 在不作故障真值主张的前提下报告有界发现 |

### `TR-CAPTURE-INTAKE` — 保留捕获身份与时钟作用域
- 触发：调用方提供清单绑定的捕获引用。
- 前置条件：清单审计已确认相对路径、大小和 SHA-256。
- 输入：`CAPTURE-IDENTITY`；输出：`PACKET-REF`
- 动作：建立捕获作用域身份，保留 section、interface 与原始 ticks 来源，不推断时钟精度。
- 错误／未知：不可读块、未支持链路类型和未知时钟精度返回解码或 UNKNOWN 元数据，不是 IUT FAIL。
- 证据：CaptureIdentity 与 PacketRef 的原始来源字段。
- 接口：`IF-EXECUTE-RECORD`；CRS：—；控制／方法：`DD-040`, `CR-2026-016 AC-03`

### `TR-DATAGRAM-REASSEMBLY` — 仅重组来源一致的 IPv4 数据报
- 触发：PacketRef 含 IPv4 分片元数据。
- 前置条件：所有分片保留 capture、section 与 interface 作用域。
- 输入：`PACKET-REF`；输出：`DATAGRAM-RECORD`
- 动作：按作用域身份分组，保留全部来源并分类缺失或冲突覆盖；不得以后片覆盖先前数据。
- 错误／未知：缺片、截断或重叠产生不完整或冲突记录，不产生完整 UDP 载荷。
- 证据：DatagramRecord 分片引用与覆盖分类。
- 接口：`IF-EXECUTE-RECORD`；CRS：—；控制／方法：`CR-2026-016 AC-03`

### `TR-TRANSFER-RECONSTRUCTION` — 重建有界 TFTP 传输候选
- 触发：存在完整或已分类不完整的 UDP 数据报。
- 前置条件：初始请求与动态 TID 证据可同普通 UDP 区分。
- 输入：`DATAGRAM-RECORD`；输出：`TRANSFER-RECORD`
- 动作：关联请求、选项协商、DATA/ACK、WAIT、ERROR 与 ABORT，保留歧义和块大小确认状态。
- 错误／未知：已确认接受的选项使用确认值。充分且一致地确认选项未被接受（包括完整基本传输而无选项确认）时采用协议默认值；缺失、冲突或无法关联的证据保持 UNKNOWN；超出块回绕界为 UNSUPPORTED。
- 证据：TransferRecord 的端点、TID、选项与完成证据。
- 接口：`IF-EXECUTE-RECORD`；CRS：`CRS-M1-00021`, `CRS-M1-00025`, `CRS-M1-00032`, `CRS-M1-00620`, `CRS-M1-00635`, `CRS-M1-00646`, `CRS-M1-00647`；控制／方法：`CRS-M1-00021`, `CRS-M1-00025`, `CRS-M1-00032`

### `TR-PROTOCOL-EVENT` — 在不虚构应用事实的前提下派生带类型协议事件
- 触发：TransferRecord 含可用线上证据。
- 前置条件：事件层已明确为 WIRE、PARSE-RESULT、APPLICATION 或 ENVIRONMENT。
- 输入：`TRANSFER-RECORD`；输出：`PROTOCOL-EVENT`
- 动作：产生带关联键、完整原始引用和解析可信边界的类型化事件。
- 错误／未知：不可观察的应用决定保持缺失或 UNKNOWN，不从模型状态推断。
- 证据：ProtocolEvent 关联键及原始 PacketRef 链。
- 接口：`IF-OBS-INTERPRET`；CRS：—；控制／方法：`DD-039`, `CR-2026-016 AC-03`

### `TR-OWNERSHIP` — 保守解析响应所有权
- 触发：ProtocolEvent 可能响应已声明的请求实例。
- 前置条件：候选实例集合具匹配策略和事件顺序。
- 输入：`PROTOCOL-EVENT`；输出：`OWNERSHIP-RESULT`
- 动作：应用 UNIQUE-KEY、FIFO 或 MOST-RECENT，并保留取消、替代和歧义证据。
- 错误／未知：可能所有者不相容时为歧义，不能作为唯一响应消费。
- 证据：OwnershipResult 的策略、请求实例和支持事件引用。
- 接口：`IF-OBS-INTERPRET`；CRS：—；控制／方法：`IF-OBS-INTERPRET`, `CR-2026-016 AC-03`

### `TR-OBSERVATION-ASSESSMENT` — 以显式时序不确定性评估观测
- 触发：存在唯一归属或明确不完整的观测。
- 前置条件：测量区间、声明域和误差依据可用或已明确无效。
- 输入：`OWNERSHIP-RESULT`, `PROTOCOL-EVENT`；输出：`OBSERVATION-ASSESSMENT`
- 动作：以区间拓扑和声明符合性域产生四值评估。
- 错误／未知：测量域交集为空或时间链无效为 ERROR；边界重叠为 INCONCLUSIVE。
- 证据：ObservationAssessment 区间、域和不确定性引用。
- 接口：`IF-OBS-INTERPRET`；CRS：—；控制／方法：`IF-OBS-INTERPRET`, `T5`

### `TR-HISTORY-COMPATIBILITY` — 保守更新有限相容历史
- 触发：ObservationAssessment 返回规范化可接纳结果。
- 前置条件：HistoryHandle 属于 SessionContext 并保留有版本前沿。
- 输入：`OBSERVATION-ASSESSMENT`, `HISTORY-HANDLE`；输出：`HISTORY-HANDLE`
- 动作：仅将接纳的相容集合与当前假设集合相交，并保留逐假设历史。
- 错误／未知：ERROR、UNKNOWN-EFFECT 和资源耗尽不排除或复活假设。
- 证据：HistoryHandle 版本及相容状态前沿引用。
- 接口：`IF-HIST-UPDATE`；CRS：—；控制／方法：`DD-039`, `IF-OBS-INTERPRET`

### `TR-TRACEABLE-FINDING` — 在不作故障真值主张的前提下报告有界发现
- 触发：存在完成评估或具名 blocked/unknown 条件。
- 前置条件：所有支持记录保留捕获和解释来源。
- 输入：`OBSERVATION-ASSESSMENT`, `INTAKE-METADATA`；输出：`FINDING-RECORD`
- 动作：输出观测事实、判断依据、范围和未决假设，并与根因标签分离。
- 错误／未知：未知拓扑、时钟、配置或根因保持显式，不能成为故障标签。
- 证据：FindingRecord 证据链接和适用范围。
- 接口：`IF-OBS-INTERPRET`；CRS：—；控制／方法：`DD-040`, `CR-2026-016 AC-03`

## 模块合同

上游策略：每个跨模块输入的生产者必须能通过 `upstreamModuleIds` 直接或传递到达；外部输入以及由消费模块自身产生的记录无需上游边。

### `MOD-CAPTURE` — 捕获接入与数据包来源
- 职责：核验清单绑定的捕获身份并产生不可变数据包引用，不推断时钟精度或字段真值。
- 前置条件：CaptureIdentity 与已审计清单字节一致。；接入元数据已明确声明或标为 UNKNOWN。
- 输入：`CAPTURE-IDENTITY`, `INTAKE-METADATA`；输出：`PACKET-REF`
- 需求：`TR-CAPTURE-INTAKE`；接口：`IF-EXECUTE-RECORD`
- 验收：`AC-SYN-TRANSFER`, `AC-EXP-SCENE`；运行参数：`RP-RESOURCE`；上游：无
- 步骤：
  - `S1`：解析任何块之前先核验捕获身份。
  - `S2`：解析受支持的 section 与 interface 声明并保留其作用域。
  - `S3`：产生含精确原始 ticks、分辨率和长度来源的 PacketRef。
- 不变量：接口身份受捕获和 section 作用域约束。；时钟分辨率绝不隐含时钟精度。；未支持块不得产生空成功捕获。
- 失败结果：
  - `IDENTITY-ERROR` — 条件：清单身份与提供字节不一致。 结果：在块解析前拒绝接入且不产生 PacketRef。
  - `UNSUPPORTED-CAPTURE` — 条件：所需块或链路类型不受支持。 结果：返回具名不支持结果，而非 IUT FAIL。
- 输出值映射：
  - 无
### `MOD-REASSEMBLY` — 保留来源的数据报重建
- 职责：从有作用域的数据包分片建立有界数据报候选，同时保留缺口、重叠冲突和全部来源引用。
- 前置条件：每个分片都有具作用域的 PacketRef。；缓冲前已有资源界。
- 输入：`PACKET-REF`；输出：`DATAGRAM-RECORD`
- 需求：`TR-DATAGRAM-REASSEMBLY`；接口：`IF-EXECUTE-RECORD`
- 验收：`AC-SYN-TRANSFER`；运行参数：`RP-RESOURCE`；上游：`MOD-CAPTURE`
- 步骤：
  - `S1`：仅按声明的作用域重建身份对分片分组。
  - `S2`：计算覆盖、缺失范围和重叠，不得覆盖先前字节。
  - `S3`：产生 COMPLETE、GAPPED 或 CONFLICT 重建并保留全部 PacketRef。
- 不变量：分片绝不跨捕获、section 或 interface 作用域。；覆盖不完整时绝不把首片视为完整数据报。
- 失败结果：
  - `INCOMPLETE-DATAGRAM` — 条件：覆盖存在缺口或截断。 结果：产生 reassemblyStatus=GAPPED 且不产生完整 UDP 载荷。
  - `OVERLAP-CONFLICT` — 条件：重叠范围含不同字节。 结果：保留双方来源并产生冲突，不采用后写覆盖。
- 输出值映射：
  - `DATAGRAM-RECORD.reassemblyStatus` → `COMPLETE`, `GAPPED`, `CONFLICT`：覆盖缺口映射为 GAPPED；INCOMPLETE-DATAGRAM 是失败码，不是记录字段值。
- 受控不覆盖先前字节的重建策略：`{"differentOverlap": "CONFLICT", "gapStatus": "GAPPED", "identicalOverlap": "DUPLICATE", "overlapPolicy": "IDENTICAL-ONLY", "overwriteEarlierBytes": false}`
### `MOD-TRANSFER` — TFTP 传输与协议事件重建
- 职责：关联有界 TFTP 传输候选并派生带类型协议事件，不虚构应用层事实。
- 前置条件：数据报完整性已经分类。；初始请求与动态 TID 证据仍可区分。
- 输入：`DATAGRAM-RECORD`, `TRANSFER-RECORD`；输出：`TRANSFER-RECORD`, `PROTOCOL-EVENT`
- 需求：`TR-TRANSFER-RECONSTRUCTION`, `TR-PROTOCOL-EVENT`；接口：`IF-EXECUTE-RECORD`, `IF-OBS-INTERPRET`
- 验收：`AC-SYN-TRANSFER`, `AC-SYN-INTEGRITY`；运行参数：`RP-RESOURCE`；上游：`MOD-REASSEMBLY`
- 步骤：
  - `S1`：依据请求与端点证据建立或保留传输候选。
  - `S2`：应用选项、块和终止规则，同时保留重传与歧义证据。
  - `S3`：产生带完整原始引用链的线上或派生类型事件。
- 不变量：未知选项证据绝不变成已接受值或默认值。；动态 TID 关联不得由固定端口假设替代。；不得从仅线上证据推断应用事实。
- 失败结果：
  - `AMBIGUOUS-TRANSFER` — 条件：证据与多个传输候选相容。 结果：保留歧义且不作唯一所有权主张。
  - `UNSUPPORTED-BLOCK-RANGE` — 条件：块推进超出声明的有界范围。 结果：返回 UNSUPPORTED，且不合并回绕后的块身份。
- 输出值映射：
  - 无
### `MOD-OWNERSHIP` — 请求实例所有权解析
- 职责：按声明的匹配策略解析响应所有权，同时保留取消、替代和歧义。
- 前置条件：候选请求实例和事件顺序均明确。；匹配策略为 UNIQUE-KEY、FIFO 或 MOST-RECENT。
- 输入：`PROTOCOL-EVENT`；输出：`OWNERSHIP-RESULT`
- 需求：`TR-OWNERSHIP`；接口：`IF-OBS-INTERPRET`
- 验收：`AC-SYN-TRANSFER`；运行参数：`RP-RESOURCE`；上游：`MOD-TRANSFER`
- 步骤：
  - `S1`：移除被有效取消或替代触发终止的候选。
  - `S2`：对剩余相容候选应用声明的策略。
  - `S3`：产生唯一、未匹配或歧义所有权及其支持引用。
- 不变量：一个响应绝不被两个不相容请求实例静默消费。；截止前的合法取消阻止该义务随后产生无响应失败。
- 失败结果：
  - `AMBIGUOUS-OWNERSHIP` — 条件：仍存在多个不相容所有者。 结果：产生 AMBIGUOUS 并禁止作为唯一响应消费。
- 输出值映射：
  - 无
### `MOD-OBSERVATION` — 观测评估、历史更新与有界报告
- 职责：产生四值评估、保守推进相容历史，并在不作根因主张的前提下报告有界发现。
- 前置条件：所有权状态与测量来源均明确。；HistoryHandle 属于当前会话和版本。
- 输入：`OWNERSHIP-RESULT`, `PROTOCOL-EVENT`, `OBSERVATION-ASSESSMENT`, `HISTORY-HANDLE`, `INTAKE-METADATA`；输出：`OBSERVATION-ASSESSMENT`, `HISTORY-HANDLE`, `FINDING-RECORD`
- 需求：`TR-OBSERVATION-ASSESSMENT`, `TR-HISTORY-COMPATIBILITY`, `TR-TRACEABLE-FINDING`；接口：`IF-OBS-INTERPRET`, `IF-HIST-UPDATE`
- 验收：`AC-SYN-TRANSFER`, `AC-EXP-TRUTH`, `AC-EXP-CAUSAL`, `AC-EXP-DENOMINATOR`；运行参数：`RP-RESOURCE`；上游：`MOD-TRANSFER`, `MOD-OWNERSHIP`
- 步骤：
  - `S1`：使用精确区间拓扑求测量域与要求域的交集。
  - `S2`：产生 PASS、FAIL、INCONCLUSIVE 或 ERROR，不折叠未知证据。
  - `S3`：仅通过 IF-HIST-UPDATE 推进历史，且绝不复活已排除假设。
  - `S4`：产生将事实、范围、假设和证据分离的有界发现。
- 不变量：PASS 要求所有可能真值均满足要求。；FAIL 要求所有可能真值均违反要求。；ERROR 和 INCONCLUSIVE 绝不降级为 FAIL。；相同假设集合可以保留不同的相容历史。
- 失败结果：
  - `INVALID-MEASUREMENT` — 条件：时间链、误差预算或测量域交集无效。 结果：产生 ERROR 且不排除假设。
  - `RESOURCE-UNKNOWN` — 条件：有界历史操作无法在声明资源内完成。 结果：保留先前历史并标为保守未知，而非 IUT FAIL。
- 输出值映射：
  - 无

## 有界算法细化

### `AR-FINITE` — 有界显式 CL-TAV 参考内核
- 边界：未规定通用求解器、隐式离散化、完备性主张或运行时实现；该内核只在声明语法与限额上显式传播有限路径。
- 表示：稳定有限的假设 ID 集合将每个假设映射到带版本的显式路径前沿。守卫使用既有受限 AST 和精确有理区间约束；更新是声明的有限赋值。仅当假设、控制状态、时钟约束和完整历史来源相同时才可合并前沿。
- 保守行为：不支持的语法、资源限额或不可判定的可行路径结果均返回具名接口 UNKNOWN、GAP、SPEC-ERROR 或受控错误路径，绝不排除假设或证明等价。
- 复杂度边界：工作量受配置的假设数、动作数、观测类数、路径长度和前沿状态数约束；不作多项式或完备性主张。
- 守卫语法：`TRUE`, `AND`, `STATE-EQUALS`, `RATIONAL-INTERVAL-CONTAINS`, `TYPED-FIELD-EQUALS`；更新语法：`STATE-ASSIGN`, `CLOCK-RESET-TO-ZERO`, `TYPED-FIELD-ASSIGN`
- 前沿：`hypothesisId`, `controlStateId`, `clockConstraint`, `typedStore`, `pathLength`, `historyProvenance`, `status`；合并键：`hypothesisId`, `controlStateId`, `clockConstraint`, `typedStore`, `historyProvenance`
- 传播步骤：
  - 校验模型和选择时快照。
  - 展开已启用转换且不丢失相关约束。
  - 求交观测与时序约束。
  - 保留每个可行后继及完整历史来源。
  - 仅合并键完全相同的条目。
  - 不支持语法按 SPEC-ERROR 拒绝；达到配置计算限额时返回保守未知。两者均不得删除假设。
- 限额行为：`{"actions": "ADMIT-REFUSED", "frontierStates": "CONSERVATIVE-UNKNOWN", "hypotheses": "SPEC-ERROR", "observationClasses": "PredictionGapError", "pathLength": "CONSERVATIVE-UNKNOWN"}`
- 结果映射：`{"IF-EQUIV": {"failure": ["UNKNOWN", "RESOURCE-UNKNOWN"], "success": ["established", "notEstablished", "unknown"]}, "IF-EXECUTE-RECORD": {"failure": ["CONFIRMED-NOT-SENT", "UNKNOWN-EFFECT"], "success": ["record", "effectClass", "correlationId"]}, "IF-HIST-UPDATE": {"failure": ["Stop-Empty", "RESOURCE-UNKNOWN", "CONSERVATIVE-UNKNOWN"], "success": ["HistoryHandlePrime", "Hprime", "Stop-Empty"]}, "IF-OBS-INTERPRET": {"failure": ["ERROR", "INCONCLUSIVE", "UNKNOWN-EFFECT"], "success": ["Iz", "effectClass", "summaryConfirmed", "postSummary", "ownershipResult", "measurementInterval"]}, "IF-PRED-OBS": {"failure": ["PredictionGapError", "RESOURCE-UNKNOWN"], "success": ["currentlyValidNonemptyClasses", "PredictionGapError"]}, "IF-PREP-RECOVER": {"failure": ["UNKNOWN-EFFECT", "PREP-ERROR", "CONFIRMED-NOT-SENT"], "success": ["targetConfirmed", "summaryConfirmed", "prepError", "ineligible", "declaredTarget", "evidence", "postSummary"]}, "IF-RESOURCE-STOP": {"failure": ["Stop-Budget", "Stop-Error", "Stop-645"], "success": ["stopClass", "finalH", "trace"]}, "IF-SELECT-ADMIT": {"failure": ["PredictionGapError", "SPEC-ERROR", "ADMIT-REFUSED"], "success": ["kind", "tStar", "S", "admitA2A5"]}}`
- 模型实例结构：`{"clockConstraint": {"boundType": "rational", "feasibility": ["FEASIBLE", "INFEASIBLE", "COMPUTATION-UNKNOWN"], "finiteWitnessProjection": "one declared clock ID plus its rational interval; W1/W2 have exact one-clock semantics", "reset": "substitute exact zero before canonicalization", "timeAdvance": "one shared nonnegative rational delta", "type": "canonical-difference-bounds", "unsupportedProjection": "multi-clock or cross-clock relation without a named DBM projection is SPEC-ERROR, never a computed successor"}, "clockIds": ["x"], "guardAst": {"operandRepresentation": "RATIONAL-INTERVAL-CONTAINS uses a declared clock ID and one structured rational interval; strings are display-only", "supported": ["TRUE", "AND", "STATE-EQUALS", "RATIONAL-INTERVAL-CONTAINS", "TYPED-FIELD-EQUALS"], "type": "tagged-tree", "unsupported": ["OR", "NOT", "CALL"], "unsupportedBehavior": "SPEC-ERROR before expansion; preserve H, summary, and charge state"}, "rational": {"canonical": "gcd(abs(numerator),positiveDenominator)=1 and positiveDenominator>0", "required": ["numerator", "positiveDenominator"], "type": "object"}, "stateIds": ["q0", "q1", "q2", "q3"], "transition": {"additionalProperties": false, "required": ["id", "source", "target", "guardAst", "simultaneousUpdates"], "type": "object"}, "typedStore": {"keys": "declared variable IDs", "type": "finite-map", "values": "declared scalar-domain members"}, "typedVariables": {"mode": ["normal", "recovery"]}}`
- 历史后端 → 接口 → S9 的有效载荷及来源：`{"backend": {"H_c": ["h0"], "eta_c": {"h0": "frontier-syn-1"}, "historyVersion": 1}, "branchWitnesses": [{"affectedHypothesisIds": [], "backend": {"H_c": ["h0"], "eta_c": {"h0": "frontier-next"}, "historyVersion": 1}, "effectKnowledge": "COMPATIBLE", "historyInputVersion": 0, "id": "HR-NO-COMMIT", "inputGamma": {"currentSummary": "q0", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "KNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "inputH": ["h0"], "inputHistoryHandle": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-old"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 0}, "interface": {"HistoryHandlePrime": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-next"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 1}, "Hprime": ["h0"], "status": "KNOWN"}, "outcome": {"postSummary": "q1", "summaryConfirmed": false}, "s9": {"GammaPrime": {"currentSummary": "q0", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "KNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "Hprime": ["h0"], "etaPrime": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-next"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 1}, "outerDisposition": "CONTINUE", "status": "OK", "summaryCommitted": false}, "snapshotVersion": 0}, {"affectedHypothesisIds": [], "backend": {"H_c": [], "eta_c": {}, "historyVersion": 1}, "effectKnowledge": "PROVEN-INCOMPATIBLE", "historyInputVersion": 0, "id": "HR-STOP-EMPTY", "inputGamma": {"currentSummary": "q0", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "KNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "inputH": ["h0"], "inputHistoryHandle": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-old"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 0}, "interface": {"HistoryHandlePrime": {"H": [], "compatibleStateByHypothesis": {}, "statusByHypothesis": {}, "version": 1}, "Hprime": [], "status": "Stop-Empty"}, "outcome": {"postSummary": null, "summaryConfirmed": false}, "s9": {"GammaPrime": {"currentSummary": "q0", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "KNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "Hprime": [], "etaPrime": {"H": [], "compatibleStateByHypothesis": {}, "statusByHypothesis": {}, "version": 1}, "outerDisposition": "Stop-Empty", "status": "OK", "summaryCommitted": false}, "snapshotVersion": 0}, {"affectedHypothesisIds": ["h0"], "backend": {"H_c": ["h0"], "eta_c": {"h0": "frontier-conservative"}, "historyVersion": 1}, "effectKnowledge": "UNKNOWN-EFFECT", "historyInputVersion": 0, "id": "HR-CONSERVATIVE", "inputGamma": {"currentSummary": "", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "UNKNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "inputH": ["h0"], "inputHistoryHandle": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-old"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 0}, "interface": {"HistoryHandlePrime": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-conservative"}, "statusByHypothesis": {"h0": "CONSERVATIVE-UNKNOWN"}, "version": 1}, "Hprime": ["h0"], "status": "CONSERVATIVE-UNKNOWN"}, "outcome": {"postSummary": null, "summaryConfirmed": false}, "s9": {"GammaPrime": {"currentSummary": "", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "UNKNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "Hprime": ["h0"], "etaPrime": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-conservative"}, "statusByHypothesis": {"h0": "CONSERVATIVE-UNKNOWN"}, "version": 1}, "outerDisposition": "CONTINUE", "status": "OK", "summaryCommitted": false}, "snapshotVersion": 0}, {"affectedHypothesisIds": [], "backend": null, "effectKnowledge": "VERSION-MISMATCH", "historyInputVersion": 0, "id": "HR-VERSION-MISMATCH", "inputGamma": {"currentSummary": "q0", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "KNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "inputH": ["h0"], "inputHistoryHandle": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-old"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 0}, "interface": null, "outcome": {"postSummary": "q1", "summaryConfirmed": true}, "s9": {"GammaPrime": {"currentSummary": "q0", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "KNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "Hprime": ["h0"], "etaPrime": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-old"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 0}, "outerDisposition": "Stop-Error", "reason": "history version mismatch", "status": "SPEC-ERROR", "summaryCommitted": false}, "snapshotVersion": 1}], "inputGamma": {"currentSummary": "q0", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "KNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "interface": {"HistoryHandlePrime": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-syn-1"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 1}, "Hprime": ["h0"], "status": "KNOWN"}, "normalizedOutcome": {"postSummary": "q1", "summaryConfirmed": true}, "s9": {"GammaPrime": {"currentSummary": "q1", "errorHistory": [], "knownEvidence": [], "knownTarget": null, "qStatus": "KNOWN", "resourceRemainder": 3, "retryCap": 2, "retryCount": 0, "sessionId": "session-syn-1", "unknownHistory": []}, "Hprime": ["h0"], "etaPrime": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-syn-1"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 1}, "status": "OK", "summaryCommitted": true, "summaryConfirmed": true}, "sourceMap": {"interface.HistoryHandlePrime.compatibleStateByHypothesis": "backend.eta_c", "interface.HistoryHandlePrime.version": "backend.historyVersion", "interface.Hprime": "backend.H_c", "s9.GammaPrime.currentSummary": "normalizedOutcome.postSummary when the S9 guard holds; otherwise inputGamma.currentSummary", "s9.GammaPrime.otherSessionFields": "inputGamma unchanged; S7/S8 effects are upstream of S9", "s9.GammaPrime.qStatus": "inputGamma.qStatus", "s9.Hprime": "interface.Hprime", "s9.etaPrime": "interface.HistoryHandlePrime"}}`
- 内部结果：`FEASIBLE`, `INFEASIBLE`, `COMPUTATION-UNKNOWN`, `UNSUPPORTED-SYNTAX`, `LIMIT-REACHED`, `EMPTY-HISTORY`
- 传播规则：`[{"id": "FK-VALIDATE", "rule": "Reject unsupported AST nodes or ill-typed operands as SPEC-ERROR before expansion."}, {"id": "FK-ADVANCE", "rule": "Advance all clocks by one shared nonnegative rational delta and retain difference correlations."}, {"id": "FK-INTERSECT", "rule": "Conjoin transition guard, observation class, and timing interval; canonicalize before feasibility classification."}, {"id": "FK-UPDATE", "rule": "Apply state/clock/store updates simultaneously, then canonicalize the successor constraint."}, {"id": "FK-MERGE", "rule": "Merge only entries identical on hypothesisId, controlStateId, clockConstraint, typedStore, and historyProvenance."}, {"id": "FK-LIMIT", "rule": "Path/frontier limits return CONSERVATIVE-UNKNOWN without deleting hypotheses; they never produce Stop-Empty or equivalence."}]`
- 完整返回映射：`[{"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-PRED-OBS", "internalResult": "FEASIBLE", "output": "currentlyValidNonemptyClasses", "reachable": true, "returnContract": {"adapter": "OK for FEASIBLE nonempty projection; all conservative failures become GAP with a named reason", "branchTag": "FEASIBLE", "fieldSources": {"classesByTest": "KERNEL", "historyVersionUsed": "KERNEL", "reason": "KERNEL", "status": "KERNEL", "uncertaintyRef": "KERNEL"}, "recordType": "PredictionResult", "requiredFields": ["status", "reason", "classesByTest", "historyVersionUsed", "uncertaintyRef"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-PRED-OBS", "internalResult": "INFEASIBLE", "output": "PredictionGapError", "reachable": true, "returnContract": {"adapter": "OK for FEASIBLE nonempty projection; all conservative failures become GAP with a named reason", "branchTag": "INFEASIBLE", "fieldSources": {"historyVersionUsed": "KERNEL", "reason": "KERNEL", "status": "KERNEL", "uncertaintyRef": "KERNEL"}, "recordType": "PredictionResult", "requiredFields": ["status", "reason", "historyVersionUsed", "uncertaintyRef"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-PRED-OBS", "internalResult": "COMPUTATION-UNKNOWN", "output": "RESOURCE-UNKNOWN", "reachable": true, "returnContract": {"adapter": "OK for FEASIBLE nonempty projection; all conservative failures become GAP with a named reason", "branchTag": "COMPUTATION-UNKNOWN", "fieldSources": {"historyVersionUsed": "KERNEL", "reason": "KERNEL", "status": "KERNEL", "uncertaintyRef": "KERNEL"}, "recordType": "PredictionResult", "requiredFields": ["status", "reason", "historyVersionUsed", "uncertaintyRef"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-PRED-OBS", "internalResult": "UNSUPPORTED-SYNTAX", "output": "PredictionGapError", "reachable": true, "returnContract": {"adapter": "OK for FEASIBLE nonempty projection; all conservative failures become GAP with a named reason", "branchTag": "UNSUPPORTED-SYNTAX", "fieldSources": {"historyVersionUsed": "KERNEL", "reason": "KERNEL", "status": "KERNEL", "uncertaintyRef": "KERNEL"}, "recordType": "PredictionResult", "requiredFields": ["status", "reason", "historyVersionUsed", "uncertaintyRef"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-PRED-OBS", "internalResult": "LIMIT-REACHED", "output": "RESOURCE-UNKNOWN", "reachable": true, "returnContract": {"adapter": "OK for FEASIBLE nonempty projection; all conservative failures become GAP with a named reason", "branchTag": "LIMIT-REACHED", "fieldSources": {"historyVersionUsed": "KERNEL", "reason": "KERNEL", "status": "KERNEL", "uncertaintyRef": "KERNEL"}, "recordType": "PredictionResult", "requiredFields": ["status", "reason", "historyVersionUsed", "uncertaintyRef"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-PRED-OBS", "internalResult": "EMPTY-HISTORY", "output": "PredictionGapError", "reachable": true, "returnContract": {"adapter": "OK for FEASIBLE nonempty projection; all conservative failures become GAP with a named reason", "branchTag": "EMPTY-HISTORY", "fieldSources": {"historyVersionUsed": "KERNEL", "reason": "KERNEL", "status": "KERNEL", "uncertaintyRef": "KERNEL"}, "recordType": "PredictionResult", "requiredFields": ["status", "reason", "historyVersionUsed", "uncertaintyRef"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-SELECT-ADMIT", "internalResult": "FEASIBLE", "output": "admitA2A5", "reachable": true, "returnContract": {"adapter": "Prediction GAP is TEST-scoped; eligible affordable Prep/Recover still pass A1-A5 admission", "branchTag": "FEASIBLE", "fieldSources": {"actionId": "KERNEL", "actionKind": "KERNEL", "classesUsed": "KERNEL", "kind": "KERNEL", "reason": "KERNEL"}, "recordType": "Decision", "requiredFields": ["kind", "actionKind", "actionId", "classesUsed", "reason"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-SELECT-ADMIT", "internalResult": "INFEASIBLE", "output": "PredictionGapError", "reachable": true, "returnContract": {"adapter": "Prediction GAP is TEST-scoped; eligible affordable Prep/Recover still pass A1-A5 admission", "branchTag": "INFEASIBLE", "fieldSources": {"actionId": "KERNEL", "actionKind": "KERNEL", "classesUsed": "KERNEL", "kind": "KERNEL", "reason": "KERNEL"}, "recordType": "Decision", "requiredFields": ["kind", "actionKind", "actionId", "classesUsed", "reason"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-SELECT-ADMIT", "internalResult": "COMPUTATION-UNKNOWN", "output": "ADMIT-REFUSED", "reachable": true, "returnContract": {"adapter": "Prediction GAP is TEST-scoped; eligible affordable Prep/Recover still pass A1-A5 admission", "branchTag": "COMPUTATION-UNKNOWN", "fieldSources": {"actionId": "KERNEL", "actionKind": "KERNEL", "classesUsed": "KERNEL", "kind": "KERNEL", "reason": "KERNEL"}, "recordType": "Decision", "requiredFields": ["kind", "actionKind", "actionId", "classesUsed", "reason"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-SELECT-ADMIT", "internalResult": "UNSUPPORTED-SYNTAX", "output": "SPEC-ERROR", "reachable": true, "returnContract": {"adapter": "Prediction GAP is TEST-scoped; eligible affordable Prep/Recover still pass A1-A5 admission", "branchTag": "UNSUPPORTED-SYNTAX", "fieldSources": {"actionId": "KERNEL", "actionKind": "KERNEL", "classesUsed": "KERNEL", "kind": "KERNEL", "reason": "KERNEL"}, "recordType": "Decision", "requiredFields": ["kind", "actionKind", "actionId", "classesUsed", "reason"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-SELECT-ADMIT", "internalResult": "LIMIT-REACHED", "output": "ADMIT-REFUSED", "reachable": true, "returnContract": {"adapter": "Prediction GAP is TEST-scoped; eligible affordable Prep/Recover still pass A1-A5 admission", "branchTag": "LIMIT-REACHED", "fieldSources": {"actionId": "KERNEL", "actionKind": "KERNEL", "classesUsed": "KERNEL", "kind": "KERNEL", "reason": "KERNEL"}, "recordType": "Decision", "requiredFields": ["kind", "actionKind", "actionId", "classesUsed", "reason"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-SELECT-ADMIT", "internalResult": "EMPTY-HISTORY", "output": "PredictionGapError", "reachable": true, "returnContract": {"adapter": "Prediction GAP is TEST-scoped; eligible affordable Prep/Recover still pass A1-A5 admission", "branchTag": "EMPTY-HISTORY", "fieldSources": {"actionId": "KERNEL", "actionKind": "KERNEL", "classesUsed": "KERNEL", "kind": "KERNEL", "reason": "KERNEL"}, "recordType": "Decision", "requiredFields": ["kind", "actionKind", "actionId", "classesUsed", "reason"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-EXECUTE-RECORD", "internalResult": "FEASIBLE", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "FEASIBLE", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-EXECUTE-RECORD", "internalResult": "INFEASIBLE", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "INFEASIBLE", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-EXECUTE-RECORD", "internalResult": "COMPUTATION-UNKNOWN", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "COMPUTATION-UNKNOWN", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-EXECUTE-RECORD", "internalResult": "UNSUPPORTED-SYNTAX", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "UNSUPPORTED-SYNTAX", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-EXECUTE-RECORD", "internalResult": "LIMIT-REACHED", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "LIMIT-REACHED", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-EXECUTE-RECORD", "internalResult": "EMPTY-HISTORY", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "EMPTY-HISTORY", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-OBS-INTERPRET", "internalResult": "FEASIBLE", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "FEASIBLE", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-OBS-INTERPRET", "internalResult": "INFEASIBLE", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "INFEASIBLE", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-OBS-INTERPRET", "internalResult": "COMPUTATION-UNKNOWN", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "COMPUTATION-UNKNOWN", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-OBS-INTERPRET", "internalResult": "UNSUPPORTED-SYNTAX", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "UNSUPPORTED-SYNTAX", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-OBS-INTERPRET", "internalResult": "LIMIT-REACHED", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "LIMIT-REACHED", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-OBS-INTERPRET", "internalResult": "EMPTY-HISTORY", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "EMPTY-HISTORY", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-PREP-RECOVER", "internalResult": "FEASIBLE", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "FEASIBLE", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-PREP-RECOVER", "internalResult": "INFEASIBLE", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "INFEASIBLE", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-PREP-RECOVER", "internalResult": "COMPUTATION-UNKNOWN", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "COMPUTATION-UNKNOWN", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-PREP-RECOVER", "internalResult": "UNSUPPORTED-SYNTAX", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "UNSUPPORTED-SYNTAX", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-PREP-RECOVER", "internalResult": "LIMIT-REACHED", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "LIMIT-REACHED", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-PREP-RECOVER", "internalResult": "EMPTY-HISTORY", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "EMPTY-HISTORY", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "INTERSECT-PROVEN", "interfaceId": "IF-HIST-UPDATE", "internalResult": "FEASIBLE", "output": "Hprime", "reachable": true, "returnContract": {"adapter": "Backend returns eta_c and H_c; IF-HIST-UPDATE exposes their typed aliases; S9 alone constructs GammaPrime and commits a confirmed summary.", "branchTag": "FEASIBLE", "fieldSources": {"HistoryHandlePrime": "INTERFACE-ADAPTER", "Hprime": "BACKEND-ALIAS", "compatibleStateByHypothesis": "KERNEL", "historyVersion": "KERNEL", "status": "KERNEL", "summaryEffect": "KERNEL"}, "recordType": "HistoryUpdateResult", "requiredFields": ["status", "compatibleStateByHypothesis", "Hprime", "HistoryHandlePrime", "historyVersion", "summaryEffect"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "INTERSECT-PROVEN", "interfaceId": "IF-HIST-UPDATE", "internalResult": "INFEASIBLE", "output": "Hprime", "reachable": true, "returnContract": {"adapter": "Backend returns eta_c and H_c; IF-HIST-UPDATE exposes their typed aliases; S9 alone constructs GammaPrime and commits a confirmed summary.", "branchTag": "INFEASIBLE", "fieldSources": {"HistoryHandlePrime": "INTERFACE-ADAPTER", "Hprime": "BACKEND-ALIAS", "compatibleStateByHypothesis": "KERNEL", "historyVersion": "KERNEL", "status": "KERNEL", "summaryEffect": "KERNEL"}, "recordType": "HistoryUpdateResult", "requiredFields": ["status", "compatibleStateByHypothesis", "Hprime", "HistoryHandlePrime", "historyVersion", "summaryEffect"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-HIST-UPDATE", "internalResult": "COMPUTATION-UNKNOWN", "output": "CONSERVATIVE-UNKNOWN", "reachable": true, "returnContract": {"adapter": "Backend returns eta_c and H_c; IF-HIST-UPDATE exposes their typed aliases; S9 alone constructs GammaPrime and commits a confirmed summary.", "branchTag": "COMPUTATION-UNKNOWN", "fieldSources": {"HistoryHandlePrime": "INTERFACE-ADAPTER", "Hprime": "BACKEND-ALIAS", "compatibleStateByHypothesis": "KERNEL", "historyVersion": "KERNEL", "status": "KERNEL", "summaryEffect": "KERNEL"}, "recordType": "HistoryUpdateResult", "requiredFields": ["status", "compatibleStateByHypothesis", "Hprime", "HistoryHandlePrime", "historyVersion", "summaryEffect"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-HIST-UPDATE", "internalResult": "UNSUPPORTED-SYNTAX", "output": "CONSERVATIVE-UNKNOWN", "reachable": true, "returnContract": {"adapter": "Backend returns eta_c and H_c; IF-HIST-UPDATE exposes their typed aliases; S9 alone constructs GammaPrime and commits a confirmed summary.", "branchTag": "UNSUPPORTED-SYNTAX", "fieldSources": {"HistoryHandlePrime": "INTERFACE-ADAPTER", "Hprime": "BACKEND-ALIAS", "compatibleStateByHypothesis": "KERNEL", "historyVersion": "KERNEL", "status": "KERNEL", "summaryEffect": "KERNEL"}, "recordType": "HistoryUpdateResult", "requiredFields": ["status", "compatibleStateByHypothesis", "Hprime", "HistoryHandlePrime", "historyVersion", "summaryEffect"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-HIST-UPDATE", "internalResult": "LIMIT-REACHED", "output": "CONSERVATIVE-UNKNOWN", "reachable": true, "returnContract": {"adapter": "Backend returns eta_c and H_c; IF-HIST-UPDATE exposes their typed aliases; S9 alone constructs GammaPrime and commits a confirmed summary.", "branchTag": "LIMIT-REACHED", "fieldSources": {"HistoryHandlePrime": "INTERFACE-ADAPTER", "Hprime": "BACKEND-ALIAS", "compatibleStateByHypothesis": "KERNEL", "historyVersion": "KERNEL", "status": "KERNEL", "summaryEffect": "KERNEL"}, "recordType": "HistoryUpdateResult", "requiredFields": ["status", "compatibleStateByHypothesis", "Hprime", "HistoryHandlePrime", "historyVersion", "summaryEffect"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "EMPTY-PROVEN", "interfaceId": "IF-HIST-UPDATE", "internalResult": "EMPTY-HISTORY", "output": "Stop-Empty", "reachable": true, "returnContract": {"adapter": "Backend returns eta_c and H_c; IF-HIST-UPDATE exposes their typed aliases; S9 alone constructs GammaPrime and commits a confirmed summary.", "branchTag": "EMPTY-HISTORY", "fieldSources": {"HistoryHandlePrime": "INTERFACE-ADAPTER", "Hprime": "BACKEND-ALIAS", "compatibleStateByHypothesis": "KERNEL", "historyVersion": "KERNEL", "status": "KERNEL", "summaryEffect": "KERNEL"}, "recordType": "HistoryUpdateResult", "requiredFields": ["status", "compatibleStateByHypothesis", "Hprime", "HistoryHandlePrime", "historyVersion", "summaryEffect"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-EQUIV", "internalResult": "FEASIBLE", "output": "notEstablished", "reachable": true, "returnContract": {"adapter": "FEASIBLE is notEstablished unless a declared equivalence proof exists", "branchTag": "FEASIBLE", "fieldSources": {"proofBasis": "KERNEL", "status": "KERNEL"}, "recordType": "EquivalenceResult", "requiredFields": ["status", "proofBasis"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-EQUIV", "internalResult": "INFEASIBLE", "output": "notEstablished", "reachable": true, "returnContract": {"adapter": "FEASIBLE is notEstablished unless a declared equivalence proof exists", "branchTag": "INFEASIBLE", "fieldSources": {"proofBasis": "KERNEL", "status": "KERNEL"}, "recordType": "EquivalenceResult", "requiredFields": ["status", "proofBasis"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-EQUIV", "internalResult": "COMPUTATION-UNKNOWN", "output": "unknown", "reachable": true, "returnContract": {"adapter": "FEASIBLE is notEstablished unless a declared equivalence proof exists", "branchTag": "COMPUTATION-UNKNOWN", "fieldSources": {"proofBasis": "KERNEL", "status": "KERNEL"}, "recordType": "EquivalenceResult", "requiredFields": ["status", "proofBasis"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-EQUIV", "internalResult": "UNSUPPORTED-SYNTAX", "output": "unknown", "reachable": true, "returnContract": {"adapter": "FEASIBLE is notEstablished unless a declared equivalence proof exists", "branchTag": "UNSUPPORTED-SYNTAX", "fieldSources": {"proofBasis": "KERNEL", "status": "KERNEL"}, "recordType": "EquivalenceResult", "requiredFields": ["status", "proofBasis"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-EQUIV", "internalResult": "LIMIT-REACHED", "output": "unknown", "reachable": true, "returnContract": {"adapter": "FEASIBLE is notEstablished unless a declared equivalence proof exists", "branchTag": "LIMIT-REACHED", "fieldSources": {"proofBasis": "KERNEL", "status": "KERNEL"}, "recordType": "EquivalenceResult", "requiredFields": ["status", "proofBasis"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-EQUIV", "internalResult": "EMPTY-HISTORY", "output": "notEstablished", "reachable": true, "returnContract": {"adapter": "FEASIBLE is notEstablished unless a declared equivalence proof exists", "branchTag": "EMPTY-HISTORY", "fieldSources": {"proofBasis": "KERNEL", "status": "KERNEL"}, "recordType": "EquivalenceResult", "requiredFields": ["status", "proofBasis"]}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-RESOURCE-STOP", "internalResult": "FEASIBLE", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "FEASIBLE", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-RESOURCE-STOP", "internalResult": "INFEASIBLE", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "INFEASIBLE", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-RESOURCE-STOP", "internalResult": "COMPUTATION-UNKNOWN", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "COMPUTATION-UNKNOWN", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-RESOURCE-STOP", "internalResult": "UNSUPPORTED-SYNTAX", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "UNSUPPORTED-SYNTAX", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "interface does not consume finite-kernel results", "historyEffect": "PRESERVE", "interfaceId": "IF-RESOURCE-STOP", "internalResult": "LIMIT-REACHED", "reachable": false, "rejectionReason": "UNREACHABLE-IN-THIS-INTERFACE", "returnContract": {"adapter": "UNREACHABLE-IN-THIS-INTERFACE", "branchTag": "LIMIT-REACHED", "fieldSources": {}, "recordType": "UNREACHABLE", "requiredFields": []}, "summaryEffect": "PRESERVE"}, {"chargeEffect": "NONE", "condition": "declared consumer path", "historyEffect": "PRESERVE", "interfaceId": "IF-RESOURCE-STOP", "internalResult": "EMPTY-HISTORY", "output": "stopClass=Stop-Empty", "reachable": true, "returnContract": {"adapter": "Apply Empty, Singleton, 645, Equivalent, Budget ordering; retry exhaustion remains Stop-Error", "branchTag": "EMPTY-HISTORY", "fieldSources": {"finalH": "KERNEL", "stopClass": "KERNEL", "trace": "KERNEL"}, "recordType": "StopResult", "requiredFields": ["stopClass", "finalH", "trace"]}, "summaryEffect": "PRESERVE"}]`
- 规格见证：`[{"expected": {"clockConstraint": {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 1, "positiveDenominator": 1}, "upperClosed": true}, "result": "FEASIBLE", "state": "q1", "typedStore": {"mode": "normal"}}, "id": "FK-W1-FEASIBLE", "input": {"clockConstraint": {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 1, "positiveDenominator": 1}, "upperClosed": true}, "delta": {"numerator": 0, "positiveDenominator": 1}, "guard": {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 2, "positiveDenominator": 1}, "upperClosed": true}, "observation": "response", "projectionClock": "x", "quantifier": "EXISTS-DELTA", "state": "q0", "transition": {"guardAst": {"clock": "x", "interval": {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 2, "positiveDenominator": 1}, "upperClosed": true}, "tag": "RATIONAL-INTERVAL-CONTAINS"}, "id": "t01", "simultaneousUpdates": [], "source": "q0", "target": "q1"}, "typedStore": {"mode": "normal"}}}, {"expected": {"result": "INFEASIBLE", "successorCount": 0}, "id": "FK-W2-INFEASIBLE", "input": {"clockConstraint": {"lower": {"numerator": 3, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 4, "positiveDenominator": 1}, "upperClosed": true}, "delta": {"numerator": 0, "positiveDenominator": 1}, "guard": {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 2, "positiveDenominator": 1}, "upperClosed": true}, "observation": "response", "projectionClock": "x", "quantifier": "EXISTS-DELTA", "state": "q0", "transition": {"guardAst": {"clock": "x", "interval": {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 2, "positiveDenominator": 1}, "upperClosed": true}, "tag": "RATIONAL-INTERVAL-CONTAINS"}, "id": "t02", "simultaneousUpdates": [], "source": "q0", "target": "q2"}, "typedStore": {"mode": "normal"}}}, {"expected": {"externalDisposition": "SPEC-ERROR", "preserveHypotheses": true, "result": "UNSUPPORTED-SYNTAX"}, "id": "FK-W3-UNKNOWN", "input": {"clockConstraint": {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 1, "positiveDenominator": 1}, "upperClosed": true}, "delta": {"numerator": 0, "positiveDenominator": 1}, "guard": {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 1, "positiveDenominator": 1}, "upperClosed": true}, "observation": "response", "quantifier": "EXISTS-DELTA", "state": "q0", "transition": {"guardAst": {"name": "unsupported", "tag": "CALL"}, "id": "t03", "simultaneousUpdates": [], "source": "q0", "target": "q3"}}}, {"expected": {"merge": false, "reason": "historyProvenance differs"}, "id": "FK-W4-HISTORY", "input": {"frontiers": ["frontier-a", "frontier-b"], "sameH": ["h0"]}}, {"expected": {"merge": false, "reason": "clockConstraint differs"}, "id": "FK-W5-CLOCK", "input": {"clockConstraints": [{"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 1, "positiveDenominator": 1}, "upperClosed": true}, {"lower": {"numerator": 0, "positiveDenominator": 1}, "lowerClosed": true, "upper": {"numerator": 2, "positiveDenominator": 1}, "upperClosed": true}], "clockId": "x", "sameH": ["h0"]}}]`
- 接口绑定：
- 返回关系：会话 Γ 与带版本的历史句柄 η 是不同返回值。S9 保留 Γ.qStatus 及其余会话字段；只有状态为 KNOWN、摘要确认标志为 true、postSummary 已确认三项同时成立才提交 currentSummary。版本不匹配时以 SPEC-ERROR 返回原 η/H/Γ。
  - `IF-PRED-OBS` — 输入：`SessionContext`, `HistoryHandle`, `H`, `measurementUncertainty`, `actionLibrary`；输出：`currentlyValidNonemptyClasses`, `PredictionGapError`；读取：仅读取带版本的 HistoryHandle 和当前会话。；写入：只读；不计费，也不写入 Γ/η。；失败：`PredictionGapError`, `RESOURCE-UNKNOWN`；参数：`RP-HYPOTHESIS-COUNT`, `RP-FRONTIER-STATE-COUNT`, `RP-OBSERVATION-CLASS-COUNT`；时序：使用会话 U 和声明的测量不确定性，不修改二者。；验收：`AC-SYN-PREDICTION`；位置：`future/reference_kernel/prediction.py`
  - `IF-SELECT-ADMIT` — 输入：`A`, `q`, `currentlyValidNonemptyClasses`, `SessionContext`, `HistoryHandle`, `H`；输出：`kind`, `tStar`, `S`, `admitA2A5`；读取：仅读取选择时输入和候选动作。；写入：只读；接口返回后由 S3-SNAP 构造不可变最终 SelectSnapshot。；失败：`PredictionGapError`, `SPEC-ERROR`, `ADMIT-REFUSED`；参数：`RP-ACTION-COUNT`, `RP-OBSERVATION-CLASS-COUNT`, `RP-RESOURCE-MODE`；时序：使用与预测和后续解释相同身份的 U。；验收：`AC-SYN-SELECT`；位置：`future/reference_kernel/selection.py`
  - `IF-EXECUTE-RECORD` — 输入：`SessionContext`, `admitted tStar`；输出：`record`, `effectClass`, `correlationId`；读取：仅读取已接纳的最终快照。；写入：单次计费后写入一条会话日志执行记录。；失败：`CONFIRMED-NOT-SENT`, `UNKNOWN-EFFECT`；参数：`RP-RESOURCE-MODE`, `RP-RETRY-CAP`；时序：执行不得替换选择时快照或 U。；验收：`AC-SYN-TRANSFER`；位置：`future/offline_adapter/execution_record.py`
  - `IF-OBS-INTERPRET` — 输入：`SessionContext`, `executionRecord`, `clocks`, `epsilon`；输出：`Iz`, `effectClass`, `summaryConfirmed`, `postSummary`, `ownershipResult`, `measurementInterval`；读取：仅读取已归属事件证据及声明的时钟和误差来源。；写入：仅返回解释值；不排除 H。；失败：`ERROR`, `INCONCLUSIVE`, `UNKNOWN-EFFECT`；参数：`RP-OBSERVATION-CLASS-COUNT`；时序：保留区间拓扑和 U 身份；无效时序证据返回 ERROR。；验收：`AC-SYN-OBSERVATION`；位置：`future/reference_kernel/interpretation.py`
  - `IF-PREP-RECOVER` — 输入：`SessionContext`, `HistoryHandle`, `tStar`, `record`；输出：`targetConfirmed`, `summaryConfirmed`, `prepError`, `ineligible`, `declaredTarget`, `evidence`, `postSummary`；读取：仅读取会话、历史和已接纳动作记录。；写入：仅返回值；S8/S9 保留 Γ 的唯一写入权。；失败：`UNKNOWN-EFFECT`, `PREP-ERROR`, `CONFIRMED-NOT-SENT`；参数：`RP-RETRY-CAP`, `RP-RESOURCE-MODE`；时序：在重试计数前评估确认，且不改写 U。；验收：`AC-SYN-PREP-RECOVER`；位置：`future/reference_kernel/recovery.py`
  - `IF-HIST-UPDATE` — 输入：`HistoryHandle`, `H`, `tStar`, `qUsedAtSelect`, `classesUsedAtSelect`, `historyVersion`, `valid Iz`, `postSummary`；输出：`HistoryHandlePrime`, `Hprime`, `Stop-Empty`；读取：仅读取选择时快照和完整历史前沿。；写入：仅通过规范化结果写入下一版本的 HistoryHandle。；失败：`Stop-Empty`, `RESOURCE-UNKNOWN`, `CONSERVATIVE-UNKNOWN`；参数：`RP-HYPOTHESIS-COUNT`, `RP-PATH-LENGTH`, `RP-FRONTIER-STATE-COUNT`；时序：携带选择时 U 身份，绝不以效果后的摘要替代 qUsedAtSelect。；验收：`AC-SYN-HISTORY`；位置：`future/reference_kernel/history.py`
  - `IF-EQUIV` — 输入：`SessionContext`, `H`, `HistoryHandle`, `remainingTests`；输出：`established`, `notEstablished`, `unknown`；读取：仅读取有限域状态。；写入：只读；不改变 H 或历史。；失败：`UNKNOWN`, `RESOURCE-UNKNOWN`；参数：`RP-HYPOTHESIS-COUNT`, `RP-PATH-LENGTH`, `RP-ACTION-COUNT`；时序：仅使用声明的有界视界；没有可用单步测试不构成等价证明。；验收：`AC-SYN-EQUIVALENCE`；位置：`future/reference_kernel/equivalence.py`
  - `IF-RESOURCE-STOP` — 输入：`SessionContext`, `H`, `HistoryHandle`, `named645Residuals`, `equivalenceStatus`；输出：`stopClass`, `finalH`, `trace`；读取：仅读取已计费资源、保留历史和具名残余。；写入：仅写入可审计停止追踪。；失败：`Stop-Budget`, `Stop-Error`, `Stop-645`；参数：`RP-RESOURCE-MODE`, `RP-RETRY-CAP`；时序：保持互斥停止顺序，绝不把重试耗尽转换为预算耗尽。；验收：`AC-SYN-RESOURCE-STOP`；位置：`future/reference_kernel/stopping.py`

## 实验接口绑定

- `IF-EXP-SCENE` — 输入：`sceneId`, `configId`, `IUT`, `faultPlan`, `resourceMode`；输出：`sceneRecord`, `unconfirmed`；读取：按受控实验注册表的可见性读取；算法不得读取评价者真值。；写入：仅在可见性声明的评价者存储或算法可见存储中写入具名实验记录。；失败：按注册表失败条件拒绝或分类；不得转换为符合性 PASS/FAIL。；资源：沿用注册表资源口径，不向实验臂赠送记录或成本。；验收：`AC-EXP-SCENE`；位置：`future/experiment/scene.py`
- `IF-EXP-INJECT` — 输入：`sceneId`, `injectionPlan`；输出：`injectionAttempt`, `injectionConfirmed`, `injectionUnconfirmed`；读取：按受控实验注册表的可见性读取；算法不得读取评价者真值。；写入：仅在可见性声明的评价者存储或算法可见存储中写入具名实验记录。；失败：按注册表失败条件拒绝或分类；不得转换为符合性 PASS/FAIL。；资源：沿用注册表资源口径，不向实验臂赠送记录或成本。；验收：`AC-EXP-TRUTH`；位置：`future/experiment/inject.py`
- `IF-EXP-TRUTH` — 输入：`sceneId`, `injectionConfirmed`, `independentGeneratorId`；输出：`truthRecord`, `sharedComponentRisk`；读取：按受控实验注册表的可见性读取；算法不得读取评价者真值。；写入：仅在可见性声明的评价者存储或算法可见存储中写入具名实验记录。；失败：按注册表失败条件拒绝或分类；不得转换为符合性 PASS/FAIL。；资源：沿用注册表资源口径，不向实验臂赠送记录或成本。；验收：`AC-EXP-TRUTH`；位置：`future/experiment/truth.py`
- `IF-EXP-COLLECT` — 输入：`sceneId`, `armId`, `algorithmVisibleRecord`；输出：`observationLog`, `resourceLog`；读取：按受控实验注册表的可见性读取；算法不得读取评价者真值。；写入：仅在可见性声明的评价者存储或算法可见存储中写入具名实验记录。；失败：按注册表失败条件拒绝或分类；不得转换为符合性 PASS/FAIL。；资源：沿用注册表资源口径，不向实验臂赠送记录或成本。；验收：`AC-EXP-CAUSAL`；位置：`future/experiment/collect.py`
- `IF-EXP-RUN` — 输入：`sceneId`, `armId`, `SessionContext`；输出：`runId`, `stopClass`, `traceRef`；读取：按受控实验注册表的可见性读取；算法不得读取评价者真值。；写入：仅在可见性声明的评价者存储或算法可见存储中写入具名实验记录。；失败：按注册表失败条件拒绝或分类；不得转换为符合性 PASS/FAIL。；资源：沿用注册表资源口径，不向实验臂赠送记录或成本。；验收：`AC-EXP-SCENE`；位置：`future/experiment/run.py`
- `IF-EXP-FILTER` — 输入：`runId`, `truthRecord`, `observationLog`, `sceneId`, `attemptId`, `injectionUnconfirmed`；输出：`validityClass`, `filterReason`；读取：按受控实验注册表的可见性读取；算法不得读取评价者真值。；写入：仅在可见性声明的评价者存储或算法可见存储中写入具名实验记录。；失败：按注册表失败条件拒绝或分类；不得转换为符合性 PASS/FAIL。；资源：沿用注册表资源口径，不向实验臂赠送记录或成本。；验收：`AC-EXP-CAUSAL`；位置：`future/experiment/filter.py`
- `IF-EXP-EVAL` — 输入：`runId`, `validityClass`, `denominators`, `truthRecord`, `algorithmResultRef`, `chargedCost`, `sceneId`, `attemptId`；输出：`metricCells`, `attemptDenominator`, `answeredSubsetDenominator`；读取：按受控实验注册表的可见性读取；算法不得读取评价者真值。；写入：仅在可见性声明的评价者存储或算法可见存储中写入具名实验记录。；失败：按注册表失败条件拒绝或分类；不得转换为符合性 PASS/FAIL。；资源：沿用注册表资源口径，不向实验臂赠送记录或成本。；验收：`AC-EXP-DENOMINATOR`；位置：`future/experiment/eval.py`

## 运行参数合同

### `RP-RESOURCE` — 离线缓冲资源界
- 单位／域：bytes and records / `POSITIVE-INTEGER`
- 配置条件：缓冲前必须有具体值；不得从抓包推断。
- 责任范围：离线捕获与重建模块
- 耗尽行为：返回有界资源／解码结果，保留来源且不报告协议 PASS/FAIL。
- 验收：`AC-SYN-TRANSFER`
### `RP-HYPOTHESIS-COUNT` — 假设数量界
- 单位／域：hypotheses / `POSITIVE-INTEGER`
- 配置条件：为声明模型域配置有限 H0 基数。
- 责任范围：有界参考内核
- 耗尽行为：返回保守未知，不排除任何假设。
- 验收：`AC-SYN-PREDICTION`, `AC-SYN-HISTORY`
### `RP-PATH-LENGTH` — 可行路径长度界
- 单位／域：transitions / `POSITIVE-INTEGER`
- 配置条件：每次参考内核调用均声明有界视界。
- 责任范围：有界参考内核
- 耗尽行为：返回未知；超过视界不是不可行性的证明。
- 验收：`AC-SYN-HISTORY`, `AC-SYN-EQUIVALENCE`
### `RP-FRONTIER-STATE-COUNT` — 每假设前沿状态界
- 单位／域：states per hypothesis / `POSITIVE-INTEGER`
- 配置条件：传播前配置有限前沿容量。
- 责任范围：历史传播
- 耗尽行为：保留先前相容历史并标记保守未知。
- 验收：`AC-SYN-PREDICTION`, `AC-SYN-HISTORY`
### `RP-ACTION-COUNT` — 动作库界
- 单位／域：actions / `POSITIVE-INTEGER`
- 配置条件：被接纳的候选动作库有限且有身份。
- 责任范围：选择与等价
- 耗尽行为：拒绝未枚举动作；不得静默评分。
- 验收：`AC-SYN-SELECT`, `AC-SYN-EQUIVALENCE`
### `RP-OBSERVATION-CLASS-COUNT` — 观测类界
- 单位／域：classes / `POSITIVE-INTEGER`
- 配置条件：评分前声明有限当前投影。
- 责任范围：预测、选择与解释
- 耗尽行为：返回具名 GAP 或保守未知，绝不返回零评分。
- 验收：`AC-SYN-PREDICTION`, `AC-SYN-SELECT`, `AC-SYN-OBSERVATION`
### `RP-RETRY-CAP` — 重试上限
- 单位／域：attempts / `POSITIVE-INTEGER`
- 配置条件：重试上限是明确的正整数，且与计费资源模式分开。
- 责任范围：恢复与停止
- 耗尽行为：返回 Stop-Error；不得转换为 Stop-Budget。
- 验收：`AC-SYN-PREP-RECOVER`, `AC-SYN-RESOURCE-STOP`
### `RP-RESOURCE-MODE` — 互斥资源模式
- 单位／域：BUDGET or ROUNDS / `EXCLUSIVE-RESOURCE-MODE`
- 配置条件：每个会话恰选一个声明模式。
- 责任范围：选择、执行、恢复与停止
- 耗尽行为：未接纳动作不得执行或计费；无力承担恢复不同于不具资格。
- 验收：`AC-SYN-SELECT`, `AC-SYN-PREP-RECOVER`, `AC-SYN-RESOURCE-STOP`

## 验收案例

### `AC-SYN-TRANSFER` — 有作用域传输重建见证
- 输入：`CAPTURE-IDENTITY`, `PACKET-REF`, `DATAGRAM-RECORD`, `TRANSFER-RECORD`, `OWNERSHIP-RESULT`, `OBSERVATION-ASSESSMENT`, `HISTORY-HANDLE`, `FINDING-RECORD`
- 工具：`TR-CAPTURE-INTAKE`, `TR-DATAGRAM-REASSEMBLY`, `TR-TRANSFER-RECONSTRUCTION`, `TR-PROTOCOL-EVENT`, `TR-OWNERSHIP`, `TR-OBSERVATION-ASSESSMENT`, `TR-HISTORY-COMPATIBILITY`, `TR-TRACEABLE-FINDING`；模块：`MOD-CAPTURE`, `MOD-REASSEMBLY`, `MOD-TRANSFER`, `MOD-OWNERSHIP`, `MOD-OBSERVATION`；算法接口：`IF-EXECUTE-RECORD`, `IF-OBS-INTERPRET`, `IF-HIST-UPDATE`；实验接口：无
- 输入夹具：`{"caseId": "AC-SYN-TRANSFER", "recordIds": ["CAPTURE-IDENTITY", "PACKET-REF", "DATAGRAM-RECORD", "TRANSFER-RECORD", "OWNERSHIP-RESULT", "OBSERVATION-ASSESSMENT", "HISTORY-HANDLE", "FINDING-RECORD"], "values": {"acceptedBlockBytes": null, "blocks": [1, 2], "captureFormat": {"capturedLength": 64, "interfaceId": 0, "packetNumber": 1, "sectionId": 1}, "captureId": "HC-01", "fieldLayout": {"encodingRule": "ASCII-2", "fieldId": "FIELD-PROTOCOL-VERSION", "ordinal": 2, "protocolFile": "LCI", "sourceRequirementId": "CRS-M1-00283", "widthBits": 16}, "gaps": [], "ipFragments": {"coverageRanges": [[0, 15]], "datagramLengthBytes": 16, "fragmentOffsets": [0, 8], "fragments": [{"bytesHex": "0001020304050607", "offset": 0}, {"bytesHex": "08090a0b0c0d0e0f", "offset": 8}], "gapPolicy": "GAPPED", "overlapConflict": false, "overlapPolicy": "IDENTICAL-ONLY"}, "labelBoundary": {"annotation": "exploratory", "independentTruth": "not-claimed", "wireOutcome": "observed"}, "noResponseFixture": {"cancelled": false, "deadline": 5, "earliestElapsed": 6, "expectedDisposition": "FAIL-NO-RESPONSE", "requestId": "REQUEST-A", "upperClosed": true}, "optionState": "DEFAULTED", "ownershipFixture": {"expectedOwner": "REQUEST-B", "key": "k1", "ownershipEvents": [{"id": "REQUEST-A", "key": "k1", "kind": "REQUEST", "sequence": 1}, {"id": "REQUEST-B", "key": "k1", "kind": "REQUEST", "sequence": 2}, {"id": "RESPONSE-B", "key": "k1", "kind": "RESPONSE", "sequence": 3}], "policy": "MOST-RECENT", "responseId": "RESPONSE-B"}, "packetRefs": [1, 2, 3], "terminal": {"block": 2, "nextZeroBlock": null, "nextZeroPayloadBytes": null, "payloadBytes": 0}, "tid": {"client": 12000, "server": 69}}}`
- 预期夹具：`{"outcome": "CONTRACT-EXPECTED", "statement": "A provenance-preserving transfer candidate and typed event retain gaps, retransmissions and option evidence.", "values": {"datagramStatus": "COMPLETE", "orderedBlocks": [1, 2], "status": "COMPLETE", "terminalConfirmed": true}}`
- 预期：保留来源的传输候选和带类型事件保留缺口、重传与选项证据。
- 禁止：不得产生协议 PASS/FAIL、根因标签或虚构的已接受选项。；路径：`protocolVerdictWithoutMeasurement`, `independentTruthFromExploratoryInput`
- 负例：`[{"expectedRejection": "RC-TRANSFER-TERMINAL at inputFixture.values.terminal", "id": "AC-SYN-TRANSFER-NEG", "mutation": "remove terminal evidence", "operation": "remove", "path": ["inputFixture", "values", "terminal"]}]`
- 依据：针对声明离线首轮切片的合成规格见证；它不是历史真值或解析器执行。；见证：`SPECIFICATION-WITNESS`；运行：`NOT-EXECUTED`
### `AC-SYN-PREDICTION` — 有限预测边界见证
- 输入：`HISTORY-HANDLE`, `OBSERVATION-ASSESSMENT`
- 工具：`TR-HISTORY-COMPATIBILITY`；模块：`MOD-OBSERVATION`；算法接口：`IF-PRED-OBS`；实验接口：无
- 输入夹具：`{"caseId": "AC-SYN-PREDICTION", "recordIds": ["HISTORY-HANDLE", "OBSERVATION-ASSESSMENT"], "values": {"H": ["h0", "h1"], "actionId": "test-a", "eligibleActions": ["test-a"], "frontiers": [{"hypothesisId": "h0", "state": "q0"}, {"hypothesisId": "h1", "state": "q1"}], "model": {"transitions": [{"actionId": "test-a", "observationClass": "response-a", "source": "q0", "target": "q0"}, {"actionId": "test-a", "observationClass": "response-b", "source": "q1", "target": "q1"}]}, "resource": {"mode": "ROUNDS", "remaining": 1}}}`
- 预期夹具：`{"outcome": "CONTRACT-EXPECTED", "statement": "A finite current projection is tagged OK or GAP before any TEST score is read.", "values": {"classes": ["response-a", "response-b"], "predictionStatus": "OK"}}`
- 预期：在读取任何 TEST 评分前，将有限当前投影标记为 OK 或 GAP。
- 禁止：空投影不得记为零分，也不得写入历史。；路径：`protocolVerdictWithoutMeasurement`, `independentTruthFromExploratoryInput`
- 负例：`[{"expectedRejection": "RC-PREDICTION-NONEMPTY at expectedOutputFixture.values.classes", "id": "AC-SYN-PREDICTION-NEG", "mutation": "replace classes with an empty list while status is OK", "operation": "replace", "path": ["expectedOutputFixture", "values", "classes"], "value": []}]`
- 依据：有限当前类传播的合成规格见证。；见证：`SPECIFICATION-WITNESS`；运行：`NOT-EXECUTED`
### `AC-SYN-SELECT` — 接纳动作选择见证
- 输入：`HISTORY-HANDLE`, `OBSERVATION-ASSESSMENT`
- 工具：`TR-HISTORY-COMPATIBILITY`；模块：`MOD-OBSERVATION`；算法接口：`IF-SELECT-ADMIT`；实验接口：无
- 输入夹具：`{"caseId": "AC-SYN-SELECT", "recordIds": ["HISTORY-HANDLE", "OBSERVATION-ASSESSMENT"], "values": {"H": ["h0", "h1"], "actions": [{"classesByHypothesis": {"h0": "response-a", "h1": "response-b"}, "cost": 1, "id": "test-b", "kind": "TEST", "worstClass": 1}, {"classesByHypothesis": {"h0": "response-a", "h1": "response-b"}, "cost": 1, "id": "test-a", "kind": "TEST", "worstClass": 1}], "distinguishingClasses": ["response-a", "response-b"], "eligibleActions": ["test-a", "test-b"], "resource": {"mode": "ROUNDS", "remaining": 1}}}`
- 预期夹具：`{"outcome": "CONTRACT-EXPECTED", "statement": "Only affordable distinguishing TEST actions are minimax-scored, then tie-broken by cost and stable action ID.", "values": {"selectedActionId": "test-a", "tieBreak": ["worstClass", "cost", "stable-id"]}}`
- 预期：仅对可负担且有区分力的 TEST 作 minimax 评分，然后按成本和稳定 action ID 决胜。
- 禁止：无信息 TEST 不得成为 A2，Prep/Recover 不得按 TEST 评分。；路径：`protocolVerdictWithoutMeasurement`, `independentTruthFromExploratoryInput`
- 负例：`[{"expectedRejection": "RC-SELECT-STABLE-ID at expectedOutputFixture.values.selectedActionId", "id": "AC-SYN-SELECT-NEG", "mutation": "select test-b with equal score and cost", "operation": "replace", "path": ["expectedOutputFixture", "values", "selectedActionId"], "value": "test-b"}]`
- 依据：声明单步决策表的合成规格见证。；见证：`SPECIFICATION-WITNESS`；运行：`NOT-EXECUTED`
### `AC-SYN-OBSERVATION` — 四值时序解释见证
- 输入：`OWNERSHIP-RESULT`, `PROTOCOL-EVENT`, `OBSERVATION-ASSESSMENT`
- 工具：`TR-OBSERVATION-ASSESSMENT`；模块：`MOD-OBSERVATION`；算法接口：`IF-OBS-INTERPRET`；实验接口：无
- 输入夹具：`{"caseId": "AC-SYN-OBSERVATION", "recordIds": ["OWNERSHIP-RESULT", "PROTOCOL-EVENT", "OBSERVATION-ASSESSMENT"], "values": {"clockValid": true, "interval": {"lower": 5.0, "lowerClosed": true, "upper": 5.2, "upperClosed": true}, "matrixTimingFixture": {"clockValid": true, "expectedVerdict": "INCONCLUSIVE", "interval": {"lower": 5.0, "lowerClosed": true, "upper": 5.2, "upperClosed": true}, "requirementWindow": {"lower": 4.0, "lowerClosed": true, "upper": 5.1, "upperClosed": true}}, "requirementWindow": {"lower": 4.0, "lowerClosed": true, "upper": 5.1, "upperClosed": true}}}`
- 预期夹具：`{"outcome": "CONTRACT-EXPECTED", "statement": "Valid intervals produce PASS, FAIL or INCONCLUSIVE; invalid timing evidence produces ERROR.", "values": {"verdict": "INCONCLUSIVE"}}`
- 预期：有效区间产生 PASS、FAIL 或 INCONCLUSIVE；无效时序证据产生 ERROR。
- 禁止：不得将 ERROR 或 INCONCLUSIVE 降级为 FAIL。；路径：`protocolVerdictWithoutMeasurement`, `independentTruthFromExploratoryInput`
- 负例：`[{"expectedRejection": "RC-VERDICT-WHOLE-INTERVAL at expectedOutputFixture.values.verdict", "id": "AC-SYN-OBSERVATION-NEG", "mutation": "change verdict to PASS for a boundary-overlapping interval", "operation": "replace", "path": ["expectedOutputFixture", "values", "verdict"], "value": "PASS"}]`
- 依据：T5 区间和所有权前提的合成规格见证。；见证：`SPECIFICATION-WITNESS`；运行：`NOT-EXECUTED`
### `AC-SYN-PREP-RECOVER` — 确认恢复交接见证
- 输入：`HISTORY-HANDLE`, `OBSERVATION-ASSESSMENT`
- 工具：`TR-HISTORY-COMPATIBILITY`；模块：`MOD-OBSERVATION`；算法接口：`IF-PREP-RECOVER`；实验接口：无
- 输入夹具：`{"caseId": "AC-SYN-PREP-RECOVER", "recordIds": ["HISTORY-HANDLE", "OBSERVATION-ASSESSMENT"], "values": {"actionKind": "PREP", "postSummary": "q1", "summaryConfirmed": true, "targetConfirmed": true}}`
- 预期夹具：`{"outcome": "CONTRACT-EXPECTED", "statement": "Prep/Recover returns confirmation fields; only S8/S9 may commit known state or successor summary.", "values": {"commitSummary": "q1", "historyVersion": 1}}`
- 预期：Prep/Recover 返回确认字段；只有 S8/S9 可提交已知状态或后继摘要。
- 禁止：未确认后继不得保留陈旧已知状态或直接写入 Γ。；路径：`protocolVerdictWithoutMeasurement`, `independentTruthFromExploratoryInput`
- 负例：`[{"expectedRejection": "RC-SUMMARY-CONFIRMATION at inputFixture.values.summaryConfirmed", "id": "AC-SYN-PREP-RECOVER-NEG", "mutation": "set summaryConfirmed false while committing q1", "operation": "replace", "path": ["inputFixture", "values", "summaryConfirmed"], "value": false}]`
- 依据：S8/S9 所有权边界的合成规格见证。；见证：`SPECIFICATION-WITNESS`；运行：`NOT-EXECUTED`
### `AC-SYN-HISTORY` — 完整历史更新见证
- 输入：`HISTORY-HANDLE`, `OBSERVATION-ASSESSMENT`
- 工具：`TR-HISTORY-COMPATIBILITY`；模块：`MOD-OBSERVATION`；算法接口：`IF-HIST-UPDATE`；实验接口：无
- 输入夹具：`{"caseId": "AC-SYN-HISTORY", "recordIds": ["HISTORY-HANDLE", "OBSERVATION-ASSESSMENT"], "values": {"compatibleObservationHypotheses": [], "history": {"H": ["h0"], "compatibleStateByHypothesis": {"h0": "frontier-syn-0"}, "statusByHypothesis": {"h0": "KNOWN"}, "version": 0}, "summaryConfirmed": true}}`
- 预期夹具：`{"outcome": "CONTRACT-EXPECTED", "statement": "A normalized valid outcome advances a versioned whole-history frontier without resurrecting excluded hypotheses.", "values": {"history": {"H": [], "compatibleStateByHypothesis": {}, "statusByHypothesis": {}, "version": 1}, "stop": "Stop-Empty"}}`
- 预期：规范化有效结果推进带版本完整历史前沿，且不复活已排除假设。
- 禁止：H prime 不得替换为 Iz，资源耗尽不得视为不相容。；路径：`protocolVerdictWithoutMeasurement`, `independentTruthFromExploratoryInput`
- 负例：`[{"expectedRejection": "RC-HISTORY-NO-RESURRECTION at expectedOutputFixture.values.history.H", "id": "AC-SYN-HISTORY-NEG", "mutation": "return the old h0 after the empty intersection", "operation": "replace", "path": ["expectedOutputFixture", "values", "history", "H"], "value": ["h0"]}]`
- 依据：保守历史传播的合成规格见证。；见证：`SPECIFICATION-WITNESS`；运行：`NOT-EXECUTED`
### `AC-SYN-EQUIVALENCE` — 有界等价弃权见证
- 输入：`HISTORY-HANDLE`
- 工具：`TR-HISTORY-COMPATIBILITY`；模块：`MOD-OBSERVATION`；算法接口：`IF-EQUIV`；实验接口：无
- 输入夹具：`{"caseId": "AC-SYN-EQUIVALENCE", "recordIds": ["HISTORY-HANDLE"], "values": {"H": ["h0", "h1"], "finiteDomainProof": "absent"}}`
- 预期夹具：`{"outcome": "CONTRACT-EXPECTED", "statement": "An established result requires declared finite-domain proof evidence; otherwise the result is unknown or notEstablished.", "values": {"result": "unknown"}}`
- 预期：established 需要声明有限域的证明依据；否则结果为 unknown 或 notEstablished。
- 禁止：没有即时可区分 TEST 不得视为等价证明。；路径：`protocolVerdictWithoutMeasurement`, `independentTruthFromExploratoryInput`
- 负例：`[{"expectedRejection": "RC-EQUIV-EVIDENCE at expectedOutputFixture.values.result", "id": "AC-SYN-EQUIVALENCE-NEG", "mutation": "return established without finite-domain proof", "operation": "replace", "path": ["expectedOutputFixture", "values", "result"], "value": "established"}]`
- 依据：有界等价语义的合成规格见证。；见证：`SPECIFICATION-WITNESS`；运行：`NOT-EXECUTED`
### `AC-SYN-RESOURCE-STOP` — 资源与停止顺序见证
- 输入：`HISTORY-HANDLE`, `FINDING-RECORD`
- 工具：`TR-HISTORY-COMPATIBILITY`, `TR-TRACEABLE-FINDING`；模块：`MOD-OBSERVATION`；算法接口：`IF-RESOURCE-STOP`；实验接口：无
- 输入夹具：`{"caseId": "AC-SYN-RESOURCE-STOP", "recordIds": ["HISTORY-HANDLE", "FINDING-RECORD"], "values": {"attemptsIssued": 1, "consecutiveErrorCount": 1, "lastOutcome": "ADAPTER-ERROR", "mode": "ROUNDS", "remaining": 0, "retryCap": 1}}`
- 预期夹具：`{"outcome": "CONTRACT-EXPECTED", "statement": "Exclusive stop ordering retains named 645 residuals and reports retry exhaustion as Stop-Error.", "values": {"charges": 1, "stop": "Stop-Error"}}`
- 预期：互斥停止顺序保留具名 645 残余，并将重试耗尽报告为 Stop-Error。
- 禁止：重试耗尽不得成为 Stop-Budget，normal 单例不得成为协议 PASS。；路径：`protocolVerdictWithoutMeasurement`, `independentTruthFromExploratoryInput`
- 负例：`[{"expectedRejection": "RC-RESOURCE-ONCE at expectedOutputFixture.values.charges", "id": "AC-SYN-RESOURCE-STOP-NEG", "mutation": "charge the single issued attempt twice", "operation": "replace", "path": ["expectedOutputFixture", "values", "charges"], "value": 2}]`
- 依据：资源和停止合同的合成规格见证。；见证：`SPECIFICATION-WITNESS`；运行：`NOT-EXECUTED`
### `AC-SYN-INTEGRITY` — 有界完整性规格见证
- 输入：`TRANSFER-RECORD`
- 工具：`TR-PROTOCOL-EVENT`；模块：`MOD-TRANSFER`；算法接口：`IF-OBS-INTERPRET`；实验接口：无
- 输入夹具：`{"caseId": "AC-SYN-INTEGRITY", "recordIds": ["TRANSFER-RECORD"], "values": {"requirementId": "CRS-M1-00076", "runtimeEvidence": "NOT-ESTABLISHED"}}`
- 预期夹具：`{"outcome": "CONTRACT-EXPECTED", "statement": "CRC-bearing inputs retain source parameters and yield NOT-EVALUATED until implementation, configuration and execution evidence exist.", "values": {"judgment": "NOT-EVALUATED"}}`
- 预期：产生声明的类型化合同结果并保留证据边界。
- 禁止：不得伪造运行结果、独立真值或符合性判定。；路径：`runtimeResultClaim`, `truthLeakage`
- 负例：`[{"expectedRejection": "RC-INTEGRITY-RUNTIME at expectedOutputFixture.values.judgment", "id": "AC-SYN-INTEGRITY-NEG", "mutation": "return PASS without qualified runtime evidence", "operation": "replace", "path": ["expectedOutputFixture", "values", "judgment"], "value": "PASS"}]`
- 依据：受控规格见证；未执行解析器、求解器、IUT 或实验。；见证：`SPECIFICATION-WITNESS`；运行：`NOT-EXECUTED`
### `AC-EXP-SCENE` — 可运行场景身份见证
- 输入：`INTAKE-METADATA`
- 工具：`TR-CAPTURE-INTAKE`；模块：`MOD-CAPTURE`；算法接口：`IF-EXECUTE-RECORD`；实验接口：`IF-EXP-SCENE`, `IF-EXP-RUN`
- 输入夹具：`{"caseId": "AC-EXP-SCENE", "recordIds": ["INTAKE-METADATA"], "values": {"algorithmVisibleFields": ["rawRecord"], "armId": "CL-T", "configurationId": "cfg-001", "faultPlan": "NONE", "iutId": "iut-001", "resetId": "reset-001", "resourceMode": "ROUNDS", "sceneId": "scene-001", "sessionContext": {"sessionId": "session-001", "state": "RESET"}, "truthSource": "evaluator-only"}}`
- 预期夹具：`{"outcome": "CONTRACT-EXPECTED", "statement": "A runnable scene has stable scene, configuration, IUT and resource identities.", "values": {"executionStatus": "NOT-EXECUTED", "registration": "ACCEPTED"}}`
- 预期：产生声明的类型化合同结果并保留证据边界。
- 禁止：不得伪造运行结果、独立真值或符合性判定。；路径：`runtimeResultClaim`, `truthLeakage`
- 负例：`[{"expectedRejection": "RC-SCENE-RESET-ID at inputFixture.values.resetId", "id": "AC-EXP-SCENE-NEG", "mutation": "remove resetId", "operation": "remove", "path": ["inputFixture", "values", "resetId"]}]`
- 依据：受控规格见证；未执行解析器、求解器、IUT 或实验。；见证：`SPECIFICATION-WITNESS`；运行：`NOT-EXECUTED`
### `AC-EXP-TRUTH` — 独立真值边界见证
- 输入：`FINDING-RECORD`
- 工具：`TR-TRACEABLE-FINDING`；模块：`MOD-OBSERVATION`；算法接口：`IF-OBS-INTERPRET`；实验接口：`IF-EXP-INJECT`, `IF-EXP-TRUTH`
- 输入夹具：`{"caseId": "AC-EXP-TRUTH", "recordIds": ["FINDING-RECORD"], "values": {"algorithmVisible": false, "generatorId": "truth-gen-001", "injectionConfirmed": true, "injectionId": "inj-001"}}`
- 预期夹具：`{"outcome": "CONTRACT-EXPECTED", "statement": "Only confirmed injection plus an independent generator creates truth, with shared-component risk named.", "values": {"sharedComponentRisk": "DECLARED", "truthStatus": "CONFIRMED"}}`
- 预期：产生声明的类型化合同结果并保留证据边界。
- 禁止：不得伪造运行结果、独立真值或符合性判定。；路径：`runtimeResultClaim`, `truthLeakage`
- 负例：`[{"expectedRejection": "RC-TRUTH-ISOLATION at inputFixture.values.algorithmVisible", "id": "AC-EXP-TRUTH-NEG", "mutation": "set algorithmVisible true", "operation": "replace", "path": ["inputFixture", "values", "algorithmVisible"], "value": true}]`
- 依据：受控规格见证；未执行解析器、求解器、IUT 或实验。；见证：`SPECIFICATION-WITNESS`；运行：`NOT-EXECUTED`
### `AC-EXP-CAUSAL` — 因果采集与实验臂公平性见证
- 输入：`OBSERVATION-ASSESSMENT`
- 工具：`TR-OBSERVATION-ASSESSMENT`；模块：`MOD-OBSERVATION`；算法接口：`IF-EXECUTE-RECORD`；实验接口：`IF-EXP-COLLECT`, `IF-EXP-FILTER`
- 输入夹具：`{"caseId": "AC-EXP-CAUSAL", "recordIds": ["OBSERVATION-ASSESSMENT"], "values": {"arm": "CL-TA", "costVector": {"actions": 1, "bytes": 64}, "visiblePrefix": ["trigger", "response"]}}`
- 预期夹具：`{"outcome": "CONTRACT-EXPECTED", "statement": "Each arm sees only its causal prefix and pays the same declared cost vector.", "values": {"causalVisibility": "PREFIX-ONLY", "costComparable": true}}`
- 预期：产生声明的类型化合同结果并保留证据边界。
- 禁止：不得伪造运行结果、独立真值或符合性判定。；路径：`runtimeResultClaim`, `truthLeakage`
- 负例：`[{"expectedRejection": "RC-CAUSAL-PREFIX at inputFixture.values.visiblePrefix", "id": "AC-EXP-CAUSAL-NEG", "mutation": "add evaluator truth to visiblePrefix", "operation": "replace", "path": ["inputFixture", "values", "visiblePrefix"], "value": ["trigger", "evaluator truth"]}]`
- 依据：受控规格见证；未执行解析器、求解器、IUT 或实验。；见证：`SPECIFICATION-WITNESS`；运行：`NOT-EXECUTED`
### `AC-EXP-DENOMINATOR` — 评价分母见证
- 输入：`FINDING-RECORD`
- 工具：`TR-TRACEABLE-FINDING`；模块：`MOD-OBSERVATION`；算法接口：`IF-RESOURCE-STOP`；实验接口：`IF-EXP-EVAL`
- 输入夹具：`{"caseId": "AC-EXP-DENOMINATOR", "recordIds": ["FINDING-RECORD"], "values": {"attempts": ["PASS", "INCONCLUSIVE", "ERROR", "UNCONFIRMED"]}}`
- 预期夹具：`{"outcome": "CONTRACT-EXPECTED", "statement": "Attempt and answered-subset denominators retain abstain, invalid, equivalent and unconfirmed membership.", "values": {"answeredDenominator": 1, "attemptDenominator": 4}}`
- 预期：产生声明的类型化合同结果并保留证据边界。
- 禁止：不得伪造运行结果、独立真值或符合性判定。；路径：`runtimeResultClaim`, `truthLeakage`
- 负例：`[{"expectedRejection": "RC-DENOMINATOR-ATTEMPTS at expectedOutputFixture.values.attemptDenominator", "id": "AC-EXP-DENOMINATOR-NEG", "mutation": "drop abstentions from the attempt denominator", "operation": "replace", "path": ["expectedOutputFixture", "values", "attemptDenominator"], "value": 1}]`
- 依据：受控规格见证；未执行解析器、求解器、IUT 或实验。；见证：`SPECIFICATION-WITNESS`；运行：`NOT-EXECUTED`

## 跨路径验收矩阵

| ID | 类别 | 正向输入 | 预期输出 | 负向变异 | 预期拒绝 |
|---|---|---|---|---|---|
| `AM-IDENTITY` | 受控类别：corpus identity | 受控清单条目与唯一的外部盘点文件身份；不声称捕获文件已进入 Git 索引。 | 仅允许探索性接入并保留原始身份。 | 增删条目、改散列/长度/路径、链接别名或重复身份。 | 生产入口必须以具名诊断拒绝，且不得发布派生视图。；案例 `AC-SYN-TRANSFER`；测试 `案例关系`；向量 `{"byteCount": 214877828, "captureId": "HC-01", "relativePath": "OHMS数据加载CPM_L1_ACT40-FCPA-38AH,报fail,260820.pcapng", "resolvedFileIdentity": "externally-inventoried-regular-file", "sha256": "0e9c160dc28f59502730e7bd860a69d095ed32671d761843bbadb18199cf103c"}` |
| `AM-LABEL` | 受控类别：label boundary | 线缆记录与操作员注释、评价真值严格分离。 | 算法仅接收协议可见字段。 | 把文件名结果或评价标签复制进算法记录。 | 生产入口必须以具名诊断拒绝，且不得发布派生视图。；案例 `AC-SYN-TRANSFER`；测试 `案例关系`；向量 `{"annotation": "exploratory", "independentTruth": "not-claimed", "wireOutcome": "observed"}` |
| `AM-FORMAT` | 受控类别：capture format | 含 section、interface、ticks、caplen 边界的捕获记录。 | 输出保留 section/interface 身份的类型化数据包。 | 截断块、未知链路类型、缺接口或混淆局部接口编号。 | 生产入口必须以具名诊断拒绝，且不得发布派生视图。；案例 `AC-SYN-TRANSFER`；测试 `案例关系`；向量 `{"capturedLength": 64, "interfaceId": 0, "packetNumber": 1, "sectionId": 1}` |
| `AM-IP` | 受控类别：IP reassembly | 带 PacketRef 来源的完整有限分片集。 | 输出完整数据报或 GAPPED/CONFLICT。 | 把缺片、乱序、重叠或 epoch 复用误作完整 UDP。 | 生产入口必须以具名诊断拒绝，且不得发布派生视图。；案例 `AC-SYN-TRANSFER`；测试 `案例关系`；向量 `{"coverageRanges": [[0, 15]], "datagramLengthBytes": 16, "fragmentOffsets": [0, 8], "fragments": [{"bytesHex": "0001020304050607", "offset": 0}, {"bytesHex": "08090a0b0c0d0e0f", "offset": 8}], "gapPolicy": "GAPPED", "overlapConflict": false, "overlapPolicy": "IDENTICAL-ONLY"}` |
| `AM-TFTP` | 受控类别：TFTP reconstruction | 动态 TID、已接受/默认选项及联合终块条件。 | 保留重传、回绕上限和终止证据的传输记录。 | 盲目去重、固定 TID、虚构选项或错误终块。 | 生产入口必须以具名诊断拒绝，且不得发布派生视图。；案例 `AC-SYN-TRANSFER`；测试 `案例关系`；向量 `{"blockNumbers": [1, 2], "optionState": "DEFAULTED", "terminalBlock": 2, "tidPair": [12000, 69]}` |
| `AM-FIELDS` | 受控类别：field contracts | 带计数和合法扩展的类型化条件字段。 | 接受并保留扩展及来源。 | ASCII/整数互换、计数不符、哨兵误用或未知枚举。 | 生产入口必须以具名诊断拒绝，且不得发布派生视图。；案例 `AC-SYN-TRANSFER`；测试 `案例关系`；向量 `{"encodingRule": "ASCII-2", "fieldId": "FIELD-PROTOCOL-VERSION", "ordinal": 2, "protocolFile": "LCI", "sourceRequirementId": "CRS-M1-00283", "widthBits": 16}` |
| `AM-OWNERSHIP` | 受控类别：matching and no response | 含顺序、取消、替代关系的活动请求实例。 | 唯一归属响应或明确歧义/未完成观测期。 | 复用响应、错键、忽略取消或把捕获结束当超时。 | 生产入口必须以具名诊断拒绝，且不得发布派生视图。；案例 `AC-SYN-OBSERVATION, AC-SYN-TRANSFER`；测试 `案例关系`；向量 `{"deadline": 5, "earliestElapsed": 6, "expectedOwner": "REQUEST-B", "key": "k1", "policy": "MOST-RECENT", "responseId": "RESPONSE-B"}` |
| `AM-TIMING` | 受控类别：timing and U | 区间、拓扑、时钟链、误差界及不可变 U 身份。 | 按 T5 输出四值判定和无响应边界。 | 改成点估计、默认零误差或更换 U 提交。 | 生产入口必须以具名诊断拒绝，且不得发布派生视图。；案例 `AC-SYN-OBSERVATION`；测试 `案例关系`；向量 `{"boundaryClosure": "UPPER-CLOSED", "clockValidity": true, "measurementInterval": {"lower": 5.0, "lowerClosed": true, "upper": 5.2, "upperClosed": true}, "requirementWindow": {"lower": 4.0, "lowerClosed": true, "upper": 5.1, "upperClosed": true}}` |
| `AM-ADMIT` | 受控类别：prediction and admission | 有限当前类与合格且可负担动作。 | TEST 按 minimax/成本/稳定 ID 选择，或进入合法 Prep/Recover/A2-A5。 | 把 GAP 计零、把无信息 TEST 当 A2 或给 Prep 打分。 | 生产入口必须以具名诊断拒绝，且不得发布派生视图。；案例 `AC-SYN-SELECT`；测试 `案例关系`；向量 `{"H": ["h0", "h1"], "distinguishingClasses": ["response-a", "response-b"], "eligibleActions": ["test-a", "test-b"], "resource": {"mode": "ROUNDS", "remaining": 1}}` |
| `AM-HISTORY` | 受控类别：history update | 带版本的全历史前沿和规范化有效结果。 | H' 等于 H 与 Iz 交集且不复活。 | 用 Iz 替换 H、丢历史相关或把限额当不相容。 | 生产入口必须以具名诊断拒绝，且不得发布派生视图。；案例 `AC-SYN-HISTORY`；测试 `案例关系`；向量 `{"H": ["h0"], "compatibleObservationHypotheses": [], "historyVersion": 0, "summaryConfirmed": true}` |
| `AM-STATE` | 受控类别：state and return | 含 S8/S9 确认字段的完整 Outcome/Resolution。 | 重试/提交/停止保留已采用上下文和写入所有权。 | 提交陈旧摘要、缺确认或返回未定义上下文。 | 生产入口必须以具名诊断拒绝，且不得发布派生视图。；案例 `AC-SYN-HISTORY`；测试 `案例关系`；向量 `{"interfaceId": "IF-RESOURCE-STOP", "internalResult": "EMPTY-HISTORY", "returnRecord": "StopResult", "sideEffects": "PRESERVE"}` |
| `AM-RESOURCE` | 受控类别：resource accounting | 互斥 BUDGET/ROUNDS 及正有限成本/上限。 | 每次已发动作只计费一次并具名耗尽。 | 拒绝动作重复计费或接受 NaN/负数/非整数。 | 生产入口必须以具名诊断拒绝，且不得发布派生视图。；案例 `AC-SYN-RESOURCE-STOP`；测试 `案例关系`；向量 `{"attemptsIssued": 1, "remaining": 0, "resourceMode": "ROUNDS", "retryCount": 1}` |
| `AM-EXPERIMENT` | 受控类别：experiment boundary | 已登记场景、已确认注入和仅评价者可见的独立真值。 | 形成因果四臂记录及显式有效性分母。 | 泄漏真值、未确认即标真、隐藏成本或把探索抓包当留出集。 | 生产入口必须以具名诊断拒绝，且不得发布派生视图。；案例 `AC-EXP-SCENE`；测试 `案例关系`；向量 `{"algorithmVisibleFields": ["rawRecord"], "armId": "CL-T", "resetId": "reset-001", "truthSource": "evaluator-only"}` |
| `AM-DRIFT` | 受控类别：controlled drift | 同一已验证快照上的权威对象和生成视图。 | 检查器与生成器一致，失败时不发布。 | 删除关系、伪造引用、仅刷新计数/散列或保留陈旧视图。 | 生产入口必须以具名诊断拒绝，且不得发布派生视图。；案例 ``；测试 `test_review_generator_refuses_invalid_authority_and_detects_stale_view`；向量 `{"failurePreservesOldView": true, "publicationMode": "--write", "sourceMutation": "remove protocolInputDispositions[0].rationaleZh", "viewMarker": "preserve this failed-publication marker\n"}` |

有限验收关系区分请求实例的活动、完成、取消、替代及歧义状态。歧义响应属于 ERROR 前提，不证明无响应；正常完成不是取消。BUDGET 按费用余额准入，ROUNDS 按剩余执行次数准入，再仅对 TEST 评分。从分片字节推导 IP 覆盖与冲突，依据绑定的 CRS fieldConstraint 核验字段位宽与编码；TFTP 终块须有有效块长及必要的后继零长度块证据。Prep／Recover 不参与 TEST 评分。
归属与无响应消费同一事件回放：旧实例一旦歧义即退出可配对集合；之后同键的新请求以新身份独立进入。UNKNOWN-EFFECT 将声明受影响的 HistoryHandle 成员标记为 CONSERVATIVE-UNKNOWN，并由接口结果及 S9 etaPrime 保留供下一轮读取；未受影响成员状态保持不变。单纯计算限额不会自行改变会话 qStatus 或收取重试费用。

## 首批实验场景

- `SC-NORMAL-UPLOAD` — 受控场景：normal single upload；服务 `UPLOAD`；可控动作 normal operation；依赖 `EXP-PREQ-IUT, EXP-PREQ-REGISTRATION`；验收 `AC-EXP-SCENE, AC-EXP-CAUSAL`；向量 `{"eventSequence": ["LUI", "LUR", "DATA", "LUS"], "expectedBoundary": "normal completion only after declared terminal status", "sessionId": "s1", "terminalStatus": "COMPLETE"}`；真值 confirmed controlled generator；复位 reset IUT/session/budget；计时 qualified monotonic clock and declared epsilon；资源 same declared cost vector and one exclusive resource mode across arms；阻塞于 interactive IUT、confirmatory registration；`NOT-EXECUTED`
- `SC-WAIT-CONTINUE` — 受控场景：WAIT then continue；服务 `UPLOAD`；可控动作 controlled WAIT followed by continuation；依赖 `EXP-PREQ-IUT, EXP-PREQ-REGISTRATION`；验收 `AC-EXP-SCENE, AC-EXP-CAUSAL`；向量 `{"eventSequence": ["WAIT", "WAIT-END", "CONTINUE"], "expectedBoundary": "WAIT preserves the active obligation until continuation", "obligationId": "o1", "waitActive": true}`；真值 confirmed event script；复位 reset loader state and session；计时 qualified monotonic clock and declared epsilon；资源 same declared cost vector and one exclusive resource mode across arms；阻塞于 interactive IUT、confirmatory registration；`NOT-EXECUTED`
- `SC-NO-RESPONSE` — 受控场景：request without matching response；服务 `INFORMATION`；可控动作 controlled suppression with complete observation horizon；依赖 `EXP-PREQ-IUT, EXP-PREQ-REGISTRATION`；验收 `AC-EXP-SCENE, AC-EXP-CAUSAL`；向量 `{"cancelled": false, "deadline": 5, "earliestElapsed": 6, "eventSequence": ["TRIGGER", "SILENCE-HORIZON"], "expectedBoundary": "no-response only when earliest admissible elapsed horizon exceeds U", "triggerAt": 0, "upperClosed": true}`；真值 confirmed suppression controller；复位 reset endpoint and capture horizon；计时 qualified clock, open/closed deadline recorded；资源 same declared cost vector and one exclusive resource mode across arms；阻塞于 interactive IUT、confirmatory registration；`NOT-EXECUTED`
- `SC-ABORT` — 受控场景：explicit abort；服务 `UPLOAD`；可控动作 confirmed abort event；依赖 `EXP-PREQ-IUT, EXP-PREQ-REGISTRATION`；验收 `AC-EXP-SCENE, AC-EXP-CAUSAL`；向量 `{"cancelled": true, "eventSequence": ["TRIGGER", "ABORT"], "expectedBoundary": "abort cancels the active obligation", "obligationId": "o2"}`；真值 independent controller log；复位 reset transfer and session；计时 qualified event order and clocks；资源 same declared cost vector and one exclusive resource mode across arms；阻塞于 interactive IUT、confirmatory registration；`NOT-EXECUTED`
- `SC-INVALID-OBS` — 受控场景：invalid or missing observation；服务 `INFORMATION`；可控动作 capture/clock evidence deliberately incomplete；依赖 `EXP-PREQ-IUT, EXP-PREQ-REGISTRATION`；验收 `AC-EXP-SCENE, AC-EXP-CAUSAL`；向量 `{"clockValid": false, "eventSequence": ["TRIGGER", "INVALID-TIMESTAMP"], "expectedBoundary": "invalid timestamp chain yields ERROR", "expectedVerdict": "ERROR"}`；真值 evaluator construction record；复位 fresh capture and session；计时 invalid chain remains ERROR；资源 same declared cost vector and one exclusive resource mode across arms；阻塞于 interactive IUT、confirmatory registration；`NOT-EXECUTED`
- `SC-SAME-KEY` — 受控场景：multiple same-key requests；服务 `INFORMATION`；可控动作 controlled overlapping requests；依赖 `EXP-PREQ-IUT, EXP-PREQ-REGISTRATION`；验收 `AC-EXP-SCENE, AC-EXP-CAUSAL`；向量 `{"eventSequence": ["REQUEST-A", "REQUEST-B", "RESPONSE-B"], "expectedBoundary": "ownership policy identifies exactly one response owner", "expectedOwner": "REQUEST-B", "key": "k1", "ownershipEvents": [{"id": "REQUEST-A", "key": "k1", "kind": "REQUEST", "sequence": 1}, {"id": "REQUEST-B", "key": "k1", "kind": "REQUEST", "sequence": 2}, {"id": "RESPONSE-B", "key": "k1", "kind": "RESPONSE", "sequence": 3}], "policy": "MOST-RECENT", "responseId": "RESPONSE-B"}`；真值 independent request schedule；复位 reset correlation state；计时 event order retained even for equal timestamps；资源 same declared cost vector and one exclusive resource mode across arms；阻塞于 interactive IUT、confirmatory registration；`NOT-EXECUTED`
- `SC-SINGLE-BATCH` — 受控场景：single versus batch context；服务 `UPLOAD`；可控动作 paired declared contexts, not historical causal inference；依赖 `EXP-PREQ-IUT, EXP-PREQ-REGISTRATION`；验收 `AC-EXP-SCENE, AC-EXP-CAUSAL`；向量 `{"eventSequence": ["RESET", "SINGLE", "RESET", "BATCH"], "expectedBoundary": "full reset separates the two contexts", "firstContext": "single", "resetId": "reset-001", "secondContext": "batch"}`；真值 controlled scene definitions；复位 full IUT reset between scenes；计时 same qualified clock/configuration；资源 same declared cost vector and one exclusive resource mode across arms；阻塞于 interactive IUT、confirmatory registration；`NOT-EXECUTED`
- `SC-RESOURCE-ERROR` — 受控场景：resource exhaustion and consecutive error；服务 `INFORMATION`；可控动作 configured bound and injected adapter error；依赖 `EXP-PREQ-IUT, EXP-PREQ-REGISTRATION`；验收 `AC-EXP-SCENE, AC-EXP-CAUSAL`；向量 `{"consecutiveErrors": 2, "eventSequence": ["ACTION", "ADAPTER-ERROR", "RETRY", "ADAPTER-ERROR"], "expectedBoundary": "retry exhaustion is Stop-Error, not Stop-Budget", "expectedStop": "Stop-Error", "retryCap": 2}`；真值 configuration plus controller record；复位 reset resource/retry counters；计时 clock evidence retained but not converted to verdict；资源 same declared cost vector and one exclusive resource mode across arms；阻塞于 interactive IUT、confirmatory registration；`NOT-EXECUTED`
- 前提 `EXP-PREQ-IUT` — 责任：Provide an interactive IUT with frozen identity and configuration.；关闭条件：registered IUT/configuration plus operator availability; not established in this PR
- 前提 `EXP-PREQ-REGISTRATION` — 责任：Register confirmatory scene, truth, reset, clock and cost contracts.；关闭条件：independent confirmatory gate record; not established in this PR

## 切片与依赖

保守未知的历史效果须保留全部输入候选；Stop-Empty 需要已证明不相容，不能由输出空集倒推。完整性变体先核验服务、符号对象身份及带类型证据，再判断适用性和数值关系。未知是否选择选项或未知件号，不构成“不适用”或“已违反”的证据。缺失校验值、未知是否选择或完成比较、未观察到 FINAL-DATA 前提均为 NOT-EVALUATED，不得判为确定 VIOLATED；已知不适用仍独立处理。运行能力仍为 NOT-ESTABLISHED。
- `SLICE-OFFLINE-UPLOAD-INFORMATION` — 离线捕获至可追踪报告 — 176 条需求用途
### 依赖 `DEP-INTEGRITY-RUNTIME` — ARINC 645 完整性运行时资格
- 规格／运行：`CLOSED` / `NOT-ESTABLISHED`；影响规格就绪：`False`
- 需求：`CRS-M1-00076`, `CRS-M1-00082`, `CRS-M1-00085`, `CRS-M1-00086`, `CRS-M1-00087`, `CRS-M1-00109`；模块：`MOD-TRANSFER`；记录：`TRANSFER-RECORD`；验收：`AC-SYN-INTEGRITY`
- 来源：`[{"contract": "information receiver: when declared integrity option selected and supported, retain option identity, receiver support and protected bytes; without qualified runtime evidence report NOT-EVALUATED.", "contractId": "INT-INFORMATION-RECEIVER-SUPPORT", "requirementId": "CRS-M1-00076", "sourceUnitId": "SU-ARINC-615A-3-5-4-2-P047-PROSE-SENTENCE-025-3CF28DC21423"}, {"contract": "upload receiver: when declared integrity option selected and supported, retain option identity, receiver support and protected bytes; without qualified runtime evidence report NOT-EVALUATED.", "contractId": "INT-UPLOAD-RECEIVER-SUPPORT", "requirementId": "CRS-M1-00082", "sourceUnitId": "SU-ARINC-615A-3-5-4-3-P048-PROSE-SENTENCE-026-F38D018C4499"}, {"contract": "final load image and LSP: when all load bytes and declared check-value fields are present, retain algorithm identity, ordered image bytes and LSP check value; without qualified runtime evidence report NOT-EVALUATED.", "contractId": "INT-FINAL-IMAGE-LSP-VALUE", "requirementId": "CRS-M1-00085", "sourceUnitId": "SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-007-F209ABE1376B"}, {"contract": "old and new target files: when optional comparison is selected and both file identities are evidenced, retain old/new file identities, bytes and comparison result; without qualified runtime evidence report NOT-EVALUATED.", "contractId": "INT-OPTIONAL-OLD-NEW-COMPARE", "requirementId": "CRS-M1-00086", "sourceUnitId": "SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-008-CDA43D6568CC"}, {"contract": "two files with the same part number: when two distinct file identities declare the same part number, retain both file identities, their common part number, CRC A, CRC B, and CRC-A-equals-CRC-B relation; without qualified runtime evidence report NOT-EVALUATED.", "contractId": "INT-SAME-PART-NUMBER-CRC-EQUALITY", "requirementId": "CRS-M1-00087", "sourceUnitId": "SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-010-F4624AC8DCB4"}, {"contract": "status-file stream after final DATA: when integrity calculation remains in progress after final DATA, retain final-DATA event, calculation interval and continued status-file events; without qualified runtime evidence report NOT-EVALUATED.", "contractId": "INT-POST-DATA-STATUS-CONTINUATION", "requirementId": "CRS-M1-00109", "sourceUnitId": "SU-ARINC-615A-3-6-3-2-P068-PROSE-SENTENCE-042-4C1D759A6B9A"}]`
- 义务见证：`[{"expected": {"protectedBytesBound": true, "receiverSupportsSelectedOption": true}, "expectedRelation": "receiver supports selected INFORMATION integrity option", "inputs": {"optionIdentity": "integrity-option-information", "optionSelected": true, "protectedBytesRef": "symbolic-information-bytes", "receiverSupport": true, "service": "INFORMATION"}, "requirementId": "CRS-M1-00076"}, {"expected": {"protectedBytesBound": true, "receiverSupportsSelectedOption": true}, "expectedRelation": "receiver supports selected UPLOAD integrity option", "inputs": {"optionIdentity": "integrity-option-upload", "optionSelected": true, "protectedBytesRef": "symbolic-upload-bytes", "receiverSupport": true, "service": "UPLOAD"}, "requirementId": "CRS-M1-00082"}, {"expected": {"checkValueRelation": "EQUALS"}, "expectedRelation": "final-image check value equals the LSP check value", "inputs": {"checkValuePresent": true, "finalImageCheckValue": "0x1234", "finalImageId": "image-A", "lspCheckValue": "0x1234", "lspId": "lsp-A", "orderedBytesPresent": true, "relation": "EQUALS"}, "requirementId": "CRS-M1-00085"}, {"expected": {"comparisonResult": "DIFFERENT", "comparisonSelected": true}, "expectedRelation": "optional old/new comparison retains both identities and its declared result", "inputs": {"comparisonResult": "DIFFERENT", "comparisonSelected": true, "newCheckValue": "0x2222", "newFileId": "new-A", "oldCheckValue": "0x1111", "oldFileId": "old-A"}, "requirementId": "CRS-M1-00086"}, {"expected": {"samePartNumberCheckValueRelation": "EQUALS"}, "expectedRelation": "same part number implies crcA equals crcB", "inputs": {"crcA": "0x1234", "crcB": "0x1234", "fileAId": "file-A", "fileBId": "file-B", "partNumberA": "PN-1", "partNumberB": "PN-1"}, "requirementId": "CRS-M1-00087"}, {"expected": {"statusContinuation": "AT-EACH-OBSERVATION-POINT"}, "expectedRelation": "STATUS continues after FINAL-DATA while calculation is in progress", "inputs": {"calculationEndAt": 12, "calculationInProgress": true, "calculationStartAt": 10, "events": [{"at": 10, "kind": "FINAL-DATA"}, {"at": 11, "kind": "STATUS"}, {"at": 12, "kind": "STATUS"}], "finalDataSeen": true, "observationComplete": true, "requiredStatusObservationPoints": [11, 12]}, "requirementId": "CRS-M1-00109"}]`
- 派生义务变体（仅规格）：`[{"branch": "VIOLATED", "changes": {"receiverSupport": false}, "requirementId": "CRS-M1-00076"}, {"branch": "NOT-EVALUATED", "changes": {"receiverSupport": null}, "requirementId": "CRS-M1-00076"}, {"branch": "NOT-APPLICABLE", "changes": {"optionSelected": false}, "requirementId": "CRS-M1-00076"}, {"branch": "VIOLATED", "changes": {"receiverSupport": false}, "requirementId": "CRS-M1-00082"}, {"branch": "NOT-EVALUATED", "changes": {"receiverSupport": null}, "requirementId": "CRS-M1-00082"}, {"branch": "NOT-APPLICABLE", "changes": {"optionSelected": false}, "requirementId": "CRS-M1-00082"}, {"branch": "VIOLATED", "changes": {"lspCheckValue": "0x5678"}, "requirementId": "CRS-M1-00085"}, {"branch": "NOT-EVALUATED", "changes": {"checkValuePresent": false, "finalImageCheckValue": null, "lspCheckValue": null}, "requirementId": "CRS-M1-00085"}, {"branch": "VIOLATED", "changes": {"comparisonResult": "EQUAL", "newCheckValue": "0x2222", "oldCheckValue": "0x1111"}, "requirementId": "CRS-M1-00086"}, {"branch": "NOT-EVALUATED", "changes": {"oldCheckValue": null}, "requirementId": "CRS-M1-00086"}, {"branch": "NOT-APPLICABLE", "changes": {"comparisonSelected": false}, "requirementId": "CRS-M1-00086"}, {"branch": "VIOLATED", "changes": {"crcA": "0x1234", "crcB": "0x5678"}, "requirementId": "CRS-M1-00087"}, {"branch": "NOT-EVALUATED", "changes": {"crcA": null}, "requirementId": "CRS-M1-00087"}, {"branch": "NOT-APPLICABLE", "changes": {"partNumberB": "PN-2"}, "requirementId": "CRS-M1-00087"}, {"branch": "VIOLATED", "changes": {"events": [{"at": 10, "kind": "FINAL-DATA"}, {"at": 11, "kind": "STATUS"}]}, "requirementId": "CRS-M1-00109"}, {"branch": "NOT-EVALUATED", "changes": {"observationComplete": false}, "requirementId": "CRS-M1-00109"}, {"branch": "NOT-APPLICABLE", "changes": {"calculationInProgress": false}, "requirementId": "CRS-M1-00109"}]`
- 合同：使用已绑定的 ARINC 645 参数叶、出现顺序字节流和精确算法身份；除非运行资格证据齐全，否则输出 NOT-EVALUATED。
- 受影响判断：依赖 CRC 的验证和相等判断在运行时仍不可用；传输／重建只能保留字节与来源。
- 运行关闭：实现身份与测试；项目特定算法／配置绑定；受控向量执行证据；独立门禁记录
- 失败：缺少运行证据时产生 NOT-EVALUATED 或具名依赖状态，绝不产生 PASS、FAIL 或能力已建立。；证据：`configs/engineering/cltav_integrity_obligation_baseline.json`, `configs/requirements/arinc_615a3_m1_crs.json`

## 论文追踪

- `PT-ARCH` / III — `toolRequirements`, `moduleContracts`, `recordContracts`, `experimentInterfaceBindings`：Layered requirements and responsibility interfaces; no implementation claim.
- `PT-METHOD` / IV — `algorithmRefinements`, `runtimeParameterContracts`：Bounded reference-kernel specification; no general solver or completeness claim.
- `PT-EXPERIMENT` / V — `experimentInterfaceBindings`, `acceptanceCases`：Historical exploratory and future controlled evidence lines remain separate.
- `PT-RESULTS` / VI — `reviewBoundary`：No confirmatory result is reported.
- `PT-LIMITS` / VII — `implementationDependencies`：Runtime integrity, IUT, clock and independent-truth dependencies remain explicit.

## 切片成员关系

| 切片 | 需求 |
|---|---|
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00021` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00025` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00032` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00071` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00072` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00073` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00074` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00075` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00076` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00077` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00078` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00079` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00080` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00081` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00082` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00083` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00084` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00085` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00086` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00087` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00088` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00089` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00090` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00091` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00093` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00094` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00095` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00096` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00097` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00098` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00099` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00100` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00101` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00102` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00103` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00104` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00105` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00106` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00107` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00108` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00109` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00124` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00125` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00126` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00127` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00128` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00129` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00130` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00131` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00132` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00133` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00134` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00135` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00136` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00137` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00138` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00139` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00140` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00141` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00142` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00143` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00144` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00145` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00146` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00147` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00148` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00149` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00150` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00151` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00152` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00153` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00154` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00155` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00156` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00157` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00158` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00159` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00160` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00161` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00162` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00163` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00164` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00165` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00166` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00186` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00282` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00283` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00284` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00285` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00286` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00287` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00288` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00289` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00290` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00291` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00292` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00293` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00294` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00295` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00296` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00297` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00298` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00299` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00300` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00301` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00302` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00303` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00304` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00305` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00306` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00307` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00308` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00309` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00310` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00311` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00312` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00313` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00314` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00315` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00316` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00317` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00318` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00319` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00320` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00321` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00322` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00323` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00324` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00325` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00326` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00327` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00328` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00329` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00330` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00331` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00332` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00333` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00346` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00347` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00348` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00349` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00350` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00351` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00352` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00353` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00354` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00355` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00356` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00357` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00358` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00359` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00360` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00361` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00362` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00363` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00364` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00365` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00366` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00367` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00368` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00369` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00370` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00371` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00372` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00373` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00374` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00375` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00376` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00378` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00618` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00620` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00622` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00632` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00645` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00646` |
| `SLICE-OFFLINE-UPLOAD-INFORMATION` | `CRS-M1-00647` |

## 处置摘要

| 处置 | 数量 |
|---|---:|
| `FIRST-SLICE-IMPLEMENTATION` | 176 |
| `LATER-SERVICE` | 137 |
| `NOT-TOOL-OBLIGATION` | 550 |

## 全部需求处置

| 需求 | 处置 | 首轮 | 模块 | 记录 | 验收 | 理由 |
|---|---|---|---|---|---|---|
| `CRS-M1-00001` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00002` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00003` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00004` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00005` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00006` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00007` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00008` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00009` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00010` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00011` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00012` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00013` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00014` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00015` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00016` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00017` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00018` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00019` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00020` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00021` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 COMMON 时序、TFTP 传输或末块观测合同。 依赖：无 |
| `CRS-M1-00022` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00023` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00024` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00025` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 COMMON 时序、TFTP 传输或末块观测合同。 依赖：无 |
| `CRS-M1-00026` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00027` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00028` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00029` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00030` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00031` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00032` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 COMMON 时序、TFTP 传输或末块观测合同。 依赖：无 |
| `CRS-M1-00033` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00034` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00035` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00036` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00037` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00038` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00039` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00040` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00041` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00042` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00043` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00044` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00045` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00046` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00047` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00048` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00049` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00050` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00051` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00052` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00053` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00054` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00055` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00056` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00057` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00058` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00059` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00060` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00061` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00062` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00063` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00064` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00065` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00066` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00067` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00068` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00069` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00070` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00071` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00072` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00073` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00074` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00075` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00076` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `TRANSFER-RECORD` | `AC-SYN-INTEGRITY` | 首轮规格保留带 CRC 的协议义务和来源参数；运行时验证仍明确为未建立，等待实现、配置和执行证据。 依赖：`DEP-INTEGRITY-RUNTIME` |
| `CRS-M1-00077` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00078` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00079` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00080` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00081` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00082` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `TRANSFER-RECORD` | `AC-SYN-INTEGRITY` | 首轮规格保留带 CRC 的协议义务和来源参数；运行时验证仍明确为未建立，等待实现、配置和执行证据。 依赖：`DEP-INTEGRITY-RUNTIME` |
| `CRS-M1-00083` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00084` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00085` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `TRANSFER-RECORD` | `AC-SYN-INTEGRITY` | 首轮规格保留带 CRC 的协议义务和来源参数；运行时验证仍明确为未建立，等待实现、配置和执行证据。 依赖：`DEP-INTEGRITY-RUNTIME` |
| `CRS-M1-00086` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `TRANSFER-RECORD` | `AC-SYN-INTEGRITY` | 首轮规格保留带 CRC 的协议义务和来源参数；运行时验证仍明确为未建立，等待实现、配置和执行证据。 依赖：`DEP-INTEGRITY-RUNTIME` |
| `CRS-M1-00087` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `TRANSFER-RECORD` | `AC-SYN-INTEGRITY` | 首轮规格保留带 CRC 的协议义务和来源参数；运行时验证仍明确为未建立，等待实现、配置和执行证据。 依赖：`DEP-INTEGRITY-RUNTIME` |
| `CRS-M1-00088` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00089` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00090` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00091` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00092` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00093` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00094` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00095` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00096` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00097` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00098` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00099` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00100` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00101` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00102` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00103` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00104` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00105` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00106` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00107` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00108` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00109` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `TRANSFER-RECORD` | `AC-SYN-INTEGRITY` | 首轮规格保留带 CRC 的协议义务和来源参数；运行时验证仍明确为未建立，等待实现、配置和执行证据。 依赖：`DEP-INTEGRITY-RUNTIME` |
| `CRS-M1-00110` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00111` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00112` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00113` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00114` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00115` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00116` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00117` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00118` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00119` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00120` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00121` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00122` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00123` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00124` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00125` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00126` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00127` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00128` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00129` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00130` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00131` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00132` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00133` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00134` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00135` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00136` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00137` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00138` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00139` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00140` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00141` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00142` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00143` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00144` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00145` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00146` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00147` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00148` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00149` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00150` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00151` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00152` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00153` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00154` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00155` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00156` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00157` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00158` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00159` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00160` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00161` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00162` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00163` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00164` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00165` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00166` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00167` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00168` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00169` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00170` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00171` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00172` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00173` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00174` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00175` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00176` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00177` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00178` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00179` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00180` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00181` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00182` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00183` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00184` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00185` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00186` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 COMMON 时序、TFTP 传输或末块观测合同。 依赖：无 |
| `CRS-M1-00187` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00188` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00189` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00190` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00191` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00192` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00193` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00194` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00195` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00196` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00197` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00198` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00199` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00200` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00201` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00202` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00203` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00204` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00205` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00206` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00207` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00208` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00209` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00210` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00211` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00212` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00213` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00214` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00215` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00216` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00217` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00218` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00219` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00220` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00221` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00222` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00223` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00224` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00225` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00226` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00227` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00228` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00229` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00230` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00231` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00232` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00233` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00234` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00235` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00236` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00237` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00238` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00239` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00240` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00241` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00242` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00243` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00244` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00245` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00246` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00247` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00248` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00249` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00250` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00251` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00252` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00253` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00254` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00255` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00256` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00257` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00258` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00259` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00260` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00261` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00262` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00263` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00264` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00265` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00266` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00267` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00268` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00269` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00270` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00271` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00272` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00273` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00274` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00275` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00276` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00277` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00278` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00279` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00280` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00281` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00282` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00283` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00284` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00285` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00286` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00287` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00288` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00289` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00290` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00291` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00292` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00293` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00294` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00295` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00296` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00297` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00298` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00299` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00300` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00301` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00302` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00303` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00304` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00305` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00306` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00307` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00308` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00309` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00310` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00311` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00312` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00313` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00314` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00315` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00316` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00317` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00318` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00319` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00320` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00321` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00322` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00323` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00324` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00325` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00326` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00327` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00328` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00329` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00330` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00331` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00332` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00333` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00334` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00335` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00336` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00337` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00338` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00339` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00340` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00341` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00342` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00343` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00344` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00345` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00346` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00347` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00348` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00349` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00350` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00351` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00352` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00353` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00354` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00355` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00356` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00357` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00358` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00359` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00360` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00361` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00362` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00363` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00364` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00365` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00366` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00367` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00368` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00369` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00370` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00371` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00372` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00373` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00374` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00375` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00376` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00377` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00378` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 有界离线 UPLOAD／INFORMATION 重建、时序、所有权或传输输入。 依赖：无 |
| `CRS-M1-00379` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00380` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00381` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00382` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00383` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00384` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00385` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00386` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00387` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00388` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00389` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00390` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00391` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00392` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00393` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00394` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00395` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00396` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00397` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00398` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00399` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00400` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00401` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00402` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00403` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00404` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00405` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00406` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00407` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00408` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00409` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00410` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00411` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00412` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00413` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00414` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00415` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00416` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00417` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00418` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00419` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00420` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00421` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00422` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00423` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00424` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00426` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00427` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00428` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00429` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00430` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00431` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00432` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00433` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00434` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00435` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00436` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00437` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00438` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00439` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00440` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00441` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00442` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00443` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00444` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00445` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00446` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00447` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00448` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00449` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00450` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00451` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00452` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00453` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00454` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00455` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00456` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00457` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00458` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00459` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00460` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00461` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00462` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00463` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00464` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00465` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00466` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00467` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00468` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00469` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00470` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00471` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00472` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00473` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00474` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00475` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00476` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00477` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00478` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00479` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00480` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00481` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00482` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00483` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00484` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00485` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00486` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00487` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00488` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00489` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00490` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00491` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00492` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00493` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00494` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00495` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00496` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00497` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00498` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00499` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00500` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00501` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00502` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00503` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00504` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00505` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00506` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00507` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00508` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00509` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00510` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00511` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00512` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00513` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00514` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00515` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00516` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00517` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00518` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00519` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00520` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00521` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00522` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00523` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00524` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00525` | `LATER-SERVICE` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00526` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00527` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00528` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00529` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00530` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00531` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00532` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00533` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00534` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00535` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00536` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00537` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00538` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00539` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00540` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00541` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00542` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00543` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00544` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00545` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00546` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00547` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00548` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00549` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00550` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00551` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00552` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00553` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00554` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00555` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00556` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00557` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00558` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00559` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00560` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00561` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00562` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00563` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00564` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00565` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00566` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00567` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00568` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00569` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00570` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00571` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00572` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00573` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00574` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00575` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00576` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00577` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00578` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00579` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00580` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00581` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00582` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00583` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00584` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00585` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00586` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00587` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00588` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00589` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00590` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00591` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00592` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00593` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00594` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00595` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00596` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00597` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00598` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00599` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00600` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00601` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00602` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00603` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00604` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00605` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00606` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00607` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00608` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00609` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00610` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00611` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00612` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00613` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00614` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00615` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00616` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00617` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00618` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 TFTP 传输身份、选项确认、请求布局或终止重建。 依赖：无 |
| `CRS-M1-00619` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00620` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 COMMON 时序、TFTP 传输或末块观测合同。 依赖：无 |
| `CRS-M1-00621` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00622` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 TFTP 传输身份、选项确认、请求布局或终止重建。 依赖：无 |
| `CRS-M1-00623` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00624` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00625` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00626` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00627` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00628` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00629` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00630` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00631` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00632` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 TFTP 传输身份、选项确认、请求布局或终止重建。 依赖：无 |
| `CRS-M1-00633` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00634` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00635` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00636` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00637` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00638` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00639` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00640` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00641` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00642` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00643` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00644` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00645` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 TFTP 传输身份、选项确认、请求布局或终止重建。 依赖：无 |
| `CRS-M1-00646` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 TFTP 传输身份、选项确认、请求布局或终止重建。 依赖：无 |
| `CRS-M1-00647` | `FIRST-SLICE-IMPLEMENTATION` | `True` | `MOD-TRANSFER` | `PROTOCOL-EVENT` | `AC-SYN-TRANSFER` | 首轮 TFTP 传输身份、选项确认、请求布局或终止重建。 依赖：无 |
| `CRS-M1-00648` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00649` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00650` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00651` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00652` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00653` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00654` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00655` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00656` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00657` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00658` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00659` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00660` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00661` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00662` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00663` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00664` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00665` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00666` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00667` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00668` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00669` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00670` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00671` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00672` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00673` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00674` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00675` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00676` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00677` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00678` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00679` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00680` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00681` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00682` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00683` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00684` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00685` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00686` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00687` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00688` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00689` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00690` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00691` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00692` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00693` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00694` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00695` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00696` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00697` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00698` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00699` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00700` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00701` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00702` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00703` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00704` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00705` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00706` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00707` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00708` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00709` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00710` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00711` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00712` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00713` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00714` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00715` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00716` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00717` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00718` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00719` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00720` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00721` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00722` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00723` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00724` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00725` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00726` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00727` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00728` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00729` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00730` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00731` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00732` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00733` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00734` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00735` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00736` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00737` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00738` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00739` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00740` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00741` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00742` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00743` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00744` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00745` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00746` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00747` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00748` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00749` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00750` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00751` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00752` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00753` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00754` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00755` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00756` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00757` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00758` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00759` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00760` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00761` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00762` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00763` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00764` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00765` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00766` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00767` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00768` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00769` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00770` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00771` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00772` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00773` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00774` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00775` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00776` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00777` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00778` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00779` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00780` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00781` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00782` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00783` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00784` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00785` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00786` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00787` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00788` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00789` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00790` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00791` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00792` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00793` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00794` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00795` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00796` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00797` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00798` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00799` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00800` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00801` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00802` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00803` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00804` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00805` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00806` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00807` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00808` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00809` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00810` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00811` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00812` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00813` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00814` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00815` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00816` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00817` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00818` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00819` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00820` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00821` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00822` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00823` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00824` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00825` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00826` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00827` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00828` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00829` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00830` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00831` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00832` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00833` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00834` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00835` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00836` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00837` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00838` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00839` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00840` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00841` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00842` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00843` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00844` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00845` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00846` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00847` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00848` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00849` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00850` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00851` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00852` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00853` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00854` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00855` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00856` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00857` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00858` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00859` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00860` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00861` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00862` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00863` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
| `CRS-M1-00864` | `NOT-TOOL-OBLIGATION` | `False` | `—` | `—` | `—` | 不属于首轮离线 UPLOAD／INFORMATION 切片。 依赖：无 |
