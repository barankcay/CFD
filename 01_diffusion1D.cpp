#include <iostream>
using namespace std;

int main()
{
    int dimension = 1;      // dimension of the case
    int nCell = 5;          // number of cells
    int nFaces = nCell + 1; // number of faces

    double L = 5;       // m, total length of the rod
    double d[1][nCell]; // m, length of the cell could be written as L/nCell, but cell sizes can differ
    double k = 100;     // W/mK, conductivity of the rod
    double Ta = 100;    // C, Left dirichlet BC
    double Tb = 200;    // C, Right dirichlet BC
    double area = 0.1;  // m2, area perpendicular to rod's axial length

    double aL[1][nCell]; // cell left face coefficient array
    double aR[1][nCell]; // cell right face coefficient array
    double aP[1][nCell]; // cell center coefficient array
    double SP[1][nCell]; // source term P
    double SU[1][nCell]; // source term U
    double D[1][nFaces]; // W/m2K, cell face diffusive flux array
    double A[1][nFaces]; // m2, cell face array

    for (int i = 0; i < nCell; i++)
    {
        d[1][i] = L / nCell;
    }

    return 0;
}