from asyncore import read
import fileinput

import os
from matplotlib.pyplot import show
import numpy as np
import pandas as pd
import random
import argparse
import torchvision.transforms.functional as F
import torch
import cv2
from tqdm import tqdm
from pathlib import Path
from PIL import Image, ImageDraw
from typing import List
from util.evaluation import Evaluator
import motmetrics as mm
import shutil
import pandas


FileName_ids_path="./result/"

FileName_path = ("./data/vis_2/pred_txt")

FileName_gt_path = ("./data/vis_2")

seq_nums =  ['video_0',
            'video_1',
            'video_2',
            'video_3',
            'video_4',
            'video_5',
            'video_6',
	        'video_7']

for seq_num in seq_nums:
    #MOT events data file
    FileName_ids=os.path.join(FileName_ids_path,f'{seq_num}_ids.csv')
    ids_res=pd.read_csv(FileName_ids)

    #predicted data file
    FileName=os.path.join(FileName_path,f'{seq_num}.txt')
    data=pd.read_csv(FileName,sep=',',header=None)
    data.columns=['frame', 'id', 'bb_left', 'bb_top', 'bb_width', 'bb_height', 'conf', 'x', 'y', 'z']

    #gt data file 
    FileName_gt=os.path.join(FileName_gt_path,seq_num)
    FileName_gt=os.path.join(FileName_gt,"gt/gt.txt")
    data_gt=pd.read_csv(FileName_gt,sep=',',header=None)
    data_gt.columns=['frame', 'id', 'bb_left', 'bb_top', 'bb_width', 'bb_height', 'conf', 'x', 'y','z']
    data_gt=data_gt.sort_values(by="frame")
    #data_gt['z']=[1]*data_gt.shape[0]

    #data_merge=data.append(data_gt)
    #data_merge=data_merge.sort_values(by="frame")
    data_ids=pd.DataFrame(columns=['frame', 'id', 'bb_left', 'bb_top', 'bb_width', 'bb_height', 'conf', 'x', 'y', 'z'])
    data_ids_frame=pd.DataFrame(columns=['FrameId','Event','Type','OId','HId','D'])

    save_path="./res"
    #ids_path_merge=os.path.join(save_path,f'{seq_num}_sortmerge.txt')
    #data_merge.to_csv(ids_path_merge,sep=',',index=False,header=None)

    last=0
    j=0
    last_gt=0
    
    for i in range(0,ids_res.shape[0]):
        if ids_res['Type'][i]=='SWITCH':
            data_ids_frame=pd.concat([data_ids_frame,ids_res[i:i+1]])
            frame=ids_res['FrameId'][i]
            oid=ids_res['OId'][i]
            hid=ids_res['HId'][i]
            j=i-1
            while j>=0:
                if ((ids_res['Type'][j]=='MATCH') | (ids_res['Type'][j]=='SWITCH')) & (ids_res['OId'][j]==oid):
                    hid_bar=ids_res['HId'][j]
                    frame_bar=ids_res['FrameId'][j]
                   
                    break
                j=j-1
            #search the Ids events in predicted data
            for j in range(last,data.shape[0]):
                if (data['frame'].iloc[j]>=frame_bar) & (data['frame'].iloc[j]<frame+2):
                    if (data['id'].iloc[j]==hid) :
                        data_ids=pd.concat([data_ids,data[j:j+1]])
        
                if data['frame'].iloc[j]>=frame+2:
                    last=j
                    break
            
            #search the Ids events in gt data
            for j in range(last_gt,data_gt.shape[0]):        
                if (data_gt['frame'].iloc[j]>=frame_bar) & (data_gt['frame'].iloc[j]<frame+2):
                    if data_gt['id'].iloc[j]==oid:
                        data_ids=pd.concat([data_ids,data_gt[j:j+1]])
        
                if data_gt['frame'].iloc[j]>=frame+2:
                    last_gt=j
                    break

    #save results 
    data_ids=data_ids.sort_values(by="frame")
    ids_path=os.path.join(save_path,f'{seq_num}_ids.txt')
    data_ids.to_csv(ids_path,sep=',',index=False,header=None)
    """
    ids_path_frame=os.path.join(save_path,f'{seq_num}_ids_frame.csv')
    data_ids_frame.to_csv(ids_path_frame,index=False,header=True)
    ids_path_merge=os.path.join(save_path,f'{seq_num}_merge.txt')
    data_merge.to_csv(ids_path_merge,sep=',',index=False,header=None)
    """
    

