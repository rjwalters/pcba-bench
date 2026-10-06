# STM32F103 development board

## Purpose

A minimal "Blue Pill"-style development board for learning and prototyping
with the STM32F103C8 microcontroller. It takes 5 V from USB, regulates it to
3.3 V, runs the MCU from an external crystal, and can be programmed and
debugged over SWD. A user LED confirms that firmware is running.

## Functional requirements

- **MCU:** STM32F103C8 (the standard STM32F103C8T6, or a fully
  pin- and function-compatible variant). Every supply pin must be connected,
  including the analog and backup supplies, and every ground pin. Each supply
  pin needs local decoupling plus some bulk capacitance.
- **Clock:** an external 8 MHz crystal on the high-speed oscillator pins, so
  the PLL can reach 72 MHz, with load capacitors appropriate to the crystal.
- **Boot:** after reset the MCU boots from internal flash by default. Boot
  pins must not float.
- **Reset:** the reset line is available to the debugger.
- **User LED:** one LED driven by an MCU GPIO pin, with current limiting.
- Use widely available components.

## Interfaces & connectors

- **USB connector** for 5 V power input. Using the USB data lines is optional.
- **SWD debug header**, 6 pins on a 2.54 mm pitch so standard SWD debuggers
  can connect. It carries SWDIO, SWCLK, reset, target voltage (3.3 V) and
  ground. Bringing out SWO is desirable. Place it at a board edge where a
  debugger can reach it.

## Power

- Input: 5 V nominal from USB (4.5 to 5.5 V), up to 500 mA.
- On-board regulation to 3.3 V: +/-5 % tolerance, at least 300 mA available,
  ripple no more than 100 mV peak-to-peak. A linear LDO is acceptable. Check
  that it can dissipate the heat at full load.

## Mechanical & manufacturing constraints

- Fabrication: JLCPCB, at most 2 copper layers (chosen for cost).
- Board outline must fit within 60 mm x 40 mm.
- Minimum trace width 0.15 mm; minimum clearance 0.15 mm.
- Assembly: JLCPCB SMT assembly. Through-hole parts may be hand-soldered.
- Fully routed, DRC-clean against JLCPCB rules, copper matching the schematic.
- RoHS-compliant parts. Every assembled part needs an LCSC part number that
  JLCPCB can source.

## Out of scope

- Firmware.
- USB data communication (optional, not required).
- Breaking out general-purpose GPIO to headers (allowed, not required).
- Battery backup, mounting holes, enclosure.

## Assumptions allowed

The choice of USB connector type, regulator part and package, LED pin and
polarity, and any fab options needed for fine-pitch escape routing are the
designer's. If a non-standard fab option must be ordered, state it in
`DECISIONS.md`.
