# importing the required module
import matplotlib.pyplot as plt
import json

plt.ylim(50, 100)

# x axis values
x = []
# corresponding y axis values
y = []

dist_cam_surface = 60
alpha_file = open('../../Tests/accuracyTest/alpha_accuracy/json/60cm-exposuretest.json')
dict_alpha = json.load(alpha_file)

origin_x = 320

for i in range(100,150):
    x.append(origin_x+i)
    y.append(dict_alpha[str(origin_x+i)])

# plotting the points 
plt.plot(x, y,'ro')
  
# naming the x axis
plt.xlabel('x - axis: x pixel')
# naming the y axis
plt.ylabel('y - axis: accuracy')
  
# giving a title to my graph
plt.title("L = "+str(dist_cam_surface)+"cm")
  
# function to show the plot
plt.show()