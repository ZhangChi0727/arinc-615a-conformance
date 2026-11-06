# B-stage 615A UPLOAD LUR-start object lifecycle

`src/cltav_615a/` is the B-stage, in-process, deterministic engineering
surrogate for the bounded `ENG-UPLOAD-LUR-START` control slice.  Its entry
object is `cltav_615a.LurStartController`.  It is source-controlled Python
code, not a released distribution, CLI, real IUT, socket implementation,
wire-packet codec, complete UPLOAD implementation, protocol conformance
verdict, or experiment runner.

The source mapping remains the scenario package at
[`configs/engineering/cltav_615a_scenarios.json`](../../configs/engineering/cltav_615a_scenarios.json).
This page explains the executable B-stage realization of that declared slice;
it does not replace the package as source/method authority.

## Direct entry and microsteps

`LurStartController` owns the virtual tick, append-only public journal,
delivery queue, reset epochs, and evaluator-only installation audit.  The
Loader and TH objects own their respective private guards and state updates.
Each single-step call makes at most one emission or delivery decision (the
explicit `deliver_all` and shared-script helpers perform multiple microsteps).
Run this source example with `src` on the Python import path:

```python
from cltav_615a import LurStartController

controller = LurStartController()
assert controller.record_list_submission_precondition().accepted
assert controller.deliver_next().accepted  # consume the application LIST record
assert controller.emit_target_lus_ready().accepted
assert controller.deliver_next().accepted  # Loader receives ready, not accepted yet
assert controller.advance_loader().accepted  # DL emits LUR WRQ
assert controller.deliver_next().accepted  # TH receives current matching WRQ
assert controller.advance_target_hardware().accepted  # TH emits matching LUR ACK
assert controller.deliver_next().accepted  # Loader receives matching ACK
assert controller.advance_loader().accepted  # DL emits LUR DATA
assert controller.deliver_next().accepted  # consume DATA without reminting it
events = controller.public_snapshot().events
assert [event.kind for event in events] == [
    "LIST-SUBMISSION-PRECONDITION-RECORDED", "EV_TH_LUS0001",
    "EV_DL_WRQ_LUR", "EV_TH_ACK_LUR", "EV_DL_DATA_LUR",
]
```

The first call records the named application-layer preparation boundary only.
It has no TFTP opcode and does not fabricate an initialization or wire event.
LUS-0001 is emitted and delivered separately; only delivery establishes
`TARGET-LIST-READY`.  It does not establish `LIST-ACCEPTED` or run the rest of
the chain.  The Loader's normal WRQ guard requires offered + ready + not
accepted.  The TH emits ACK only after delivery of the current matching WRQ.
The Loader emits normal DATA only after delivery of the matching ACK.

Repeated input has a named no-op or rejection result; it never silently resets
the attempt or emits duplicate WRQ/DATA events.

## Bounded variants and evaluator evidence

Only one protocol variant may be installed per attempt:

| Variant | Actual local change | What remains guarded |
|---|---|---|
| `NORMAL` | No installation | All normal guards |
| `EARLY-WRQ` | The Loader bypasses only the missing-ready conjunct when offered and not accepted | list offer and not-accepted conditions |
| `EARLY-DATA` | The Loader bypasses only the missing-matching-ACK conjunct after real WRQ | actual WRQ and one-DATA conditions |

`install_fault()` produces evaluator-only installation/readback evidence.
An installation is not activation: an installed branch that does not execute
is returned as `NOT-TRIGGERED`.  A real bypass produces a distinct activation
record which references the actual public event ID and an execution position.
Install/readback failures and reset-revocation failures preserve their failed
attempt/reason and block further direct execution; they are never silently
converted into `NORMAL`.

If control is unconfirmed while events remain pending, `deliver_all()` returns
one named undelivered rejection and stops without consuming the queue or
altering the journal and failure audit.  Repeating the call remains bounded.
An event that was delivered but rejected by its peer is different: its queue
entry has been consumed, so bulk delivery continues to the remaining events.
Raw snapshots remain readable after control failure, but all inspection and
prefix-completion entry points return incomplete control-unconfirmed evidence.
Matching historical content alone cannot restore completion eligibility; a
successful full reset establishes a new clean attempt.

There is no third protocol-fault variant.  Synthetic controller confirmation
failure exists solely to test lifecycle handling and is not a protocol claim.

## Public and evaluator-only projection

| Material | Availability | Contents / boundary |
|---|---|---|
| `PublicEvent`, `JournalSnapshot`, `CompletionReceipt` | Public engineering journal | Event ID with reset/attempt epoch, attempt/session/correlation, actor/receiver/direction, semantic kind, applicable opcode/file role, tick and stable sequence. No fault ID, private state, source path/hash, code identity, prediction, expected H, or verdict. |
| `RuntimeReadback`, installation and activation records, reset evidence, archived attempts | Evaluator only | Private Loader/TH state, active installation, code identity, branch activation and reset/revocation disposition. An activation may cite a public event ID; a public event never points back to private audit state. |
| `OperationResult`, `DeliveryResult`, shared-script return values | Direct controller / evaluator only | Internal guard and bypass reasons are diagnostic control metadata, not an algorithm input. Only their owned `PublicEvent` values may enter the declared public journal projection; future C must not forward these entire result records. |

The public journal represents semantic engineering events only.  It does not
send UDP/IP, encode LUR bytes, compute CRC/check values, invent a TFTP opcode
for application preparation/readback tooling, or characterize a physical
clock.  Virtual ticks are nonnegative scheduler positions; same-tick
happens-before is defined by the controller-assigned `sequence_number`.  A
finite journal receipt is not a protocol timeout, no-response FAIL, or
calibrated deadline.

## Loaded source identity (B, not a distribution claim)

The constructor derives `source_identity` from the five bounded package modules
(`__init__.py`, `controller.py`, `objects.py`, `source_identity.py`, `types.py`).
Each module registers at the end of its real module execution: the same raw
source bytes are compiled with that module's filename/optimization and must
equal its executing code object.  Path and module-name checks bind this to the
loaded package, including when Python has a cached bytecode file.  Only then
are UTF-8 bytes normalized from CRLF to LF and frozen with file SHA-256/size.
The manifest identity is SHA-256 of the sorted `(path, hash, size)` tuples,
under `CLTAV-615A-LOADED-SOURCE-SHA256-LF-V1`; no current-commit self-reference
is embedded.  The scenario checker also requires the exact safe, tracked,
ordinary source files and their registration hooks.

Construction verifies the complete frozen set against current source files.
Missing files or post-import source drift raise a named `SourceIdentityError`
before any reset/installation can be confirmed.  A fresh process loading a
changed source revision obtains a new identity; an old cached object is not
relabelled with new disk hashes.  This is controlled normal-load provenance,
not protection against malicious Python monkeypatching or a sandbox claim.

`implementation_identity`, when supplied, is an expected-identity check, not
an arbitrary label.  `run_label` is separate evaluator-only metadata.
`AttemptAudit.source_identity` retains the immutable manifest; its own
`code_identity` and reset, installation, activation and runtime/fault readback
identities all reference `source_identity.identifier`.  Reset archives that
same manifest without rewriting earlier evidence.  Neither source identity
nor run label appears in the public event projection.  Review commit pins
supplement this B content binding; C adapter binding, D distributions/CLI and
real-IUT identity remain unestablished.

## Reset and journal invariants

`full_reset()` is not protocol abort and is not `Recover`.  A successful reset
clears Loader state, TH state, virtual tick, current journal, pending delivery,
delivery position, local correlation/sequence allocation, and the active fault
installation.  It then creates a fresh reset/attempt/session/correlation
epoch.  Local sequence numbering may restart, but public event identity cannot
collide across attempts or controller instances: every controller allocates a
fresh UUID run namespace unrelated to the fault variant, inherited by reset,
attempt, session, correlation and event IDs.  Cross-run semantic comparisons
normalize only these named identity fields (preserving equality and reply
links); they retain all roles, kinds, directions, times and sequence numbers.
Prior attempt journals and evaluator records remain
in the outer audit archive rather than contaminating the active attempt.

Emission appends one immutable `PublicEvent`; delivery does not remint,
renumber, reorder, or remove it.  A snapshot is a frozen tuple.  Retained
prefix validation permits exact equality or genuine append-only extension, but
only exact current content can be called a completed inspection.  Missing,
replaced, repeated, reordered, disconnected, or cross-attempt material is
named incomplete/invalid and cannot roll back object state.

Both delivery entrances use the same current-identity, semantic-tuple,
recorded-value, FIFO and single-consumption checks.  `deliver_external_event`
is not arbitrary external input: only a value exactly matching the owned,
unconsumed queue head may be submitted.  A faithful value copy is legal;
foreign, forged, modified, duplicate and out-of-order records cannot advance
state or consume the real pending event.  The five bounded semantic tuples are
checked independently of protocol order, so real early WRQ/DATA events remain
visible rather than being removed as malformed input.

## B-stage acceptance mapping

| B row | Direct evidence in this increment |
|---|---|
| B01 | Normal preparation, ready, WRQ, ACK, DATA microsteps and named duplicate behavior |
| B02 | Real EARLY-WRQ readiness-only bypass, install vs. activation distinction |
| B03 | Real EARLY-DATA matching-ACK-only bypass and late-ACK preservation |
| B04 | Every direct-object source module has no protected runtime/network import; the real controller consumes no prediction/session input |
| B05 | The same public control script drives NORMAL, EARLY-WRQ and EARLY-DATA; immutable public DTO projection remains independent of evaluator-only audit |
| B06 | Full reset clears active objects while preserving archived audit and new epochs |
| B07 | Old, foreign, wrong-correlation, wrong-WRQ-reference and duplicate ACKs cannot advance the active Loader |
| B08 | No-fault, installed/not-triggered, failed, reset-failed and single-fault-limit records; bounded bulk rejection retains pending evidence, successful reset restores operation, and delivered peer rejection does not stop the queue |
| B09 | Integer virtual ticks, same-tick stable order and finite engineering receipts |
| B10 | Immutable snapshots, append-only continuity and failure-without-rollback |
| B11 | Early semantic events remain raw events; no UDP/IP/payload/tool-error disguise |
| B12 | Existing scenario/checker/seam contracts remain separate and protected |

The B-stage object has not started C's `ReferenceSession` closure, `S7/S8/S9`,
history update, q-summary commit, production CLI/publisher/wheel, real network
or IUT work, four-arm execution, experiment admission, or a protocol
conformance claim.
