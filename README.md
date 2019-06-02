# Tamper Detection daemon for Minnowboard

This repository contains a small daemon (for python 3) that monitors a GPIO
pin on the minnowboard and responds if the value changes.  It is intended for
use with a case-mounted switch.

Run the daemon with `./tamperd start`.  The tamper switch should be connected
between pin 1 and pin 21 (bottom left pin and third pin from the right on the
bottom on the low speed expansion header).

For safety reasons, tamper response is not enabled until the switch has been
connected.  Once the switch is connected, any disconnection will immediately
lead to the system syncing file systems (for safety) and immediately halting.

Halting is used instead of rebooting as the minnowboard disconnects USB power
upon halt.  This ensures that any keys on attached smart cards, encrypted USB
sticks, etc. are wiped.
