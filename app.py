import streamlit as st
import streamlit.components.v1 as components 
import os
import copy
import pandas as pd
from io import StringIO
from utils import *
#load_base_view, get_interface_residues, highlight_interface_residues, parse_final_design_stats, apply_cartoon_style, get_interface_residue_table
from settings import SETTINGS
import json
from pathlib import Path

config_path = Path(__file__).parent / "thresholds.json"
with open(config_path) as f:
    THRESHOLDS = json.load(f)

# settings
DISTANCE_THRESHOLD = 3.5
filters = [
    SETTINGS['primary_filters'],
    SETTINGS['secondary_flters'],
    SETTINGS['tertiary_filters']
    ]

# UI layout
st.sidebar.header("Data")
st.set_page_config(layout="wide", page_title="BindCraft Dashboard (Prototype)")


uploaded_pdb = st.sidebar.file_uploader("Upload PDB", type=["pdb"])
pdb_name = ('-').join(os.path.basename(uploaded_pdb.name).split('_')[0:2]) if uploaded_pdb else None
st.title(f"{pdb_name if pdb_name else ''}")

df_interface = None
if uploaded_pdb:
    pdb_text = uploaded_pdb.read().decode("utf-8")
    pdb_object = StringIO(pdb_text)
    
    # cache raw model
    base_view = load_base_view(pdb_text, show_A=True, show_B=True)


    #UI checkboxes
    show_A = st.checkbox("Show Target (Chain A)", value=True)
    show_B = st.checkbox("Show Binder (Chain B)", value=True)
    show_interface = st.sidebar.checkbox("Highlight Interface Residues", value=False)
    distance = st.sidebar.slider("Interface Distance Threshold (Å)", min_value=2.0, max_value=10.0, value=DISTANCE_THRESHOLD, step=0.5)
    DISTANCE_THRESHOLD = distance 
    
    # Copy cached view before adding highlighting
    view = copy.deepcopy(base_view)

    # Apply cartoon styles based on checkbox selections
    apply_cartoon_style(view, show_A=show_A, show_B=show_B)
    
    # Highlight interface residues if selected
    interface_residues_target, interface_residues_binder = get_interface_residues(pdb_object, distance_threshold=DISTANCE_THRESHOLD)
   
    target_color = st.sidebar.selectbox(
        "Target Residues Color (Chain A)",
        ["limegreen", "red", "orange", "magenta", "yellow", "cyan"],
        index=0
    )

    binder_color = st.sidebar.selectbox(
        "Binder Residues Color (Chain B)",
        ["deepskyblue", "red", "orange", "magenta", "yellow", "cyan"],
        index=0
    )
    updated_view = None
    if show_interface:
        updated_view = highlight_interface_residues(
            view, 
            interface_residues_target, 
            interface_residues_binder,
            target_color=target_color, 
            binder_color=binder_color,
            show_A=show_A, 
            show_B=show_B
        )
        updated_view.zoomTo({})
        df_interface = get_interface_residue_table(interface_residues_target, interface_residues_binder)
        
        # Render the view
        components.html(updated_view._make_html(), height=500, width=900)
    
    else:
        updated_view = view
    
        updated_view.zoomTo({})
    
        # Render the view
        components.html(updated_view._make_html(), height=500, width=900)
    
else:
    st.info("Upload PDB file to visualize")

if df_interface is not None:
    st.subheader("Interface Residues")
    st.dataframe(df_interface)

# Final designs stats upload
final_designs_csv = st.sidebar.file_uploader("Upload final_design_stats.csv", type=["csv"])
if final_designs_csv:
    df = parse_final_design_stats(final_designs_csv)
    df_metrics = get_metrics(df, metric_type='top_metrics')
    if df_metrics.empty:
        st.markdown(
            """
            <div style="background-color:#f8d7da; color:#721c24; padding:10px; border-radius:5px;">
                ❌ No metrics found. Please check the uploaded CSV file.<br>
                Ensure it is labeled final_design_stats.csv.
            </div>
            """,
        unsafe_allow_html=True
        )


    st.subheader("Final Design Stats")
    st.dataframe(df_metrics)
              
    st.subheader("Designs Filtered by Selected Metrics")
    st.sidebar.header("Check Filters to Apply")

    df_metrics_filter = df_metrics.copy()  # start with the full DataFrame
    
    for filter in filters:
        filters = []
        for f in filter:
            # Draw checkbox
            if st.sidebar.checkbox(f["label"], value=False):
                # Draw slider + get cutoff
                cutoff = get_slider_cutoff(f["metric_type"], f["metric_key"])
                # Apply filter
                df_metrics_filter = filter_dataframe_by_cutoff(
                    df=df_metrics_filter,
                    metric_type=f["metric_type"],
                    metric_key=f["metric_key"],
                    cutoff=cutoff,
                )
              
        # Show the filtered dataframe
        if filters:
            st.write(f"Applied Filters: {', '.join(filters)}")
    st.dataframe(df_metrics_filter)

    #df[df['Design'].isin(df_metrics_filter['Design'])]
    st.subheader("Full Stats for Filtered Designs")
    df_metrics_filter_full = df[df['Design'].isin(df_metrics_filter['Design'])]
    st.dataframe(df_metrics_filter_full)
    csv = df_metrics_filter_full.to_csv(index=False).encode("utf-8")

    # Download button
    st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="BindCraft_Filtered_Final_Design_Stats.csv",
    mime="text/csv",
)
    