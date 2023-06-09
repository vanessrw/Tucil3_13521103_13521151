from flask import Flask, render_template, request, session
from src.IOFile import *
from src.algorithm import *
from timeit import timeit
from werkzeug.utils import secure_filename
from jinja2 import Environment
import networkx as nx
import json

app = Flask(__name__)
app.secret_key = 'stima'

locations = []

def jinja2_enumerate(iterable, start=0):
    return enumerate(iterable, start=start)

env = Environment()
env.filters['enumerate'] = jinja2_enumerate

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_node', methods=['POST'])
def add_node():
    # Retrieve the location coordinates from the request data
    lat = float(request.form['lat'])
    lng = float(request.form['lng'])
    
    # Add the location to the locations list
    locations.append((lat, lng))
    
    for i in locations:
        print(i)
        
    print("================================")
    
    return ''

@app.route('/display_locations')
def display_locations():
    # Display the locations as a list
    return '<br>'.join(str(location) for location in locations)

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/file_upload')
def file_upload():
    return render_template('file_upload.html')

@app.route('/process_file', methods=['POST'])
def process_file():
    # Get the uploaded file
    # uploaded_file = request.files['file']
    # filename = secure_filename(uploaded_file.filename)
    # file_path = os.path.join('test', uploaded_file.filename)
    # uploaded_file.save(file_path)
    
    algorithm = request.form['algorithm']
    file = request.files['file']
    
    file_path = os.path.join('test', file.filename)
    
    # Check if a file was uploaded
    if file.filename == '':
        return render_template("no_file.html")
    
    if is_valid_input_format(file_path):
        # if format is valid, parse the file
        filepath = parse_input_file(file.filename)
        file_path = os.path.join('test', filepath)
    else:
        file_path = os.path.join('test', file.filename)
        with open(file_path, 'r') as f:
            # nodes name
            line = f.readline()
            name = [str(x) for x in line.strip().split(',')]
            size = len(name)
            if size < 8:
                return render_template('file_salah.html')
            
            matrix = []
            for i in range(size):
                line = f.readline()
                row = line.strip().split()
                if len(row) != size:
                    return render_template('file_salah.html')
                # check all elements are non negative
                try:
                    row = [float(element) for element in row]
                    if any(element < 0 for element in row):
                        return render_template('file_salah.html')
                    matrix.append(row)
                except ValueError:
                    return render_template('file_salah.html')
            
            # check if matrix symmetric
            for i in range(size):
                for j in range(i+1, size):
                    if matrix[i][j] != matrix[j][i]:
                        return render_template('file_salah.html')
            
        
                
        # check if matrix symmetric
        for i in range(size):
            for j in range(i+1, size):
                if matrix[i][j] != matrix[j][i]:
                    print("tai4")
                    return render_template('file_salah.html')
    
        filename = secure_filename(file.filename)
        file_path = os.path.join('test', file.filename)
        file.save(file_path)
    session['file_path'] = file_path
    session['algorithm'] = algorithm

    graph = ubahGraf(file_path)
    with open(file_path, 'r') as f:
        # nodes name
        line = f.readline()
        name = [str(x) for x in line.strip().split(',')]

    return render_template('start_node.html', name=name)

@app.route('/exc_node', methods=['POST'])
def exc_node():
    algorithm = request.form['algorithm']
    file_path = request.form['file_path']
    
    graph = ubahGraf(file_path)
    with open(file_path, 'r') as f:
        # nodes name
        line = f.readline()
        name = [str(x) for x in line.strip().split(',')]

    return render_template('start_node.html', algorithm=algorithm, file_path=file_path, name=name)

@app.route('/exc_node2', methods=['POST'])
def exc_node2():
    algorithm = request.form['algorithm']
    file_path = request.form['file_path']
    start = request.form['start']
    name = session['name']
    
    # graph = ubahGraf(file_path)
    # with open(file_path, 'r') as f:
    #     # nodes name
    #     line = f.readline()
    #     name = [str(x) for x in line.strip().split(',')]

    return render_template('goal_node.html', algorithm=algorithm, file_path=file_path, name=name, start=start)

@app.route('/start_node', methods=['POST'])
def start_node():
    algorithm = request.form['algorithm']
    file_path = request.form['file_path']
    start = request.form['start']
    
    if(start == ''):
        return render_template('node_kosong.html', file_path=file_path, algorithm=algorithm)
    
    for i in start:
        if not i.isdigit():
            return render_template('right_number.html', file_path=file_path, algorithm=algorithm)
    
    graph = ubahGraf(file_path)
    with open(file_path, 'r') as f:
        # nodes name
        line = f.readline()
        name = [str(x) for x in line.strip().split(',')]
       
    start_node = int(start)
    session['start'] = start_node
    flag = False
    for index, value in enumerate(name, start=1):
        print(index)
        print(value)
        if index == start_node:
            flag = True
            
    if (not flag):
        return render_template('right_number.html', file_path=file_path, algorithm=algorithm)
    
    name.pop(start_node-1)
    session['name'] = name
    
    return render_template('goal_node.html', name=name)

@app.route('/result', methods=['POST'])
def result():
    algorithm = request.form['algorithm']
    file_path = request.form['file_path']
    start = request.form['start']
    goal = request.form['goal']
    name = session['name']
    
    if(goal == ''):
        return render_template('node_kosong2.html', file_path=file_path, algorithm=algorithm, name=name)
    
    for i in goal:
        if not i.isdigit():
            return render_template('right_number2.html', file_path=file_path, algorithm=algorithm, name=name)
    
    goal = int(goal)
    start_node = int(start)
    flag = False
    for index, value in enumerate(name, start=1):
        if index == goal:
            flag = True
            
    if (not flag):
        return render_template('right_number2.html', file_path=file_path, algorithm=algorithm, name=name)
    
    start_node = start_node - 1
    goal_node = goal - 1
    
    if(goal_node>=start_node):
        goal_node += 1
    
    graph = ubahGraf(file_path)   
    with open(file_path, 'r') as f:
        # nodes name
        line = f.readline()
        name = [str(x) for x in line.strip().split(',')]
    
    # Plot graf awal
    path = []
    imgawal = plot(graph, name, path, "graphawal.png")
    imgGraph = "static/graphawal.png"
    
    
    if algorithm == 'astar':
        astar_iteration, astar_cost, astar_path = astar(graph, start_node, goal_node, name)
        astar_time = timeit(lambda: astar(graph, start_node, goal_node, name), number=1) * 1000
        # output = result("A*", name, start_node, goal_node, astar_iteration, astar_cost, astar_path, astar_time)
        algo = "A*"
        sn = name[start_node]
        en = name[goal_node]
        path = astar_path
        cost = astar_cost
        time = astar_time
        it = astar_iteration
        img = plot(graph, name, astar_path, "astargraph.png")
        imgPath = "static/astargraph.png"
    elif algorithm == 'ucs':
        # the shortest path UCS
        ucs_iteration, ucs_cost, ucs_path = ucs(graph, start_node, goal_node, name)
        ucs_time = timeit(lambda: ucs(graph, start_node, goal_node, name), number=1) * 1000
        # output = result("UCS", name, start_node, goal_node, ucs_iteration, ucs_cost, ucs_path, ucs_time)
        algo = "UCS"
        sn = name[start_node]
        en = name[goal_node]
        path = ucs_path
        cost = ucs_cost
        time = ucs_time
        it = ucs_iteration
        img = plot(graph, name, ucs_path, "ucsgraph.png")
        imgPath = "static/ucsgraph.png"
        
    return render_template('result.html', algo=algo, sn=sn, en=en, path=path, cost=cost, time=time, it=it, imgGraph=imgGraph,imgPath=imgPath)


if __name__ == '__main__':
    app.run(debug=True)
