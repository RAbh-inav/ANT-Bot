#include<ESP32Servo.h>//ESP32Servo header file is included

Servo myservo;//Servo object is created
int pos = 0; //Variable to store position of servo motor  
const int servo= 12;//Variable to store pin at which servo motor is connected to ESP32 camera module
int i;//Iteration variable for executing the instructions given
const int motor=2;//Variable to store pin at which motor is connected to ESP32 camera module
//Instructions for direction in which the vehicle should move and when it should stop after completing the task is in obtained from the python code

char instructions[]={'l', 'l', 'r', 'l', 'r', 'l', 'r', 'r', 'r', 'r', 'l', 'l', 'l', 'r', 'l', 'l', 'r', 'r', 'l', 'l', 'r', 'r', 'r', 'l', 'l', 'l','X'};
//Angle needed to be turned obtained from the python code
int angle[]={62, 10, 14, 24, 28, 27, 20, 70, 1, 60, 12, 89, 2, 1, 36, 13, 77, 8, 90, 90, 0, 31, 37, 4, 36, 27};
//Distance to be covered after each instruction in cm
float distance[]=	    {0.77,1.66,0.55,0.86,0.62,1.38,0.86,3.59,4.25,0.55,0.57,0.55,0.60,0.85, 0.82,4.48,2.08,4.64,0.52,0.84,5.22,0.55,0.46,0.87,0.82,15.98};

// Function to be used when the vehicle is turning right
void right()
{
  digitalWrite(motor,LOW);//motor is turned LOW
  int b= angle[i]+90;// As 90 degrees is considered straight, angle needed to be turned towards right will be 90 plus the angle given
  for( pos=90; pos<b;pos++)// goes from 90 degrees to b degrees which is more than 90 in incremental steps of 1 degree
  {
  myservo.write(pos);//Position of servo motor is written to pos whose value is upgraded in every iteration
  Serial.println(pos);//Current position of servo motor is displayed on serial monitor followed by a new line  
  delay(30);//Delay of 30 ms is given for servo to reach the position given and maintain it
  }
}


//Function to be used when the vehicle is turning left
void left()
 {
  digitalWrite(motor,LOW);//motor is turned LOW
  int a= 90-angle[i];// As 90 degrees is considered straight, angle needed to be turned towards right will be 90 plus the angle given
  for(pos=90;pos>=a;pos--)// goes from 90 degrees to a degrees which is less than 90 degrees in decremental steps of 1 degree
  {
  myservo.write(pos);//Position of servo motor is written to pos whose value is upgraded in every iteration
  Serial.println(pos); //Current position of servo motor is displayed on serial monitor followed by a new line  
  delay(30);//Delay of 30 ms is given for servo to reach the position given and maintain it            
  }
}


//Function to be used when the vehicle is moving forward
void straight(float d1)
{
  digitalWrite(motor,HIGH);//motor is turned HIGH
  myservo.write(90);//Position of servo motor is written to 90 degrees which is the straight position
  long t= d1/0.03401;//Time for which vehicle must go straight is calculated by t= d1/(speed of motor(1.667rpms)*distance covered in 1 rotation by wheel(20.41cm)) 
  delay(t);//Delay of t ms is given to reach and maintain the position of servo and state of motor for the distance given
}

//Setup is used for initialization which is executed only once
void setup()//
{
  // allocation of all the timers
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
  pinMode(motor,OUTPUT);//Assigning motor pin to OUTPUT
  myservo.setPeriodHertz(50);//Servo used has frequency of 50 Hz, so the object myservo is set to the same value
  myservo.attach(servo, 544, 2400); //servo pin is attached to myservo with minimum and maximum pulse width of 544us and 2400us corresponding to 0 degree and 180 degrees respectively
  Serial.begin(115200);//Serial monitor is initialised at a baud rate of 115200 bps
}

//Loop will be executed continuously
void loop()
{
Serial.println("Started");//Print in the serial monitor that program has "Started" followed by a new line
for (i =0; i<27; i++)//Loop to execute the instructions given
{
    if(instructions[i]=='r')//If the instruction is 'r' following statements are executed
   {
   right();//right function is called
   Serial.println("Right");//Print in the serial monitor that instruction has been given to turn "Right" followed by a new line
   straight(distance[i]);//straight function is called which has distance as parameter
   Serial.println("Forward");//Print in the serial monitor that instruction has been given to go "Forward" followed by a new line
   }
  if(instructions[i]=='l')//If the instruction is 'l' following statements are executed
   {
   left();//left function is called
   Serial.println("Left");//Print in the serial monitor that instruction has been given to turn "Left" followed by a new line
   straight(distance[i]);//straight function is called which has distance as parameter
   Serial.println("Forward");//Print in the serial monitor that instruction has been given to go "Forward" followed by a new line
   }
   if(instructions[i]=='X')//If the instruction is 'X' following statements are executed
   {
 
  Serial.println("End");//Print in the serial monitor that instruction has been given to "End" the execution followed by a new line
   digitalWrite(motor,LOW);//motor is turned LOW
   myservo.write(90);//Position of servo motor is written to 90 degrees which is the straight position
   delay(100);//Delay of 100 ms is given to reach and maintain the position of servo and state of motor
   while(1)//Infinite loop to make it a single execution program 
   {
    Serial.println("Execution over");//Print in the serial monitor that execution is over
   }
   }
}
}
