/**
 * Circular Queue (Ring Buffer) Visualizer Engine & Applications
 */
class CircularQueueEngine {
    constructor() {
        this.capacity = 6;
        this.arr = new Array(this.capacity).fill(null);
        this.front = -1;
        this.rear = -1;
        this.count = 0;
        this.isAnimating = false;

        // Base memory address
        this.baseAddress = 0x8A1000;
        this.addressStep = 4;

        // DOM elements
        this.svgRing = null;
        this.linearContainer = null;
        this.formulaHud = null;
        this.statusBadge = null;
        this.frontRearBadge = null;
    }

    init() {
        this.svgRing = document.getElementById('cq-svg-ring');
        this.linearContainer = document.getElementById('cq-linear-container');
        this.formulaHud = document.getElementById('cq-formula-hud');
        this.statusBadge = document.getElementById('cq-status-badge');
        this.frontRearBadge = document.getElementById('cq-front-rear-display');

        this.render();
    }

    setCapacity(newCap) {
        if (newCap < 4 || newCap > 8) return;
        if (this.count > 0) {
            window.app.log(`Cannot resize while queue has ${this.count} elements. Clear first!`, 'warning');
            window.soundEngine.playError();
            return;
        }
        this.capacity = newCap;
        this.arr = new Array(this.capacity).fill(null);
        this.front = -1;
        this.rear = -1;
        this.count = 0;
        window.app.log(`Circular Queue capacity set to ${this.capacity}`, 'info');
        this.render();
    }

    isFull() {
        return this.count === this.capacity;
    }

    isEmpty() {
        return this.count === 0;
    }

    enqueue(val) {
        if (this.isAnimating) return;
        if (val === undefined || val === null || String(val).trim() === '') {
            window.app.log('Enqueue aborted: Please enter a value', 'warning');
            window.soundEngine.playError();
            return;
        }

        if (this.isFull()) {
            window.app.log(`Queue Overflow! (rear + 1) % ${this.capacity} == front (${this.front}). Cannot enqueue "${val}".`, 'error');
            this.triggerShake();
            window.soundEngine.playError();
            window.app.highlightCode('circularQueue', 'overflow');
            return;
        }

        this.isAnimating = true;
        window.app.highlightCode('circularQueue', 'enqueue');

        const prevRear = this.rear;
        if (this.isEmpty()) {
            this.front = 0;
            this.rear = 0;
        } else {
            this.rear = (this.rear + 1) % this.capacity;
        }

        const isWrap = prevRear !== -1 && this.rear < prevRear;
        this.arr[this.rear] = String(val);
        this.count++;

        window.soundEngine.playEnqueue();
        this.render();

        const wrapMsg = isWrap ? ` [CIRCULAR WRAP-AROUND TO 0! Formula: (${prevRear} + 1) % ${this.capacity} = 0]` : '';
        window.app.log(`ENQUEUE: Inserted "${val}" at index [${this.rear}] | Front: ${this.front}, Rear: ${this.rear}, Count: ${this.count}/${this.capacity}${wrapMsg}`, 'success');

        setTimeout(() => {
            this.isAnimating = false;
        }, 300);
    }

    dequeue() {
        if (this.isAnimating) return;

        if (this.isEmpty()) {
            window.app.log('Queue Underflow! Queue is currently empty (count = 0).', 'error');
            this.triggerShake();
            window.soundEngine.playError();
            window.app.highlightCode('circularQueue', 'underflow');
            return;
        }

        this.isAnimating = true;
        window.app.highlightCode('circularQueue', 'dequeue');

        const prevFront = this.front;
        const val = this.arr[this.front];
        this.arr[this.front] = null;
        this.count--;

        const isWrap = this.count > 0 && ((prevFront + 1) % this.capacity === 0);

        if (this.count === 0) {
            this.front = -1;
            this.rear = -1;
        } else {
            this.front = (this.front + 1) % this.capacity;
        }

        window.soundEngine.playDequeue();
        this.render();

        const wrapMsg = isWrap ? ` [FRONT WRAP-AROUND TO 0! Formula: (${prevFront} + 1) % ${this.capacity} = 0]` : '';
        window.app.log(`DEQUEUE: Removed "${val}" from index [${prevFront}] | Front: ${this.front}, Rear: ${this.rear}, Count: ${this.count}/${this.capacity}${wrapMsg}`, 'info');

        setTimeout(() => {
            this.isAnimating = false;
        }, 300);
    }

    peekFront() {
        if (this.isEmpty()) {
            window.app.log('FRONT is NULL (Queue is empty)', 'warning');
            window.soundEngine.playError();
            return;
        }
        window.soundEngine.playPeek();
        window.app.log(`GET FRONT: Value is "${this.arr[this.front]}" at index [${this.front}]`, 'success');
        this.highlightSlot(this.front, 'peek-front');
    }

    peekRear() {
        if (this.isEmpty()) {
            window.app.log('REAR is NULL (Queue is empty)', 'warning');
            window.soundEngine.playError();
            return;
        }
        window.soundEngine.playPeek();
        window.app.log(`GET REAR: Value is "${this.arr[this.rear]}" at index [${this.rear}]`, 'success');
        this.highlightSlot(this.rear, 'peek-rear');
    }

    clear() {
        this.arr = new Array(this.capacity).fill(null);
        this.front = -1;
        this.rear = -1;
        this.count = 0;
        this.render();
        window.soundEngine.playDequeue();
        window.app.log('Circular Queue reset to empty state.', 'info');
    }

    async runWrapDemo() {
        if (this.isAnimating) return;
        this.clear();
        window.app.log('--- STARTING CIRCULAR WRAP DEMONSTRATION ---', 'info');
        
        // Fill up first 4 items
        for (const item of ['A', 'B', 'C', 'D']) {
            this.enqueue(item);
            await this.delay(450);
        }

        window.app.log('Now dequeuing 2 items to free up slots [0] and [1] at the start...', 'warning');
        await this.delay(700);
        this.dequeue();
        await this.delay(500);
        this.dequeue();
        await this.delay(700);

        window.app.log('Now enqueuing items until rear reaches the end and wraps to [0]!', 'info');
        const remaining = ['E', 'F', 'WRAP_1', 'WRAP_2'];
        for (const item of remaining) {
            if (this.isFull()) break;
            this.enqueue(item);
            await this.delay(550);
        }

        window.app.log('Circular Wrap-Around demonstration complete! Notice how slots 0 and 1 are reused without shifting!', 'success');
        window.soundEngine.playSuccess();
    }

    highlightSlot(index, cssClass) {
        const svgNode = document.getElementById(`cq-node-${index}`);
        const linearNode = document.getElementById(`cq-linear-cell-${index}`);

        if (svgNode) {
            svgNode.classList.add(cssClass);
            setTimeout(() => svgNode.classList.remove(cssClass), 900);
        }
        if (linearNode) {
            linearNode.classList.add(cssClass);
            setTimeout(() => linearNode.classList.remove(cssClass), 900);
        }
    }

    triggerShake() {
        const stage = document.getElementById('cq-visual-stage');
        if (stage) {
            stage.classList.add('error-shake');
            setTimeout(() => stage.classList.remove('error-shake'), 450);
        }
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    render() {
        this.renderBadges();
        this.renderRadialSVG();
        this.renderLinearArray();
        this.renderFormulaHud();
    }

    renderBadges() {
        if (this.statusBadge) {
            if (this.isEmpty()) {
                this.statusBadge.textContent = 'EMPTY (F: -1, R: -1)';
                this.statusBadge.className = 'status-tag tag-empty';
            } else if (this.isFull()) {
                this.statusBadge.textContent = `FULL (${this.count}/${this.capacity})`;
                this.statusBadge.className = 'status-tag tag-full';
            } else {
                this.statusBadge.textContent = `ACTIVE (${this.count}/${this.capacity})`;
                this.statusBadge.className = 'status-tag tag-active';
            }
        }

        if (this.frontRearBadge) {
            this.frontRearBadge.innerHTML = `
                <span class="pointer-pill pill-front">FRONT: ${this.front === -1 ? 'None' : '[' + this.front + ']'}</span>
                <span class="pointer-pill pill-rear">REAR: ${this.rear === -1 ? 'None' : '[' + this.rear + ']'}</span>
            `;
        }
    }

    renderRadialSVG() {
        if (!this.svgRing) return;

        const size = 380;
        const center = size / 2;
        const radius = 135;
        const nodeRadius = 32;

        let svgContent = `
            <defs>
                <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="4" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
                <linearGradient id="ringTrackGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#00f2fe" stop-opacity="0.3"/>
                    <stop offset="50%" stop-color="#9d4edd" stop-opacity="0.15"/>
                    <stop offset="100%" stop-color="#00f5a0" stop-opacity="0.3"/>
                </linearGradient>
            </defs>

            <!-- Base Guide Track Ring -->
            <circle cx="${center}" cy="${center}" r="${radius}" 
                    fill="none" stroke="url(#ringTrackGrad)" stroke-width="4" stroke-dasharray="6 6" opacity="0.8"/>
            
            <!-- Center Decorative Ring -->
            <circle cx="${center}" cy="${center}" r="45" fill="#0b1020" stroke="rgba(255,255,255,0.08)" stroke-width="2"/>
            <text x="${center}" y="${center - 6}" text-anchor="middle" fill="#7d8ca3" font-size="11" font-family="'Outfit', sans-serif" font-weight="600">CAPACITY</text>
            <text x="${center}" y="${center + 16}" text-anchor="middle" fill="#00f5a0" font-size="20" font-family="'JetBrains Mono', monospace" font-weight="700">${this.count}/${this.capacity}</text>
        `;

        // Render slots
        for (let i = 0; i < this.capacity; i++) {
            const angle = (2 * Math.PI * i) / this.capacity - Math.PI / 2;
            const x = center + radius * Math.cos(angle);
            const y = center + radius * Math.sin(angle);

            const isFilled = this.arr[i] !== null;
            const isFront = this.front === i;
            const isRear = this.rear === i;

            // Indicator tags offset
            const tagOffset = 52;
            const tagX = center + (radius + tagOffset) * Math.cos(angle);
            const tagY = center + (radius + tagOffset) * Math.sin(angle);

            let nodeClass = 'cq-svg-slot';
            if (isFilled) nodeClass += ' filled';
            if (isFront) nodeClass += ' is-front';
            if (isRear) nodeClass += ' is-rear';

            svgContent += `
                <g class="${nodeClass}" id="cq-node-${i}">
                    <!-- Outer slot boundary -->
                    <circle cx="${x}" cy="${y}" r="${nodeRadius}" class="slot-circle" />

                    <!-- Index badge -->
                    <circle cx="${x}" cy="${y - nodeRadius + 4}" r="9" class="index-pill-bg" />
                    <text x="${x}" y="${y - nodeRadius + 7}" text-anchor="middle" class="index-pill-text">${i}</text>

                    <!-- Value -->
                    <text x="${x}" y="${y + (isFilled ? 6 : 4)}" text-anchor="middle" class="slot-value-text">
                        ${isFilled ? this.escapeHtml(this.arr[i]) : '&middot;'}
                    </text>
            `;

            // Pointer Indicators
            if (isFront && isRear) {
                svgContent += `
                    <g class="pointer-group pointer-both" transform="translate(${tagX}, ${tagY})">
                        <rect x="-38" y="-12" width="76" height="24" rx="12" class="tag-bg-both"/>
                        <text x="0" y="4" text-anchor="middle" class="tag-text">F &amp; R</text>
                    </g>
                    <!-- Pointer directional line -->
                    <line x1="${tagX}" y1="${tagY}" x2="${x + Math.cos(angle)*nodeRadius}" y2="${y + Math.sin(angle)*nodeRadius}" stroke="#ffd166" stroke-width="2" stroke-dasharray="2 2" />
                `;
            } else if (isFront) {
                svgContent += `
                    <g class="pointer-group pointer-front" transform="translate(${tagX}, ${tagY})">
                        <rect x="-32" y="-12" width="64" height="24" rx="12" class="tag-bg-front"/>
                        <text x="0" y="4" text-anchor="middle" class="tag-text">FRONT</text>
                    </g>
                    <line x1="${tagX}" y1="${tagY}" x2="${x + Math.cos(angle)*nodeRadius}" y2="${y + Math.sin(angle)*nodeRadius}" stroke="#00f5a0" stroke-width="2" />
                `;
            } else if (isRear) {
                svgContent += `
                    <g class="pointer-group pointer-rear" transform="translate(${tagX}, ${tagY})">
                        <rect x="-30" y="-12" width="60" height="24" rx="12" class="tag-bg-rear"/>
                        <text x="0" y="4" text-anchor="middle" class="tag-text">REAR</text>
                    </g>
                    <line x1="${tagX}" y1="${tagY}" x2="${x + Math.cos(angle)*nodeRadius}" y2="${y + Math.sin(angle)*nodeRadius}" stroke="#d946ef" stroke-width="2" />
                `;
            }

            svgContent += `</g>`;
        }

        this.svgRing.innerHTML = svgContent;
    }

    renderLinearArray() {
        if (!this.linearContainer) return;

        let html = '';
        for (let i = 0; i < this.capacity; i++) {
            const isFilled = this.arr[i] !== null;
            const isFront = this.front === i;
            const isRear = this.rear === i;
            const slotAddr = '0x' + (this.baseAddress + i * this.addressStep).toString(16).toUpperCase();

            let tags = [];
            if (isFront && isRear) tags.push('<span class="cq-pill-both">F &amp; R</span>');
            else {
                if (isFront) tags.push('<span class="cq-pill-front">FRONT</span>');
                if (isRear) tags.push('<span class="cq-pill-rear">REAR</span>');
            }

            html += `
                <div class="cq-linear-cell ${isFilled ? 'filled' : 'empty'} ${isFront ? 'is-front' : ''} ${isRear ? 'is-rear' : ''}" id="cq-linear-cell-${i}">
                    <div class="cell-pointers">${tags.join('')}</div>
                    <div class="cell-box">
                        <span class="cell-value">${isFilled ? this.escapeHtml(this.arr[i]) : '&mdash;'}</span>
                    </div>
                    <div class="cell-meta">
                        <span class="cell-idx">[${i}]</span>
                        <span class="cell-addr">${slotAddr}</span>
                    </div>
                </div>
            `;
        }

        this.linearContainer.innerHTML = html;
    }

    renderFormulaHud() {
        if (!this.formulaHud) return;

        const nextRear = this.isEmpty() ? 0 : (this.rear + 1) % this.capacity;
        const currentFront = this.isEmpty() ? 'None (Queue Empty)' : `[${this.front}] ("${this.arr[this.front]}")`;
        const nextFrontAfterDeq = this.count <= 1 ? -1 : (this.front + 1) % this.capacity;
        const fullCheck = `(rear + 1) % ${this.capacity} == front &rarr; (${this.rear} + 1) % ${this.capacity} == ${this.front} (${this.isFull() ? '<span style="color: #f43f5e; font-weight:700;">TRUE (FULL - OVERFLOW)</span>' : '<span style="color: #00f5a0; font-weight:700;">FALSE (CAN ENQUEUE)</span>'})`;
        const emptyCheck = `count == 0 &rarr; ${this.count} == 0 (${this.isEmpty() ? '<span style="color: #f59e0b; font-weight:700;">TRUE (EMPTY)</span>' : 'FALSE'})`;

        this.formulaHud.innerHTML = `
            <div class="hud-item">
                <span class="hud-label">Next Enqueue Index:</span>
                <span class="hud-formula"><code>(rear + 1) % ${this.capacity}</code> = <strong>${this.isFull() ? '<span style="color: #f43f5e;">BLOCKED (FULL)</span>' : `[${nextRear}]`}</strong></span>
            </div>
            <div class="hud-item">
                <span class="hud-label">Next Dequeue Slot (Front):</span>
                <span class="hud-formula"><strong>${this.isEmpty() ? '<span style="color: #f59e0b;">UNDERFLOW (EMPTY)</span>' : currentFront}</strong> (Next Front &rarr; <code>${nextFrontAfterDeq}</code>)</span>
            </div>
            <div class="hud-item full-row">
                <span class="hud-label">Overflow Check Formula:</span>
                <span class="hud-formula">${fullCheck}</span>
            </div>
        `;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

/**
 * CPU Round-Robin Task Scheduler Simulator using Circular Queue
 */
class RoundRobinScheduler {
    constructor() {
        this.timeQuantum = 2;
        this.tasks = [];
        this.queue = [];
        this.running = false;
        this.timer = null;
        this.currentTask = null;
        this.completedTasks = [];
        this.timeStep = 0;
    }

    init() {
        this.container = document.getElementById('rr-tasks-container');
        this.activeTaskEl = document.getElementById('rr-active-task');
        this.completedEl = document.getElementById('rr-completed-container');
        this.timeQuantumEl = document.getElementById('rr-quantum-val');
        this.timelineEl = document.getElementById('rr-timeline-log');
        this.reset();
    }

    reset() {
        this.running = false;
        clearTimeout(this.timer);
        this.timeStep = 0;
        this.completedTasks = [];
        this.currentTask = null;

        // Default set of tasks
        this.tasks = [
            { id: 'P1', name: 'Task P1 (DB Sync)', burst: 5, remaining: 5, color: '#38bdf8' },
            { id: 'P2', name: 'Task P2 (Audio Stream)', burst: 3, remaining: 3, color: '#00f5a0' },
            { id: 'P3', name: 'Task P3 (Render 3D)', burst: 6, remaining: 6, color: '#f43f5e' },
            { id: 'P4', name: 'Task P4 (Network Ping)', burst: 2, remaining: 2, color: '#eab308' }
        ];

        this.queue = [...this.tasks.map(t => ({ ...t }))];
        this.render();
        if (this.timelineEl) {
            this.timelineEl.innerHTML = '<div class="timeline-entry info">Scheduler reset. Press "Start Scheduler" to execute Round-Robin.</div>';
        }
    }

    start() {
        if (this.running) return;
        this.running = true;
        this.logTimeline('Round-Robin CPU Scheduling started with Time Quantum = ' + this.timeQuantum + ' units.', 'start');
        this.step();
    }

    pause() {
        this.running = false;
        clearTimeout(this.timer);
        this.logTimeline('Scheduler paused.', 'info');
    }

    step() {
        if (!this.running) return;

        if (this.queue.length === 0) {
            this.running = false;
            this.currentTask = null;
            this.render();
            this.logTimeline('All tasks completed execution! CPU is IDLE.', 'done');
            window.soundEngine.playSuccess();
            return;
        }

        // Dequeue from front of circular task queue
        this.currentTask = this.queue.shift();
        const executeTime = Math.min(this.timeQuantum, this.currentTask.remaining);
        this.currentTask.remaining -= executeTime;
        this.timeStep += executeTime;

        window.soundEngine.playPeek();
        this.render();

        this.logTimeline(
            `CPU Executing [${this.currentTask.id}] for ${executeTime} units (Remaining: ${this.currentTask.remaining})`,
            'exec'
        );

        this.timer = setTimeout(() => {
            if (this.currentTask.remaining > 0) {
                this.logTimeline(`Time slice expired for [${this.currentTask.id}] &rarr; Re-enqueued to back of Circular Queue!`, 're-enqueue');
                window.soundEngine.playEnqueue();
                this.queue.push(this.currentTask);
            } else {
                this.logTimeline(`[${this.currentTask.id}] FINISHED! Removed from queue.`, 'done');
                window.soundEngine.playPop();
                this.completedTasks.push(this.currentTask);
            }

            this.currentTask = null;
            this.render();

            if (this.running) {
                this.timer = setTimeout(() => this.step(), 600);
            }
        }, 1100);
    }

    logTimeline(msg, type) {
        if (!this.timelineEl) return;
        const entry = document.createElement('div');
        entry.className = `timeline-entry type-${type}`;
        entry.innerHTML = `<span class="time-stamp">T=${this.timeStep}:</span> ${msg}`;
        this.timelineEl.appendChild(entry);
        this.timelineEl.scrollTop = this.timelineEl.scrollHeight;
    }

    render() {
        if (this.timeQuantumEl) {
            this.timeQuantumEl.textContent = this.timeQuantum;
        }

        // Render queue
        if (this.container) {
            if (this.queue.length === 0) {
                this.container.innerHTML = '<div class="empty-queue-msg">Ready queue is empty</div>';
            } else {
                this.container.innerHTML = this.queue.map((task, idx) => `
                    <div class="rr-task-card" style="border-left: 4px solid ${task.color}">
                        <div class="task-head">
                            <span class="task-id">${task.id}</span>
                            <span class="task-pos">${idx === 0 ? 'FRONT &rarr;' : '#' + idx}</span>
                        </div>
                        <div class="task-name">${task.name}</div>
                        <div class="task-bar-wrap">
                            <div class="task-bar-fill" style="width: ${(task.remaining / task.burst) * 100}%; background: ${task.color}"></div>
                        </div>
                        <div class="task-foot">Remaining: <strong>${task.remaining} / ${task.burst}</strong></div>
                    </div>
                `).join('');
            }
        }

        // Render Active CPU Core
        if (this.activeTaskEl) {
            if (this.currentTask) {
                this.activeTaskEl.innerHTML = `
                    <div class="cpu-core-active" style="border-color: ${this.currentTask.color}">
                        <div class="core-pulse" style="background: ${this.currentTask.color}"></div>
                        <span class="core-label">RUNNING IN CPU CORE</span>
                        <span class="core-task-id">${this.currentTask.id}</span>
                        <span class="core-task-name">${this.currentTask.name}</span>
                        <span class="core-task-burst">Remaining Burst: ${this.currentTask.remaining}</span>
                    </div>
                `;
            } else {
                this.activeTaskEl.innerHTML = `
                    <div class="cpu-core-idle">
                        <span class="idle-icon">&empty;</span>
                        <span class="idle-text">CPU Core Idle</span>
                    </div>
                `;
            }
        }

        // Render Completed
        if (this.completedEl) {
            if (this.completedTasks.length === 0) {
                this.completedEl.innerHTML = '<div class="empty-completed-msg">No tasks completed yet</div>';
            } else {
                this.completedEl.innerHTML = this.completedTasks.map(t => `
                    <span class="completed-pill" style="border-color: ${t.color}">
                        &check; ${t.id} (${t.burst} units)
                    </span>
                `).join('');
            }
        }
    }
}

window.circularQueueEngine = new CircularQueueEngine();
window.roundRobinScheduler = new RoundRobinScheduler();
