import React, { useEffect, useState } from "react";

export default function PantryList() {
  const [items, setItems] = useState(null); // null = loading, [] = empty
  const [error, setError] = useState(null);

  useEffect(() => {
    const ac = new AbortController();
    setItems(null);
    fetch("/api/v1/pantry", { signal: ac.signal })
      .then((res) => {
        if (!res.ok) throw new Error("network response not ok " + res.status);
        return res.json();
      })
      .then((data) => setItems(data || []))
      .catch((err) => {
        if (err.name === "AbortError") return;
        console.error("pantry fetch error", err);
        setError(err);
        setItems([]); // stop loading
      });
    return () => ac.abort();
  }, []);

  if (items === null && !error) return <div>Loading pantry...</div>;
  if (error) return <div>Error loading pantry</div>;
  if (Array.isArray(items) && items.length === 0)
    return <div>No pantry items</div>;

  return (
    <section>
      <h2>Pantry</h2>
      <ul style={{ padding: 0, listStyle: "none" }}>
        {items.map((it) => (
          <li
            key={it.id}
            style={{
              display: "flex",
              justifyContent: "space-between",
              padding: 8,
              background: "#fff",
              marginBottom: 8,
              borderRadius: 6,
            }}
          >
            <span>{it.name}</span>
            <span style={{ color: "#666" }}>{it.qty ?? ""}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
