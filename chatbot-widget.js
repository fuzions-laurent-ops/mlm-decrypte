/**
 * MLM Décrypté — Widget Chatbot
 *
 * Widget frontend prêt à être connecté à un backend LLM open source.
 * Inclure ce script dans n'importe quelle page :
 *   <script src="/chatbot-widget.js" defer></script>
 *
 * CONFIGURATION BACKEND :
 * Modifier CHATBOT_API_URL ci-dessous pour pointer vers votre API.
 * L'API doit accepter POST avec { "message": "..." }
 * et retourner { "reply": "...", "articles": [{ "title": "...", "url": "..." }] }
 */

(function () {
  'use strict';

  // ══════════════════════════════════════════════
  //  CONFIGURATION — À modifier par ton ami
  // ══════════════════════════════════════════════
  const CHATBOT_API_URL = '/api/chat'; // URL de l'API backend LLM
  const BOT_NAME = 'MLM Assistant';
  const WELCOME_MESSAGE = 'Salut ! 👋 Je suis l\'assistant MLM Décrypté. Pose-moi une question sur le marketing de réseau et je te guiderai vers les articles qui y répondent.';
  const SUGGESTED_QUESTIONS = [
    'Le MLM, c\'est une arnaque ?',
    'Comment bien démarrer en MLM ?',
    'Quelle différence avec Ponzi ?',
    'Peut-on vraiment vivre du MLM ?'
  ];
  const ERROR_MESSAGE = 'Désolé, je n\'ai pas pu traiter ta question. Réessaie dans un instant.';
  const PLACEHOLDER_TEXT = 'Pose ta question ici…';

  // ══════════════════════════════════════════════
  //  STYLES
  // ══════════════════════════════════════════════
  const STYLES = `
    /* ─── Chatbot Widget ─── */
    #mlm-chatbot-toggle {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 9999;
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background: linear-gradient(135deg, #1a5c44, #0d3b2e);
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 20px rgba(13, 59, 46, 0.35);
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    #mlm-chatbot-toggle:hover {
      transform: scale(1.08);
      box-shadow: 0 6px 28px rgba(13, 59, 46, 0.45);
    }
    #mlm-chatbot-toggle svg {
      width: 28px;
      height: 28px;
      fill: white;
      transition: opacity 0.2s;
    }
    #mlm-chatbot-toggle .icon-close { display: none; }
    #mlm-chatbot-toggle.is-open .icon-chat { display: none; }
    #mlm-chatbot-toggle.is-open .icon-close { display: block; }

    /* Notification dot */
    #mlm-chatbot-toggle::after {
      content: '';
      position: absolute;
      top: 6px;
      right: 6px;
      width: 14px;
      height: 14px;
      background: #e8a020;
      border-radius: 50%;
      border: 2.5px solid white;
      transition: opacity 0.3s;
    }
    #mlm-chatbot-toggle.is-open::after,
    #mlm-chatbot-toggle.seen::after {
      opacity: 0;
    }

    /* ─── Chat Window ─── */
    #mlm-chatbot-window {
      position: fixed;
      bottom: 100px;
      right: 24px;
      z-index: 9998;
      width: 380px;
      max-width: calc(100vw - 32px);
      height: 520px;
      max-height: calc(100vh - 140px);
      background: #fff;
      border-radius: 20px;
      box-shadow: 0 12px 48px rgba(0,0,0,0.18);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      opacity: 0;
      transform: translateY(20px) scale(0.95);
      pointer-events: none;
      transition: opacity 0.3s ease, transform 0.3s ease;
    }
    #mlm-chatbot-window.is-open {
      opacity: 1;
      transform: translateY(0) scale(1);
      pointer-events: auto;
    }

    /* ─── Header ─── */
    .mlm-cb-header {
      background: linear-gradient(135deg, #1a5c44, #0d3b2e);
      color: white;
      padding: 18px 20px;
      display: flex;
      align-items: center;
      gap: 12px;
      flex-shrink: 0;
    }
    .mlm-cb-avatar {
      width: 40px;
      height: 40px;
      background: rgba(255,255,255,0.18);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.2rem;
      flex-shrink: 0;
    }
    .mlm-cb-header-info h3 {
      font-family: 'Inter', sans-serif;
      font-size: 0.95rem;
      font-weight: 700;
      margin: 0;
      line-height: 1.3;
    }
    .mlm-cb-header-info p {
      font-size: 0.75rem;
      opacity: 0.75;
      margin: 0;
      line-height: 1.3;
    }

    /* ─── Messages area ─── */
    .mlm-cb-messages {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      background: #faf8f3;
    }
    .mlm-cb-messages::-webkit-scrollbar { width: 5px; }
    .mlm-cb-messages::-webkit-scrollbar-track { background: transparent; }
    .mlm-cb-messages::-webkit-scrollbar-thumb { background: #c4c4c4; border-radius: 10px; }

    /* ─── Bubbles ─── */
    .mlm-cb-msg {
      max-width: 85%;
      padding: 12px 16px;
      border-radius: 16px;
      font-size: 0.88rem;
      line-height: 1.55;
      font-family: 'Inter', sans-serif;
      word-wrap: break-word;
    }
    .mlm-cb-msg--bot {
      background: white;
      color: #1a1a2e;
      border-bottom-left-radius: 4px;
      align-self: flex-start;
      box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .mlm-cb-msg--user {
      background: linear-gradient(135deg, #1a5c44, #0d3b2e);
      color: white;
      border-bottom-right-radius: 4px;
      align-self: flex-end;
    }

    /* ─── Article links ─── */
    .mlm-cb-articles {
      margin-top: 8px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .mlm-cb-article-link {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      background: #f0faf4;
      border: 1px solid #d4f0e4;
      border-radius: 10px;
      font-size: 0.82rem;
      font-weight: 600;
      color: #1a5c44;
      text-decoration: none;
      transition: background 0.2s, transform 0.15s;
    }
    .mlm-cb-article-link:hover {
      background: #d4f0e4;
      transform: translateX(3px);
    }
    .mlm-cb-article-link::before {
      content: '📄';
      flex-shrink: 0;
    }

    /* ─── Suggested questions ─── */
    .mlm-cb-suggestions {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 10px;
    }
    .mlm-cb-suggestion {
      padding: 7px 14px;
      background: white;
      border: 1.5px solid #d4f0e4;
      border-radius: 20px;
      font-size: 0.78rem;
      font-weight: 500;
      color: #1a5c44;
      cursor: pointer;
      transition: all 0.2s;
      font-family: 'Inter', sans-serif;
    }
    .mlm-cb-suggestion:hover {
      background: #1a5c44;
      color: white;
      border-color: #1a5c44;
    }

    /* ─── Typing indicator ─── */
    .mlm-cb-typing {
      display: none;
      align-self: flex-start;
      padding: 12px 18px;
      background: white;
      border-radius: 16px;
      border-bottom-left-radius: 4px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .mlm-cb-typing.is-visible { display: flex; gap: 5px; align-items: center; }
    .mlm-cb-typing span {
      width: 7px;
      height: 7px;
      background: #9a9aaa;
      border-radius: 50%;
      animation: mlm-cb-bounce 1.4s infinite ease-in-out;
    }
    .mlm-cb-typing span:nth-child(2) { animation-delay: 0.16s; }
    .mlm-cb-typing span:nth-child(3) { animation-delay: 0.32s; }
    @keyframes mlm-cb-bounce {
      0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
      40% { transform: scale(1); opacity: 1; }
    }

    /* ─── Input area ─── */
    .mlm-cb-input-area {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px 16px;
      border-top: 1px solid #eee;
      background: white;
      flex-shrink: 0;
    }
    .mlm-cb-input {
      flex: 1;
      border: 1.5px solid #e0e0e0;
      border-radius: 24px;
      padding: 10px 18px;
      font-size: 0.88rem;
      font-family: 'Inter', sans-serif;
      outline: none;
      transition: border-color 0.2s;
      color: #1a1a2e;
      background: #faf8f3;
    }
    .mlm-cb-input::placeholder { color: #9a9aaa; }
    .mlm-cb-input:focus { border-color: #1a5c44; }
    .mlm-cb-send {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      border: none;
      background: linear-gradient(135deg, #1a5c44, #0d3b2e);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      transition: transform 0.2s, opacity 0.2s;
    }
    .mlm-cb-send:hover { transform: scale(1.08); }
    .mlm-cb-send:disabled { opacity: 0.4; cursor: default; transform: none; }
    .mlm-cb-send svg { width: 18px; height: 18px; fill: white; }

    /* ─── Footer branding ─── */
    .mlm-cb-footer {
      text-align: center;
      padding: 6px;
      font-size: 0.65rem;
      color: #9a9aaa;
      background: white;
      border-top: 1px solid #f0f0f0;
    }

    /* ─── Mobile ─── */
    @media (max-width: 480px) {
      #mlm-chatbot-window {
        bottom: 0;
        right: 0;
        width: 100vw;
        max-width: 100vw;
        height: calc(100vh - 70px);
        max-height: calc(100vh - 70px);
        border-radius: 20px 20px 0 0;
      }
      #mlm-chatbot-toggle {
        bottom: 16px;
        right: 16px;
        width: 54px;
        height: 54px;
      }
    }
  `;

  // ══════════════════════════════════════════════
  //  HTML
  // ══════════════════════════════════════════════
  const HTML = `
    <button id="mlm-chatbot-toggle" aria-label="Ouvrir le chat">
      <svg class="icon-chat" viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.2L4 17.2V4h16v12z"/><path d="M7 9h10v2H7zm0-3h10v2H7z"/></svg>
      <svg class="icon-close" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
    </button>

    <div id="mlm-chatbot-window">
      <div class="mlm-cb-header">
        <div class="mlm-cb-avatar">💬</div>
        <div class="mlm-cb-header-info">
          <h3>${BOT_NAME}</h3>
          <p>Pose ta question, je te guide !</p>
        </div>
      </div>

      <div class="mlm-cb-messages" id="mlm-cb-messages">
        <!-- Messages will be inserted here -->
      </div>

      <div class="mlm-cb-input-area">
        <input type="text" class="mlm-cb-input" id="mlm-cb-input" placeholder="${PLACEHOLDER_TEXT}" autocomplete="off" />
        <button class="mlm-cb-send" id="mlm-cb-send" aria-label="Envoyer" disabled>
          <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
        </button>
      </div>

      <div class="mlm-cb-footer">MLM Décrypté — Assistant IA</div>
    </div>
  `;

  // ══════════════════════════════════════════════
  //  INIT
  // ══════════════════════════════════════════════
  function init() {
    // Inject styles
    var styleEl = document.createElement('style');
    styleEl.textContent = STYLES;
    document.head.appendChild(styleEl);

    // Inject HTML
    var wrapper = document.createElement('div');
    wrapper.id = 'mlm-chatbot-wrapper';
    wrapper.innerHTML = HTML;
    document.body.appendChild(wrapper);

    // DOM refs
    var toggle = document.getElementById('mlm-chatbot-toggle');
    var chatWindow = document.getElementById('mlm-chatbot-window');
    var messagesEl = document.getElementById('mlm-cb-messages');
    var inputEl = document.getElementById('mlm-cb-input');
    var sendBtn = document.getElementById('mlm-cb-send');
    var isOpen = false;

    // Toggle chat
    toggle.addEventListener('click', function () {
      isOpen = !isOpen;
      toggle.classList.toggle('is-open', isOpen);
      toggle.classList.add('seen');
      chatWindow.classList.toggle('is-open', isOpen);
      if (isOpen) {
        inputEl.focus();
        // Show welcome on first open
        if (messagesEl.children.length === 0) {
          showWelcome();
        }
      }
    });

    // Close on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && isOpen) {
        toggle.click();
      }
    });

    // Input handling
    inputEl.addEventListener('input', function () {
      sendBtn.disabled = !inputEl.value.trim();
    });

    inputEl.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !sendBtn.disabled) {
        sendMessage();
      }
    });

    sendBtn.addEventListener('click', sendMessage);

    // ── Show Welcome ──
    function showWelcome() {
      addBotMessage(WELCOME_MESSAGE);
      addSuggestions();
    }

    // ── Add a bot message ──
    function addBotMessage(text, articles) {
      var msgEl = document.createElement('div');
      msgEl.className = 'mlm-cb-msg mlm-cb-msg--bot';
      msgEl.textContent = text;

      if (articles && articles.length > 0) {
        var linksWrap = document.createElement('div');
        linksWrap.className = 'mlm-cb-articles';
        articles.forEach(function (a) {
          var link = document.createElement('a');
          link.className = 'mlm-cb-article-link';
          link.href = a.url;
          link.textContent = a.title;
          link.target = '_self';
          linksWrap.appendChild(link);
        });
        msgEl.appendChild(linksWrap);
      }

      messagesEl.appendChild(msgEl);
      scrollToBottom();
    }

    // ── Add a user message ──
    function addUserMessage(text) {
      var msgEl = document.createElement('div');
      msgEl.className = 'mlm-cb-msg mlm-cb-msg--user';
      msgEl.textContent = text;
      messagesEl.appendChild(msgEl);
      scrollToBottom();
    }

    // ── Add suggested questions ──
    function addSuggestions() {
      var wrap = document.createElement('div');
      wrap.className = 'mlm-cb-suggestions';
      SUGGESTED_QUESTIONS.forEach(function (q) {
        var btn = document.createElement('button');
        btn.className = 'mlm-cb-suggestion';
        btn.textContent = q;
        btn.addEventListener('click', function () {
          wrap.remove();
          inputEl.value = q;
          sendBtn.disabled = false;
          sendMessage();
        });
        wrap.appendChild(btn);
      });
      messagesEl.appendChild(wrap);
      scrollToBottom();
    }

    // ── Typing indicator ──
    function showTyping() {
      var el = document.createElement('div');
      el.className = 'mlm-cb-typing is-visible';
      el.id = 'mlm-cb-typing';
      el.innerHTML = '<span></span><span></span><span></span>';
      messagesEl.appendChild(el);
      scrollToBottom();
    }

    function hideTyping() {
      var el = document.getElementById('mlm-cb-typing');
      if (el) el.remove();
    }

    // ── Send message ──
    function sendMessage() {
      var text = inputEl.value.trim();
      if (!text) return;

      // Remove suggestion buttons if present
      var suggestions = messagesEl.querySelector('.mlm-cb-suggestions');
      if (suggestions) suggestions.remove();

      addUserMessage(text);
      inputEl.value = '';
      sendBtn.disabled = true;
      inputEl.disabled = true;

      showTyping();

      callAPI(text)
        .then(function (data) {
          hideTyping();
          addBotMessage(data.reply, data.articles || []);
          inputEl.disabled = false;
          inputEl.focus();
        })
        .catch(function () {
          hideTyping();
          addBotMessage(ERROR_MESSAGE);
          inputEl.disabled = false;
          inputEl.focus();
        });
    }

    // ── API Call ──
    function callAPI(message) {
      return fetch(CHATBOT_API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
      })
        .then(function (res) {
          if (!res.ok) throw new Error('API error');
          return res.json();
        });
    }

    // ── Scroll ──
    function scrollToBottom() {
      requestAnimationFrame(function () {
        messagesEl.scrollTop = messagesEl.scrollHeight;
      });
    }
  }

  // Launch when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
