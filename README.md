# Internet Inuti (EITN30)
Repository for code and documents related to the course Internet Inside at Lunds Tekniska Högskola.

## Connection
The functionality of the code is split in two. The first being connecting two different Raspberry Pis with external 2.4GHz radios and establishing half-duplex communication.

## Application
The second part, which utilizes the above mentioned connection, is a yet to be determined application.


## Notes:
NRF Module handles communication for L1-2, the control plane for L1-2 however has to be implemented by hand (e.g. controlled/random access, queueing, collision detection). As for the actual data handling, only L3 and above has to be implemented. Base functionality includes IP and ICMP(ping).
