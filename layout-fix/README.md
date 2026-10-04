# Narrow-screen layout fix sample

This small, synthetic portfolio example demonstrates one reproducible issue: a dashboard grid with `min-width: 680px` creates horizontal page overflow on a narrow viewport.

Open `index.html` in a browser and use **Show fix** / **Show original**. The corrected view changes the grid to `minmax(0, 1fr)` and stacks cards below 520px. The sample contains no external assets or dependencies and does not represent client work.

Observed in Chrome on 2026-10-04 using the HTML preview at W3Schools Tryit:

| View | Document viewport | Document scroll width | Grid columns |
|---|---:|---:|---|
| Original | 360px | 711px | two |
| Fixed | 360px | 360px | one |
| Fixed | 768px | 768px | two |
| Fixed | 1280px | 1280px | two |

Enter on the native button switched both ways and updated `aria-pressed`. The corrected media selector matches the fixed-view selector's specificity so the narrow view stacks correctly. These checks cover this synthetic sample in Chrome; they do not establish behavior on every browser or a customer's website. See `browser-checks.json` for the observed values.

## Discuss a layout fix

For one reproducible HTML/CSS/JavaScript issue, view [my website layout-fix service on LaborX](https://laborx.com/gigs/fix-one-html-css-javascript-layout-issue-123298). Please send the affected URL or source, expected behavior and a screenshot so the scope can be confirmed.
