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
## Usage
```
cd ./MOT_tool
```
Download the data from and organize them as follows
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
