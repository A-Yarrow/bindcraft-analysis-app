SETTINGS = {
    'top_metrics': 
    [
    'Average_dSASA',
    'Average_ShapeComplementarity',
    'Average_dG',
    'Average_i_pLDDT',
    'Average_i_pAE',
    'Average_Binder_pLDDT',
    'Average_pLDDT',
    'Average_pAE',
    'Average_pTM',
    'Average_Hotspot_RMSD',
    'Average_PackStat',
    'Average_Relaxed_Clashes',
    'Average_n_InterfaceHbonds',
    ],

    'primary_filters': 
    [
    {
        "label": "Filter dSASA",
        "metric_type": "rosetta_metrics",
        "metric_key": "Average_dSASA",
        "unit": "Å²"
    },
    {
        "label": "Filter Shape Complementarity",
        "metric_type": "rosetta_metrics",
        "metric_key": "Average_ShapeComplementarity",
        "unit": ""
    },
    {
        "label": "Filter dG",
        "metric_type": "rosetta_metrics",
        "metric_key": "Average_dG",
        "unit": "kcal/mol"
    }
    ],

'secondary_flters': 
    [
    {
        "label": "Filter i_pLDDT",
        "metric_type": "af2_metrics",
        "metric_key": "Average_i_pLDDT",
        "unit": ""
    },
    {
        "label": "Filter i_pAE",
        "metric_type": "af2_metrics",
        "metric_key": "Average_i_pAE",
        "unit": ""
    },
    {
        "label": "Filter Binder pLDDT",
        "metric_type": "af2_metrics",
        "metric_key": "Average_Binder_pLDDT",
        "unit": ""
    },
    {
        "label": "Filter pLDDT",
        "metric_type": "af2_metrics",
        "metric_key": "Average_pLDDT",
        "unit": ""
    },
    {
        "label": "Filter pAE",
        "metric_type": "af2_metrics",
        "metric_key": "Average_pAE",
        "unit": ""
    },
    {
        "label": "Filter pTM",
        "metric_type": "af2_metrics",
        "metric_key": "Average_pTM",
        "unit": ""
    }
    ],
    
    'tertiary_filters':
    [
    {    "label": "Filter Hotspot RMSD",
        "metric_type": "rosetta_metrics",
        "metric_key": "Average_Hotspot_RMSD",
        "unit": "Å"
    },
    {
        "label": "Filter PackStat",
        "metric_type": "rosetta_metrics",
        "metric_key": "Average_PackStat",
        "unit": ""
    },
    {
        "label": "Filter Relaxed Clashes",
        "metric_type": "rosetta_metrics",
        "metric_key": "Average_Relaxed_Clashes",
        "unit": ""
    },
    {
        "label": "Filter n Interface H-bonds",
        "metric_type": "rosetta_metrics",
        "metric_key": "Average_n_InterfaceHbonds",
        "unit": ""
    }
    ],
}