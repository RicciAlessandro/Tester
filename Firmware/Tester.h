/*
  Tester.h - Library for control of wiring tester.
  Created by A. Ricci, January 18, 2020.
  Released into the public domain.
*/
#ifndef Tester_h
#define Tester_h

#define DEMUX_A0 2
#define DEMUX_A1 3
#define DEMUX_A2 4
#define DEMUX_A3 5
#define DEMUX_A4 6
#define DEMUX_A5 7

#define MUX_A0 A0
#define MUX_A1 A1
#define MUX_A2 A2
#define MUX_A3 A3
#define MUX_A4 A4
#define MUX_A5 A5

#define IN_SIGNAL 8     //26

#include "Arduino.h"


class Tester
{
  public:
    Tester();                   //unique costructor
                                //METHODS
    bool testWire();            //test the selected continuity from adrres demux pin to addres mux pin
    void setDEMUX(int addr);   //set a determinate address for MUX/DEMUX
    void setMUX(int addr);
    //void setMUX();
    //void incMUX();              //increment DEMUX/MUX but it's not so usefull
    //void incDEMUX();            //queste funzioni potrebbero essere private e comandate dal comando read
  private:
    int _pinDEMUX[];              // è possibile definirlo come costante?
    int _pinMUX[];     
};

#endif
