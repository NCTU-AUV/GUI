from numpy import arange, sin, pi
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import Tkinter as tk
import traceback
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import rospy
class Page(tk.Frame):
	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)
	def show(self):
		self.lift()
class Page1(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		#---------End of imports

		fig = plt.Figure()




		root = tk.Tk()

		#label = Tk.Label(root,text="SHM Simulation").grid(column=0, row=0)

		canvas = FigureCanvasTkAgg(fig, master=root)
		canvas.get_tk_widget().grid(column=0,row=1)

		ax = fig.add_subplot(111)
		x = [1,2,3,4,5]
		y = [5,7,2,5,3]
		data = np.column_stack([np.linspace(0, yi, 50) for yi in y])
		line, = ax.plot(x, np.sin(x))
		rects = ax.bar(x, data[0], color='c')
		ax.set_ylim(0, max(y))

		def animate(i):
				print i
				for rect, yi in zip(rects, data[i]):
				    rect.set_height(yi)
				line.set_data(x, data[i])
				return rects, line

		anim = animation.FuncAnimation(fig, animate, frames=len(data), interval=40)


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Motor show", command=p1.lift())

        b1.pack(side="left")
        self.pack(side="top")

def GUI():
	rospy.init_node('Show_motor', anonymous=True)
	root = tk.Tk()
	main = MainView(root)
	main.pack(side="top", fill="both", expand=True)
	root.wm_geometry("1500x1000")
	root.mainloop()

if __name__ == "__main__":
	try:
		GUI()
	except Exception as e:
	    exstr = traceback.format_exc()
	    print(exstr)