# Sensored BLDC motor controller

## Purpose

A small bench demonstrator that spins a small, unloaded three-phase brushless DC motor with Hall sensors. It runs from a current-limited laboratory supply and is meant for conservative bring-up and firmware development, not for traction or high-power use.

## Functional requirements

- Drive the three motor phases from three half-bridges, commutated from the motor's three Hall sensors.
- An on-board programmable microcontroller reads the Hall sensors and controls each half-bridge independently, setting both its PWM and its enable.
- Phase current: 0.5 A continuous, 1 A peak.
- Sense motor current in hardware. A comparator raises a fault to the microcontroller at a nominal 1 A, on an input that can interrupt it, and the bridge must be able to be shut down from that fault.
- An on-board adjustable control sets the speed demand, which the microcontroller reads as an analog voltage.
- An external RUN switch input. The motor must not run while the switch is open.
- A fault indicator LED driven by the microcontroller.

## Interfaces & connectors

Separate connectors for:

- DC power input;
- the three motor phases;
- the Hall sensors, carrying +5 V, ground and three Hall signals;
- the RUN switch;
- in-system programming of the microcontroller.

Hall inputs must accept 5 V logic and include pull-ups so that open-drain Hall sensors work.

## Power

- Input is 12–24 V DC.
- The input needs reverse-polarity protection, a fuse, a transient-voltage clamp, and bulk capacitance rated for the 24 V motor bus with margin.
- An on-board regulated 5 V rail powers the logic and the Hall sensors. It must supply at least 20 mA to the Hall sensors.
- The regulator and the motor driver must stay within their thermal limits at 24 V input.

## Mechanical & manufacturing constraints

- Fabrication and assembly by JLCPCB.
- At most four copper layers, 1 oz copper.
- Board no larger than 70 × 90 mm.
- Exposed-pad power packages must be soldered down, with a thermal path into ground copper.
- Current-carrying copper must be sized for the 1 A peak.
- Surface-mount parts are machine-assembled. Through-hole connectors and the speed control may be left out of the placement file and hand-soldered.

## Out of scope

- Firmware.
- Enclosure.
- Phase currents above 1 A.
- Regenerative braking, and driving the motor shaft from an external source.
- Closed-loop current regulation.
- Measured motor and thermal validation.
