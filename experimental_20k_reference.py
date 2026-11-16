# SST - Proteus Raspberry Pi Pico GPIO test
# GP0/GP1: first H-bridge (transformer)
# GP2/GP3: second H-bridge (bipolar SPWM, 50 Hz reference)
# Uses only machine.Pin, time.sleep_us, math.sin.
# NOTE: software loops cannot guarantee requested 20 kHz!

from machine import Pin
import time
import math

# ===============================================
# EDIT THIS ONE VALUE FOR BOTH H-BRIDGES:
SWITCH_FREQ_HZ = 20000
# ===============================================

OUTPUT_FREQ_HZ = 50
MODULATION_INDEX = 0.80

if SWITCH_FREQ_HZ < OUTPUT_FREQ_HZ * 20:
    print('WARNING: Use >= 1000 Hz for a meaningful 50 Hz SPWM test')
if SWITCH_FREQ_HZ <= 0:
    raise ValueError('SWITCH_FREQ_HZ must be positive')
if MODULATION_INDEX < 0 or MODULATION_INDEX > 0.90:
    raise ValueError('MODULATION_INDEX must be 0 to 0.90')

period_us = int(1000000 / SWITCH_FREQ_HZ)
half_us = period_us // 2
if half_us < 2:
    raise ValueError('Frequency too high for software loop')

samples = max(1, int(SWITCH_FREQ_HZ / OUTPUT_FREQ_HZ))
# Precompute the Stage 5 pulse widths to avoid math.sin() on every cycle.
duty_table = []
for i in range(samples):
    phase = 2.0 * math.pi * i / samples
    duty = 0.5 + 0.5 * MODULATION_INDEX * math.sin(phase)
    on_time = int(period_us * duty)
    on_time = max(1, min(period_us - 1, on_time))
    duty_table.append(on_time)

GP0 = Pin(0, Pin.OUT)
GP1 = Pin(1, Pin.OUT)
GP2 = Pin(2, Pin.OUT)
GP3 = Pin(3, Pin.OUT)

# Set all driver IN signals low before starting.
GP0.value(0)
GP1.value(0)
GP2.value(0)
GP3.value(0)

def first_diagonal():
    GP1.value(0)
    GP0.value(1)

def second_diagonal():
    GP0.value(0)
    GP1.value(1)

def second_bridge_positive():
    GP3.value(0)
    GP2.value(1)

def second_bridge_negative():
    GP2.value(0)
    GP3.value(1)

print('SST four-driver test started')
print('Requested carrier frequency (Hz):', SWITCH_FREQ_HZ)
print('Target 50 Hz output SPWM; index:', MODULATION_INDEX)
print('Requested period (us):', period_us)
print('Software GPIO timing is NOT hardware-timed PWM')

index = 0
try:
    while True:
        on_us = duty_table[index]
        # Stage 2 switches at half of each carrier cycle.
        # Stage 5 switches at the SPWM duty boundary.
        first_diagonal()
        second_bridge_positive()

        if on_us <= half_us:
            time.sleep_us(on_us)
            second_bridge_negative()
            if half_us - on_us > 0:
                time.sleep_us(half_us - on_us)
            second_diagonal()
            time.sleep_us(period_us - half_us)
        else:
            time.sleep_us(half_us)
            second_diagonal()
            time.sleep_us(on_us - half_us)
            second_bridge_negative()
            time.sleep_us(period_us - on_us)

        index += 1
        if index >= samples:
            index = 0

except KeyboardInterrupt:
    print('SST switching test stopped')
finally:
    GP0.value(0)
    GP1.value(0)
    GP2.value(0)
    GP3.value(0)
