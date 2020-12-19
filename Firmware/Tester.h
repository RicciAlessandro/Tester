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
#define nPinAddress 6

#include "Arduino.h"


class Tester{
  public:
    Tester();                   //unique costructor
                                //METHODS
    bool testWire();            //test the selected continuity from adrres demux pin to addres mux pin
    void setDEMUX(int addr);   //set a determinate address for MUX/DEMUX
    void setMUX(int addr);
    void setNPinConn1(int nPin);  // numero di pin del connettore 2
    void setNPinConn2(int nPin);  // numero di pin del connettore 2
    int getNPinConn1();  // numero di pin del connettore 2
    int getNPinConn2();  // numero di pin del connettore 2
    
    //void setMUX();
    //void incMUX();              //increment DEMUX/MUX but it's not so usefull
    //void incDEMUX();            //queste funzioni potrebbero essere private e comandate dal comando read
  private:
    int _nPinDEMUX = nPinAddress;               //numero dei pin fisici con i quali vengono comandati gli address
    int _nPinMUX = nPinAddress;
    int _nPinConn1;               // numero dei pin del connettore 1 sotto test
    int _nPinConn2;
    // qui non ho capito perchè non posso dichiarare il vettore e assegnarlo nel costruttore
    int _pinDEMUX[6] = {DEMUX_A0,DEMUX_A1,DEMUX_A2,DEMUX_A3,DEMUX_A4,DEMUX_A5};              // è possibile definirlo come costante?
    int _pinMUX[6] = {MUX_A0,MUX_A1,MUX_A2,MUX_A3,MUX_A4,MUX_A5};   
};
#endif
