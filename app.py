from flask import Flask, render_template_string, request, jsonify
# Import the logic module (must be in the same directory)
from atomic_logic import create_plotly_json, MAX_ATOMIC_NUMBER, get_element_name

app = Flask(__name__)

# --- HTML Template (Served by Flask) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dynamic 3D Atomic Model (Flask/Plotly)</title>
    <script src="https://cdn.plot.ly/plotly-2.30.0.min.js"></script>
    <style>
        /* --- CSS Styling --- */
        body {
            font-family: Rakena, Selasy;
            margin: 0;
            padding: 0;
            background-color: #151515;
            color: #f5f5f5;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .controls {
            padding: 20px;
            background-color: #232323;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }
        input[type="number"] {
            padding: 10px;
            border: 1px solid #555;
            border-radius: 4px;
            background-color: #333;
            color: #fff;
            width: 80px;
            text-align: center;
            margin-right: 10px;
        }
        button {
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            background-color: #007bff;
            color: white;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        button:hover {
            background-color: #0056b3;
        }
        #plotly-graph {
            width: 90vw;
            max-width: 800px;
            height: 80vh;
            min-height: 600px;
            background-color: #000;
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.7);
        }
        #loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    <h1>Dynamic 3D Atomic Model</h1>
    
    <div class="controls">
        <label for="atomicNumber">Enter Atomic Number (1 to {{ max_z }}):</label>
        <input type="number" id="atomicNumber" value="{{ default_z }}" min="1" max="{{ max_z }}">
        <button onclick="updateModel()">Visualize Element</button>
        <p id="error-message" style="color: red; margin-left: 10px;"></p>
    </div>

    <div id="plotly-graph">
        {{ plot_script | safe }}
        <div id="loading" style="display: none;">Generating Model...</div>
    </div>

    <script>
        const graphDiv = document.getElementById('plotly-graph');
        const loadingDiv = document.getElementById('loading');
        const maxZ = {{ max_z }};
        
        function updateModel() {
            const input = document.getElementById('atomicNumber');
            const z = parseInt(input.value);
            const errorElement = document.getElementById('error-message');

            if (isNaN(z) || z < 1 || z > maxZ) {
                errorElement.textContent = `Please enter a valid number between 1 and ${maxZ}.`;
                return;
            }
            errorElement.textContent = '';
            
            loadingDiv.style.display = 'block'; // Show loading message
            
            // 1. AJAX Request to the Flask API
            fetch('/api/generate/' + z)
                .then(response => response.json())
                .then(data => {
                    loadingDiv.style.display = 'none'; // Hide loading message
                    
                    if (data.error) {
                        errorElement.textContent = data.error;
                        return;
                    }
                    
                    // 2. Plotly.js Redraw
                    const figure = JSON.parse(data.plot_json);

                    // Use Plotly.react for smooth updates
                    Plotly.react('plotly-graph', figure.data, figure.layout);
                })
                .catch(error => {
                    loadingDiv.style.display = 'none';
                    errorElement.textContent = 'Server error during generation.';
                    console.error('Fetch error:', error);
                });
        }
    </script>
</body>
</html>
"""

# --- Flask Routes ---

@app.route('/')
def index():
    """Renders the main page with a default H-atom."""
    default_z = 1
    # Generate the initial Plotly figure's JSON
    plot_json = create_plotly_json(default_z)
    
    # Create the initial script tag to load the graph on the frontend
    initial_plot_script = f"""
        <script>
            document.addEventListener("DOMContentLoaded", function() {{ 
                const figure = JSON.parse('{plot_json}');
                Plotly.newPlot("plotly-graph", figure.data, figure.layout);
            }});
        </script>
    """
    
    return render_template_string(HTML_TEMPLATE, 
                                  max_z=MAX_ATOMIC_NUMBER,
                                  default_z=default_z,
                                  plot_script=initial_plot_script)

@app.route('/api/generate/<int:z>')
def generate_atom(z):
    """API endpoint that receives Z and returns the new Plotly JSON."""
    if z < 1 or z > MAX_ATOMIC_NUMBER:
        return jsonify({'error': f'Atomic number must be between 1 and {MAX_ATOMIC_NUMBER}.'})

    try:
        plot_json = create_plotly_json(z)
        # Flask returns the JSON string generated by the Python logic
        return jsonify({'plot_json': plot_json})
    except Exception as e:
        return jsonify({'error': f'Failed to generate plot: {str(e)}'})

if __name__ == '__main__':
    # This must be the ONLY code that runs the app.
    app.run(debug=True)