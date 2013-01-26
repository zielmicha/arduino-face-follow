#include <Servo.h>

Servo servo_dol;
Servo servo_gora;
int pos_dol = 90;
int pos_gora = 30;

void setup()
{
  servo_dol.attach(8);
  servo_gora.attach(9);
  Serial.begin (9600);
  pinMode (13, OUTPUT);
  
    servo_dol.write(pos_dol);
    servo_gora.write(pos_gora);
}

int mkp(char s) {
   switch(s) {
      case '+': return +1;
      case '-': return -1;
      case '0': return 0;
   } 
   return 0;
}

void loop()
{
  if (Serial.available () >= 2) {
    digitalWrite (13, 1);
    int y = mkp(Serial.read());
    
    int x = mkp(Serial.read());
    //    Serial

    servo_dol.write(pos_dol += 7 * x);
    servo_gora.write(pos_gora += 4 * y);
    if(pos_dol < 0) pos_dol = 0;
    if(pos_dol >= 180) pos_dol = 179;
    if(pos_gora < 0) pos_gora = 0;
    if(pos_gora >= 180) pos_gora = 179;
    Serial.print ("odebralem");
    Serial.print (pos_dol);
    Serial.print (" ");
    Serial.println (pos_gora);

    delay(100);
        digitalWrite (13, 0);

  }
}
