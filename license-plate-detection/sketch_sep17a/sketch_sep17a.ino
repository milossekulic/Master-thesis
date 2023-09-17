#include <Servo.h>
const unsigned int TRIG_PIN=12;
const unsigned int ECHO_PIN=13;
Servo myservo;  // create servo object to control a servo


int val;    // variable to read the value from the analog pin
int x;

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  Serial.begin(9600);
 Serial.setTimeout(1)  ;
}

void loop() {   
  // for (int i = 0; i <= 180; i=i+10) {
  //   myservo.write(i); 
  //   delay(100);
    
  // }
//  while (!Serial.available());
 x = Serial.readString().toInt();

myservo.write(0);
     digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

 const unsigned long duration= pulseIn(ECHO_PIN, HIGH);

 int distance= duration/29/2;

//Serial.println(distance);
if (distance < 10)
{
  Serial.println("True");
  while (Serial.available() == 0) {
  }
 int response = Serial.parseInt();
 if (response == 1){
    myservo.write(90);
   delay(20000);
 }

  }

 

}  
//  delay(100);
//}  // scale it to use it with the servo (value between 0 and 180)
                  // sets the servo position according to the scaled value
                          // waits for the servo to get there


