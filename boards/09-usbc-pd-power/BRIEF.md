# USB-C PD 5 V power supply

## Purpose

A standalone power board. It takes power from a USB-C Power Delivery charger, negotiates a higher-voltage contract, and converts it to a regulated 5 V output, targeting 3 A. An external host can read the output voltage and current over I2C. Ordinary power conversion must work with no firmware and no host attached.

## Functional requirements

- Acts as a USB-C PD sink only. It negotiates a 15 V or 20 V contract on its own, with no firmware or host.
- The converter's input is switched. VBUS reaches the converter only through a switch controlled by the PD sink, after a contract has been negotiated.
- On ordinary 5 V USB input, with no higher-voltage contract, the converter stays disabled and there is no output.
- A synchronous buck regulator produces 5 V at a 3 A target. It must cover the full input voltage of a 20 V contract, including tolerance.
- The output current is measured through a shunt resistor with Kelvin connections. A voltage/current monitor reports it over I2C.
- An external I2C host can also read the PD sink's configuration and status.
- An LED indicates that the output is present (nice to have).

## Interfaces & connectors

- A USB-C receptacle for input.
- A 2-pin 5 V output connector rated for 3 A.
- A telemetry header carrying ground, I2C clock and data, a 3.3 V reference observation pin, the PD-sink alert line and the monitor alert line.
- The I2C bus uses 3.3 V logic. The board does not draw its supply from the host.

## Power

- A separate low-current 3.3 V rail, derived on the board, powers the telemetry circuits and the I2C pull-ups. It is not a supply for external loads.
- The input path has overcurrent protection.

## Mechanical & manufacturing constraints

- Fabrication and assembly by JLCPCB.
- At most four copper layers.
- Ordinary plated through vias only.
- Keep the input switching loop compact and the switch-node copper small.
- Keep the feedback network away from the switch node and the inductor.
- Size power copper and via arrays for the 3 A output, with broad ground return copper.
- Machine-assemble the surface-mount parts. Through-hole headers may be hand-soldered.

## Out of scope

- Firmware.
- Reprogramming the PD sink's profiles.
- Measured ripple, efficiency, transient or thermal performance.
- USB data.
- Powering the board from its output.
