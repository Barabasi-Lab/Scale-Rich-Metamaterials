# Scale-Rich-Metamaterials

Scale-Rich Metamaterials (SR) are a new class of architected systems that overcome the traditional limitations of periodic or monolithic solids. They exhibit heterogeneity in ligament lengths, thicknesses, and connectivity distributions, generated through the controlled growth of ligaments with prescribed thickness evolution from random nucleation sites.

This repository contains the code used to generate SR architectures and the reference structures (square, hexagonal, kagome, triangular, and Voronoi lattices) described in:

**Scale-Rich Network-Based Metamaterials**   
Csaba Both, Andrew Yen-Jong Chen, Ting-Ting Gao, Niek Mooij, Mohammad Charara, Jayna Wadhwa, Carlos M. Portela, Albert-László Barabási  

### Scale-Rich-Metamaterials generator code
- **Python code for structure generation:**  
[SR - Python](https://github.com/NiekMooij/RDG_networks.git)

- **MATLAB code for structure generation:**  
[SR - MATLAB](https://github.com/Ting-TingGao/SR-Net-generation-matlab.git)


## Repository layout

```
Scale-Rich_system/            Main SR generative model
   ├── SR_code/                  Python package (import target)
   │   ├── Classes.py                geometry primitives (Line, LineSegment, Polygon, Cycle)
   │   ├── generate_line_segments_dynamic_thickness.py   core generator
   │   └── sample_in_polygon.py      point sampling inside polygons
   ├── 2D_SR_samples.ipynb       generate a family of SR samples + export STL
   └── SR_framework_arbitrary_domain.ipynb   generate SR inside an arbitrary domain
Reference_systems/            Reference architectures for comparison
   ├── 2D_REGULAR_LATTICE.ipynb  hexagonal / square / kagome / traingular lattices
   ├── VORONOI_LATTICE.ipynb     Voronoi tessellation 
   └── E_Voronoi_K_foam.ipynb    E-Voronoi and k-nearest foam networks
Sample_files/                 Sample inputs/outputs for FE homogenization
   ├── README_FEA.md             FEM pipeline 
   └── Elastic_Stiffness_Examples/
        ├── input_sample_*.pkl        example input geometries (polygon dictionaries: { ligament_index : [ (x0, y0), (x1, y1), ... ] , ... } ) 
        └── directional_stiffness_*.csv   corresponding directional-stiffness output
```

---

## 1. System requirements

**Operating systems:** macOS (tested on macOS 14), Linux, Windows 10/11.
No non-standard hardware required (standard desktop CPU; no GPU).

**Python:** 3.10 (tested on 3.10.14)

**Packages:** numpy, scipy, shapely, matplotlib, networkx, pandas, numpy-stl, trimesh

Reproducing the elastic-stiffness results additionally requires **Abaqus**
(optional) — see [Sample_files/README_FEA.md](Sample_files/README_FEA.md).

---

## 2. Installation guide

No compilation is required. Clone/copy this folder and install the Python
dependencies into a fresh environment:

```bash
pip install numpy scipy shapely matplotlib networkx pandas numpy-stl trimesh jupyter
```

Typical install time on a normal desktop computer: **2–5 minutes**.

---

## 3. Demo

From `Scale-Rich_system/`, launch Jupyter and run
[2D_SR_samples.ipynb](Scale-Rich_system/2D_SR_samples.ipynb) top to bottom. It
generates SR unit cells, plots the networks, and writes STL files.

Expected run time for a `size = 500` SR system on a normal desktop computer is a few seconds to ~30 seconds.  
Run time grows with `size`, so the full configuration sample sweep takes considerably longer — on the order of tens of minutes.

---

## 4. Instructions for use

Call `generate_line_segments_dynamic_thickness(...)`. Key arguments: x

- `size` — number of ligaments to insert.
- `thickness_arr` — per-ligament thicknesses (length `size`); use a power law
  `lambda_0 * n^(-alpha)` for scale-rich, or a constant list for uniform.
- `angles` — ligament orientations in radians (length `size`).
- `epsilon` — minimum spacing between ligaments.
- `box_size` — edge length of the (square) unit cell.

Returns `segments_dict`, `polygon_arr`, `segment_thickness_dict` (one `Polygon`
per ligament, each with a `.middle_segment`; `v.area()` → ligament area, sum →
relative density), and `generated_config` (the realized `[x, y, theta]` per
ligament, which can be fed back in as `config=` to reproduce the network).

- **Arbitrary domain:** follow
  [SR_framework_arbitrary_domain.ipynb](Scale-Rich_system/SR_framework_arbitrary_domain.ipynb).
- **STL export:** the notebooks union the polygon tiling and write a watertight
  STL via `polygon_to_3d_mesh(...)`; pickle the polygon dictionary to get the
  `input_sample_*.pkl` format used by the FE workflow.
- **Reference systems:** run the notebooks in `Reference_systems/` top to bottom.

