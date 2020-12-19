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
/*
int nPinConn1=0;
int nPinConn2=0;*/
Tester tester;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.print("SETUP OK\n");
  setConfig(tester);
  setSingleAddress(tester,0,true);
  setSingleAddress(tester,0,false);
}

void loop() {
  // put there a while loop that waits for serial data with nPin_DEMUX e nPin_MUX
  bool newData = false;
  int byte1;
  int nPinConn1;
  int nPinConn2;
  int addr;

  Serial.print("attesa di un comando sulla SERIALE\n");
  /*
  while(!newData){
    if(Serial.available() > 0){
      byte1=Serial.read(); // legge il byte che indica l'operazione da svolgere
      newData=true; 
      Serial.print("operazione = ");
      Serial.print(byte1);
      Serial.print("\n");
      //LEGGI nPinConn1e2, se non ci sono ritorna in ascolto da zero
      if(Serial.available() > 0){
        nPinConn1 = Serial.read();  // legge il byte che indica il numero di pin del primo connettore
        Serial.print("nPinConn1 = ");
        Serial.print(nPinConn1);
        Serial.print("\n");
      }
      else{
        Serial.print("no nPinConn1");
        continue;  // se non c'è il byte ritorna in attesa di un comando sulla seriale
      }
      if(Serial.available() > 0){
        nPinConn2 = Serial.read();  // legge il byte che indica il numero di pin del primo connettore
        Serial.print("nPinConn2 = ");
        Serial.print(nPinConn2);
        Serial.print("\n");
      }
      else{
        Serial.print("no nPinConn2");
        continue;  // se non c'è il byte ritorna in attesa di un comando sulla seriale
      }
      // fai l'operazione richiesta contenuta nel byte letto sulla seriale
      switch (byte1)
      {
      case 0:
        Serial.print("test automatico\n");
        testAumatico(nPinConn1,nPinConn2);
        Serial.print("-DONE-\n");
        break;
      case 1:
        if(Serial.available() > 0){
          addr = Serial.read();  // legge il byte che indica il numero di pin del primo connettore
          Serial.print("addr = ");
          Serial.print(addr);
          Serial.print("\n");
        }
        else{
          Serial.print("no addr");
          continue;  // se non c'è il byte ritorna in attesa di un comando sulla seriale
        }
        Serial.print("setAddres in output\n");
        setOutputAddress(nPinConn1,nPinConn2,addr);
      break;
      case 1:
        Serial.print("setAddres in input\n");
      break;
      
      default:
        Serial.print("operazione richiesta non consentita\n");
        break;
      }
      Serial.print("Comando ricevuto\n");

      // do i need to clear Serial buffer?
     }
     delay(100);
  }
  */
  int i=0;
  while(!newData){
    if(Serial.available() > 0){
      byte1 = Serial.read();
      //byte1=Serial.read(); do i need 2 bytes for this data?
      //byte1=Serial.read();
      newData=true; 
      Serial.print("Comando ricevuto\n");
      // do i need to clear Serial buffer?
    }
    else{
      delay(1000);
      if(i == 10){
        i=0;
        Serial.print("Nessuna operazione comandata\n");
      }
      i++;
    }
  }
  
  newData = false;
  
  
  delay(1000);
  //nPinConn1 = 40;
  //nPinConn2 = 40;
  
  bool boolMatrix[100][100];
  //boolMatrix = checkContinuity(nPinConn1, nPinConn2, tester);

        // this costructor need to accept npin in parameter. Tester tester(nPinConn1,nPinConn2);
  switch (byte1) 
  {
  case 0b10000000:  // config
    setConfig(tester);
    // IN TEORIA QUI DOVREI LEGGERE DUE BYTE E SCIVERE QUEI VALORI IN NPIN E IN EEPROM
    break;
  
  
  case 97:  // config per provarlo dalla seriale 97=a in ASCII
    setConfig(tester);
    setSingleAddress(tester,0,false);
    delay(1000);
    setSingleAddress(tester,1,false);
    delay(1000);
    setSingleAddress(tester,2,false);
    delay(1000);
    setSingleAddress(tester,3,false);
    delay(1000);
    setSingleAddress(tester,4,false);
    delay(1000);
    setSingleAddress(tester,5,false);
    delay(1000);

    setSingleAddress(tester,0,true);
    delay(1000);
    setSingleAddress(tester,1,true);
    delay(1000);
    setSingleAddress(tester,2,true);
    delay(1000);
    setSingleAddress(tester,3,true);
    delay(1000);
    setSingleAddress(tester,4,true);
    delay(1000);
    setSingleAddress(tester,5,true);
    // IN TEORIA QUI DOVREI LEGGERE DUE BYTE E SCIVERE QUEI VALORI IN NPIN E IN EEPROM
    break;

  
  
  case 0b10000010:  // sendiSingleAddress
    // QUI DOVREI LEGGERE UN BYTE, VEDERE SE L'8AVO BIT è UNO E SE è UNO SETTO ADDRESS MUX ALTRIMENTI SETTO ADDRESS DEMUX
    /* se && con maschera ==1 allora setta il mux con l'address altrimenti setta il demux*/
    setSingleAddress(tester,0,false);
    break;
  
  case 0b10000100:  // sendiEachAddress
    Serial.print("TotalCheck\n");
    break;
  
  case 0b10001000:  // totalChecks
    Serial.print("TotalCheck\n");
    break;

  
  
  default:
    Serial.print("Premuto ");
    Serial.print(byte1);
    Serial.print("\n");
    Serial.print("Comando non riconosciuto sulla seriale\n");
    break;
  }
}

void setConfig(Tester _tester){
  // qua dovrei fare un read e vedere quanti pin mi sta mandando
  int _nPin1;
  int _nPin2;
  _nPin1 = 10;
  _nPin2 = 10;
  /*
  _nPin1 = Serial.read();
  _nPin2 = Serial.read();
  _nPin1 = _nPin1 & 0b01111111;
  _nPin2 = _nPin2 & 0b01111111;
  */
   Serial.print("inizio configurazione\n");
  _tester.setNPinConn1(_nPin1);
  _tester.setNPinConn2(_nPin2);
  Serial.print("configurazione completata\n");
}

void setSingleAddress(Tester _tester, int _addr, bool _MUXflag){
  // legge il byte, se il MSB è 1 setta il DEMUX, se è zero setta il DEMUX
  
  _addr = _addr & 0b01111111;

  /*
  _byte = Serial.read();
  _MUXflag = (_byte>>7) && 0b00000001;
  */
 //indirizzo di prova
  
  if (_MUXflag){
    _tester.setMUX(_addr);
    //Serial.print("MUX ");
  }
  else{
    _tester.setDEMUX(_addr);
    //Serial.print("DEMUX ");
  }/*
  Serial.print("settato l'indirizzo: ");
  Serial.print(_addr);
  Serial.print("\n");*/
}
/*
bool setOutputAddress(Tester _tester, int _addr){
  _tester.setDEMUX(_addr);
  Serial.print("selezionata l'uscita numero");
  Serial.print(_addr);
}
bool setInputAddress(Tester _tester, int _addr){
  _tester.setDEMUX(_addr);
  Serial.print("selezionata l'uscita numero");
  Serial.print(_addr);
}
*/

void chekWiring(Tester tester){
  bool boolMatrix[100][100];
  int _nPinConn1 = tester.getNPinConn1();
  int _nPinConn2 = tester.getNPinConn1();

  Serial.print("START TESTING \n");
  for(int i=0; i<_nPinConn1; i++){
    //Serial.write(35);//35 in decimale è # in ASCII
    //Serial.write(10);//10 in decimale è \n in ASCII
    tester.setDEMUX(i);
    
    for (int j=0; j<_nPinConn2; j++){
      tester.setMUX(j);
      //Serial.write(36);
      //Serial.write(10);
      boolMatrix[i][j] = tester.testWire();
    }
    Serial.print("pin ");
    Serial.print(i+1);
    Serial.print("/");
    Serial.print(_nPinConn1);
    Serial.print(" tested \n");
  }
  Serial.print("DONE \n\n");
  // insert here serial print versus PC
  for(int i=0; i<_nPinConn1; i++){
    for (int j=0; j<_nPinConn2; j++){
      Serial.print(int(boolMatrix[i][j]));
      Serial.print(" ");
    }
    Serial.print("\n");
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