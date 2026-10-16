# IEEE TAES model-figure style contract

The target is restrained IEEE engineering communication, not a generic
"Nature look". Current IEEE Author Center guidance was checked on 2026-10-14;
reverify before claiming submission compliance.

## Canvas and typography

- Prepare for 88.9 mm single-column or 182 mm two-column width.
- Use white background and a compact horizontal or vertical reading path.
- Use Helvetica or Arial-compatible sans serif; target approximately 9--10 pt
  at final size and avoid text below 8 pt.
- Keep captions and formal figure titles outside the artwork. Retain only short
  panel/stage headings and essential semantic notes.
- Use consistent sentence case, mathematical symbols, and project terms.

## Visual language

- Core CL-TAV logic: restrained blue.
- External actors/systems and context: neutral grey.
- evidence, requirements, or planned/unverified material: pale amber.
- evaluator-only truth or protected information boundary: pale violet.
- valid/accepted path: pale green only when a non-colour cue is also present.
- stop, error, forbidden, or risk: pale red plus a distinct line style or
  explicit label; never encode it by red alone.
- Use flat fills, 1--1.5 pt strokes, no gradients, shadows, clipart, or
  decorative icons.

Keep a small shape vocabulary: rounded rectangles for processes/modules,
plain rectangles for records/artifacts, containers for boundaries, diamonds
only for real decisions, and quiet note shapes for limitations. Different
arrow styles must have declared meanings.

## Layout and accessibility

- Use layout before colour to express hierarchy.
- Route orthogonal edges through whitespace and separate feedback/retry lanes
  from the primary path.
- Avoid crossings; split a dense figure or use lanes before shrinking text.
- Pair colour with labels, dashes, markers, geometry, or position. Inspect a
  grayscale preview.
- Keep long explanations, provenance, and limitations in the caption or
  review packet rather than shrinking them inside boxes.

## Export and QA

- Canonical editable source: uncompressed `.drawio` XML.
- Preferred manuscript exports: SVG and PDF with editable or embedded fonts.
- PNG is a QA preview, not the authority for line art.
- Check XML structure, finite registered semantic consistency, font embedding, final physical size,
  clipping, overlaps, off-canvas objects, arrowheads, and grayscale meaning.
- Dense control-flow views may use compact guard references only when an
  adjacent legend expands every guard and preserves mutually exclusive cases.
- Report the calculated final point size from canvas width and publication
  width; source font size alone is not a final-size readability result.
- Preserve repository-relative paths and SHA-256 identities in the manifest.

Official reference points:

- IEEE Author Center, Create Graphics for Your Article.
- IEEE Author Center, Resolution and Size.
- IEEE Author Center, File Formatting.

If these sources change, mark the style `ESTIMATED` until reverified.
