# Voltage divider

## Purpose

A small passive board that takes a 5 V input and provides an output at exactly
half of it (2.5 V nominal). It is a simple, easily verified reference circuit:
the output should measure half of whatever is on the input.

## Functional requirements

- Produce an output voltage of 0.5 x the input voltage, i.e. 2.5 V nominal
  from a 5 V input, using a passive resistive divider.
- The division ratio must be set by the component values alone (no active
  parts, no adjustment).

## Interfaces & connectors

- Input connector: 2 pins on 2.54 mm pitch (breadboard-compatible), carrying
  the 5 V input and ground.
- Output connector: a separate 2-pin, 2.54 mm pitch connector carrying the
  divided output and ground.
- Input and output share a common ground.

## Power

- 5 V DC from an external source. The board is passive and has no regulation.

## Mechanical & manufacturing constraints

- Fabrication: JLCPCB, at most 2 copper layers.
- Board outline must fit within 30 mm x 25 mm.
- Minimum trace width 0.3 mm; minimum copper clearance 0.2 mm.
- Assembly: JLCPCB SMT assembly; through-hole connectors may be hand-soldered
  (mixed assembly is fine).
- All nets must be completely routed and the board must pass DRC against
  JLCPCB's rules; its copper must match the schematic.
- RoHS-compliant parts. Every assembled part needs an LCSC part number that
  JLCPCB can source.

## Out of scope

- Buffering the output, or guaranteeing the ratio under an external load.
- Precision beyond what standard resistor tolerances give.
- Protection circuitry, mounting holes, enclosure.

## Assumptions allowed

The source specifies no output load, resistor tolerance or absolute resistor
values, and no connector orientation or placement. Choose sensible values (for
example, a total divider resistance that draws negligible current from 5 V),
and record them in `DECISIONS.md`.
