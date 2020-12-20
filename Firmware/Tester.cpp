#include "Arduino.h"
#include "Tester.h"

Tester::Tester(){
  //SET PINMODE
  pinMode(IN_SIGNAL,INPUT_PULLUP);
  // set all the MUX_AX address pin output 

  //int _nPinDEMUX = sizeof(_pinDEMUX);
  //int _nPinMUX = sizeof(_pinMUX);
  _nPinConn1 = 0;
  _nPinConn2 = 0;// questo valore andrebbe letto dalla EEPROM
  _busy = false;
  // setto tutti i pin degli address in uscita
  for( int i=0; i<_nPinDEMUX; i++){     // set address pin of DEMUX in output
    pinMode(_pinDEMUX[i],OUTPUT);
  }
  for( int i=0; i<_nPinMUX; i++){       // set address pin of MUX in output
    pinMode(_pinMUX[i],OUTPUT);
  }
  pinMode(ledPin,OUTPUT);
  pinMode(ledBusy,OUTPUT);
  // non c'è bisogno che setto il pin di lettura continuità come ingresso
}

void Tester::setBusy(){
  _busy = true;
  digitalWrite(ledBusy, true);
}

void Tester::setFree(){
  _busy = true;
  digitalWrite(ledBusy, false);
}

void Tester::setNPinConn1(int nPin){
  _nPinConn1 = nPin;
}
void Tester::setNPinConn2(int nPin){
  _nPinConn2 = nPin;
}

bool Tester::testWire() // check continuity between pre setted pins and pilot ledPin to show the result
{
  bool isConnected = false;
  int readedValue = digitalRead(IN_SIGNAL);
  if(readedValue==LOW){
    isConnected = true;
    digitalWrite(ledPin,HIGH);
  }else{
    digitalWrite(ledPin,LOW);
  }
  return isConnected;
}

void Tester::setDEMUX(int addr){   //READ HERE!!! here i can use DDRX and PORTX for assign port status immediatly or i can convert address in a sting that contain address in binary and compare single String index: String ad = String(addr,BIN), and then addr[i]=="0" or =="1"
  //Serial.print("\n\nSET DEMUX   \n\n");
  for( int i=0; i<_nPinDEMUX; i++)       // set address pin of MUX in output
  {
    if ((addr>>i) & 0b00000001==0b00000001) // (bitshift right x i ) AND with mask. !!! can i omit the last equality?
    {
      digitalWrite(_pinDEMUX[i],true);
      //Serial.print("true\n");
    }
    else
    {
      digitalWrite(_pinDEMUX[i],false);
      //Serial.print("false\n");
    }
  }
}

void Tester::setMUX(int addr){
 for(int i=0; i<_nPinMUX; i++)       // set address pin of MUX in output
  {
    if ((addr>>i) & 0b00000001==0b00000001) // (bitshift right x i ) AND with mask
    {
      digitalWrite(_pinMUX[i],true);
    }
    else
    {
      digitalWrite(_pinMUX[i],false);
    }
  }
}