# Internet Inuti (EITN30)
Repository for code and documents related to the course Internet Inside at Lunds Tekniska Högskola.

## Connection
The functionality of the code is split in two. The first being connecting two different Raspberry Pis with external 2.4GHz radios and establishing half-duplex communication.

## Application
The second part, which utilizes the above mentioned connection, is a yet to be determined application.


## Notes:
NRF Module handles communication for L1-2, the control plane for L1-2 however has to be implemented by hand (e.g. controlled/random access, queueing, collision detection). Enhanced Shockburst can be used to handle RMA and collision detection. As for the actual data handling, only L3 and above has to be implemented. Base functionality includes IP and ICMP(ping).

## Current situation:
Radio communication has been achieved. Current goals are to restructure the code base to an OOP format and create unit tests for code that is not directly linked to the hardware (e.g. data parsing, data handling, web interface).

As for the control plane. The base station will implement a DHCP server with a local subnet, and with its LongGe interface masquerading through the Eth0 interface. The nodes will implement a DHCP client which communicates with the base station DHCP server. The LongGe interface on the nodes inherit whatever local IP the DHCP server provides in each lease.
