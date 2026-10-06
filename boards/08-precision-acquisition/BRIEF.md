# Four-channel precision acquisition

## Purpose

A USB-powered data-acquisition board. It samples four differential analog inputs simultaneously and streams the samples to a host computer over USB. It is meant to show good analog practice: input protection and filtering, clean converter clocking and power, and placement that respects return paths.

## Functional requirements

- Four differential input channels, sampled simultaneously, at 8 kSPS per channel or faster.
- A real microcontroller with native USB streams the samples to the host. It may sit on the board or be an off-the-shelf MCU module mounted in sockets.
- Connect the converter's data, control, data-ready and reset/synchronisation signals to the microcontroller, so that firmware can reset, identify, configure, read back and stream the converter.
- The digital link must have the bandwidth to carry all four channels at 8 kSPS.
- A dedicated oscillator supplies the converter's clock.
- Every input has a matched RC filter network, matched between its P and N legs and from channel to channel.

## Interfaces & connectors

- A USB connection to the host.
- Four input connectors, one per differential channel, each with protection against overvoltage and ESD.
- Choose the input connector type and record your choice.

## Power

- The board is powered from USB alone. It must not need, or connect, a second supply.
- The converter's analog section gets its own low-noise supply, separate from the digital supply.
- Every converter supply pin is bypassed locally.

## Mechanical & manufacturing constraints

- Fabrication and assembly by JLCPCB.
- At most four copper layers.
- Ordinary plated through vias only.
- One continuous, unsplit ground plane. Do not split ground under returning digital signals.
- Keep the input, filter and converter circuitry in its own placement region, away from the USB, the microcontroller and the clocks.
- Choose the supported differential and common-mode input range before you set the protection, bias and filter values, and justify those values against it in DECISIONS.md. A 24-bit output format is not a 24-bit accuracy claim.
- Machine-assemble the surface-mount parts. Through-hole parts and sockets may be hand-soldered.

## Out of scope

- Firmware.
- USB VID/PID allocation.
- Enclosure.
- Measured noise, crosstalk, gain/offset or frequency-response performance.
