# Charlieplexed 3x3 LED grid

## Purpose

A small self-contained LED display module: nine LEDs in a 3 x 3 grid,
driven by an on-board microcontroller using charlieplexing so that only four
GPIO lines control all nine LEDs. Typical uses are status indication and simple
animations. The board must be programmable in-circuit.

## Functional requirements

- Nine LEDs arranged physically as a 3 x 3 grid.
- All nine LEDs are driven by charlieplexing from exactly four microcontroller
  GPIO lines. Every LED must be individually addressable, i.e. each LED sits on
  a distinct ordered pair of the four lines.
- Current limiting must be matched across the four lines so that every LED
  sees the same current. Peak LED current must not exceed about 4.6 mA at a
  5 V supply.
- The microcontroller is a small 8-bit AVR (ATtiny85-class) that runs from its
  internal clock. Its supply must be properly decoupled, and its reset line
  must stay functional (not repurposed as GPIO) and must not float.

## Interfaces & connectors

- Power input: a 2-pin, 2.54 mm pitch header (supply and ground).
- Programming: a standard 6-pin (2 x 3, 2.54 mm) AVR ISP header with the
  conventional pinout (1 MISO, 2 VCC, 3 SCK, 4 MOSI, 5 RESET, 6 GND).
  If any ISP signal shares a microcontroller pin with the LED matrix,
  the design must still allow reliable in-circuit programming.

## Power

- Regulated 3.3 V to 5.0 V DC supplied externally. Maximum 100 mA.
- No on-board regulator is required.

## Mechanical & manufacturing constraints

- Fabrication: JLCPCB, at most 2 copper layers.
- Board outline must fit within 50 mm x 55 mm.
- Minimum trace width 0.2 mm; minimum copper clearance 0.2 mm.
- Assembly: JLCPCB SMT assembly; through-hole parts (for example the
  microcontroller package or headers) may be hand-soldered after SMT.
- Fully routed, DRC-clean against JLCPCB rules, copper matching the schematic.
- RoHS-compliant parts. Every assembled part needs an LCSC part number that
  JLCPCB can source.

## Out of scope

- Firmware. The design only has to make it possible.
- Voltage regulation, reverse-polarity protection.
- Populating more than nine LEDs (four lines could address twelve).

## Assumptions allowed

LED colour and package, which MCU pins drive the matrix, the microcontroller
package (through-hole or SMD), and the placement of the support parts are the
designer's choice. Record them in `DECISIONS.md`.
