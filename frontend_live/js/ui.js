const API_BASE = "http://127.0.0.1:5000/api/v1";

// === Utilities ===
function getToken() {
  return localStorage.getItem("mygrocer_token");
}

function setToken(t) {
  localStorage.setItem("mygrocer_token", t);
}

function clearToken() {
  localStorage.removeItem("mygrocer_token");
}

async function apiFetch(endpoint, method = "GET", data = null, auth = true) {
  const opts = {
    method,
    headers: { "Content-Type": "application/json" },
  };
  if (auth && getToken())
    opts.headers["Authorization"] = `Bearer ${getToken()}`;
  if (data) opts.body = JSON.stringify(data);

  const res = await fetch(`${API_BASE}${endpoint}`, opts);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

// === Home Page ===
function homePage() {
  return {
    statusMsg: "",
    async checkHealth() {
      try {
        const r = await fetch(`${API_BASE}/health/`);
        this.statusMsg = r.ok ? "✅ API is live" : "❌ API issue";
      } catch {
        this.statusMsg = "⚠️ Connection failed";
      }
    },
    tokenPreview() {
      const t = getToken();
      return t ? t.slice(0, 40) + "..." : null;
    },
    logout() {
      clearToken();
      window.location.href = "./login.html";
    },
    init() {
      console.log("Home ready");
    },
  };
}

// === Auth Page (Login / Register) ===
function authPage() {
  return {
    email: "",
    password: "",
    message: "",
    async login() {
      try {
        const data = await apiFetch(
          "/auth/login",
          "POST",
          { email: this.email, password: this.password },
          false
        );
        setToken(data.access_token);
        this.message = "✅ Logged in successfully";
        setTimeout(() => (window.location.href = "./index.html"), 1000);
      } catch {
        this.message = "❌ Login failed";
      }
    },
    async register() {
      try {
        await apiFetch(
          "/auth/register",
          "POST",
          { email: this.email, password: this.password },
          false
        );
        this.message = "✅ Account created, you can log in now";
      } catch {
        this.message = "❌ Registration failed";
      }
    },
  };
}

// === Pantry Page ===
function pantryPage() {
  return {
    items: [],
    name: "",
    barcode: "",
    lookupResult: "",
    message: "",

    async loadItems() {
      try {
        this.items = await apiFetch("/pantry/");
      } catch {
        this.message = "⚠️ Failed to load pantry.";
      }
    },

    async addItem() {
      if (!this.name) return;
      try {
        await apiFetch("/pantry/", "POST", { name: this.name });
        this.name = "";
        this.loadItems();
        this.message = "✅ Item added.";
      } catch {
        this.message = "❌ Add failed.";
      }
    },

    async removeItem(id) {
      try {
        await apiFetch(`/pantry/${id}`, "DELETE");
        this.loadItems();
        this.message = "🗑️ Item deleted.";
      } catch {
        this.message = "❌ Delete failed.";
      }
    },

    async lookupItem() {
      if (!this.barcode) return;
      try {
        const res = await fetch(
          `https://world.openfoodfacts.org/api/v0/product/${this.barcode}.json`
        );
        const data = await res.json();
        this.lookupResult = data.product?.product_name || "No product found";
        if (this.lookupResult && !this.name) this.name = this.lookupResult;
      } catch {
        this.lookupResult = "Lookup failed";
      }
    },

    init() {
      this.loadItems();
    },
  };
}

// === Households Page ===
function householdsPage() {
  return {
    households: [],
    name: "",
    message: "",

    async loadHouseholds() {
      try {
        this.households = await apiFetch("/households/");
      } catch {
        this.message = "⚠️ Load failed.";
      }
    },

    async addHousehold() {
      if (!this.name) return;
      try {
        await apiFetch("/households/", "POST", { name: this.name });
        this.name = "";
        this.loadHouseholds();
        this.message = "✅ Household added.";
      } catch {
        this.message = "❌ Add failed.";
      }
    },

    async removeHousehold(id) {
      try {
        await apiFetch(`/households/${id}`, "DELETE");
        this.loadHouseholds();
        this.message = "🗑️ Household deleted.";
      } catch {
        this.message = "❌ Delete failed.";
      }
    },

    init() {
      this.loadHouseholds();
    },
  };
}

// === Recipes Page (Open Food Facts Demo) ===
function recipesPage() {
  return {
    barcode: "",
    product: "",
    async fetchRef() {
      if (!this.barcode) return;
      try {
        const res = await fetch(
          `https://world.openfoodfacts.org/api/v0/product/${this.barcode}.json`
        );
        const data = await res.json();
        this.product = data.product?.product_name || "No result";
      } catch {
        this.product = "Lookup failed";
      }
    },
  };
}
