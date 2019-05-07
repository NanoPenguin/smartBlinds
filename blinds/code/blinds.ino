#include <math.h>

const byte buffSize = 40;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;

unsigned long curMillis;

unsigned long prevReplyToPCmillis = 0;
unsigned long replyToPCinterval = 1000;
char messageFromPC[buffSize] = {0};

int arguments[5];
int numberOfArg = 0;

int setpoint = 0;
int incomingSetpoint = 0;
int plus = 3;
int minus = 2;
int feedbackPot;
int tolerance = 5;

void setup() {
  // put your setup code here, to run once:
  pinMode(plus, OUTPUT); //Nedre på motorn
  pinMode(minus, OUTPUT); // Övre på motorn
  setpoint = analogRead(A0);
  feedbackPot = analogRead(A0);
  Serial.begin(9600);
  Serial.println("<Arduino is ready>");
}

void loop() {
  // put your main code here, to run repeatedly: 
  getDataFromPC();
  callFunction();
}

void getDataFromPC() {
  curMillis = millis();

  // receive data from PC and save it into inputBuffer

  if(Serial.available() > 0) {

    char x = Serial.read();

    // the order of these IF clauses is significant

    if (x == endMarker) {
      readInProgress = false;
      newDataFromPC = true;
      inputBuffer[bytesRecvd] = 0;
      parseData();
    }

    if(readInProgress) {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker) { 
      bytesRecvd = 0; 
      readInProgress = true;
    }
  }
}

void parseData() {

  // split the data into its parts

  char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(inputBuffer,",");      // get the first part - the string
  strcpy(messageFromPC, strtokIndx);

  strtokIndx = strtok(NULL,",");
  numberOfArg = atoi(strtokIndx);

  for(int i=0; i<numberOfArg; i++){
    strtokIndx = strtok(NULL,",");
    arguments[i] = atoi(strtokIndx);     // convert this part to an integer
  }
}

void callFunction(){
  if (strcmp(messageFromPC, "setBlinds") == 0){
    updateSetpoint(arguments[0]);
    setBlinds();
  }

  if (strcmp(messageFromPC, "getBlinds") == 0){
    replyToPC();
  } 
}

void updateSetpoint(int incomingSetpoint){
  if(incomingSetpoint >= 0 and incomingSetpoint <= 1023 and newDataFromPC){
    setpoint = sin(3.14*incomingSetpoint/1900)*incomingSetpoint;//(square(-incomingSetpoint)+15)/1023; 
  }
}

void setBlinds(){
  while(feedbackPot < setpoint-tolerance || feedbackPot > setpoint+tolerance){
    feedbackPot = analogRead(A0);
    if(feedbackPot < setpoint-tolerance){
      digitalWrite(plus, HIGH);
      digitalWrite(minus, LOW);
    }

    else if (feedbackPot > setpoint+tolerance){
      digitalWrite(plus, LOW);
      digitalWrite(minus, HIGH);
    }
  }
  
  digitalWrite(plus, LOW);
  digitalWrite(minus, LOW);
}

void replyToPC() {
  feedbackPot = analogRead(A0);
  
  if (newDataFromPC) {
    newDataFromPC = false;
    Serial.print("<setpoint ");
    Serial.print(setpoint);
    Serial.print(" feedbackPot ");
    Serial.print(feedbackPot);
    Serial.println(">");
  }
}





