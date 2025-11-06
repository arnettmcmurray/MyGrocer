import React, { useState } from "react";

export default function NavBar() {
  const [open, setOpen] = useState(false);

  return (
    <header className="nav">
      <div className="nav-inner">
        <div className="brand">MyGrocer</div>

        <nav className={`links ${open ? "open" : ""}`}>
          <a href="#pantry">Pantry</a>
          <a href="#lists">Lists</a>
          <a href="#recipes">Recipes</a>
          <a href="#settings">Settings</a>
        </nav>

        <button
          className="hamburger"
          aria-label="Toggle menu"
          onClick={() => setOpen((v) => !v)}
        >
          <span className="bar" />
          <span className="bar" />
          <span className="bar" />
        </button>
      </div>
    </header>
  );
}
