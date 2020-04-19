from flask import Flask, render_template, request, redirect, session
from flask import send_file, make_response, send_from_directory, flash
from werkzeug.utils import secure_filename
from puzzle_functions import get_children, bfs_shortest_path, get_children_app, a_star_heuristic
from upload_functions import allowed_file
from keys import SECRET_KEY
from textwrap import wrap
import os

# Sets CWD to whatever directory app.py is located in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, template_folder="templates")
app.root_path = os.path.dirname(os.path.abspath(__file__))
app.secret_key=SECRET_KEY

UPLOAD_PATH = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'PNG', 'JPG', 'JPEG'])
app.config['UPLOAD_PATH'] = UPLOAD_PATH


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/eabsentee')
def eabsentee():
    return render_template('eabsentee.html')

@app.route('/ion')
def ion():
    return render_template('ion.html')


# Upload
@app.route('/upload', methods=['GET', 'POST'])
def image_upload():
    if request.method == 'POST':
        if 'image' not in request.files:
            print('Not in')
            flash('No file uploaded')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(os.path.join(app.config['UPLOAD_PATH'], filename))
            file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            return redirect(f"/image/{filename}")
    if request.method == 'GET':
        return render_template('upload.html')

@app.route('/image/<path>')
def image_host(path):
    return send_from_directory(app.config['UPLOAD_PATH'], path, as_attachment=False)


# Puzzles

global path
path = []

@app.route('/slidingpuzzles', methods=['GET', 'POST'])
def puzzles():
    if request.method == 'POST':
        global path
        path = bfs_shortest_path(request.form['puzzle'], '3')
        return redirect((request.url + 'puzzle/' + request.form['puzzle']))
    if request.method == 'GET':
        return render_template('puzzle_home.html')


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
    app.run(debug=True)
