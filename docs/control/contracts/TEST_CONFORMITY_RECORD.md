# Test Article and Setup Conformity Record Contract

| Field | Value |
|---|---|
| **Version** | 1.0 |
| **Baseline** | RB-2026-001-v4.3 |
| **Classification** | ARINC Profile/Binding candidate — certification-oriented |
| **Generic correspondence** | Configuration/provenance role: NOT-DETERMINED |
| **Authority acceptance** | NOT ESTABLISHED |
| **Roles** | IUT, test setup, procedure |

This local record applies certification-oriented test-conformity discipline to
Profile/Binding configuration and provenance. It does not establish external
Configuration equivalence, authority conformity, or certification credit.

## Conceptual schema

```yaml
testArticle:
  manufacturer: ...
  equipmentId: ...
  hardwarePartNumber: ...
  hardwareSerialNumber: ...
  softwarePartNumber: ...
  softwareVersion: ...
  configurationId: ...
  loadSetIdentity: ...

testSetup:
  setupId: ...
  setupVersion: ...
  networkTopologyId: ...
  supportHardware: []
  supportSoftware: []
  simulatorRefs: []
  toolRefs: []
  environmentId: ...

procedure:
  procedureId: ...
  procedureVersion: ...

conformityStatus:
  testArticle: CONFIRMED | NOT_CONFIRMED
  setup: CONFIRMED | NOT_CONFIRMED
  procedure: CONFIRMED | NOT_CONFIRMED
```

## Rules

- the IUT, setup, and procedure identities are evidence, not configuration
  convenience;
- `NOT_CONFIRMED` invalidates conformance evidence and cannot be hidden by a
  case-level `PASS`;
- identities are stable artifact IDs and versions;
- this record is referenced from the Execution Evidence Manifest.

## Non-claims

This record is certification-oriented discipline, not an authority conformity
inspection. Tool qualification credit is not claimed unless explicitly
established under an applicable qualification basis.

---

# 中文版

| 字段 | 内容 |
|---|---|
| **版本** | 1.0 |
| **基线** | RB-2026-001-v4.3 |
| **分类** | ARINC Profile/Binding 候选——面向认证 |
| **Generic 对应** | Configuration/来源角色：NOT-DETERMINED |
| **权威接受** | 尚未建立 |
| **角色** | IUT、测试装置、规程 |

本地记录把面向认证的测试符合性纪律用于 Profile/Binding 配置与来源；它不建立外部
Configuration 等价、权威符合性或认证信用。

## 概念 schema

```yaml
testArticle:
  manufacturer: ...
  equipmentId: ...
  hardwarePartNumber: ...
  hardwareSerialNumber: ...
  softwarePartNumber: ...
  softwareVersion: ...
  configurationId: ...
  loadSetIdentity: ...

testSetup:
  setupId: ...
  setupVersion: ...
  networkTopologyId: ...
  supportHardware: []
  supportSoftware: []
  simulatorRefs: []
  toolRefs: []
  environmentId: ...

procedure:
  procedureId: ...
  procedureVersion: ...

conformityStatus:
  testArticle: CONFIRMED | NOT_CONFIRMED
  setup: CONFIRMED | NOT_CONFIRMED
  procedure: CONFIRMED | NOT_CONFIRMED
```

## 规则

IUT、装置与规程身份属于证据而非配置便利；`NOT_CONFIRMED` 使符合性证据失效，且不得被用例级 `PASS` 掩盖；身份为稳定产物 ID 和版本；本记录由执行证据清单引用。

## 非主张

本记录是面向认证的纪律，而非权威符合性检查。除非在适用鉴定基础上明确建立，否则不主张工具鉴定信用。
