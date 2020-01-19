#include "Arduino.h"
#include "Tester.h"

Tester::Tester()
{
  pinMode(IN_SIGNAL,INPUT_PULLUP);
  // set all the MUX_A address pin output 
  pinMode(DEMUX_A0,OUTPUT);
  pinMode(DEMUX_A1,OUTPUT);
  pinMode(DEMUX_A2,OUTPUT);
  pinMode(DEMUX_A3,OUTPUT);
  pinMode(DEMUX_A4,OUTPUT);
  pinMode(DEMUX_A5,OUTPUT);  
  // set all the MUX_A address pin output 
  pinMode(MUX_A0,OUTPUT);
  pinMode(MUX_A1,OUTPUT);
  pinMode(MUX_A2,OUTPUT);
  pinMode(MUX_A3,OUTPUT);
  pinMode(MUX_A4,OUTPUT);
  pinMode(MUX_A5,OUTPUT);
}

bool Tester::testWire()
{
  return digitalRead(IN_SIGNAL);
}

void Tester::setDEMUX(byte addr){
  //ADDRESS_0
  if (addr & 0b00000001==0b00000001)
  {
    digitalWrite(DEMUX_A0,true);
  }
  else
  {
    digitalWrite(DEMUX_A0,false);
  }
  //ADDRESS_1
  if (addr & 0b00000010==0b00000010)
  {
    digitalWrite(DEMUX_A1,true);
  }
  else
  {
    digitalWrite(DEMUX_A1,false);
  }
  //ADDRESS_2
  if (addr & 0b00000100==0b00000100)
  {
    digitalWrite(DEMUX_A2,true);
  }
  else
  {
    digitalWrite(DEMUX_A2,false);
  }
  //ADDRESS_3
  if (addr & 0b00001000==0b00001000)
  {
    digitalWrite(DEMUX_A3,true);
  }
  else
  {
    digitalWrite(DEMUX_A3,false);
  }
  //ADDRESS_4
  if (addr & 0b00010000==0b00010000)
  {
    digitalWrite(DEMUX_A4,true);
  }
  else
  {
    digitalWrite(DEMUX_A4,false);
  }
  //ADDRESS_5
  if (addr & 0b00100000==0b00100000)
  {
    digitalWrite(DEMUX_A5,true);
  }
  else
  {
    digitalWrite(DEMUX_A5,false);
  }
}


void Tester::setMUX(byte addr){
  //ADDRESS_0
  if (addr & 0b00000001==0b00000001)
  {
    digitalWrite(MUX_A0,true);
  }
  else
  {
    digitalWrite(MUX_A0,false);
  }
  //ADDRESS_1
  if (addr & 0b00000010==0b00000010)
  {
    digitalWrite(MUX_A1,true);
  }
  else
  {
    digitalWrite(MUX_A1,false);
  }
  //ADDRESS_2
  if (addr & 0b00000100==0b00000100)
  {
    digitalWrite(MUX_A2,true);
  }
  else
  {
    digitalWrite(MUX_A2,false);
  }
  //ADDRESS_3
  if (addr & 0b00001000==0b00001000)
  {
    digitalWrite(MUX_A3,true);
  }
  else
  {
    digitalWrite(MUX_A3,false);
  }
  //ADDRESS_4
  if (addr & 0b00010000==0b00010000)
  {
    digitalWrite(MUX_A4,true);
  }
  else
  {
    digitalWrite(MUX_A4,false);
  }
  //ADDRESS_5
  if (addr & 0b00100000==0b00100000)
  {
    digitalWrite(MUX_A5,true);
  }
  else
  {
    digitalWrite(MUX_A5,false);
  }
}
