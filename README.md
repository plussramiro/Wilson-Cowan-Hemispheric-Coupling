# Hemispheric-Specific Coupling Improves Modeling of Functional Connectivity Using Wilson–Cowan Dynamics

This repository contains the source code, simulation data, and analysis tools for the study:

**“Hemispheric-Specific Coupling Improves Modeling of Functional Connectivity Using Wilson–Cowan Dynamics”**

In this work, we extend the classical Wilson–Cowan neural mass model, which traditionally uses a single global coupling parameter **G** [inspired by Abeysuriya et al. [(PLOS Comput Biol, 2018)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006007)], by introducing **two coupling parameters**:  

- **G1** for intra-hemispheric interactions  
- **G2** for inter-hemispheric interactions  

This modification allows us to investigate the role of hemispheric-specific coupling in shaping large-scale brain dynamics and functional connectivity (FC). Using empirical structural connectomes from healthy controls and schizophrenia patients, we show that distinguishing intra- and inter-hemispheric connectivity improves the correspondence between simulated and empirical FC.

---

## 🧠 Dataset

All simulations are based on the dataset from Vohryzek et al. [(Zenodo, 2020)](https://doi.org/10.5281/zenodo.3758534). This dataset contains diffusion and resting-state fMRI data acquired from 27 patients with schizophrenia and 27 demographically matched healthy controls, used to build the group-average structural and functional connectivity matrices analyzed in this work.

---

## 📁 Repository Structure

```
├── run_global.py             # Run simulations with global coupling G
├── run_hemispheric.py        # Run simulations with hemispheric-specific couplings G1 and G2
│
├── model.py                  # Wilson–Cowan model implementation
├── metrics.py                # Correlation, RMSE, and network metrics
├── preprocessing.py          # Data loading and preprocessing utilities
├── plotting.py               # Plotting functions for simulations and analysis
├── utils.py                  # Helper utilities
│
├── analysis.ipynb            # Notebook with post-processing and figure generation
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## 🧪 How to Run the Simulations

### 1. Clone the repository
```bash
git clone https://github.com/ramirop2021/Wilson-Cowan-Hemispheric-Coupling.git
cd Wilson-Cowan-Hemispheric-Coupling
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate.bat       # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the global coupling model
```bash
python run_global.py
```

### 5. Run the hemispheric-specific model
```bash
python run_hemispheric.py
```

> Simulation outputs (time series, envelopes, FC matrices) are automatically stored under `results/`.

---

## 📊 Jupyter Notebook: `analysis.ipynb`

The notebook contains code for **post-processing and reproducing the figures** of the manuscript:

- Structural connectivity (SC) distributions (weights, betweenness, degrees).  
- Comparison between simulated and empirical FC (correlation and RMSE).  
- Heatmaps of correlation across different (G1, G2) values.  
- Global vs. hemispheric coupling results.  

> **Note:** Some of the FC results (`corr` and `dist` plots) are derived from an earlier version of the main scripts.  
> If you run new simulations with the current repository, you only need to adapt the data loading in the plotting section of the notebook.

---

## 🔧 Requirements

This project was tested with **Python 3.11**.  

Main dependencies:
- `numpy`
- `scipy`
- `matplotlib`
- `networkx`
- `numba`
- `pandas`
- `tqdm`
- `jupyter`

All dependencies are listed in `requirements.txt`.

To install:
```bash
pip install -r requirements.txt
```

---

## 📬 Contact

If you have questions or want to contribute, feel free to reach out:

**Ramiro Plüss**  

Email: rpluss@itba.edu.ar

LinkedIn: [https://www.linkedin.com/in/ramiropluss/](https://www.linkedin.com/in/ramiropluss/)

GitHub: [https://github.com/ramirop2021](https://github.com/ramirop2021)  

---

## 📄 Citation

If you use this code or the data provided in this work, please cite the associated research paper:

Ramiro Plüss, Hernán Villota, Patricio Orio.  
"Hemispheric-Specific Coupling Improves Modeling of Functional Connectivity Using Wilson–Cowan Dynamics."  
*arXiv preprint* [arXiv:2506.22951](https://arxiv.org/abs/2506.22951)

---

## 📑 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
