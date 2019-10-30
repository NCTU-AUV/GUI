#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray
import traceback
import cv2
from PIL import ImageTk
from PIL import Image
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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
import Tkinter as tk
import time


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
def Re_Canvasdraw(Eular_Matrix,ax):
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

class Page(tk.Frame):
	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)
	def show(self):
		self.lift()

class Page1(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		self.label = tk.Label(self,text='1')
		self.label.pack()
		self.cap = cv2.VideoCapture(0)
		self.label.after(1000,self.refresh_Label)
	def refresh_Label(self):
		suc , image = self.cap.read()
		if suc:
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			image = Image.fromarray(image)
			image = ImageTk.PhotoImage(image)
			self.label.configure(image=image)
			self.label.image = image
			self.label.after(50, self.refresh_Label)
		else:
			print("trouble")
		
class Page2(Page):
	def __init__(self, *args, **kwargs):
		#===============      for temp  ====================#

		self.temp_x = 0
		self.last_tdata = 0
		Page.__init__(self, *args, **kwargs)
		rospy.Subscriber("/Temp", Float32, self.Temp_back)
		self.temp_fig =Figure(figsize=(5,3), dpi=100)
		self.temp_ax=self.temp_fig.add_subplot(111)
		self.temp_ax.set_xlim((0, 100))
		self.canvas_T =FigureCanvasTkAgg(self.temp_fig, master=self)
		self.canvas_T.show()
		self.canvas_T.get_tk_widget().pack(side=tk.TOP,fill="both")

		#===============      for humidity  =================#

		self.humi_x = 0
		self.last_hdata = 0
		rospy.Subscriber("/Humidity", Float32, self.Humi_back)
		self.humi_fig =Figure(figsize=(5,3), dpi=100)
		self.humi_ax=self.humi_fig.add_subplot(111)
		self.humi_ax.set_xlim((0, 100))
		self.canvas_H =FigureCanvasTkAgg(self.humi_fig, master=self)
		self.canvas_H.show()
		self.canvas_H.get_tk_widget().pack(side=tk.TOP,fill="both")

	def Temp_back(self,data):
		print(data.data)
		self.temp_ax.plot([self.temp_x-1,self.temp_x],[self.last_tdata,data.data],'blue')
		self.last_tdata = data.data
		self.canvas_T.draw()
		if self.temp_x>100:
			self.temp_ax.set_xlim((self.temp_x-100, self.temp_x))
		self.temp_x=self.temp_x+1
	def Humi_back(self,data):
		print(data.data)
		self.humi_ax.plot([self.temp_x-1,self.temp_x],[self.last_hdata,data.data],'blue')
		self.last_hdata = data.data
		self.canvas_H.draw()
		if self.temp_x>100:
			self.humi_ax.set_xlim((self.humi_x-100, self.humi_x))
		self.humi_x=self.humi_x+1
class Page3(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		fig = Figure(figsize=(10, 10), dpi=50) 
		canvas = FigureCanvasTkAgg(fig, master=self)
		canvas.draw()
		self.x = [0,0,0]    #Eular angle X ,Y,Z
		R=eulerAnglesToRotationMatrix(self.x)
		#print(R)
		x_axis=np.dot(R,np.array([[1],[0],[0]]))
		y_axis=np.dot(R,np.array([[0],[1],[0]]))
		z_axis=np.dot(R,np.array([[0],[0],[0.5]]))

		self.ax = fig.add_subplot(111, projection='3d')
		self.ax.plot([0,x_axis[0][0]], [0,x_axis[1][0]], [0,x_axis[2][0]],  'r',label='X_axis(Roll)')
		a = Arrow3D([0,y_axis[0][0]], [0,y_axis[1][0]], [0,y_axis[2][0]],mutation_scale=3, lw=1, arrowstyle="-|>", color="green")
		#ax.plot([0,y_axis[0][0]], [0,y_axis[1][0]], [0,y_axis[2][0]], color='green')
		self.ax.plot([0,z_axis[0][0]], [0,z_axis[1][0]], [0,z_axis[2][0]], color='blue')
		self.ax.add_artist(a)
		self.ax.set_xlim(-0.6,1)
		self.ax.set_ylim(-0.6,1)
		self.ax.set_zlim(-0.6,1)
		self.ax.legend()
		self.ax.mouse_init()
		self.ax.view_init(30, 189)
		#toolbar = NavigationToolbar2TkAgg(canvas, root)
		#toolbar.update()
		canvas.get_tk_widget().place(x=0, y=0)
		global canvas
		s_roll = tk.Scale(self,label="row",from_=-90,to=90,orient=tk.HORIZONTAL ,length=200,showvalue=1,tickinterval=90,resolution=0.01,command=self.change_Roll)
		s_pitch = tk.Scale(self,label="pitch",from_=-90,to=90,orient=tk.HORIZONTAL,length=200,showvalue=1,tickinterval=90,resolution=0.01,command=self.change_Pitch)
		s_yaw = tk.Scale(self,label="yaw",from_=-90,to=90,orient=tk.HORIZONTAL,length=200,showvalue=1,tickinterval=90,resolution=0.01,command=self.change_Yaw)
		s_roll.set(0)
		s_pitch.set(0)
		s_yaw.set(0)
		s_yaw.pack()
		s_pitch.pack()
		s_roll.pack()
	def change_Roll(self,roll):
	    self.x[0]=float(roll)*math.pi/180.
	    Re_Canvasdraw(self.x,self.ax)
	def change_Pitch(self,pitch):
	    self.x[1]=float(pitch)*math.pi/180.
	    Re_Canvasdraw(self.x,self.ax)
	def change_Yaw(self,yaw):
		self.x[2]=float(yaw)*math.pi/180.
		Re_Canvasdraw(self.x,self.ax)


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Page 1", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Page 2", command=p2.lift)
        b3 = tk.Button(buttonframe, text="Page 3", command=p3.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        #p1.show()
def GUI():
	rospy.init_node('listener', anonymous=True)
	root = tk.Tk()
	main = MainView(root)
	main.pack(side="top", fill="both", expand=True)
	root.wm_geometry("1500x1000")
	root.mainloop()
	cv2.destroyAllWindows()
if __name__ == "__main__":
	try:
		GUI()
	except Exception as e:
	    exstr = traceback.format_exc()
	    print(exstr)