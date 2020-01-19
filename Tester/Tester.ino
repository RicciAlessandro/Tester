/*
  Tester.ino - wiring tester.
  Created by A. Ricci, January 18, 2020.
  Released into the public domain.
*/
#include "Tester.h"


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

  bool boolMatrix[nPinConn1][nPinConn2];
  Tester tester;    // this costructor need to accept npin in parameter. Tester tester(nPinConn1,nPinConn2);
  

  Serial.print("START TESTING\n\n");
  for(int i=0; i<nPinConn1; i++){
    tester.setDEMUX(i);
    for (int j=0; j<nPinConn2; j++){
      tester.setMUX(j);
      delay(1); //delay us?
      boolMatrix[i][j] = tester.testWire();
    }
    Serial.print("pin ");
    Serial.print( String(i+1));
    Serial.print("/");
    Serial.print( String(nPinConn1));
    Serial.print(" tested \n");
  }
  Serial.print(" DONE \n\n");
  
  // insert here serial print versus PC
  for(int i=0; i<nPinConn1; i++){
    for (int j=0; j<nPinConn2; j++){
      String text = String(boolMatrix[i][j],HEX);
      Serial.print(text);  //serial.write() is only for char or byte
    }
    Serial.print("\n");
  }
  while(true){
    
  }
  
}
