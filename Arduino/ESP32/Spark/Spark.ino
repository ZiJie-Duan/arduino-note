// 在树莓派上运行OLED1.3 首先需要注意修改 pico内部的iic引脚映射，接着修改Adafruit_SSD1306.h文件，移除掉提示不存在的库文件
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>
#include <string.h>

#define SCREEN_WIDTH 128     // OLED display width, in pixels
#define SCREEN_HEIGHT 64     // OLED display height, in pixels
#define OLED_RESET -1        // Reset pin # (or -1 if sharing Arduino reset pin)
#define i2c_Address 0x3c  ///< See datasheet for Address; 0x3C

#define SSEQ_TIME_NUM 30 //screen_sequence pixel life length
#define SSEQ_PIXS_NUM 800 //screen_sequence max number of useful pixel
#define SSEQ_BASE_UNIT 4 //screen_sequence base unit
// SSEQ_PIXS_NUM, the first location is a arr [x,0,0], x direct how many data in the SSEQ_PIXS_NUM
#define WHITE SH110X_WHITE
#define BLACK SH110X_BLACK

#define SPARK_SPEED 0
#define SPARK_TYPE 8
#define SMALLEST_SPARK 5
#define BIGEST_SPARK 17
#define SHORTEST_SPARK_LIFE 2
#define LONGEST_SPARK_LIFE 7

#define SCREEN_SPACE_WIDTH 4
#define SCREEN_SPACE_HEIGHT 4

uint8_t Screen_Sequence[SSEQ_TIME_NUM][SSEQ_PIXS_NUM][SSEQ_BASE_UNIT];
int Screen_Time_Index = 0;

int g_x_axis = 0;
int g_y_axis = 0;
int g_spark_type = 0;
int g_spark_size = 0;


Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
int boundary_check(int x_axis, int y_axis);
void print_pixel();
void ordered_insert(int screen_time_index_tem, int *pix_data);
void draw_a_line(int x_axis, int y_axis, int direction, int size, int life = 1);
void draw_a_point(int x_axis, int y_axis, int life = 1);
void spark_maker(int x_axis, int y_axis, int type, int size);
void send_signal();

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  display.begin(i2c_Address, true);
  display.setCursor(0,0);
  display.clearDisplay();
  display.setTextSize(1);               // Normal 1:1 pixel scale
  display.setTextColor(WHITE);  // Draw white text
  delay(3000);
  //spark_maker(50,30,2,5);
}

void loop() {
  // put your main code here, to run repeatedly:
  g_x_axis = random(SCREEN_SPACE_WIDTH, SCREEN_WIDTH-SCREEN_SPACE_WIDTH);
  g_y_axis = random(SCREEN_SPACE_HEIGHT, SCREEN_HEIGHT-SCREEN_SPACE_HEIGHT);
  g_spark_type = random(1, SPARK_TYPE+1);
  g_spark_size = random(SMALLEST_SPARK, BIGEST_SPARK+1);
  spark_maker(g_x_axis,g_y_axis,g_spark_type,g_spark_size);
  spark_maker(g_x_axis,g_y_axis,g_spark_type,g_spark_size);
  spark_maker(g_x_axis,g_y_axis,g_spark_type,g_spark_size);
  print_pixel();
  //if (cont > 15) {cont = 0; display.clearDisplay();}
}

void spark_maker(int x_axis, int y_axis, int type, int size){
  switch (type)
  {
  case 1: //十字
    draw_a_point(x_axis,y_axis,2);
    draw_a_line(x_axis,y_axis,1,size,2);
    draw_a_line(x_axis,y_axis,3,size,2);
    draw_a_line(x_axis,y_axis,5,size,2);
    draw_a_line(x_axis,y_axis,7,size,2);
    break;
  
  case 2: //斜十字
    draw_a_point(x_axis,y_axis,2);
    draw_a_line(x_axis,y_axis,2,size,2);
    draw_a_line(x_axis,y_axis,4,size,2);
    draw_a_line(x_axis,y_axis,6,size,2);
    draw_a_line(x_axis,y_axis,8,size,2);
    break;
  
  case 3: //正方体
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
  
  default:
    int i = random(1, 9);
    for (int ii=0; ii<i; ii++){
      int dir = random(1,9);
      int life = random(SHORTEST_SPARK_LIFE,LONGEST_SPARK_LIFE+1);
      draw_a_line(x_axis,y_axis,dir,size,life);
    }
    break;
  }
}

void draw_a_point(int x_axis, int y_axis, int life){
  int sseq_data[] = {x_axis,y_axis,1}; //light
  ordered_insert(Screen_Time_Index, sseq_data);
  sseq_data[2] = 0; //dark
  ordered_insert(Screen_Time_Index+life, sseq_data);
}

void ordered_insert(int screen_time_index_tem, int *pix_data)
{ 
  int period = 1; // this period, zero means there data can rewrite
  while(screen_time_index_tem >= SSEQ_TIME_NUM){
    screen_time_index_tem -= SSEQ_TIME_NUM;
    period ++;
  }
  if (screen_time_index_tem < Screen_Time_Index) period --;

  for (int i=0; i<SSEQ_PIXS_NUM; i++){
    if (Screen_Sequence[screen_time_index_tem][i][0]==0){
      Screen_Sequence[screen_time_index_tem][i][0] = (uint8_t)period;
      Screen_Sequence[screen_time_index_tem][i][1] = (uint8_t)pix_data[0];
      Screen_Sequence[screen_time_index_tem][i][2] = (uint8_t)pix_data[1];
      Screen_Sequence[screen_time_index_tem][i][3] = (uint8_t)pix_data[2];
      break;
    }
  }
}

void draw_a_line(int x_axis, int y_axis, int direction, int size, int life)
{ 
  int sseq_data[] = {0,0,0}; //init
  for (int i=0; i<size; i++){
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
      ordered_insert(Screen_Time_Index+i, sseq_data);
      sseq_data[2] = 0;
      ordered_insert(Screen_Time_Index+i+life, sseq_data);

    }
  }
}

int boundary_check(int x_axis, int y_axis){
  if ((x_axis > SCREEN_WIDTH) || (x_axis < 0)) return 0;
  if ((y_axis > SCREEN_HEIGHT) || (y_axis < 0)) return 0;
  return 1;
}

void print_pixel(){
  for (int i=0; i<SSEQ_PIXS_NUM; i++){
    switch (Screen_Sequence[Screen_Time_Index][i][0])
    {
    case 0:
      break;

    case 1:
      if (Screen_Sequence[Screen_Time_Index][i][3]){
        display.drawPixel(
        Screen_Sequence[Screen_Time_Index][i][1],
        Screen_Sequence[Screen_Time_Index][i][2],
        WHITE);
      } else {
        display.drawPixel(
        Screen_Sequence[Screen_Time_Index][i][1],
        Screen_Sequence[Screen_Time_Index][i][2],
        BLACK);
      }
      Screen_Sequence[Screen_Time_Index][i][0] -= 1;
      break;

    default:
      Screen_Sequence[Screen_Time_Index][i][0] -= 1;
      break;
    }
  }
  Serial.println("ok I know you will die here");
  display.display();
  Serial.println("right!");
  if (Screen_Time_Index >= SSEQ_TIME_NUM-1){ //these code use the Screen_Time_Index value First
    Screen_Time_Index = 0;
  } else {
    Screen_Time_Index += 1;
  }
}

void send_signal(){
  Serial.println("Program FINISH HERE");
}
