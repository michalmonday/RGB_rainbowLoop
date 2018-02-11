'''
Example based on the formula from the following page:
https://www.rapidtables.com/convert/color/hsv-to-rgb.html

RYB to RGB conversion is based on the work of Nathan Gossett and Baoquan Chen
https://bahamas10.github.io/ryb/assets/ryb.pdf
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


RYB_RGB_cube = {
    "front_up_left": [1, 1, 0], 
    "front_up_right": [1, 0.5, 0],
    "front_down_left": [1, 1, 1], 
    "front_down_right": [1, 0, 0],
    "back_up_left": [0, 0.66, 0.2],
    "back_up_right": [0.2, 0.094, 0], 
    "back_down_left": [0.163, 0.373, 0.6], 
    "back_down_right": [0.5, 0.0, 0.5], 
    }
'''
Visualized cube is at: https://bahamas10.github.io/ryb/assets/magic-colors.png
Let's assume that there is a Red-Yellow-Blue(RYB) color with RYB values of:
R - 0.2 (range between 0 - 1, which later will be multiplied by 255)
Y - 0.2
B - 0.8

These 3 values are the coordinates of a single point in the 3D space of the cube.
R - determines how far the point is to the right
Y - determines how high the point is vertically (upwards)
B - determines how far the point is to the back

Depending on the location of that point within the cube different corners will
affect the value of the final converted RGB color. If the point is close
to the back_down_left corner of the cube it will be more blue, if it's closer
to the front_down_right corner it will be more red. In case if the RYB values
are equal to the values mentioned before (0.2, 0.2, 0.8) the point within the cube
will be located near the left_lower_back corner of it.

It seems like a difficult thing to measure at first but it can be completed with
3x loop of 7 relatively simple operations with a fancy name "linear interpolation" which
is explained here: https://www.youtube.com/watch?v=M0R8-rYed0I
By googling this phrase someone could notice complex formulas but the concept itself is
simple. Linear interpolation is a way of checking how values between certain range would
represent themselves in another range of values. For example let's assume that
3 days ago I had 30 apples and today (after 3 days) I have 120 apples. Using linear interpolation
it is possible to measure how many apples I had on each day between that period of time (assuming that their value was increased in a constant/linear way, hence the word "linear").
(Check comments within "Interpolate" function for another example)



Linear interpolation - line (how 2 ends of the line affect the point between them)

Bilinear interpolation - rectangle (how 4 corners holding different values affect
the point within the 2D area of rectangle, depending on how close it is to each corner
the value will change accordingly, keep in mind that each corner can hold different value)
Bilinear interpolation is explained here: https://www.youtube.com/watch?v=zT7fVcGiG7w
I'd ignore the complex formulas in that video and focus on the sole idea of using 2x initial linear
interpolation + 1x final linear interpolation. (google images are very helpful to visualize that process)
In order to convert RYB from RGB it's necessary to go 1 step further.

Trilinear interpolation - cube (how 8 corners of a 3D shape holding different values affect the point within it,
depending on how close it is to each corner the value will change) 4x initial linear interpolation will have to
be done for 1 of the 3-RYB-vectors (e.g. Red-horizontal_sidewise), followed by 2x linear interpolations for another
vector (e.g. Yellow-vertical) based on the previously calculated 4 values and finalized by the last linear
interpolation using the remaining vector (e.g. Blue-depth) based on the previously calculated 2 values. The RYB_to_RGB
cube holds 3 values at each corner which means that trilinear interpolation has to be done 3 times which adds a
lot to confusion. Keep in mind that for each trilinear interpolation all the 3 RYB values are the same, we just
take into account different number from the 3 numbers at each corner depending on which color of RGB we want to find.

Visualized: https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/3D_interpolation2.svg/220px-3D_interpolation2.svg.png
Source of the image: https://en.wikipedia.org/wiki/Trilinear_interpolation
'''

def Interpolate(val, s, s2):
    '''
    Example:
    val = 5 # value between set 1 that has to be interpolated into set 2
    s = [3, 6] # set 1
    s2 = [30, 120] # set 2

    In such case return value would be 90, that's because 90 relates
    to 30-120 the same way 5 relates to 3-6.    
    '''
    #print "Interpolate: ", str(val), str(s), str(s2)
    # in the next line everything is converted to float just to make sure that the values won't be rounded
    val, s, s2 = float(val), [float(v) for v in s], [float(v) for v in s2]  
    return s2[0] + (s2[1] - s2[0]) * (val - s[0]) / (s[1] - s[0])

def RYB_to_RGB(ryb):
    #print "RYB: ", str(ryb)
    ryb = [c/255.0 for c in ryb]
    r = ryb[0]
    y = ryb[1]
    b = ryb[2]

    rgb = [0,0,0]

    for i in range(3): # for each color use appropriate mapping of 8 corners from the RYB_RGB_cube
        # first step (4x initial sideways measurements)
        sideways_front_up = Interpolate(r, [0,1], [
            RYB_RGB_cube["front_up_left"][i],
            RYB_RGB_cube["front_up_right"][i]
            ])

        sideways_front_down = Interpolate(r, [0,1], [
            RYB_RGB_cube["front_down_left"][i],
            RYB_RGB_cube["front_down_right"][i]
            ])

        sideways_back_up = Interpolate(r, [0,1], [
            RYB_RGB_cube["back_up_left"][i],
            RYB_RGB_cube["back_up_right"][i]
            ])

        sideways_back_down = Interpolate(r, [0,1], [
            RYB_RGB_cube["back_down_left"][i],
            RYB_RGB_cube["back_down_right"][i]
            ])

        #print sideways_1, sideways_2, sideways_3, sideways_4
        
        # second step (2x vertical measurement based on previous results)
        side_vert_front = Interpolate(y, [0,1], [
            sideways_front_down,
            sideways_front_up
            ])

        side_vert_back = Interpolate(y, [0,1], [
            sideways_back_down,
            sideways_back_up
            ])

        # third step (final check of the depth with previous sideways+vertical results affecting the measurement)
        rgb[i] = Interpolate(b, [0,1], [
            side_vert_front,
            side_vert_back
            ])

    rgb = [int(c*255.0) for c in rgb]
    #print "RGB: ", str(rgb)
    return rgb



sectionList = [ # RYB based
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 1, 1],
    [0, 0, 1],
    [1, 0, 1],
    ]

''' # example with custom color variations (red/blue, yellow/green)
sectionList = [ # RYB based
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 1, 1],
    [0, 0, 1],
    [1, 0, 1], # initial 6 (rainbow)    
    [0, 0, 1],
    [1, 0, 0],
    [0, 0, 1],
    [1, 0, 0],
    [0, 0, 1],
    [1, 0, 0],
    [0, 1, 0],
    [0, 1, 1],
    [0, 1, 0],
    [0, 1, 1],
    [0, 1, 0],
    [0, 1, 1],
    [0, 1, 0],
    [0, 1, 1],    
    ]
'''

x_shift = 0 # not related to the concept (shifts each circle to the right forming a rainbow)
for i in range(255*len(sectionList)):
    
    section = sectionList[i/255] # gets the appropriate section like [1,0,0]
    nextSectionIndex = i/255 + 1 if i/255 + 1 < len(sectionList) else 0 # if index of the next section is not lower than the size of sectionList then use the first (0) index
    nextSection = sectionList[nextSectionIndex] # gets the next section like [1,1,0]

    clr = [0,0,0] # initialize list for rgb
    for j in range(3): # loop through 3 colors
        if section[j] == nextSection[j]: # if both corresponding sections have the same values then just use 0 or 255 for this color depending on their value
            clr[j] = section[j] * 255
        elif section[j] > nextSection[j]:
            clr[j] = 255 - (i % 255)
        else:
            clr[j] = i % 255
            
    #clr = RYB_to_RGB(clr)    
    #DrawCircle(clr[0],clr[1],clr[2],-700+i,0)

    
    if i % 5 == 0:
        clr = RYB_to_RGB(clr)
        DrawCircle(clr[0],clr[1],clr[2],-200+x_shift,0)
        x_shift += 1


turtle.getscreen()._root.mainloop()
