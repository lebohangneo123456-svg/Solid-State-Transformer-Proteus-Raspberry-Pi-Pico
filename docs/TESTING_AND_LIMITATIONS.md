# Testing, observations and limitations

## Project provenance

- Uploaded Proteus file: `Solid-State Transformer (SST).pdsprj` (saved 16 Nov 2026, Proteus 8.17 project format)
- Embedded Pico source extracted without modifications from `FIRMWARE/PI_PICO_1/main.py`.
- Frequency in embedded project: `SWITCH_FREQ_HZ = 5000`; output reference = 50 Hz; modulation index = 0.80.
- Separate code file with 20 kHz requested frequency is provided as an *experimental reference*, not as proof of successful operation at 20 kHz.

## What the screenshots show

- Complete multi-stage schematic showing input rectifier, two IR2104-driven H-bridges, TR1 transformer, secondary rectifier and final LC filter.
- Operating voltage readings at several points, varying across saved snapshots.
- Four traces on a Proteus digital oscilloscope showing repetitive switching waveforms.

Screenshots alone **do not** confirm the actual RMS fundamental output, harmonic distortion, efficiency, 20 W load delivery, isolation integrity or long-duration SPICE stability. The scope channels may be connected to different nodes, and the traces are not all equivalent; separate differential probes are needed to validate the output stage.

## Recommended measurements for further validation

1. Measure input AC true RMS and source peak; for 24 V RMS sine, peak = 33.94 V.
2. Measure first DC link mean and 100 Hz ripple under load.
3. Measure MD1–MD2 differential square wave, actual switching frequency, and MOSFET gate-to-source waveforms.
4. Measure TR1 primary-to-secondary differential amplitude ratio and magnetising current.
5. Measure secondary DC link after the rectifier and its ripple under load.
6. Measure AC_OUT–MD4 over at least 60 ms to establish 50 Hz RMS fundamental and switching ripple.
7. Progress from 100 Ω toward 7.2 Ω output load, verifying 12 V RMS at 20 W and checking current/power device stresses.
8. Repeat long-run simulation and reduce maximum SPICE timestep to check numerical robustness.

## SPICE convergence notes

This design encountered `Timestep too small` errors associated with a MOSFET model in earlier tests. Keep stage-by-stage testing, finite source/winding/ESR resistance, GEAR (order 2 as starting method), decoupled drivers, controlled enable and sensible time steps. Increasing GMIN can sometimes help the solver but may distort results; it does not prove a physically correct circuit.

## Operational limitations

- The firmware uses software GPIO toggling, not deterministic hardware PWM.
- Transformer model does not establish physical ferrite saturation/thermal behaviour.
- Current simplified GPIO wiring bypasses galvanic isolation.
- No independently validated protection and fault-handling system is supplied.
- No experimental hardware test or complete power/efficiency dataset is included.
