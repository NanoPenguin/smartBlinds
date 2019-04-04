/* 
 * Demo for SSD1306 based 128x64 OLED module using Adafruit SSD1306 
 * library (https://github.com/adafruit/Adafruit_SSD1306).
 * 
 * See https://github.com/pacodelgado/arduino/wiki/SSD1306-based-OLED-connected-to-Arduino 
 * for more information.
 *
 */
 
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// If using software SPI (the default case):
#define OLED_MOSI  11   //D1
#define OLED_CLK   12   //D0
#define OLED_DC    9
#define OLED_CS    8
#define OLED_RESET 10

Adafruit_SSD1306 display(OLED_MOSI, OLED_CLK, OLED_DC, OLED_RESET, OLED_CS);

int loopTime = 1000;
unsigned long lastSwitch = 0;
bool time = false;

void setup()   {                
//  Serial.begin(9600);
  display.begin(SSD1306_SWITCHCAPVCC);
  //display.display();
  //delay(1000);
  display.clearDisplay();
  display.setTextSize(1.7);
  display.setTextColor(WHITE);
}

void loop()
{
  if(millis()-lastSwitch>loopTime){
    lastSwitch = millis();
    time=!time;
  }
  display.clearDisplay();
  
  if(time){
    display.setCursor(20,5);
    display.setTextSize(3);
    display.print("15:55");
  }else{
    display.setCursor(0,10);
    display.setTextSize(1);
    display.print("    Lejonkungarna \n");
    display.print("     is the best \n");
  }
  display.display();
}
