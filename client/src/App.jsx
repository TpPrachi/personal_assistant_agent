import { useState, useRef, useEffect } from "react";

// ── Theme styles ──────────────────────────────────────────────────
const themes = {
  dark: {
    bg: "#0a0a0f",
    surface: "#1e1e2e",
    surfaceAlt: "#111",
    border: "#222",
    text: "#fff",
    textMuted: "#666",
    textDim: "#888",
    userBubble: "#2563eb",
    thinkingBg: "#0f1a0f",
    thinkingBorder: "#1a3a1a",
    thinkingText: "#4ade80",
    toolBg: "#0a0a1a",
    toolBorder: "#1a1a3a",
    toolText: "#818cf8",
    inputBg: "#1a1a2e",
    inputBorder: "#333",
    btnDisabled: "#333",
  },
  light: {
    bg: "#f8fafc",
    surface: "#ffffff",
    surfaceAlt: "#f1f5f9",
    border: "#e2e8f0",
    text: "#0f172a",
    textMuted: "#94a3b8",
    textDim: "#64748b",
    userBubble: "#2563eb",
    thinkingBg: "#f0fdf4",
    thinkingBorder: "#bbf7d0",
    thinkingText: "#16a34a",
    toolBg: "#f5f3ff",
    toolBorder: "#ddd6fe",
    toolText: "#7c3aed",
    inputBg: "#ffffff",
    inputBorder: "#cbd5e1",
    btnDisabled: "#cbd5e1",
  },
};

// ── Thinking step component ───────────────────────────────────────
function ThinkingStep({ text, t }) {
  return (
    <div style={{
      display: "flex",
      alignItems: "flex-start",
      gap: "8px",
      padding: "8px 12px",
      background: t.thinkingBg,
      border: `1px solid ${t.thinkingBorder}`,
      borderRadius: "8px",
      marginBottom: "6px",
    }}>
      <span style={{ fontSize: "14px" }}>🧠</span>
      <span style={{ fontSize: "13px", color: t.thinkingText, fontFamily: "monospace" }}>
        {text}
      </span>
    </div>
  );
}

// ── Tool result component ─────────────────────────────────────────
function ToolResult({ text, t }) {
  const [expanded, setExpanded] = useState(false);
  return (
    <div style={{
      padding: "8px 12px",
      background: t.toolBg,
      border: `1px solid ${t.toolBorder}`,
      borderRadius: "8px",
      marginBottom: "6px",
      cursor: "pointer",
    }} onClick={() => setExpanded(!expanded)}>
      <div style={{ fontSize: "12px", color: t.toolText, marginBottom: expanded ? "6px" : "0" }}>
        📦 Tool result {expanded ? "▲" : "▼"}
      </div>
      {expanded && (
        <pre style={{
          fontSize: "11px",
          color: t.textDim,
          whiteSpace: "pre-wrap",
          margin: 0,
          maxHeight: "200px",
          overflowY: "auto",
        }}>
          {text}
        </pre>
      )}
    </div>
  );
}

// ── Message component ─────────────────────────────────────────────
function Message({ role, text, steps, streaming, t }) {
  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: role === "user" ? "flex-end" : "flex-start",
      marginBottom: "20px",
    }}>
      {/* Role label */}
      <div style={{
        fontSize: "11px",
        color: t.textMuted,
        marginBottom: "4px",
        paddingLeft: "4px",
      }}>
        {role === "user" ? "You" : "🤖 Agent"}
      </div>

      {/* Thinking steps */}
      {steps && steps.length > 0 && (
        <div style={{ width: "100%", maxWidth: "80%", marginBottom: "8px" }}>
          {steps.map((step, i) =>
            step.type === "thinking"
              ? <ThinkingStep key={i} text={step.text} t={t} />
              : <ToolResult key={i} text={step.text} t={t} />
          )}
        </div>
      )}

      {/* Message bubble */}
      {(text || streaming) && (
        <div style={{
          maxWidth: "80%",
          padding: "12px 16px",
          borderRadius: role === "user"
            ? "18px 18px 4px 18px"
            : "18px 18px 18px 4px",
          background: role === "user" ? t.userBubble : t.surface,
          color: t.text,
          fontSize: "15px",
          lineHeight: "1.6",
          whiteSpace: "pre-wrap",
          border: role === "assistant" ? `1px solid ${t.border}` : "none",
        }}>
          {text}
          {streaming && <span style={{ opacity: 0.4 }}>▌</span>}
        </div>
      )}
    </div>
  );
}

// ── Main App ──────────────────────────────────────────────────────
export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [theme, setTheme] = useState("dark");
  const bottomRef = useRef(null);
  const t = themes[theme];

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function ask(e) {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const question = input.trim();
    setInput("");
    setLoading(true);

    // Add user message
    setMessages(prev => [...prev, { role: "user", text: question }]);

    // Add empty assistant message
    const id = Date.now();
    setMessages(prev => [...prev, {
      id,
      role: "assistant",
      text: "",
      steps: [],
      streaming: true,
    }]);

    const es = new EventSource(
      `http://localhost:8000/api/ask?q=${encodeURIComponent(question)}`
    );

    es.onmessage = (e) => {
      const data = JSON.parse(e.data);

      if (data.type === "thinking" || data.type === "tool_result") {
        setMessages(prev => prev.map(m =>
          m.id === id
            ? { ...m, steps: [...(m.steps || []), data] }
            : m
        ));
      } else if (data.type === "answer") {
        setMessages(prev => prev.map(m =>
          m.id === id ? { ...m, text: data.text } : m
        ));
      } else if (data.type === "done") {
        es.close();
        setLoading(false);
        setMessages(prev => prev.map(m =>
          m.id === id ? { ...m, streaming: false } : m
        ));
      } else if (data.type === "error") {
        es.close();
        setLoading(false);
        setMessages(prev => prev.map(m =>
          m.id === id ? { ...m, text: `Error: ${data.text}`, streaming: false } : m
        ));
      }
    };

    es.onerror = () => {
      es.close();
      setLoading(false);
    };
  }

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      height: "100vh",
      background: t.bg,
      color: t.text,
      fontFamily: "system-ui, sans-serif",
      transition: "all 0.2s",
    }}>
      {/* Header */}
      <div style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "16px 24px",
        borderBottom: `1px solid ${t.border}`,
      }}>
        <div>
          <span style={{ fontSize: "18px", fontWeight: "600" }}>
            🤖 Personal Assistant
          </span>
          <span style={{ fontSize: "12px", color: t.textMuted, marginLeft: "8px" }}>
            Gmail · Calendar · LangGraph
          </span>
        </div>

        {/* Theme toggle */}
        <button
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          style={{
            padding: "6px 12px",
            borderRadius: "8px",
            border: `1px solid ${t.border}`,
            background: t.surface,
            color: t.text,
            cursor: "pointer",
            fontSize: "13px",
          }}
        >
          {theme === "dark" ? "☀️ Light" : "🌙 Dark"}
        </button>
      </div>

      {/* Suggested prompts */}
      {messages.length === 0 && (
        <div style={{ padding: "32px 24px" }}>
          <div style={{
            textAlign: "center",
            color: t.textMuted,
            marginBottom: "32px",
          }}>
            <div style={{ fontSize: "48px", marginBottom: "12px" }}>🤖</div>
            <div style={{ fontSize: "16px" }}>
              Ask me anything about your Gmail or Calendar
            </div>
          </div>

          {/* Quick prompts */}
          <div style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: "10px",
            maxWidth: "600px",
            margin: "0 auto",
          }}>
            {[
              "What are my latest 5 emails?",
              "What meetings do I have this week?",
              "Draft an email to test@example.com saying hello",
              "Create a meeting called Standup tomorrow at 10am to 11am",
            ].map((prompt, i) => (
              <button
                key={i}
                onClick={() => setInput(prompt)}
                style={{
                  padding: "12px 16px",
                  borderRadius: "10px",
                  border: `1px solid ${t.border}`,
                  background: t.surface,
                  color: t.text,
                  cursor: "pointer",
                  fontSize: "13px",
                  textAlign: "left",
                  lineHeight: "1.4",
                }}
              >
                {prompt}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Messages */}
      <div style={{ flex: 1, overflowY: "auto", padding: "24px" }}>
        {messages.map((m, i) => (
          <Message key={i} {...m} t={t} />
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <form onSubmit={ask} style={{
        display: "flex",
        gap: "8px",
        padding: "16px 24px",
        borderTop: `1px solid ${t.border}`,
        background: t.bg,
      }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Ask about your emails or calendar..."
          disabled={loading}
          style={{
            flex: 1,
            padding: "12px 16px",
            borderRadius: "12px",
            border: `1px solid ${t.inputBorder}`,
            background: t.inputBg,
            color: t.text,
            fontSize: "15px",
            outline: "none",
          }}
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          style={{
            padding: "12px 20px",
            borderRadius: "12px",
            border: "none",
            background: loading || !input.trim() ? t.btnDisabled : t.userBubble,
            color: "#fff",
            fontSize: "15px",
            cursor: loading ? "not-allowed" : "pointer",
            minWidth: "48px",
          }}
        >
          {loading ? "⏳" : "→"}
        </button>
      </form>
    </div>
  );
}