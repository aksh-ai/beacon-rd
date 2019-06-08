//Include Libraries
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

//create an RF24 object
RF24 radio(7, 8);  // CE, CSN
#define mq2 A1
#define mq7 A0
#include <SimpleDHT.h>
int pinDHT11 = 6;
SimpleDHT11 dht11(pinDHT11);
//address through which two modules communicate.
const byte address[6] = "00001";
typedef struct{
  int dmq2;
  int dmq7;
  int dtemp;
  int dhumi;
  
}Data;
Data datas;
void setup()
{
  radio.begin();
  Serial.begin(9600);
  pinMode(mq2,INPUT);
  pinMode(mq7,INPUT);
  //set the address
//  radio.setPALevel(RF24_PA_HIGH);
  radio.openWritingPipe(address);
  
  //Set module as transmitter
  radio.stopListening();
 
}
void loop()
{
  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT11 failed, err="); Serial.println(err);delay(1000);
    return;
  }
  
  Serial.print("Sample OK: ");
  datas.dtemp=(int)temperature;
  datas.dhumi=(int)humidity;
  Serial.print((int)temperature); Serial.print(" *C, "); 
  Serial.print((int)humidity); Serial.println(" H");
  datas.dmq2=analogRead(mq2);
  Serial.println(datas.dmq2);
  datas.dmq7=analogRead(mq7);
  //Send message to receiver
  Serial.println(datas.dmq7);
//  Serial.println(datas.data);
  radio.write(&datas, sizeof(datas));
  const char text[]="Acknowledge";
  radio.write(&text, sizeof(text));
  delay(1000);
}
