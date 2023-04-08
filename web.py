from flask import Flask, render_template, request
from graph import convertToInit
from algorithm import *
import os

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

@app.route('/find_path', methods=['GET','POST'])
def find_path():
    if request.method == 'POST':
        # Retrieve the form data
        uploaded_file = request.form['file_data']
        start_node = request.form['start']
        goal_node = request.form['goal']
        algorithm = request.form['algorithm']
        
        graph = {}
        matrix = []
        nodes = []

        # rest of the code
        convertToInit(uploaded_file, graph, nodes, matrix)
        
        grid = Grid(matrix)
        
        if algorithm == 'UCS':
            result = grid.ucs(start_node, goal_node)
        elif algorithm == 'A*':
            result = grid.astar(start_node, goal_node)    

        # Render the template with the result
        return render_template('result.html', result=result)
    else:
        return render_template('result.html')

@app.route('/process_file', methods=['POST'])
def process_file():
    # Get the uploaded file
    uploaded_file = request.files['file']
    algorithm = request.form['algorithm']
    
    # Render the result to a new HTML page
    return render_template('result.html', file_data=uploaded_file, algorithm=algorithm)

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