import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [items, setItems] = useState([]);
  const [metrics, setMetrics] = useState({});
  const [query, setQuery] = useState("");

  useEffect(() => {
    Promise.all([fetch(`${API}/api/work-items`).then(r => r.json()), fetch(`${API}/api/metrics`).then(r => r.json())])
      .then(([workItems, summary]) => { setItems(workItems); setMetrics(summary); });
  }, []);

  const visible = useMemo(() => items.filter(item => [item.title, item.owner].join(" ").toLowerCase().includes(query.toLowerCase())), [items, query]);

  return <main>
    <header><div><p className="eyebrow">OPERATIONS CONTROL</p><h1>Workflow Hub</h1><p>Turn scattered requests into owned, measurable work.</p></div><button>+ New work item</button></header>
    <section className="metrics">{["total","open","blocked","urgent"].map(key => <article key={key}><span>{key}</span><strong>{metrics[key] ?? "—"}</strong></article>)}</section>
    <section className="panel"><div className="toolbar"><div><h2>Work queue</h2><p>Prioritized operational requests</p></div><input aria-label="Search work items" placeholder="Search title or owner…" value={query} onChange={e => setQuery(e.target.value)} /></div>
      <div className="table"><div className="row labels"><span>Work item</span><span>Owner</span><span>Priority</span><span>Status</span></div>
      {visible.map(item => <div className="row" key={item.id}><strong>{item.title}</strong><span>{item.owner}</span><span className={`pill ${item.priority}`}>{item.priority}</span><span className="status">{item.status.replace("_"," ")}</span></div>)}</div>
    </section>
  </main>;
}

createRoot(document.getElementById("root")).render(<App />);
