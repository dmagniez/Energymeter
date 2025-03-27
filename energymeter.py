from gpiozero import Button
from time import time, sleep
from influxdb_client import InfluxDBClient, Point, WriteOptions
import os

# Configuration des GPIOs et descriptions
INPUT_PINS = {
    18: "eclairage zone 3",
    23: "prises zone 3",
    24: "CVC zone 3",
    25: "BECS zone 2"
}

# Configuration InfluxDB
INFLUXDB_URL = "http://10.20.99.10:8086"
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = "okto"
INFLUXDB_BUCKET = "energymeter"

#
#name of the server in influxdb
SERVERNAME = "em-zone3"

buttons = {pin: Button(pin, pull_up=True) for pin in INPUT_PINS}
last_pulse_times = {pin: None for pin in INPUT_PINS}
counter = {pin: None for pin in INPUT_PINS}
instant_power_kW = {pin: 0 for pin in INPUT_PINS}


client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=WriteOptions(batch_size=1))

def log_pulse(pin):
    global last_pulse_times, instant_power_kW
    current_time = time()
    if last_pulse_times[pin] is not None:
        time_diff = current_time - last_pulse_times[pin]
        if time_diff > 0:
            instant_power_kW[pin] = 3600 / time_diff  # Convert impulses per second to kW
    last_pulse_times[pin] = current_time
    #print(f"Impulse detected on {INPUT_PINS[pin]} (GPIO {pin})! Instant Power: {instant_power_kW[pin]:.2f} kW")

for pin, button in buttons.items():
    button.when_pressed = lambda pin=pin: log_pulse(pin)
def send_power_to_influx():
    global instant_power_kW
    while True:
        for pin, power in instant_power_kW.items():
            point = (
                Point("power_consumption")
                .tag("source", SERVERNAME)
                .tag("sensor", INPUT_PINS[pin])
                .field("power", float(power))
            )
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            #print(f"Sent to InfluxDB: {INPUT_PINS[pin]} (GPIO {pin}) -> {power:.2f} kW")
        sleep(5)  # Send data every 5 seconds

if __name__ == "__main__":
    print("Monitoring power consumption for multiple sensors. Press Ctrl+C to exit.")
    send_power_to_influx()
