# Examples

Worked manifests, validated in CI by the `examples-valid` gate. Copy one and
change the facts rather than starting from an empty file.

| File | Shows |
|---|---|
| `invoice-api.project.yaml` | A production service: stable, owned by a team, deployed |
| `design-system.project.yaml` | A platform project consumed by other repositories |
| `sunset-gateway.project.yaml` | A deprecated project, with successor and sunset date |
| `payments.admin.yaml` | A team profile: six duties assigned, an agent under sponsorship |
| `acme.org.yaml` | An organization: bounded stewards and policy defaults |
| `migrate-fleet.workstream.yaml` | A workstream mid-flight |

```bash
atlas validate examples/invoice-api.project.yaml
atlas validate examples/*.yaml
```
