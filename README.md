# Scale-Rich-Metamaterials

Scale-Rich Metamaterials (SR) are a new class of architected systems that overcome the traditional limitations of periodic or monolithic solids. They exhibit heterogeneity in ligament lengths, thicknesses, and connectivity distributions, generated through the controlled growth of ligaments with prescribed thickness evolution from random nucleation sites.

This repository contains the code used to generate SR architectures and the reference structures (square, hexagonal, and Voronoi lattices) described in:

**Scale-Rich Network-Based Metamaterials**   
Csaba Both, Andrew Yen-Jong Chen, Ting-Ting Gao, Niek Mooij, Mohammad Charara, Jayna Wadhwa, Carlos M. Portela, Albert-László Barabási  

### Scale-Rich-Metamaterials generator code
- **Python code for structure generation:**  
[SR - Python](https://github.com/NiekMooij/RDG_networks.git)

- **MATLAB code for structure generation:**  
[SR - MATLAB](https://github.com/Ting-TingGao/SR-Net-generation-matlab.git)

### Scale-Rich-Metamaterials noteboooks
Notebooks that generate SR samples with various parameters and domains. They output STL files and polygon lists (saved as dictionary 
{ ligament_index : [ (x0, y0), (x1, y1), ... ] , ... }).

### Reference systems
Notebooks for generating square, hexagonal, triangular, Kagome, Voronoi and K-nearest foam lattices. They output STL files and polygon lists (saved as dictionary { ligament_index : [ (x0, y0), (x1, y1), ... ] , ... }).

### Sample systems
Example input geometries (polygon dictionaries, .pkl) paired with their directional stiffness outputs (.csv) for Scale-Rich and reference systems. The FEM pipeline is described in the README_FEA.md file. 

