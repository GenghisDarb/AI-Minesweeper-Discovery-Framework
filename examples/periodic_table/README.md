# Periodic Table Demo

This demo explores gaps and anomalies in the periodic table. Each cell represents an element, with adjacency defined by group and period.

## Goals

- Discover unfilled positions (eka-elements).
- Analyze patterns in atomic properties.

## Data

The dataset (`elements.csv`) includes atomic number, symbol, group, period, and other properties.

## Logic

- **Neighbors**: Same group or same period.
- **Mines**: Unfilled positions.
- **Clues**: Count of unfilled neighbors.

# Periodic Table Data

## Columns

- **Z**: Atomic number.
- **Symbol**: Chemical symbol.
- **Group**: Group number.
- **Period**: Period number.
- **is_discovered**: Boolean indicating if the element is discovered.

## Mine-Flag Criterion

Undiscovered elements (is_discovered = False) are treated as mines.
