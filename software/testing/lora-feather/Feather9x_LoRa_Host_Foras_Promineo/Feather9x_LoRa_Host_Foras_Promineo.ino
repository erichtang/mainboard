// Feather9x_TX
// -*- mode: C++ -*-
// Example sketch showing how to create a simple messaging client (transmitter)
// with the RH_RF95 class. RH_RF95 class does not provide for addressing or
// reliability, so you should only use RH_RF95 if you do not need the higher
// level messaging abilities.
// It is designed to work with the other example Feather9x_RX

#include <SPI.h>
#include <RH_RF95.h>
#include <RHReliableDatagram.h>

#define RFM95_RST 27  // "A"
#define RFM95_CS 33   // "B"
#define RFM95_INT 15  // "C"

//#define super_secret_code = 0x00 not used here


// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 433.0

uint8_t sat_address = 250;
uint8_t my_address = 171;

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);
//RHReliableDatagram manager(rf95, my_address);



void setup() {
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  Serial.begin(115200);
  while (!Serial) {
    delay(1);
  }

  delay(100);

  Serial.println("Feather LoRa TRx Test!");

  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    Serial.println("Uncomment '#define SERIAL_DEBUG' in RH_RF95.cpp for detailed debug info");
    while (1)
      ;
  }
  Serial.println("LoRa radio init OK!");

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1)
      ;
  }
  // Serial.print("Set Freq to: "); Serial.println(RF95_FREQ);

  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(23, false);
}

bool tx_flag = false;
uint8_t bytes2read;
uint8_t tx_buf[RH_RF95_MAX_MESSAGE_LEN];

void loop() {

  // check for packet usb port, if nothing just listen
  if (Serial.available() > 0) {
    // first byte will say how many bytes to read
    bytes2read = Serial.read();
    if (bytes2read > 0) {
      Serial.readBytes(tx_buf, bytes2read);
      tx_flag = true;
      // clear the serial buffer for any extra data that should NOT be there
      while (Serial.available() > 0) {
        char trash = Serial.read();
      }
    }
  }

  uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
  uint8_t len = sizeof(buf);

  if (rf95.available()) {
    // Wait for a message addressed to us from the client
    if (rf95.recv(buf, &len)) {
      Serial.print("RX START :::");
      Serial.write(buf, len);
      Serial.println("::: RX END");
      Serial.print("RSSI: ");
      Serial.println(rf95.lastRssi(), DEC);
      if (tx_flag == true) {  // transmit packet
        Serial.print("TX START :::");
        Serial.write(tx_buf, bytes2read);
        rf95.send(tx_buf, bytes2read);
        rf95.waitPacketSent();
        Serial.println("::: TX END");
        tx_flag = false;
      }
    } else {
      Serial.println("[RX FAIL]");
    }
    delay(50);
  }
}