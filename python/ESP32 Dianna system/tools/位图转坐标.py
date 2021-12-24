import numpy as np
from PIL import Image
import json

class PpmToJson:

	def __init__(self):

		self.path = r""
		self.data_name_list = [] #这里不需要包括文件后缀
	
	def change_ppm_to_json(self):

		for name in self.data_name_list:
			ppm_path = self.path + "\\" + str(name) + ".ppm"
			json_path = self.path + "\\" + str(name) + ".json"

			print("开始转换：" + ppm_path)

			image = Image.open(ppm_path)
			mat= np.array(image)
			xs_list = []

			line = 0
			px = 0

			for linee in mat:
				for pxx in linee:
					if pxx[0] < 120: #120
						xs_list.append([px,line])
					px += 1
				line += 1
				px = 0

			with open(json_path,'w') as ojbk:
				json.dump(xs_list,ojbk)

			print("转换完成：" + json_path)

ppm = PpmToJson()
ppm.data_name_list = ["black_heart"]
ppm.path = r"C:\Users\lucyc\Desktop\ESP32 Dianna system\apps\Love_For_Dianna"
ppm.change_ppm_to_json()