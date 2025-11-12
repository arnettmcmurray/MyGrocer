import { CONFIG } from "./config.js";
const API_BASE = CONFIG.API_BASE;
console.log("✅ Live build loaded");
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

// === Home Page ===
function homePage() {
  return {
    statusMsg: "",
    async checkHealth() {
      try {
        const r = await fetch(`${API_BASE}/health`);
        this.statusMsg = r.ok ? "✅ API is live" : "❌ API issue";
      } catch {
        this.statusMsg = "⚠️ Connection failed";
      }
    },
    logout() {
      clearToken();
      window.location.href = "./login.html";
    },
    init() {
      this.checkHealth();
    },
  };
}

// === Auth Page ===
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
          {
            email: this.email.trim().toLowerCase(),
            password: this.password,
          },
          false
        );
        setToken(data.access_token);
        this.message = "✅ Logged in";
        setTimeout(() => (window.location.href = "./index.html"), 700);
      } catch {
        this.message = "❌ Login failed";
      }
    },
    async register() {
      try {
        await apiFetch(
          "auth/register",
          "POST",
          {
            email: this.email.trim().toLowerCase(),
            password: this.password,
          },
          false
        );
        this.message = "✅ Account created. Log in now.";
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
    message: "",
    async loadItems() {
      try {
        this.items = await apiFetch("pantry");
      } catch {
        this.message = "⚠️ Failed to load pantry.";
      }
    },
    async addItem() {
      const name = prompt("Item name:");
      if (!name) return;
      await apiFetch("pantry", "POST", { name });
      this.loadItems();
    },
    init() {
      this.loadItems();
    },
  };
}

// === Recipes Page ===
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

// === Expose for Alpine ===
window.homePage = homePage;
window.authPage = authPage;
window.pantryPage = pantryPage;
window.recipesPage = recipesPage;
