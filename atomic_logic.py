import plotly.graph_objects as go
import math
import json # Ensure json is imported for string conversions if needed

# --- Configuration & Constants ---
R_NUCLEUS = 0.5
R_ELECTRON = 0.1
MAX_ATOMIC_NUMBER = 118

# Define Subshells (The core physics logic)
SUBSHELL_DATA = [
    [1, 0, 2, 3.0, 'XY'], [2, 0, 2, 4.0, 'XY'], [2, 1, 6, 5.0, 'YZ'], [3, 0, 2, 6.0, 'XZ'], 
    [3, 1, 6, 7.0, 'XY'], [4, 0, 2, 8.0, 'YZ'], [3, 2, 10, 8.5, 'XZ'], [4, 1, 6, 9.0, 'XY'], 
    [5, 0, 2, 10.0, 'YZ'], [4, 2, 10, 10.5, 'XY'], [5, 1, 6, 11.0, 'XZ'], [6, 0, 2, 12.0, 'XY'], 
    [4, 3, 14, 12.5, 'YZ'], [5, 2, 10, 13.0, 'XZ'], [6, 1, 6, 13.5, 'XY'], [7, 0, 2, 14.0, 'YZ'], 
    [5, 3, 14, 14.5, 'XZ'], [6, 2, 10, 15.0, 'XY'], [7, 1, 6, 15.5, 'YZ']
]

ELEMENT_NAMES = {
    1:'Hydrogen', 2:'Helium', 3:'Lithium', 4:'Beryllium', 5:'Boron', 6:'Carbon', 7:'Nitrogen', 8:'Oxygen', 9:'Fluorine', 10:'Neon',
    11:'Sodium', 12:'Magnesium', 13:'Aluminum', 14:'Silicon', 15:'Phosphorus', 16:'Sulfur', 17:'Chlorine', 18:'Argon', 19:'Potassium', 20:'Calcium',
    21:'Scandium', 22:'Titanium', 23:'Vanadium', 24:'Chromium', 25:'Manganese', 26:'Iron', 27:'Cobalt', 28:'Nickel', 29:'Copper', 30:'Zinc',
    31:'Gallium', 32:'Germanium', 33:'Arsenic', 34:'Selenium', 35:'Bromine', 36:'Krypton', 37:'Rubidium', 38:'Strontium', 39:'Yttrium', 40:'Zirconium',
    41:'Niobium', 42:'Molybdenum', 43:'Technetium', 44:'Ruthenium', 45:'Rhodium', 46:'Palladium', 47:'Silver', 48:'Cadmium', 49:'Indium', 50:'Tin',
    51:'Antimony', 52:'Tellurium', 53:'Iodine', 54:'Xenon', 55:'Cesium', 56:'Barium', 57:'Lanthanum', 58:'Cerium', 59:'Praseodymium', 60:'Neodymium',
    61:'Promethium', 62:'Samarium', 63:'Europium', 64:'Gadolinium', 65:'Terbium', 66:'Dysprosium', 67:'Holmium', 68:'Erbium', 69:'Thulium', 70:'Ytterbium',
    71:'Lutetium', 72:'Hafnium', 73:'Tantalum', 74:'Tungsten', 75:'Rhenium', 76:'Osmium', 77:'Iridium', 78:'Platinum', 79:'Gold', 80:'Mercury',
    81:'Thallium', 82:'Lead', 83:'Bismuth', 84:'Polonium', 85:'Astatine', 86:'Radon', 87:'Francium', 88:'Radium', 89:'Actinium', 90:'Thorium',
    91:'Protactinium', 92:'Uranium', 93:'Neptunium', 94:'Plutonium', 95:'Americium', 96:'Curium', 97:'Berkelium', 98:'Californium', 99:'Einsteinium', 100:'Fermium',
    101:'Mendelevium', 102:'Nobelium', 103:'Lawrencium', 104:'Rutherfordium', 105:'Dubnium', 106:'Seaborgium', 107:'Bohrium', 108:'Hassium', 109:'Meitnerium', 110:'Darmstadtium',
    111:'Roentgenium', 112:'Copernicium', 113:'Nihonium', 114:'Flerovium', 115:'Moscovium', 116:'Livermorium', 117:'Tennessine', 118:'Oganesson'
}

# --- Helper Functions ---
def get_plane_matrix(plane_str):
    if plane_str == 'YZ':
        return [[0, 0, 1], [0, 1, 0], [-1, 0, 0]]
    elif plane_str == 'XZ':
        return [[1, 0, 0], [0, 0, -1], [0, 1, 0]]
    else:
        return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

def apply_rotation(x, y, z, matrix):
    x_new = x * matrix[0][0] + y * matrix[0][1] + z * matrix[0][2]
    y_new = x * matrix[1][0] + y * matrix[1][1] + z * matrix[1][2]
    z_new = x * matrix[2][0] + y * matrix[2][1] + z * matrix[2][2]
    return x_new, y_new, z_new

def get_element_name(atomic_number):
    return ELEMENT_NAMES.get(atomic_number, f"Z={atomic_number} (Unknown)")

# --- Core Plotly Generation Function ---

def generate_atom_data(num_electrons):
    """
    Generates lists of X, Y, Z coordinates for electrons and shells.
    """
    electron_x, electron_y, electron_z = [0], [0], [0]
    shell_traces = []
    
    electron_count = 0
    shell_color_map = {1:'cyan', 2:'magenta', 3:'yellow', 4:'green', 5:'blue', 6:'orange', 7:'purple'}
    
    for n, l, capacity, radius, plane_str in SUBSHELL_DATA:
        if electron_count >= num_electrons:
            break

        electrons_needed = num_electrons - electron_count
        electrons_on_subshell = min(capacity, electrons_needed)
        
        if electrons_on_subshell == 0:
            continue

        rotation_matrix = get_plane_matrix(plane_str)
        
        # --- Shell Visualization (Draw a Ring) ---
        shell_x_points, shell_y_points, shell_z_points = [], [], []
        for i in range(51):
            angle = i * (2 * math.pi / 50)
            x_base = radius * math.cos(angle)
            y_base = radius * math.sin(angle)
            z_base = 0
            x_final, y_final, z_final = apply_rotation(x_base, y_base, z_base, rotation_matrix)
            shell_x_points.append(x_final)
            shell_y_points.append(y_final)
            shell_z_points.append(z_final)

        shell_traces.append(go.Scatter3d(
            x=shell_x_points, y=shell_y_points, z=shell_z_points,
            mode='lines',
            line=dict(color=shell_color_map.get(n, 'white'), width=2),
            opacity=0.5,
            name=f'Shell {n}{["s","p","d","f"][l]}',
            hoverinfo='none'
        ))

        # --- Electron Placement ---
        angle_increment = 2 * math.pi / electrons_on_subshell
        
        for j in range(electrons_on_subshell):
            angle = j * angle_increment
            x_base = radius * math.cos(angle)
            y_base = radius * math.sin(angle)
            z_base = 0
            x_final, y_final, z_final = apply_rotation(x_base, y_base, z_base, rotation_matrix)
            
            electron_x.append(x_final)
            electron_y.append(y_final)
            electron_z.append(z_final)
            
        electron_count += electrons_on_subshell
            
    return electron_x, electron_y, electron_z, shell_traces

def create_plotly_json(num_electrons):
    """
    Creates the Plotly figure and returns its JSON representation.
    """
    if num_electrons < 1 or num_electrons > MAX_ATOMIC_NUMBER:
        return {}
        
    x_data, y_data, z_data, shell_traces = generate_atom_data(num_electrons)
    element_name = get_element_name(num_electrons)

    # 1. Nucleus and Electrons (Scatter plot)
    electron_trace = go.Scatter3d(
        x=x_data, y=y_data, z=z_data,
        mode='markers',
        marker=dict(
            # Scaling size for better visualization
            size=[20 * R_NUCLEUS] + [10 * R_ELECTRON] * (len(x_data) - 1), 
            color=['red'] + ['blue'] * (len(x_data) - 1),
            opacity=1.0,
            symbol='circle'
        ),
        name=f'{element_name} (Z={num_electrons})',
        hoverinfo='text',
        text=[f'Nucleus<br>Protons: {num_electrons}'] + ['Electron'] * (len(x_data) - 1)
    )

    # 2. Layout Configuration
    atom_radius = SUBSHELL_DATA[-1][3] + 1.0
    layout = go.Layout(
        scene=dict(
            xaxis=dict(visible=False, range=[-atom_radius, atom_radius]),
            yaxis=dict(visible=False, range=[-atom_radius, atom_radius]),
            zaxis=dict(visible=False, range=[-atom_radius, atom_radius]),
            aspectmode='cube',
            bgcolor='rgb(0,0,0)'
        ),
        title=f'{element_name} (Z={num_electrons}) Atomic Model',
        font=dict(color='white'),
        showlegend=False,
        margin=dict(l=0, r=0, b=0, t=30),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    fig = go.Figure(data=[electron_trace] + shell_traces, layout=layout)
    
    # Use to_json() to send the plot structure to the frontend
    return fig.to_json()