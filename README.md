DYNAMIC ATOMIC STRUCTURE VISUALIZER



OVERVIEW

  This project is a full-stack web application that creates dynamic, rotatable 3D visualizations of all 118 elements in the Periodic Table. It uses a Python Flask server to accurately model electron configurations based on the Aufbau principle across multiple orbital planes. Plotly generates the interactive 3D graph, which is asynchronously updated via AJAX communication with the browser. The result is an accessible, powerful tool for exploring complex atomic structure through immersive 3D interaction.

FEATURES

1. 🌐 Full Periodic Table Coverage
Universal Modeling: The application can generate the structure for all 118 known elements ($Z=1$ to $Z=118$).
Dynamic Input: Users interactively input the Atomic Number ($Z$) via a web interface, and the model instantly updates.
2. ⚛️ Advanced Scientific Accuracy
Quantum Rules: Electron placement is determined by strictly adhering to the Aufbau principle and Madelung's rule, correctly filling energy subshells (s, p, d, f) rather than relying on the simplistic Bohr model
Multi-Planar Orbits: Electrons are visualized across multiple orbital planes (X-Y, Y-Z, X-Z), accurately representing the complexity of $p$, $d$, and $f$ orbitals in 3D space.
3. 🖥️ Interactive 3D Visualization
Real-Time Rendering: Uses the Plotly visualization engine to generate lightweight, interactive 3D scatter plots.
Mouse Interaction: The model is fully navigable, allowing users to rotate, zoom, and pan the atomic structure to observe complex electron layers from any angle.
Element Labeling: The nucleus is clearly labeled with the current Atomic Number ($Z$) and the corresponding Element Name.
4. ⚙️ Robust Full-Stack Architecture
Server-Side Calculation: The computationally heavy physics logic is handled efficiently by the Python Flask server.
Asynchronous Updates: Communication between the browser (JavaScript) and the server (Flask) uses AJAX, ensuring the model updates dynamically without requiring a full page reload.
Clean Separation of Concerns: The project maintains a clean separation between the scientific logic (atomic_logic.py) and the web server (app.py).

Technologies/ Tools Used

1. Backend Server: Python Flask is the web micro-framework used to create the server, handle user requests, and manage API routing.
2. Scientific Logic: Custom Python Logic implements the Aufbau Principle and Madelung's rule to accurately model electron configurations and positions.
3. Visualization Engine: The Plotly library is used to transform the complex 3D coordinates (derived from the subshell filling rules) into an embeddable, interactive graphical format.
4. Frontend Interaction: HTML, CSS, and JavaScript provide the user interface. AJAX communication handles the dynamic update, sending the requested Atomic Number ($Z$) to the Flask server and instantly redrawing the 3D model in the browser.
5. Development Environment: Conda/Virtual Environment is used to manage dependencies (Flask, Plotly) and ensure the project runs consistently.

STEPS TO INSTALL AND RUN THE PROJECT


1. 💾 Project Setup
Ensure you have the following two Python files in your project directory: app.py (Flask server) and atomic_logic.py (Scientific logic).

2. 🛠️ Install Dependencies
Open your terminal and use pip to install the required server and visualization libraries:

        pip install Flask plotly
   
4. 🚀 Run the Flask Server
In your terminal, set the application environment variable:

        export FLASK_APP=app.py
  Start the server using the dedicated command:

      python app.py
(The terminal will show: * Running on http://127.0.0.1:5000)

4. 🌐 Access and Interact
Open your web browser and navigate to the address: http://127.0.0.1:5000.

Enter an Atomic Number (1-118) and click "Visualize Element" to dynamically update the rotatable 3D model.
