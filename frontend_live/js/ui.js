import { CONFIG } from "./config.js";
const API_BASE = CONFIG.API_BASE;

// optional debug
console.log("API_BASE =", API_BASE);

// === Token helpers ===
function getToken() {
  return localStorage.getItem(CONFIG.TOKEN_KEY);
}
function setToken(t) {
  localStorage.setItem(CONFIG.TOKEN_KEY, t);
}
function clearToken() {
  localStorage.removeItem(CONFIG.TOKEN_KEY);
}

// === Generic API fetch ===
async function apiFetch(endpoint, method = "GET", data = null, auth = true) {
  const headers = { "Content-Type": "application/json" };
  if (auth && getToken()) headers.Authorization = `Bearer ${getToken()}`;

  const url = `${API_BASE.replace(/\/$/, "")}/${endpoint.replace(/^\//, "")}`;
  const res = await fetch(url, {
    method,
    headers,
    body: data ? JSON.stringify(data) : null,
    credentials: "include",
  });

  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

// === Pages ===
function homePage() {
  return {
    statusMsg: "",
    async checkHealth() {
      try {
        const r = await fetch(`${API_BASE.replace(/\/$/, "")}/health`);
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
  };
}

function authPage() {
  return {
    email: "",
    password: "",
    message: "",
    async login() {
      try {
        const data = await apiFetch(
          "auth/login",
          "POST",
          { email: this.email.trim().toLowerCase(), password: this.password },
          false
        );
        setToken(data.access_token);
        this.message = "✅ Logged in";
        setTimeout(() => (window.location.href = "./index.html"), 600);
      } catch (e) {
        console.error(e);
        this.message = "❌ Login failed";
      }
    },
    async register() {
      try {
        await apiFetch(
          "auth/register",
          "POST",
          { email: this.email.trim().toLowerCase(), password: this.password },
          false
        );
        this.message = "✅ Account created. Log in now.";
      } catch (e) {
        console.error(e);
        this.message = "❌ Registration failed";
      }
    },
  };
}

function pantryPage() {
  return {
    items: [],
    name: "",
    barcode: "",
    lookupResult: "",
    message: "",
    async loadItems() {
      try {
        this.items = await apiFetch("pantry");
      } catch {
        this.message = "⚠️ Failed to load pantry.";
      }
    },
    async addItem() {
      if (!this.name) return;
      try {
        await apiFetch("pantry", "POST", { name: this.name });
        this.name = "";
        this.loadItems();
        this.message = "✅ Item added.";
      } catch {
        this.message = "❌ Add failed.";
      }
    },
    async removeItem(id) {
      try {
        await apiFetch(`pantry/${id}`, "DELETE");
        this.loadItems();
        this.message = "🗑️ Item deleted.";
      } catch {
        this.message = "❌ Delete failed.";
      }
    },
    async lookupItem() {
      if (!this.barcode) return;
      try {
        const r = await fetch(
          `https://world.openfoodfacts.org/api/v0/product/${this.barcode}.json`
        );
        const d = await r.json();
        this.lookupResult = d.product?.product_name || "No product found";
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

function householdsPage() {
  return {
    households: [],
    name: "",
    message: "",
    async loadHouseholds() {
      try {
        this.households = await apiFetch("households");
      } catch {
        this.message = "⚠️ Load failed.";
      }
    },
    async addHousehold() {
      if (!this.name) return;
      try {
        await apiFetch("households", "POST", { name: this.name });
        this.name = "";
        this.loadHouseholds();
        this.message = "✅ Household added.";
      } catch {
        this.message = "❌ Add failed.";
      }
    },
    async removeHousehold(id) {
      try {
        await apiFetch(`households/${id}`, "DELETE");
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

function recipesPage() {
  return {
    barcode: "",
    product: "",
    async fetchRef() {
      if (!this.barcode) return;
      try {
        const r = await fetch(
          `https://world.openfoodfacts.org/api/v0/product/${this.barcode}.json`
        );
        const d = await r.json();
        this.product = d.product?.product_name || "No result";
      } catch {
        this.product = "Lookup failed";
      }
    },
  };
}

// expose page factories so Alpine can call x-data="authPage()"
window.homePage = homePage;
window.authPage = authPage;
window.pantryPage = pantryPage;
window.householdsPage = householdsPage;
window.recipesPage = recipesPage;
