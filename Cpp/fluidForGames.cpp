#include <iostream>
#include <vector>

using namespace std;

const int N = 5;

const double length = 20.0;

double h = length / N;

const double dt = 0.100;
const double diff = 10;

vector<vector<double>> u(N + 2, vector<double>(N + 2));
vector<vector<double>> u0(N, vector<double>(N));

vector<vector<double>> v(N + 2, vector<double>(N + 2));
vector<vector<double>> v0(N + 2, vector<double>(N + 2));

vector<vector<double>> dens(N + 2, vector<double>(N + 2));
vector<vector<double>> dens0(N + 2, vector<double>(N + 2));

vector<vector<double>> source(N + 2, vector<double>(N + 2));

void SWAP(vector<vector<double>> &dens, vector<vector<double>> &dens0)
{
    vector<vector<double>> temp(N + 2, vector<double>(N + 2));
    temp = dens;
    dens0 = temp;
}

void createSource(vector<vector<double>> &source)
{
    for (int i = 0; i < N + 2; i++)
    {
        for (int j = 0; j < N + 2; j++)
        {
            source[i][j] = 100.0;
        }
    }
}

void addSource(vector<vector<double>> &source, vector<vector<double>> &dens) // vectors dont need pointers. they will change their values permanently
{
    for (int i = 1; i <= N; i++)
    {
        for (int j = 1; j <= N; j++)
        {
            dens0[i][j] = dens0[i][j] + source[i][j] * dt;
        }
    }
}

void diffuseBad(vector<vector<double>> &dens, vector<vector<double>> &dens0)
{
    double a = diff * dt / (h * h);
    for (int i = 1; i <= N; i++)
    {
        for (int j = 1; j <= N; j++)
        {
            dens[i][j] = dens0[i][j] + a * (dens0[i - 1][j] + dens0[i + 1][j] + dens0[i][j - 1] + dens0[i][j + 1] - 4 * dens0[i][j]);
        }
    }
}

void diffuse(vector<vector<double>> &dens, vector<vector<double>> &dens0)
{
    double a = diff * dt / (h * h);
    for (int k = 0; k < 300; k++)
    {
        for (int i = 1; i <= N; i++)
        {
            for (int j = 1; j <= N; j++)
            {
                dens[i][j] = (dens0[i][j] + a * (dens[i - 1][j] + dens[i + 1][j] + dens[i][j - 1] + dens[i][j + 1] - 4 * dens[i][j])) / (1 + 4 * a);
            }
        }
    }
}

int main()
{
    createSource(source);
    addSource(source, dens);
    for (int t = 0; t < 10; t++)
    {

        for (int i = 0; i < N + 2; i++)
        {
            for (int j = 0; j < N + 2; j++)
            {
                cout << dens0[i][j] << " ";
            }
            cout << "\n";
        }
        diffuse(dens, dens0);
        SWAP(dens, dens0);
        cout << "\n";
        cout << "\n";
    }

    return 0;
}
