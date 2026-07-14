// ---- Configuration ----
// Change this if your FastAPI server runs on a different host/port.
const API_BASE = "http://127.0.0.1:8080";
const POLL_INTERVAL_MS = 3000;

// ---- Element refs ----
const board = document.getElementById("board");
const emptyState = document.getElementById("emptyState");
const composer = document.getElementById("composer");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const statusDot = document.getElementById("statusDot");
const statusLabel = document.getElementById("statusLabel");

let lastRenderedCount = 0;
let pollTimer = null;

// ---- Rendering ----
function renderMessages(messages) {
  // Avoid re-rendering (and re-animating) if nothing changed.
  if (messages.length === lastRenderedCount) return;
  lastRenderedCount = messages.length;

  board.querySelectorAll(".bubble").forEach((el) => el.remove());

  if (messages.length === 0) {
    emptyState.style.display = "block";
    return;
  }

  emptyState.style.display = "none";

  messages.forEach((text, index) => {
    const bubble = document.createElement("div");
    bubble.className = "bubble" + (index === messages.length - 1 ? " latest" : "");
    bubble.textContent = text;
    board.appendChild(bubble);
  });

  board.scrollTop = board.scrollHeight;
}

function setStatus(online) {
  statusDot.classList.toggle("online", online);
  statusDot.classList.toggle("offline", !online);
  statusLabel.textContent = online ? "Live" : "Offline";
}

// ---- API calls ----
async function fetchAllMessages() {
  try {
    const res = await fetch(`${API_BASE}/read/all`);
    if (!res.ok) throw new Error("Bad response");
    const data = await res.json();
    setStatus(true);
    renderMessages(data);
  } catch (err) {
    setStatus(false);
  }
}

async function sendMessage(text) {
  sendBtn.disabled = true;
  try {
    const res = await fetch(`${API_BASE}/send`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    if (!res.ok) throw new Error("Send failed");
    await fetchAllMessages();
    lastRenderedCount = -1; // force re-render even if count matches by coincidence
    await fetchAllMessages();
    setStatus(true);
  } catch (err) {
    setStatus(false);
  } finally {
    sendBtn.disabled = false;
  }
}

// ---- Events ----
composer.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = messageInput.value.trim();
  if (!text) return;
  messageInput.value = "";
  sendMessage(text);
});

// ---- Polling ----
function startPolling() {
  fetchAllMessages();
  pollTimer = setInterval(fetchAllMessages, POLL_INTERVAL_MS);
}

document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    clearInterval(pollTimer);
  } else {
    startPolling();
  }
});

startPolling();
