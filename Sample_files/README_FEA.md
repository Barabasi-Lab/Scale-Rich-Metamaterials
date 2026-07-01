# Finite-element homogenization of Scale-Rich structures

This script takes a generated SR geometry and computes its effective 2D
elasticity (stiffness) tensor **C** by finite-element analysis in Abaqus.

## Input

The input is a single pickle file containing a **dictionary of polygons**:

```
{ ligament_index : [ (x0, y0), (x1, y1), ... ] , ... }
```

Each key is a ligament index (its order of insertion during generation), and
each value is the list of `(x, y)` vertices that trace that ligament's outline.
Together the polygons tile the full unit cell.

## Structure generation

The model is built directly from the polygon dictionary:

1. Each polygon is drawn as a closed sketch and turned into a 2D planar
   deformable shell part.
2. All parts are merged with a Boolean union into a single part (`union`), so
   overlapping ligaments fuse into one continuous solid.
3. The bounding box of the union defines the outer edges (`left`, `right`,
   `top`, `bottom`) used later for boundary conditions.

The material is linear elastic with Poisson ratio `nu = 0.35`. 
The elastic modulus is arbitrary and directional stiffness results are normalized by this value.
The analysis is 2D **plane strain** with unit out-of-plane thickness.

## Element type

The geometry is meshed with **quadratic plane-strain triangles**: `CPE6`
(6-node) with `CPE8R` (8-node reduced) where quadrilaterals form. Quadratic
elements are used so that thin, curved ligaments are resolved with few elements
across their width. The mesh is unstructured (`TRI` controls) with a global
seed size.

## Boundary conditions: three unit-strain load cases

To extract the stiffness tensor, the structure is loaded three times under
small strain (linear, `nlgeom=OFF`).
Each case corresponds to imposing one state of the macroscopic average strain,
(i) uniaxial compression in x; (ii) uniaxial compression in y; (iii) simple shear.

Because of the lack of periodicity, affine boundary conditions are applied by prescribing
displacement boundary conditions.

## Output tensor C

For each load case the script reads the last-increment field output (stress
`S`, element volume `EVOL`) and computes the **volume-averaged
macroscopic stress**:

```
sigma_bar = sum(sigma_e * V_e) / sum(V_e)
```

The effective stiffness **C** relates volume-average macroscopic stress to 
volume-averaged macroscopic strain in Voigt notation:

```
[ sigma_11 ]   [ C11  C12  C13 ] [ eps_11 ]
[ sigma_22 ] = [ C12  C22  C23 ] [ eps_22 ]
[ sigma_12 ]   [ C13  C23  C33 ] [ eps_12 ]
```

Stacking the three averaged stress vectors as columns of a matrix `Sigma` and
the three strain vectors as columns of `Eps`, the tensor is obtained by solving
`Sigma = C * Eps`:

```
C = Sigma @ inv(Eps)
```

C is the homogenized in-plane stiffness of the architecture. It can be used to 
compute the directional stiffness, Ed in a given direction e_d = [cos(theta), sin(theta)]
by using the Voigt notation:

Let n_d = [cos^2(theta), sin^2(theta), cos(theta)*sin(theta)].
Then 1/Ed = (n_d)^T C^(-1) n_d.