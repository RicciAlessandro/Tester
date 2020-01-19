#include "Tester.h"

Tester tester;

byte nPinConn1=0;
byte nPinConn2=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  /* put there a while loop that waits fpr serial data qith nPin_DEMUX e nPin_MUX
  while(!newData) 
  {
     if(Serial.available() > 0){
        byte1=Serial.read();
        byte1=Serial.read(); do i need 2 bytes for this data?
        byte1=Serial.read();
        newData=true; 
        // do i need to clear Serial buffer?
     }
  }
  newData = false
  */
  nPinConn1 = 40;
  nPinConn2 = 40;

  for(int i=0; i<nPinConn1; i=i+1){
    tester.setDEMUX(i);
    for (int j=0; j<nPinConn2; j=j+1){
      tester.setMUX(j);
      delay(10); //delay ms?
      //boolMatrix[i][j] = tester.testWire;
    }
  }
  // insert here serial print versus PC
}
