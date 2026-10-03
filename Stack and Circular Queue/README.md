# StructLab: Stack & Circular Queue Interactive Visualizer Suite 🚀
*(डेटा स्ट्रक्चर्स इंटरेक्टिव विज़ुअलाइज़र और लर्निंग सुइट)*

> ⚡ **LEAD DEVELOPER & ARCHITECT:** **SWAYAM BAJPAI**

एक आधुनिक, हाई-डेफिनिशन और एनिमेटेड वेब एप्लिकेशन जो **Stack (LIFO)** और **Circular Queue (FIFO Ring Buffer)** डेटा स्ट्रक्चर्स को विज़ुअलाइज़ करने, समझने और सीखने के लिए बनाया गया है।

---

## 🌟 मुख्य विशेषताएँ (Key Features)

### 🥞 1. Stack Visualizer (LIFO - Last In, First Out)
- **3D-स्टाइल ग्लास कंटेनर**: एलिमेंट्स ऊपर से गिरते हैं (smooth bounce) और टॉप से पॉप होकर निकलते हैं।
- **Dynamic TOP Pointer**: वर्तमान टॉप एलिमेंट और मेमोरी एड्रेस (उदा. `0x7FFE04`) को रियल-टाइम में ट्रैक करता है।
- **ऑपरेशन्स**:
  - `Push(x)` - नए आइटम को स्टैक में डालना।
  - `Pop()` - टॉप आइटम को बाहर निकालना।
  - `Peek() / Top()` - बिना हटाए टॉप आइटम को हाईलाइट करके देखना।
  - `Randomize` - रैंडम डेटा से स्टैक भरना।
  - `Clear` - स्टैक को रीसेट करना।
- **बाउंड्री चेकिंग**: Overflow (`top == capacity - 1`) और Underflow (`top == -1`) पर विजुअल शेक और ऑडियो अलर्ट।
- **कस्टमाइज़ेबल कैपेसिटी**: 4 से 10 स्लॉट्स।

---

### 🔄 2. Circular Queue Visualizer (FIFO Ring Buffer)
- **डुअल सिंक्रोनाइज़्ड विज़ुअलाइज़ेशन**:
  1. **Radial Ring SVG Visualizer**: एक सर्कुलर रिंग जिसमें क्लॉकवाइज़ इंडेक्स `0` से `N-1` होते हैं। `FRONT` (Emerald Neon) और `REAR` (Pink/Magenta Neon) पॉइंटर्स रियल-टाइम में रोटेट होते हैं।
  2. **Linear Memory Array Projection**: दिखाता है कि स्टैंडर्ड क्यू की मेमोरी वेस्टेज को सर्कुलर क्यू कैसे खत्म करता है।
- **Modulo Arithmetic HUD**:
  - `rear = (rear + 1) % capacity`
  - `front = (front + 1) % capacity`
  - Overflow Check: `(rear + 1) % capacity == front`
- **Auto-Wrap Demo**: एक क्लिक में दिखाता है कि कैसे एलिमेंट्स एंड से वापस इंडेक्स `0` पर रैप होकर खाली स्लॉट्स को दोबारा इस्तेमाल करते हैं!

---

### 🧪 3. Real-World Applications Arena
1. **Balanced Parentheses Checker (Compiler Parsing)**:
   - कंपाइलर पार्सिंग का लाइव सिमुलेशन (`{[()]}`, `((a+b)*[c-d])` आदि)।
   - स्टेप-बाय-स्टेप ब्रैकेट्स का स्टैक में पुश होना और क्लोजिंग ब्रैकेट मिलने पर टॉप से मैच होकर पॉप होना।
2. **CPU Round-Robin Task Scheduler (Operating Systems)**:
   - ऑपरेटिंग सिस्टम में प्रोसेस शेड्यूलिंग का लाइव सिमुलेशन।
   - Time Quantum (2 units) के साथ प्रोसेस सर्कुलर रेडी क्यू से CPU कोर में जाते हैं और टास्क पूरा न होने पर वापस REAR में जुड़ते हैं!

---

### 📖 4. Code & Algorithm Explorer
- **Multi-Language Implementation**:
  - C++ (Class with Dynamic Pointer Array)
  - Java (Fixed-capacity Array Implementation)
  - Python (List-based Fixed Buffer)
  - JavaScript (ES6 Class Implementation)
- **One-Click Copy**: कोड को आसानी से कॉपी करने का विकल्प।

---

### 🎯 5. Concept Mastery Quiz
- स्टैक और सर्कुलर क्यू की समझ को परखने के लिए 5 बहुविकल्पीय प्रश्न (MCQ)।
- तुरंत उत्तर का विश्लेषण, स्कोर कार्ड और विस्तृत स्पष्टीकरण (Explanation)।

---

### 🔊 6. Built-in Web Audio API Synthesizer
- पुश, पॉप, एनक्यू, डीक्यू, पीक, एरर और सक्सेस पर कस्टम सिंथेसाइज़्ड साउंड इफेक्ट्स (बिना किसी बाहरी ऑडियो फाइल के, 100% ऑफलाइन काम करता है)।

---

## ⌨️ कीबोर्ड शॉर्टकट्स (Keyboard Shortcuts)

| Shortcut Key | Action |
|---|---|
| `Enter` | Stack में **Push** या Circular Queue में **Enqueue** करना |
| `Delete` / `Backspace` | Stack से **Pop** या Circular Queue से **Dequeue** करना |
| `1` | Switch to **Stack Visualizer** |
| `2` | Switch to **Circular Queue** |
| `3` | Switch to **Real-World Apps** |
| `4` | Switch to **Code Explorer** |
| `5` | Switch to **Quiz & Challenge** |

---

## 📁 प्रोजेक्ट स्ट्रक्चर (Project Structure)

```
Stack and Circular Queue/
├── index.html              # मुख्य वेब पेज (Semantic HTML5)
├── css/
│   └── style.css           # Glassmorphism, Neon Dark UI और Fluid Animations
├── js/
│   ├── audio.js            # Web Audio API साउंड जनरेटर
│   ├── codeSnippets.js     # C++, Java, Python, JS कोड स्निपेट्स
│   ├── stack.js            # स्टैक विज़ुअलाइज़र और Balanced Parentheses इंजन
│   ├── circularQueue.js    # सर्कुलर क्यू SVG रिंग और CPU Scheduler इंजन
│   └── app.js              # मुख्य कंट्रोलर, कीबोर्ड शॉर्टकट्स और क्विज लॉजिक
└── README.md               # यह दस्तावेज़ (Documentation)
```

---

## 🚀 इस प्रोजेक्ट को कैसे चलाएं (How to Run)

### 💻 1. Command Prompt (CMD / Terminal) में चलाने के लिए:
- फ़ोल्डर में मौजूद [`run.bat`](file:///c:/Users/Swayam/OneDrive/Desktop/Stack%20and%20Circular%20Queue/run.bat) फाइल पर **डबल क्लिक** करें, **या**
- Command Prompt (CMD) में लिखें:
  ```cmd
  cd "c:\Users\Swayam\OneDrive\Desktop\Stack and Circular Queue"
  run.bat
  ```
- यह तुरंत CMD विंडो में कलरफुल ASCII विजुअलाइज़र, ऑडियो बीप्स और मेन्यू के साथ शुरू हो जाएगा!

### 🌐 2. Web Browser में चलाने के लिए:
- फ़ोल्डर में मौजूद [`index.html`](file:///c:/Users/Swayam/OneDrive/Desktop/Stack%20and%20Circular%20Queue/index.html) फाइल पर **डबल क्लिक** करें।

