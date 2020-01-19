/*
  Tester.h - Library for control of wiring tester.
  Created by A. Ricci, January 18, 2020.
  Released into the public domain.
*/
#ifndef Tester_h
#define Tester_h

#define DEMUX_A0 5
#define DEMUX_A1 6
#define DEMUX_A2 7
#define DEMUX_A3 8
#define DEMUX_A4 9
#define DEMUX_A5 10

#define MUX_A0 19
#define MUX_A1 20
#define MUX_A2 21
#define MUX_A3 22
#define MUX_A4 23
#define MUX_A5 24

#define IN_SIGNAL 26

#include "Arduino.h"


class Tester
{
  public:
    Tester();                   //unique costructor
                                //METHODS
    bool testWire();            //test the selected continuity from adrres demux pin to addres mux pin
    void setDEMUX(byte addr);   //set a determinate address for MUX/DEMUX
    void setMUX(byte addr);
    //void setMUX();
    //void incMUX();              //increment DEMUX/MUX but it's not so usefull
    //void incDEMUX();            //queste funzioni potrebbero essere private e comandate dal comando read
  private:
    int _pinDEMUX[];              // è possibile definirlo come costante?
    int _pinMUX[];     
};

#endif
