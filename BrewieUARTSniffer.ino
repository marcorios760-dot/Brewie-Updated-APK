/*
  Brewie Serial UART Sniffer

  Using the UART1 and UART2 of the Atmega2560,
  Sniff the RX and TX in the Brewie control board

  Copyright 2017 DrGus
  
  Permission is hereby granted, free of charge, to any person obtaining a copy of 
  this software and associated documentation files (the "Software"), to deal in the 
  Software without restriction, including without limitation the rights to use, copy, 
  modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
  and to permit persons to whom the Software is furnished to do so, subject to the 
  following conditions:
  
  The above copyright notice and this permission notice shall be included in all copies 
  or substantial portions of the Software.
  
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
 */

#define UART_BAUD_RATE 115200 //I figured out Brewie runs at 115200
#define PIN_BREWIE_RESET 3    //Detect when the control board is reset by the master

String  rxBuffer   = "";
String  txBuffer   = "";
boolean txComplete = false;
boolean rxComplete = false;
volatile boolean resetSent = false;

void setup() 
{
  pinMode(PIN_BREWIE_RESET, INPUT);
  attachInterrupt(digitalPinToInterrupt(PIN_BREWIE_RESET), resetISR, FALLING);
  rxBuffer.reserve(200);
  txBuffer.reserve(200);
  Serial.begin(115200);
  Serial1.begin(UART_BAUD_RATE);
  Serial2.begin(UART_BAUD_RATE);
  Serial.println("-----------------------------------------------------");
  Serial.println("Brewie Control Board UART Sniffer V1.0");
  Serial.println("Written by DrGus");
  Serial.println("Copyright 2017 DrGus");
  Serial.println("-----------------------------------------------------");
}

void loop() 
{
  if (rxComplete) 
  {
    Serial.print("Rx\t");
    Serial.println(rxBuffer);
    rxBuffer = "";
    rxComplete = false;
  }
  
  if (txComplete) 
  {
    Serial.print("Tx\t");
    Serial.print(txBuffer);
    txBuffer = "";
    txComplete = false;
  }

  if (resetSent)
  {
    Serial.print("Rst\t");
    Serial.println("Brewie Control Board Reset!");
    resetSent = false;    
  }
}

void resetISR()
{
  resetSent = true;
}

void serialEvent1() 
{
  while (Serial1.available()) {
    delay(15);
    char inChar1 = (char)Serial1.read();
    rxBuffer += inChar1;
  }

  if (rxBuffer != "") 
  {
    rxComplete = true;
  }
}

void serialEvent2() 
{
  while (Serial2.available()) {
    char inChar2 = (char)Serial2.read();
    txBuffer += inChar2;
    if (inChar2 == '\n') 
    {
      txComplete = true;
    }
  }
}

