import motmetrics as mm
import numpy as np 
import os

metrics = list(mm.metrics.motchallenge_metrics)

seq_nums =  ['video_0',
            'video_1',
            'video_2',
            'video_3',
            'video_4',
            'video_5',
            'video_6',
            'video_7']

save_ids_path='./result'
for seq_num in seq_nums:
    #evaluate the model, save the events in acc[]
    acc = []

    #load gt and test file
    gt_file="./data/vis_2"
    gt_file=os.path.join(gt_file,seq_num)
    gt_file=os.path.join(gt_file,"gt/gt.txt")

    ts_file="./data/vis_2/pred_txt"
    ts_file=os.path.join(ts_file,f'{seq_num}.txt')

    gt=mm.io.loadtxt(gt_file, fmt="mot15-2D", min_confidence=-1)
    ts=mm.io.loadtxt(ts_file, fmt="mot15-2D")
    name=os.path.splitext(os.path.basename(ts_file))[0]
    #compute single acc
    acc=mm.utils.compare_to_groundtruth(gt, ts, 'iou', distth=0.5)

    print(acc.mot_events)
    #search the events of 'SWITCH' and 'MATCH'
    mot_ids=acc.mot_events[acc.mot_events['Type']=='SWITCH']
    mot_match=acc.mot_events[acc.mot_events['Type']=='MATCH']
    mot_ids=mot_ids.append(mot_match)
    mot_ids=mot_ids.sort_values(by='FrameId')
        
    #save result data
    ids_path=os.path.join(save_ids_path,f'{seq_num}_ids.csv')
    path=os.path.join(save_ids_path,f'{seq_num}_mot.csv')
    mot_ids.to_csv(ids_path)
    acc.mot_events.to_csv(path)