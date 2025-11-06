import React from "react";

export default function HouseholdCard({ household }) {
  return (
    <div
      style={{
        border: "1px solid #e6e6e6",
        padding: 12,
        borderRadius: 8,
        width: 340,
        boxShadow: "0 1px 2px rgba(0,0,0,0.03)",
      }}
    >
      <h3 style={{ margin: 0 }}>{household.name}</h3>
      <div style={{ fontSize: 13, color: "#555" }}>
        Members: {household.members?.length ?? 0}
      </div>
      <div style={{ fontSize: 12, color: "#888", marginTop: 8 }}>
        ID: {household.id}
      </div>
    </div>
  );
}
