# MOT-debugging-tool
A tool for searching Id-switch frames

## Installation
Requiements
* Linux, CUDA>=9.2, GCC>=5.4
* Python>=3.7\
Use Anaconda to create a conda environment:
```
conda create -n mot_tool python=3.7 pip
```
Then, activate the environment:
```
conda activate mot_tool
```
Other requirements
```
pip install -r requirements.txt
```
## Usage
```
cd ./MOT_tool
```
Organize the data as follows
```
.
├── data
│   │── vis_2
│   │    ├── pred_txt
│   │    │    ├── video_0.txt
│   │    │    ├── video_1.txt
│   │    ├── video_0
│   │    │    ├── gt
│   │    │    │    ├── gt.txt
│   │    │    ├── img1
│   │    │    │    ├── 000000.jpg
│   │    │    │    ├── 000001.jpg
│   │    ├── video_1
│   │    ├── video_2
│   │    ├── video_3
│   │    ├── video_4
│   │    ├── video_5
│   │    ├── video_6
│   │    ├── video_7
```


## Evaluation and Visualization
Run the following command:
```
sh model_submit.sh
```
There will be a webpage shown, which is built by dash,a repo for data visualization\

The video generated is in ./video_res

## Dash web
`Video_Jump`: Jump to the video selected from the list\
`Index_Jump`: Jump to a certain frame of input\
`Previous`: Jump to the previous frame\
`Next`: Jump to the next frame\
`Bug_Previous`: Jump to the previous frame of Id-Switch\
`Bug_Next`: Jump to the next frame of Id-Switch\
