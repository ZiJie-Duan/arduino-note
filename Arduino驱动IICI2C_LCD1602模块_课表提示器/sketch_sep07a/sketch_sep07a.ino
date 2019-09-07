#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <EEPROM.h>

LiquidCrystal_I2C lcd(0x27,16,2); // set the LCD address to 0x27 for a 16 chars and 2 line display

int zc_day = 1;
int zc_class = 1;

 int red = 5; // 按键的管脚定义
 int green = 3;  // 按键的管脚定义


void setup()
{
Serial.begin(9600);
pinMode(red, INPUT_PULLUP); //设置按键管脚上拉输入模式
pinMode(green, INPUT_PULLUP); //设置按键管脚上拉输入模式
lcd.init(); 
lcd.backlight();

}


int get_day(){
  
  int js = 0;
  lcd.clear();
  lcd.print("day");
  lcd.print(js);
  
  while(true){
  int ztm = digitalRead(green);
  int ztm2 = digitalRead(red);
  if (ztm == HIGH){
    delay(500);
    int ztm = digitalRead(green);
    if (ztm == HIGH){
      js = js + 1;
      lcd.clear();
      lcd.print("day");
      lcd.print(js);
    }
  }

  if (ztm2 == HIGH){
    delay(600);
    int ztm2 = digitalRead(red);
    if (ztm2 == HIGH){
      break;
    }
  }
  }
  return js;
}


int get_class(){
  
  int js = 0;
  lcd.clear();
  lcd.print("class");
  lcd.print(js);
  
  while(true){
    
  int ztm = digitalRead(green);
  int ztm2 = digitalRead(red);
  if (ztm == HIGH){
    delay(500);
    int ztm = digitalRead(green);
    if (ztm == HIGH){
      js = js + 1;
      lcd.clear();
      lcd.print("class");
      lcd.print(js);
    }
  }

  if (ztm2 == HIGH){
    delay(600);
    int ztm2 = digitalRead(red);
    if (ztm2 = HIGH){
      break;
    }
  }
  }
  return js;
}


int read_zc(){
  zc_day = EEPROM.read(0);
  zc_class = EEPROM.read(1);
  
}

int write_zc(){
  EEPROM.write(0, zc_day);
  EEPROM.write(1, zc_class);
  
}



void flash(){
  lcd.clear();
  lcd.print("seeting time");
  delay(500);
  lcd.clear();
  delay(500);
  lcd.clear();
  lcd.print("seeting time");
  delay(500);
  lcd.clear();
  delay(500);
  lcd.clear();
  lcd.print("seeting time");
  delay(500);
  lcd.clear();
  
}



void loop()
{
lcd.print("waite...");

int ztm = digitalRead(red);
if (ztm == HIGH){
  delay(500);
  int ztm = digitalRead(red);
  if (ztm == HIGH){
    read_zc();
    flash();
    int ztm = digitalRead(red);
    if (ztm == HIGH){
      zc_day = get_day();
      lcd.clear();
      delay(500);
      zc_class = get_class();
      lcd.clear();
      delay(500);
      
      print_time_table(zc_day,zc_class);
      delay(4000);
      write_zc();
    }
    
    lcd.print("day ");
    lcd.print(zc_day);
    lcd.setCursor(0,1); //newline
    lcd.print("class ");
    lcd.print(zc_class);
    delay(2000);
    
    int ztm2 = digitalRead(red);
    
    if (ztm2 == HIGH){
      lcd.clear();
      delay(500);
      int ztm2 = digitalRead(red);
      if (ztm2 == HIGH){
        zc_class = zc_class + 1;
      }
      lcd.print("day ");
      lcd.print(zc_day);
      lcd.setCursor(0,1); //newline
      lcd.print("class ");
      lcd.print(zc_class);
      delay(1000);
    }
    print_time_table(zc_day,zc_class);
    delay(5000);
    write_zc(); 
    }
    }
  }














void print_time_table(int day,int classs){
  if (day == 1){
    if (classs == 1){
     lcd.clear();
     lcd.print("EALF Charles");
     lcd.setCursor(0,1); //newline
     lcd.print("212");     
    }
    if (classs == 2){
     lcd.clear();
     lcd.print("ACCA Daniel");
     lcd.setCursor(0,1); //newline
     lcd.print("222");  
    }
    if (classs == 3){
     lcd.clear();
     lcd.print("SCIE Alice");
     lcd.setCursor(0,1); //newline
     lcd.print("316"); 
    }
    if (classs == 4){
     lcd.clear();
     lcd.print("MAB Zhao Iris");
     lcd.setCursor(0,1); //newline
     lcd.print("114"); 
    }
    if (classs == 5){
     lcd.clear();
     lcd.print("MAB Zhao Iris");
     lcd.setCursor(0,1); //newline
     lcd.print("114"); 
    }
    if (classs == 6){
     lcd.clear();
     lcd.print("ESLF Cooke");
     lcd.setCursor(0,1); //newline
     lcd.print("214"); 
    }
    if (classs == 7){
     lcd.clear();
     lcd.print("CFLA Wu Sisi");
     lcd.setCursor(0,1); //newline
     lcd.print("221"); 
    }
    if (classs == 8){
     lcd.clear();
     lcd.print("NO CLASS");
     lcd.setCursor(0,1); //newline
     lcd.print("000"); 
    }
  }
  
  if (day == 2){
    if (classs == 1){
     lcd.clear();
     lcd.print("ESLF Cooke");
     lcd.setCursor(0,1); //newline
     lcd.print("214");     
    }
    if (classs == 2){
     lcd.clear();
     lcd.print("EALF Charles");
     lcd.setCursor(0,1); //newline
     lcd.print("212");  
    }
    if (classs == 3){
     lcd.clear();
     lcd.print("ESKA Linda");
     lcd.setCursor(0,1); //newline
     lcd.print("211"); 
    }
    if (classs == 4){
     lcd.clear();
     lcd.print("CFLA Wu Sisi");
     lcd.setCursor(0,1); //newline
     lcd.print("221"); 
    }
    if (classs == 5){
     lcd.clear();
     lcd.print("CFLA Wu Sisi");
     lcd.setCursor(0,1); //newline
     lcd.print("221"); 
    }
    if (classs == 6){
     lcd.clear();
     lcd.print("SCIE Alice");
     lcd.setCursor(0,1); //newline
     lcd.print("316"); 
    }
    if (classs == 7){
     lcd.clear();
     lcd.print("ACCA Daniel");
     lcd.setCursor(0,1); //newline
     lcd.print("222"); 
    }
    if (classs == 8){
     lcd.clear();
     lcd.print("NO CLASS");
     lcd.setCursor(0,1); //newline
     lcd.print("000"); 
    }
  }
  
  if (day == 3){
    if (classs == 1){
     lcd.clear();
     lcd.print("MAB Zhao Iris");
     lcd.setCursor(0,1); //newline
     lcd.print("114");     
    }
    if (classs == 2){
     lcd.clear();
     lcd.print("ESLF Cooke");
     lcd.setCursor(0,1); //newline
     lcd.print("214");  
    }
    if (classs == 3){
     lcd.clear();
     lcd.print("EALF Charles");
     lcd.setCursor(0,1); //newline
     lcd.print("212"); 
    }
    if (classs == 4){
     lcd.clear();
     lcd.print("ACCA Daniel");
     lcd.setCursor(0,1); //newline
     lcd.print("222"); 
    }
    if (classs == 5){
     lcd.clear();
     lcd.print("ACCA Daniel");
     lcd.setCursor(0,1); //newline
     lcd.print("222"); 
    }
    if (classs == 6){
     lcd.clear();
     lcd.print("ESKA Linda");
     lcd.setCursor(0,1); //newline
     lcd.print("211"); 
    }
    if (classs == 7){
     lcd.clear();
     lcd.print("NO CLASS");
     lcd.setCursor(0,1); //newline
     lcd.print("000"); 
    }
    if (classs == 8){
     lcd.clear();
     lcd.print("NO CLASS");
     lcd.setCursor(0,1); //newline
     lcd.print("000"); 
    }
    
  }
  if (day == 4){
    if (classs == 1){
     lcd.clear();
     lcd.print("ESKA Linda");
     lcd.setCursor(0,1); //newline
     lcd.print("211");     
    }
    if (classs == 2){
     lcd.clear();
     lcd.print("CFLA Wu Sisi");
     lcd.setCursor(0,1); //newline
     lcd.print("221");  
    }
    if (classs == 3){
     lcd.clear();
     lcd.print("MAB Zhao Iris");
     lcd.setCursor(0,1); //newline
     lcd.print("114"); 
    }
    if (classs == 4){
     lcd.clear();
     lcd.print("PEE Sun Jack");
     lcd.setCursor(0,1); //newline
     lcd.print("gym1"); 
    }
    if (classs == 5){
     lcd.clear();
     lcd.print("PEE Sun Jack");
     lcd.setCursor(0,1); //newline
     lcd.print("gym1"); 
    }
    if (classs == 6){
     lcd.clear();
     lcd.print("EALF Charles");
     lcd.setCursor(0,1); //newline
     lcd.print("212"); 
    }
    if (classs == 7){
     lcd.clear();
     lcd.print("EALF Charles");
     lcd.setCursor(0,1); //newline
     lcd.print("212"); 
    }
    if (classs == 8){
     lcd.clear();
     lcd.print("NO CLASS");
     lcd.setCursor(0,1); //newline
     lcd.print("000"); 
    }
    
  }
  if (day == 5){
    if (classs == 1){
     lcd.clear();
     lcd.print("ACCA Daniel");
     lcd.setCursor(0,1); //newline
     lcd.print("222");     
    }
    if (classs == 2){
     lcd.clear();
     lcd.print("SCIE Alice");
     lcd.setCursor(0,1); //newline
     lcd.print("316");  
    }
    if (classs == 3){
     lcd.clear();
     lcd.print("CFLA Wu Sisi");
     lcd.setCursor(0,1); //newline
     lcd.print("221"); 
    }
    if (classs == 4){
     lcd.clear();
     lcd.print("ESLF Cooke");
     lcd.setCursor(0,1); //newline
     lcd.print("214"); 
    }
    if (classs == 5){
     lcd.clear();
     lcd.print("ESLF Cooke");
     lcd.setCursor(0,1); //newline
     lcd.print("214"); 
    }
    if (classs == 6){
     lcd.clear();
     lcd.print("MAB Zhao Iris");
     lcd.setCursor(0,1); //newline
     lcd.print("114"); 
    }
    if (classs == 7){
     lcd.clear();
     lcd.print("NO CLASS");
     lcd.setCursor(0,1); //newline
     lcd.print("000"); 
    }
    if (classs == 8){
     lcd.clear();
     lcd.print("NO CLASS");
     lcd.setCursor(0,1); //newline
     lcd.print("000"); 
    }
    
  }
}
