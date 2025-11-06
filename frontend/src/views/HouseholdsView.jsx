import React, { useEffect, useState } from "react";
import { getHouseholds } from "../api/households";
import HouseholdCard from "../components/HouseholdCard";

export default function HouseholdsView() {
  const [households, setHouseholds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    getHouseholds()
      .then((res) => {
        setHouseholds(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("households fetch error", err);
        setError(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading households...</div>;
  if (error) return <div>Error loading households</div>;

  return (
    <div>
      <h1>Households</h1>
      <div style={{ display: "grid", gap: 12 }}>
        {households.length === 0 ? (
          <p>No households found</p>
        ) : (
          households.map((h) => <HouseholdCard key={h.id} household={h} />)
        )}
      </div>
    </div>
  );
}
