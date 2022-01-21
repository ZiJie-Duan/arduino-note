from maix import display, camera

camera.config(size=(1280, 720))
while True:
    img = camera.capture()
    #img_show = img.copy().resize(240, 240)
    img_show = img.copy(240, 240)
    img_show.draw_string(0, 220, "Widowmaker", 1, color=(0, 225, 0))
    img_show.draw_line(120,100,120,140,color=(255, 0, 0))
    img_show.draw_line(100,120,140,120,color=(255, 0, 0))

    display.show(img_show)