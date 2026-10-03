/**
 * Stack Visualizer Engine & Applications
 */
class StackEngine {
    constructor() {
        this.capacity = 6;
        this.items = []; // array of { value, id, address }
        this.isAnimating = false;
        this.baseAddress = 0x7FFE00;
        this.addressStep = 4; // 4 bytes per integer

        // DOM elements
        this.container = null;
        this.topPointer = null;
        this.capacityBadge = null;
        this.statusBadge = null;
        this.topValueDisplay = null;
    }

    init() {
        this.container = document.getElementById('stack-elements-container');
        this.topPointer = document.getElementById('stack-top-pointer');
        this.capacityBadge = document.getElementById('stack-capacity-display');
        this.statusBadge = document.getElementById('stack-status-badge');
        this.topValueDisplay = document.getElementById('stack-top-val-display');

        this.render();
    }

    setCapacity(newCap) {
        if (newCap < 3 || newCap > 10) return;
        if (newCap < this.items.length) {
            window.app.log(`Cannot resize to ${newCap}: contains ${this.items.length} items. Pop items first!`, 'warning');
            window.soundEngine.playError();
            return;
        }
        this.capacity = newCap;
        window.app.log(`Stack capacity set to ${this.capacity}`, 'info');
        this.render();
    }

    isFull() {
        return this.items.length >= this.capacity;
    }

    isEmpty() {
        return this.items.length === 0;
    }

    getTop() {
        return this.isEmpty() ? null : this.items[this.items.length - 1];
    }

    async push(value) {
        if (this.isAnimating) return;
        if (value === undefined || value === null || String(value).trim() === '') {
            window.app.log('Push aborted: Enter a valid value', 'warning');
            window.soundEngine.playError();
            return;
        }

        if (this.isFull()) {
            window.app.log(`Stack Overflow! Cannot push "${value}" - Capacity (${this.capacity}) reached.`, 'error');
            this.triggerContainerShake();
            window.soundEngine.playError();
            window.app.highlightCode('stack', 'overflow');
            return;
        }

        this.isAnimating = true;
        window.app.highlightCode('stack', 'push');

        const topIndex = this.items.length;
        const memoryAddr = '0x' + (this.baseAddress + topIndex * this.addressStep).toString(16).toUpperCase();
        const itemObj = {
            value: String(value),
            id: 'stack-item-' + Date.now() + '-' + Math.floor(Math.random() * 1000),
            address: memoryAddr
        };

        this.items.push(itemObj);
        window.soundEngine.playPush();

        this.render();
        const newEl = document.getElementById(itemObj.id);
        if (newEl) {
            newEl.classList.add('dropping-in');
            setTimeout(() => newEl.classList.remove('dropping-in'), 400);
        }

        window.app.log(`PUSH: Inserted "${value}" at index [${topIndex}] (${memoryAddr}) | Top is now ${topIndex}`, 'success');
        
        setTimeout(() => {
            this.isAnimating = false;
        }, 350);
    }

    async pop() {
        if (this.isAnimating) return;

        if (this.isEmpty()) {
            window.app.log('⚠️ STACK UNDERFLOW! Cannot pop from an empty stack (top = -1). Please enter a value and click Push first!', 'error');
            this.triggerContainerShake();
            window.soundEngine.playError();
            window.app.highlightCode('stack', 'underflow');

            const statusBadge = document.getElementById('stack-status-badge');
            if (statusBadge) {
                const prevText = statusBadge.textContent;
                const prevClass = statusBadge.className;
                statusBadge.textContent = 'UNDERFLOW! (Cannot Pop Empty Stack)';
                statusBadge.className = 'status-tag tag-full';
                setTimeout(() => {
                    statusBadge.textContent = prevText;
                    statusBadge.className = prevClass;
                }, 1800);
            }
            return;
        }

        this.isAnimating = true;
        window.app.highlightCode('stack', 'pop');

        const topIndex = this.items.length - 1;
        const poppedItem = this.items[topIndex];
        const topEl = document.getElementById(poppedItem.id);

        window.soundEngine.playPop();

        if (topEl) {
            topEl.classList.add('popping-out');
        }

        setTimeout(() => {
            this.items.pop();
            this.render();
            window.app.log(`✅ POP SUCCESS: Removed "${poppedItem.value}" from index [${topIndex}] (${poppedItem.address}) | New Top is ${this.items.length - 1}`, 'info');
            this.isAnimating = false;
        }, 300);
    }

    peek() {
        if (this.isEmpty()) {
            window.app.log('PEEK: Stack is empty! Top index is -1.', 'warning');
            window.soundEngine.playError();
            window.app.highlightCode('stack', 'peek_empty');
            return;
        }

        window.app.highlightCode('stack', 'peek');
        window.soundEngine.playPeek();

        const topItem = this.getTop();
        const topIndex = this.items.length - 1;
        const topEl = document.getElementById(topItem.id);

        if (topEl) {
            topEl.classList.add('peeking');
            setTimeout(() => topEl.classList.remove('peeking'), 800);
        }

        window.app.log(`PEEK: Top element is "${topItem.value}" at index [${topIndex}] (${topItem.address})`, 'success');
    }

    clear() {
        if (this.isEmpty()) return;
        this.items = [];
        this.render();
        window.soundEngine.playDequeue();
        window.app.log('Stack cleared successfully.', 'info');
    }

    fillRandom() {
        this.clear();
        const count = Math.min(this.capacity, Math.floor(Math.random() * 3) + 3);
        const randomValues = [14, 28, 42, 57, 73, 89, 99, 105, 128, 256];
        randomValues.sort(() => Math.random() - 0.5);

        for (let i = 0; i < count; i++) {
            const memoryAddr = '0x' + (this.baseAddress + i * this.addressStep).toString(16).toUpperCase();
            this.items.push({
                value: String(randomValues[i]),
                id: 'stack-item-' + Date.now() + '-' + i,
                address: memoryAddr
            });
        }
        this.render();
        window.soundEngine.playSuccess();
        window.app.log(`Stack initialized with ${count} random elements.`, 'success');
    }

    triggerContainerShake() {
        const frame = document.getElementById('stack-visual-frame');
        if (frame) {
            frame.classList.add('error-shake');
            setTimeout(() => frame.classList.remove('error-shake'), 450);
        }
    }

    render() {
        if (!this.container) return;

        // Update badges
        const count = this.items.length;
        if (this.capacityBadge) {
            this.capacityBadge.textContent = `${count} / ${this.capacity}`;
        }

        if (this.statusBadge) {
            if (this.isEmpty()) {
                this.statusBadge.textContent = 'EMPTY (top = -1)';
                this.statusBadge.className = 'status-tag tag-empty';
            } else if (this.isFull()) {
                this.statusBadge.textContent = 'FULL (Overflow)';
                this.statusBadge.className = 'status-tag tag-full';
            } else {
                this.statusBadge.textContent = `NORMAL (top = ${count - 1})`;
                this.statusBadge.className = 'status-tag tag-active';
            }
        }

        if (this.topValueDisplay) {
            this.topValueDisplay.textContent = this.isEmpty() ? 'NULL' : this.getTop().value;
        }

        // Render slots from top (capacity - 1) down to 0
        let html = '';
        for (let i = this.capacity - 1; i >= 0; i--) {
            const isFilled = i < this.items.length;
            const item = isFilled ? this.items[i] : null;
            const isTop = isFilled && i === this.items.length - 1;
            const slotAddr = '0x' + (this.baseAddress + i * this.addressStep).toString(16).toUpperCase();

            html += `
                <div class="stack-slot ${isFilled ? 'filled' : 'empty-slot'} ${isTop ? 'is-top-slot' : ''}" data-index="${i}">
                    <div class="slot-meta">
                        <span class="slot-index">[${i}]</span>
                        <span class="slot-address">${slotAddr}</span>
                    </div>
                    <div class="slot-content">
                        ${isFilled ? `
                            <div class="stack-item ${isTop ? 'top-item' : ''}" id="${item.id}">
                                <span class="item-val">${this.escapeHtml(item.value)}</span>
                                ${isTop ? '<span class="item-pointer-label">TOP &larr;</span>' : ''}
                            </div>
                        ` : `
                            <div class="empty-placeholder">
                                <span>&mdash; Empty &mdash;</span>
                            </div>
                        `}
                    </div>
                </div>
            `;
        }

        this.container.innerHTML = html;
        this.updateTopPointer();
    }

    updateTopPointer() {
        if (!this.topPointer) return;
        const topIdx = this.items.length - 1;

        if (this.isEmpty()) {
            this.topPointer.style.opacity = '0.4';
            this.topPointer.innerHTML = `
                <div class="pointer-badge empty">
                    <span class="pointer-arrow">&larr;</span>
                    <span class="pointer-text">TOP: -1 (Stack is Empty)</span>
                </div>
            `;
        } else {
            this.topPointer.style.opacity = '1';
            const topItem = this.getTop();
            this.topPointer.innerHTML = `
                <div class="pointer-badge active">
                    <span class="pointer-arrow">&larr;</span>
                    <span class="pointer-text">TOP: [${topIdx}] = "${this.escapeHtml(topItem.value)}"</span>
                </div>
            `;
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

/**
 * Stack Application: Balanced Parentheses Checker Simulator
 */
class ParenthesesChecker {
    constructor() {
        this.exprInput = null;
        this.stepContainer = null;
        this.resultContainer = null;
        this.speed = 600;
        this.isRunning = false;
    }

    init() {
        this.exprInput = document.getElementById('paren-input');
        this.stepContainer = document.getElementById('paren-steps-log');
        this.resultContainer = document.getElementById('paren-result-banner');
    }

    async run() {
        if (this.isRunning) return;
        const expr = (this.exprInput ? this.exprInput.value : '{[()]}').trim();
        if (!expr) return;

        this.isRunning = true;
        this.stepContainer.innerHTML = '';
        this.resultContainer.className = 'result-banner running';
        this.resultContainer.innerHTML = `<span class="spinner"></span> Evaluating expression: <code>${expr}</code>...`;

        const stack = [];
        const pairs = { ')': '(', '}': '{', ']': '[' };
        const openBrackets = new Set(['(', '{', '[']);
        const closeBrackets = new Set([')', '}', ']']);

        let isBalanced = true;
        let failReason = '';

        for (let i = 0; i < expr.length; i++) {
            const char = expr[i];

            if (openBrackets.has(char)) {
                stack.push({ char, idx: i });
                this.addStepLog(i, char, `Opening bracket '${char}' detected &rarr; Pushed to stack. Stack size: ${stack.length}`, 'push');
                window.soundEngine.playPush();
                await this.delay(this.speed);
            } else if (closeBrackets.has(char)) {
                if (stack.length === 0) {
                    isBalanced = false;
                    failReason = `Unmatched closing bracket '${char}' at index ${i} with an empty stack!`;
                    this.addStepLog(i, char, failReason, 'error');
                    window.soundEngine.playError();
                    break;
                }

                const top = stack.pop();
                if (top.char === pairs[char]) {
                    this.addStepLog(i, char, `Closing bracket '${char}' matches Top bracket '${top.char}' &rarr; Popped from stack!`, 'match');
                    window.soundEngine.playPop();
                    await this.delay(this.speed);
                } else {
                    isBalanced = false;
                    failReason = `Mismatched brackets: Expected '${pairs[char]}' but found '${top.char}' for closing '${char}' at index ${i}!`;
                    this.addStepLog(i, char, failReason, 'error');
                    window.soundEngine.playError();
                    break;
                }
            } else {
                // Regular operand/operator
                this.addStepLog(i, char, `Character '${char}' is operand/operator &rarr; Skipped.`, 'skip');
            }
        }

        if (isBalanced && stack.length > 0) {
            isBalanced = false;
            failReason = `Stack not empty at end! Remaining unmatched opening brackets: ${stack.map(s => s.char).join(', ')}`;
            this.addStepLog(expr.length, 'EOF', failReason, 'error');
            window.soundEngine.playError();
        }

        if (isBalanced) {
            this.resultContainer.className = 'result-banner success';
            this.resultContainer.innerHTML = `<strong>VALID &amp; BALANCED!</strong> All brackets correctly paired and stack is clean.`;
            window.soundEngine.playSuccess();
        } else {
            this.resultContainer.className = 'result-banner failure';
            this.resultContainer.innerHTML = `<strong>INVALID / UNBALANCED!</strong> ${failReason}`;
        }

        this.isRunning = false;
    }

    addStepLog(index, char, desc, type) {
        if (!this.stepContainer) return;
        const div = document.createElement('div');
        div.className = `step-log-item step-${type}`;
        div.innerHTML = `
            <span class="step-char">[Pos ${index}: <code>${char}</code>]</span>
            <span class="step-desc">${desc}</span>
        `;
        this.stepContainer.appendChild(div);
        this.stepContainer.scrollTop = this.stepContainer.scrollHeight;
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

window.stackEngine = new StackEngine();
window.parenthesesChecker = new ParenthesesChecker();
