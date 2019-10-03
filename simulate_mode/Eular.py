import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
matplotlib.use('TkAgg')
import Tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

#==========            Make a 3D Arrow             ==============
class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)
#=========            function to rotate           ===========
def eulerAnglesToRotationMatrix(theta) :
    R_x = np.array([[1,         0,                  0                   ],
                    [0,         math.cos(theta[0]), -math.sin(theta[0]) ],
                    [0,         math.sin(theta[0]), math.cos(theta[0])  ]
                    ])
         
         
                     
    R_y = np.array([[math.cos(theta[1]),    0,      math.sin(theta[1])  ],
                    [0,                     1,      0                   ],
                    [-math.sin(theta[1]),   0,      math.cos(theta[1])  ]
                    ])
                 
    R_z = np.array([[math.cos(theta[2]),    -math.sin(theta[2]),    0],
                    [math.sin(theta[2]),    math.cos(theta[2]),     0],
                    [0,                     0,                      1]
                    ])
                     
                     
    R = np.dot(R_z, np.dot( R_y, R_x ))
 
    return R
def Re_Canvasdraw(Eular_Matrix):
    global ax
    global canvas
    R=eulerAnglesToRotationMatrix(Eular_Matrix)
    x_axis=np.dot(R,np.array([[1],[0],[0]]))
    y_axis=np.dot(R,np.array([[0],[1],[0]]))
    z_axis=np.dot(R,np.array([[0],[0],[0.5]]))
    ax.cla()
    ax.plot([0,y_axis[0][0]], [0,y_axis[1][0]], [0,y_axis[2][0]],  'green',label='X_axis(Roll)')
    a = Arrow3D([0,x_axis[0][0]], [0,x_axis[1][0]], [0,x_axis[2][0]],mutation_scale=20, lw=1, arrowstyle="-|>", color="red")
    ax.add_artist(a)
    ax.plot([0,z_axis[0][0]], [0,z_axis[1][0]], [0,z_axis[2][0]], color='blue')
    ax.set_xlim(-0.6,1)
    ax.set_ylim(-0.6,1)
    ax.set_zlim(-0.6,1)
    ax.legend()
    canvas.draw()
def change_Roll(roll):
    global x
    x[0]=float(roll)*math.pi/180.
    Re_Canvasdraw(x)
def change_Pitch(pitch):
    global x
    x[1]=float(pitch)*math.pi/180.
    Re_Canvasdraw(x)
def change_Yaw(yaw):
    global x
    x[2]=float(yaw)*math.pi/180.
    Re_Canvasdraw(x)
root = tk.Tk()
root.title("IMU in Tk")
root.geometry("1000x600")
fig = Figure(figsize=(10, 10), dpi=50) 
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
x=[0,0,0]    #Eular angle X ,Y,Z
R=eulerAnglesToRotationMatrix(x)
#print(R)
x_axis=np.dot(R,np.array([[1],[0],[0]]))
y_axis=np.dot(R,np.array([[0],[1],[0]]))
z_axis=np.dot(R,np.array([[0],[0],[0.5]]))

ax = fig.add_subplot(111, projection='3d')
ax.plot([0,x_axis[0][0]], [0,x_axis[1][0]], [0,x_axis[2][0]],  'r',label='X_axis(Roll)')
a = Arrow3D([0,y_axis[0][0]], [0,y_axis[1][0]], [0,y_axis[2][0]],mutation_scale=3, lw=1, arrowstyle="-|>", color="green")
#ax.plot([0,y_axis[0][0]], [0,y_axis[1][0]], [0,y_axis[2][0]], color='green')
ax.plot([0,z_axis[0][0]], [0,z_axis[1][0]], [0,z_axis[2][0]], color='blue')
ax.add_artist(a)
ax.set_xlim(-0.6,1)
ax.set_ylim(-0.6,1)
ax.set_zlim(-0.6,1)
ax.legend()

'''
plt.xlim((-0.6, 1))
plt.ylim((-0.6, 1))

plt.show()
'''
ax.mouse_init()
ax.view_init(30, 189)
#toolbar = NavigationToolbar2TkAgg(canvas, root)
#toolbar.update()
canvas.get_tk_widget().pack(padx = 10,side = tk.LEFT)
s_roll = tk.Scale(root,label="row",from_=-90,to=90,orient=tk.HORIZONTAL,length=200,showvalue=1,tickinterval=90,resolution=0.01,command=change_Roll)
s_pitch = tk.Scale(root,label="pitch",from_=-90,to=90,orient=tk.HORIZONTAL,length=200,showvalue=1,tickinterval=90,resolution=0.01,command=change_Pitch)
s_yaw = tk.Scale(root,label="yaw",from_=-90,to=90,orient=tk.HORIZONTAL,length=200,showvalue=1,tickinterval=90,resolution=0.01,command=change_Yaw)
s_roll.set(0)
s_pitch.set(0)
s_yaw.set(0)
s_yaw.pack()
s_pitch.pack()
s_roll.pack()
tk.mainloop()