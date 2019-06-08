
 int keylist[4];
 int bot = 4; // 按键的管脚定义
 int red = 6;  // LED灯管脚定义
 int green = 5;  // LED灯管脚定义
 int blue = 3;  // LED灯管脚定义

 
 void setup() {
   Serial.begin(9600);
   pinMode(red, OUTPUT);  //设置LED管脚输出模式
   pinMode(green, OUTPUT);  //设置LED管脚输出模式
   pinMode(bot, INPUT_PULLUP); //设置按键管脚上拉输入模式
 }


void flash(int z ,int t){
  //让led闪烁的函数
  if (z == 3){
    digitalWrite(green,HIGH);
    delay(t);
    digitalWrite(green,LOW);
  }else{
    if (z==1){
    digitalWrite(red,HIGH);
    delay(t);
    digitalWrite(red,LOW);
  }else{
    digitalWrite(blue,HIGH);
    delay(t);
    digitalWrite(blue,LOW);
  }
  

}}

bool start() {
  int ztm = digitalRead(bot);
  bool fhz = false;
  
  if (ztm == HIGH){
    delay(500);
    //防手抖
    int ztm = digitalRead(bot);
    if (ztm == HIGH){
      fhz = true;
    }else {
      fhz = false;
    }
  
}
  return fhz;
}


int getkeyone(){
  //获取个位数的key
  int js =0;
  while (true){
   
    int ztm = digitalRead(bot);

    if (ztm == HIGH){
      delay(50);
      int ztm = digitalRead(bot);
      if (ztm == HIGH){
        flash(1,1000);
        int ztm = digitalRead(bot);
        if (ztm==HIGH){
          delay(1000);
          flash(2,200);
          break;
        }else{
          js = js + 1;
        }
      }
    }
    
}
  return js;
}


int getkey(){
  //结合key为列表，列表放置在全局变量中
  int js = 0;
  while (true){
    
    int z = getkeyone();
    keylist[js] = z;
    js = js+1;
    if (js > 3){
      break;
    }
      
  }
}


bool yz_key(){
  //验证key是否正确的函数
  bool zt = true;
  int password[4]{2,3,3,2};
  for (int i=0;i<4;i++){
    if (zt){
      
      if (keylist[i] == password[i]){
        zt = true;
      }else{
        zt = false;
      }
      
   }else{
    break;
   }

  }
 return zt;
     
}


 void loop() {
   bool zt = start();
   if (zt == true){
     Serial.println("strat get key");
     flash(1,2000);
     getkey();
     
     int js = 0;
     for (;js<4;js = js + 1){
      Serial.println(keylist[js]);
     }
     
     bool zt = yz_key();
     if (zt){
        flash(3,2000);
     }else{
        flash(1,2000);
     }
     Serial.println("while over");
     
     
    
   }
 
 for (int i = 0; i < 4; i++){
  keylist[i] = '\0' ;  
 
 }
 }











 
