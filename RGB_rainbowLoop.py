import turtle
 
#initial setup
t = turtle.Turtle(shape="turtle")
turtle.colormode(255)
t.speed(0)
x = 10
y = 10
 
 
def DrawCircle(r,g,b,x,y):
    t.penup()
    t.setposition(x, y)
    t.pendown()
    t.pencolor(r,g,b)
    t.circle(30)
 
sectionList = [
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 1, 1],
    [0, 0, 1],
    [1, 0, 1],
    ]
     
for i in range(255*6): 
    section = sectionList[i/255]
    nextSectionIndex = i/255 + 1 if i/255 + 1 < len(sectionList) else 0
    nextSection = sectionList[nextSectionIndex]
 
    rgb = [0,0,0]
    for j in range(3):
        if section[j] == nextSection[j]:
            rgb[j] = section[j] * 255
        elif section[j] > nextSection[j]:
            rgb[j] = 255 - (i % 255)
        else:
            rgb[j] = i % 255
     
    DrawCircle(rgb[0],rgb[1],rgb[2],-700+i,0)
     
    #if i % 5 == 0:
        #DrawCircle(rgb[0],rgb[1],rgb[2],-700+i,0)
 
 
 
  
turtle.getscreen()._root.mainloop()
