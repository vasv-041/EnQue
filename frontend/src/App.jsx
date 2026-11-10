import React, { useState, useEffect, useRef, useCallback } from "react";
import {
  BarChart3, Users, Compass, Brain, FlaskConical, Database, Layers,
  Sparkles, ArrowUpRight, TrendingUp, BookmarkCheck, CheckCircle2,
  RefreshCw, Send, Building2, LogOut, Upload, AlertCircle, Loader2,
  Plus, ChevronDown
} from "lucide-react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from "recharts";

const API_BASE = "http://localhost:8000/api";

// ─── API helpers ────────────────────────────────────────────────────────────
async function apiFetch(path, options = {}, token = null) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

async function apiUpload(path, formData, token) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

// ─── Colour palette ──────────────────────────────────────────────────────────
const C = {
  bg: "#090d16",
  sidebar: "#0d1526",
  card: "#0f172a",
  card2: "#1e293b",
  border: "#1e293b",
  border2: "#334155",
  text: "#f1f5f9",
  muted: "#94a3b8",
  blue: "#3b82f6",
  green: "#10b981",
  teal: "#38bdf8",
  red: "#f43f5e",
  purple: "#6366f1",
  accent: "#2563eb",
};

// ─── Tiny UI atoms ───────────────────────────────────────────────────────────
const Card = ({ children, style = {} }) => (
  <div style={{ backgroundColor: C.card, borderRadius: 12, border: `1px solid ${C.border}`, padding: 24, ...style }}>
    {children}
  </div>
);

const Badge = ({ children, color = C.blue }) => (
  <span style={{ fontSize: 11, padding: "3px 8px", backgroundColor: color + "33", color, borderRadius: 12, fontWeight: 600 }}>
    {children}
  </span>
);

const Btn = ({ children, onClick, loading, disabled, style = {}, secondary }) => (
  <button
    onClick={onClick}
    disabled={disabled || loading}
    style={{
      display: "flex", alignItems: "center", gap: 8,
      padding: "8px 18px",
      backgroundColor: secondary ? C.card2 : C.accent,
      color: "#fff", border: secondary ? `1px solid ${C.border2}` : "none",
      borderRadius: 7, cursor: "pointer", fontSize: 13, fontWeight: 600,
      opacity: (disabled || loading) ? 0.6 : 1,
      ...style,
    }}
  >
    {loading ? <Loader2 size={14} style={{ animation: "spin 1s linear infinite" }} /> : null}
    {children}
  </button>
);

const Input = ({ value, onChange, placeholder, type = "text", style = {} }) => (
  <input
    type={type}
    value={value}
    onChange={onChange}
    placeholder={placeholder}
    style={{
      width: "100%", padding: "10px 14px",
      backgroundColor: C.card2, border: `1px solid ${C.border2}`,
      borderRadius: 7, color: C.text, fontSize: 14,
      boxSizing: "border-box", ...style,
    }}
  />
);

const ErrorBox = ({ msg }) => msg ? (
  <div style={{ display: "flex", gap: 8, alignItems: "center", padding: "10px 14px", backgroundColor: "#1c0914", border: `1px solid ${C.red}`, borderRadius: 7, color: C.red, fontSize: 13 }}>
    <AlertCircle size={14} /> {msg}
  </div>
) : null;

const Spinner = () => (
  <div style={{ display: "flex", justifyContent: "center", padding: 48, color: C.muted }}>
    <Loader2 size={32} style={{ animation: "spin 1s linear infinite" }} />
  </div>
);

// ─── Auth Screen ─────────────────────────────────────────────────────────────
function AuthScreen({ onLogin }) {
  const [mode, setMode] = useState("login");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("demo@enque.ai");
  const [password, setPassword] = useState("demo1234");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const submit = async () => {
    setError(""); setLoading(true);
    try {
      if (mode === "register") {
        await apiFetch("/auth/register", { method: "POST", body: JSON.stringify({ name, email, password }) });
        setMode("login");
        setError("");
        return;
      }
      const data = await apiFetch("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) });
      onLogin(data.access_token);
    } catch (e) { setError(e.message); }
    finally { setLoading(false); }
  };

  return (
    <div style={{ minHeight: "100vh", backgroundColor: C.bg, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <style>{`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
      <div style={{ width: 400, padding: 40, backgroundColor: C.card, borderRadius: 16, border: `1px solid ${C.border}` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 32 }}>
          <div style={{ width: 42, height: 42, borderRadius: 10, background: `linear-gradient(135deg, ${C.blue}, ${C.purple})`, display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 800, fontSize: 22, color: "#fff" }}>Q</div>
          <div>
            <h1 style={{ margin: 0, fontSize: 22, fontWeight: 800, color: C.text }}>EnQue</h1>
            <p style={{ margin: 0, fontSize: 11, color: C.muted }}>Audience Intelligence Platform</p>
          </div>
        </div>
        <h2 style={{ margin: "0 0 24px", fontSize: 18, fontWeight: 700, color: C.text }}>
          {mode === "login" ? "Sign in to your workspace" : "Create your account"}
        </h2>
        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          {mode === "register" && (
            <Input value={name} onChange={e => setName(e.target.value)} placeholder="Full name" />
          )}
          <Input value={email} onChange={e => setEmail(e.target.value)} placeholder="Email address" type="email" />
          <Input value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" type="password" />
          <ErrorBox msg={error} />
          <Btn onClick={submit} loading={loading} style={{ justifyContent: "center", padding: "11px 18px", fontSize: 14 }}>
            {mode === "login" ? "Sign In" : "Create Account"}
          </Btn>
          <p style={{ margin: 0, textAlign: "center", fontSize: 13, color: C.muted }}>
            {mode === "login" ? "No account? " : "Already have one? "}
            <span onClick={() => setMode(mode === "login" ? "register" : "login")} style={{ color: C.teal, cursor: "pointer", fontWeight: 600 }}>
              {mode === "login" ? "Register" : "Sign In"}
            </span>
          </p>
          {mode === "login" && (
            <p style={{ margin: 0, textAlign: "center", fontSize: 11, color: C.muted }}>
              Demo credentials pre-filled. Register first if new.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── Brand Setup ─────────────────────────────────────────────────────────────
function BrandSetup({ token, onComplete }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [brands, setBrands] = useState([]);
  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({
    brand_name: "GlowUp Skincare",
    description: "D2C Clean Clinical Skincare brand focused on ingredient transparency and science-backed formulations.",
    industry: "Beauty & Personal Care",
    target_audience: "Skincare-curious consumers aged 18–35, ingredient-aware, follow dermatology content",
    brand_voice: "Educational, transparent, clinical yet approachable",
    objectives: "Build authority in clean clinical skincare, grow save rate on educational content"
  });

  useEffect(() => {
    apiFetch("/brands", {}, token).then(setBrands).catch(() => {});
  }, [token]);

  const createBrand = async () => {
    setError(""); setLoading(true);
    try {
      const brand = await apiFetch("/brands", { method: "POST", body: JSON.stringify(form) }, token);
      onComplete(brand);
    } catch (e) { setError(e.message); }
    finally { setLoading(false); }
  };

  if (brands.length > 0 && !showCreate) {
    return (
      <div style={{ minHeight: "100vh", backgroundColor: C.bg, display: "flex", alignItems: "center", justifyContent: "center" }}>
        <style>{`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
        <Card style={{ width: 480 }}>
          <h2 style={{ margin: "0 0 20px", color: C.text }}>Select Brand</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {brands.map(b => (
              <div key={b.id} onClick={() => onComplete(b)} style={{ padding: "14px 18px", backgroundColor: C.card2, borderRadius: 8, cursor: "pointer", border: `1px solid ${C.border2}` }}>
                <strong style={{ fontSize: 14 }}>{b.brand_name}</strong>
                <p style={{ margin: "4px 0 0", fontSize: 12, color: C.muted }}>{b.industry}</p>
              </div>
            ))}
            <Btn secondary onClick={() => setShowCreate(true)} style={{ justifyContent: "center" }}>
              <Plus size={14} /> Create New Brand
            </Btn>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div style={{ minHeight: "100vh", backgroundColor: C.bg, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <style>{`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
      <Card style={{ width: 520 }}>
        <h2 style={{ margin: "0 0 6px", color: C.text }}>Set Up Brand Workspace</h2>
        <p style={{ margin: "0 0 24px", fontSize: 13, color: C.muted }}>Pre-filled with GlowUp Skincare demo data.</p>
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {[
            ["Brand Name", "brand_name"],
            ["Industry", "industry"],
            ["Description", "description"],
            ["Target Audience", "target_audience"],
            ["Brand Voice", "brand_voice"],
            ["Objectives", "objectives"],
          ].map(([label, key]) => (
            <div key={key}>
              <label style={{ fontSize: 12, color: C.muted, display: "block", marginBottom: 5 }}>{label}</label>
              <Input value={form[key]} onChange={e => setForm(f => ({ ...f, [key]: e.target.value }))} placeholder={label} />
            </div>
          ))}
          <ErrorBox msg={error} />
          <Btn onClick={createBrand} loading={loading} style={{ justifyContent: "center", marginTop: 8 }}>
            Create Brand Workspace
          </Btn>
        </div>
      </Card>
    </div>
  );
}

// ─── Data Loader ─────────────────────────────────────────────────────────────
function DataLoader({ token, brand, onDone }) {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");
  const [fileCount, setFileCount] = useState({});

  useEffect(() => {
    // Check if data already ingested
    apiFetch(`/data/files?brand_id=${brand.id}`, {}, token).then(d => {
      if (d.total_posts > 0) onDone();
    }).catch(() => {});
  }, []);

  const uploadFile = async (filename, type) => {
    setStatus(`Fetching ${filename}...`);
    try {
      const res = await fetch(`/datasets/demo/${filename}`);
      if (!res.ok) throw new Error(`${filename} not found in public folder`);
      const blob = await res.blob();
      const form = new FormData();
      form.append("brand_id", brand.id);
      form.append("dataset_type", type);
      form.append("file", blob, filename);
      const result = await apiUpload("/data/upload", form, token);
      setFileCount(prev => ({ ...prev, [filename]: result.imported || 0 }));
      return result;
    } catch (e) {
      // Fallback: try absolute path
      setStatus(`Uploading ${filename} from disk...`);
      throw e;
    }
  };

  const loadDemo = async () => {
    setError(""); setLoading(true);
    try {
      setStatus("Uploading posts.csv...");
      await uploadFile("posts.csv", "posts");
      setStatus("Uploading comments.csv...");
      await uploadFile("comments.csv", "comments");
      setStatus("Demo data loaded successfully!");
      setTimeout(onDone, 800);
    } catch (e) {
      setError(`Upload failed: ${e.message}. You can skip to upload manually.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: "100vh", backgroundColor: C.bg, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <style>{`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
      <Card style={{ width: 480 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 20 }}>
          <Database size={20} color={C.teal} />
          <h2 style={{ margin: 0, color: C.text }}>Load GlowUp Demo Dataset</h2>
        </div>
        <p style={{ fontSize: 13, color: C.muted, marginTop: 0 }}>
          Upload 25 posts + 30 audience comments to seed the intelligence platform.
        </p>
        {status && <p style={{ color: C.green, fontSize: 13 }}>{status}</p>}
        <ErrorBox msg={error} />
        <div style={{ display: "flex", flexDirection: "column", gap: 10, marginTop: 16 }}>
          <Btn onClick={loadDemo} loading={loading} style={{ justifyContent: "center" }}>
            <Upload size={14} /> Load Demo Data
          </Btn>
          <Btn secondary onClick={onDone} style={{ justifyContent: "center" }}>
            Skip (data already loaded)
          </Btn>
        </div>
      </Card>
    </div>
  );
}

// ─── Main Dashboard ───────────────────────────────────────────────────────────
const TABS = [
  { id: "overview", label: "Overview", icon: Layers },
  { id: "audience", label: "Audience Insights", icon: Users },
  { id: "content", label: "Content Analytics", icon: BarChart3 },
  { id: "strategy", label: "AI Strategy", icon: Compass },
  { id: "memory", label: "AI Memory", icon: Brain },
  { id: "experiments", label: "Experiments", icon: FlaskConical },
  { id: "data", label: "Data Sources", icon: Database },
];

function Dashboard({ token, brand, onLogout }) {
  const [activeTab, setActiveTab] = useState("overview");
  const [contentAnalytics, setContentAnalytics] = useState(null);
  const [topPosts, setTopPosts] = useState([]);
  const [audienceInsights, setAudienceInsights] = useState(null);
  const [strategyRecs, setStrategyRecs] = useState([]);
  const [memories, setMemories] = useState(null);
  const [experiments, setExperiments] = useState([]);
  const [dataFiles, setDataFiles] = useState(null);
  const [chatMessages, setChatMessages] = useState([
    { sender: "agent", text: `I am your EnQue Orchestrator for ${brand.brand_name}. Ask me about your audience, content performance, or next month's strategy.` }
  ]);
  const [chatInput, setChatInput] = useState("");
  const [loadingStrategy, setLoadingStrategy] = useState(false);
  const [loadingChat, setLoadingChat] = useState(false);
  const [loading, setLoading] = useState({});
  const [errors, setErrors] = useState({});
  const chatEndRef = useRef(null);

  const setLoad = (key, v) => setLoading(p => ({ ...p, [key]: v }));
  const setErr = (key, v) => setErrors(p => ({ ...p, [key]: v }));

  const fetchContent = useCallback(async () => {
    setLoad("content", true); setErr("content", "");
    try {
      const [analytics, top] = await Promise.all([
        apiFetch(`/content/analytics?brand_id=${brand.id}`, {}, token),
        apiFetch(`/content/top-performing?brand_id=${brand.id}&limit=5`, {}, token),
      ]);
      setContentAnalytics(analytics);
      setTopPosts(top);
    } catch (e) { setErr("content", e.message); }
    finally { setLoad("content", false); }
  }, [token, brand.id]);

  const fetchAudience = useCallback(async () => {
    setLoad("audience", true); setErr("audience", "");
    try {
      const data = await apiFetch(`/audience/insights?brand_id=${brand.id}`, {}, token);
      setAudienceInsights(data);
    } catch (e) { setErr("audience", e.message); }
    finally { setLoad("audience", false); }
  }, [token, brand.id]);

  const fetchRecs = useCallback(async () => {
    setLoad("recs", true); setErr("recs", "");
    try {
      const data = await apiFetch(`/recommendations?brand_id=${brand.id}`, {}, token);
      setStrategyRecs(data);
    } catch (e) { setErr("recs", e.message); }
    finally { setLoad("recs", false); }
  }, [token, brand.id]);

  const fetchMemories = useCallback(async () => {
    setLoad("memory", true); setErr("memory", "");
    try {
      const data = await apiFetch(`/memory/overview?brand_id=${brand.id}`, {}, token);
      setMemories(data);
    } catch (e) { setErr("memory", e.message); }
    finally { setLoad("memory", false); }
  }, [token, brand.id]);

  const fetchExperiments = useCallback(async () => {
    setLoad("experiments", true); setErr("experiments", "");
    try {
      const data = await apiFetch(`/experiments?brand_id=${brand.id}`, {}, token);
      setExperiments(data);
    } catch (e) { setErr("experiments", e.message); }
    finally { setLoad("experiments", false); }
  }, [token, brand.id]);

  const fetchDataFiles = useCallback(async () => {
    setLoad("data", true);
    try {
      const data = await apiFetch(`/data/files?brand_id=${brand.id}`, {}, token);
      setDataFiles(data);
    } catch (e) {}
    finally { setLoad("data", false); }
  }, [token, brand.id]);

  // Initial load
  useEffect(() => {
    fetchContent();
    fetchAudience();
    fetchRecs();
    fetchMemories();
    fetchExperiments();
    fetchDataFiles();
  }, []);

  // Auto-scroll chat
  useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [chatMessages]);

  const handleGenerateStrategy = async () => {
    setLoadingStrategy(true);
    try {
      const res = await apiFetch("/agents/strategy", {
        method: "POST",
        body: JSON.stringify({ brand_id: brand.id, query: "What content strategy should we execute next month?" }),
      }, token);
      if (res.recommendations) setStrategyRecs(res.recommendations);
      await fetchMemories();
    } catch (e) {
      setErr("recs", e.message);
    } finally {
      setLoadingStrategy(false);
    }
  };

  const handleSendMessage = async () => {
    if (!chatInput.trim() || loadingChat) return;
    const userMsg = chatInput;
    setChatMessages(prev => [...prev, { sender: "user", text: userMsg }]);
    setChatInput("");
    setLoadingChat(true);
    try {
      const res = await apiFetch("/agents/chat", {
        method: "POST",
        body: JSON.stringify({ brand_id: brand.id, message: userMsg }),
      }, token);
      setChatMessages(prev => [...prev, { sender: "agent", text: res.agent_response || "No response from orchestrator." }]);
    } catch (e) {
      setChatMessages(prev => [...prev, { sender: "agent", text: `Error: ${e.message}` }]);
    } finally {
      setLoadingChat(false);
    }
  };

  // Derived chart data from real API
  const formatChartData = (analytics) => {
    if (!analytics?.performance_by_format) return [];
    return Object.entries(analytics.performance_by_format).map(([format, stats]) => ({
      format,
      engRate: parseFloat((stats.avg_engagement_rate || 0).toFixed(2)),
      saveRate: parseFloat((stats.avg_save_rate || 0).toFixed(2)),
    }));
  };

  const sentimentData = audienceInsights ? [
    { name: "Positive", value: audienceInsights.sentiment_breakdown?.positive || 0, color: C.green },
    { name: "Neutral", value: audienceInsights.sentiment_breakdown?.neutral || 0, color: "#64748b" },
    { name: "Negative", value: audienceInsights.sentiment_breakdown?.negative || 0, color: C.red },
  ] : [];

  const confidenceColor = (c) => {
    if (!c) return C.muted;
    const cl = c.toLowerCase();
    if (cl.includes("high")) return C.green;
    if (cl.includes("medium")) return "#f59e0b";
    return C.muted;
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh", backgroundColor: C.bg, color: C.text }}>
      <style>{`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } } * { box-sizing: border-box; }`}</style>

      {/* Sidebar */}
      <aside style={{ width: 256, backgroundColor: C.sidebar, borderRight: `1px solid ${C.border}`, padding: "24px 14px", display: "flex", flexDirection: "column", gap: 24, flexShrink: 0 }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "0 6px", marginBottom: 20 }}>
            <div style={{ width: 36, height: 36, borderRadius: 8, background: `linear-gradient(135deg, ${C.blue}, ${C.purple})`, display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 800, fontSize: 20, color: "#fff" }}>Q</div>
            <div>
              <h1 style={{ margin: 0, fontSize: 17, fontWeight: 800 }}>EnQue</h1>
              <p style={{ margin: 0, fontSize: 10, color: C.muted }}>Audience Intelligence</p>
            </div>
          </div>
          <div style={{ padding: "10px 12px", backgroundColor: C.card2, borderRadius: 8, display: "flex", alignItems: "center", gap: 8, marginBottom: 16 }}>
            <Building2 size={15} color={C.teal} />
            <div style={{ overflow: "hidden" }}>
              <p style={{ margin: 0, fontSize: 12, fontWeight: 600, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{brand.brand_name}</p>
              <p style={{ margin: 0, fontSize: 10, color: C.muted }}>{brand.industry}</p>
            </div>
          </div>
        </div>

        <nav style={{ display: "flex", flexDirection: "column", gap: 2, flex: 1 }}>
          {TABS.map(item => {
            const Icon = item.icon;
            const active = activeTab === item.id;
            return (
              <button key={item.id} onClick={() => setActiveTab(item.id)} style={{
                display: "flex", alignItems: "center", gap: 11, padding: "9px 12px",
                borderRadius: 7, border: "none",
                backgroundColor: active ? C.accent : "transparent",
                color: active ? "#fff" : C.muted,
                cursor: "pointer", fontSize: 13, fontWeight: active ? 600 : 500, textAlign: "left",
              }}>
                <Icon size={16} /> {item.label}
              </button>
            );
          })}
        </nav>

        <button onClick={onLogout} style={{ display: "flex", alignItems: "center", gap: 8, padding: "8px 12px", borderRadius: 7, border: "none", backgroundColor: "transparent", color: C.muted, cursor: "pointer", fontSize: 12 }}>
          <LogOut size={14} /> Sign Out
        </button>
      </aside>

      {/* Main */}
      <main style={{ flex: 1, padding: "28px 36px", overflowY: "auto" }}>
        {/* Header */}
        <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 28 }}>
          <div>
            <h2 style={{ margin: 0, fontSize: 22, fontWeight: 700 }}>
              {TABS.find(t => t.id === activeTab)?.label}
            </h2>
            <p style={{ margin: "3px 0 0", fontSize: 12, color: C.muted }}>
              Persistent experiential memory & coordinated AI intelligence
            </p>
          </div>
          <span style={{ display: "flex", alignItems: "center", gap: 6, padding: "5px 12px", backgroundColor: "#064e3b", color: "#34d399", borderRadius: 20, fontSize: 11, fontWeight: 600 }}>
            <span style={{ width: 7, height: 7, backgroundColor: C.green, borderRadius: "50%" }} />
            Hindsight Bank Active
          </span>
        </header>

        {/* ── Overview Tab ── */}
        {activeTab === "overview" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
            {loading.content ? <Spinner /> : (
              <>
                {/* KPI Row */}
                <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 16 }}>
                  {[
                    { label: "Posts Analysed", value: contentAnalytics?.total_posts ?? "—", sub: "in dataset", icon: BarChart3, color: C.blue },
                    { label: "Avg. Engagement Rate", value: contentAnalytics?.avg_engagement_rate != null ? `${contentAnalytics.avg_engagement_rate}%` : "—", sub: "across all formats", icon: TrendingUp, color: C.teal },
                    { label: "Avg. Save Rate", value: contentAnalytics?.avg_save_rate != null ? `${contentAnalytics.avg_save_rate}%` : "—", sub: "top retention metric", icon: BookmarkCheck, color: C.green },
                    { label: "Audience Sentiment", value: audienceInsights?.overall_sentiment ?? "—", sub: `${audienceInsights?.sentiment_breakdown?.positive_ratio ?? 0}% positive`, icon: Users, color: C.purple },
                  ].map((kpi, i) => {
                    const Icon = kpi.icon;
                    return (
                      <Card key={i} style={{ padding: 20 }}>
                        <div style={{ display: "flex", justifyContent: "space-between", color: C.muted, marginBottom: 8 }}>
                          <span style={{ fontSize: 11, fontWeight: 500 }}>{kpi.label}</span>
                          <Icon size={15} color={kpi.color} />
                        </div>
                        <div style={{ fontSize: 26, fontWeight: 700, color: kpi.color }}>{kpi.value}</div>
                        <div style={{ fontSize: 11, color: C.muted, marginTop: 4 }}>{kpi.sub}</div>
                      </Card>
                    );
                  })}
                </div>

                {/* Charts */}
                <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 24 }}>
                  <Card>
                    <h3 style={{ margin: "0 0 16px", fontSize: 14, fontWeight: 600 }}>Engagement & Save Rate by Content Format</h3>
                    <div style={{ height: 220 }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={formatChartData(contentAnalytics)}>
                          <XAxis dataKey="format" stroke={C.muted} fontSize={11} />
                          <YAxis stroke={C.muted} fontSize={11} unit="%" />
                          <Tooltip contentStyle={{ backgroundColor: C.card2, borderColor: C.border2, color: "#fff", fontSize: 12 }} />
                          <Legend wrapperStyle={{ fontSize: 11 }} />
                          <Bar dataKey="engRate" fill={C.blue} radius={[4,4,0,0]} name="Engagement %" />
                          <Bar dataKey="saveRate" fill={C.green} radius={[4,4,0,0]} name="Save Rate %" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </Card>
                  <Card>
                    <h3 style={{ margin: "0 0 12px", fontSize: 14, fontWeight: 600 }}>Audience Sentiment</h3>
                    {loading.audience ? <Spinner /> : (
                      <>
                        <div style={{ height: 160 }}>
                          <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                              <Pie data={sentimentData} innerRadius={40} outerRadius={60} paddingAngle={4} dataKey="value">
                                {sentimentData.map((entry, i) => <Cell key={i} fill={entry.color} />)}
                              </Pie>
                              <Tooltip contentStyle={{ backgroundColor: C.card2, borderColor: C.border2, color: "#fff", fontSize: 12 }} />
                            </PieChart>
                          </ResponsiveContainer>
                        </div>
                        <div style={{ display: "flex", justifyContent: "space-around", fontSize: 11, color: C.muted, marginTop: 8 }}>
                          {sentimentData.map(s => (
                            <span key={s.name} style={{ color: s.color }}>{s.name}: {s.value}</span>
                          ))}
                        </div>
                      </>
                    )}
                  </Card>
                </div>

                {/* Recent Recs */}
                <Card>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
                    <h3 style={{ margin: 0, fontSize: 14, fontWeight: 600 }}>Recent AI Recommendations & Hindsight Grounding</h3>
                    <button onClick={() => setActiveTab("strategy")} style={{ backgroundColor: "transparent", color: C.teal, border: "none", cursor: "pointer", fontSize: 12, display: "flex", alignItems: "center", gap: 4 }}>
                      Open Strategy <ArrowUpRight size={13} />
                    </button>
                  </div>
                  {loading.recs ? <Spinner /> : strategyRecs.length === 0 ? (
                    <p style={{ color: C.muted, fontSize: 13 }}>No recommendations yet. Generate a strategy in the AI Strategy tab.</p>
                  ) : (
                    <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                      {strategyRecs.slice(0, 2).map((rec, i) => (
                        <div key={i} style={{ padding: 16, backgroundColor: C.card2, borderRadius: 8, borderLeft: `4px solid ${C.blue}` }}>
                          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                            <h4 style={{ margin: "0 0 6px", fontSize: 13, fontWeight: 600 }}>{rec.recommendation}</h4>
                            <Badge color={confidenceColor(rec.evidence)}>{rec.status || "proposed"}</Badge>
                          </div>
                          <p style={{ margin: "0 0 8px", fontSize: 12, color: C.muted }}>{rec.reasoning}</p>
                          {rec.evidence && (
                            <div style={{ fontSize: 11, color: C.teal, display: "flex", alignItems: "center", gap: 6 }}>
                              <Brain size={12} /> {rec.evidence}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </Card>
              </>
            )}
          </div>
        )}

        {/* ── Audience Tab ── */}
        {activeTab === "audience" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
            <div style={{ display: "flex", justifyContent: "flex-end" }}>
              <Btn secondary onClick={fetchAudience} loading={loading.audience}><RefreshCw size={13} /> Refresh</Btn>
            </div>
            <ErrorBox msg={errors.audience} />
            {loading.audience ? <Spinner /> : audienceInsights ? (
              <>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
                  <Card>
                    <h3 style={{ margin: "0 0 16px", fontSize: 14, fontWeight: 600 }}>Dominant Audience Topics</h3>
                    <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
                      {audienceInsights.dominant_topics?.map((t, i) => (
                        <span key={i} style={{ padding: "7px 14px", backgroundColor: C.card2, borderRadius: 20, fontSize: 13, color: C.teal, border: `1px solid ${C.border2}` }}>
                          #{t}
                        </span>
                      ))}
                    </div>
                    <div style={{ marginTop: 16 }}>
                      <p style={{ fontSize: 12, color: C.muted, marginBottom: 8 }}>Emerging Trends</p>
                      <div style={{ display: "flex", gap: 8 }}>
                        {audienceInsights.emerging_trends?.map((t, i) => (
                          <Badge key={i} color={C.purple}>{t}</Badge>
                        ))}
                      </div>
                    </div>
                  </Card>
                  <Card>
                    <h3 style={{ margin: "0 0 16px", fontSize: 14, fontWeight: 600 }}>Sentiment Breakdown</h3>
                    <div style={{ height: 160 }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie data={sentimentData} innerRadius={40} outerRadius={65} paddingAngle={4} dataKey="value">
                            {sentimentData.map((e, i) => <Cell key={i} fill={e.color} />)}
                          </Pie>
                          <Tooltip contentStyle={{ backgroundColor: C.card2, borderColor: C.border2, color: "#fff", fontSize: 12 }} />
                          <Legend wrapperStyle={{ fontSize: 11 }} />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                    <div style={{ marginTop: 10, fontSize: 13, fontWeight: 600, textAlign: "center", color: C.green }}>
                      Overall: {audienceInsights.overall_sentiment}
                    </div>
                  </Card>
                </div>

                <Card>
                  <h3 style={{ margin: "0 0 16px", fontSize: 14, fontWeight: 600 }}>Recurring Audience Questions</h3>
                  {audienceInsights.common_questions?.length > 0 ? (
                    <ul style={{ margin: 0, paddingLeft: 20, fontSize: 13, color: "#cbd5e1", lineHeight: 1.8 }}>
                      {audienceInsights.common_questions.map((q, i) => <li key={i}>{q}</li>)}
                    </ul>
                  ) : <p style={{ color: C.muted, fontSize: 13 }}>No questions detected yet.</p>}
                </Card>

                <Card>
                  <h3 style={{ margin: "0 0 12px", fontSize: 14, fontWeight: 600, color: C.red }}>Detected Pain Points & Concerns</h3>
                  {audienceInsights.pain_points?.length > 0 ? (
                    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                      {audienceInsights.pain_points.map((p, i) => (
                        <div key={i} style={{ padding: "10px 16px", backgroundColor: "#1c0914", borderLeft: `4px solid ${C.red}`, borderRadius: 4, fontSize: 13 }}>
                          {p}
                        </div>
                      ))}
                    </div>
                  ) : <p style={{ color: C.muted, fontSize: 13 }}>No pain points detected.</p>}
                </Card>
              </>
            ) : <p style={{ color: C.muted }}>No audience data available. Upload comments to begin analysis.</p>}
          </div>
        )}

        {/* ── Content Analytics Tab ── */}
        {activeTab === "content" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
            <div style={{ display: "flex", justifyContent: "flex-end" }}>
              <Btn secondary onClick={fetchContent} loading={loading.content}><RefreshCw size={13} /> Refresh</Btn>
            </div>
            <ErrorBox msg={errors.content} />
            {loading.content ? <Spinner /> : (
              <>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 16 }}>
                  {[
                    { label: "Total Posts", value: contentAnalytics?.total_posts ?? "—" },
                    { label: "Avg Engagement Rate", value: `${contentAnalytics?.avg_engagement_rate ?? "—"}%` },
                    { label: "Avg Save Rate", value: `${contentAnalytics?.avg_save_rate ?? "—"}%` },
                  ].map((kpi, i) => (
                    <Card key={i} style={{ padding: 18 }}>
                      <p style={{ margin: "0 0 6px", fontSize: 11, color: C.muted }}>{kpi.label}</p>
                      <div style={{ fontSize: 24, fontWeight: 700, color: C.teal }}>{kpi.value}</div>
                    </Card>
                  ))}
                </div>

                <Card>
                  <h3 style={{ margin: "0 0 16px", fontSize: 14, fontWeight: 600 }}>Performance by Format</h3>
                  <div style={{ height: 240 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={formatChartData(contentAnalytics)}>
                        <XAxis dataKey="format" stroke={C.muted} fontSize={11} />
                        <YAxis stroke={C.muted} fontSize={11} unit="%" />
                        <Tooltip contentStyle={{ backgroundColor: C.card2, borderColor: C.border2, color: "#fff" }} />
                        <Legend wrapperStyle={{ fontSize: 11 }} />
                        <Bar dataKey="engRate" fill={C.blue} radius={[4,4,0,0]} name="Engagement %" />
                        <Bar dataKey="saveRate" fill={C.green} radius={[4,4,0,0]} name="Save Rate %" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </Card>

                <Card>
                  <h3 style={{ margin: "0 0 16px", fontSize: 14, fontWeight: 600 }}>Top Performing Posts</h3>
                  {topPosts.length > 0 ? (
                    <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                      {topPosts.map((p, i) => (
                        <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px 16px", backgroundColor: C.card2, borderRadius: 8 }}>
                          <div>
                            <span style={{ fontSize: 10, textTransform: "uppercase", padding: "2px 6px", backgroundColor: C.border2, borderRadius: 4, marginRight: 8 }}>{p.content_type}</span>
                            <span style={{ fontSize: 13, fontWeight: 600 }}>{p.caption?.slice(0, 60) || `Post #${p.id}`}{p.caption?.length > 60 ? "…" : ""}</span>
                          </div>
                          <div style={{ display: "flex", gap: 20, fontSize: 12 }}>
                            <span>Eng: <strong style={{ color: C.teal }}>{(p.engagement_rate || 0).toFixed(1)}%</strong></span>
                            <span>Saves: <strong style={{ color: C.green }}>{p.saves || 0}</strong></span>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : <p style={{ color: C.muted, fontSize: 13 }}>No post data available.</p>}
                </Card>
              </>
            )}
          </div>
        )}

        {/* ── AI Strategy Tab ── */}
        {activeTab === "strategy" && (
          <div style={{ display: "grid", gridTemplateColumns: "1.6fr 1fr", gap: 24 }}>
            {/* Recommendations */}
            <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <h3 style={{ margin: 0, fontSize: 15, fontWeight: 600 }}>AI Strategic Recommendations</h3>
                <Btn onClick={handleGenerateStrategy} loading={loadingStrategy}>
                  <RefreshCw size={13} /> {loadingStrategy ? "Orchestrating…" : "Generate Strategy"}
                </Btn>
              </div>
              <ErrorBox msg={errors.recs} />
              {loading.recs && !loadingStrategy ? <Spinner /> : strategyRecs.length === 0 ? (
                <Card>
                  <p style={{ color: C.muted, fontSize: 13, margin: 0 }}>
                    No recommendations yet. Click "Generate Strategy" to run the full Orchestrator cycle (Audience Agent → Content Agent → Hindsight recall → Strategy Agent).
                  </p>
                </Card>
              ) : (
                strategyRecs.map((rec, i) => (
                  <Card key={i} style={{ borderLeft: `4px solid ${C.blue}` }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                      <h4 style={{ margin: "0 0 8px", fontSize: 14, fontWeight: 600 }}>{rec.recommendation}</h4>
                      <Badge color={C.blue}>{rec.status || "proposed"}</Badge>
                    </div>
                    <p style={{ margin: "0 0 10px", fontSize: 13, color: C.muted }}>{rec.reasoning}</p>
                    {rec.expected_outcome && (
                      <p style={{ margin: "0 0 10px", fontSize: 12, color: "#a3e635" }}>Expected: {rec.expected_outcome}</p>
                    )}
                    {rec.evidence && (
                      <div style={{ padding: "9px 12px", backgroundColor: C.card2, borderRadius: 6, fontSize: 12, color: C.teal, display: "flex", alignItems: "center", gap: 7 }}>
                        <Brain size={13} /> <strong>Hindsight:</strong>&nbsp;{rec.evidence}
                      </div>
                    )}
                  </Card>
                ))
              )}
            </div>

            {/* Chat */}
            <div style={{ backgroundColor: C.card, borderRadius: 12, border: `1px solid ${C.border}`, display: "flex", flexDirection: "column", height: 580 }}>
              <div style={{ padding: "14px 18px", borderBottom: `1px solid ${C.border}`, display: "flex", alignItems: "center", gap: 8 }}>
                <Sparkles size={15} color={C.teal} />
                <h4 style={{ margin: 0, fontSize: 13, fontWeight: 600 }}>Strategic Assistant (Orchestrator)</h4>
              </div>
              <div style={{ flex: 1, padding: 16, overflowY: "auto", display: "flex", flexDirection: "column", gap: 10 }}>
                {chatMessages.map((msg, i) => (
                  <div key={i} style={{
                    alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
                    maxWidth: "88%", padding: "9px 13px", borderRadius: 8,
                    backgroundColor: msg.sender === "user" ? C.accent : C.card2,
                    fontSize: 12, lineHeight: 1.5,
                  }}>{msg.text}</div>
                ))}
                {loadingChat && <div style={{ alignSelf: "flex-start", fontSize: 12, color: C.muted }}>Thinking…</div>}
                <div ref={chatEndRef} />
              </div>
              <div style={{ padding: 12, borderTop: `1px solid ${C.border}`, display: "flex", gap: 8 }}>
                <input
                  value={chatInput} onChange={e => setChatInput(e.target.value)}
                  onKeyDown={e => e.key === "Enter" && handleSendMessage()}
                  placeholder="Ask about your audience or strategy…"
                  style={{ flex: 1, padding: "8px 12px", backgroundColor: C.card2, border: `1px solid ${C.border2}`, borderRadius: 6, color: C.text, fontSize: 12 }}
                />
                <Btn onClick={handleSendMessage} loading={loadingChat} style={{ padding: "8px 12px" }}>
                  <Send size={13} />
                </Btn>
              </div>
            </div>
          </div>
        )}

        {/* ── Memory Tab ── */}
        {activeTab === "memory" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
            <div style={{ display: "flex", justifyContent: "flex-end" }}>
              <Btn secondary onClick={fetchMemories} loading={loading.memory}><RefreshCw size={13} /> Refresh</Btn>
            </div>
            <ErrorBox msg={errors.memory} />
            {loading.memory ? <Spinner /> : memories ? (
              <>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 16 }}>
                  {[
                    { label: "Total Recommendations", value: memories.total_recommendations ?? 0, color: C.blue },
                    { label: "Campaign Learnings", value: memories.total_campaign_learnings ?? 0, color: C.green },
                    { label: "Total Experiments", value: memories.total_experiments ?? 0, color: C.purple },
                  ].map((s, i) => (
                    <Card key={i} style={{ padding: 18 }}>
                      <p style={{ margin: "0 0 6px", fontSize: 11, color: C.muted }}>{s.label}</p>
                      <div style={{ fontSize: 28, fontWeight: 700, color: s.color }}>{s.value}</div>
                    </Card>
                  ))}
                </div>

                <Card>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
                    <h3 style={{ margin: 0, fontSize: 14, fontWeight: 600 }}>Hindsight Memory Bank</h3>
                    <code style={{ fontSize: 11, color: C.muted, backgroundColor: C.card2, padding: "3px 8px", borderRadius: 5 }}>{memories.hindsight_bank_id}</code>
                  </div>
                  <div style={{ marginBottom: 20 }}>
                    <p style={{ fontSize: 12, color: C.muted, margin: "0 0 10px" }}>Brand Knowledge Profile</p>
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
                      {memories.stored_brand_knowledge && Object.entries(memories.stored_brand_knowledge).filter(([,v]) => v).map(([k, v]) => (
                        <div key={k} style={{ padding: "10px 14px", backgroundColor: C.card2, borderRadius: 7 }}>
                          <p style={{ margin: "0 0 4px", fontSize: 10, color: C.muted, textTransform: "uppercase", fontWeight: 600 }}>{k.replace(/_/g, " ")}</p>
                          <p style={{ margin: 0, fontSize: 12 }}>{v}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                  <h4 style={{ margin: "0 0 10px", fontSize: 13, fontWeight: 600 }}>Recent Campaign Learnings</h4>
                  {memories.recent_learnings?.length > 0 ? (
                    <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                      {memories.recent_learnings.map((m, i) => (
                        <div key={i} style={{ padding: "14px 16px", backgroundColor: C.card2, borderRadius: 8, borderLeft: `4px solid ${C.green}` }}>
                          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: C.muted, marginBottom: 6 }}>
                            <Badge color={m.evaluation === "Positive" ? C.green : C.red}>{m.evaluation}</Badge>
                            <span>{m.evaluated_at ? new Date(m.evaluated_at).toLocaleDateString() : ""}</span>
                          </div>
                          <p style={{ margin: 0, fontSize: 13 }}>{m.learning_summary}</p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p style={{ color: C.muted, fontSize: 13 }}>
                      No learnings stored yet. Run the Strategy cycle and evaluate an experiment to populate Hindsight memory.
                    </p>
                  )}
                </Card>
              </>
            ) : null}
          </div>
        )}

        {/* ── Experiments Tab ── */}
        {activeTab === "experiments" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
            <div style={{ display: "flex", justifyContent: "flex-end" }}>
              <Btn secondary onClick={fetchExperiments} loading={loading.experiments}><RefreshCw size={13} /> Refresh</Btn>
            </div>
            <ErrorBox msg={errors.experiments} />
            {loading.experiments ? <Spinner /> : (
              <Card>
                <h3 style={{ margin: "0 0 16px", fontSize: 14, fontWeight: 600 }}>Campaign Experiments & Learning Cycle</h3>
                {experiments.length === 0 ? (
                  <div>
                    <p style={{ color: C.muted, fontSize: 13 }}>No experiments yet. Generate a strategy, implement a recommendation, then submit actual results to trigger the Evaluation Agent and Learning cycle.</p>
                    <Btn onClick={handleGenerateStrategy} loading={loadingStrategy} style={{ marginTop: 12 }}>
                      <Sparkles size={13} /> Generate Strategy (creates experiments)
                    </Btn>
                  </div>
                ) : (
                  <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                    {experiments.map((e, i) => (
                      <div key={i} style={{ padding: "14px 18px", backgroundColor: C.card2, borderRadius: 8 }}>
                        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
                          <strong style={{ fontSize: 13 }}>{e.hypothesis}</strong>
                          <Badge color={e.status === "completed" ? C.green : e.status === "active" ? C.teal : C.muted}>
                            {e.status}
                          </Badge>
                        </div>
                        {e.measurement_method && (
                          <p style={{ margin: "0 0 6px", fontSize: 12, color: C.muted }}>Method: {e.measurement_method}</p>
                        )}
                        <p style={{ margin: 0, fontSize: 11, color: C.muted }}>
                          Created: {e.created_at ? new Date(e.created_at).toLocaleDateString() : "—"}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </Card>
            )}
          </div>
        )}

        {/* ── Data Sources Tab ── */}
        {activeTab === "data" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
            <div style={{ display: "flex", justifyContent: "flex-end" }}>
              <Btn secondary onClick={fetchDataFiles} loading={loading.data}><RefreshCw size={13} /> Refresh</Btn>
            </div>
            {loading.data ? <Spinner /> : dataFiles && (
              <>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 16 }}>
                  {[
                    { label: "Posts Ingested", value: dataFiles.total_posts, icon: BarChart3, color: C.blue },
                    { label: "Comments Ingested", value: dataFiles.total_comments, icon: Users, color: C.teal },
                    { label: "Documents Stored", value: dataFiles.documents?.length || 0, icon: Database, color: C.purple },
                  ].map((s, i) => {
                    const Icon = s.icon;
                    return (
                      <Card key={i} style={{ padding: 18 }}>
                        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                          <span style={{ fontSize: 11, color: C.muted }}>{s.label}</span>
                          <Icon size={15} color={s.color} />
                        </div>
                        <div style={{ fontSize: 28, fontWeight: 700, color: s.color }}>{s.value}</div>
                      </Card>
                    );
                  })}
                </div>

                <Card>
                  <h3 style={{ margin: "0 0 16px", fontSize: 14, fontWeight: 600 }}>Uploaded Documents</h3>
                  {dataFiles.documents?.length > 0 ? (
                    <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                      {dataFiles.documents.map((doc, i) => (
                        <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "11px 16px", backgroundColor: C.card2, borderRadius: 7 }}>
                          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                            <Database size={14} color={C.teal} />
                            <span style={{ fontSize: 13, fontWeight: 600 }}>{doc.file_name}</span>
                          </div>
                          <div style={{ display: "flex", gap: 12, fontSize: 12, alignItems: "center" }}>
                            <span style={{ color: C.muted }}>{doc.document_type}</span>
                            <Badge color={doc.processing_status === "processed" ? C.green : C.muted}>{doc.processing_status}</Badge>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p style={{ color: C.muted, fontSize: 13 }}>No documents uploaded. Data is ingested directly via the CSV upload endpoint.</p>
                  )}
                </Card>

                <Card>
                  <h3 style={{ margin: "0 0 12px", fontSize: 14, fontWeight: 600 }}>Data Ingestion Guide</h3>
                  <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 12 }}>
                    {[
                      { file: "posts.csv", type: "Social Media Posts & Metrics", desc: "post_id, platform, content_type, caption, reach, likes, comments, shares, saves" },
                      { file: "comments.csv", type: "Audience Comments & Feedback", desc: "post_id, comment_text, author, comment_date" },
                      { file: "campaigns.csv", type: "Campaign Objectives", desc: "campaign_name, start_date, end_date, budget, objective, platform" },
                    ].map((ds, i) => (
                      <div key={i} style={{ padding: 16, backgroundColor: C.card2, borderRadius: 8 }}>
                        <div style={{ display: "flex", alignItems: "center", gap: 7, marginBottom: 8 }}>
                          <Database size={14} color={C.teal} />
                          <strong style={{ fontSize: 12 }}>{ds.file}</strong>
                        </div>
                        <p style={{ margin: "0 0 6px", fontSize: 12, color: "#a3e635" }}>{ds.type}</p>
                        <p style={{ margin: 0, fontSize: 11, color: C.muted }}>{ds.desc}</p>
                      </div>
                    ))}
                  </div>
                </Card>
              </>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

// ─── App Root ─────────────────────────────────────────────────────────────────
export default function App() {
  const [token, setToken] = useState(() => localStorage.getItem("enque_token") || "");
  const [brand, setBrand] = useState(() => {
    try { return JSON.parse(localStorage.getItem("enque_brand") || "null"); } catch { return null; }
  });
  const [step, setStep] = useState(() => {
    if (!localStorage.getItem("enque_token")) return "auth";
    if (!localStorage.getItem("enque_brand")) return "brand";
    return "data";
  });

  const handleLogin = (tok) => {
    localStorage.setItem("enque_token", tok);
    setToken(tok);
    setStep(brand ? "data" : "brand");
  };

  const handleBrand = (b) => {
    localStorage.setItem("enque_brand", JSON.stringify(b));
    setBrand(b);
    setStep("data");
  };

  const handleDataDone = () => {
    setStep("dashboard");
  };

  const handleLogout = () => {
    localStorage.removeItem("enque_token");
    localStorage.removeItem("enque_brand");
    setToken(""); setBrand(null); setStep("auth");
  };

  if (step === "auth") return <AuthScreen onLogin={handleLogin} />;
  if (step === "brand") return <BrandSetup token={token} onComplete={handleBrand} />;
  if (step === "data") return <DataLoader token={token} brand={brand} onDone={handleDataDone} />;
  return <Dashboard token={token} brand={brand} onLogout={handleLogout} />;
}
