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
Download the data from [MOT17](https://motchallenge.net/) and organize them as follows
```
.
├── data
│   │── MOT17
│   │    ├── images
│   │    │   ├── MOT17-02-SDP
│   │    │   ├── MOT17-04-SDP
│   │    │   ├── MOT17-05-SDP
│   │    │   ├── MOT17-09-SDP
│   │    │   ├── MOT17-10-SDP
│   │    │   ├── MOT17-11-SDP
│   │    │   ├── MOT17-13-SDP
```
Save your pre-trained model in `MOTtool/pre_models`, and name it `pre_model.pth`

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
