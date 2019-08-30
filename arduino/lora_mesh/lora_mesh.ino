#include <SPI.h> //Import SPI librarey 
#include <RH_RF95.h> // RF95 from RadioHead Librarey 
#include<string.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif
#include <SimpleDHT.h>
#define RFM95_CS 10 //CS if Lora connected to pin 10
#define RFM95_RST 9 //RST of Lora connected to pin 9
#define RFM95_INT 2 //INT of Lora connected to pin 2
#define MQ7 A3
#define MQ2 A2
#define PIN 8
#define NUMPIXELS 3
// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 434.0
int pinDHT11 = 6;
int butd,butm,ledctr=0;
int butpin = 5;
int pause = 100;
int note = 770;
int ctr=0,rctr=0;
SimpleDHT11 dht11(pinDHT11);
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
int delayval1 = 250;
// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);
int MQ7d,MQ2d;
unsigned int sdpin=4;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(RFM95_RST, OUTPUT); 
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);
  pinMode(MQ7, INPUT);
  pinMode(MQ2, INPUT);
  delay(10);
  pixels.begin(); 
  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    //while (1);
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    //while (1);
  }
  //rf95.setSpreadingFactor(12);
  //rf95.setModeRx();   
  rf95.setTxPower(23);  
  }
}

void loop() {
  int b;
  delay(delayval1);
  char radiopacket[]="Node1 ";
  char radiopacket1[100];
  char string[100];
  //char string1[1024];
  // put your main code here, to run repeatedly:
 if(ledctr==0){
  pixels.setPixelColor(0, pixels.Color(0x00,0x22,0x3b));
  pixels.show();
  delay(200);
  pixels.setPixelColor(0, pixels.Color(0,0,0));
  pixels.show();
  delay(200);
  pixels.setPixelColor(1, pixels.Color(0x20,0x5e,0x8a));
  pixels.show();
  delay(200);
  pixels.setPixelColor(1, pixels.Color(0,0,0));
  pixels.show();
  delay(200);
  pixels.setPixelColor(2, pixels.Color(0x80,0xd0,0xff));
  pixels.show();
  delay(200);
  pixels.setPixelColor(2, pixels.Color(0,0,0));
  pixels.show();
  delay(200);
  ledctr++;
 }
 if(rf95.available()){
   b = rf95.recv((uint8_t *)string,strlen(string));
   Serial.println(string);
   int rssi_val = rf95.lastRssi();
   Serial.println(rssi_val);
   //rf95.setModeTx();
 }
 else{
  MQ7d=analogRead(MQ7);
  MQ2d=analogRead(MQ2);
  char data[10]={0},data1[10]={0},data2[10]={0},data3[10]={0};
  char mqq[3];
  char data4[5];  
  while(butd=digitalRead(butpin)){
       if(ctr<3){
       ctr+=1;
       rctr++;
       Serial.println(butd);
       Serial.println(ctr);
       Serial.println(rctr);
       delay(1000);}
       else if(rctr>=0){
        rctr++;
        Serial.println(rctr);
        delay(1000);
        if(rctr>=8){
          ctr=0;
          rctr=0;
        }
        }
  }
  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    //Serial.print("Read DHT11 failed, err="); Serial.println(err);
    //delay(1000);
    return;
  }
  int dtemp=(int)temperature;
  int dhumi=(int)humidity;
  Serial.println("Send: ");
  //Serial.println(MQ7d);
  //Serial.println(MQ2d);
  itoa(MQ2d,mqq,10);
  //Serial.println(data1);
  itoa(dtemp,data2,10);
  //Serial.println(data2);
  itoa(MQ7d,data,10);
  itoa(dhumi,data3,10);
  Serial.println(data);
  Serial.println(mqq);
  Serial.println(data2); 
  Serial.println(data3);
  char ack[]="ACK";
  char alert[]="SOS";
  //char data1[] = "ACK1";
  //char data2[]="ACK2";
  strcpy(radiopacket1,radiopacket);
  strcat(radiopacket1,data);
  strcat(radiopacket1," ");
  strcat(radiopacket1,mqq);
  strcat(radiopacket1," ");
  strcat(radiopacket1,data2);
  strcat(radiopacket1," ");
  strcat(radiopacket1,data3);
  strcat(radiopacket1," ");
  if(ctr>=2){
    strcpy(data4,alert);
    strcat(radiopacket1,data4);
  }
  else{
    strcpy(data4,ack);
    strcat(radiopacket1,data4);
  }
  rf95.send((uint8_t *)radiopacket1, strlen(radiopacket1));
  //rf95.send((uint8_t *)data, sizeof(data));
  if(dhumi>90||dtemp>56||MQ7d>600||MQ2d>450){
    tone(sdpin,770,150);
    delay(150);
    noTone(sdpin);
    tone(sdpin,750,350);
    delay(250);
    noTone(sdpin); 
  }
  if((!(strcmp(data4,"SOS"))))
  {
    pixels.setPixelColor(0, pixels.Color(56,1,3));
    pixels.setPixelColor(1, pixels.Color(56,1,3));
    pixels.setPixelColor(2, pixels.Color(56,1,3));
    pixels.show();
    delay(delayval1);
    threeDots();
    threeDashes();
    threeDots();
    pixels.setPixelColor(0, pixels.Color(0,0,0));
    pixels.setPixelColor(1, pixels.Color(0,0,0));
    pixels.setPixelColor(2, pixels.Color(0,0,0));
    pixels.show();
    delay(30);
    delay(100); 
  }
 }
 if(b==1){
    rf95.send((uint8_t *)string,strlen(string));
    Serial.println(string);
    }
 delay(500);
}

void threeDots()
{
  for (int i=0; i<3; i++){
    tone(sdpin, note, 100);
    delay(200);
    noTone(sdpin);
  }
}

void threeDashes()
{
  for (int i=0; i<3; i++){
    tone(sdpin, note, 300);
    delay(400);
    noTone(sdpin);
  }
}
