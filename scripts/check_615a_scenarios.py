"""Validate the bounded 615A UPLOAD control-slice scenario package.

This checker validates an engineering-scene contract.  It does not execute a
protocol, establish a 615A conformance verdict, or admit an experiment.  Its
authority consumers read the exact Git blobs declared by the package, then
parse those same bytes; mutable worktree files never substitute an authority.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import stat
import subprocess
import sys
from collections import Counter
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PATH = Path("configs/engineering/cltav_615a_scenarios.json")
SCHEMA_PATH = Path("configs/engineering/cltav_615a_scenarios.schema.json")
CONTROL_CHANGE_PATH = Path("docs/control/changes/CR-2026-022.md")
CONTROL_CHANGE_ID = "CR-2026-022"
REQUIRED_BINDINGS = {
    "configs/requirements/arinc_615a3_m1_crs.json": "ACCEPTED-CRS",
    "configs/models/arinc_615a3_m2_model.json": "ACCEPTED-M2",
    "configs/engineering/cltav_development_contracts.json": "DEVELOPMENT-CONTRACT",
    "configs/research/cltav_interface_registry.json": "INTERFACE-REGISTRY",
    "configs/research/cltav_experiment_design.json": "EXPERIMENT-DESIGN",
    "configs/engineering/cltav_runtime_applicability.json": "RUNTIME-APPLICABILITY",
    "src/cltav_runtime/synthetic.py": "RUNTIME-SEAM",
    "src/cltav_runtime/session.py": "RUNTIME-SEAM",
    "pyproject.toml": "INSTALLATION-CONTRACT",
}

REQUIRED_SOURCE_RELATIONS = {
    "SRC-LIST-OFFER-PRECONDITION": {
        "requirementId": "CRS-M1-00363",
        "transitionId": "T_UPL_LIST_OFFER",
        "eventId": "EV_DL_OFFER_LIST",
        "eventDirection": "APPLICATION-NO-WIRE",
        "semanticOpcodeClass": "APPLICATION-NO-WIRE",
        "fileRole": "LOAD-LIST",
        "scenarioRationale": "Records the named application-layer list-offer prerequisite without dispatching a network event.",
        "scenarioRationaleZh": "记录具名的应用层清单提交前置，不调度网络事件。",
        "assertions": (
            "Application-level list submission is recorded as a named preparation boundary.",
            "DLA is not a WRQ, ACK, or DATA network endpoint in this scenario.",
        ),
        "source": "S_UPL_LIST_SENT",
        "target": "S_UPL_WAIT_LUS0001",
        "visibility": "APPLICATION",
        "scenarioUse": "PRECONDITION-ONLY",
        "executedByScenario": False,
        "notWireOpcode": True,
        "before": "UPLOAD-INITIALIZATION-ACCEPTED",
        "after": "LIST-OFFERED",
    },
    "SRC-LUS-READY": {
        "requirementId": "CRS-M1-00364",
        "transitionId": "T_UPL_WAIT_LUS0001",
        "eventId": "EV_TH_LUS0001",
        "eventDirection": "TH-TO-DL",
        "semanticOpcodeClass": "SEMANTIC-LUS-READY-NO-RAW-PACKET",
        "fileRole": "LUS-0001",
        "scenarioRationale": "Provides the current-session readiness stimulus without accepting the list or dispatching LUR.",
        "scenarioRationaleZh": "提供当前会话的就绪刺激，但不接受清单，也不调度 LUR。",
        "assertions": (
            "LUS-0001 establishes target readiness for this session.",
            "LUS-0001 does not accept the list and does not start LUR.",
        ),
        "source": "S_UPL_WAIT_LUS0001",
        "target": "S_UPL_WAIT_LUS0001",
        "visibility": "NETWORK-VISIBLE",
        "scenarioUse": "VISIBLE-STIMULUS",
        "executedByScenario": True,
        "notWireOpcode": False,
        "before": "listOffered=TRUE;listAccepted=FALSE",
        "after": "targetListReady=TRUE;listAccepted=FALSE",
    },
    "SRC-LUR-WRQ": {
        "requirementId": "CRS-M1-00365",
        "transitionId": "T_UPL_LUR_WRQ",
        "eventId": "EV_DL_WRQ_LUR",
        "eventDirection": "DL-TO-TH",
        "semanticOpcodeClass": "TFTP-WRQ-SEMANTIC",
        "fileRole": "LUR",
        "scenarioRationale": "Binds the DATA-LOADER readiness/list-acceptance guard to the visible semantic LUR WRQ emission.",
        "scenarioRationaleZh": "把 DATA-LOADER 的就绪／清单接受守卫绑定到可见的语义 LUR WRQ 发射。",
        "assertions": (
            "The source condition LIST-ACCEPTED is represented at the semantic level.",
            "The M2 guard reads listAccepted=FALSE before this transition writes TRUE.",
        ),
        "source": "S_UPL_WAIT_LUS0001",
        "target": "S_UPL_LUR_WRQ",
        "visibility": "NETWORK-VISIBLE",
        "scenarioUse": "VISIBLE-OBJECT-EVENT",
        "executedByScenario": True,
        "notWireOpcode": False,
        "before": "listOffered=TRUE;targetListReady=TRUE;listAccepted=FALSE",
        "after": "listAccepted=TRUE",
    },
    "SRC-LUR-ACK": {
        "requirementId": "CRS-M1-00366",
        "transitionId": "T_UPL_LUR_ACK",
        "eventId": "EV_TH_ACK_LUR",
        "eventDirection": "TH-TO-DL",
        "semanticOpcodeClass": "TFTP-ACK-SEMANTIC",
        "fileRole": "LUR",
        "scenarioRationale": "Binds the TARGET-HARDWARE peer response to the preceding matching semantic LUR WRQ.",
        "scenarioRationaleZh": "把 TARGET-HARDWARE 对端响应绑定到前序匹配的语义 LUR WRQ。",
        "assertions": (
            "The matching ACK is specific to the preceding LUR WRQ.",
        ),
        "source": "S_UPL_LUR_WRQ",
        "target": "S_UPL_LUR_ACK",
        "visibility": "NETWORK-VISIBLE",
        "scenarioUse": "VISIBLE-STIMULUS",
        "executedByScenario": True,
        "notWireOpcode": False,
        "before": "S_UPL_LUR_WRQ",
        "after": "S_UPL_LUR_ACK",
    },
    "SRC-LUR-DATA": {
        "requirementId": "CRS-M1-00367",
        "transitionId": "T_UPL_LUR_XFER",
        "eventId": "EV_DL_DATA_LUR",
        "eventDirection": "DL-TO-TH",
        "semanticOpcodeClass": "TFTP-DATA-SEMANTIC",
        "fileRole": "LUR",
        "scenarioRationale": "Binds normal DATA emission to the matching-ACK state; the named fault bypass remains evaluator-only.",
        "scenarioRationaleZh": "把正常 DATA 发射绑定到匹配 ACK 状态；具名故障旁路仍仅评估方可见。",
        "assertions": (
            "Normal execution emits DATA only after the matching ACK state.",
            "EARLY-DATA is a named local guard bypass, not an ACK timeout assertion.",
        ),
        "source": "S_UPL_LUR_ACK",
        "target": "S_UPL_LUR_XFER",
        "visibility": "NETWORK-VISIBLE",
        "scenarioUse": "VISIBLE-OBJECT-EVENT",
        "executedByScenario": True,
        "notWireOpcode": False,
        "before": "S_UPL_LUR_ACK",
        "after": "S_UPL_LUR_XFER",
    },
}

REQUIRED_HYPOTHESES = {
    "NORMAL": "NORMAL",
    "EARLY-WRQ": "SINGLE-FAULT",
    "EARLY-DATA": "SINGLE-FAULT",
}
REQUIRED_ACTION_KINDS = {
    "ACT-INSPECT-NO-WRQ-BEFORE-READY": "TEST",
    "ACT-PREP-ENTER-READY-WINDOW": "PREP",
    "ACT-TEST-ACK-BEFORE-DATA": "TEST",
    "ACT-RECOVER-RECONFIRM-READY": "RECOVER",
}
REQUIRED_CASE_IDS = {
    "CASE-NORMAL-CONTROL-TIMELINE",
    "CASE-EARLY-WRQ-TIMELINE",
    "CASE-EARLY-DATA-TIMELINE",
    "CASE-UNKNOWN-RECOVER-CONTINUATION",
    "CASE-RESOURCE-ADMISSION-BLOCK",
}
REQUIRED_CASE_TIMELINES = {
    "CASE-NORMAL-CONTROL-TIMELINE": (
        ("ACT-INSPECT-NO-WRQ-BEFORE-READY", ("NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001",), "Q-PRE-READY-NO-WRQ", ("NORMAL", "EARLY-DATA"), True),
        ("ACT-PREP-ENTER-READY-WINDOW", ("EV_TH_LUS0001",), "Q-TARGET-READY", ("NORMAL", "EARLY-DATA"), True),
        ("ACT-TEST-ACK-BEFORE-DATA", ("EV_DL_WRQ_LUR", "EV_TH_ACK_LUR", "EV_DL_DATA_LUR"), "Q-LUR-ORDER-ASSESSED", ("NORMAL",), False),
    ),
    "CASE-EARLY-WRQ-TIMELINE": (
        ("ACT-INSPECT-NO-WRQ-BEFORE-READY", ("EV_DL_WRQ_LUR",), "Q-EARLY-WRQ-OBSERVED", ("EARLY-WRQ",), False),
    ),
    "CASE-EARLY-DATA-TIMELINE": (
        ("ACT-INSPECT-NO-WRQ-BEFORE-READY", ("NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001",), "Q-PRE-READY-NO-WRQ", ("NORMAL", "EARLY-DATA"), True),
        ("ACT-PREP-ENTER-READY-WINDOW", ("EV_TH_LUS0001",), "Q-TARGET-READY", ("NORMAL", "EARLY-DATA"), True),
        ("ACT-TEST-ACK-BEFORE-DATA", ("EV_DL_WRQ_LUR", "EV_DL_DATA_LUR"), "Q-LUR-ORDER-ASSESSED", ("EARLY-DATA",), False),
    ),
    "CASE-UNKNOWN-RECOVER-CONTINUATION": (
        ("ACT-PREP-ENTER-READY-WINDOW", ("EV_TH_LUS0001",), "Q-TARGET-READY", ("NORMAL", "EARLY-DATA"), True),
        ("ACT-TEST-ACK-BEFORE-DATA", ("EXECUTION-EFFECT-UNKNOWN",), "NONE", ("NORMAL", "EARLY-DATA"), True),
        ("ACT-RECOVER-RECONFIRM-READY", ("RECOVER-READY-READBACK",), "Q-TARGET-READY", ("NORMAL", "EARLY-DATA"), True),
    ),
    "CASE-RESOURCE-ADMISSION-BLOCK": (
        ("ACT-TEST-ACK-BEFORE-DATA", ("NO-DISPATCH-INSUFFICIENT-RESOURCE",), "NONE", ("NORMAL", "EARLY-DATA"), False),
    ),
}
REQUIRED_CASE_INITIAL_CONTEXTS = {
    "CASE-NORMAL-CONTROL-TIMELINE": {
        "entryKind": "FRESH-ATTEMPT",
        "sessionBinding": "NEW-CURRENT-SESSION",
        "correlationBinding": "NEW-CURRENT-OPERATION-CORRELATION",
        "qStatus": "KNOWN",
        "currentSummary": "SCENE-ENTRY",
        "compatibleHypotheses": ["NORMAL", "EARLY-WRQ", "EARLY-DATA"],
        "completedActionIds": [],
        "retainedPublicPrefix": ["LIST-SUBMISSION-PRECONDITION-RECORDED"],
    },
    "CASE-EARLY-WRQ-TIMELINE": {
        "entryKind": "FRESH-ATTEMPT",
        "sessionBinding": "NEW-CURRENT-SESSION",
        "correlationBinding": "NEW-CURRENT-OPERATION-CORRELATION",
        "qStatus": "KNOWN",
        "currentSummary": "SCENE-ENTRY",
        "compatibleHypotheses": ["NORMAL", "EARLY-WRQ", "EARLY-DATA"],
        "completedActionIds": [],
        "retainedPublicPrefix": ["LIST-SUBMISSION-PRECONDITION-RECORDED"],
    },
    "CASE-EARLY-DATA-TIMELINE": {
        "entryKind": "FRESH-ATTEMPT",
        "sessionBinding": "NEW-CURRENT-SESSION",
        "correlationBinding": "NEW-CURRENT-OPERATION-CORRELATION",
        "qStatus": "KNOWN",
        "currentSummary": "SCENE-ENTRY",
        "compatibleHypotheses": ["NORMAL", "EARLY-WRQ", "EARLY-DATA"],
        "completedActionIds": [],
        "retainedPublicPrefix": ["LIST-SUBMISSION-PRECONDITION-RECORDED"],
    },
    "CASE-UNKNOWN-RECOVER-CONTINUATION": {
        "entryKind": "INHERITED-CONTINUATION",
        "sessionBinding": "CURRENT-SESSION-ONLY",
        "correlationBinding": "CURRENT-OPERATION-CORRELATION",
        "qStatus": "KNOWN",
        "currentSummary": "Q-PRE-READY-NO-WRQ",
        "compatibleHypotheses": ["NORMAL", "EARLY-DATA"],
        "completedActionIds": ["ACT-INSPECT-NO-WRQ-BEFORE-READY"],
        "retainedPublicPrefix": [
            "LIST-SUBMISSION-PRECONDITION-RECORDED",
            "INSPECT-NO-WRQ-BEFORE-READY-COMPLETED",
            "NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001",
        ],
    },
    "CASE-RESOURCE-ADMISSION-BLOCK": {
        "entryKind": "INHERITED-CONTINUATION",
        "sessionBinding": "CURRENT-SESSION-ONLY",
        "correlationBinding": "CURRENT-OPERATION-CORRELATION",
        "qStatus": "KNOWN",
        "currentSummary": "Q-TARGET-READY",
        "compatibleHypotheses": ["NORMAL", "EARLY-DATA"],
        "completedActionIds": [
            "ACT-INSPECT-NO-WRQ-BEFORE-READY",
            "ACT-PREP-ENTER-READY-WINDOW",
        ],
        "retainedPublicPrefix": [
            "LIST-SUBMISSION-PRECONDITION-RECORDED",
            "INSPECT-NO-WRQ-BEFORE-READY-COMPLETED",
            "EV_TH_LUS0001",
            "TH-LUS0001-READY-RECEIPT",
        ],
    },
}
REQUIRED_UNKNOWN_RECOVER_CONTRACT = {
    "trigger": "POST-DISPATCH-TEST-SUMMARY-CONFIRMATION-FAILURE",
    "triggerActionId": "ACT-TEST-ACK-BEFORE-DATA",
    "triggerRound": 2,
    "mayHaveVisibleEvents": ["EV_DL_WRQ_LUR", "EV_TH_ACK_LUR", "EV_DL_DATA_LUR"],
    "sessionDisposition": "UNKNOWN-PRESERVE-ACTUAL-SUCCESSOR-AND-POST-DISPATCH-JOURNAL",
    "recoverEntryQStatus": "UNKNOWN",
    "recoverRequiredPublicEvidence": [
        "CURRENT-SESSION-READY-READBACK",
        "RECOVER-READY-READBACK-COMPLETED",
        "EXACT-RETAINED-POST-DISPATCH-PUBLIC-PREFIX",
        "RECOVER-READY-READBACK-ONLY-EXTENSION",
    ],
    "targetAndSummaryConfirmation": "SEPARATE-REQUIRED-NO-REWIND-OR-REPLAY",
    "rewindProhibited": "NO-REWIND-TO-Q-PRE-READY-NO-WRQ",
    "unconfirmedRecoveryDisposition": "REMAIN-UNKNOWN",
}
REQUIRED_PUBLIC_SUMMARY_SOURCES = {
    "ACT-INSPECT-NO-WRQ-BEFORE-READY": {"VISIBLE-JOURNAL-PREFIX", "INSPECTION-COMPLETION-RECEIPT"},
    "ACT-PREP-ENTER-READY-WINDOW": {"VISIBLE-JOURNAL-PREFIX", "TH-LUS0001-READY-RECEIPT"},
    "ACT-TEST-ACK-BEFORE-DATA": {"VISIBLE-JOURNAL-PREFIX", "LUR-ORDER-CHECK-COMPLETED"},
    "ACT-RECOVER-RECONFIRM-READY": {"VISIBLE-JOURNAL-PREFIX", "RECOVER-READY-READBACK-COMPLETED"},
}
REQUIRED_PUBLIC_EVIDENCE_PROJECTIONS = {
    "ACT-INSPECT-NO-WRQ-BEFORE-READY": {
        "projectionKind": "CURRENT-SESSION-BOUNDED-JOURNAL-RECEIPT",
        "sessionBinding": "CURRENT-SESSION",
        "correlationBinding": "CURRENT-OPERATION-CORRELATION",
        "ordering": "STABLE-SEQUENCE-NUMBER",
        "inspectedRange": "RECEIPT-BOUNDED-CONTIGUOUS-CLOSED-PREFIX",
        "completionReceipt": "INSPECT-NO-WRQ-BEFORE-READY-COMPLETED",
        "receiptMustBeCompleted": True,
        "invalidOrUnconfirmedDisposition": "UNKNOWN-EFFECT-REQUIRES-QUALIFIED-RECOVER",
    },
    "ACT-PREP-ENTER-READY-WINDOW": {
        "projectionKind": "CURRENT-SESSION-BOUNDED-JOURNAL-RECEIPT",
        "sessionBinding": "CURRENT-SESSION",
        "correlationBinding": "CURRENT-OPERATION-CORRELATION",
        "ordering": "STABLE-SEQUENCE-NUMBER",
        "inspectedRange": "RECEIPT-BOUNDED-CONTIGUOUS-CLOSED-PREFIX",
        "completionReceipt": "TH-LUS0001-READY-RECEIPT",
        "receiptMustBeCompleted": True,
        "invalidOrUnconfirmedDisposition": "EXECUTED-UNCONFIRMED-SUMMARY-REQUIRES-UNKNOWN",
    },
    "ACT-TEST-ACK-BEFORE-DATA": {
        "projectionKind": "CURRENT-SESSION-BOUNDED-JOURNAL-RECEIPT",
        "sessionBinding": "CURRENT-SESSION",
        "correlationBinding": "CURRENT-OPERATION-CORRELATION",
        "ordering": "STABLE-SEQUENCE-NUMBER",
        "inspectedRange": "RECEIPT-BOUNDED-CONTIGUOUS-CLOSED-PREFIX",
        "completionReceipt": "LUR-ORDER-CHECK-COMPLETED",
        "receiptMustBeCompleted": True,
        "invalidOrUnconfirmedDisposition": "UNKNOWN-EFFECT-REQUIRES-QUALIFIED-RECOVER",
    },
    "ACT-RECOVER-RECONFIRM-READY": {
        "projectionKind": "CURRENT-SESSION-BOUNDED-JOURNAL-RECEIPT",
        "sessionBinding": "CURRENT-SESSION",
        "correlationBinding": "CURRENT-OPERATION-CORRELATION",
        "ordering": "STABLE-SEQUENCE-NUMBER",
        "inspectedRange": "RECEIPT-BOUNDED-CONTIGUOUS-CLOSED-PREFIX",
        "completionReceipt": "RECOVER-READY-READBACK-COMPLETED",
        "receiptMustBeCompleted": True,
        "invalidOrUnconfirmedDisposition": "DO-NOT-MARK-KNOWN",
    },
}
REQUIRED_ACTION_OUTCOME_COUNTS = {
    "ACT-INSPECT-NO-WRQ-BEFORE-READY": 2,
    "ACT-PREP-ENTER-READY-WINDOW": 1,
    "ACT-TEST-ACK-BEFORE-DATA": 2,
    "ACT-RECOVER-RECONFIRM-READY": 1,
}
REQUIRED_ACTION_RETURN_CONTRACTS = {
    "ACT-INSPECT-NO-WRQ-BEFORE-READY": (
        "PUBLIC-OBSERVATION-SUMMARY-CONFIRMATION",
        "UNKNOWN-EFFECT-REQUIRES-QUALIFIED-RECOVER",
    ),
    "ACT-PREP-ENTER-READY-WINDOW": (
        "PREP-SUMMARY-COMMIT-SEPARATE-FROM-TARGET-STATUS",
        "PREP-EFFECT-BRANCH-TABLE-REQUIRED",
    ),
    "ACT-TEST-ACK-BEFORE-DATA": (
        "PUBLIC-OBSERVATION-SUMMARY-CONFIRMATION",
        "UNKNOWN-EFFECT-REQUIRES-QUALIFIED-RECOVER",
    ),
    "ACT-RECOVER-RECONFIRM-READY": (
        "TARGET-AND-SUMMARY-CONFIRMED-SEPARATELY",
        "DO-NOT-MARK-KNOWN",
    ),
}
REQUIRED_PREP_EFFECT_BRANCHES = {
    "confirmed": {
        "effectClass": "NONE",
        "targetConfirmation": "TARGET-CONFIRMED",
        "summaryConfirmation": "SUMMARY-CONFIRMED",
        "historyDisposition": "COMMIT-CONFIRMED-HISTORY",
        "qDisposition": "KNOWN-S9-COMMIT",
        "successorDisposition": "PRESERVE-RETURNED-SUCCESSOR",
        "chargeDisposition": "CHARGE-ONCE",
    },
    "confirmedNotSent": {
        "effectClass": "CONFIRMED-NOT-SENT",
        "targetConfirmation": "NO-DISPATCH-CONFIRMED",
        "summaryConfirmation": "NO-SUCCESSOR-SUMMARY",
        "historyDisposition": "PRESERVE-EXISTING-HISTORY",
        "qDisposition": "PRESERVE-KNOWN-SUMMARY",
        "successorDisposition": "NO-OBJECT-ADVANCE",
        "chargeDisposition": "CHARGE-ONCE",
    },
    "executedSummaryUnconfirmed": {
        "effectClass": "UNKNOWN-EFFECT",
        "targetConfirmation": "ACTUAL-SUCCESSOR-MAY-HAVE-EXECUTED",
        "summaryConfirmation": "SUCCESSOR-SUMMARY-UNCONFIRMED",
        "historyDisposition": "PRESERVE-CONSERVATIVE-HISTORY",
        "qDisposition": "UNKNOWN-REQUIRES-QUALIFIED-RECOVER",
        "successorDisposition": "PRESERVE-RETURNED-SUCCESSOR",
        "chargeDisposition": "CHARGE-ONCE",
    },
    "targetNotReachedWithConfirmedSuccessor": {
        "effectClass": "NONE",
        "targetConfirmation": "TARGET-NOT-REACHED-BUT-SUCCESSOR-CONFIRMED",
        "summaryConfirmation": "SUMMARY-CONFIRMED",
        "historyDisposition": "COMMIT-CONFIRMED-HISTORY",
        "qDisposition": "KNOWN-S9-COMMIT",
        "successorDisposition": "PRESERVE-RETURNED-SUCCESSOR",
        "chargeDisposition": "CHARGE-ONCE",
    },
}
REQUIRED_RESOURCE_TEXT = {
    "roundsMeaning": "A positive remaining execution count admits the next bounded action; it is not a monetary budget.",
    "budgetMeaning": "The declared engineering action cost must be affordable before dispatch.",
}
REQUIRED_SCOPE = {
    "operation": "UPLOAD",
    "roles": ["DATA-LOADER", "TARGET-HARDWARE"],
    "startBoundary": "LIST-SUBMISSION-PRECONDITION-RECORDED",
    "endBoundary": "LUR-CONTROL-SLICE-OBSERVATION-END",
    "preparedButNotExecuted": [
        "EV_DL_OFFER_LIST",
        "UPLOAD-INITIALIZATION",
        "FULL-LUR-BYTES",
        "CRC-CHECK-VALUE-NAMING",
    ],
    "notEvaluatedObligations": [
        "FULL-UPLOAD-COMPLETION",
        "LUR-PAYLOAD-INTEGRITY",
        "CRC-CHECK-VALUE-NAMING-CAPABILITY",
        "PROTOCOL-NO-RESPONSE-DEADLINE",
        "REAL-NETWORK-OR-IUT",
        "FOUR-ARM-EXPERIMENT",
    ],
    "relationshipToExperimentScenario": {
        "scenarioId": "SC-NORMAL-UPLOAD",
        "relation": "PREPARES-INTERFACE",
        "reason": "The LUR-start slice records engineering interfaces only; it does not demonstrate qualified UPLOAD completion or admitted experiment execution.",
    },
}
REQUIRED_TIME_AND_OBSERVATION = {
    "virtualClockId": "CLK-VIRTUAL-615A-SLICE",
    "tickRepresentation": "NONNEGATIVE-INTEGER",
    "tickMeaning": "One deterministic engineering scheduler tick; it is not a calibrated physical duration.",
    "uncertaintyIdentity": "U-VIRTUAL-EXACT-ENGINEERING-ONLY",
    "uncertaintyModel": "ZERO-WIDTH-VIRTUAL-ENGINEERING-MODEL",
    "sameTickOrdering": "Stable sequenceNumber establishes happens-before for same-tick events.",
    "ownershipPolicy": "CURRENT-SESSION-MATCHING-CORRELATION-ONLY",
    "finiteObservationBoundary": "A completed inspection horizon bounds the simulated object check only and never establishes a protocol timeout or no-response FAIL.",
}
REQUIRED_HYPOTHESIS_DOMAIN = {
    "members": [
        {
            "id": "NORMAL",
            "kind": "NORMAL",
            "definition": "The loader waits for session-local LUS-0001, emits LUR WRQ, waits for the matching TH ACK, then emits LUR DATA.",
        },
        {
            "id": "EARLY-WRQ",
            "kind": "SINGLE-FAULT",
            "definition": "The loader actually bypasses the readiness guard and emits LUR WRQ after the list-submission boundary but before LUS-0001.",
        },
        {
            "id": "EARLY-DATA",
            "kind": "SINGLE-FAULT",
            "definition": "After LUR WRQ, the loader actually bypasses the matching-ACK guard and emits LUR DATA before that ACK.",
        },
    ],
    "activeFaultVisibility": "EVALUATOR-ONLY",
    "algorithmMayKnow": [
        "DECLARED-HYPOTHESIS-DOMAIN",
        "DECLARED-PREDICTIONS",
        "PUBLIC-SCENE-CONFIGURATION",
    ],
    "algorithmMustNotReceive": [
        "ACTIVE-FAULT-ID",
        "FAULT-INSTALLATION-READBACK",
        "FAULT-ACTIVATION-RECORD",
        "PRIVATE-LOADER-STATE",
        "EXPECTED-FINAL-H",
    ],
    "coverageLimit": "The finite domain is an engineering diagnostic domain only; a surviving member is neither a protocol PASS nor a real-device root-cause finding.",
    "coverageLimitZh": "有限假设域仅用于工程诊断；剩余成员既不表示协议 PASS，也不表示已定位真实设备根因。",
}
REQUIRED_ACTION_DETAILS = {
    "ACT-INSPECT-NO-WRQ-BEFORE-READY": {
        "eligibility": "LIST-SUBMISSION-PRECONDITION-RECORDED and no session-local LUS-0001 journal event",
        "cost": (1, 1, 0, 0),
        "publicStimulus": "Complete one bounded inspection of the current visible journal prefix.",
        "observationMode": "FINITE-ENGINEERING-LOG-CHECK",
        "inspection": (
            "INSPECT-NO-WRQ-BEFORE-READY-COMPLETED",
            "NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001",
            1,
            False,
            False,
        ),
        "outcomes": (
            (
                "NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001",
                "Q-PRE-READY-NO-WRQ",
                "The public inspection receipt and the public no-WRQ journal predicate agree.",
                ("NORMAL", "EARLY-DATA"),
            ),
            (
                "EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001",
                "Q-EARLY-WRQ-OBSERVED",
                "The public inspection receipt is bound to the current journal event order.",
                ("EARLY-WRQ",),
            ),
        ),
        "nonEvaluatedObligations": ("PROTOCOL-NO-RESPONSE-DEADLINE", "PHYSICAL-CLOCK-CALIBRATION"),
    },
    "ACT-PREP-ENTER-READY-WINDOW": {
        "eligibility": "Q-PRE-READY-NO-WRQ is confirmed and the session has affordable preparation resource",
        "cost": (0, 1, 1, 0),
        "publicStimulus": "TH emits the session-local visible EV_TH_LUS0001 ready stimulus.",
        "observationMode": "VISIBLE-PREPARATION-EVENT",
        "inspection": (
            "TH-LUS0001-READY-RECEIPT",
            "EV_TH_LUS0001-RECORDED-FOR-CURRENT-SESSION",
            1,
            False,
            False,
        ),
        "outcomes": (
            (
                "EV_TH_LUS0001",
                "Q-TARGET-READY",
                "The public ready receipt is bound to the current session and is present in the visible journal.",
                ("NORMAL", "EARLY-DATA"),
            ),
        ),
        "nonEvaluatedObligations": ("FULL-UPLOAD-COMPLETION",),
    },
    "ACT-TEST-ACK-BEFORE-DATA": {
        "eligibility": "Q-TARGET-READY is confirmed and the session has an affordable TEST",
        "cost": (1, 1, 0, 0),
        "publicStimulus": "Drive one bounded loader control step and inspect the visible LUR WRQ, TH ACK and loader DATA event order.",
        "observationMode": "FINITE-JOURNAL-ORDER-CHECK",
        "inspection": (
            "LUR-ORDER-CHECK-COMPLETED",
            "EV_DL_WRQ_LUR followed either by matching EV_TH_ACK_LUR before EV_DL_DATA_LUR, or by EV_DL_DATA_LUR before any matching ACK",
            3,
            False,
            False,
        ),
        "outcomes": (
            (
                "WRQ-ACK-DATA-IN-ORDER",
                "Q-LUR-ORDER-ASSESSED",
                "The completed current-correlation prefix contains a matching ACK before its first DATA after WRQ.",
                ("NORMAL",),
            ),
            (
                "DATA-BEFORE-MATCHING-ACK",
                "Q-LUR-ORDER-ASSESSED",
                "The completed current-correlation prefix contains the first DATA after WRQ before any matching ACK; a later ACK cannot change that observed order.",
                ("EARLY-DATA",),
            ),
        ),
        "nonEvaluatedObligations": ("LUR-PAYLOAD-INTEGRITY", "FULL-UPLOAD-COMPLETION"),
    },
    "ACT-RECOVER-RECONFIRM-READY": {
        "eligibility": "SessionContext is UNKNOWN and a declared ready target can be publicly re-confirmed within the finite object boundary",
        "cost": (0, 1, 1, 0),
        "publicStimulus": "Request the controlled TH ready read-back and retain its visible journal receipt.",
        "observationMode": "VISIBLE-RECOVER-READBACK",
        "inspection": (
            "RECOVER-READY-READBACK-COMPLETED",
            "EXACT-RETAINED-POST-DISPATCH-PREFIX-EXTENDED-BY-CURRENT-SESSION-READY-READBACK",
            1,
            False,
            False,
        ),
        "outcomes": (
            (
                "RECOVER-READY-READBACK",
                "Q-TARGET-READY",
                "The public recover receipt extends the exact retained post-dispatch public prefix only by the current-session ready read-back; it re-confirms ready without replaying or rewinding an earlier action.",
                ("NORMAL", "EARLY-DATA"),
            ),
        ),
        "nonEvaluatedObligations": ("PHYSICAL-DEVICE-RECOVERY",),
    },
}
REQUIRED_LIFECYCLE_EVIDENCE = {
    "fullReset": {
        "successEvidence": "RESET-READBACK-AND-EMPTY-NEW-ATTEMPT-JOURNAL",
    },
    "faultInjection": {
        "installationEvidence": "CONTROLLER-READBACK-OF-NAMED-GUARD-OR-EMISSION-VARIANT",
        "activationEvidence": "INDEPENDENT-JOURNAL-BRANCH-ACTIVATION",
        "unconfirmedDisposition": "RETAIN-ATTEMPT-AS-UNCONFIRMED-NOT-NORMAL",
    },
}
REQUIRED_TRACEABILITY_RELATIONS = {
    "MAP-LIST-OFFER-PRECONDITION": {
        "stateOrActionId": "LIST-SUBMISSION-PRECONDITION-RECORDED",
        "sourceRelationIds": ("SRC-LIST-OFFER-PRECONDITION",),
        "existingInterfaceIds": (),
        "interfaceUse": "PRECONDITION-NO-DISPATCH",
        "acceptanceWitnessIds": ("WIT-FINITE-NO-WRQ-TEST",),
    },
    "MAP-NO-WRQ-FINITE-TEST": {
        "stateOrActionId": "ACT-INSPECT-NO-WRQ-BEFORE-READY",
        "sourceRelationIds": ("SRC-LUS-READY", "SRC-LUR-WRQ"),
        "existingInterfaceIds": ("IF-EXECUTE-RECORD", "IF-OBS-INTERPRET", "IF-HIST-UPDATE"),
        "interfaceUse": "FINITE-TEST-OBSERVATION-AND-HISTORY",
        "acceptanceWitnessIds": ("WIT-FINITE-NO-WRQ-TEST", "WIT-PUBLIC-SUMMARY"),
    },
    "MAP-PREP-READY": {
        "stateOrActionId": "ACT-PREP-ENTER-READY-WINDOW",
        "sourceRelationIds": ("SRC-LUS-READY",),
        "existingInterfaceIds": ("IF-EXECUTE-RECORD", "IF-PREP-RECOVER", "IF-HIST-UPDATE"),
        "interfaceUse": "PREP-RECEIPT-AND-CONFIRMATION",
        "acceptanceWitnessIds": ("WIT-PUBLIC-SUMMARY",),
    },
    "MAP-LUR-ORDER-TEST": {
        "stateOrActionId": "ACT-TEST-ACK-BEFORE-DATA",
        "sourceRelationIds": ("SRC-LUR-WRQ", "SRC-LUR-ACK", "SRC-LUR-DATA"),
        "existingInterfaceIds": ("IF-EXECUTE-RECORD", "IF-OBS-INTERPRET", "IF-HIST-UPDATE"),
        "interfaceUse": "FINITE-TEST-OBSERVATION-AND-HISTORY",
        "acceptanceWitnessIds": ("WIT-PUBLIC-SUMMARY",),
    },
    "MAP-RECOVER-READY": {
        "stateOrActionId": "ACT-RECOVER-RECONFIRM-READY",
        "sourceRelationIds": ("SRC-LUS-READY",),
        "existingInterfaceIds": ("IF-EXECUTE-RECORD", "IF-PREP-RECOVER", "IF-HIST-UPDATE"),
        "interfaceUse": "UNKNOWN-TO-QUALIFIED-RECOVER",
        "acceptanceWitnessIds": ("WIT-SUCCESSOR-AND-RECOVER",),
    },
}
REQUIRED_INTERFACE_OUTPUTS = {
    "IF-EXECUTE-RECORD": {"record", "effectClass", "correlationId"},
    "IF-OBS-INTERPRET": {"Iz", "effectClass", "summaryConfirmed", "postSummary"},
    "IF-PREP-RECOVER": {"targetConfirmed", "summaryConfirmed", "postSummary"},
    "IF-HIST-UPDATE": {"HistoryHandlePrime", "Hprime", "Stop-Empty"},
}
REQUIRED_FAULT_VARIANTS = {
    "EARLY-WRQ": {
        "installationTarget": "LOADER-READINESS-GUARD-BYPASS",
        "activationObservable": "EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001",
        "controllerReadback": "READBACK-READINESS-GUARD-BYPASS-ACTIVE",
        "algorithmVisibility": "EVALUATOR-ONLY",
    },
    "EARLY-DATA": {
        "installationTarget": "LOADER-MATCHING-ACK-GUARD-BYPASS",
        "activationObservable": "EV_DL_DATA_LUR-BEFORE-MATCHING-EV_TH_ACK_LUR",
        "controllerReadback": "READBACK-MATCHING-ACK-GUARD-BYPASS-ACTIVE",
        "algorithmVisibility": "EVALUATOR-ONLY",
    },
}
REQUIRED_OBJECT_STATES = {
    "LIST-OFFERED": ("M2-VARIABLE:listOffered", "FALSE"),
    "TARGET-LIST-READY": ("M2-VARIABLE:targetListReady", "FALSE"),
    "LIST-ACCEPTED": ("M2-VARIABLE:listAccepted", "FALSE"),
    "MATCHING-LUR-ACK": ("M2-STATE:S_UPL_LUR_ACK", "FALSE"),
    "TH-MATCHING-LUR-WRQ-RECEIVED": ("M2-STATE:S_UPL_LUR_WRQ", "FALSE"),
}
REQUIRED_OBJECT_OWNERS = {
    "LIST-OFFERED": "DATA-LOADER",
    "TARGET-LIST-READY": "DATA-LOADER",
    "LIST-ACCEPTED": "DATA-LOADER",
    "MATCHING-LUR-ACK": "DATA-LOADER",
    "TH-MATCHING-LUR-WRQ-RECEIVED": "TARGET-HARDWARE",
}
REQUIRED_OBJECT_STATE_INVARIANTS = {
    "LIST-OFFERED": "The named application-layer list-submission preparation boundary establishes this state; it is not a fabricated wire event.",
    "TARGET-LIST-READY": "Only the current-session EV_TH_LUS0001 stimulus establishes readiness; readiness does not itself accept the list.",
    "LIST-ACCEPTED": "The normal WRQ guard reads FALSE and only the controlled WRQ transition writes TRUE.",
    "MATCHING-LUR-ACK": "Only a current-session ACK correlated to the preceding LUR WRQ establishes this state for normal DATA emission.",
    "TH-MATCHING-LUR-WRQ-RECEIVED": "Only a current-session LUR WRQ establishes the peer state that permits the matching TH ACK emission.",
}
REQUIRED_OBJECT_NOT_ESTABLISHED = (
    "The bounded source-controlled Loader/TH surrogate is available only for direct synthetic engineering validation; "
    "no real-IUT identity, CL-TAV adapter, experiment execution, or protocol conformance behavior is established."
)
REQUIRED_OBJECT_NOT_ESTABLISHED_ZH = (
    "该受控源码 Loader／TH 替身仅用于直接合成工程验证；尚未建立真实 IUT 身份、CL-TAV 适配器、实验执行或协议符合性行为。"
)
REQUIRED_OBJECT_STAGE = "B-OBJECT-LIFECYCLE-CANDIDATE-PENDING-INDEPENDENT-REVIEW"
REQUIRED_OBJECT_IDENTITY_STATUS = "SOURCE-OBJECT-CANDIDATE-PENDING-INDEPENDENT-REVIEW"
REQUIRED_OBJECT_SOURCE_ROOT = "src/cltav_615a"
REQUIRED_OBJECT_ENTRY_POINT = "cltav_615a.LurStartController"
REQUIRED_OBJECT_SOURCE_FILES = tuple(
    f"src/cltav_615a/{name}" for name in ("__init__.py", "controller.py", "objects.py", "source_identity.py", "types.py")
)
REQUIRED_OBJECT_SOURCE_BINDING = {
    "scheme": "CLTAV-615A-LOADED-SOURCE-SHA256-LF-V1",
    "loadVerification": "MODULE-CODE-EQUALITY-FROZEN-SOURCE-AND-CONSTRUCTOR-DRIFT-CHECK",
    "auditLinkage": "FROZEN-MANIFEST-IN-ATTEMPT-AUDIT-SHARED-CODE-IDENTITY",
}
REQUIRED_OBJECT_GUARDS = {
    "GUARD-WRQ-AFTER-READY": {
        "sourceRelationId": "SRC-LUR-WRQ",
        "requiresState": ("LIST-OFFERED=TRUE", "TARGET-LIST-READY=TRUE", "LIST-ACCEPTED=FALSE"),
        "normalVisibleOutputId": "OUT-DL-WRQ-LUR",
        "faultBypassHypothesisId": "EARLY-WRQ",
    },
    "GUARD-DATA-AFTER-MATCHING-ACK": {
        "sourceRelationId": "SRC-LUR-DATA",
        "requiresState": ("MATCHING-LUR-ACK=TRUE",),
        "normalVisibleOutputId": "OUT-DL-DATA-LUR",
        "faultBypassHypothesisId": "EARLY-DATA",
    },
    "GUARD-TH-ACK-AFTER-MATCHING-WRQ": {
        "sourceRelationId": "SRC-LUR-ACK",
        "requiresState": ("TH-MATCHING-LUR-WRQ-RECEIVED=TRUE",),
        "normalVisibleOutputId": "OUT-TH-ACK-LUR",
        "faultBypassHypothesisId": "NO-FAULT-BYPASS",
    },
}
REQUIRED_OBJECT_STIMULI = {
    "STIM-LIST-SUBMISSION-PRECONDITION": ("SRC-LIST-OFFER-PRECONDITION", "EV_DL_OFFER_LIST", "APPLICATION"),
    "STIM-TH-LUS0001": ("SRC-LUS-READY", "EV_TH_LUS0001", "NETWORK-VISIBLE"),
    "STIM-TH-ACK-LUR": ("SRC-LUR-ACK", "EV_TH_ACK_LUR", "NETWORK-VISIBLE"),
}
REQUIRED_OBJECT_OUTPUTS = {
    "OUT-TH-ACK-LUR": ("SRC-LUR-ACK", "EV_TH_ACK_LUR", "NETWORK-VISIBLE"),
    "OUT-DL-WRQ-LUR": ("SRC-LUR-WRQ", "EV_DL_WRQ_LUR", "NETWORK-VISIBLE"),
    "OUT-DL-DATA-LUR": ("SRC-LUR-DATA", "EV_DL_DATA_LUR", "NETWORK-VISIBLE"),
}
REQUIRED_RESOURCE_CASE = {
    "actionId": "ACT-TEST-ACK-BEFORE-DATA",
    "event": "NO-DISPATCH-INSUFFICIENT-RESOURCE",
    "candidates": ("NORMAL", "EARLY-DATA"),
    "expectation": {
        "admission": "NOT-ADMITTED",
        "reason": "INSUFFICIENT-RESOURCE-BEFORE-DISPATCH",
        "mode": "ROUNDS",
        "availableRounds": 0,
        "requiredRounds": 1,
        "actionCostCharged": False,
        "successorDisposition": "PRE-DISPATCH-SUCCESSOR-UNCHANGED",
    },
}
REQUIRED_EXPERIMENT_INTERFACES = {
    "IF-EXP-SCENE",
    "IF-EXP-INJECT",
    "IF-EXP-TRUTH",
    "IF-EXP-COLLECT",
    "IF-EXP-RUN",
    "IF-EXP-FILTER",
    "IF-EXP-EVAL",
}
REQUIRED_EXPERIMENT_HANDOFFS = {
    "IF-EXP-SCENE": {
        "engineeringHandoff": "Stable scenario family, public configuration and preparation boundary only.",
        "publicProjection": "Scenario family, public configuration, preparation boundary and attempt identity only.",
        "evaluatorProjection": "No active fault, controller state or private loader state is released through this handoff.",
        "sharedComponentRisk": "Scenario and source interpretation are shared with the predictor and remain a disclosed common-mode risk.",
        "notAdmitted": "No formal experiment scenario, real-IUT run or qualified UPLOAD completion is admitted.",
    },
    "IF-EXP-INJECT": {
        "engineeringHandoff": "Installation, controller read-back, activation and unconfirmed-attempt records remain distinct.",
        "publicProjection": "Only the resulting visible journal may be consumed by the algorithm path.",
        "evaluatorProjection": "Named fault plan, controller read-back, activation record and unconfirmed disposition remain evaluator-only.",
        "sharedComponentRisk": "The controller, read-back and object branch are authored together; no independent injection oracle is claimed.",
        "notAdmitted": "An installed or planned variant is not automatically a confirmed fault truth or experimental injection plan.",
    },
    "IF-EXP-TRUTH": {
        "engineeringHandoff": "Evaluator-only surrogate truth with explicit shared-component risk.",
        "publicProjection": "No truth hypothesis, installation result or equivalence disposition enters the algorithm projection.",
        "evaluatorProjection": "Surrogate truth is retained only for later evaluator/audit comparison with its provenance.",
        "sharedComponentRisk": "Object, source interpretation, clock and event DTOs can be shared with the predictor or evaluator.",
        "notAdmitted": "No independent oracle, root-cause label or scientific detection claim is established.",
    },
    "IF-EXP-COLLECT": {
        "engineeringHandoff": "This run's visible journal and resource log only.",
        "publicProjection": "Current-run visible journal, resource log and stable attempt references only.",
        "evaluatorProjection": "Private controller/read-back records remain separate from the algorithm-visible collection.",
        "sharedComponentRisk": "Shared event serialization and journal ordering remain implementation risks to disclose.",
        "notAdmitted": "No cross-arm borrowing, historical capture truth, or complete evidence package is established.",
    },
    "IF-EXP-RUN": {
        "engineeringHandoff": "CL-LOOP engineering run, stop and trace identities only.",
        "publicProjection": "CL-LOOP engineering attempt identity, typed session context, stop and trace reference only.",
        "evaluatorProjection": "Evaluator truth and fault activation remain outside the typed session context.",
        "sharedComponentRisk": "The limited loop, predictor and adapter remain a single engineering chain, not independent arms.",
        "notAdmitted": "No four-arm runner, performance comparison or real-IUT execution is admitted.",
    },
    "IF-EXP-FILTER": {
        "engineeringHandoff": "Retain not-run, unconfirmed and invalid attempts for later accounting.",
        "publicProjection": "Named attempt disposition and trace reference are retained without silently deleting failures.",
        "evaluatorProjection": "Unconfirmed installation and invalid-record reasons remain available to audit accounting.",
        "sharedComponentRisk": "Disposition categories share the same engineering controller and are not an independent quality filter.",
        "notAdmitted": "No valid-sample denominator, scientific exclusion rule or confirmed experiment dataset is established.",
    },
    "IF-EXP-EVAL": {
        "engineeringHandoff": "Preserve linked evidence and permissions; do not calculate experiment metrics.",
        "publicProjection": "Linked public evidence and the declared permission boundary only.",
        "evaluatorProjection": "Evaluator/audit evidence remains associated by stable reference without becoming algorithm input.",
        "sharedComponentRisk": "Evidence comparison shares the scenario source and event model with the engineering chain.",
        "notAdmitted": "No detection, localization, answered denominator, effect size or formal experiment metric is calculated.",
    },
}
REQUIRED_WITNESSES = {
    "WIT-FINITE-NO-WRQ-TEST",
    "WIT-PUBLIC-SUMMARY",
    "WIT-P3-UNAVAILABLE",
    "WIT-SUCCESSOR-AND-RECOVER",
}
REQUIRED_TRANSLATION_KEYS = {
    "identity.title",
    "scope.summary",
    "scope.relationship.reason",
    "sourceRelations.SRC-LIST-OFFER-PRECONDITION.summary",
    "sourceRelations.SRC-LUS-READY.summary",
    "sourceRelations.SRC-LUR-WRQ.summary",
    "sourceRelations.SRC-LUR-ACK.summary",
    "sourceRelations.SRC-LUR-DATA.summary",
    "traceability.MAP-LIST-OFFER-PRECONDITION.summary",
    "traceability.MAP-NO-WRQ-FINITE-TEST.summary",
    "traceability.MAP-PREP-READY.summary",
    "traceability.MAP-LUR-ORDER-TEST.summary",
    "traceability.MAP-RECOVER-READY.summary",
    "hypotheses.NORMAL.summary",
    "hypotheses.EARLY-WRQ.summary",
    "hypotheses.EARLY-DATA.summary",
    "actions.ACT-INSPECT-NO-WRQ-BEFORE-READY.summary",
    "actions.ACT-PREP-ENTER-READY-WINDOW.summary",
    "actions.ACT-TEST-ACK-BEFORE-DATA.summary",
    "actions.ACT-RECOVER-RECONFIRM-READY.summary",
    "timeAndObservation.summary",
    "resourceContract.summary",
    "lifecycle.fullReset.summary",
    "lifecycle.faultInjection.summary",
    "lifecycle.recover.summary",
    "cases.CASE-NORMAL-CONTROL-TIMELINE.summary",
    "cases.CASE-EARLY-WRQ-TIMELINE.summary",
    "cases.CASE-EARLY-DATA-TIMELINE.summary",
    "cases.CASE-UNKNOWN-RECOVER-CONTINUATION.summary",
    "cases.CASE-RESOURCE-ADMISSION-BLOCK.summary",
    "experimentRelations.IF-EXP-SCENE.summary",
    "experimentRelations.IF-EXP-INJECT.summary",
    "experimentRelations.IF-EXP-TRUTH.summary",
    "experimentRelations.IF-EXP-COLLECT.summary",
    "experimentRelations.IF-EXP-RUN.summary",
    "experimentRelations.IF-EXP-FILTER.summary",
    "experimentRelations.IF-EXP-EVAL.summary",
    "limitations.0",
    "limitations.1",
    "limitations.2",
    "feasibilityWitnesses.WIT-FINITE-NO-WRQ-TEST.summary",
    "feasibilityWitnesses.WIT-PUBLIC-SUMMARY.summary",
    "feasibilityWitnesses.WIT-P3-UNAVAILABLE.summary",
    "feasibilityWitnesses.WIT-SUCCESSOR-AND-RECOVER.summary",
}
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
CONTROL_BASE_ROW_RE = re.compile(
    r"^\|\s*(Immutable base|不可变基点)\s*\|\s*`([0-9a-f]{40})`",
    re.MULTILINE,
)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _row_list(value: Any) -> list[dict[str, Any]]:
    return [row for row in value if isinstance(row, dict)] if isinstance(value, list) else []


def _duplicate_values(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if value and count > 1)


def _translation_errors(package: dict[str, Any]) -> list[str]:
    translations = package.get("translationsZh")
    if not isinstance(translations, dict):
        return ["BILINGUAL: translationsZh must be an object"]
    errors: list[str] = []
    actual = set(translations)
    missing = REQUIRED_TRANSLATION_KEYS - actual
    unexpected = actual - REQUIRED_TRANSLATION_KEYS
    if missing:
        errors.append("BILINGUAL: missing controlled Chinese fields: " + ", ".join(sorted(missing)))
    if unexpected:
        errors.append("BILINGUAL: unexpected controlled Chinese fields: " + ", ".join(sorted(unexpected)))
    for key in REQUIRED_TRANSLATION_KEYS & actual:
        value = translations.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"BILINGUAL: {key} must be nonblank Chinese-controlled text")
    return errors


def _index(rows: Any, label: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in _row_list(rows):
        row_id = row.get("id")
        if not isinstance(row_id, str) or not row_id:
            errors.append(f"{label}: row has no nonempty id")
            continue
        if row_id in indexed:
            errors.append(f"{label}: duplicate id {row_id}")
            continue
        indexed[row_id] = row
    return indexed


def _safe_relative(path: object) -> bool:
    if not isinstance(path, str) or not path or "\\" in path:
        return False
    posix = PurePosixPath(path)
    windows = PureWindowsPath(path)
    return (
        not posix.is_absolute()
        and not windows.is_absolute()
        and not windows.drive
        and ".." not in posix.parts
        and ".." not in windows.parts
    )


def _git_bytes(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.STDOUT)


def _control_authority_errors(root: Path, package: dict[str, Any]) -> list[str]:
    """Bind the package snapshot to the immutable base named by its G0 CR.

    The control document is read from the Git commit that first introduced it,
    not from the mutable worktree or from an authority commit declared by the
    package. Thus rebinding accepted-input rows cannot silently advance the
    controlled scenario authority baseline.
    """

    errors: list[str] = []
    identity = package.get("identity")
    binding = package.get("controlBinding")
    if not isinstance(identity, dict) or not isinstance(binding, dict):
        return ["CONTROL: identity and controlBinding must be objects"]
    if identity.get("changeRequest") != CONTROL_CHANGE_ID:
        errors.append("CONTROL: scenario package must remain bound to CR-2026-022")
    if binding.get("path") != CONTROL_CHANGE_PATH.as_posix():
        errors.append("CONTROL: controlBinding path must name the G0 change request")
        return errors

    control_commit = binding.get("controlCommit")
    control_oid = binding.get("gitBlobOid")
    control_hash = binding.get("rawSha256")
    if not isinstance(control_commit, str) or not SHA1_RE.fullmatch(control_commit):
        errors.append("CONTROL: controlBinding controlCommit is not a full lowercase Git SHA")
        return errors
    if not isinstance(control_oid, str) or not SHA1_RE.fullmatch(control_oid):
        errors.append("CONTROL: controlBinding gitBlobOid is not a full lowercase Git SHA")
        return errors
    if not isinstance(control_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", control_hash):
        errors.append("CONTROL: controlBinding rawSha256 is not a full lowercase SHA-256")
        return errors

    path = CONTROL_CHANGE_PATH.as_posix()
    try:
        additions = _git_bytes(
            root, "log", "--diff-filter=A", "--format=%H", "--", path
        ).decode("ascii", "strict").splitlines()
        if len(additions) != 1:
            errors.append("CONTROL: G0 change request must have exactly one Git introduction")
            return errors
        if control_commit != additions[0]:
            errors.append("CONTROL: controlBinding must use the first Git introduction of CR-2026-022")
            return errors
        listing = _git_bytes(root, "ls-tree", control_commit, "--", path).decode("utf-8", "strict").strip()
        if not listing:
            errors.append("CONTROL: G0 change request is not tracked at its control commit")
            return errors
        mode, _kind, _name = listing.partition("\t")[0].split(maxsplit=2)
        if mode not in {"100644", "100755"}:
            errors.append("CONTROL: G0 change request is not an ordinary Git file")
            return errors
        resolved_oid = _git_bytes(root, "rev-parse", f"{control_commit}:{path}").decode("ascii", "strict").strip()
        if resolved_oid != control_oid:
            errors.append("CONTROL: controlBinding Git blob OID does not match the immutable G0 document")
            return errors
        blob = _git_bytes(root, "cat-file", "blob", resolved_oid)
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError, ValueError) as exc:
        return [f"CONTROL: unable to load immutable G0 change request: {type(exc).__name__}"]

    if hashlib.sha256(blob).hexdigest() != control_hash:
        return ["CONTROL: controlBinding SHA-256 does not match the immutable G0 document"]
    try:
        document = blob.decode("utf-8-sig")
    except UnicodeDecodeError:
        return ["CONTROL: immutable G0 change request is not UTF-8 text"]
    rows = CONTROL_BASE_ROW_RE.findall(document)
    values = {label: value for label, value in rows}
    if len(rows) != 2 or set(values) != {"Immutable base", "不可变基点"}:
        return ["CONTROL: immutable G0 change request must state one English and one Chinese base row"]
    if len(set(values.values())) != 1:
        return ["CONTROL: English and Chinese immutable-base rows disagree"]
    immutable_base = next(iter(values.values()))
    if identity.get("acceptedAuthorityCommit") != immutable_base:
        errors.append("CONTROL: acceptedAuthorityCommit differs from the immutable CR-2026-022 base")
    try:
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", immutable_base, control_commit],
            cwd=root,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        errors.append("CONTROL: immutable base must be an ancestor of the G0 control commit")
    return errors


def _schema_errors(schema: Any, package: Any) -> list[str]:
    if not isinstance(schema, dict):
        return ["SCHEMA: schema root must be an object"]
    try:
        Draft202012Validator.check_schema(schema)
        errors = []
        for issue in Draft202012Validator(schema).iter_errors(package):
            location = ".".join(str(part) for part in issue.absolute_path) or "<root>"
            errors.append(f"SCHEMA {location}: {issue.message}")
        return sorted(errors)
    except SchemaError as exc:
        return [f"SCHEMA: invalid schema: {exc.message}"]
    except Exception as exc:  # pragma: no cover - defensive checker boundary
        return [f"SCHEMA: validation unavailable: {type(exc).__name__}: {exc}"]


def _snapshot_from_bindings(
    root: Path, package: dict[str, Any], errors: list[str]
) -> dict[str, bytes]:
    identity = package.get("identity")
    base = identity.get("acceptedAuthorityCommit") if isinstance(identity, dict) else None
    if not isinstance(base, str) or not SHA1_RE.fullmatch(base):
        errors.append("INPUT: acceptedAuthorityCommit is not a full lowercase Git SHA")
        return {}

    bindings = _row_list(package.get("acceptedInputs"))
    if len(bindings) != len(package.get("acceptedInputs", [])):
        errors.append("INPUT: acceptedInputs must contain objects only")
    for row in bindings:
        candidate_path = row.get("path")
        if not _safe_relative(candidate_path):
            errors.append(f"INPUT: unsafe binding path {candidate_path!r}")
    paths = [row.get("path") for row in bindings if isinstance(row.get("path"), str)]
    for value in _duplicate_values(paths):
        errors.append(f"INPUT: duplicate binding path {value}")
    by_path = {str(row.get("path", "")): row for row in bindings}
    for path in sorted(set(REQUIRED_BINDINGS) - set(by_path)):
        errors.append(f"INPUT: missing required binding {path}")
    for path in sorted(set(by_path) - set(REQUIRED_BINDINGS)):
        errors.append(f"INPUT: unexpected binding {path}")

    snapshot: dict[str, bytes] = {}
    for path, required_role in REQUIRED_BINDINGS.items():
        binding = by_path.get(path)
        if binding is None:
            continue
        if binding.get("role") != required_role:
            errors.append(f"INPUT: role mismatch for {path}; expected {required_role}")
        if binding.get("commit") != base:
            errors.append(f"INPUT: binding commit mismatch for {path}")
        raw_oid = binding.get("gitBlobOid")
        if not _safe_relative(path):
            errors.append(f"INPUT: unsafe binding path {path!r}")
            continue
        if not isinstance(raw_oid, str) or not SHA1_RE.fullmatch(raw_oid):
            errors.append(f"INPUT: invalid Git blob OID for {path}")
            continue
        try:
            listing = _git_bytes(root, "ls-tree", base, "--", path).decode("utf-8", "replace").strip()
            if not listing:
                errors.append(f"INPUT: bound path is not tracked at accepted commit: {path}")
                continue
            mode, _kind, remainder = listing.partition("\t")[0].split(maxsplit=2)
            if mode not in {"100644", "100755"}:
                errors.append(f"INPUT: bound path is not an ordinary Git file: {path}")
                continue
            resolved = _git_bytes(root, "rev-parse", f"{base}:{path}").decode("ascii", "strict").strip()
            if resolved != raw_oid:
                errors.append(f"INPUT: Git blob OID mismatch for {path}")
                continue
            blob = _git_bytes(root, "cat-file", "blob", resolved)
        except (OSError, subprocess.CalledProcessError, UnicodeDecodeError, ValueError) as exc:
            errors.append(f"INPUT: unable to load bound Git blob {path}: {type(exc).__name__}")
            continue
        if hashlib.sha256(blob).hexdigest() != binding.get("rawSha256"):
            errors.append(f"INPUT: SHA-256 mismatch for {path}")
            continue
        snapshot[path] = blob
    return snapshot


def _json_snapshot(snapshot: dict[str, bytes], path: str, errors: list[str]) -> dict[str, Any]:
    blob = snapshot.get(path)
    if blob is None:
        errors.append(f"INPUT: missing valid snapshot bytes for {path}")
        return {}
    try:
        value = json.loads(blob.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"INPUT: snapshot JSON is invalid for {path}: {type(exc).__name__}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"INPUT: snapshot root must be an object for {path}")
        return {}
    return value


def _enum_assignment(transition: dict[str, Any], target: str) -> str | None:
    for update in _row_list(transition.get("updates")):
        if update.get("kind") != "ASSIGN" or update.get("target") != target:
            continue
        value = update.get("value")
        if isinstance(value, dict) and value.get("kind") == "ENUM":
            rendered = value.get("value")
            return rendered if isinstance(rendered, str) else None
    return None


def _guard_enum(guard: Any, target: str) -> str | None:
    if not isinstance(guard, dict):
        return None
    if guard.get("kind") == "COMPARE":
        left = guard.get("left")
        right = guard.get("right")
        if (
            guard.get("op") == "EQ"
            and isinstance(left, dict)
            and isinstance(right, dict)
            and left.get("kind") == "VAR"
            and left.get("name") == target
            and right.get("kind") == "ENUM"
            and isinstance(right.get("value"), str)
        ):
            return str(right["value"])
    if guard.get("kind") == "AND":
        for child in guard.get("args", []):
            value = _guard_enum(child, target)
            if value is not None:
                return value
    return None


def _source_locator(source: Any) -> str | None:
    if not isinstance(source, dict):
        return None
    source_id = source.get("sourceId")
    clause = source.get("clause")
    table_or_figure = source.get("tableOrFigure")
    fragment_kind = source.get("fragmentKind")
    fragment_ordinal = source.get("fragmentOrdinal")
    if not all(isinstance(item, str) and item for item in (source_id, clause, table_or_figure, fragment_kind)):
        return None
    if not isinstance(fragment_ordinal, int) or fragment_ordinal < 1:
        return None
    return f"{source_id} §{clause} / {table_or_figure} / {fragment_kind} E{fragment_ordinal:03d}"


def _source_errors(package: dict[str, Any], snapshot: dict[str, bytes]) -> list[str]:
    errors: list[str] = []
    crs = _json_snapshot(snapshot, "configs/requirements/arinc_615a3_m1_crs.json", errors)
    m2 = _json_snapshot(snapshot, "configs/models/arinc_615a3_m2_model.json", errors)
    model = m2.get("model") if isinstance(m2.get("model"), dict) else {}
    requirements = _index(crs.get("requirements"), "SOURCE requirement", errors)
    transitions = _index(model.get("transitions"), "SOURCE transition", errors)
    events = _index(model.get("events"), "SOURCE event", errors)

    rows = _row_list(package.get("sourceRelations"))
    row_ids = _index(rows, "SOURCE relation", errors)
    actual_ids = set(row_ids)
    if actual_ids != set(REQUIRED_SOURCE_RELATIONS):
        errors.append("SOURCE: relations must be exactly the five declared UPLOAD control-slice anchors")
    for relation_id, expected in REQUIRED_SOURCE_RELATIONS.items():
        row = row_ids.get(relation_id)
        if row is None:
            continue
        for key in (
            "requirementId", "transitionId", "eventId", "eventDirection", "semanticOpcodeClass", "fileRole", "scenarioRationale", "scenarioRationaleZh", "visibility", "scenarioUse",
            "executedByScenario", "notWireOpcode",
        ):
            if row.get(key) != expected[key]:
                errors.append(f"SOURCE: {relation_id} {key} does not match the controlled relation")
        facts = row.get("stateFacts")
        if not isinstance(facts, dict):
            errors.append(f"SOURCE: {relation_id} stateFacts is missing")
        else:
            for field in ("before", "after"):
                if facts.get(field) != expected[field]:
                    errors.append(f"SOURCE: {relation_id} stateFacts.{field} is not the controlled state boundary")
            assertions = facts.get("assertions")
            actual_assertions = tuple(assertions) if isinstance(assertions, list) else ()
            if actual_assertions != expected["assertions"]:
                errors.append(f"SOURCE: {relation_id} stateFacts.assertions differ from the controlled source contract")

        requirement = requirements.get(str(row.get("requirementId", "")))
        transition = transitions.get(str(row.get("transitionId", "")))
        event = events.get(str(row.get("eventId", "")))
        if requirement is None:
            errors.append(f"SOURCE: {relation_id} references an unknown CRS requirement")
            continue
        if transition is None:
            errors.append(f"SOURCE: {relation_id} references an unknown M2 transition")
            continue
        if event is None:
            errors.append(f"SOURCE: {relation_id} references an unknown M2 event")
            continue
        if row.get("sourceUnitId") != requirement.get("sourceUnitId"):
            errors.append(f"SOURCE: {relation_id} sourceUnitId does not match the bound CRS")
        source = requirement.get("source") if isinstance(requirement.get("source"), dict) else {}
        if row.get("documentPage") != source.get("documentPage") or row.get("pdfPage") != source.get("pdfPage"):
            errors.append(f"SOURCE: {relation_id} document/PDF page does not match the bound CRS locator")
        locator = _source_locator(source)
        if locator is None or row.get("sourceLocator") != locator:
            errors.append(f"SOURCE: {relation_id} sourceLocator does not match the bound CRS locator")
        semantic = requirement.get("semantic") if isinstance(requirement.get("semantic"), dict) else {}
        for field in ("actor", "receiver", "action"):
            if row.get(field) != semantic.get(field):
                errors.append(f"SOURCE: {relation_id} {field} does not match the bound CRS semantic")
        if row.get("objects") != semantic.get("objects"):
            errors.append(f"SOURCE: {relation_id} objects do not match the bound CRS semantic")
        if transition.get("event") != row.get("eventId"):
            errors.append(f"SOURCE: {relation_id} transition does not consume its declared event")
        if row.get("requirementId") not in transition.get("requirementIds", []):
            errors.append(f"SOURCE: {relation_id} transition does not carry its declared CRS requirement")
        if transition.get("source") != expected["source"] or transition.get("target") != expected["target"]:
            errors.append(f"SOURCE: {relation_id} M2 source/target state does not match the controlled boundary")
        if event.get("visibility") != row.get("visibility"):
            errors.append(f"SOURCE: {relation_id} event visibility does not match M2")
        if bool(event.get("notAWireOpcode", False)) != bool(row.get("notWireOpcode")):
            errors.append(f"SOURCE: {relation_id} wire/application classification does not match M2")
        if row.get("eventDirection") == "APPLICATION-NO-WIRE":
            if event.get("direction") is not None:
                errors.append(f"SOURCE: {relation_id} application boundary must not manufacture a network direction")
        elif event.get("direction") != row.get("eventDirection"):
            errors.append(f"SOURCE: {relation_id} event direction does not match M2")

    wait = transitions.get("T_UPL_WAIT_LUS0001", {})
    wrq = transitions.get("T_UPL_LUR_WRQ", {})
    if _guard_enum(wait.get("guard"), "listOffered") != "TRUE":
        errors.append("SOURCE: T_UPL_WAIT_LUS0001 must guard listOffered=TRUE")
    if _guard_enum(wait.get("guard"), "listAccepted") != "FALSE":
        errors.append("SOURCE: T_UPL_WAIT_LUS0001 must guard listAccepted=FALSE")
    if _enum_assignment(wait, "targetListReady") != "TRUE" or _enum_assignment(wait, "listAccepted") is not None:
        errors.append("SOURCE: LUS-0001 must set target readiness without accepting the list")
    if _guard_enum(wrq.get("guard"), "listOffered") != "TRUE":
        errors.append("SOURCE: T_UPL_LUR_WRQ must guard listOffered=TRUE")
    if _guard_enum(wrq.get("guard"), "targetListReady") != "TRUE":
        errors.append("SOURCE: T_UPL_LUR_WRQ must guard targetListReady=TRUE")
    if _guard_enum(wrq.get("guard"), "listAccepted") != "FALSE" or _enum_assignment(wrq, "listAccepted") != "TRUE":
        errors.append("SOURCE: T_UPL_LUR_WRQ must read listAccepted=FALSE then write TRUE")

    return errors


def _boundary_errors(package: dict[str, Any]) -> list[str]:
    """Keep the controlled scenario scope and virtual observation non-protocol."""

    errors: list[str] = []
    scope = package.get("scope") if isinstance(package.get("scope"), dict) else {}
    if scope != REQUIRED_SCOPE:
        errors.append("SCOPE: controlled UPLOAD control-slice boundaries or non-claim obligations differ")
    observation = package.get("timeAndObservation") if isinstance(package.get("timeAndObservation"), dict) else {}
    if observation != REQUIRED_TIME_AND_OBSERVATION:
        errors.append("TIME: virtual finite-observation contract differs from the controlled engineering boundary")
    return errors


def _object_source_file_errors(root: Path) -> list[str]:
    """Check the current B source tree, not the separately pinned A authorities.

    This verifies safe tracked source presence and the declared loading hook;
    runtime code/source equality and immutable hashes are checked by that hook.
    No B module is imported or executed by this governance checker.
    """
    errors: list[str] = []
    try:
        entries = _git_bytes(root, "ls-files", "--stage", "-z", "--", *REQUIRED_OBJECT_SOURCE_FILES)
        tracked = {}
        for entry in entries.decode("utf-8").split("\0"):
            if entry:
                metadata, path = entry.split("\t", 1)
                mode, _, stage = metadata.split()
                tracked[path] = (mode, stage)
    except (OSError, subprocess.CalledProcessError, UnicodeError, ValueError) as exc:
        return [f"OBJECT-SOURCE: unable to verify source Git tracking: {type(exc).__name__}"]
    for relative in REQUIRED_OBJECT_SOURCE_FILES:
        if tracked.get(relative) not in {("100644", "0"), ("100755", "0")}:
            errors.append(f"OBJECT-SOURCE: source must be a tracked ordinary file: {relative}")
            continue
        path = root / relative
        try:
            components = [root.joinpath(*Path(relative).parts[:index]) for index in range(1, len(Path(relative).parts) + 1)]
            if any(
                part.is_symlink() or getattr(part.lstat(), "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
                for part in components
            ) or not path.resolve().is_relative_to(root.resolve()) or not stat.S_ISREG(path.lstat().st_mode):
                errors.append(f"OBJECT-SOURCE: unsafe or nonordinary source path: {relative}")
                continue
            tree = ast.parse(path.read_bytes(), filename=relative)
            last = tree.body[-1] if tree.body else None
            if not (
                isinstance(last, ast.Expr) and isinstance(last.value, ast.Call)
                and isinstance(last.value.func, ast.Name) and last.value.func.id == "register_loaded_module"
                and [ast.dump(arg) for arg in last.value.args] == [ast.dump(ast.Name(id=name, ctx=ast.Load())) for name in ("__name__", "__file__")]
                and not last.value.keywords
            ):
                errors.append(f"OBJECT-SOURCE: source must register its executing module frame: {relative}")
            if relative.endswith("/controller.py") and not any(
                isinstance(node, ast.ClassDef) and node.name == "LurStartController" for node in tree.body
            ):
                errors.append("OBJECT-SOURCE: declared controller entry point is absent")
        except (OSError, SyntaxError, ValueError) as exc:
            errors.append(f"OBJECT-SOURCE: source unavailable or invalid: {relative}: {type(exc).__name__}")
    return errors


def _object_contract_errors(package: dict[str, Any]) -> list[str]:
    """Validate the bounded B-stage object/peer contract and its non-claims."""

    errors: list[str] = []
    contract = package.get("objectContract") if isinstance(package.get("objectContract"), dict) else {}
    if contract.get("stage") != REQUIRED_OBJECT_STAGE:
        errors.append("OBJECT: contract must retain the controlled B-stage object-lifecycle candidate state")
    if contract.get("objectKind") != "IN-PROCESS-CONTROLLED-DATA-LOADER-SURROGATE":
        errors.append("OBJECT: object kind must remain the controlled in-process loader surrogate")
    if contract.get("peerKind") != "IN-PROCESS-CONTROLLED-TARGET-HARDWARE-DRIVER":
        errors.append("OBJECT: peer kind must remain the controlled in-process TH driver")

    states = _index(contract.get("stateVariables"), "OBJECT state", errors)
    actual_states = {
        state_id: (row.get("sourceAnchor"), row.get("initial"))
        for state_id, row in states.items()
    }
    if actual_states != REQUIRED_OBJECT_STATES:
        errors.append("OBJECT: loader/peer state variables must retain the controlled source anchors and initial values")
    for state_id, row in states.items():
        if row.get("owner") != REQUIRED_OBJECT_OWNERS.get(state_id):
            errors.append(f"OBJECT: {state_id} must retain its controlled loader/peer ownership")
        for field in ("invariant", "meaningZh"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(f"OBJECT: {state_id} requires nonblank {field}")
        if row.get("invariant") != REQUIRED_OBJECT_STATE_INVARIANTS.get(state_id):
            errors.append(f"OBJECT: {state_id} invariant differs from the controlled state contract")

    sources = _index(package.get("sourceRelations"), "OBJECT source", errors)
    guards = _index(contract.get("guardTransitions"), "OBJECT guard", errors)
    if set(guards) != set(REQUIRED_OBJECT_GUARDS):
        errors.append("OBJECT: contract must define exactly the WRQ, TH-ACK and matching-ACK guards")
    outputs = _index(contract.get("visibleOutputs"), "OBJECT output", errors)
    stimuli = _index(contract.get("publicStimuli"), "OBJECT stimulus", errors)
    for label, rows, expected in (
        ("stimulus", stimuli, REQUIRED_OBJECT_STIMULI),
        ("output", outputs, REQUIRED_OBJECT_OUTPUTS),
    ):
        if set(rows) != set(expected):
            errors.append(f"OBJECT: public {label} IDs differ from the controlled contract")
        for row_id, required in expected.items():
            row = rows.get(row_id)
            if row is None:
                continue
            actual = (row.get("sourceRelationId"), row.get("eventId"), row.get("visibility"))
            if actual != required:
                errors.append(f"OBJECT: {row_id} does not match its source/event/visibility contract")
            relation = sources.get(str(row.get("sourceRelationId")))
            if relation is None or relation.get("eventId") != row.get("eventId") or relation.get("visibility") != row.get("visibility"):
                errors.append(f"OBJECT: {row_id} is not bound to the declared source relation")
            if not isinstance(row.get("meaningZh"), str) or not row["meaningZh"].strip():
                errors.append(f"OBJECT: {row_id} requires nonblank Chinese-controlled meaning")
    for guard_id, expected in REQUIRED_OBJECT_GUARDS.items():
        guard = guards.get(guard_id)
        if guard is None:
            continue
        diagnostic_name = "TH-ACK guard" if guard_id == "GUARD-TH-ACK-AFTER-MATCHING-WRQ" else guard_id
        for field, required in expected.items():
            actual = tuple(guard.get(field, ())) if field == "requiresState" else guard.get(field)
            if actual != required:
                errors.append(f"OBJECT: {diagnostic_name} {field} differs from the controlled guard contract")
        if guard.get("sourceRelationId") not in sources:
            errors.append(f"OBJECT: {guard_id} references an unknown source relation")
        if guard.get("normalVisibleOutputId") not in outputs:
            errors.append(f"OBJECT: {guard_id} references an unknown visible output")
        if not isinstance(guard.get("meaningZh"), str) or not guard["meaningZh"].strip():
            errors.append(f"OBJECT: {guard_id} requires nonblank Chinese-controlled meaning")

    payload = contract.get("semanticPayloadBoundary") if isinstance(contract.get("semanticPayloadBoundary"), dict) else {}
    if (
        payload.get("fileRole") != "LUR"
        or set(payload.get("semanticOpcodes", [])) != {"WRQ", "ACK", "DATA"}
        or payload.get("payloadRepresentation") != "OPAQUE-NO-LUR-BYTE-PAYLOAD-OR-CHECKSUM-EVALUATED"
        or payload.get("notWirePacketImplementation") is not True
    ):
        errors.append("OBJECT: semantic file-role/opcode/opaque-payload boundary is incomplete")

    domain = package.get("hypothesisDomain") if isinstance(package.get("hypothesisDomain"), dict) else {}
    private = contract.get("privateBoundary") if isinstance(contract.get("privateBoundary"), dict) else {}
    permitted = set(private.get("permittedAlgorithmProjection", [])) if isinstance(private.get("permittedAlgorithmProjection"), list) else set()
    may_know = set(domain.get("algorithmMayKnow", [])) if isinstance(domain.get("algorithmMayKnow"), list) else set()
    forbidden = set(domain.get("algorithmMustNotReceive", [])) if isinstance(domain.get("algorithmMustNotReceive"), list) else set()
    if set(private.get("evaluatorOnly", [])) != forbidden or set(private.get("algorithmForbidden", [])) != forbidden:
        errors.append("OBJECT: evaluator-only and algorithm-forbidden projections must match the declared domain boundary")
    if set(private.get("permittedAlgorithmProjection", [])) != {
        "DECLARED-HYPOTHESIS-DOMAIN",
        "DECLARED-PREDICTIONS",
        "PUBLIC-SCENE-CONFIGURATION",
        "TYPED-ACTION-AND-OBSERVATION-INTERFACE",
    }:
        errors.append("OBJECT: permitted algorithm projection differs from the controlled typed interface boundary")
    if not may_know <= permitted or may_know & forbidden or may_know & set(private.get("evaluatorOnly", [])):
        errors.append("OBJECT: algorithm-visible hypothesis data must remain disjoint from evaluator-only fields")

    lifecycle_boundary = contract.get("lifecycleBoundary") if isinstance(contract.get("lifecycleBoundary"), dict) else {}
    fault = package.get("lifecycle", {}).get("faultInjection", {}) if isinstance(package.get("lifecycle"), dict) else {}
    for object_field, fault_field in (
        ("faultInstallationLifetime", "installationLifetime"),
        ("faultRevocationAction", "revocationAction"),
        ("revocationEvidence", "revocationEvidence"),
    ):
        if lifecycle_boundary.get(object_field) != fault.get(fault_field):
            errors.append("OBJECT: lifecycle boundary must agree with fault installation/revocation contract")
            break

    identity = contract.get("implementationIdentityPlan") if isinstance(contract.get("implementationIdentityPlan"), dict) else {}
    if identity.get("status") != REQUIRED_OBJECT_IDENTITY_STATUS:
        errors.append("OBJECT: implementation identity must retain the controlled B-stage candidate status")
    if identity.get("sourceRoot") != REQUIRED_OBJECT_SOURCE_ROOT:
        errors.append("OBJECT: implementation source root differs from the controlled bounded object package")
    if identity.get("entryPoint") != REQUIRED_OBJECT_ENTRY_POINT:
        errors.append("OBJECT: implementation entry point differs from the controlled direct lifecycle controller")
    binding = identity.get("sourceBinding", {})
    if any(binding.get(key) != value for key, value in REQUIRED_OBJECT_SOURCE_BINDING.items()):
        errors.append("OBJECT-SOURCE: loaded source binding policy differs from the controlled B contract")
    if set(binding.get("files", [])) != set(REQUIRED_OBJECT_SOURCE_FILES):
        errors.append("OBJECT-SOURCE: binding must cover the exact five B source modules")
    for field in ("meaning", "meaningZh"):
        if not isinstance(binding.get(field), str) or not binding[field].strip():
            errors.append(f"OBJECT-SOURCE: binding requires nonblank {field}")
    if set(identity.get("requiredAtImplementation", [])) != {
        "OBJECT-SOURCE-COMMIT",
        "OBJECT-DISTRIBUTION-IDENTITY",
        "ADAPTER-SOURCE-IDENTITY",
    }:
        errors.append("OBJECT: downstream implementation identity requirements are incomplete")
    if identity.get("notEstablished") != REQUIRED_OBJECT_NOT_ESTABLISHED:
        errors.append("OBJECT: B-stage non-claim identity boundary differs from the controlled contract")
    if identity.get("notEstablishedZh") != REQUIRED_OBJECT_NOT_ESTABLISHED_ZH:
        errors.append("OBJECT: B-stage Chinese non-claim identity boundary differs from the controlled contract")
    return errors


def _action_and_case_errors(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    domain = package.get("hypothesisDomain") if isinstance(package.get("hypothesisDomain"), dict) else {}
    if domain != REQUIRED_HYPOTHESIS_DOMAIN:
        errors.append("DOMAIN: finite hypotheses, visibility and coverage limit differ from the controlled engineering contract")
    members = _index(domain.get("members"), "DOMAIN hypothesis", errors)
    if {key: row.get("kind") for key, row in members.items()} != REQUIRED_HYPOTHESES:
        errors.append("DOMAIN: members must be NORMAL, EARLY-WRQ and EARLY-DATA with their controlled kinds")
    forbidden = set(domain.get("algorithmMustNotReceive", [])) if isinstance(domain.get("algorithmMustNotReceive"), list) else set()
    may_know = set(domain.get("algorithmMayKnow", [])) if isinstance(domain.get("algorithmMayKnow"), list) else set()
    if may_know & forbidden:
        errors.append("DOMAIN: algorithmMayKnow must be disjoint from algorithmMustNotReceive")
    if not isinstance(domain.get("coverageLimitZh"), str) or not domain["coverageLimitZh"].strip():
        errors.append("BILINGUAL: finite-domain coverage limit requires controlled Chinese semantics")

    actions = _index(package.get("actionLibrary"), "ACTION", errors)
    if {key: row.get("kind") for key, row in actions.items()} != REQUIRED_ACTION_KINDS:
        errors.append("ACTION: library must contain exactly the four controlled TEST/PREP/RECOVER actions")
    all_hypotheses = set(members)
    observed_outcomes: dict[str, set[tuple[str, str, tuple[str, ...]]]] = {}
    for action_id, action in actions.items():
        private = action.get("summaryDerivation", {}).get("forbiddenPrivateSources") if isinstance(action.get("summaryDerivation"), dict) else None
        public = action.get("summaryDerivation", {}).get("publicSources") if isinstance(action.get("summaryDerivation"), dict) else None
        if not isinstance(private, list) or not {"ACTIVE-FAULT-ID", "FAULT-ACTIVATION-RECORD", "PRIVATE-LOADER-STATE"} <= set(private):
            errors.append(f"ACTION: {action_id} does not prohibit all private summary sources")
        if not isinstance(public, list) or set(public) != REQUIRED_PUBLIC_SUMMARY_SOURCES.get(action_id, set()):
            errors.append(f"ACTION: {action_id} does not derive confirmation from a public journal")
        projection = action.get("summaryDerivation", {}).get("publicEvidenceProjection") if isinstance(action.get("summaryDerivation"), dict) else None
        if projection != REQUIRED_PUBLIC_EVIDENCE_PROJECTIONS.get(action_id):
            errors.append(f"ACTION: {action_id} public evidence projection differs from the controlled contract")
        inspection_projection = action.get("inspection") if isinstance(action.get("inspection"), dict) else {}
        if isinstance(projection, dict) and projection.get("completionReceipt") != inspection_projection.get("completionReceipt"):
            errors.append(f"ACTION: {action_id} public evidence projection receipt must match its inspection receipt")
        expected_return = REQUIRED_ACTION_RETURN_CONTRACTS.get(action_id)
        if expected_return is not None and (
            action.get("successorConfirmation"), action.get("unconfirmedEffectDisposition")
        ) != expected_return:
            errors.append(f"ACTION: {action_id} successor confirmation or unconfirmed-effect contract differs")
        if action.get("historyDisposition") != "SUBMIT-CONFIRMED-SUMMARY-THROUGH-IF-HIST-UPDATE":
            errors.append(f"ACTION: {action_id} must submit only a confirmed summary through IF-HIST-UPDATE")
        if action_id == "ACT-PREP-ENTER-READY-WINDOW":
            if action.get("prepEffectBranches") != REQUIRED_PREP_EFFECT_BRANCHES:
                errors.append("ACTION: Prep effect-branch contract differs from the controlled disposition table")
        detail = REQUIRED_ACTION_DETAILS.get(action_id)
        if detail is not None:
            inspection_detail = action.get("inspection") if isinstance(action.get("inspection"), dict) else {}
            actual_inspection = (
                inspection_detail.get("completionReceipt"),
                inspection_detail.get("journalPredicate"),
                inspection_detail.get("finiteHorizonTicks"),
                inspection_detail.get("isProtocolNoResponseVerdict"),
                inspection_detail.get("fabricatedProtocolResponse"),
            )
            cost = action.get("cost") if isinstance(action.get("cost"), dict) else {}
            actual_cost = tuple(cost.get(field) for field in ("acquisition", "computation", "preparation", "retry"))
            actual_outcomes = tuple(
                (
                    outcome.get("observable"),
                    outcome.get("postSummary"),
                    outcome.get("summaryConfirmedWhen"),
                    tuple(outcome.get("compatibleHypotheses", ())),
                )
                for outcome in _row_list(action.get("possibleOutcomes"))
            )
            if (
                action.get("eligibility") != detail["eligibility"]
                or actual_cost != detail["cost"]
                or action.get("publicStimulus") != detail["publicStimulus"]
                or action.get("observationMode") != detail["observationMode"]
                or actual_inspection != detail["inspection"]
                or actual_outcomes != detail["outcomes"]
                or tuple(action.get("nonEvaluatedObligations", ())) != detail["nonEvaluatedObligations"]
            ):
                errors.append(f"ACTION: {action_id} detailed action/observation/cost contract differs")
        localized = action.get("zh") if isinstance(action.get("zh"), dict) else {}
        for field in (
            "eligibility", "publicStimulus", "observationMode", "successorConfirmation",
            "unconfirmedEffectDisposition", "historyDisposition",
        ):
            if not isinstance(localized.get(field), str) or not localized[field].strip():
                errors.append(f"BILINGUAL: {action_id} requires a nonblank Chinese {field} field")
        if action_id == "ACT-PREP-ENTER-READY-WINDOW":
            localized_branches = localized.get("prepEffectBranches")
            if not isinstance(localized_branches, dict) or set(localized_branches) != set(REQUIRED_PREP_EFFECT_BRANCHES) or any(
                not isinstance(value, str) or not value.strip() for value in localized_branches.values()
            ):
                errors.append("BILINGUAL: Prep effect-branch contract requires all nonblank Chinese branch semantics")
        outcomes: set[tuple[str, str, tuple[str, ...]]] = set()
        declared_outcomes = _row_list(action.get("possibleOutcomes"))
        for outcome in declared_outcomes:
            compatible = outcome.get("compatibleHypotheses")
            candidate_set = tuple(compatible) if isinstance(compatible, list) else ()
            if not candidate_set or not set(candidate_set) <= all_hypotheses:
                errors.append(f"ACTION: {action_id} outcome references an undeclared hypothesis")
            if not isinstance(outcome.get("summaryConfirmedWhenZh"), str) or not outcome["summaryConfirmedWhenZh"].strip():
                errors.append(f"BILINGUAL: {action_id} outcome requires Chinese summary confirmation semantics")
            outcomes.add((str(outcome.get("observable", "")), str(outcome.get("postSummary", "")), candidate_set))
        if not outcomes:
            errors.append(f"ACTION: {action_id} has no usable possible outcome")
        if len(declared_outcomes) != REQUIRED_ACTION_OUTCOME_COUNTS.get(action_id) or len(outcomes) != len(declared_outcomes):
            errors.append(f"ACTION: {action_id} must retain its complete, non-duplicated finite outcome relation")
        observed_outcomes[action_id] = outcomes

    inspect = actions.get("ACT-INSPECT-NO-WRQ-BEFORE-READY", {})
    if inspect.get("observationMode") != "FINITE-ENGINEERING-LOG-CHECK":
        errors.append("ACTION: no-WRQ action must be a finite engineering log check")
    inspection = inspect.get("inspection") if isinstance(inspect.get("inspection"), dict) else {}
    if inspection.get("isProtocolNoResponseVerdict") is not False or inspection.get("fabricatedProtocolResponse") is not False:
        errors.append("ACTION: no-WRQ action must not manufacture a protocol no-response verdict or response")
    expected_inspection_outcomes = {
        ("NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001", "Q-PRE-READY-NO-WRQ", ("NORMAL", "EARLY-DATA")),
        ("EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001", "Q-EARLY-WRQ-OBSERVED", ("EARLY-WRQ",)),
    }
    if observed_outcomes.get("ACT-INSPECT-NO-WRQ-BEFORE-READY") != expected_inspection_outcomes:
        errors.append("ACTION: no-WRQ action must keep the finite public early-WRQ and no-WRQ outcome split")
    if actions.get("ACT-PREP-ENTER-READY-WINDOW", {}).get("cost", {}).get("preparation") != 1:
        errors.append("ACTION: Prep must declare one preparation cost")
    if actions.get("ACT-RECOVER-RECONFIRM-READY", {}).get("kind") != "RECOVER":
        errors.append("ACTION: UNKNOWN continuation requires a distinct Recover action")

    resource = package.get("resourceContract") if isinstance(package.get("resourceContract"), dict) else {}
    if resource.get("admissionOwner") != "IF-SELECT-ADMIT" or resource.get("accountingOwner") != "REFERENCE-SESSION":
        errors.append("RESOURCE: existing admission/accounting ownership is not retained")
    if set(resource.get("allowedModes", [])) != {"ROUNDS", "BUDGET"}:
        errors.append("RESOURCE: controlled modes must be exactly ROUNDS and BUDGET")
    if resource.get("admissionBoundary") != "CHECK-BEFORE-DISPATCH" or resource.get("postDispatchError") != "CHARGE-ONCE-PRESERVE-ACTUAL-SUCCESSOR":
        errors.append("RESOURCE: pre-dispatch admission or post-dispatch successor boundary is incomplete")
    for field, expected in REQUIRED_RESOURCE_TEXT.items():
        if resource.get(field) != expected:
            errors.append(f"RESOURCE: {field} must retain the controlled non-interchangeable meaning")
    localized_resource = resource.get("zh") if isinstance(resource.get("zh"), dict) else {}
    for field in ("roundsMeaning", "budgetMeaning", "admissionBoundary", "postDispatchError", "notEvaluated"):
        if not isinstance(localized_resource.get(field), str) or not localized_resource[field].strip():
            errors.append(f"BILINGUAL: resource contract requires nonblank Chinese {field} semantics")
    if set(resource.get("notEvaluated", [])) != {"REAL-HARDWARE-COST", "EXPERIMENT-ARM-FAIRNESS"}:
        errors.append("RESOURCE: non-claim boundaries are incomplete")

    cases = _index(package.get("cases"), "CASE", errors)
    if set(cases) != REQUIRED_CASE_IDS:
        errors.append("CASE: package must contain exactly the four controlled design witnesses")
    for case_id, case in cases.items():
        if case.get("initialContext") != REQUIRED_CASE_INITIAL_CONTEXTS.get(case_id):
            errors.append(f"CASE: {case_id} initial context must retain the controlled H/q/session/prefix boundary")
        if case_id == "CASE-UNKNOWN-RECOVER-CONTINUATION":
            if case.get("unknownRecoverContract") != REQUIRED_UNKNOWN_RECOVER_CONTRACT:
                errors.append("CASE: UNKNOWN Recover contract must retain its trigger, successor, journal and no-rewind boundary")
        elif "unknownRecoverContract" in case:
            errors.append(f"CASE: {case_id} must not declare an UNKNOWN Recover contract")
        rounds = _row_list(case.get("rounds"))
        if [round_.get("round") for round_ in rounds] != list(range(1, len(rounds) + 1)):
            errors.append(f"CASE: {case_id} rounds must be sequential beginning at one")
        for index, round_ in enumerate(rounds):
            action_id = round_.get("actionId")
            if action_id not in actions:
                errors.append(f"CASE: {case_id} references an unknown action {action_id}")
                continue
            candidates = round_.get("expectedCandidates")
            if not isinstance(candidates, list) or not candidates or not set(candidates) <= all_hypotheses:
                errors.append(f"CASE: {case_id} has an invalid expected candidate set")
            if round_.get("continues") is False and index != len(rounds) - 1:
                errors.append(f"CASE: {case_id} runs an action after a declared stop")
            summary = round_.get("expectedPublicSummary")
            if summary == "NONE":
                if case_id not in {"CASE-UNKNOWN-RECOVER-CONTINUATION", "CASE-RESOURCE-ADMISSION-BLOCK"}:
                    errors.append(f"CASE: only UNKNOWN or pre-dispatch resource witnesses may have no confirmed summary")
                continue
            outcomes = observed_outcomes.get(str(action_id), set())
            expected = tuple(candidates) if isinstance(candidates, list) else ()
            if not any(item[1] == summary and item[2] == expected for item in outcomes):
                errors.append(f"CASE: {case_id} round {index + 1} does not consume an action outcome with its declared summary/candidates")
        if case.get("afterStopMayEmitEvents") is not False:
            errors.append(f"CASE: {case_id} must forbid post-stop events")
        expected_timeline = REQUIRED_CASE_TIMELINES.get(case_id)
        actual_timeline = tuple(
            (
                round_.get("actionId"),
                tuple(round_.get("expectedVisibleEvents", ())),
                round_.get("expectedPublicSummary"),
                tuple(round_.get("expectedCandidates", ())),
                round_.get("continues"),
            )
            for round_ in rounds
        )
        if expected_timeline is not None and actual_timeline != expected_timeline:
            errors.append(f"CASE: {case_id} timeline differs from the controlled action/event/summary/candidate relation")
    resource_case = cases.get("CASE-RESOURCE-ADMISSION-BLOCK", {})
    resource_rounds = _row_list(resource_case.get("rounds"))
    if len(resource_rounds) != 1:
        errors.append("CASE: resource-admission witness must contain exactly one non-dispatched round")
    else:
        round_ = resource_rounds[0]
        if (
            round_.get("actionId") != REQUIRED_RESOURCE_CASE["actionId"]
            or tuple(round_.get("expectedVisibleEvents", ())) != (REQUIRED_RESOURCE_CASE["event"],)
            or tuple(round_.get("expectedCandidates", ())) != REQUIRED_RESOURCE_CASE["candidates"]
            or round_.get("expectedPublicSummary") != "NONE"
            or round_.get("continues") is not False
            or round_.get("resourceExpectation") != REQUIRED_RESOURCE_CASE["expectation"]
        ):
            errors.append("CASE: resource-admission witness must retain pre-dispatch no-charge/no-successor-change semantics")
    lifecycle = package.get("lifecycle") if isinstance(package.get("lifecycle"), dict) else {}
    full_reset = lifecycle.get("fullReset") if isinstance(lifecycle.get("fullReset"), dict) else {}
    required_reset = {"LOADER-STATE", "TH-STATE", "VIRTUAL-CLOCK", "EVENT-JOURNAL", "PENDING-DELIVERY", "CORRELATION-ID-SEQUENCE", "FAULT-INSTALLATION-STATE"}
    if set(full_reset.get("scope", [])) != required_reset or full_reset.get("notProtocolAbort") is not True:
        errors.append("LIFECYCLE: full reset scope or abort boundary is incomplete")
    if full_reset.get("successEvidence") != REQUIRED_LIFECYCLE_EVIDENCE["fullReset"]["successEvidence"]:
        errors.append("LIFECYCLE: full reset success evidence differs from the controlled contract")
    recover = lifecycle.get("recover") if isinstance(lifecycle.get("recover"), dict) else {}
    if recover.get("requires") != "UNKNOWN-EFFECT" or recover.get("targetAndSummaryAreDistinct") is not True or recover.get("confirmationFailureDisposition") != "DO-NOT-MARK-KNOWN":
        errors.append("LIFECYCLE: Recover must retain the controlled UNKNOWN/confirmation contract")
    fault = lifecycle.get("faultInjection") if isinstance(lifecycle.get("faultInjection"), dict) else {}
    for field, expected in REQUIRED_LIFECYCLE_EVIDENCE["faultInjection"].items():
        if fault.get(field) != expected:
            errors.append(f"LIFECYCLE: fault {field} differs from the controlled evidence contract")
    if (
        fault.get("installationLifetime") != "CURRENT-ENGINEERING-ATTEMPT-UNTIL-FULL-RESET"
        or fault.get("revocationAction") != "FULL-RESET-REVOKES-ALL-NAMED-VARIANTS"
        or fault.get("revocationEvidence") != "RESET-READBACK-FAULT-INSTALLATION-STATE-CLEARED"
        or fault.get("revocationFailureDisposition") != "RETAIN-ATTEMPT-AS-INVALID-NOT-NORMAL"
    ):
        errors.append("LIFECYCLE: fault revocation/lifetime contract is incomplete")
    variants: dict[str, dict[str, Any]] = {}
    for row in _row_list(fault.get("variants")):
        hypothesis_id = row.get("hypothesisId")
        if not isinstance(hypothesis_id, str) or not hypothesis_id or hypothesis_id in variants:
            errors.append("LIFECYCLE: fault variants require unique nonblank hypothesisId values")
            continue
        variants[hypothesis_id] = row
    if set(variants) != set(REQUIRED_FAULT_VARIANTS):
        errors.append("LIFECYCLE: fault variants must cover exactly EARLY-WRQ and EARLY-DATA")
    for hypothesis_id, expected in REQUIRED_FAULT_VARIANTS.items():
        variant = variants.get(hypothesis_id)
        if variant is None:
            continue
        for field, value in expected.items():
            if variant.get(field) != value:
                errors.append(f"LIFECYCLE: {hypothesis_id} {field} differs from the controlled injection contract")
    return errors


def _traceability_errors(package: dict[str, Any], snapshot: dict[str, bytes]) -> list[str]:
    """Close every scenario action/state to source, existing interface and witness."""

    errors: list[str] = []
    registry = _json_snapshot(snapshot, "configs/research/cltav_interface_registry.json", errors)
    interfaces = _index(registry.get("interfaces"), "TRACE interface", errors)
    relations = _index(package.get("sourceRelations"), "TRACE source relation", errors)
    actions = _index(package.get("actionLibrary"), "TRACE action", errors)
    witnesses = _index(package.get("feasibilityWitnesses"), "TRACE witness", errors)
    rows = _index(package.get("traceabilityMatrix"), "TRACE matrix", errors)
    if set(rows) != set(REQUIRED_TRACEABILITY_RELATIONS):
        errors.append("TRACE: matrix must contain exactly the five controlled action/state mappings")
    for relation_id, expected in REQUIRED_TRACEABILITY_RELATIONS.items():
        row = rows.get(relation_id)
        if row is None:
            continue
        for field in ("stateOrActionId", "interfaceUse"):
            if row.get(field) != expected[field]:
                errors.append(f"TRACE: {relation_id} {field} differs from the controlled interface relation")
        for field in ("sourceRelationIds", "existingInterfaceIds", "acceptanceWitnessIds"):
            values = row.get(field)
            actual = tuple(values) if isinstance(values, list) else ()
            if actual != expected[field]:
                errors.append(f"TRACE: {relation_id} {field} differs from the controlled relation")
            if len(actual) != len(set(actual)):
                errors.append(f"TRACE: {relation_id} {field} contains a duplicate reference")
        if not isinstance(row.get("visibleEvidence"), str) or not row["visibleEvidence"].strip():
            errors.append(f"TRACE: {relation_id} requires named visible evidence")
        not_covered = row.get("notCovered")
        if not isinstance(not_covered, list) or not not_covered or not all(isinstance(value, str) and value for value in not_covered):
            errors.append(f"TRACE: {relation_id} must retain a nonempty non-claim boundary")
        state_or_action = row.get("stateOrActionId")
        if state_or_action != "LIST-SUBMISSION-PRECONDITION-RECORDED" and state_or_action not in actions:
            errors.append(f"TRACE: {relation_id} does not bind a declared action or the named preparation state")
        for source_id in row.get("sourceRelationIds", []):
            if source_id not in relations:
                errors.append(f"TRACE: {relation_id} references an unknown source relation {source_id}")
        for interface_id in row.get("existingInterfaceIds", []):
            declared = interfaces.get(str(interface_id))
            if declared is None:
                errors.append(f"TRACE: {relation_id} references an unknown existing interface {interface_id}")
                continue
            expected_outputs = REQUIRED_INTERFACE_OUTPUTS.get(str(interface_id), set())
            outputs = declared.get("outputs")
            if not isinstance(outputs, list) or not expected_outputs <= set(outputs):
                errors.append(f"TRACE: {relation_id} existing interface {interface_id} lacks its bound output contract")
        for witness_id in row.get("acceptanceWitnessIds", []):
            if witness_id not in witnesses:
                errors.append(f"TRACE: {relation_id} references an unknown acceptance witness {witness_id}")
    return errors


def _experiment_and_limit_errors(package: dict[str, Any], snapshot: dict[str, bytes]) -> list[str]:
    errors: list[str] = []
    registry = _json_snapshot(snapshot, "configs/research/cltav_interface_registry.json", errors)
    design = _json_snapshot(snapshot, "configs/research/cltav_experiment_design.json", errors)
    declared_interfaces = _index(registry.get("experimentInterfaces"), "INTERFACE", errors)
    relations: dict[str, dict[str, Any]] = {}
    for relation in _row_list(package.get("experimentRelations")):
        interface_id = relation.get("interfaceId")
        if not isinstance(interface_id, str) or not interface_id:
            errors.append("EXPERIMENT: relation has no nonempty interfaceId")
            continue
        if interface_id in relations:
            errors.append(f"EXPERIMENT: duplicate relation for {interface_id}")
            continue
        relations[interface_id] = relation
    if set(relations) != REQUIRED_EXPERIMENT_INTERFACES:
        errors.append("EXPERIMENT: relations must include exactly the seven IF-EXP handoffs")
    for interface_id in REQUIRED_EXPERIMENT_INTERFACES:
        if interface_id not in declared_interfaces:
            errors.append(f"EXPERIMENT: bound registry is missing {interface_id}")
        relation = relations.get(interface_id)
        if relation is None or not isinstance(relation.get("engineeringHandoff"), str) or not relation["engineeringHandoff"].strip():
            errors.append(f"EXPERIMENT: missing engineering handoff for {interface_id}")
            continue
        expected_handoff = REQUIRED_EXPERIMENT_HANDOFFS[interface_id]
        if any(relation.get(field) != value for field, value in expected_handoff.items()):
            errors.append(f"EXPERIMENT: {interface_id} handoff/private-boundary/non-admission contract differs")
        for field in ("publicProjection", "evaluatorProjection", "sharedComponentRisk", "notAdmitted"):
            if not isinstance(relation.get(field), str) or not relation[field].strip():
                errors.append(f"EXPERIMENT: {interface_id} requires a named {field}")
        localized = relation.get("zh") if isinstance(relation.get("zh"), dict) else {}
        for field in ("engineeringHandoff", "publicProjection", "evaluatorProjection", "sharedComponentRisk", "notAdmitted"):
            if not isinstance(localized.get(field), str) or not localized[field].strip():
                errors.append(f"BILINGUAL: {interface_id} requires Chinese {field} semantics")
    scope = package.get("scope") if isinstance(package.get("scope"), dict) else {}
    relation = scope.get("relationshipToExperimentScenario") if isinstance(scope.get("relationshipToExperimentScenario"), dict) else {}
    scenarios = _index(design.get("scenarios"), "EXPERIMENT scenario", errors)
    if relation.get("scenarioId") not in scenarios:
        errors.append("EXPERIMENT: scenario relationship must bind an existing experiment scenario")
    if relation.get("relation") != "PREPARES-INTERFACE":
        errors.append("EXPERIMENT: the LUR-start slice may only prepare an interface, not claim a completed experiment scenario")
    admission = design.get("designAdmission") if isinstance(design.get("designAdmission"), dict) else {}
    if admission.get("confirmatoryRunStatus") != "BLOCKED":
        errors.append("EXPERIMENT: bound design admission must remain BLOCKED")
    limitations = package.get("limitations")
    joined = " ".join(limitations) if isinstance(limitations, list) and all(isinstance(item, str) for item in limitations) else ""
    for phrase in ("complete UPLOAD", "No protocol no-response deadline", "No four-arm runner"):
        if phrase not in joined:
            errors.append(f"LIMITATION: required boundary phrase missing: {phrase}")
    return errors


def _witness_errors(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    witnesses = _index(package.get("feasibilityWitnesses"), "WITNESS", errors)
    if set(witnesses) != REQUIRED_WITNESSES:
        errors.append("WITNESS: package must declare the four G0/A feasibility witnesses")
    p3 = witnesses.get("WIT-P3-UNAVAILABLE", {})
    if "P3-UNAVAILABLE" not in str(p3.get("claim", "")):
        errors.append("WITNESS: P3 witness must retain P3-UNAVAILABLE rather than borrowing old applicability")
    successor = witnesses.get("WIT-SUCCESSOR-AND-RECOVER", {})
    if "successor" not in str(successor.get("claim", "")).lower() or "Recover" not in str(successor.get("claim", "")):
        errors.append("WITNESS: successor witness must cover evolved object preservation and Recover")
    return errors


def validate_package(
    root: Path = ROOT,
    package: Any | None = None,
    schema: Any | None = None,
) -> list[str]:
    """Return all named package-contract violations without modifying a file."""

    errors: list[str] = []
    try:
        if package is None:
            package = _read_json(root / PACKAGE_PATH)
        if schema is None:
            schema = _read_json(root / SCHEMA_PATH)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"PACKAGE: unable to load scenario package or schema: {type(exc).__name__}: {exc}"]
    schema_errors = _schema_errors(schema, package)
    if schema_errors:
        return schema_errors
    if not isinstance(package, dict):
        return ["PACKAGE: scenario package root must be an object"]

    errors.extend(_translation_errors(package))
    errors.extend(_control_authority_errors(root, package))
    snapshot = _snapshot_from_bindings(root, package, errors)
    if snapshot:
        errors.extend(_source_errors(package, snapshot))
        errors.extend(_experiment_and_limit_errors(package, snapshot))
    errors.extend(_boundary_errors(package))
    errors.extend(_object_contract_errors(package))
    errors.extend(_object_source_file_errors(root))
    errors.extend(_action_and_case_errors(package))
    if snapshot:
        errors.extend(_traceability_errors(package, snapshot))
    errors.extend(_witness_errors(package))
    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root")
    args = parser.parse_args(argv)
    errors = validate_package(args.root.resolve())
    if errors:
        print("615A scenario package validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("615A scenario package validation passed: source-bound UPLOAD LUR-start engineering contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
