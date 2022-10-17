#include <Wire.h>

void oled_write_data(int data);
void oled_write_command(int data);
void send_data(int data);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin();

  Serial.println("IIC OLED INIT");

  //Wire.write(0b00101000);
  //delay(200);
  //Wire.write(0b00101100);
  //delay(200);
  //Wire.write(0b10001000);
  //delay(200);
  //Wire.write(0b10001100);
  //delay(200);
  oled_write_command(0x30);
  delay(200);
  oled_write_command(0x30);
  delay(200);
  oled_write_command(0x30);
  delay(200);
  oled_write_command(0x20);
  delay(200);
  oled_write_command(0x80);
  delay(200);
  oled_write_command(1);//清屏
  delay(1200);
  Serial.println("IIC OLED INIT FINISH");

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Start IIC");

  //清除光标
  //oled_write_command(0xf); //显示光标
  oled_write_command(0x80); //变更光标位置
  //oled_write_command(0xf); //显示光标
  oled_write_command(0xf); //显示光标
  //test_o();
  //test_o2();
  oled_write_data('A');


  Serial.println("FINISH A LOOP");
  delay(5000);
}


void send_data(int data){
  delay(500);
  Wire.beginTransmission(0x27);
  Wire.write(data);
  Wire.endTransmission();
  delay(500);
  Wire.beginTransmission(0x27);
  Wire.write(data|0b00000100);
  Wire.endTransmission();
  delay(500);
  Wire.beginTransmission(0x27);
  Wire.write(data&0b11111011);
  Wire.endTransmission();
  delay(500);
}

void send_data(int data){
  delay(500);
  Wire.beginTransmission(0x27);
  Wire.write(data);
  Wire.endTransmission();
  delay(500);
  Wire.beginTransmission(0x27);
  Wire.write(data|0b00000100);
  Wire.endTransmission();
  delay(500);
  Wire.beginTransmission(0x27);
  Wire.write(data&0b11111011);
  Wire.endTransmission();
  delay(500);
}


void oled_write_data(int data){
  int data1 = data&0b11110000;
  data1 = data>>4;
  int data2 = data&0b00001111;
  data1 = (data1*16)|0b00001001;
  data2 = (data2*16)|0b00001001;
  Wire.beginTransmission(0x27);
  Wire.write(data1);
  delay(50);
  Wire.write(data1|0b00000100);
  delay(50);
  Wire.write(data2);
  delay(50);
  Wire.write(data2|0b00000100);
  delay(50);
  Wire.endTransmission();
}

void oled_write_command(int data){
  int data1 = data&0b11110000;
  data1 = data>>4;
  int data2 = data&0b00001111;
  data1 = (data1*16)|0b00001000;
  data2 = (data2*16)|0b00001000;
  send_data(data1);
  send_data(data2);
}



