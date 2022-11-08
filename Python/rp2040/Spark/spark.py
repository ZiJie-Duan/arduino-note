import random

class SPARK:
    def __init__(self):
        self.screen_sequence = [[] for i in range(30)]
        self.location = []
        self.boundary = [128,64]

    def boundary_check(self,location):
        if location[0] >= self.boundary[0] or location[1] >= self.boundary[1]\
             or location[0] < 0 or location[1] < 0:
            return False
        else:
            return True

    def draw_a_point(self,location,delay=1):
        self.screen_sequence[0].append(location[:]+[1])
        self.screen_sequence[delay].append(location[:]+[0])

    def draw_a_line(self,direction,number,delay=1):
        location = self.location[:]
        for i in range(1,number):
            if direction == 1:
                location[1] = location[1] - 1
            elif direction == 2:
                location[0] = location[0] + 1
                location[1] = location[1] - 1
            elif direction == 3:
                location[0] = location[0] + 1
            elif direction == 4:
                location[0] = location[0] + 1
                location[1] = location[1] + 1
            elif direction == 5:
                location[1] = location[1] + 1
            elif direction == 6:
                location[0] = location[0] - 1
                location[1] = location[1] + 1
            elif direction == 7:
                location[0] = location[0] - 1
            elif direction == 8:
                location[0] = location[0] - 1
                location[1] = location[1] - 1
            if self.boundary_check(location):
                self.screen_sequence[i].append(location[:]+[1])
                self.screen_sequence[i+delay].append(location[:]+[0])

    def spark_maker(self,location,spark_type,size):
        #location is the coordinate of screen
        #size is the size of spark
        #spark_type is the spark_type of spark
        self.location = location[:]
        if spark_type == 1:
            self.draw_a_point(self.location)
            self.draw_a_line(1,size,delay=2)
            self.draw_a_line(3,size,delay=2)
            self.draw_a_line(5,size,delay=2)
            self.draw_a_line(7,size,delay=2)
        elif spark_type == 2:
            self.draw_a_point(self.location)
            self.draw_a_line(2,size,delay=2)
            self.draw_a_line(4,size,delay=2)
            self.draw_a_line(6,size,delay=2)
            self.draw_a_line(8,size,delay=2)
        elif spark_type == 3:
            self.draw_a_point(self.location)
            self.draw_a_line(1,size)
            self.draw_a_line(2,size)
            self.draw_a_line(3,size)
            self.draw_a_line(4,size)
            self.draw_a_line(5,size)
            self.draw_a_line(6,size)
            self.draw_a_line(7,size)
            self.draw_a_line(8,size)
        elif spark_type == 4:
            self.draw_a_point(self.location)
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(3,8))
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(3,8))
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(3,8))
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(3,8))
        elif spark_type == 5:
            self.draw_a_point(self.location)
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(1,5))
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(1,5))
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(1,5))
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(1,5))
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(1,5))
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(1,5))
        elif spark_type == 6:
            self.draw_a_point(self.location)
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(1,5))
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(1,5))
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(1,5))
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(1,5))
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(1,5))
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(1,5))
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(1,5))
            self.draw_a_line(random.randint(1,8),size,delay=random.randint(1,5))


