/*
  Tester.cpp - source code for control of wiring tester.
  Created by A. Ricci, January 18, 2020.
  Released into the public domain.
*/
#include "Arduino.h"
#include "Tester.h"

Tester::Tester()
{
  
  pinMode(IN_SIGNAL,INPUT_PULLUP);//_PULLUP);
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
  if (digitalRead(IN_SIGNAL)== HIGH)
  {
    return false;
  }
  else
  {
    return true; 
  }
}

void Tester::setDEMUX(int addr){
  //ADDRESS_0
  if ((addr & B00000001)==B00000001)
  {
    digitalWrite(DEMUX_A0,HIGH);
  }
  else
  {
    digitalWrite(DEMUX_A0,LOW);
  }
  //ADDRESS_1
  if ((addr & B00000010)==B00000010)
  {
    digitalWrite(DEMUX_A1,HIGH);
  }
  else
  {
    digitalWrite(DEMUX_A1,LOW);
  }
  //ADDRESS_2
  if ((addr & B00000100)==B00000100)
  {
    digitalWrite(DEMUX_A2,HIGH);
  }
  else
  {
    digitalWrite(DEMUX_A2,LOW);
  }
  //ADDRESS_3
  if ((addr & B00001000)==B00001000)
  {
    digitalWrite(DEMUX_A3,HIGH);
  }
  else
  {
    digitalWrite(DEMUX_A3,LOW);
  }
  //ADDRESS_4
  if ((addr & B00010000)==B00010000)
  {
    digitalWrite(DEMUX_A4,HIGH);
  }
  else
  {
    digitalWrite(DEMUX_A4,LOW);
  }
  //ADDRESS_5
  if ((addr & B00100000)==B00100000)
  {
    digitalWrite(DEMUX_A5,HIGH);
  }
  else
  {
    digitalWrite(DEMUX_A5,LOW);
  }
}


void Tester::setMUX(int addr){
  //ADDRESS_0
  if ((addr & B00000001)==B00000001)
  {
    digitalWrite(MUX_A0,HIGH);
  }
  else
  {
    digitalWrite(MUX_A0,LOW);
  }
  //ADDRESS_1
  if ((addr & B00000010)==B00000010)
  {
    digitalWrite(MUX_A1,HIGH);
  }
  else
  {
    digitalWrite(MUX_A1,LOW);
  }
  //ADDRESS_2
  if ((addr & B00000100)==B00000100)
  {
    digitalWrite(MUX_A2,HIGH);
  }
  else
  {
    digitalWrite(MUX_A2,LOW);
  }
  //ADDRESS_3
  if ((addr & B00001000)==B00001000)
  {
    digitalWrite(MUX_A3,HIGH);
  }
  else
  {
    digitalWrite(MUX_A3,LOW);
  }
  //ADDRESS_4
  if ((addr & B00010000)==B00010000)
  {
    digitalWrite(MUX_A4,HIGH);
  }
  else
  {
    digitalWrite(MUX_A4,LOW);
  }
  //ADDRESS_5
  if ((addr & B00100000)==B00100000)
  {
    digitalWrite(MUX_A5,HIGH);
  }
  else
  {
    digitalWrite(MUX_A5,LOW);
  }
}
