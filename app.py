import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import glob
import os.path as osp
from skimage import io
import pickle
import numpy as np
import os
import pandas as pd

return_previous_text= "Previous"
return_next_text= "Next"

return_bug_previous_text=0
return_bug_next_text=0

DEBUG = True
GLOBAL_IDX = 1
BUG_IDX = 0
MARK_TRAJ_ID = -1
is_next = False
is_previous = False
is_bug_next = False
is_bug_previous = False
figure_index = 1 


# Prepare image data
FileName_ids_path="./res/"
#IMG_FOLDER = '/home/ubuntu/MOT15/train/KITTI-13/img1'
IMG_FOLDER ='./img_res/MOT17-02-SDP'
filelist = sorted(glob.glob(osp.join(IMG_FOLDER, '*.jpg')))
# print(filelist)
IMG_NUM = len(filelist)
BUG_NUM = len(filelist)
example_img = io.imread(filelist[0])
# (480,640)
IMG_WIDTH, IMG_HEIGHT = example_img.shape[:2]
jump_index_value = 0
IMG_FOLDER ='./img_res'

# Prepare point trajectory data
# point_traj_list:
# point on time0:[(x0, y0, point_id0),(x1, y1, point_id1)...]
# point on time1:[(x0', y0', point_id0),(x1', y1', point_id1)...]


def debug_print(*args):
    if DEBUG:
        print(*args)

def create_fig():
    return px.imshow(io.imread(filelist[GLOBAL_IDX]), binary_backend="jpg")


video_nums = ['MOT17-02-SDP',
            'MOT17-04-SDP',
            'MOT17-05-SDP',
            'MOT17-09-SDP',
            'MOT17-10-SDP',
            'MOT17-11-SDP',
            'MOT17-13-SDP']

bug_nums = ['Id-switch',
            'False positive',
            'Miss']


"""
                dcc.Dropdown(
                    id="bug-type",
                    options=[
                        {"label": seq, "value": seq}
                        for seq in bug_nums
                    ],
                    value="bug",
                    style={'width': "50%"},
                    clearable=False,
                    searchable=False,
                    className="dropdown",
                ),
"""

# Cards
image_annotation_card = dbc.Card(
    id="imagebox",
    children=[
        dbc.CardHeader(html.H2("MOT")),
        dbc.CardBody(
            [
                dcc.Graph(
                    id="graph",
                    
                ),

            ]
        ),
        dbc.CardFooter(
            [
                
                dcc.Markdown(
                    id="figure-index"
                ),
                dcc.Dropdown(
                    id="video-seq",
                    options=[
                        {"label": seq, "value": seq}
                        for seq in video_nums
                    ],
                    value="video",
                    style={'width': "50%"},
                    clearable=False,
                    className="dropdown",
                ),
                dbc.Button(
                    children="Video_Jump", id="video_jump", outline=True
                ),                
                dcc.Input(
                    id="jump-index", value=jump_index_value, type="text"
                ),
                dbc.Button(
                    children="Index_Jump", id="jump", outline=True
                ),
                dbc.ButtonGroup(
                    [
                        dbc.Button(children="Previous",
                                   id="previous", outline=True),
                        dbc.Button(children="Next", id="next", outline=True),
                    ],
                    size="lg",
                    style={"width": "100%"},
                ),
                dbc.ButtonGroup(
                    [
                        dbc.Button(children="Bug_Previous",
                                   id="bug_previous", outline=True),
                        dbc.Button(children="Bug_Next", id="bug_next", outline=True),
                    ],
                    size="lg",
                    style={"width": "100%"},
                ),
            ]
        ),
    ],
)

external_stylesheets = [dbc.themes.BOOTSTRAP,
                        "/home/ubuntu/exp/dash-motion-visualization/assets/image_annotation_style.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Mot ID-switch"
server = app.server



app.layout = html.Div(
    [
        
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(image_annotation_card, md=10),
                    ],
                ),
            ],
            fluid=True,
        ),
    ]
)


"""
app.layout = html.Div(children=[
    html.H1("Mot debugging", style={'text-align': 'center'}),
    html.Div(children=[
        html.Div(
            children=[
                html.Div(children="Video", className="menu-title"),
                dcc.Dropdown(
                    id="region-filter",
                    options=[
                        {"label": seq, "value": seq}
                        for seq in video_nums
                    ],
                    value="Albany",
                    style={'width': "50%"},
                    clearable=False,
                    className="dropdown",
                ),
            ]
        ),
        html.Div(
            children=[
                html.Div(children="Debugging Type", className="menu-title"),
                dcc.Dropdown(
                    id="type-filter",
                    options=[
                        {"label": seq, "value": seq}
                        for seq in bug_nums
                    ],
                    value="organic",
                    style={'width': "50%"},
                    clearable=False,
                    searchable=False,
                    className="dropdown",
                ),
            ],
        ),
    ],
        className="menu",
    ),

    html.Video(
        controls=True,
        id='movie_player',
        #src = "/home/ubuntu/exp/MOTChallengeEvalKit-master/res/KITTI-17/KITTI-17_test1.mp4",
        #src="https://www.w3schools.com/html/mov_bbb.mp4",
        src = "https://drive.google.com/file/d/1XeMmG3oEy7AK1jqruV_Zmxs57cYsZ6h2/view?usp=share_link",
        autoPlay=True,
        style={'width': "50%"}
    ),
    dcc.Graph(

        id="graph",
        figure=example_img,
    ),
    dcc.Input(
            id='bug-id',
            value='1',
            type='text'
            ),
    dcc.Slider(
               min=0,
               max=9,
               marks={i: 'level{}'.format(i) for i in range(10)},
               value=5,
           ),
    dbc.ButtonGroup(
                    [
                        dbc.Button(children="Previous", id="previous", outline=True),
                        dbc.Button(children="Next", id="next", outline=True),
                    ],
                    size="lg",
                    style={"width": "100%"},
    ),
])
"""

@app.callback(
    [Output("graph","figure"), Output("next", "children"), Output("previous", "children"),Output("bug_next", "n_clicks"), Output("bug_previous", "n_clicks"),Output("figure-index", "children")],
    [Input("previous", "n_clicks"), Input("next", "n_clicks"),Input("bug_previous", "n_clicks"), Input("bug_next", "n_clicks"),Input('video-seq','value'),Input('video_jump', 'n_clicks'), Input('jump', 'n_clicks'), Input('jump-index', 'value')]
)
def control_video(previous_n_clicks, next_n_clicks, bug_previous_n_clicks, bug_next_n_clicks, video_value,video_jump_n_clicks, jump_n_clicks ,jump_index):
    global GLOBAL_IDX, BUG_IDX,IMG_NUM,BUG_NUM, POINT_NUM, MARK_TRAJ_ID, jump_index_value
    global filelist, point_traj_list
    global is_next, is_previous
    global is_bug_next, is_bug_previous
    global return_previous_text, return_next_text
    global return_bug_previous_text, return_bug_next_text
    global figure_index
    global Frame_bug
    # global next_children, previous_children
    calllback_context = [p["prop_id"]
                         for p in dash.callback_context.triggered][0]
    """
    if calllback_context == "previous.n_clicks" and is_previous == False:
        is_previous = True
        return_previous_text = "Stop"
        calllback_context = ""

    if calllback_context == "previous.n_clicks" and is_previous == True:
        is_previous = False
        return_previous_text = "Previous"
        calllback_context = ""

    if calllback_context == "next.n_clicks" and is_next == False:
        is_next = True
        return_next_text = "Stop"
        calllback_context = ""

    if calllback_context == "next.n_clicks" and is_next == True:
        is_next = False
        return_next_text = "Next"
        calllback_context = ""
    """
    if calllback_context == "previous.n_clicks" :
        is_previous = True
        return_previous_text = "Previous"
        GLOBAL_IDX = (GLOBAL_IDX - 1) % IMG_NUM
        debug_print('GLOBAL_IDX:', GLOBAL_IDX)
        calllback_context = ""

    if calllback_context == "next.n_clicks":
        is_next = True
        return_next_text = "Next"
        GLOBAL_IDX = (GLOBAL_IDX + 1) % IMG_NUM
        debug_print('GLOBAL_IDX:', GLOBAL_IDX)
        calllback_context = ""
        # fig_next_thread = threading.Thread(target=fig_next).start()
        # return fig_next_thread

    """
    if calllback_context == "bug_previous.n_clicks" and is_bug_previous == False:
        is_bug_previous = True
        return_bug_previous_text = "Bug_Stop"
        calllback_context = ""

    if calllback_context == "bug_previous.n_clicks" and is_bug_previous == True:
        is_bug_previous = False
        return_bug_previous_text = "bug_Previous"
        calllback_context = ""

    if calllback_context == "bug_next.n_clicks" and is_bug_next == False:
        is_bug_next = True
        return_bug_next_text = "Bug_Stop"
        calllback_context = ""

    if calllback_context == "bug_next.n_clicks" and is_bug_next == True:
        is_bug_next = False
        return_bug_next_text = "bug_Next"
        calllback_context = ""
    """
    if calllback_context == "bug_previous.n_clicks" and BUG_NUM>0:
        #is_bug_previous = False
        return_bug_previous_text = "bug_Previous"

        BUG_IDX = (BUG_IDX - 1) % BUG_NUM 
        GLOBAL_IDX = Frame_bug[BUG_IDX]-1
        debug_print('GLOBAL_IDX:', GLOBAL_IDX)
        debug_print('BUG_IDX:', BUG_IDX)
        calllback_context = ""

    if calllback_context == "bug_next.n_clicks" and BUG_NUM>0:
        #is_bug_next = False
        return_bug_next_text = "bug_Next"
        BUG_IDX = (BUG_IDX + 1) % BUG_NUM
        GLOBAL_IDX = Frame_bug[BUG_IDX]-1
        debug_print('GLOBAL_IDX:', GLOBAL_IDX)
        debug_print('BUG_IDX:', BUG_IDX)
        calllback_context = ""

    if calllback_context == 'jump.n_clicks':
        GLOBAL_IDX = int(jump_index)-1
        debug_print('GLOBAL_IDX:', GLOBAL_IDX)
        calllback_context = ""

    """
    if is_next:
        GLOBAL_IDX = (GLOBAL_IDX + 1) % IMG_NUM
        debug_print('GLOBAL_IDX:', GLOBAL_IDX)

    if is_previous:
        GLOBAL_IDX = ((GLOBAL_IDX - 1) % IMG_NUM + IMG_NUM) % IMG_NUM
        debug_print('GLOBAL_IDX:', GLOBAL_IDX)
    
    """
    
    """
    if is_bug_next and BUG_NUM>0:
        BUG_IDX = (BUG_IDX + 1) % BUG_NUM
        GLOBAL_IDX = Frame_bug[BUG_IDX]
        debug_print('GLOBAL_IDX:', GLOBAL_IDX)
        debug_print('BUG_IDX:', BUG_IDX)

    if is_bug_previous and BUG_NUM>0:
        BUG_IDX = (BUG_IDX - 1) % BUG_NUM 
        GLOBAL_IDX = Frame_bug[BUG_IDX]
        debug_print('GLOBAL_IDX:', GLOBAL_IDX)
        debug_print('BUG_IDX:', BUG_IDX)
    """
    

    if calllback_context == 'video_jump.n_clicks':
        BUG_IDX=-1
        GLOBAL_IDX=0
        #IMG_FOLDER = '/home/ubuntu/exp/MOTR-main/MOT17/images/train'
        
        img_folder =os.path.join(IMG_FOLDER ,video_value)
        len_name=len(img_folder)
        #IMG_FOLDER =os.path.join(IMG_FOLDER ,"img1")
        filelist = glob.glob(osp.join(img_folder, '*.jpg'))
        filelist.sort(key = lambda x : int(x[(len_name+1):-4]))

        FileName_ids=os.path.join(FileName_ids_path,f'{video_value}_ids_frame.csv')
    #FileName_ids=os.path.join(FileName_ids_path,f'MOT17-02-SDP_ids.csv')
        ids_res=pd.read_csv(FileName_ids)
        Frame_bug=ids_res["FrameId"]
    #Frame_bug=Frame_bug.drop_duplicates()
    # print(filelist)
        IMG_NUM = len(filelist)
        BUG_NUM = len(Frame_bug)
       
    

    figure=px.imshow(io.imread(filelist[GLOBAL_IDX]), binary_backend="jpg")
    figure_index = "Figure index: " + str(GLOBAL_IDX+1) + "/" + str(IMG_NUM)
    return [figure,return_next_text, return_previous_text,return_bug_next_text, return_bug_previous_text,figure_index]


if __name__ == "__main__":
    app.run_server(debug=True)