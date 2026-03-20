#include<iostream>
using namespace std;

struct Node {
    char data;
    Node* next;
};

class Stack {
private:
    Node* head;

public:
    Stack() : head(nullptr) {}

    void Push(char var) {
        Node* temp = new Node;
        temp->data = var;
        temp->next = head;
        head = temp;
    }

    char Pop() {
        if (head == nullptr) {
            cout << "Stack empty\n";
            return '\0';
        }
        char val = head->data;
        Node* temp = head;
        head = head->next;
        delete temp;
        return val;
    }

    char Top() {
        if (head != nullptr)
            return head->data;
        return '\0';
    }

    bool isEmpty() {
        return head == nullptr;
    }
};

int precedence(char op) {
    if (op == '^') return 3;
    if (op == '*' || op == '/') return 2;
    if (op == '+' || op == '-') return 1;
    return -1;
}

bool isOperand(char x) {
    return !(x == '+' || x == '-' || x == '*' || x == '/' || x == '^' || x == '(' || x == ')');
}

bool checkPrecedence(char a, char b) {
    int p1 = precedence(a);
    int p2 = precedence(b);
    if (p1 > p2) return true;
    if (p1 < p2) return false;
    if (p1 == p2) {
        if (a == '^') return false; // right associative
        else return true;           // left associative
    }
    return false;
}

string InfixToPostfix(string expression, Stack& stk) {
    string result = "";
    for (int i = 0; i < expression.length(); i++) {
        char symb = expression[i];

        if (isOperand(symb)) {
            result += symb;
        }
        else if (symb == '(') {
            stk.Push(symb);
        }
        else if (symb == ')') {
            while (!stk.isEmpty() && stk.Top() != '(') {
                result += stk.Pop();
            }
            if (!stk.isEmpty()) stk.Pop(); // pop '('
        }
        else {
            while (!stk.isEmpty() && checkPrecedence(stk.Top(), symb)) {
                result += stk.Pop();
            }
            stk.Push(symb);
        }
    }

    while (!stk.isEmpty()) {
        result += stk.Pop();
    }

    return result;
}

int main() {
    Stack s;
    string exp = "A+B*C";
    cout << "Postfix: " << InfixToPostfix(exp, s) << endl;
}
