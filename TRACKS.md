# Workstreams and Artifact Flow

The project is no longer managed as “tutorial first, software second, thesis
last.” It uses synchronized workstreams governed by the same frozen baseline.

```text
                 Frozen methodology baseline
                            |
       +--------------------+--------------------+
       |                    |                    |
Requirements/model     Engineering/Test      Research/Analysis
       |                    |                    |
       +---------> controlled evidence <---------+
                            |
                 Review and Inspection gates
                            |
             engineering decision + publication
```

| Workstream | Owns | Does not own |
|---|---|---|
| Requirements/model | applicability, CRS, EFSM, trace relations | tool behavior or statistical claims |
| Engineering/Test | executable VCs, instrument, environments, verdict evidence | interpretation beyond achieved gates |
| Research/Analysis | adequacy, uncertainty, diagnosis, validity | rewriting raw observations |
| Governance/review | baselines, risks, changes, gate decisions | authoring artifacts it independently approves |
| Publication/tutorial | communication and reproducible teaching | creating new unsupported claims |

## Shared configuration spine

Every downstream artifact should reference:

```text
baseline_id
standard_edition
applicability_id
crs_version
model_version
vcs_version
iut_version
tool_version
environment_id
experiment_id
```

This spine connects requirements to execution, analysis, engineering release,
and publication without relying on document prose alone.

## Working rule

- Questions about normative obligation or scope go upstream to requirements.
- Questions about observable behavior or verdict production go to Test.
- Questions about sufficiency, uncertainty, or diagnosis go to Analysis.
- Questions about whether a claim may be released go to the applicable gate.
