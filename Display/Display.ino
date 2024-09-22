/*
 * Author: Seth Klupka (dyw246).
 * Modified example: File > Examples > RGB matrix Panel > testshapes_32x64.
 * Examples require 'RGB matrix Panel' by Adafruit library installed.
 * Code for the RGB matrix panel.
 * Programmed to the Arduino Mega 2560.
 */
#include <RGBmatrixPanel.h>
#include <string.h>

//CLK was changed for compatibility with Arduino Mega 2560.
#define CLK 11
#define OE   9
#define LAT 10
#define A   A0
#define B   A1
#define C   A2
#define D   A3

RGBmatrixPanel matrix(A, B, C, D, CLK, LAT, OE, false, 64);

size_t bytesReceived;
char messageBuffer[64];
bool messagedReceived;

void setup() {

  //Start both serial ports.                            
  matrix.begin();
  Serial.begin(9600);
  Serial1.begin(9600);
  bool messagedReceived = false;
  matrix.setCursor(0, 0);    // next line
  matrix.setTextColor(matrix.Color333(7,7,7));
}

// Main loop.
void loop()
{
  // Clear old message.
  messageBuffer[bytesReceived] = '\0';
  // Bytes read up until '@' in string. '@' is terminating character.
  bytesReceived = Serial1.readBytesUntil('@', messageBuffer, 62);
  
  //If messaged recieved print message data.
  if(bytesReceived > 0)
  {
    // Erase old message
    matrix.fillRect(0, 0, matrix.width(), matrix.height(), matrix.Color333(0, 0, 0));
    matrix.setCursor(0, 0); 


    //loop for printing each line (separated by \n) with different color
    int i = 0;
    char * token = strtok(messageBuffer, "\n");
    // loop through the string to extract all other tokens
    while( token != NULL ) {
      switch(i){
        case 0: //humidity
          //matrix.setTextColor(matrix.Color333(7,7,7));
          //break;
        case 1: //light
          matrix.setTextColor(matrix.Color333(7,7,7)); // white for both light and humidity currently
          break;
        case 2:  //risk, print different risk levels AND/OR injury type with different colors 
          if(strcmp(token, "R: Low") == 0 || strcmp(token, "no-injury") == 0)
             matrix.setTextColor(matrix.Color333(144,238,144)); //traffic green
          else if(strcmp(token, "R: Medium") == 0 || strcmp(token, "possible") == 0 || strcmp(token, "minor") == 0)
            matrix.setTextColor(matrix.Color333(255,50,0));  //traffic orange
          else // risk is high, injury types: fatal, serious, unknown
            matrix.setTextColor(matrix.Color333(255,0,0)); // traffic red  
          break;
      }
      Serial.println(token); 
      matrix.println(token); //printing each token
      token = strtok(NULL, "\n");
      i++;
    }

    // Delay 2 seconds, if no delay the no data will overwrite msg.
    delay(2000);
  }
  
  //If no message recieved print "No data".
  if(!bytesReceived)
  {
    matrix.setTextColor(matrix.Color333(7,0,0));
    matrix.print("No data");
    delay(1800);
    matrix.fillRect(0, 0, matrix.width(), matrix.height(), matrix.Color333(0, 0, 0));
    matrix.setCursor(0, 0); 
  }
 } 
