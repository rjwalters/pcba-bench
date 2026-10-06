# SDRAM length-matched bus test vehicle

## Purpose

A test vehicle for length-matched, impedance-controlled parallel buses. A standalone microcontroller tests an external 8 MiB SDR SDRAM and reports pass or fail. It is a room-temperature bench demonstrator.

## Functional requirements

- A microcontroller with an integrated SDRAM controller connects to one 8 MiB (64 Mbit), 16-bit-wide SDR SDRAM.
- Every address, bank, data, byte-mask, clock and command/control signal is connected, so the whole 8 MiB is addressable and both byte lanes can be masked independently.
- The memory interface must be designed to run at a 48 MHz SDRAM clock.
- The microcontroller boots unattended from its internal flash at power-up. Reset and boot-mode pins are biased accordingly.
- Two status LEDs, pass and fail, are driven by the microcontroller.

## Bus routing requirements

- Treat the bus as four length-matched groups:
  1. lower data byte with its byte mask;
  2. upper data byte with its byte mask;
  3. address and bank;
  4. command/control with the SDRAM clock.
- Within each group, the spread in electrical length is no more than 5 mm.
- Every bus signal's length is within 10 mm of the SDRAM clock's length.
- Lengths include vertical travel through vias.
- Every bus trace is shorter than 120 mm.
- Bus traces are 50 Ω ±10 % single-ended on every layer they use, calculated against a stated JLCPCB stackup.
- Long data runs are separated from address/control runs, either on different layers or at least 5 mm apart on a shared layer.
- The clock is spaced at least three trace widths from other signals.

## Interfaces & connectors

- 2-pin power input connector.
- SWD programming/debug header, including reset and target-voltage sense.
- 3.3 V logic-level UART header carrying ground, TX and RX.

## Power

- Regulated 5 V ±5 % input. The board regulates its own 3.3 V on-board.
- Total continuous board current is 230 mA or less, at 0–30 °C ambient, with the regulator inside its thermal limits.
- Every microcontroller and memory supply pin has its own local decoupling capacitor.
- The microcontroller's analog supply is filtered.

## Mechanical & manufacturing constraints

- Fabrication and assembly by JLCPCB.
- At most six copper layers, including a dedicated, unbroken ground plane and a dedicated 3.3 V plane. Don't route signals on either plane.
- Ordinary plated through vias only.
- Surface-mount parts may go on both sides. Through-hole headers may be hand-soldered.

## Out of scope

- Firmware.
- USB.
- Industrial temperature range.
- IBIS/transient signal-integrity qualification.
- Measured hardware timing.
