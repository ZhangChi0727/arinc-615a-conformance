# 615A engineering delivery (`cltav-615a-engineering`)

This is a D-stage **engineering** command. Exit code `0` means a valid
engineering record, verification, or replay comparison completed. It is **not**
an IUT PASS, protocol conformance, complete UPLOAD, four-arm result, or CRC
capability. CRC / check-value / naming / complete-integrity remain
`NOT-ESTABLISHED`.

Producer mode: `CLTAV-615A-ENGINEERING-CONTROL-SLICE-V1`. It must not be labelled
as the PR #25 G3 synthetic producer.

## Command

Authority Git objects are explicit. The command does not search `cwd`, import
pytest fixtures, or bind the current worktree copy of the scenario JSON. The
H-B scenario pin consumed by C remains
`d0c674f9fdb165b6ff8c2a40565d4deb7226d2a0:configs/engineering/cltav_615a_scenarios.json`.

```text
cltav-615a-engineering run \
  --authority-repository <git-dir> \
  --authority-commit <40-hex> \
  --case-id ENG-CASE-NORMAL|ENG-CASE-EARLY-WRQ|ENG-CASE-EARLY-DATA|ENG-CASE-ACCESS-UNKNOWN-RECOVER-GAP \
  --resource-mode ROUNDS|BUDGET \
  --resource-remaining 8 \
  --output <external-directory>

cltav-615a-engineering verify \
  --authority-repository <git-dir> --authority-commit <40-hex> \
  --evidence <external-directory>

cltav-615a-engineering replay \
  --authority-repository <git-dir> --authority-commit <40-hex> \
  --evidence <external-directory>
```

### Exit codes

| Code | Meaning |
|---|---|
| 0 | Valid engineering record written, verified, or replayed under this contract |
| 1 | Named `EngineeringError` (identity, schema, tamper, unsafe path, publish) |

A controlled ERROR or `Stop-Prediction-Gap` session can still yield exit `0`
when the envelope is a complete engineering record. The session stop reason is
inside `algorithm-visible/stop.json`.

## Evidence layout

```text
<output>/
  manifest.json              # operator map; not an algorithm input
  envelope.json              # closed envelope
  algorithm-visible/         # identities, journal, rounds, stop, fingerprint
  evaluator-audit/           # fault plan, reset, injection, limitations
```

`verify` recomputes H-B source identity, the full implementation identity
(adapter/object/runtime/engineering files), fingerprint, event
direction/sequence/tick/session identity, H-B action-library costs and remaining
resources, monotone H contraction and stop compatibility, split-file/envelope
closure, and then re-executes the recorded case to compare semantic fields.
Refreshing fingerprint after synergistic tamper still fails.

`replay` re-executes the same case and compares semantic fields. The named
exclusion whitelist is only new run/attempt/reset/session/correlation/event IDs
and wall-clock time.

## DM-C-R01

After UNKNOWN, a qualified Recover reconfirms q/target from current public
readback and does not emit protocol events. The full `ReferenceSession`
retains conservative H members and stops at `Stop-Prediction-Gap`. That
conservative stop is the accepted C/D behaviour. It is **not** post-recovery
continued diagnosis. Direct adapter FIFO continuation remains a C fact and is
not a restored discriminator.

`ENG-CASE-ACCESS-UNKNOWN-RECOVER-GAP` records that stop honestly.

## Limits

- Finite in-process surrogate loop only.
- Not complete UPLOAD, real network, IUT, SIL/HIL, or protocol PASS.
- Not four-arm execution or confirmatory results.
- Does not modify `src/cltav_runtime` to promote conservative members.
