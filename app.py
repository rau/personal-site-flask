from flask import Flask, render_template, request, redirect, session
from flask import send_file, make_response, send_from_directory
from functions import get_children, bfs_shortest_path, get_children_app, a_star_heuristic
from textwrap import wrap
import os
import time

# Sets CWD to whatever directory app.py is located in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize flask app, SECRET_KEY can be found in keys.py
app = Flask(__name__, template_folder="templates")
app.root_path = os.path.dirname(os.path.abspath(__file__))


global path
path = []
'''Static Routes'''
# Homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        global path
        path = bfs_shortest_path(request.form['puzzle'], '3')
        return redirect((request.url + 'puzzle/' + request.form['puzzle']))
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/puzzle/<puzzle>', methods=['GET', 'POST'])
def display_new_puzzle(puzzle):
    global path

    children = get_children_app(puzzle, '3')
    left, right, up, down = 'NO <br/> PUZZLE <br/> HERE', 'NO <br/> PUZZLE <br/> HERE', 'NO <br/> PUZZLE <br/> HERE', 'NO <br/> PUZZLE <br/> HERE'

    url = request.url_root + 'puzzle/'
    left_link, right_link, up_link, down_link = url + left, url + right, url + up, url + down

    left_style, right_style, up_style, down_style = "background-color: #ff0000", "background-color: #ff0000", "background-color: #ff0000", "background-color: #ff0000"

    if 'left' in children:
        left = children['left']
        left_link = url + left
        list_left = wrap(left, 3)
        left = ''.join([string + '<br/>' for string in list_left])
        left += ("Inv: " + str(a_star_heuristic(children['left'], 3)))

        if children['left'] in path:
            left_style = "background-color: #00ff00"

    if 'right' in children:
        right = children['right']
        right_link = url + right
        list_left = wrap(right, 3)
        right = ''.join([string + '<br/>' for string in list_left])
        right += ("Inv: " + str(a_star_heuristic(children['right'], 3)))
        if children['right'] in path:
            right_style = "background-color: #00ff00"

    if 'up' in children:
        up = children['up']
        up_link = url + up
        list_left = wrap(up, 3)
        up = ''.join([string + '<br/>' for string in list_left])
        up += ("Inv: " + str(a_star_heuristic(children['up'], 3)))
        if children['up'] in path:
            up_style = "background-color: #00ff00"

    if 'down' in children:
        down = children['down']
        down_link = url + down
        list_left = wrap(down, 3)
        down = ''.join([string + '<br/>' for string in list_left])
        down += ("Inv: " + str(a_star_heuristic(children['down'], 3)))
        if children['down'] in path:
            down_style = "background-color: #00ff00"

    list_puzzle = wrap(puzzle, 3)
    puzzle = ''.join([string + '<br/>' for string in list_puzzle])

    return render_template('puzzle.html', puzzle_up=up, puzzle_down=down,
                           puzzle_left=left, puzzle_right=right, puzzle_middle=puzzle,
                           left_link=left_link, right_link=right_link, up_link=up_link,
                           down_link=down_link, left_style=left_style, right_style=right_style,
                           up_style=up_style, down_style=down_style)


if __name__ == '__main__':
    app.run()
