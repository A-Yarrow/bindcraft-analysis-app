import py3Dmol
from Bio.PDB import PDBParser
from io import StringIO
import pandas as pd
import streamlit as st
import json
from pathlib import Path

from settings import SETTINGS

config_path = Path(__file__).parent / "thresholds.json"
with open(config_path) as f:
    THRESHOLDS = json.load(f)

@st.cache_resource(show_spinner="Loading PDB...")
def load_base_view(pdb_text: str, show_A=True, show_B=True)->py3Dmol.view:
    """Load PDB into a py3Dmol view with base cartoon styles only."""
    view = py3Dmol.view(width=800, height=400)
    view.addModel(pdb_text, 'pdb')
    view.setStyle({}, {}) #Remove default wireframe
    view.setBackgroundColor('0x303030')  # dark gray background
    view.zoomTo()
    return view

def apply_cartoon_style(view, show_A=True, show_B=True):
    """Apply cartoon styles based on checkbox selections."""
    if show_A:
        view.setStyle({"chain": "A"}, {'cartoon': {'color': 'limegreen'}}) 
    if show_B:
        view.setStyle({"chain": "B"}, {'cartoon': {'color': 'deepskyblue'}}) 

    view.zoomTo()
    view.setViewStyle({'style':'orthographic', 'center':[0,0,0]})


def highlight_interface_residues(view, target_residues, binder_residues,
                                  show_A=True, show_B=True,
                                  target_color="limegreen", binder_color="deepskyblue"):
    
    backbone_atoms = ["N", "O"]  # atoms to skip
    
    if show_A:
        for chain, resi in target_residues:
            selection = {"chain": chain, "resi": str(resi), "not": {"atom": backbone_atoms}}
            view.addStyle(selection, {"stick": {"radius": 0.25, "colorscheme": "element"}})
            view.addStyle(selection, {"sphere": {"scale": 0.30, "colorscheme": "element"}})
            carbon_selection = {"chain": chain, "resi": str(resi), "elem": "C"}
            view.addStyle(carbon_selection, {"stick": {"color": target_color, "radius": 0.25},
                                            "sphere": {"color": target_color, "radius": 0.30}
                                            })
    
    if show_B:
        for chain, resi in binder_residues:
            selection = {"chain": chain, "resi": str(resi), "not": {"atom": backbone_atoms}}
            view.addStyle(selection, {"stick": {"radius": 0.25, "colorscheme": "element"}})
            view.addStyle(selection, {"sphere": {"scale": 0.30, "colorscheme": "element"}})
            carbon_selection = {"chain": chain, "resi": str(resi), "elem": "C"}
            view.addStyle(carbon_selection, {"stick": {"color": binder_color, "radius": 0.25,}, 
                                         "sphere": {"color": binder_color, "radius": 0.30}
                                         })
    
    view.setViewStyle({'style':'orthographic', 'center':[0,0,0]})
    view.zoomTo()
    return view

@st.cache_data(show_spinner="Calculating interface residues...")
def get_interface_residues(pdb_file, distance_threshold=3.5)->tuple[set, set]:
    """
    Inputs:
    pdb_file: file-like object containing the PDB structure of the protein complex
    distance_threshold: distance in Å to consider residues as part of the interface
    
    Returns:
    Tuple of two sets:
        - binder residues: set of ('A', resnum)
        - target residues: set of ('B', resnum)
    """
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure('complex', pdb_file)

    model = structure[0]
    Target = model['A']
    Binder = model['B']

    interface_residues_target = set()
    interface_residues_binder = set()
    

    for residueA in Target:
        if residueA.id[0] != ' ':  # Skip hetero residues
            continue
        for atomA in residueA:
            for residueB in Binder:
                if residueB.id[0] != ' ':  # Skip hetero residues
                    continue
                for atomB in residueB:
                    distance = atomA - atomB # Euclidean distance in Å
                    if distance < distance_threshold:
                        interface_residues_target.add(('A', residueA.id[1]))
                        interface_residues_binder.add(('B', residueB.id[1]))

    return interface_residues_target, interface_residues_binder

def get_interface_residue_table(interface_residues_target, interface_residues_binder):
    """Display interface residues in a table format."""
    import pandas as pd

    target_residues = [res for _, res in sorted(interface_residues_target)]
    binder_residues = [res for _, res in sorted(interface_residues_binder)]

    # Pad shorter list with None
    max_len = max(len(target_residues), len(binder_residues))
    target_residues += [None] * (max_len - len(target_residues))
    binder_residues += [None] * (max_len - len(binder_residues))

    df_interface = pd.DataFrame({
        "Target Residues (Chain A)": target_residues,
        "Binder Residues (Chain B)": binder_residues
    })
    
    df_interface['Target Residues (Chain A)'] = df_interface['Target Residues (Chain A)'].astype('Int64')
    df_interface['Binder Residues (Chain B)'] = df_interface['Binder Residues (Chain B)'].astype('Int64')
    
    return df_interface



def parse_final_design_stats(results_file):
    """
    Parses a results file containing scoring metrics.
    
    Args:
        results_file: file-like object containing the results data.
        
    Returns:

        A pandas DataFrame with the parsed data.
    """
    df = pd.read_csv(results_file)
    df = df.dropna(axis=1, how='all')
    return df

def get_metrics(df:pd.DataFrame, metric_type:str) -> pd.DataFrame:
    metrics = SETTINGS[metric_type]
    df = df[['Rank', 'Design'] + metrics ]
    return df



# utils.py

import streamlit as st

def get_slider_cutoff(metric_type: str, metric_key: str) -> float:
    """
    Display a sidebar slider for a metric and return the selected cutoff.

    Args:
        metric_type (str): Type of metric, e.g., 'rosetta_metrics' or 'af2_metrics'.
        metric_key (str): Key from THRESHOLDS, e.g., 'Average_dSASA'.

    Returns:
        float: User-selected cutoff value from slider.
    """
    params = THRESHOLDS[metric_type][metric_key]
    cutoff = st.sidebar.slider(
        f"Filter {metric_key}",
        min_value=float(params['min']),
        max_value=float(params['max']),
        value=float(params['thresh']),
        step=float(params['step'])
    )
    return cutoff

def filter_dataframe_by_cutoff(df, metric_type:str, metric_key:str, cutoff: float):
    """
    Filter a DataFrame based on a cutoff value for a given metric.

    Args:
        df (pd.DataFrame): Input metrics DataFrame.
        metric_type (str): Type of metric, e.g., 'rosetta_metrics' or 'af2_metrics'.
        metric_key (str): Column name to filter on.
        cutoff (float): Cutoff value to apply.
        greater_equal (bool): If True, filter df[metric_key] >= cutoff; else <= cutoff.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    params = THRESHOLDS[metric_type][metric_key]
    if params['>=']:
        return df[df[metric_key] >= cutoff]
    else:
        return df[df[metric_key] <= cutoff]

