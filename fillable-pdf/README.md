# Fillable project brief

A one-page synthetic form demonstrating standard PDF text fields, a dropdown,
a checkbox and a multiline brief. It contains no customer data.

[Download the interactive PDF](../output/pdf/project-brief-fillable.pdf).

Open it in a PDF viewer that supports forms, enter values, then save a copy.
The five fields are `contact_name`, `project_name`, `service_type`,
`source_ready` and `brief`. Viewer support can vary; this example does not
include calculations or a signature workflow.

## Rebuild

Install `reportlab`, then run `python fillable-pdf/build_sample.py` from the
repository root. The output is written to `output/pdf/`.

Validation included a separate fill/save/reopen check with `pypdf`, comparing
the canonical form values with all five page widgets and checking their
appearance streams. The blank and filled pages were rendered and visually
reviewed. Those checks establish the sample's structure and round-trip
behavior, not compatibility with every viewer.

For this service's scope and price, see the
[Microlancer PDF listing](https://microlancer.io/service/view/2369).
