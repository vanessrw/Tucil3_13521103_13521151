from tkinter import Grid
from flask import Flask, render_template, request, url_for
import src
import io
from src.IOFile import *
from src.algorithm import *
from algorithm import *
from timeit import timeit

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/file_upload')
def file_upload():
    return render_template('file_upload.html')

# @app.route('/find_path', methods=['GET','POST'])
# def find_path():
#     if request.method == 'POST':
#         # Retrieve the form data
#         uploaded_file = request.files['file_data']
#         start_node = request.form['start']
#         goal_node = request.form['goal']
#         algorithm = request.form['algorithm']
        
#         graph = {}
#         matrix = []
#         nodes = []

#         # rest of the code
#         convertToInit(uploaded_file, graph, nodes, matrix)
        
#         grid = algorithm(graph, matrix)
        
#         if algorithm == 'UCS':
#             result = grid.ucs(start_node, goal_node)
#         elif algorithm == 'A*':
#             result = grid.astar(start_node, goal_node)    

#         # Render the template with the result
#         return render_template('result.html', result=result)
#     else:
#         return render_template('result.html')

@app.route('/process_file', methods=['POST'])
def process_file():
    # Get the uploaded file
    uploaded_file = request.files['file']
    file_path = os.path.join('test', uploaded_file.filename)
    uploaded_file.save(file_path)

    graph = ubahGraf(file_path)
    with open(file_path, 'r') as f:
        # nodes name
        line = f.readline()
        name = [str(x) for x in line.strip().split(',')]
        
    print(f"INI {len(name)}")
        
    choosen_algorithm = request.form['algorithm']
    start_node = request.form['start']
    goal_node = request.form['goal']
    
    start_node = int(start_node)
    goal_node = int(goal_node)
    
    # Plot graf awal
    path = []
    imgawal = plot(graph, name, path, "graphawal.png")
    imgGraph = "static/graphawal.png"
    
    print(choosen_algorithm)
    
    if choosen_algorithm == 'astar':
        astar_iteration, astar_cost, astar_path = astar(graph, start_node, goal_node, name)
        astar_time = timeit(lambda: astar(graph, start_node, goal_node, name), number=1) * 1000
        result("A*", name, start_node, goal_node, astar_iteration, astar_cost, astar_path, astar_time)
        img = plot(graph, name, astar_path, "astargraph.png")
        imgPath = "static/astargraph.png"
    elif choosen_algorithm == 'ucs':
        # the shortest path UCS
        ucs_iteration, ucs_cost, ucs_path = ucs(graph, start_node, goal_node, name)
        ucs_time = timeit(lambda: ucs(graph, start_node, goal_node, name), number=1) * 1000
        result("UCS", name, start_node, goal_node, ucs_iteration, ucs_cost, ucs_path, ucs_time)
        img = plot(graph, name, ucs_path, "ucsgraph.png")
        imgPath = "static/ucsgraph.png"
    
    # Render the result to a new HTML page
    return render_template('result.html', imgGraph=imgGraph, imgPath=imgPath)


def process_uploaded_file(file):
    # Process the uploaded file as usual
    with io.StringIO(file.stream.read().decode('utf-8')) as f:
        # nodes name
        line = f.readline()
        name = [str(x) for x in line.strip().split(',')]
        size = len(name)
        if size < 8:
            raise ValueError("err: File must contain at least 8 nodes")
            
        # adjacency matrix
        matrix = []
        for i in range(size):
            line = f.readline()
            row = line.strip().split()
            if len(row) != size:
                raise ValueError("err: the adjacency matrix must be rectangular.")
            # check all elements are non negative
            try:
                row = [float(element) for element in row]
                if any(element < 0 for element in row):
                    raise ValueError("err: elements must be non-negative integers")
                matrix.append(row)
            except ValueError:
                raise ValueError("err: elements must be integers")
                
        # check if matrix symmetric
        for i in range(size):
            for j in range(i+1, size):
                if matrix[i][j] != matrix[j][i]:
                    raise ValueError("The adjacency matrix is not symmetric.")
            
        return name, matrix

def process_text_file(content):
    # Process the text file
    with io.StringIO(content) as f:
        # nodes name
        line = f.readline()
        name = [str(x) for x in line.strip().split(',')]
        size = len(name)
        if size < 8:
            raise ValueError("err: File must contain at least 8 nodes")
            
        # adjacency matrix
        matrix = []
        for i in range(size):
            line = f.readline()
            row = line.strip().split()
            if len(row) != size:
                raise ValueError("err: the adjacency matrix must be rectangular.")
            # check all elements are non negative
            try:
                row = [float(element) for element in row]
                if any(element < 0 for element in row):
                    raise ValueError("err: elements must be non-negative integers")
                matrix.append(row)
            except ValueError:
                raise ValueError("err: elements must be integers")
                
        # check if matrix symmetric
        for i in range(size):
            for j in range(i+1, size):
                if matrix[i][j] != matrix[j][i]:
                    raise ValueError("The adjacency matrix is not symmetric")


if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, render_template, request
# import networkx as nx

# app = Flask(__name__)

# # function to convert adjacency matrix to graph
# def adjacency_matrix_to_graph(matrix):
#     G = nx.Graph()
#     for i, row in enumerate(matrix):
#         for j, weight in enumerate(row):
#             if weight != 0:
#                 G.add_edge(i+1, j+1, weight=weight)
#     return G

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            matrix = []
            for line in file:
                row = list(map(int, line.strip().split()))
                matrix.append(row)
            G = adjacency_matrix_to_graph(matrix)
            return render_template('result.html', graph=G)
    return render_template('home.html')

# if __name__ == '__main__':
#     app.run(debug=True)