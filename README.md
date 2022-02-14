# Internet Inuti (EITN30)
Repository for code and documents related to the course Internet Inside at Lunds Tekniska Högskola.

## Connection
The functionality of the code is split in two. The first being connecting two different Raspberry Pis with external 2.4GHz radios and establishing half-duplex communication.

## Application
The second part, which utilizes the above mentioned connection, is a yet to be determined application.


## Notes:
NRF Module handles communication for L1-2, the control plane for L1-2 however has to be implemented by hand (e.g. controlled/random access, queueing, collision detection). Enhanced Shockburst can be used to handle RMA and collision detection. As for the actual data handling, only L3 and above has to be implemented. Base functionality includes IP and ICMP(ping).

## Current situation:
Typechecks have been amended. Currently it seems that the radio library isn't communicating properly via SPI, and thus returns error message "Can't send SPI message". Applying dtoverlays for SPI buses 0 & 1 in /boot/config.txt seems to have set their corresponding GPIO pins to the correct mode. Currently testing if the library is using the correct pins for each bus.
