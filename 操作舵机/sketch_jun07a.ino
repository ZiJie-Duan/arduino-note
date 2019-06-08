#include <Servo.h>  

#define PIN_SERVO 5

Servo myservo;  
void setup()  
{  
  myservo.attach(PIN_SERVO);  
}  
void loop()  
{  
  myservo.write(20);  
  delay(50);  
  myservo.write(80);  
  delay(50);  

} 
