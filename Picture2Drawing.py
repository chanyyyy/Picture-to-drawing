from PIL import Image
import numpy as np
 
a = np.asarray(Image.open('./artist.jpg').convert('L')).astype('float')
 
depth = 10.                      #深度，控制素描笔触深浅，在（0，100）区间
grad = np.gradient(a)             #取图像灰度的梯度值
grad_x, grad_y = grad               #横纵方向的梯度值分别反映对应方向的灰度变化率
grad_x = grad_x*depth/100.              #深度影响后的x方向梯度，标准化
grad_y = grad_y*depth/100.
A = np.sqrt(grad_x**2 + grad_y**2 + 1.)  #单位坐标系
unit_x = grad_x/A                #单位坐标轴方向梯度
unit_y = grad_y/A               
unit_z = 1./A               
 
elevation = np.pi/2.3                   #光源的俯视角度
azimuth = np.pi/2.                    #光源的方位角度
dx = np.cos(elevation)*np.cos(azimuth)   #光源对坐标轴的影响
dy = np.cos(elevation)*np.sin(azimuth)   
dz = np.sin(elevation)                 
 
b = 255*(dx*unit_x + dy*unit_y + dz*unit_z)     #考虑光源影响后的梯度转化为灰度
b = b.clip(0,255)               #将灰度裁剪到（0，255）区间
 
im = Image.fromarray(b.astype('uint8'))  #生成素描图像
im.save('./artist_drawing.jpg')
