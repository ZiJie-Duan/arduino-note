import base64

s = ""
with open(r"C:\Users\lucyc\Desktop\arduino-note\ev3_Dianna\website-esay\fontawesome-webfont.ttf", 'rb') as f:
    base64_data = base64.b64encode(f.read())
    s = base64_data.decode()
    s = 'data:image/jpeg;base64,'+s

with open("test.txt","w") as f:
    f.write(s)