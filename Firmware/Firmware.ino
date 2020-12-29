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
Tester tester;
bool err;   //flag attivo con anomalia

void setup() {
  // put your setup code here, to run once:
  err=false;    //nessuma anomalia
  tester.setBusy();
  Serial.begin(9600);
  Serial.print("SETUP OK\n");
  // condigurazioni di default
  setConfig(tester,0,0);  
  setSingleAddress(tester,0,true);
  setSingleAddress(tester,0,false);
}

void loop() {
  // put there a while loop that waits for serial data with nPin_DEMUX e nPin_MUX
  bool newData = false;
  uint8_t byte1;
  uint8_t nPinConn1;
  uint8_t nPinConn2;
  uint8_t addr;
  bool boolMatrix[100][100];

  Serial.print("attesa di un comando sulla SERIALE\n");
  uint8_t k=0;
  //ATTENDI PER IL COMANDO
  while(!newData){
    if(Serial.available() > 0){
      byte1 = Serial.read();
      newData=true; 
      Serial.print("Comando ricevuto\n");
      // do i need to clear Serial buffer?
    }
    else{
      tester.setFree(); //spenge il led per far vedere che non è occupato
      delay(500);
      if(k == 10){
        k=0;
        Serial.print("Nessuna operazione comandata\n");
      }
      k++;
    }
  }
  tester.setBusy();
  newData = false;
  
  //boolMatrix = checkContinuity(nPinConn1, nPinConn2, tester);

        // this costructor need to accept npin in parameter. Tester tester(nPinConn1,nPinConn2);
  switch (byte1) 
  {
  case 0b10000000:  // config
    Serial.print("send config");
    nPinConn1 = Serial.read();
    nPinConn2 = Serial.read();
    setConfig(tester, nPinConn1, nPinConn2);
    // IN TEORIA QUI DOVREI LEGGERE DUE BYTE E SCIVERE QUEI VALORI IN NPIN E IN EEPROM
    break;
  case 97:  // config per provarlo dalla seriale 97=a in ASCII
    Serial.print("a case");
    setConfig(tester,10,10);
    setSingleAddress(tester,0,false);
    tester.testWire();
    delay(1000);
    setSingleAddress(tester,0,true);
    tester.testWire();
    delay(1000);
    setSingleAddress(tester,2,false);
    tester.testWire();
    delay(1000);
    setSingleAddress(tester,2,true);
    tester.testWire();
    delay(2000);
    // IN TEORIA QUI DOVREI LEGGERE DUE BYTE E SCIVERE QUEI VALORI IN NPIN E IN EEPROM
    break;
  case 0b10000010:  // sendSingleAddress
  {
    Serial.print("send single address");
    // QUI DOVREI LEGGERE UN BYTE, VEDERE SE L'8AVO BIT è UNO E SE è UNO SETTO ADDRESS MUX ALTRIMENTI SETTO ADDRESS DEMUX
    /* se && con maschera ==1 allora setta il mux con l'address altrimenti setta il demux*/
    uint8_t _single_addr = Serial.read(); //indirizzo da settare
    uint8_t _conn = Serial.read();        //byte contente l'informazione relativa a quale dei due connettori si stà facendo oriferimento
    //SETTA MUX O DEMUX IN FUNZIONE DEI 2 BYTE RICEVUTI
    if(_conn == 0b00001111){              // se contiene 0x0F allora è il MUX/DEMUX da settare
      setSingleAddress(tester,_single_addr,true);   // OCCHIO  a true e false MUX/DEMUX
    }
    else if (_conn == 0b11110000)
    {
      setSingleAddress(tester,_single_addr,false);
    }
    else{
      err = true;
    }
    break;
  }
  case 0b10000100:  // sendEachAddress
  {
    Serial.print("send double address");
    uint8_t _addr1 = Serial.read();
    uint8_t _addr2 = Serial.read();
    setSingleAddress(tester, _addr1, true);
    setSingleAddress(tester, _addr2, false);
    break;
  }
  case 0b10010000:
    Serial.print("single check");
    tester.testWire();
    break;
  case 0b11111111:  // totalCheck
    {
      Serial.print("total check\n\n");
      //numero pin lo dovrebbe ricavare in automatico
      nPinConn1 = 16;
      nPinConn2 = 16;
      for(int i=0; i<nPinConn1; i++){
        setSingleAddress(tester, i, true);
        for(int j=0; j<nPinConn2; j++){
          setSingleAddress(tester, j, false);
          delay(10);
          if(tester.testWire()==true){
            Serial.print("1 ");
          }
          else{
            Serial.print("0 ");
          }
          //boolMatrix[i][j] = tester.testWire();
        }
        Serial.print("\n");
      }/*
      for(int i=0; i<nPinConn1; i++){
        for(int j=0; j<nPinConn2; j++){
          if(boolMatrix[i][j]==true){
            Serial.print(i);
          }
          else{
            Serial.print(j);
          }
        }*/
      
    
      Serial.print("_____________________\n");
    }
    break;  
  default:
    err = true;
    Serial.print("Premuto ");
    Serial.print(byte1);
    Serial.print("\n");
    Serial.print("Comando non riconosciuto sulla seriale\n");
    break;
  }

}

void setConfig(Tester _tester,uint8_t _nPin1, uint8_t _nPin2){
   Serial.print("inizio configurazione\n");
  _tester.setNPinConn1(_nPin1);
  _tester.setNPinConn2(_nPin2);
  Serial.print("configurazione completata\n");
}

void setSingleAddress(Tester _tester, int _addr, bool _MUXflag){  
  if (_MUXflag){
    _tester.setMUX(_addr);
  }
  else{
    _tester.setDEMUX(_addr);
  }
}
