/**
 * ==============================================================================
 * Stack & Circular Queue CLI Console Program in C++
 * Standard Menu-Driven Interactive Program for Command Prompt / Terminal
 * ==============================================================================
 */

#include <iostream>
#include <string>
#include <iomanip>

using namespace std;

// ------------------------------------------------------------------------------
// STACK IMPLEMENTATION (LIFO)
// ------------------------------------------------------------------------------
class Stack {
private:
    int top;
    int capacity;
    int* arr;

public:
    Stack(int cap = 6) {
        capacity = cap;
        arr = new int[capacity];
        top = -1;
    }

    ~Stack() {
        delete[] arr;
    }

    bool isFull() const {
        return top == capacity - 1;
    }

    bool isEmpty() const {
        return top == -1;
    }

    void push(int val) {
        if (isFull()) {
            cout << "\n[!] STACK OVERFLOW! Stack capacity (" << capacity << ") reached.\n";
            return;
        }
        top++;
        arr[top] = val;
        cout << "\n[+] Successfully pushed " << val << " at index [" << top << "].\n";
    }

    int pop() {
        if (isEmpty()) {
            cout << "\n[!] STACK UNDERFLOW! Stack is empty.\n";
            return -1;
        }
        int val = arr[top];
        top--;
        cout << "\n[-] Successfully popped " << val << ". New top index is " << top << ".\n";
        return val;
    }

    void peek() const {
        if (isEmpty()) {
            cout << "\n[!] Stack is empty (top = -1).\n";
            return;
        }
        cout << "\n[*] Top element is " << arr[top] << " at index [" << top << "].\n";
    }

    void display() const {
        cout << "\n--- Current Stack (Capacity: " << (top + 1) << "/" << capacity << ") ---\n";
        if (isEmpty()) {
            cout << "  [Empty Stack]\n";
            return;
        }
        for (int i = capacity - 1; i >= 0; i--) {
            if (i <= top) {
                cout << "  [" << i << "] | " << setw(6) << arr[i] << " |";
                if (i == top) cout << " <-- TOP";
                cout << "\n";
            } else {
                cout << "  [" << i << "] | (empty) |\n";
            }
        }
        cout << "      +---------+\n";
    }
};

// ------------------------------------------------------------------------------
// CIRCULAR QUEUE IMPLEMENTATION (FIFO Ring Buffer)
// ------------------------------------------------------------------------------
class CircularQueue {
private:
    int front, rear, size, capacity;
    int* arr;

public:
    CircularQueue(int cap = 6) {
        capacity = cap;
        arr = new int[capacity];
        front = -1;
        rear = -1;
        size = 0;
    }

    ~CircularQueue() {
        delete[] arr;
    }

    bool isFull() const {
        return size == capacity;
    }

    bool isEmpty() const {
        return size == 0;
    }

    void enqueue(int val) {
        if (isFull()) {
            cout << "\n[!] QUEUE OVERFLOW! Formula: (rear + 1) % " << capacity 
                 << " == front (" << front << "). Queue is full.\n";
            return;
        }
        if (isEmpty()) {
            front = 0;
            rear = 0;
        } else {
            rear = (rear + 1) % capacity;
        }
        arr[rear] = val;
        size++;
        cout << "\n[+] Enqueued " << val << " at index [" << rear 
             << "]. (Front: " << front << ", Rear: " << rear << ", Size: " << size << "/" << capacity << ")\n";
    }

    int dequeue() {
        if (isEmpty()) {
            cout << "\n[!] QUEUE UNDERFLOW! Queue is empty.\n";
            return -1;
        }
        int val = arr[front];
        if (front == rear) {
            front = -1;
            rear = -1;
        } else {
            front = (front + 1) % capacity;
        }
        size--;
        cout << "\n[-] Dequeued " << val << ". (New Front: " << front 
             << ", Rear: " << rear << ", Size: " << size << "/" << capacity << ")\n";
        return val;
    }

    void peekFront() const {
        if (isEmpty()) {
            cout << "\n[!] Queue is empty.\n";
            return;
        }
        cout << "\n[*] Front element is " << arr[front] << " at index [" << front << "].\n";
    }

    void peekRear() const {
        if (isEmpty()) {
            cout << "\n[!] Queue is empty.\n";
            return;
        }
        cout << "\n[*] Rear element is " << arr[rear] << " at index [" << rear << "].\n";
    }

    void display() const {
        cout << "\n--- Circular Queue Array (Size: " << size << "/" << capacity << ") ---\n";
        cout << "Index: ";
        for (int i = 0; i < capacity; i++) cout << "  [" << i << "] ";
        cout << "\nArray: ";
        for (int i = 0; i < capacity; i++) {
            bool inQueue = false;
            if (!isEmpty()) {
                if (front <= rear) {
                    inQueue = (i >= front && i <= rear);
                } else {
                    inQueue = (i >= front || i <= rear);
                }
            }
            if (inQueue) {
                cout << "  " << setw(3) << arr[i] << " ";
            } else {
                cout << "  --- ";
            }
        }
        cout << "\nTag:   ";
        for (int i = 0; i < capacity; i++) {
            if (i == front && i == rear && !isEmpty()) cout << "  F&R ";
            else if (i == front) cout << " FRONT";
            else if (i == rear) cout << "  REAR";
            else cout << "      ";
        }
        cout << "\n";
    }
};

// ------------------------------------------------------------------------------
// MAIN MENU
// ------------------------------------------------------------------------------
int main() {
    Stack s(5);
    CircularQueue q(5);

    int mainChoice = -1;
    while (mainChoice != 0) {
        cout << "\n============================================\n";
        cout << "   STRUCTLAB : STACK & CIRCULAR QUEUE CLI   \n";
        cout << "============================================\n";
        cout << "  [1] Stack (LIFO) Operations\n";
        cout << "  [2] Circular Queue (FIFO) Operations\n";
        cout << "  [0] Exit\n";
        cout << "--------------------------------------------\n";
        cout << "Enter your choice: ";
        if (!(cin >> mainChoice)) {
            cin.clear();
            cin.ignore(10000, '\n');
            continue;
        }

        if (mainChoice == 1) {
            int stackChoice = -1;
            while (stackChoice != 0) {
                s.display();
                cout << "\nSTACK OPERATIONS:\n";
                cout << "  1. Push\n  2. Pop\n  3. Peek\n  0. Back to Main Menu\n";
                cout << "Choose: ";
                cin >> stackChoice;
                if (stackChoice == 1) {
                    int val;
                    cout << "Enter value to push: ";
                    cin >> val;
                    s.push(val);
                } else if (stackChoice == 2) {
                    s.pop();
                } else if (stackChoice == 3) {
                    s.peek();
                }
            }
        } else if (mainChoice == 2) {
            int qChoice = -1;
            while (qChoice != 0) {
                q.display();
                cout << "\nCIRCULAR QUEUE OPERATIONS:\n";
                cout << "  1. Enqueue\n  2. Dequeue\n  3. Peek Front\n  4. Peek Rear\n  0. Back to Main Menu\n";
                cout << "Choose: ";
                cin >> qChoice;
                if (qChoice == 1) {
                    int val;
                    cout << "Enter value to enqueue: ";
                    cin >> val;
                    q.enqueue(val);
                } else if (qChoice == 2) {
                    q.dequeue();
                } else if (qChoice == 3) {
                    q.peekFront();
                } else if (qChoice == 4) {
                    q.peekRear();
                }
            }
        }
    }

    cout << "\nExiting StructLab CLI. Goodbye!\n";
    return 0;
}
