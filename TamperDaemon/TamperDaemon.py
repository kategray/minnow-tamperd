from os import path, system
import sys
import time
import logging

from daemons.prefab import run,step

logfile = "/var/log/tamperd.log"
logging.basicConfig(filename=logfile, level=logging.DEBUG)
LOG = logging.getLogger(__name__)


class Daemon(run.RunDaemon):
    ACTIVITY_LED = {"number": 360, "direction": "out"}
    TAMPER_INPUT = {"number": 338, "direction": "in"}
    gpio_pins = [ACTIVITY_LED, TAMPER_INPUT]

    def pin_path (self, pin):
        return ("/sys/class/gpio/gpio" + str(pin["number"]) + "/")

    def run (self):
        LOG.debug ("Registering GPIOs")

        try:
            for pin in self.gpio_pins:
                # Export the pin
                LOG.debug ("Registering pin number " + str (pin["number"]))
                f = open ("/sys/class/gpio/export","w")
                f.write (str (pin["number"]))
                f.close ()

                # Set pin direction
                f = open (self.pin_path (pin) + "direction", "w")
                f.write (pin["direction"])
                f.close ()
        except Exception as ex:
            sys.exit ("Error: " + str(ex))

        activity_led_value = 0
        tamper_seen = False

        while True:
            # Read the tamper input
            tamper_input = open (self.pin_path (self.TAMPER_INPUT) + "value", "r")
            tamper_value = int(tamper_input.read ())
            tamper_input.close()
            # LOG.debug ("Read tamper value {0}".format(tamper_value))

            # If the tamper is enabled, and tamper has not previously been seen, mark tamper input as seen
            if (tamper_value == 0) and not (tamper_seen):
                LOG.debug ("Tamper switch detected.  Enabling tamper response.")
                tamper_seen = True
            elif (tamper_value == 1 and tamper_seen == True):
                LOG.debug ("Tamper event detected.  Responding by halting immediately.")

                # Enable sysrq
                sysrq = open ("/proc/sys/kernel/sysrq", "w")
                sysrq.write ("1")
                sysrq.close()

                # Sync the filesystems
                sysrq = open ("/proc/sysrq-trigger", "w")
                sysrq.write ("s")
                sysrq.close ()

                # Force shutdown, right now
                sysrq = open ("/proc/sysrq-trigger", "w")
                sysrq.write ("o")
                sysrq.close ()

                # If we get here, something has gone wrong.
                sys.exit ("Tamper event detected.")

            # Toggle the activity LED
            activity_led_value = 0 if activity_led_value == 1 else 1
            # LOG.debug ("Setting activity led {0} to {1}.".format(self.pin_path (self.ACTIVITY_LED) + "value", activity_led_value))
            activity_led = open (self.pin_path (self.ACTIVITY_LED) + "value", "w")
            activity_led.write (str (activity_led_value))
            activity_led.close ()

            # Sleep for 0.25 seconds before running again
            time.sleep (0.25)

    def cleanup (self):
        LOG.debug ("Unregistering GPIOs")
        try:
            for pin in self.gpio_pins:
                f = open ("/sys/class/gpio/unexport","w")
                f.write (str (pin["number"]))
                f.close ()
        except Exception as ex:
            sys.exit ("Error: " + str(ex))
