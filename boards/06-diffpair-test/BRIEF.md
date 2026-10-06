# Four-channel LVDS link test coupon

## Purpose

A test coupon for controlled-impedance differential routing. It carries four independent, one-way logic signals across the board as LVDS. Each channel turns a 3.3 V LVTTL input into LVDS, sends it down a terminated differential pair, and turns it back into a 3.3 V LVTTL output. The coupon is driven from a bench signal source and checked with a high-impedance instrument. It needs no firmware.

## Functional requirements

- Four identical, independent channels. Each one is: LVTTL input → LVDS driver → 100 Ω differential pair → LVDS receiver → LVTTL output.
- Each pair is terminated with 100 Ω differential at its receiver.
- An undriven input must leave its channel in a defined logic state.

## Interfaces & connectors

- A 2-pin power connector.
- An input header carrying the four channel inputs.
- An output header carrying the four channel outputs.
- On both signal headers, every signal pin has its own adjacent ground pin.
- All headers use 2.54 mm pitch, for bench wiring.

## Power

- An external regulated 3.3 V supply powers the board through the power connector. No other supply is available.
- Each driver and receiver IC has local bypass capacitors.
- The supply input has bulk capacitance.

## Mechanical & manufacturing constraints

- Fabrication and assembly by JLCPCB.
- At most four copper layers.
- The differential pairs must meet a 100 Ω ±15 % differential impedance target. Calculate it against a stated JLCPCB stackup, and record that stackup, the trace width and gap, and the resulting impedance in DECISIONS.md.
- Intra-pair length skew must be no more than 0.1 mm on every pair.
- Route the pairs as coupled pairs over a continuous ground reference plane on the adjacent layer, with no splits or voids under them.
- Use ordinary plated through vias only: no blind, buried, micro or via-in-pad vias.
- Surface-mount parts are machine-assembled. The through-hole headers may be hand-soldered.

## Out of scope

- Any protocol compliance, such as USB, PCIe or MIPI.
- Measured bandwidth or eye quality.
- An on-board regulator.
- Firmware.
