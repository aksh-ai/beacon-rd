#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

//create an RF24 object
RF24 radio(7, 8);  // CE, CSN
int ackled=6;
//address through which two modules communicate.
const byte address[6] = "00001";
typedef struct{
  int data1;
  int data2;
  int dtemp;
  int dhum;
}Data;
Data datas;
void setup()
{
  while (!Serial);
    Serial.begin(9600);
  
  radio.begin();
  //radio.setPALevel(RF24_PA_HIGH);
  //set the address
  radio.openReadingPipe(0, address);
  pinMode(ackled,OUTPUT);
  //Set module as receiver
  radio.startListening();
}

void loop()
{
  //Read the data if available in buffer
//  if (radio.available())
//  {

    const char text[32]= {0};
    radio.read(&datas,sizeof(datas));
    
    radio.read(&text, sizeof(text));
    
    if(String(text)=="Acknowledge"){
      Serial.print(datas.data1);
      Serial.print(",");
    Serial.print(datas.data2);
    Serial.print(",");
    Serial.print(datas.dtemp);  
    Serial.print(",");  
    Serial.print(datas.dhum);
    Serial.print(",");
    Serial.print(text);
    Serial.println("");
    }
    else{
      digitalWrite(ackled,HIGH);
      delay(500);
      digitalWrite(ackled,LOW);
    }
  
delay(500);
}
