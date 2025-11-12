console.log("UI script loaded");
window.authPage && console.log("authPage visible");

function saveToken(token) {
  localStorage.setItem(window.STORE_KEYS.token, token);
}
function getToken() {
  return localStorage.getItem(window.STORE_KEYS.token);
}
function saveUser(u) {
  localStorage.setItem(window.STORE_KEYS.user, JSON.stringify(u));
}
function getUser() {
  try {
    return JSON.parse(localStorage.getItem(window.STORE_KEYS.user) || "null");
  } catch {
    return null;
  }
}
async function api(path, { method = "GET", body = null, auth = true } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (auth) {
    const t = getToken();
    if (t) headers["Authorization"] = `Bearer ${t}`;
  }
  const res = await fetch(`${window.API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });
  const text = await res.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }
  if (!res.ok) {
    const msg = (data && (data.detail || data.message)) || `HTTP ${res.status}`;
    throw new Error(msg);
  }
  return data;
}

// ===== pages =====

// login.html / register flow
function authPage() {
  return {
    mode: "login", // "login" | "register"
    email: "",
    password: "",
    name: "",
    loading: false,
    error: "",
    success: "",
    toggleMode() {
      this.mode = this.mode === "login" ? "register" : "login";
      this.error = "";
      this.success = "";
    },
    async submit() {
      this.loading = true;
      this.error = "";
      this.success = "";
      try {
        if (this.mode === "register") {
          const out = await api("/auth/register", {
            method: "POST",
            auth: false,
            body: {
              name: this.name,
              email: this.email,
              password: this.password,
            },
          });
          this.success = "Registered. You can log in now.";
          // optional auto-login:
          // await this.loginInternal();
        } else {
          await this.loginInternal();
        }
      } catch (e) {
        this.error = e.message || "Failed.";
      } finally {
        this.loading = false;
      }
    },
    async loginInternal() {
      const out = await api("/auth/login", {
        method: "POST",
        auth: false,
        body: { email: this.email, password: this.password },
      });
      if (!out || !out.access_token) throw new Error("No token returned.");
      saveToken(out.access_token);
      if (out.user) saveUser(out.user);
      this.success = "Logged in.";
      // redirect to pantry
      window.location.href = "/frontend_live/pantry.html";
    },
  };
}

// pantry.html
function pantryPage() {
  return {
    loading: true,
    error: "",
    items: [],
    async init() {
      // guard
      if (!getToken()) {
        window.location.href = "/frontend_live/login.html";
        return;
      }
      try {
        this.items = await api("/pantry");
      } catch (e) {
        this.error = e.message || "Failed to load pantry.";
      } finally {
        this.loading = false;
      }
    },
    async addItem(name) {
      if (!name) return;
      try {
        const created = await api("/pantry", {
          method: "POST",
          body: { name },
        });
        this.items.push(created);
      } catch (e) {
        alert(e.message || "Failed to add.");
      }
    },
    async removeItem(id) {
      try {
        await api(`/pantry/${id}`, { method: "DELETE" });
        this.items = this.items.filter((i) => i.id !== id);
      } catch (e) {
        alert(e.message || "Failed to remove.");
      }
    },
  };
}

// recipes.html — OpenFoodFacts demo (no API key)
function recipesPage() {
  return {
    q: "",
    loading: false,
    error: "",
    results: [],
    async search() {
      this.error = "";
      this.results = [];
      if (!this.q?.trim()) return;
      this.loading = true;
      try {
        // OpenFoodFacts v2 search (free, CORS-friendly)
        // fields kept tight to avoid payload bloat
        const url = new URL("https://world.openfoodfacts.org/api/v2/search");
        url.searchParams.set("page_size", "20");
        url.searchParams.set(
          "fields",
          "product_name,brands,nutriments,image_small_url"
        );
        url.searchParams.set("nutrition_data", "on");
        url.searchParams.set("sort_by", "popularity_key");
        url.searchParams.set("search_terms", this.q.trim());

        const r = await fetch(url.toString());
        const data = await r.json();
        const products = data?.products || [];
        // Normalize a narrow shape for the UI
        this.results = products.map((p) => ({
          name: p.product_name || "(no name)",
          brand: p.brands || "",
          kcal: p.nutriments?.["energy-kcal_100g"] ?? null,
          protein: p.nutriments?.["proteins_100g"] ?? null,
          fat: p.nutriments?.["fat_100g"] ?? null,
          carbs: p.nutriments?.["carbohydrates_100g"] ?? null,
          img: p.image_small_url || "",
        }));
      } catch (e) {
        this.error = "Search failed.";
      } finally {
        this.loading = false;
      }
    },
  };
}

// simple header component (optional)
function topNav() {
  return {
    get loggedIn() {
      return !!getToken();
    },
    logout() {
      localStorage.removeItem(window.STORE_KEYS.token);
      localStorage.removeItem(window.STORE_KEYS.user);
      window.location.href = "/frontend_live/login.html";
    },
  };
}
// --- expose existing page factories to global scope for Alpine (append) ---
console.log("ui.js loaded (expose step)");
try {
  if (typeof authPage === "function") window.authPage = authPage;
  if (typeof pantryPage === "function") window.pantryPage = pantryPage;
  if (typeof recipesPage === "function") window.recipesPage = recipesPage;
  if (typeof homePage === "function") window.homePage = homePage;
  if (typeof topNav === "function") window.topNav = topNav;

  console.log("ui.js: exposed:", {
    authPage: !!window.authPage,
    pantryPage: !!window.pantryPage,
    recipesPage: !!window.recipesPage,
    homePage: !!window.homePage,
    topNav: !!window.topNav,
  });
} catch (e) {
  console.warn("ui.js: expose failed", e);
}
