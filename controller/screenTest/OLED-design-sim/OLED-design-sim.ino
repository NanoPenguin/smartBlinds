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

//int loopTime = 4000;
//unsigned long lastSwitch = 0;
//bool time = false;

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
  display.clearDisplay();

  display.setCursor(62,0);
  display.setTextSize(1);
  display.print("\x18\n");          //uppil
  display.setCursor(35,9);
  display.setTextSize(2);
  display.print("15:55");           //klocka
  display.setTextSize(1);
  display.setCursor(62,25);
  display.print("\x19\n");          //nerpil

  display.display();
  delay(2000);
  display.clearDisplay();

  display.setCursor(0,0);
  display.setTextSize(1);
  display.setTextColor(WHITE);      //omarkerad
  display.print("        ALARM       \n");
  display.setTextColor(BLACK, WHITE); //nästa är markerad, x4 är valt alarm
  display.print("06:00               \n");
  display.setTextColor(WHITE);      //omarkerad
  display.print("06:45              \x4\n");
  display.print("NYTT ALARM\n");
  
  display.display();
  delay(1000);
  display.clearDisplay();

  display.setCursor(0,0);
  display.setTextSize(1);
  display.setTextColor(WHITE);      //omarkerad
  display.print("        ALARM       \n");
  display.print("06:00               \n");
  display.setTextColor(BLACK, WHITE); //nästa är markerad, x4 är valt alarm
  display.print("06:45              \x4\n");
  display.setTextColor(WHITE);      //omarkerad
  display.print("NYTT ALARM\n");

  display.display();
  delay(1000);
  display.clearDisplay();

  display.setCursor(0,0);
  display.setTextSize(1);
  display.setTextColor(WHITE);      //omarkerad
  display.print("        ALARM       \n");
  display.print("06:00               \n");
  display.print("06:45              \x4\n");
  display.setTextColor(BLACK, WHITE); //nästa är markerad, x4 är valt alarm
  display.print("NYTT ALARM          \n");
  display.setTextColor(WHITE);      //omarkerad

  
  display.display();
  delay(1000);
}
