/*
  Tester.ino - wiring tester.
  Created by A. Ricci, January 18, 2020.
  Released into the public domain.
*/
#include "Tester.h"
#include <string.h>

/*
#include "stdafx.h"
#include <iostream>
*/

int nPinConn1=0;
int nPinConn2=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.print("SETUP OK\n");
}

void loop() {
  // put there a while loop that waits for serial data with nPin_DEMUX e nPin_MUX
  bool newData = false;
  Serial.print("attesa di un comando sulla SERIALE\n");
  while(!newData){
    if(Serial.available() > 0){
      int byte1=Serial.read();
      //byte1=Serial.read(); do i need 2 bytes for this data?
      //byte1=Serial.read();
      newData=true; 
      Serial.print("Comando ricevuto\n");
      // do i need to clear Serial buffer?
     }
     delay(100);
  }
  newData = false;
  Tester tester;
  
  delay(1000);
  nPinConn1 = 40;
  nPinConn2 = 40;
  
  bool boolMatrix[40][40];
  //boolMatrix = checkContinuity(nPinConn1, nPinConn2, tester);

        // this costructor need to accept npin in parameter. Tester tester(nPinConn1,nPinConn2);
    
  Serial.print("START TESTING \n");
  for(int i=0; i<nPinConn1; i++){
    //Serial.write(35);//35 in decimale è # in ASCII
    //Serial.write(10);//10 in decimale è \n in ASCII
    tester.setDEMUX(i);
    
    for (int j=0; j<nPinConn2; j++){
      tester.setMUX(j);
      //Serial.write(36);
      //Serial.write(10);
      boolMatrix[i][j] = tester.testWire();
    }
    Serial.print("pin ");
    Serial.print(i+1);
    Serial.print("/");
    Serial.print(nPinConn1);
    Serial.print(" tested \n");
  }
  Serial.print("DONE \n\n");
  // insert here serial print versus PC
  for(int i=0; i<nPinConn1; i++){
    for (int j=0; j<nPinConn2; j++){
      Serial.print(int(boolMatrix[i][j]));
      Serial.print(" ");
    }
    Serial.print("\n");
  }
  while(true){  

  }
}

/*
bool checkContinuity(int _nPinConn1, int _nPinConn2, Tester _tester){  
  //bool boolMatrix[nPinConn1][nPinConn2];
  
    bool boolMatrix[40][40];
        // this costructor need to accept npin in parameter. Tester tester(nPinConn1,nPinConn2);
    

    Serial.print("START TESTING\n");
    for(int i=0; i<_nPinConn1; i++){
      _tester.setDEMUX(i);
      for (int j=0; j<_nPinConn2; j++){
        _tester.setMUX(j);
        delay(1); //delay us?
        boolMatrix[i][j] = _tester.testWire();
      }
      Serial.print("pin ");
      Serial.print(String(i+1));
      Serial.print("/");
      Serial.print(String(_nPinConn1));
      Serial.print(" tested \n");
    }
    Serial.print("DONE \n\n");
  return boolMatrix;
}
*/