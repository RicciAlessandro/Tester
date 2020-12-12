#include "Arduino.h"
#include "Tester.h"

Tester::Tester()
{
  //SET PINMODE
  pinMode(IN_SIGNAL,INPUT_PULLUP);
  // set all the MUX_AX address pin output 
  byte _pinDEMUX[] = {DEMUX_A0,DEMUX_A1,DEMUX_A2,DEMUX_A3,DEMUX_A4,DEMUX_A5};
  byte _pinMUX[] = {MUX_A0,MUX_A1,MUX_A2,MUX_A3,MUX_A4,MUX_A5};

  for( int i=0; i<sizeof(_pinDEMUX); i++)     // set address pin of DEMUX in output
  {
    pinMode(_pinDEMUX[i],OUTPUT);
  }
  for( int i=0; i<sizeof(_pinMUX); i++)       // set address pin of MUX in output
  {
    pinMode(_pinMUX[i],OUTPUT);
  }
}


bool Tester::testWire()
{
  return digitalRead(IN_SIGNAL);
}

void Tester::setDEMUX(byte addr){   //READ HERE!!! here i can use DDRX and PORTX for assign port status immediatly or i can convert address in a sting that contain address in binary and compare single String index: String ad = String(addr,BIN), and then addr[i]=="0" or =="1"
  for( int i=0; i<sizeof(_pinDEMUX); i++)       // set address pin of MUX in output
  {
    if ((addr>>i) & 0b00000001==0b00000001) // (bitshift right x i ) AND with mask. !!! can i omit the last equality?
    {
      digitalWrite(_pinDEMUX[i],true);
    }
    else
    {
      digitalWrite(_pinDEMUX[i],false);
    }
  }
}


void Tester::setMUX(byte addr){
 for( int i=0; i<sizeof(_pinMUX); i++)       // set address pin of MUX in output
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
