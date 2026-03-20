#include <iostream>
using namespace std;

template <typename T, int ROWS, int COLS>
class Matrix
{
private:
    T** matrix;
public:
    // Constructor: allocate dynamic 2D array
    Matrix() {
        matrix = new T*[ROWS];
        for (int i = 0; i < ROWS; i++) {
            matrix[i] = new T[COLS];
            for (int j = 0; j < COLS; j++) matrix[i][j] = 0; // ✅ initialize
        }
    }

    // Getter
    T get(int r, int c) const {
        return matrix[r][c];
    }

    // Setter
    void set(int r, int c, T value) {
        matrix[r][c] = value;
    }

    // Input function
    void allocate() {
        for (int i = 0; i < ROWS; i++) {
            cout << "Enter the elements of row " << i + 1 << " : " << endl;
            for (int j = 0; j < COLS; j++) {
                cin >> matrix[i][j];
            }
        }
    }

    // Print function
    void display() const {
        for (int i = 0; i < ROWS; i++) {
            for (int j = 0; j < COLS; j++) {
                cout << matrix[i][j] << " ";
            }
            cout << endl;
        }
    }

    // Multiplication operator
    template<int OTHER_ROWS, int OTHER_COLS>
    Matrix<T, ROWS, OTHER_COLS> operator*(const Matrix<T, OTHER_ROWS, OTHER_COLS>& m2) {
        
        Matrix<T, ROWS, OTHER_COLS> final;

        if (COLS != OTHER_ROWS) {
            cerr << "Error: Matrix dimensions do not match for multiplication!" << endl;
            return final; // returns empty
        }

        for (int i = 0; i < ROWS; i++) {
            for (int j = 0; j < COLS; j++) {
                for (int h = 0; h < OTHER_COLS; h++) {
                    // ✅ using getter and setter
                    final.set(i, h, final.get(i, h) + (get(i, j) * m2.get(j, h)));
                }
            }
        }

        return final; 
    }

    // Destructor
    ~Matrix() {
        for (int i = 0; i < ROWS; i++) {
            delete[] matrix[i];
        }
        delete[] matrix;
    }
};

// ---------------- DRIVER ------------------
int main() {
    // Example: 2x3 * 3x2 → 2x2 result
    Matrix<int, 2, 3> A;
    Matrix<int, 3, 2> B;

    // Fill A
    // A = [1 2 3]
    //     [4 5 6]
    cout << "Enter elements for Matrix A (2x3):\n";
    A.allocate(); 

    // Fill B
    // B = [7  8]
    //     [9 10]
    //     [11 12]
    cout << "Enter elements for Matrix B (3x2):\n";
    B.allocate();

    cout << "\nMatrix A:\n";
    A.display();

    cout << "\nMatrix B:\n";
    B.display();

    // Multiply
    Matrix<int, 2, 2> C = A * B;

    cout << "\nMatrix C = A * B:\n";
    C.display();

    /*
    Expected result:
    A = [1 2 3]
        [4 5 6]

    B = [ 7  8]
        [ 9 10]
        [11 12]

    C = A*B = 
        [1*7 + 2*9 + 3*11 , 1*8 + 2*10 + 3*12]
        [4*7 + 5*9 + 6*11 , 4*8 + 5*10 + 6*12]

        [ 58,  64 ]
        [139, 154 ]
    */
    return 0;
}
