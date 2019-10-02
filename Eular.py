import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)
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
x=[-20*3.14/180,0,0]
R=eulerAnglesToRotationMatrix(x)
print(R)
x_axis=np.dot(R,np.array([[1],[0],[0]]))
y_axis=np.dot(R,np.array([[0],[1],[0]]))
z_axis=np.dot(R,np.array([[0],[0],[1]]))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot([0,x_axis[0][0]], [0,x_axis[1][0]], [0,x_axis[2][0]],  'r')
a = Arrow3D([0,y_axis[0][0]], [0,y_axis[1][0]], [0,y_axis[2][0]],mutation_scale=20, lw=1, arrowstyle="-|>", color="green")
#ax.plot([0,y_axis[0][0]], [0,y_axis[1][0]], [0,y_axis[2][0]], color='green')
ax.plot([0,z_axis[0][0]], [0,z_axis[1][0]], [0,z_axis[2][0]], color='blue')

ax.add_artist(a)
ax.set_zlim(-0.6,1)
ax.legend()
plt.xlim((-0.6, 1))
plt.ylim((-0.6, 1))

plt.show()
