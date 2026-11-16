
from machine import Pin
import time
import math

# ==========================================
# SOLID STATE TRANSFORMER - ALL 4 DRIVERS
# ==========================================

# CHANGE THIS VARIABLE TO ADJUST FREQUENCY
SWITCH_FREQ_HZ = 5000

# Output inverter settings
OUTPUT_FREQ_HZ = 50
MODULATION_INDEX = 0.80

# Calculate switching timing
period_us = int(1000000 / SWITCH_FREQ_HZ)
half_us = period_us // 2

if half_us < 2:
    raise ValueError("Frequency too high")

# Precalculate SPWM values
samples = max(1, int(
    SWITCH_FREQ_HZ / OUTPUT_FREQ_HZ
))

duty_table = []

for i in range(samples):
    phase = 2 * math.pi * i / samples

    duty = 0.5 + (
        0.5 * MODULATION_INDEX *
        math.sin(phase)
    )

    on_time = int(period_us * duty)
    on_time = max(1, min(period_us - 1, on_time))
    duty_table.append(on_time)

# GPIO CONFIGURATION
GP0 = Pin(0, Pin.OUT)
GP1 = Pin(1, Pin.OUT)
GP2 = Pin(2, Pin.OUT)
GP3 = Pin(3, Pin.OUT)

GP0.value(0)
GP1.value(0)
GP2.value(0)
GP3.value(0)

# First H-bridge switching
def first_diagonal():
    GP1.value(0)
    GP0.value(1)

def second_diagonal():
    GP0.value(0)
    GP1.value(1)

# Second H-bridge switching
def spwm_positive():
    GP3.value(0)
    GP2.value(1)

def spwm_negative():
    GP2.value(0)
    GP3.value(1)

print("SST Controller Started")
print("Requested switching frequency:", SWITCH_FREQ_HZ)
print("Output reference frequency:", OUTPUT_FREQ_HZ)
print("Modulation index:", MODULATION_INDEX)

index = 0

try:
    while True:
        on_us = duty_table[index]

        first_diagonal()
        spwm_positive()

        if on_us <= half_us:
            time.sleep_us(on_us)

            spwm_negative()

            if half_us - on_us > 0:
                time.sleep_us(
                    half_us - on_us
                )

            second_diagonal()

            time.sleep_us(
                period_us - half_us
            )

        else:
            time.sleep_us(half_us)

            second_diagonal()

            time.sleep_us(
                on_us - half_us
            )

            spwm_negative()

            time.sleep_us(
                period_us - on_us
            )

        index += 1

        if index >= samples:
            index = 0

except KeyboardInterrupt:
    print("SST Controller Stopped")

finally:
    GP0.value(0)
    GP1.value(0)
    GP2.value(0)
    GP3.value(0)
