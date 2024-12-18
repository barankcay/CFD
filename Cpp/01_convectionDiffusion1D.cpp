#include <iostream>
using namespace std;
// Ax=B
int main()
{
    int dimension = 1;      // dimension of the case
    int nCell = 5;          // number of cells
    int nFaces = nCell + 1; // number of faces

    double L = 5;              // m, total length of the rod
    double d[1][nCell] = {0};  // m, length of the cell could be written as L/nCell, but cell sizes can differ
    double k = 100;            // W/mK, conductivity of the rod
    double Ta = 100;           // C, Left dirichlet BC
    double Tb = 200;           // C, Right dirichlet BC
    double area = 0.1;         // m2, area perpendicular to rod's axial length
    double source = 1000;      // W/m3, heat source
    double rho = 1;            // density of the fluid
    double cp = 1000;          // specific heat
    double U[1][nFaces] = {0}; // velocity array

    const double velocity = 0.1; // constant velocity field value. for only diffusion solving, it can be set to 0

    double V[1][nCell] = {0};  // m3, volumes of each cell
    double aL[1][nCell] = {0}; // W/K, cell left face coefficient array
    double aR[1][nCell] = {0}; // W/K, cell right face coefficient array
    double aP[1][nCell] = {0}; // W/K, cell center coefficient array
    double SP[1][nCell] = {0}; // W, source term P
    double SU[1][nCell] = {0}; // W, source term U
    double D[1][nFaces] = {0}; // W/m2K, cell face diffusive flux array
    double F[1][nFaces] = {0}; // W/K, cell face convective flux array
    double A[1][nFaces] = {0}; // m2, cell face array
    double coefficientMatrix[nCell][nCell] = {0};
    double constantMatrix[nCell][1] = {0};
    double unkownMatrix[nCell][1] = {0};

    // coefficient arrays for thomas algorithm. "ta" stands for thomas algorithm
    // malalasekera page 212
    double ta_alpha[1][nCell] = {0};
    double ta_beta[1][nCell] = {0};
    double ta_D[1][nCell] = {0};
    double ta_C[1][nCell] = {0};
    double ta_A[1][nCell] = {0};
    double ta_Cprime[1][nCell] = {0};

    for (int i = 0; i < nFaces; i++) // assigning left and right face cell areas
    {
        A[0][i] = area; // m2
        U[0][i] = velocity;
    }

    for (int i = 0; i < nCell; i++) // assigning cell lengths and volumes
    {
        if (i == 0)
        {
            d[0][i] = L / nCell; // we can assign direct values to length of the nodes
            V[0][i] = d[0][i] * ((A[0][i] + A[0][i + 1]) / 2);
            // average of right and left face area is used to determine area of the cell. since rod has uniform area, usage of only one of thea areas is suitable aswell
            // cout << "Volume of cell= " << V[0][i] << endl;
        }
        else if (i == nCell - 1)
        {
            d[0][i] = L / nCell;
            V[0][i] = d[0][i] * ((A[0][i] + A[0][i + 1]) / 2);
            // cout << "Volume of cell= " << V[0][i] << endl;
        }
        else
        {
            d[0][i] = L / nCell;
            V[0][i] = d[0][i] * ((A[0][i] + A[0][i + 1]) / 2);
            // cout << "Volume of cell= " << V[0][i] << endl;
        }
    }

    for (int i = 0; i < nFaces; i++) // assigning diffusive fluxes to faces
    {
        if (i > 0 && i < nFaces - 1)
        {
            D[0][i] = k / (0.5 * d[0][i - 1] + 0.5 * d[0][i]);
            F[0][i] = rho * cp * U[0][i] * A[0][i];

            // cout << D[0][i] << "\n";
        }
        else if (i == 0)
        {
            D[0][i] = k / d[0][i];
            F[0][i] = rho * cp * U[0][i] * A[0][i];

            // cout << D[0][i] << "\n";
        }

        else
        {
            D[0][i] = k / d[0][i - 1];
            F[0][i] = rho * cp * U[0][i] * A[0][i];
            // cout << D[0][i] << "\n";
        }
    }
    for (int i = 0; i < nCell; i++) // assignin coefficients of cells and creating coefficient matrix, B
    {
        if (i == 0)
        {
            // assignin coefficients of cells
            aL[0][i] = 0;
            aR[0][i] = D[0][i + 1] * A[0][i + 1] - F[0][i + 1] / 2;
            SP[0][i] = -(2 * D[0][i] * A[0][i] + F[0][i]);
            SU[0][i] = Ta * (2 * D[0][i] * A[0][i] + F[0][i]) + source * V[0][i];
            aP[0][i] = aL[0][i] + aR[0][i] + (F[0][i + 1] - F[0][i]) - SP[0][i];

            // creating matrix A and B
            coefficientMatrix[i][i] = aP[0][i];
            coefficientMatrix[i][i + 1] = -aR[0][i];
            constantMatrix[i][0] = SU[0][i];

            // coefficients for thomas algortihm
            ta_alpha[0][i] = -coefficientMatrix[i][i + 1];
            ta_beta[0][i] = 0;
            ta_D[0][i] = coefficientMatrix[i][i];
            ta_C[0][i] = constantMatrix[i][0];
            ta_A[0][i] = ta_alpha[0][i] / (ta_D[0][i]);
            ta_Cprime[0][i] = (ta_C[0][i]) / (ta_D[0][i]);
        }
        else if (i == nCell - 1)
        {
            // assignin coefficients of cells
            aL[0][i] = D[0][i] * A[0][i] + F[0][i] / 2;
            aR[0][i] = 0;
            SP[0][i] = -(2 * D[0][i + 1] * A[0][i + 1] - F[0][i + 1]);
            SU[0][i] = Tb * (2 * D[0][i + 1] * A[0][i + 1] - F[0][i + 1]) + source * V[0][i];
            aP[0][i] = aL[0][i] + aR[0][i] + (F[0][i + 1] - F[0][i]) - SP[0][i];

            // creating matrix A and B
            coefficientMatrix[i][i] = aP[0][i];
            coefficientMatrix[i][i - 1] = -aL[0][i];
            constantMatrix[i][0] = SU[0][i];

            // coefficients for thomas algortihm
            ta_alpha[0][i] = 0;
            ta_beta[0][i] = -coefficientMatrix[i][i - 1];
            ta_D[0][i] = coefficientMatrix[i][i];
            ta_C[0][i] = constantMatrix[i][0];

            ta_A[0][i] = ta_alpha[0][i] / (ta_D[0][i] - ta_beta[0][i] * ta_A[0][i - 1]);
            ta_Cprime[0][i] = (ta_beta[0][i] * ta_Cprime[0][i - 1] + ta_C[0][i]) / (ta_D[0][i] - ta_beta[0][i] * ta_A[0][i - 1]);
        }
        else
        {
            // assignin coefficients of cells
            aL[0][i] = D[0][i] * A[0][i] + F[0][i] / 2;
            aR[0][i] = D[0][i + 1] * A[0][i + 1] - F[0][i + 1] / 2;
            SP[0][i] = 0;
            SU[0][i] = source * V[0][i];
            aP[0][i] = aL[0][i] + aR[0][i] + (F[0][i + 1] - F[0][i]) - SP[0][i];

            // creating matrix A and B
            coefficientMatrix[i][i] = aP[0][i];
            coefficientMatrix[i][i - 1] = -aL[0][i];
            coefficientMatrix[i][i + 1] = -aR[0][i];
            constantMatrix[i][0] = SU[0][i];

            // coefficients for thomas algortihm
            ta_alpha[0][i] = -coefficientMatrix[i][i + 1];
            ta_beta[0][i] = -coefficientMatrix[i][i - 1];
            ta_D[0][i] = coefficientMatrix[i][i];
            ta_C[0][i] = constantMatrix[i][0];

            ta_A[0][i] = ta_alpha[0][i] / (ta_D[0][i] - ta_beta[0][i] * ta_A[0][i - 1]);
            ta_Cprime[0][i] = (ta_beta[0][i] * ta_Cprime[0][i - 1] + ta_C[0][i]) / (ta_D[0][i] - ta_beta[0][i] * ta_A[0][i - 1]);
        }
    }

    // for (int i = 0; i < nCell; i++)
    // {
    //     for (int j = 0; j < nCell; j++)
    //     {
    //         cout << coefficientMatrix[i][j] << " ";
    //     }
    //     cout << endl;
    // }

    // SOLUTION

    for (int i = nCell; i > 0; i--)
    {
        if (i == nCell)
        {
            unkownMatrix[i - 1][0] = ta_Cprime[0][i - 1];
            cout << "T" << i << " is equal to " << unkownMatrix[i - 1][0] << "\n";
        }
        else
        {
            unkownMatrix[i - 1][0] = unkownMatrix[i][0] * ta_A[0][i - 1] + ta_Cprime[0][i - 1];
            cout << "T" << i << " is equal to " << unkownMatrix[i - 1][0] << "\n";
        }
    }

    // cout << ta_Cprime[0][4];

    return 0;
}