# USB joystick controller

## Purpose

A USB game-controller board. It plugs into a computer over USB-C, enumerates
as a standard USB HID device, and reports a two-axis analog joystick plus
buttons. It takes all its power from the USB bus.

## Functional requirements

- A microcontroller with a native USB 2.0 full-speed device interface. Its
  clock source must meet USB full-speed timing accuracy, so use a crystal
  or a USB-qualified equivalent.
- Two analog joystick axes (X and Y) read by the MCU's ADC at 10-bit or better
  resolution. Signal bandwidth of interest is DC to 1 kHz. Each axis input is
  low-pass filtered, and analog signals are kept away from fast digital and USB
  signals.
- Four on-board tactile push-buttons and the joystick's push switch, each
  read as a digital input. No input may float when its switch is open.
- A way to reset the MCU manually is desirable.
- An on-board header that allows the MCU firmware to be loaded and
  re-loaded in-circuit.

## Interfaces & connectors

- **USB-C receptacle**, USB 2.0 full-speed, device role. It must work with
  both cable orientations and with C-to-C cables. That is, the board must
  present itself correctly as a USB-C sink so that a host supplies VBUS.
- **Joystick connector**: a keyed (polarized) 5-pin wire-to-board connector
  for an external potentiometer joystick, with pin order
  1 = 5 V, 2 = GND, 3 = X wiper, 4 = Y wiper, 5 = switch (to ground).
- **Programming header** as above.

## Power

- USB bus powered, 5 V nominal. The whole board, including the external
  joystick potentiometers, must stay within a 100 mA budget.
- It must keep working at the low end of the USB VBUS range (about 4.35 V at
  the connector), after any protection-device drops.
- ESD protection on the USB data lines and VBUS, and resettable over-current
  protection on the VBUS input.
- Total capacitance seen directly on VBUS must stay below 10 uF (USB inrush
  limit).

## Mechanical & manufacturing constraints

- Fabrication: JLCPCB, at most 4 copper layers, with a continuous ground
  reference plane.
- Board outline must fit within 80 mm x 60 mm.
- The USB connector sits at a board edge.
- Route the USB D+/D- pair as a coupled, length-matched differential pair,
  at most 50 mm long. Keep the crystal connections short.
- Minimum trace width 0.15 mm; minimum clearance 0.15 mm; minimum via
  diameter 0.3 mm.
- Assembly: JLCPCB SMT assembly. Through-hole parts may need a secondary
  hand-solder step; say so if you use any.
- Fully routed, DRC-clean against JLCPCB rules, copper matching the schematic.
- RoHS-compliant parts. Every assembled part needs an LCSC part number that
  JLCPCB can source.

## Out of scope

- Firmware and USB descriptors (the hardware must make HID firmware possible).
- USB compliance certification and measured impedance.
- Enclosure, and the joystick module itself.

## Assumptions allowed

The MCU family, connector series, button footprints and placement are the
designer's choice, as are any special fabrication options. If a fab option
must be ordered (for example via filling), state it in `DECISIONS.md`.
