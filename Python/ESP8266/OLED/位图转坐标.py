import numpy as np
from PIL import Image
image = Image.open(r'C:\Users\lucyc\Desktop\a.ppm')
mat= np.array(image)
xs_list = []

line = 0
px = 0

for linee in mat:
	for pxx in linee:
		if pxx[0] < 180:
			xs_list.append([px,line])
		px += 1
	line += 1
	px = 0

print(xs_list)
input()
