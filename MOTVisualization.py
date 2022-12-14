from Visualize import Visualizer
import glob
import os
import cv2
import numpy as np
import pandas as pd

class MOTVisualizer(Visualizer):

	def load(self, FilePath):
		data = np.genfromtxt(FilePath, delimiter=',')
		if data.ndim == 1:  # Because in MOT we have different delimites in result files?!?!?!?!?!?
			data = np.genfromtxt(FilePath, delimiter=' ')
		if data.ndim == 1:  # Because
			print("Ooops, cant parse %s, skipping this one ... " % FilePath)

			return None
		# clean nan from results
		#data = data[~np.isnan(data)]
		nan_index = np.sum( np.isnan(data ), axis = 1)
		data = data[nan_index==0]
		return data

	def drawResults(self, im = None, t = 0):
		self.draw_boxes = False

		maxConf = 1
		if self.mode == "det":
			maxConf = max(self.resFile[:,6])



		# boxes in this frame
		thisF=np.flatnonzero(self.resFile[:,0]==t)


		for bb in thisF:
			targetID = self.resFile[bb,1]
			IDstr = "%d" % targetID
			left=((self.resFile[bb,2]-1)*self.imScale).astype(int)
			top=((self.resFile[bb,3]-1)*self.imScale).astype(int)
			width=((self.resFile[bb,4])*self.imScale).astype(int)
			height=((self.resFile[bb,5])*self.imScale).astype(int)

			left=((self.resFile[bb,2]-1)).astype(int)
			top=((self.resFile[bb,3]-1)).astype(int)
			width=((self.resFile[bb,4])).astype(int)
			height=((self.resFile[bb,5])).astype(int)

			# normalize confidence to [0,5]
			rawConf=self.resFile[bb,6]
			conf=(rawConf)/maxConf
			conf = int(conf * 5)


			pt1=(left,top)
			pt2=(left+width,top+height)

			color = self.colors[int(targetID % len(self.colors))]
			color = tuple([int(c*255) for c in color])



			if  self.mode == "gt":
				label = self.resFile[bb, 7]
			else:
				label = 1


			# occluder
			if ((self.mode == "gt") & (self.showOccluder) & (int(label) in [9, 10, 11, 13])):

				overlay = im.copy()
				alpha = 0.7
				color = (0.7*255, 0.7*255, 0.7*255)
				cv2.rectangle(overlay,pt1,pt2,color ,-1)
				im = cv2.addWeighted(overlay, alpha, im, 1 - alpha, 0)

			else:
				cv2.rectangle(im,pt1,pt2,color,2)
				if not self.mode == "det":
					cv2.putText(im,IDstr,pt1,cv2.FONT_HERSHEY_SIMPLEX,1, color = color)
		
		#cv2.imwrite("/home/ubuntu/exp/MOTChallengeEvalKit-master/res/img/image.jpg",im)
		return im

if __name__ == "__main__":
	seq_nums =  ['MOT17-02-SDP',
            'MOT17-04-SDP',
            'MOT17-05-SDP',
            'MOT17-09-SDP',
            'MOT17-10-SDP',
            'MOT17-11-SDP',
            'MOT17-13-SDP']

	for seq_num in seq_nums:
		filepath="./res"
		filepath=os.path.join(filepath,f'{seq_num}_ids.txt')
		image="./data/MOT17/images/"
		image=os.path.join(image,seq_num)
		image=os.path.join(image,"img1")
		print(filepath)
		#ids=pd.read_csv(filepath,sep=',',header=None)
		MODE=None
		if os.path.getsize(filepath)==0 :
			MODE='raw'


		
		visualizer = MOTVisualizer(
			seqName = seq_num,
		#FilePath ="data/MOT16/train/MOT16-02/gt/gt.txt",
			FilePath =filepath,
		#image_dir = "data/MOT16/train/MOT16-02/img1",
			image_dir = image,
			mode = MODE,
			output_dir  = "./video_res")

		visualizer.generateVideo(
	        	displayTime = True,
	        	displayName = "MOT",
	        	showOccluder = True,
	        	fps = 25 )
