# Simple LED indicator

## Purpose

A minimal "power-on" indicator board: when 5 V is applied, a single LED lights.
It is the smallest possible complete design and is meant to exercise the whole
path from schematic to a JLCPCB-ready fabrication and assembly package.

## Functional requirements

- One indicator LED that lights steadily whenever the board is powered.
- The LED current must be limited by the board itself, so the board can be
  connected straight to a 5 V supply. Target LED current is about 10 mA (a
  standard-value design landing slightly below 10 mA is fine), and it must
  stay within the chosen LED's continuous-current rating.
- Design the circuit around an LED forward voltage of about 2 V (for example a
  red LED). If you choose an LED with a different forward voltage, size the
  current limit for that LED.

## Interfaces & connectors

- One 2-pin power input connector on a 2.54 mm pitch: one pin for +5 V, one
  for ground. Ideally the pin functions are identifiable from the board (silkscreen
  or pin-1 marking).

## Power

- Input: 5 V DC from an external source. There is no on-board regulation.

## Mechanical & manufacturing constraints

- Fabrication: JLCPCB, at most 2 copper layers.
- Board outline must fit within 25 mm x 20 mm.
- Assembly: JLCPCB SMT assembly. Through-hole parts are allowed and may be
  hand-soldered. Placing all parts on one side is preferred.
- The board must pass DRC against JLCPCB's standard capabilities, and its
  copper must match the schematic.
- Every assembled part needs an LCSC part number that JLCPCB can source.

## Out of scope

- Reverse-polarity, over-voltage or ESD protection.
- Dimming, blinking or any control of the LED.
- Mounting holes and enclosure.

## Assumptions allowed

The source specifies no LED colour, package, mounting holes, or exact board
shape beyond the size limit. These are left to the designer; record your
choices in `DECISIONS.md`.
