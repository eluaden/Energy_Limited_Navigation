# generator.cpp Overview

This file describes how `generator.cpp` works and how it prints its generated output.

## Program flow

1. `main` calls `registerGen(argc, argv)` and `parseArgs(argc, argv)` to initialize generator state and parse command-line arguments.
2. It reads and validates the expected arguments:
   - `n`: number of vertices
   - `m`: number of edges
   - `limWeight`: maximum edge weight
   - `limCost`: not used in the current output logic, but still parsed
   - `heavyPercent`: percentage of edges that should be "heavy"
   - `lightPercent`: percentage of edges that should be "light"
   - `rechargePercent`: percentage used to compute recharge vertices
3. It ensures:
   - `heavyPercent + lightPercent <= 100`
   - `rechargePercent <= 100`
   - all percentages are non-negative
   - `n > 0`
   - `m >= n-1` so the graph can be connected
   - `limWeight > 0`
   - `limCost > 0`
4. It generates a random graph with `n` vertices and `m` edges using `Graph::random(n, m)`, then makes it connected with `.connected()` and allows parallel edges with `.allowMulti()`.
5. It retrieves the graph edges with `g.edges()`.

## Edge weights

For each edge, `generator.cpp` chooses a random integer `randPercent` from 1 to 100, then assigns the edge weight as:

- heavy edge: if `randPercent <= heavyPercent`
  - weight is random in `[9 * limWeight / 10, limWeight]`
- light edge: else if `randPercent <= heavyPercent + lightPercent`
  - weight is random in `[1, limWeight / 10]`
- normal edge: otherwise
  - weight is random in `[1, limWeight]`

The code uses `rnd.next(1, 100)` to generate the percentile roll and `rnd.next(...)` to sample weights.

## Output format

The program writes three sections to standard output:

1. First line: `n m`
2. Next `m` lines: each edge is printed as `u v weight`
   - `u` and `v` are 1-based vertex indices, converted from the 0-based graph representation with `u.first + 1` and `u.second + 1`
3. Final line: the number of recharge vertices, computed as `n * rechargePercent / 100`

Example output for a small run:

```
5 6
1 2 7
2 4 1
3 5 10
1 3 2
2 5 9
4 5 4
2
```

In this example, the last line `2` means `2` recharge vertices are chosen by percentage, not explicitly listed.

## Notes

- The generated graph may contain parallel edges because `.allowMulti()` is enabled.
- The recharge count is rounded down because integer division is used.

> Note: This markdown file was generated with assistance from an AI tool.
