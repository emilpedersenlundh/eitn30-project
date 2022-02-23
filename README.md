# Internet Inuti (EITN30)
Repository for code and documents related to the course Internet Inside at Lunds Tekniska Högskola.

## Connection
The functionality of the code is split in two. The first being connecting two different Raspberry Pis with external 2.4GHz radios and establishing half-duplex communication.

## Application
The second part, which utilizes the above mentioned connection, is a yet to be determined application.


## Notes:
NRF Module handles communication for L1-2, the control plane for L1-2 however has to be implemented by hand (e.g. controlled/random access, queueing, collision detection). Enhanced Shockburst can be used to handle RMA and collision detection. As for the actual data handling, only L3 and above has to be implemented. Base functionality includes IP and ICMP(ping).

## Current situation:
Typechecks have been amended. Native RPi SPI driver has been swapped for SPIDEV. Applying dtoverlays for SPI buses 0 & 1 in /boot/config.txt seems to have set their corresponding GPIO pins to the correct mode (manual modes are still applied though). Setting the correct parameters for the radio module is now a priority as that seems most likely to garner success.
