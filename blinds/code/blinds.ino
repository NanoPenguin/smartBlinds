#include <math.h>

/*---GLOBAL VARIABELS---*/
const byte buffSize = 40;
char inputBuffer[buffSize];
char messageFromPC[buffSize] = {0};
const char startMarker = '<';
const char endMarker = '>';
unsigned long arguments[5];
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;
int tolerance = 5;
int plus = 3;
int minus = 2;
unsigned long setpoint = 0;
int feedbackPot;


/*---FUNCTION DECLARATION---*/
void callFunction();
void clearMessage();
void getDataFromPC();
void parseData();
void replyToPC();
int readPot();
void setBlinds(int, unsigned long);
unsigned long updateSetpoint(unsigned long);

void setup() {
  pinMode(plus, OUTPUT); //Nedre på motorn
  pinMode(minus, OUTPUT); // Övre på motorn
  feedbackPot = readPot();
  setpoint = feedbackPot;
  Serial.begin(9600);
  Serial.println("<Arduino is ready>");
}

void loop() {
  // put your main code here, to run repeatedly:
  getDataFromPC();
  callFunction();
}

void getDataFromPC() {
  // receive data from PC and save it into inputBuffer

  if (Serial.available() > 0) {

    char _x = Serial.read();

    // the order of these IF clauses is significant

    if (_x == endMarker) {
      readInProgress = false;
      newDataFromPC = true;
      inputBuffer[bytesRecvd] = 0;
      parseData();
    }

    if (readInProgress) {
      inputBuffer[bytesRecvd] = _x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (_x == startMarker) {
      bytesRecvd = 0;
      readInProgress = true;
    }
  }
}

void parseData() {
  // split the data into its parts
  char * _strtokIndx; // this is used by strtok() as an index
  int _numberOfArg = 0;

  _strtokIndx = strtok(inputBuffer, ",");     // get the first part - the string
  strcpy(messageFromPC, _strtokIndx);

  _strtokIndx = strtok(NULL, ",");
  _numberOfArg = atoi(_strtokIndx);

  for (int i = 0; i < _numberOfArg; i++) {
    _strtokIndx = strtok(NULL, ",");
    arguments[i] = atol(_strtokIndx);     // convert this part to an long
  }
}

void callFunction() {
  if (strcmp(messageFromPC, "setBlinds") == 0) {
    setBlinds(updateSetpoint(arguments[0]), arguments[1]);
    clearMessage();
  }

  if (strcmp(messageFromPC, "getBlinds") == 0) {
    replyToPC();
    clearMessage();
  }
}

unsigned long updateSetpoint(unsigned long incomingSetpoint) {
  unsigned long _setpoint = 0;
  if (incomingSetpoint >= 0 and incomingSetpoint <= 1023 and newDataFromPC) {
    _setpoint = sin(3.14 * incomingSetpoint / 1900) * incomingSetpoint; //= incomingSetpoint;
  }
  return _setpoint;
}

int readPot() {
  /*To be transformed*/
  int _feedbackPot = analogRead(A0);
  return _feedbackPot;
}

void setBlinds(int setpoint, unsigned long time_) {
  Serial.println("setBlinds()");
  int _startPoint = readPot();
  int _steps = 20;
  unsigned long _delayTime = time_ / abs((_startPoint - setpoint) / 20);
  unsigned long _curMillis = millis();
  unsigned long _startTime = _curMillis;
  
  if (time_ == 0) {
    while (feedbackPot < setpoint - tolerance || feedbackPot > setpoint + tolerance) {
      feedbackPot = readPot();
      if (feedbackPot < setpoint - tolerance) {
        digitalWrite(plus, HIGH);
        digitalWrite(minus, LOW);
      }

      else if (feedbackPot > setpoint + tolerance) {
        digitalWrite(plus, LOW);
        digitalWrite(minus, HIGH);
      }

      if (Serial.read() == '#') {
        break;
      }
    }
    digitalWrite(plus, LOW);
    digitalWrite(minus, LOW);
  }

  else if (time_ > 0) { //GÅR EJ GENOM TRANSFORM!!!
    bool loopBreaker = false;
    while (_curMillis - _startTime <= time_ && loopBreaker == false) {
      if (_startPoint < setpoint) {
        _startPoint = _startPoint + _steps;
      }

      if (_startPoint > setpoint) {
        _startPoint = _startPoint - _steps;
      }

      while (feedbackPot < sin(3.14 * _startPoint / 1900) * _startPoint - tolerance || feedbackPot > sin(3.14 * _startPoint / 1900) * _startPoint + tolerance) {
        feedbackPot = readPot();
        if (feedbackPot < sin(3.14 * _startPoint / 1900) * _startPoint - tolerance) {
          digitalWrite(plus, HIGH);
          digitalWrite(minus, LOW);
        }

        else if (feedbackPot > sin(3.14 * _startPoint / 1900) * _startPoint + tolerance) {
          digitalWrite(plus, LOW);
          digitalWrite(minus, HIGH);
        }

        if (Serial.read() == '#') {
          loopBreaker = true;
          break;
        }
      }
      digitalWrite(plus, LOW);
      digitalWrite(minus, LOW);

      delay(_delayTime);
      _curMillis = millis();
    }

  }

}

void replyToPC() {
  int _feedbackPot = readPot();

  if (newDataFromPC) {
    newDataFromPC = false;
    Serial.print("<setpoint ");
    Serial.print(setpoint);
    Serial.print(" feedbackPot ");
    Serial.print(_feedbackPot);
    Serial.println(">");
  }
}

void clearMessage() {
  for (int i = 0; i < sizeof(messageFromPC); i++) {
    messageFromPC[i] = (char)0;
  }
}
