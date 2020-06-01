from loguru import logger
import adafruit_dht
from w1thermsensor import W1ThermSensor
try:
    import RPi.GPIO as GPIO
except ImportError:
    from virtualhardware import dummy_GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pumps = {            # Initializing the GPIO pins 17,27,22 for Dosage pumps
    'Co2': 17,
    'Fertilizer': 27,
    'Water Conditioner': 22
}
for (p_type, pin) in pumps.items():
    GPIO.setup(pin, GPIO.OUT)
Button = 16  # Initializing the GPIO pin 16 for Button
led_pin = 12  # Initializing the GPIO pin 12 for LED
FLASH = 0  # Initializing LED States
PULSE = 1  # Initializing LED States
dht_device = adafruit_dht.DHT22(14)
GPIO.setup(Button, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Setup Button
GPIO.setup(led_pin, GPIO.OUT)  # Notification LED pin
pwm = GPIO.PWM(led_pin, 100)  # Created a PWM object
pwm.start(0)  # Started PWM at 0% duty cycle


class Hardware:
    def __init__(self):
        self.sensors = {
            'temp_tank': W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "011447ba3caa"),
            'temp_room': dht_device.temperature,
            'humidity_room': dht_device.humidity
        }
        self.cal_status = ["Success", "Failed", "In Progress", "None"]

    def pump_on(self, pump_type):
        pin = pumps.get(pump_type, None)
        if pin is None:
            raise Exception('Invalid Pump Type!')
        GPIO.output(pumps[pump_type], 1)

    def pump_off(self, pump_type):
        pin = pumps.get(pump_type, None)
        if pin is None:
            raise Exception('Invalid Pump Type!')
        GPIO.output(pumps[pump_type], 0)

    def email_setup(self):
        pass

    def read_temperature(self, temp_sensor_type):
        sensor = self.sensors.get(temp_sensor_type, None)
        if sensor is None:
            raise Exception('Invalid Sensor Type!')
        if isinstance(sensor, W1ThermSensor):
            temperature_in_all_units = sensor.get_temperatures([W1ThermSensor.DEGREES_C, W1ThermSensor.DEGREES_F])
            return temperature_in_all_units

    def water_level(self):
        pass

    def button_state(self):
        while GPIO.input(Button):
            #print(f"{GPIO.input(Button)}: Button Idle")
            sleep(0.1)
            if self.cCancelled:
                raise CalibrationCancelled()

        while not GPIO.input(Button):
            #print(f"{GPIO.input(Button)}: Button Pushed")
            sleep(0.1)
            if self.cCancelled:
                raise CalibrationCancelled()
