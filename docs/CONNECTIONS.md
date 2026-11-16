# Circuit connections (as documented)

## Raspberry Pi Pico to IR2104 drivers

| Pico GPIO | Driver IN | Half-bridge |
|---|---|---|
| GP0 | U1 pin 2 | Primary left, Q1/Q2 |
| GP1 | U2 pin 2 | Primary right, Q3/Q4 |
| GP2 | U3 pin 2 | Secondary/output left, Q5/Q6 |
| GP3 | U4 pin 2 | Secondary/output right, Q7/Q8 |

## IR2104 reference pinout

1. VCC: regulated ~12 V driver supply
2. IN: logic input from Pico in this simplified simulation
3. SD: active-low shutdown / enable
4. COM: driver reference
5. LO: low-side gate through resistor
6. VS: half-bridge switch node
7. HO: high-side gate through resistor
8. VB: high-side bootstrap supply

Bootstrap capacitor goes between VB and VS; diode goes from +12 V (anode) to VB (cathode). High-side gate-to-source resistors return to the *switching node*, not global ground. Add 100 nF VCC–COM decoupling per driver; verify actual values in the saved project.

## Primary H-bridge

- Upper drains connect to primary positive DC bus.
- Left half-bridge midpoint is MD1 (upper source / lower drain).
- Right midpoint is MD2.
- Transformer primary is between MD1 and MD2.

## Secondary rectifier and final bridge

- Transformer secondary feeds a full bridge diode rectifier and capacitor.
- The output H-bridge uses midpoints MD3 (Q5/Q6) and MD4 (Q7/Q8).
- Filter: MD3 -> series inductor -> AC_OUT; capacitor and resistive load in parallel between AC_OUT and MD4.
- AC output voltage is measured *differentially* between AC_OUT and MD4.

## Isolation limitation

The implemented direct-GPIO scheme requires common reference between primary Pico and output-side driver logic, creating a conductive path across the transformer barrier. **This is a simplified non-isolated control demonstration**, not an isolated hardware design. An isolated power/control interface is necessary for a proper SST.
