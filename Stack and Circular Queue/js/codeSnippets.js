/**
 * Multi-language implementation code snippets for Stack and Circular Queue
 * With step line mapping for real-time code highlighting during operations.
 */
const CODE_SNIPPETS = {
    stack: {
        cpp: `// C++ Array-based Stack Implementation
#include <iostream>
using namespace std;

class Stack {
    int top;
    int capacity;
    int* arr;
public:
    Stack(int size) {
        capacity = size;
        arr = new int[capacity];
        top = -1;
    }

    bool isFull() {
        return top == capacity - 1;
    }

    bool isEmpty() {
        return top == -1;
    }

    void push(int x) {
        if (isFull()) {
            cout << "Stack Overflow!\\n";
            return;
        }
        top++;
        arr[top] = x;
    }

    int pop() {
        if (isEmpty()) {
            cout << "Stack Underflow!\\n";
            return -1;
        }
        int val = arr[top];
        top--;
        return val;
    }

    int peek() {
        if (isEmpty()) return -1;
        return arr[top];
    }
};`,
        java: `// Java Stack Implementation using Fixed Array
public class ArrayStack {
    private int[] arr;
    private int top;
    private int capacity;

    public ArrayStack(int size) {
        capacity = size;
        arr = new int[capacity];
        top = -1;
    }

    public boolean isFull() {
        return top == capacity - 1;
    }

    public boolean isEmpty() {
        return top == -1;
    }

    public void push(int x) {
        if (isFull()) {
            throw new RuntimeException("Stack Overflow!");
        }
        arr[++top] = x;
    }

    public int pop() {
        if (isEmpty()) {
            throw new RuntimeException("Stack Underflow!");
        }
        return arr[top--];
    }

    public int peek() {
        if (isEmpty()) throw new RuntimeException("Stack is Empty");
        return arr[top];
    }
}`,
        python: `# Python Fixed-Capacity Stack Implementation
class Stack:
    def __init__(self, capacity):
        self.capacity = capacity
        self.arr = [None] * capacity
        self.top = -1

    def is_full(self):
        return self.top == self.capacity - 1

    def is_empty(self):
        return self.top == -1

    def push(self, val):
        if self.is_full():
            raise OverflowError("Stack Overflow!")
        self.top += 1
        self.arr[self.top] = val

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack Underflow!")
        val = self.arr[self.top]
        self.arr[self.top] = None
        self.top -= 1
        return val

    def peek(self):
        if self.is_empty():
            return None
        return self.arr[self.top]`,
        js: `// JavaScript Stack Class
class Stack {
    constructor(capacity) {
        this.capacity = capacity;
        this.arr = new Array(capacity);
        this.top = -1;
    }

    isFull() {
        return this.top === this.capacity - 1;
    }

    isEmpty() {
        return this.top === -1;
    }

    push(val) {
        if (this.isFull()) {
            console.error("Stack Overflow!");
            return false;
        }
        this.top++;
        this.arr[this.top] = val;
        return true;
    }

    pop() {
        if (this.isEmpty()) {
            console.error("Stack Underflow!");
            return null;
        }
        const val = this.arr[this.top];
        this.arr[this.top] = undefined;
        this.top--;
        return val;
    }

    peek() {
        if (this.isEmpty()) return null;
        return this.arr[this.top];
    }
}`
    },

    circularQueue: {
        cpp: `// C++ Circular Queue (Ring Buffer)
#include <iostream>
using namespace std;

class CircularQueue {
    int front, rear, size, capacity;
    int* arr;
public:
    CircularQueue(int cap) {
        capacity = cap;
        arr = new int[capacity];
        front = -1;
        rear = -1;
        size = 0;
    }

    bool isFull() {
        return (front == 0 && rear == capacity - 1) || 
               ((rear + 1) % capacity == front);
    }

    bool isEmpty() {
        return front == -1;
    }

    void enqueue(int val) {
        if (isFull()) {
            cout << "Queue Overflow!\\n";
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
    }

    int dequeue() {
        if (isEmpty()) {
            cout << "Queue Underflow!\\n";
            return -1;
        }
        int val = arr[front];
        if (front == rear) { // single element
            front = -1;
            rear = -1;
        } else {
            front = (front + 1) % capacity;
        }
        size--;
        return val;
    }

    int getFront() {
        return isEmpty() ? -1 : arr[front];
    }

    int getRear() {
        return isEmpty() ? -1 : arr[rear];
    }
};`,
        java: `// Java Circular Queue Implementation
public class CircularQueue {
    private int[] arr;
    private int front, rear, size, capacity;

    public CircularQueue(int k) {
        capacity = k;
        arr = new int[capacity];
        front = -1;
        rear = -1;
        size = 0;
    }

    public boolean isFull() {
        return size == capacity;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public boolean enQueue(int value) {
        if (isFull()) return false;
        if (isEmpty()) {
            front = 0;
        }
        rear = (rear + 1) % capacity;
        arr[rear] = value;
        size++;
        return true;
    }

    public boolean deQueue() {
        if (isEmpty()) return false;
        if (front == rear) {
            front = -1;
            rear = -1;
        } else {
            front = (front + 1) % capacity;
        }
        size--;
        return true;
    }

    public int Front() {
        return isEmpty() ? -1 : arr[front];
    }

    public int Rear() {
        return isEmpty() ? -1 : arr[rear];
    }
}`,
        python: `# Python Circular Queue (Ring Buffer)
class CircularQueue:
    def __init__(self, k: int):
        self.capacity = k
        self.arr = [None] * k
        self.front = -1
        self.rear = -1
        self.size = 0

    def is_full(self) -> bool:
        return self.size == self.capacity

    def is_empty(self) -> bool:
        return self.size == 0

    def enqueue(self, val: int) -> bool:
        if self.is_full():
            return False
        if self.is_empty():
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.capacity
        self.arr[self.rear] = val
        self.size += 1
        return True

    def dequeue(self) -> int:
        if self.is_empty():
            return None
        val = self.arr[self.front]
        self.arr[self.front] = None
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return val`,
        js: `// JavaScript Circular Queue Class
class CircularQueue {
    constructor(capacity) {
        this.capacity = capacity;
        this.arr = new Array(capacity).fill(null);
        this.front = -1;
        this.rear = -1;
        this.size = 0;
    }

    isFull() {
        return this.size === this.capacity;
    }

    isEmpty() {
        return this.size === 0;
    }

    enqueue(val) {
        if (this.isFull()) return false;
        if (this.isEmpty()) {
            this.front = 0;
            this.rear = 0;
        } else {
            this.rear = (this.rear + 1) % this.capacity;
        }
        this.arr[this.rear] = val;
        this.size++;
        return true;
    }

    dequeue() {
        if (this.isEmpty()) return null;
        const val = this.arr[this.front];
        this.arr[this.front] = null;
        if (this.front === this.rear) {
            this.front = -1;
            this.rear = -1;
        } else {
            this.front = (this.front + 1) % this.capacity;
        }
        this.size--;
        return val;
    }
}`
    }
};

window.CODE_SNIPPETS = CODE_SNIPPETS;
