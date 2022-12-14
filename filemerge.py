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

#print(ids_res)

FileName_path = ("./pre_models/pub_submit_15")

#print(data2)
FileName_gt_path = ("./data/MOT17/images/")

"""
#fra=data_merge['frame']
print(data_merge['frame'])
print(data_merge['frame'].iloc[144])
print(data_merge.iloc[6,0])
#print(fra[6])
"""

seq_nums =  ['MOT17-02-SDP',
            'MOT17-04-SDP',
            'MOT17-05-SDP',
            'MOT17-09-SDP',
            'MOT17-10-SDP',
            'MOT17-11-SDP',
            'MOT17-13-SDP']

for seq_num in seq_nums:
    FileName_ids=os.path.join(FileName_ids_path,f'{seq_num}_ids.csv')
    FileName=os.path.join(FileName_path,f'{seq_num}.txt')
    FileName_gt=os.path.join(FileName_gt_path,seq_num)
    #print("Filename",FileName_gt_path,"\n")
    FileName_gt=os.path.join(FileName_gt,"gt/gt.txt")
    #print("Filename",FileName_gt,"\n")
    ids_res=pd.read_csv(FileName_ids)

    data=pd.read_csv(FileName,sep=',',header=None)
    #print(data)
    data.columns=['frame', 'id', 'bb_left', 'bb_top', 'bb_width', 'bb_height', 'conf', 'x', 'y', 'z']

    data_gt=pd.read_csv(FileName_gt,sep=',',header=None)
    #print(data_gt)
    data_gt.columns=['frame', 'id', 'bb_left', 'bb_top', 'bb_width', 'bb_height', 'conf', 'x', 'y']
    data_gt=data_gt.sort_values(by="frame")
    data_gt['z']=[1]*data_gt.shape[0]
    """
    
    """
    data_merge=data.append(data_gt)
    data_merge=data_merge.sort_values(by="frame")

    data_ids=pd.DataFrame(columns=['frame', 'id', 'bb_left', 'bb_top', 'bb_width', 'bb_height', 'conf', 'x', 'y', 'z'])

    data_ids_frame=pd.DataFrame(columns=['FrameId','Event','Type','OId','HId','D'])


    save_path="./res"
    #ids_path=os.path.join(save_path,f'{seq_num}_ids.txt')
    #data_ids.to_csv(ids_path,sep=',',index=False,header=None)
    ids_path_merge=os.path.join(save_path,f'{seq_num}_sortmerge.txt')
    data_merge.to_csv(ids_path_merge,sep=',',index=False,header=None)

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
        #print("ids_res",frame,oid,hid,"\n")
            for j in range(last,data.shape[0]):
        #print("frame",j,data_merge['frame'],frame-neigh,"\n")
        
                if (data['frame'].iloc[j]>=frame_bar) & (data['frame'].iloc[j]<frame+2):
                    if (data['id'].iloc[j]==hid) | (data['id'].iloc[j]==hid_bar):
                #print("data ",data_merge['id'].iloc[j],"\n")
                #print(data_merge[j-1:j])
                    #print(data_merge[j:j+1],"\n")
                        data_ids=pd.concat([data_ids,data[j:j+1]])
        
                if data['frame'].iloc[j]>=frame+2:
                    last=j
                    break
            
            for j in range(last_gt,data_gt.shape[0]):
        #print("frame",j,data_merge['frame'],frame-neigh,"\n")
        
                if (data_gt['frame'].iloc[j]>=frame_bar) & (data_gt['frame'].iloc[j]<frame+2):
                    if data_gt['id'].iloc[j]==oid:
                #print("data ",data_merge['id'].iloc[j],"\n")
                #print(data_merge[j-1:j])
                        #print(data_gt[j:j+1],"\n")
                        data_ids=pd.concat([data_ids,data_gt[j:j+1]])
                        #print(data_ids,"\n")
        
                if data_gt['frame'].iloc[j]>=frame+2:
                    last_gt=j
                    break

    data_ids=data_ids.sort_values(by="frame")

    
    ids_path=os.path.join(save_path,f'{seq_num}_ids.txt')
    data_ids.to_csv(ids_path,sep=',',index=False,header=None)
    ids_path_frame=os.path.join(save_path,f'{seq_num}_ids_frame.csv')
    data_ids_frame.to_csv(ids_path_frame,index=False,header=True)
    ids_path_merge=os.path.join(save_path,f'{seq_num}_merge.txt')
    data_merge.to_csv(ids_path_merge,sep=',',index=False,header=None)

"""
for i in range(0,ids_res.shape[0]):
    frame=ids_res['FrameId'][i]
    oid=ids_res['OId'][i]
    hid=ids_res['HId'][i]
    #print("ids_res",frame,oid,hid,"\n")
    for j in range(last,data_merge.shape[0]):
        #print("frame",j,data_merge['frame'],frame-neigh,"\n")
        if (data_merge['frame'].iloc[j]>frame-neigh) & (data_merge['frame'].iloc[j]<frame+neigh):
            if (data_merge['id'].iloc[j]==oid) | (data_merge['id'].iloc[j]==hid):
                #print(data_merge[j-1:j])
                
                data_ids=pd.concat([data_ids,data_merge[j-1:j]])
        
        if data_merge['frame'].iloc[j]>=frame+neigh:
            last=j
            break
"""



#print(data_ids)




"""
data=[]
with open(FileName,'r') as f:
    for line in f:
        data.append(line.strip())

FileName_gt = ("/home/ubuntu/MOT15/train/KITTI-17/gt/gt.txt")
with open(FileName_gt,'r') as f:
    for line in f:
        data.append(line.strip())

FileName_ids = ("/home/ubuntu/exp/MOTR-main/models/motr_mot15/pub_submit_15/KITTI-17_ids.txt")
"""





"""
with open(FileName_ids,'w') as f:
    for line in sorted(data):
        f.writelines(line)
        f.writelines('\n')
    f.close
"""
