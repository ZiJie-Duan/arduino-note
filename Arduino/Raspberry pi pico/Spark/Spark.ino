// 在树莓派上运行OLED1.3 首先需要注意修改 pico内部的iic引脚映射，接着修改Adafruit_SSD1306.h文件，移除掉提示不存在的库文件
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <string.h>

#define SCREEN_WIDTH 128     // OLED display width, in pixels
#define SCREEN_HEIGHT 64     // OLED display height, in pixels
#define OLED_RESET -1        // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C  ///< See datasheet for Address; 0x3C
#define SSEQ_TIME_INDEX 13 //screen_sequence pixel life length
#define SSEQ_BASE_UNIT 3 //screen_sequence base unit
#define SSEQ_PIXS_NUM 3730 //screen_sequence max number of pixel
// SSEQ_PIXS_NUM, the first location is a arr [x,0,0], x direct how many data in the SSEQ_PIXS_NUM
#define WHITE SSD1306_WHITE
#define BLACK SSD1306_BLACK

#define SMALLEST_SPARK 3
#define SPARK_TYPE 5
#define BIGEST_SPARK 8
#define SMALLEST_SPARK_LIFE 2
#define BIGEST_SPARK_LIFE 8

uint8_t Screen_Sequence[SSEQ_TIME_INDEX+1][SSEQ_PIXS_NUM][SSEQ_BASE_UNIT];
uint8_t Screen_Time_Index = 0;
uint8_t g_x_axis = 0;
uint8_t g_y_axis = 0;
uint8_t g_spark_type = 0;
uint8_t g_spark_size = 0;
int cont = 0;

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
void print_pixel();
void draw_a_line(uint8_t x_axis, uint8_t y_axis, uint8_t direction, uint8_t number, uint8_t delay = 1);
void draw_a_point(uint8_t x_axis, uint8_t y_axis, uint8_t delay = 1);
uint8_t boundary_check(uint8_t x_axis, uint8_t y_axis);
void ordered_insert(uint8_t screen_time_index, uint8_t *pix_data);
uint8_t add_screen_time_index(uint8_t screen_time_index);
void clean_screen_sequence();
void spark_maker(uint8_t x_axis, uint8_t y_axis, uint8_t type, uint8_t size);
void send_signal();

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS);
  display.clearDisplay();
  display.setTextSize(1);               // Normal 1:1 pixel scale
  display.setTextColor(WHITE);  // Draw white text
}

void loop() {
  // put your main code here, to run repeatedly:
  g_x_axis = random(8, SCREEN_WIDTH-7);
  g_y_axis = random(8, SCREEN_HEIGHT-7);
  g_spark_type = random(1, SPARK_TYPE+1);
  g_spark_size = random(SMALLEST_SPARK, BIGEST_SPARK+1);
  spark_maker(g_x_axis,g_y_axis,g_spark_type,g_spark_size);
  Serial.println(" I am not die here maker");
  print_pixel();
  Serial.println(" I am not die here print");
  send_signal();
}

void spark_maker(uint8_t x_axis, uint8_t y_axis, uint8_t type, uint8_t size){
  switch (type)
  {
  case 1:
    draw_a_point(x_axis,y_axis,2);
    draw_a_line(x_axis,y_axis,1,size,2);
    draw_a_line(x_axis,y_axis,3,size,2);
    draw_a_line(x_axis,y_axis,5,size,2);
    draw_a_line(x_axis,y_axis,7,size,2);
    break;
  
  case 2:
    draw_a_point(x_axis,y_axis,2);
    draw_a_line(x_axis,y_axis,2,size,2);
    draw_a_line(x_axis,y_axis,4,size,2);
    draw_a_line(x_axis,y_axis,6,size,2);
    draw_a_line(x_axis,y_axis,8,size,2);
    break;
  
  case 3:
    draw_a_point(x_axis,y_axis,2);
    draw_a_line(x_axis,y_axis,1,size,2);
    draw_a_line(x_axis,y_axis,2,size,2);
    draw_a_line(x_axis,y_axis,3,size,2);
    draw_a_line(x_axis,y_axis,4,size,2);
    draw_a_line(x_axis,y_axis,5,size,2);
    draw_a_line(x_axis,y_axis,6,size,2);
    draw_a_line(x_axis,y_axis,7,size,2);
    draw_a_line(x_axis,y_axis,8,size,2);
    break;
  
  case 4:
    draw_a_point(x_axis,y_axis,2);
    draw_a_line(x_axis,y_axis,1,size,2);
    draw_a_line(x_axis,y_axis,1,size,2);
    break;

  default:
    int i = random(1, 9);
    for (int ii=0; ii<i; ii++){
      uint8_t dir = random(1,9);
      uint8_t life = random(SMALLEST_SPARK_LIFE,BIGEST_SPARK_LIFE+1);
      draw_a_line(x_axis,y_axis,dir,size,life);
    }
    break;
  }
}

uint8_t boundary_check(uint8_t x_axis, uint8_t y_axis){
  if ((x_axis > SCREEN_WIDTH) && (x_axis < 0) &&
    (y_axis > SCREEN_HEIGHT) && (y_axis < 0)) return 0;
  return 1;
}

void draw_a_line(uint8_t x_axis, uint8_t y_axis, uint8_t direction, uint8_t number, uint8_t delay)
{ 
  uint8_t sseq_data[] = {0,0,0}; //init
  for (int i=0; i<number; i++){
    switch (direction)
    {
    case 1:
      y_axis -= 1;
      break;
    case 2:
      x_axis += 1;
      y_axis -= 1;
      break;
    case 3:
      x_axis += 1;
      break;
    case 4:
      x_axis += 1;
      y_axis += 1;
      break;
    case 5:
      y_axis += 1;
      break;
    case 6:
      x_axis -= 1;
      y_axis += 1;
      break;
    case 7:
      x_axis -= 1;
      break;
    case 8:
      x_axis -= 1;
      y_axis -= 1;
      break;
    }
    if (boundary_check(x_axis,y_axis)){
      sseq_data[0] = x_axis;
      sseq_data[1] = y_axis;
      sseq_data[2] = 1;
      ordered_insert(
                  add_screen_time_index(Screen_Time_Index+i),
                  sseq_data);
      sseq_data[2] = 0;
      ordered_insert(
                  add_screen_time_index(Screen_Time_Index+delay+i),
                  sseq_data);
    }
  }
}

void clean_screen_sequence(){
  memset(&Screen_Sequence[Screen_Time_Index],0,sizeof Screen_Sequence[Screen_Time_Index]);
}

void ordered_insert(uint8_t screen_time_index, uint8_t *pix_data)
{ 
  uint8_t data_index = Screen_Sequence[screen_time_index][0][0];
  Screen_Sequence[screen_time_index][data_index+1][0] = pix_data[0];
  Screen_Sequence[screen_time_index][data_index+1][1] = pix_data[1];
  Screen_Sequence[screen_time_index][data_index+1][2] = pix_data[2];
  Screen_Sequence[screen_time_index][0][0] += 1;
}

uint8_t add_screen_time_index(uint8_t screen_time_index){
  if (screen_time_index > SSEQ_TIME_INDEX){ 
    //here screen_time_index is a index, so the max value of it is less than SSEQ_TIME_INDEX
    return screen_time_index - SSEQ_TIME_INDEX;
  } else {
    return screen_time_index;
  }
}

void print_pixel(){
  Serial.println(Screen_Time_Index);
  uint8_t data_index = Screen_Sequence[Screen_Time_Index][0][0];
  Serial.println(" I am not die here print -1");
  for (int i=1; i<=data_index; i++){
    Serial.println(" I am not die here print -2");
    if (Screen_Sequence[Screen_Time_Index][i][2]){
      display.drawPixel(
      Screen_Sequence[Screen_Time_Index][i][0],
      Screen_Sequence[Screen_Time_Index][i][1],
      WHITE);
    } else {
      display.drawPixel(
      Screen_Sequence[Screen_Time_Index][i][0],
      Screen_Sequence[Screen_Time_Index][i][1],
      BLACK);
    }
  }
  Serial.println(" I am not die here print 1");
  display.display();
  Serial.println(" I am not die here print 2");
  clean_screen_sequence();
  Serial.println(" I am not die here print 3");
  if (Screen_Time_Index >= SSEQ_TIME_INDEX){ //these code use the Screen_Time_Index value First
    Screen_Time_Index = 0;
  } else {
    Screen_Time_Index += 1;
  }
  Serial.println(" I am not die here print 4");
}

void draw_a_point(uint8_t x_axis, uint8_t y_axis, uint8_t delay){
  uint8_t sseq_data[] = {x_axis,y_axis,1}; //light
  ordered_insert(
                add_screen_time_index(Screen_Time_Index),
                sseq_data);
  sseq_data[2] = 0; //dark
  ordered_insert(
                add_screen_time_index(Screen_Time_Index+delay),
                sseq_data);
}

void send_signal(){
  Serial.println("Program FINISH HERE");
  //Serial.println(cont);
  cont++;
  
}


//display.drawPixel(1,1,BLACK);
//display.setCursor(40, 30);
//display.println("HOWDY !");
//display.display();