# Drinking Water Quality (DWQMP) data model

This document explains how the existing `dwqmp` app is structured so we can
coordinate upcoming refactors. Each section highlights key models, their
relationships, and how they support the current UI.

## High-level process flow

1. **ServiceProvider** – entity responsible for DWQMP schemes. Has optional
   primary contact.
2. **Scheme** – describes a water or wastewater scheme (type, location) owned by a
   service provider.
3. **TestPoint** – sampling point within a scheme. References the scheme and the
   test types performed there, plus sampling frequency.
4. **FieldSample** – actual sampling event at a test point. Captures time and who
   collected it.
5. **SampleCollection** – bundles one or more field samples into a shipment to a
   lab, tracking send/receive timestamps and attachments.
6. **SampleResult** – lab result for a given field sample + test type combination.
7. **NonConformance** – created when a sample result exceeds limits/needs action.
8. **Incident** – escalation linked to a non-conformance with its own status and
   follow-up correspondence + corrective actions.
9. **CorrectiveAction** – remedial work items tied to an incident.

## Detailed model notes

### ServiceProvider
- Fields: `name`, `spid`, `primary_contact (FK auth.User)`
- Relations: One-to-many with Scheme (`ServiceProvider.schemes`).
- UI: list/manage under `/water/providers/`.

### Scheme
- Fields: `service_provider`, `type` (DW/WW/RW), `description`, coordinates,
  `address`.
- Relations: Many schemes per provider. Each scheme has many `test_points`.
- UI: `/water/schemes/` lists schemes; `/water/schemes/<id>/` shows detail and
  sampling points for that scheme.

### TestPoint
- Fields: `scheme`, `reference`, `description`, `frequency` and units, M2M
  `test_types`.
- Relations: belongs to a scheme, many field samples.
- UI: `/water/testpoints/` overall list, plus inline table on scheme detail for
  managing points and adding new ones scoped to the scheme.

### TestType
- Describes lab tests (name, units, limit, method, estimated cost).
- M2M to test points to indicate which tests are run at each point.

### FieldSample
- Fields: FK to `test_point`, datetime, `collected_by` user.
- Relations: may appear in multiple `SampleCollection` records (M2M); has many
  `SampleResult`s.
- UI: `/water/samples/` list with edit links.

### Laboratory
- Simple contact info (name/address/email/phone). Not currently referenced by
  other models, but intended for future link from `SampleCollection` or results.

### SampleCollection
- M2M `field_samples`, `sent_at`, optional `received_at`, attachments.
- Provides `is_complete()` helper.
- UI: `/water/collections/` list; edit page for tracking receipt.

### SampleResult
- FK `field_sample`, FK `test_type`, value, comments.
- Each result can spawn zero or more non-conformances.
- UI: `/water/results/` list with edit links.

### NonConformance
- FK `sample_result`, status flag, auto timestamp.
- Leads to `Incident` records.
- UI: `/water/nonconformances/` list; edit page to update status.

### Incident & IncidentCorrespondence
- Incident links to one non-conformance, stores ID, datetime, status.
- Correspondence attachments/time/comments tracked separately (Incident →
  IncidentCorrespondence one-to-many).
- UI: `/water/incidents/` list and form; correspondence currently handled via
  model but no dedicated UI yet.

### CorrectiveAction
- Tied to an incident; stores short/long descriptions, status, delivery dates,
  estimated cost.
- UI: `/water/actions/` list with edit form.

## Current navigation / UI summary

- `/water/` dashboard shows counts and shortcuts, with entry points to schemes,
  samples, results, non-conformances, incidents, and corrective actions.
- Each list page uses a simple table with row links to edit pages.
- Scheme detail page surfaces all sampling points under that scheme and includes
  a dedicated "Add sampling point" action (prefills scheme on the create form).
- Report page `/water/reports/` lets the user specify start/end dates and shows:
  - Field samples collected
  - Sample collections dispatched
  - Non-conformances raised
  - Incidents recorded
  - Corrective actions scheduled
  Each item links back to its edit page.

## Follow-up

Use this document to describe desired changes to the model relationships,
fields, or UI flows. For example, you can add sections like “Proposed changes”
or inline comments describing new models (e.g. scheduled sampling plans, lab
chain-of-custody records). Once updated, I can follow the instructions to
implement the refactor.

## Feedback prompts by URL

- `/water/` – Does the dashboard surface the right shortcuts? Would a live feed
  of upcoming sampling tasks help?
- `/water/providers/` – Is there additional contact info you’d capture per
  provider? Any bulk actions required?
- `/water/schemes/` – Should the list include sampling compliance summaries or
  links to maps?
- `/water/schemes/<id>/` – Would it be useful to show a map with sampling points
  and metadata (e.g. “it would be nice if the view for `/water/schemes/<int>/`
  showed a Google map with labels for all sampling points”)?
- `/water/testpoints/` – Do you need filtering/grouping to spot overdue points?
- `/water/samples/` – Is the sampling log missing context (e.g. weather,
  operator notes) that would improve decision making?
- `/water/collections/` – Would barcodes or courier tracking integrations help?
- `/water/results/` – Should limits/highlights be shown inline to spot
  exceedances faster?
- `/water/nonconformances/` – Are there other statuses or notifications you want
  to track?
- `/water/incidents/` – Do you need a timeline or attachments summary here?
- `/water/actions/` – Would a Gantt-style view or progress tracking help?
- `/water/reports/` – Are there additional export formats or metrics you need?
