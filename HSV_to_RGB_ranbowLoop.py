'''
Example based on the formula from the following page:
https://www.rapidtables.com/convert/color/hsv-to-rgb.html
'''

import turtle

#initial setup
t = turtle.Turtle(shape="turtle")
turtle.colormode(255)
t.speed(0)

def DrawCircle(r,g,b,x,y):
    t.penup()
    t.setposition(x, y)
    t.pendown()
    t.pencolor(r,g,b)
    t.circle(30)


for i in range(360):
    hue = i
    saturation = 1.0
    value = 1.0
    C = value * saturation
    X = C * (1.0 - abs((hue/60.0)%2 - 1.0))
    m = value - C
    sectionList = [
        [C, X, 0],
        [X, C, 0],
        [0, C, X],
        [0, X, C],
        [X, 0, C],
        [C, 0, X],
        ]
    section = sectionList[hue/60]
    rgb = [
        (section[0]+m)*255,
        (section[1]+m)*255,
        (section[2]+m)*255,
        ]
    DrawCircle(rgb[0],rgb[1],rgb[2],-200+i,0)
    
turtle.getscreen()._root.mainloop()
