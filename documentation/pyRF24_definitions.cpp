// ******************** RF24 class  **************************
bp::class_< RF24 >("RF24", bp::init< uint16_t, uint16_t >((bp::arg("_cepin"), bp::arg("_cspin"))))
    #if defined (RF24_LINUX) && !defined (MRAA)
    .def(bp::init< uint16_t, uint16_t, uint32_t >((bp::arg("_cepin"), bp::arg("_cspin"), bp::arg("spispeed"))))
    .def(bp::init< uint32_t >((bp::arg("spispeed"))))
    .def(bp::init< >())
    #endif
    .def("available", (bool (::RF24::*)())(&::RF24::available))
    .def("available_pipe", &available_wrap)    // needed to rename this method as python does not allow such overloading
    .def("begin", (bool (::RF24::*)(void))(&::RF24::begin))
    .def("begin", &begin_with_pins)
    .def("closeReadingPipe", &RF24::closeReadingPipe)
    .def("disableCRC", &RF24::disableCRC)
    .def("enableAckPayload", &RF24::enableAckPayload)
    .def("enableDynamicAck", &RF24::enableDynamicAck)
    .def("enableDynamicPayloads", &RF24::enableDynamicPayloads)
    .def("disableDynamicPayloads", &RF24::disableDynamicPayloads)
    .def("flush_tx", &RF24::flush_tx)
    .def("flush_rx", &RF24::flush_rx)
    .def("getCRCLength", &RF24::getCRCLength)
    .def("getDataRate", &RF24::getDataRate)
    .def("getDynamicPayloadSize", &RF24::getDynamicPayloadSize)
    .def("getPALevel", &RF24::getPALevel)
    .def("isAckPayloadAvailable", &RF24::isAckPayloadAvailable)
    .def("isPVariant", &RF24::isPVariant)
    .def("isValid", &RF24::isValid)
    .def("maskIRQ", &RF24::maskIRQ, (bp::arg("tx_ok"), bp::arg("tx_fail"), bp::arg("rx_ready")))
    .def("openReadingPipe", &openReadingPipe_wrap, (bp::arg("number"), bp::arg("address")))
    .def("openReadingPipe", (void (::RF24::*)(::uint8_t,::uint64_t))(&::RF24::openReadingPipe), (bp::arg("number"), bp::arg("address")))
    .def("openWritingPipe", &openWritingPipe_wrap, (bp::arg("address")))
    .def("openWritingPipe", (void (::RF24::*)(::uint64_t))(&::RF24::openWritingPipe), (bp::arg("address")))
    .def("powerDown", &RF24::powerDown)
    .def("powerUp", &RF24::powerUp)
    .def("printDetails", &RF24::printDetails)
    .def("printPrettyDetails", &RF24::printPrettyDetails)
    .def("sprintfPrettyDetails", &sprintfPrettyDetails_wrap)
    .def("reUseTX", &RF24::reUseTX)
    .def("read", &read_wrap, (bp::arg("maxlen")))
    .def("rxFifoFull", &RF24::rxFifoFull)
    .def("setAddressWidth", &RF24::setAddressWidth)
    .def("setAutoAck", (void (::RF24::*)(bool))(&::RF24::setAutoAck), (bp::arg("enable")))
    .def("setAutoAck", (void (::RF24::*)(::uint8_t, bool))(&::RF24::setAutoAck), (bp::arg("pipe"), bp::arg("enable")))
    .def("setCRCLength", &RF24::setCRCLength, (bp::arg("length")))
    .def("setDataRate", &RF24::setDataRate, (bp::arg("speed")))
    .def("setPALevel", &RF24::setPALevel, (bp::arg("level"), bp::arg("lnaEnable")=1))
    .def("setPALevel", &setPALevel_wrap, (bp::arg("level")))
    .def("setRetries", &RF24::setRetries, (bp::arg("delay"), bp::arg("count")))
    .def("startFastWrite", &startFastWrite_wrap1, (bp::arg("buf"), bp::arg("len"), bp::arg("multicast")))
    .def("startFastWrite", &startFastWrite_wrap2, (bp::arg("buf"), bp::arg("len"), bp::arg("multicast"), bp::arg("startTx")))
    .def("startListening", &RF24::startListening)
    .def("startWrite", &startWrite_wrap, (bp::arg("buf"), bp::arg("len"), bp::arg("multicast")))
    .def("stopListening", &RF24::stopListening)
    .def("testCarrier", &RF24::testCarrier)
    .def("testRPD", &RF24::testRPD)
    .def("toggleAllPipes", &RF24::toggleAllPipes)
    .def("setRadiation", &RF24::setRadiation)
    .def("txStandBy", (bool (::RF24::*)(::uint32_t, bool))(&RF24::txStandBy), txStandBy_wrap1(bp::args("timeout", "startTx")))
    .def("whatHappened", &whatHappened_wrap)
    .def("startConstCarrier", &RF24::startConstCarrier, (bp::arg("level"), bp::arg("channel")))
    .def("stopConstCarrier", &RF24::stopConstCarrier)
    .def("write", &write_wrap1, (bp::arg("buf")))
    .def("write", &write_wrap2, (bp::arg("buf"), bp::arg("multicast")))
    .def("writeAckPayload", writeAckPayload_wrap, (bp::arg("pipe"), bp::arg("buf")))
    .def("writeBlocking", &writeBlocking_wrap, (bp::arg("buf"), bp::arg("timeout")))
    .def("writeFast", &writeFast_wrap1, (bp::arg("buf")))
    .def("writeFast", &writeFast_wrap2, (bp::arg("buf"), bp::arg("multicast")))
    .add_property("channel", &RF24::getChannel, &RF24::setChannel)
    .def("setChannel", &RF24::setChannel, (bp::arg("channel")))
    .def("getChannel", &RF24::getChannel)
    .add_property("payloadSize", &RF24::getPayloadSize, &RF24::setPayloadSize)
    .def("setPayloadSize", &RF24::setPayloadSize, (bp::arg("size")))
    .def("getPayloadSize", &RF24::getPayloadSize)
    .def_readwrite("failureDetected", &RF24::failureDetected);