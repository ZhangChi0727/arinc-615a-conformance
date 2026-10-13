# Quantitative figure contract

Each figure entry should contain:

- stable figure ID and manuscript label;
- purpose and linked research question or claim;
- input paths plus SHA-256 hashes;
- generator path and revision identity;
- parameters and random seed, or an explicit statement that no randomness is
  used;
- output PDF/SVG paths and optional PNG preview;
- plotting-library and relevant tool versions;
- status: `EXPLORATORY`, `CANDIDATE`, `HUMAN-REVIEWED`, or `PUBLISHED`;
- reviewer and review date for human-reviewed output.

Use a consistent TAES-oriented style: dimensions derived from the manuscript
column width, fonts embedded where possible, colorblind-safe colors paired with
line styles or markers, units on axes, uncertainty encoding explained in the
caption, and no chart decoration that changes the apparent magnitude.

When the data are unavailable, create a clearly labelled layout placeholder or
schematic. Do not create plausible-looking result values.
