//Include Libraries
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

//create an RF24 object
RF24 radio(7, 8);  // CE, CSN
#define mq6 A1
#define mq135 A0
//address through which two modules communicate.
const byte address[6] = "00001";
typedef struct{
  int dmq6;
  int dmq135;
  
}Data;
Data datas;
void setup()
{
  radio.begin();
  Serial.begin(9600);
  pinMode(mq6,INPUT);
  pinMode(mq135,INPUT);
  //set the address
  radio.openWritingPipe(address);
  
  //Set module as transmitter
  radio.stopListening();
}
void loop()
{
  datas.dmq6=analogRead(mq6);
  Serial.println(datas.dmq6);
  datas.dmq135=analogRead(mq135);
  //Send message to receiver
  Serial.println(datas.dmq135);
//  Serial.println(datas.data);
  radio.write(&datas, sizeof(datas));
  const char text[]="Hello World";
  radio.write(&text, sizeof(text));
  delay(1000);
}
