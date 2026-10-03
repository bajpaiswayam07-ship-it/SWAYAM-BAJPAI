/**
 * Main Application Orchestrator
 */
class AppController {
    constructor() {
        this.activeTab = 'stack';
        this.activeLang = 'cpp';
        this.logEntries = [];
        this.quizState = {
            currentQuestion: 0,
            score: 0
        };
    }

    init() {
        // Setup Tabs
        const tabBtns = document.querySelectorAll('.nav-tab-btn');
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const target = btn.dataset.tab;
                this.switchTab(target);
            });
        });

        // Initialize Engines
        window.stackEngine.init();
        window.circularQueueEngine.init();
        window.parenthesesChecker.init();
        window.roundRobinScheduler.init();

        // Setup Controls & Listeners
        this.setupStackControls();
        this.setupCircularQueueControls();
        this.setupCodeExplorer();
        this.setupGlobalControls();
        this.setupQuiz();

        // Render initial Code snippet
        this.renderCode();

        this.log('Stack & Circular Queue Interactive Suite initialized.', 'success');
        this.log('Tip: Try keyboard shortcut [Enter] to push/enqueue and [Delete] to pop/dequeue.', 'info');
    }

    switchTab(tabId) {
        this.activeTab = tabId;

        // Update tab buttons
        document.querySelectorAll('.nav-tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabId);
        });

        // Update sections
        document.querySelectorAll('.app-section').forEach(sec => {
            sec.classList.toggle('active', sec.id === `section-${tabId}`);
        });

        window.soundEngine.playPeek();
        this.log(`Switched to tab: ${tabId.toUpperCase()}`, 'info');

        // Re-render components if needed
        if (tabId === 'circularQueue') {
            window.circularQueueEngine.render();
        } else if (tabId === 'stack') {
            window.stackEngine.render();
        } else if (tabId === 'code') {
            this.renderCode();
        }
    }

    setupStackControls() {
        const pushBtn = document.getElementById('btn-stack-push');
        const popBtn = document.getElementById('btn-stack-pop');
        const peekBtn = document.getElementById('btn-stack-peek');
        const clearBtn = document.getElementById('btn-stack-clear');
        const randomBtn = document.getElementById('btn-stack-random');
        const valInput = document.getElementById('stack-val-input');
        const capSelect = document.getElementById('stack-cap-select');

        if (pushBtn) {
            pushBtn.addEventListener('click', () => {
                const val = valInput.value.trim() || Math.floor(Math.random() * 90 + 10);
                window.stackEngine.push(val);
                valInput.value = '';
                valInput.focus();
            });
        }

        if (popBtn) popBtn.addEventListener('click', () => window.stackEngine.pop());
        if (peekBtn) peekBtn.addEventListener('click', () => window.stackEngine.peek());
        if (clearBtn) clearBtn.addEventListener('click', () => window.stackEngine.clear());
        if (randomBtn) randomBtn.addEventListener('click', () => window.stackEngine.fillRandom());

        if (capSelect) {
            capSelect.addEventListener('change', (e) => {
                window.stackEngine.setCapacity(parseInt(e.target.value, 10));
            });
        }

        if (valInput) {
            valInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    pushBtn.click();
                }
            });
        }

        // Parentheses checker app
        const parenRunBtn = document.getElementById('btn-paren-run');
        const parenClearBtn = document.getElementById('btn-paren-clear');
        const parenInput = document.getElementById('paren-input');
        const sampleBtns = document.querySelectorAll('.paren-preset-btn');

        if (parenRunBtn) parenRunBtn.addEventListener('click', () => window.parenthesesChecker.run());
        if (parenClearBtn) {
            parenClearBtn.addEventListener('click', () => {
                if (parenInput) parenInput.value = '';
                const log = document.getElementById('paren-steps-log');
                if (log) log.innerHTML = '';
                const banner = document.getElementById('paren-result-banner');
                if (banner) {
                    banner.className = 'result-banner idle';
                    banner.innerHTML = 'Enter an expression with brackets <code>() {} []</code> and click "Run Evaluation".';
                }
            });
        }

        sampleBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                if (parenInput) {
                    parenInput.value = btn.dataset.expr;
                    window.parenthesesChecker.run();
                }
            });
        });
    }

    setupCircularQueueControls() {
        const enqBtn = document.getElementById('btn-cq-enqueue');
        const deqBtn = document.getElementById('btn-cq-dequeue');
        const frontBtn = document.getElementById('btn-cq-front');
        const rearBtn = document.getElementById('btn-cq-rear');
        const clearBtn = document.getElementById('btn-cq-clear');
        const wrapDemoBtn = document.getElementById('btn-cq-wrap-demo');
        const valInput = document.getElementById('cq-val-input');
        const capSelect = document.getElementById('cq-cap-select');

        if (enqBtn) {
            enqBtn.addEventListener('click', () => {
                const val = valInput.value.trim() || String.fromCharCode(65 + Math.floor(Math.random() * 26)) + (Math.floor(Math.random() * 9) + 1);
                window.circularQueueEngine.enqueue(val);
                valInput.value = '';
                valInput.focus();
            });
        }

        if (deqBtn) deqBtn.addEventListener('click', () => window.circularQueueEngine.dequeue());
        if (frontBtn) frontBtn.addEventListener('click', () => window.circularQueueEngine.peekFront());
        if (rearBtn) rearBtn.addEventListener('click', () => window.circularQueueEngine.peekRear());
        if (clearBtn) clearBtn.addEventListener('click', () => window.circularQueueEngine.clear());
        if (wrapDemoBtn) wrapDemoBtn.addEventListener('click', () => window.circularQueueEngine.runWrapDemo());

        if (capSelect) {
            capSelect.addEventListener('change', (e) => {
                window.circularQueueEngine.setCapacity(parseInt(e.target.value, 10));
            });
        }

        if (valInput) {
            valInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    enqBtn.click();
                }
            });
        }

        // Round Robin controls
        const rrStartBtn = document.getElementById('btn-rr-start');
        const rrPauseBtn = document.getElementById('btn-rr-pause');
        const rrResetBtn = document.getElementById('btn-rr-reset');

        if (rrStartBtn) rrStartBtn.addEventListener('click', () => window.roundRobinScheduler.start());
        if (rrPauseBtn) rrPauseBtn.addEventListener('click', () => window.roundRobinScheduler.pause());
        if (rrResetBtn) rrResetBtn.addEventListener('click', () => window.roundRobinScheduler.reset());
    }

    setupCodeExplorer() {
        const langBtns = document.querySelectorAll('.lang-pill-btn');
        langBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                langBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.activeLang = btn.dataset.lang;
                this.renderCode();
                window.soundEngine.playPeek();
            });
        });

        const dsPillBtns = document.querySelectorAll('.ds-code-pill');
        dsPillBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                dsPillBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.activeDsCode = btn.dataset.ds;
                this.renderCode();
                window.soundEngine.playPeek();
            });
        });
        this.activeDsCode = 'stack';

        const copyBtn = document.getElementById('btn-copy-code');
        if (copyBtn) {
            copyBtn.addEventListener('click', () => {
                const codeSnippet = window.CODE_SNIPPETS[this.activeDsCode][this.activeLang];
                navigator.clipboard.writeText(codeSnippet).then(() => {
                    const originalText = copyBtn.innerHTML;
                    copyBtn.innerHTML = '&#10003; Copied!';
                    window.soundEngine.playSuccess();
                    setTimeout(() => {
                        copyBtn.innerHTML = originalText;
                    }, 1800);
                });
            });
        }
    }

    renderCode() {
        const codeDisplay = document.getElementById('code-display-block');
        if (!codeDisplay) return;

        const rawCode = window.CODE_SNIPPETS[this.activeDsCode][this.activeLang];
        codeDisplay.innerHTML = this.highlightSyntax(rawCode);
    }

    highlightCode(ds, action) {
        // Visual indicator that code responded to user action
        const codeSection = document.getElementById('code-display-block');
        if (!codeSection) return;

        codeSection.classList.add('pulse-glow');
        setTimeout(() => codeSection.classList.remove('pulse-glow'), 600);
    }

    highlightSyntax(code) {
        // Escaping HTML
        let escaped = code
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');

        // Simple and robust regex syntax highlighter
        // Comments
        escaped = escaped.replace(/(\/\/[^\n]*)/g, '<span class="tok-comment">$1</span>');
        escaped = escaped.replace(/(#[^\n]*)/g, '<span class="tok-comment">$1</span>');

        // Keywords
        const keywords = /\b(class|public|private|int|bool|void|return|if|else|throw|new|constructor|def|self|const|let|var|None|true|false|True|False)\b/g;
        escaped = escaped.replace(keywords, '<span class="tok-keyword">$1</span>');

        // Strings
        escaped = escaped.replace(/(".*?"|'.*?')/g, '<span class="tok-string">$1</span>');

        // Numbers
        escaped = escaped.replace(/\b(\d+)\b/g, '<span class="tok-number">$1</span>');

        // Functions
        escaped = escaped.replace(/\b([a-zA-Z_]\w*)\s*(?=\()/g, '<span class="tok-func">$1</span>');

        return escaped;
    }

    setupGlobalControls() {
        // Developer Badge Hacker FX
        const devBtn = document.getElementById('btn-dev-hacker');
        if (devBtn) {
            devBtn.addEventListener('click', () => {
                window.soundEngine.playHacker();
                this.log('⚡ [ROOT ACCESS] LEAD DEVELOPER & ARCHITECT: SWAYAM BAJPAI', 'success');
                devBtn.classList.add('pulse-glow');
                setTimeout(() => devBtn.classList.remove('pulse-glow'), 800);
            });
        }

        // Sound Mute Toggle
        const soundBtn = document.getElementById('btn-sound-toggle');
        if (soundBtn) {
            soundBtn.addEventListener('click', () => {
                const enabled = window.soundEngine.toggle();
                soundBtn.classList.toggle('muted', !enabled);
                soundBtn.innerHTML = enabled ? '&#128266; Sound: ON' : '&#128263; Sound: OFF';
                this.log(`Audio effects ${enabled ? 'ENABLED' : 'MUTED'}`, 'info');
                if (enabled) window.soundEngine.playSuccess();
            });
        }

        // Clear Log
        const clearLogBtn = document.getElementById('btn-clear-logs');
        if (clearLogBtn) {
            clearLogBtn.addEventListener('click', () => {
                const logContainer = document.getElementById('activity-terminal-body');
                if (logContainer) logContainer.innerHTML = '';
                this.log('Activity terminal logs cleared.', 'info');
            });
        }

        // Global Keyboard Shortcuts
        document.addEventListener('keydown', (e) => {
            // Ignore if active typing inside text inputs
            if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
                return;
            }

            if (e.key === 'Enter') {
                if (this.activeTab === 'stack') {
                    const btn = document.getElementById('btn-stack-push');
                    if (btn) btn.click();
                } else if (this.activeTab === 'circularQueue') {
                    const btn = document.getElementById('btn-cq-enqueue');
                    if (btn) btn.click();
                }
            } else if (e.key === 'Delete' || e.key === 'Backspace') {
                if (this.activeTab === 'stack') {
                    const btn = document.getElementById('btn-stack-pop');
                    if (btn) btn.click();
                } else if (this.activeTab === 'circularQueue') {
                    const btn = document.getElementById('btn-cq-dequeue');
                    if (btn) btn.click();
                }
            } else if (e.key === '1') {
                this.switchTab('stack');
            } else if (e.key === '2') {
                this.switchTab('circularQueue');
            } else if (e.key === '3') {
                this.switchTab('apps');
            } else if (e.key === '4') {
                this.switchTab('code');
            } else if (e.key === '5') {
                this.switchTab('quiz');
            } else if (e.key === 'h' || e.key === 'H') {
                const devBtn = document.getElementById('btn-dev-hacker');
                if (devBtn) devBtn.click();
            }
        });
    }

    log(msg, type = 'info') {
        const body = document.getElementById('activity-terminal-body');
        if (!body) return;

        const time = new Date().toLocaleTimeString();
        const entry = document.createElement('div');
        entry.className = `term-entry term-${type}`;
        entry.innerHTML = `<span class="term-time">[${time}]</span> <span class="term-type">${type.toUpperCase()}:</span> <span class="term-text">${msg}</span>`;

        body.appendChild(entry);
        body.scrollTop = body.scrollHeight;
    }

    setupQuiz() {
        const questions = [
            {
                q: "What principle governs the behavior of a Stack?",
                options: ["FIFO (First In First Out)", "LIFO (Last In First Out)", "Random Access", "Priority Based"],
                correct: 1,
                explanation: "Stack operates strictly on LIFO (Last In, First Out). The most recently added element is always the first one to be popped."
            },
            {
                q: "In a Circular Queue of capacity N, what formula calculates the next position of the REAR pointer?",
                options: ["(rear + 1)", "(rear - 1) % N", "(rear + 1) % N", "(rear + N) % 2"],
                correct: 2,
                explanation: "(rear + 1) % N wraps the rear pointer around to 0 when it exceeds N - 1."
            },
            {
                q: "What major flaw of a linear array queue does a Circular Queue solve?",
                options: ["Slow O(N) peek time", "Wastage of memory at front slots after dequeuing", "Inability to hold strings", "Requires linked lists"],
                correct: 1,
                explanation: "In a linear queue, dequeuing leaves empty front slots that cannot be reused without an expensive O(N) shift. Circular Queue reuses them via wrap-around modulo arithmetic!"
            },
            {
                q: "What is the Time Complexity of Push and Pop in a Stack, and Enqueue and Dequeue in a Circular Queue?",
                options: ["O(N) for all", "O(log N) for all", "O(1) constant time for all", "O(N²)"],
                correct: 2,
                explanation: "All core operations in both Stack and Circular Queue run in optimal O(1) constant time because they directly operate on top or front/rear pointers."
            },
            {
                q: "When checking balanced parentheses like '{[()]}', what action is taken when an opening bracket is encountered?",
                options: ["Pop from stack", "Push onto stack", "Clear stack", "Reverse string"],
                correct: 1,
                explanation: "Opening brackets are pushed onto the stack. When a closing bracket arrives, it is checked against the popped top bracket."
            }
        ];

        this.quizData = questions;
        this.renderQuizQuestion();

        const nextBtn = document.getElementById('btn-quiz-next');
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                this.quizState.currentQuestion++;
                if (this.quizState.currentQuestion >= this.quizData.length) {
                    this.renderQuizScore();
                } else {
                    this.renderQuizQuestion();
                }
            });
        }

        const resetBtn = document.getElementById('btn-quiz-reset');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                this.quizState.currentQuestion = 0;
                this.quizState.score = 0;
                this.renderQuizQuestion();
            });
        }
    }

    renderQuizQuestion() {
        const qContainer = document.getElementById('quiz-question-box');
        const nextBtn = document.getElementById('btn-quiz-next');
        const scoreCard = document.getElementById('quiz-score-card');
        if (!qContainer) return;

        if (scoreCard) scoreCard.style.display = 'none';
        qContainer.style.display = 'block';
        if (nextBtn) nextBtn.style.display = 'none';

        const q = this.quizData[this.quizState.currentQuestion];
        const progress = `Question ${this.quizState.currentQuestion + 1} of ${this.quizData.length}`;

        qContainer.innerHTML = `
            <div class="quiz-badge">${progress}</div>
            <h3 class="quiz-title">${q.q}</h3>
            <div class="quiz-options-list">
                ${q.options.map((opt, idx) => `
                    <button class="quiz-opt-btn" data-index="${idx}">
                        <span class="opt-letter">${String.fromCharCode(65 + idx)}</span>
                        <span class="opt-label">${opt}</span>
                    </button>
                `).join('')}
            </div>
            <div id="quiz-feedback-box" class="quiz-feedback" style="display:none;"></div>
        `;

        const optBtns = qContainer.querySelectorAll('.quiz-opt-btn');
        optBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const selected = parseInt(btn.dataset.index, 10);
                const feedbackBox = document.getElementById('quiz-feedback-box');
                optBtns.forEach(b => b.disabled = true);

                if (selected === q.correct) {
                    btn.classList.add('correct');
                    this.quizState.score++;
                    feedbackBox.className = 'quiz-feedback success';
                    feedbackBox.innerHTML = `<strong>&check; Correct!</strong> ${q.explanation}`;
                    window.soundEngine.playSuccess();
                } else {
                    btn.classList.add('wrong');
                    optBtns[q.correct].classList.add('correct');
                    feedbackBox.className = 'quiz-feedback error';
                    feedbackBox.innerHTML = `<strong>&cross; Incorrect!</strong> ${q.explanation}`;
                    window.soundEngine.playError();
                }

                feedbackBox.style.display = 'block';
                if (nextBtn) nextBtn.style.display = 'inline-flex';
            });
        });
    }

    renderQuizScore() {
        const qContainer = document.getElementById('quiz-question-box');
        const nextBtn = document.getElementById('btn-quiz-next');
        const scoreCard = document.getElementById('quiz-score-card');
        if (!scoreCard) return;

        if (qContainer) qContainer.style.display = 'none';
        if (nextBtn) nextBtn.style.display = 'none';
        scoreCard.style.display = 'block';

        const total = this.quizData.length;
        const score = this.quizState.score;
        const pct = Math.round((score / total) * 100);

        scoreCard.innerHTML = `
            <div class="score-trophy">${pct >= 80 ? '&#127942;' : (pct >= 60 ? '&#128079;' : '&#128161;')}</div>
            <h2 class="score-title">Challenge Completed!</h2>
            <div class="score-val">${score} / ${total}</div>
            <p class="score-pct">${pct}% Correct</p>
            <p class="score-eval">${pct >= 80 ? 'Mastery Achieved! You understand Stack & Circular Queue fundamentals thoroughly.' : 'Good effort! Review the algorithms tab and run a few simulations to solidify your concepts.'}</p>
        `;
        window.soundEngine.playSuccess();
    }
}

window.app = new AppController();
document.addEventListener('DOMContentLoaded', () => {
    window.app.init();
});
