console.log("UI script loaded");

// token helpers
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
  if (window.API && typeof window.API.req === "function") {
    return window.API.req(path.replace(/^\//, ""), method, body, auth);
  }
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
function homePage() {
  return {
    statusMsg: "unknown",
    async init() {
      try {
        const res = await fetch(window.API_BASE);
        this.statusMsg = res.ok
          ? "Backend reachable"
          : `Backend returned ${res.status}`;
      } catch {
        this.statusMsg = "Backend unreachable";
      }
    },
    checkHealth() {
      this.init();
    },
  };
}

function authPage() {
  return {
    mode: "login",
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
          if (window.API && typeof window.API.register === "function") {
            await window.API.register(this.name, this.email, this.password);
          } else {
            await api("/auth/register", {
              method: "POST",
              auth: false,
              body: {
                name: this.name,
                email: this.email,
                password: this.password,
              },
            });
          }
          this.success = "Registered. You can log in now.";
        } else {
          await this.loginInternal();
        }
      } catch (e) {
        this.error = (e && e.message) || "Failed.";
      } finally {
        this.loading = false;
      }
    },

    async loginInternal() {
      let out;
      if (window.API && typeof window.API.login === "function") {
        out = await window.API.login(this.email, this.password);
      } else {
        out = await api("/auth/login", {
          method: "POST",
          auth: false,
          body: { email: this.email, password: this.password },
        });
      }

      const token =
        out?.access_token ||
        out?.token ||
        out?.accessToken ||
        (out?.data && out.data.token);
      if (!token) throw new Error("No token returned.");
      saveToken(token);
      if (out.user) saveUser(out.user);
      this.success = "Logged in.";
      window.location.href = "./pantry.html";
    },
  };
}

// === PANTRY PAGE ===
function pantryPage() {
  return {
    pantry: [],

    async init() {
      const token = localStorage.getItem("token");
      if (!token) return (window.location.href = "/login.html");

      const res = await fetch(`${API_BASE}/pantry`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      this.pantry = res.ok ? await res.json() : [];
    },

    async addItem() {
      const name = document.getElementById("itemName").value.trim();
      const quantity = parseInt(document.getElementById("itemQty").value) || 1;
      const expiration_date = document.getElementById("itemExp").value;

      if (!name) return;

      const token = localStorage.getItem("token");

      const payload = { name, quantity };
      if (expiration_date) payload.expiration_date = expiration_date;

      const res = await fetch(`${API_BASE}/pantry`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        const newItem = await res.json();
        this.pantry.push(newItem);

        document.getElementById("itemName").value = "";
        document.getElementById("itemQty").value = "";
        document.getElementById("itemExp").value = "";
      }
    },

    async removeItem(id) {
      const token = localStorage.getItem("token");

      const res = await fetch(`${API_BASE}/pantry/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (res.ok) {
        this.pantry = this.pantry.filter((item) => item.id !== id);
      }
    },

    logout() {
      localStorage.removeItem("token");
      window.location.href = "/login.html";
    },
  };
}

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

        this.results = products.map((p) => ({
          name: p.product_name || "(no name)",
          brand: p.brands || "",
          kcal: p.nutriments?.["energy-kcal_100g"] ?? null,
          protein: p.nutriments?.["proteins_100g"] ?? null,
          fat: p.nutriments?.["fat_100g"] ?? null,
          carbs: p.nutriments?.["carbohydrates_100g"] ?? null,
          img: p.image_small_url || "",
        }));
      } catch {
        this.error = "Search failed.";
      } finally {
        this.loading = false;
      }
    },

    async autoFromPantry() {
      this.error = "";
      this.results = [];
      this.loading = true;

      try {
        const pantry = await api("/pantry");

        if (!Array.isArray(pantry) || pantry.length === 0) {
          this.error = "Your pantry is empty.";
          this.loading = false;
          return;
        }

        const combined = pantry.map((i) => i.name).join(" ");
        this.q = combined;

        const url = new URL("https://world.openfoodfacts.org/api/v2/search");
        url.searchParams.set("page_size", "20");
        url.searchParams.set(
          "fields",
          "product_name,brands,nutriments,image_small_url"
        );
        url.searchParams.set("nutrition_data", "on");
        url.searchParams.set("sort_by", "popularity_key");
        url.searchParams.set("search_terms", combined);

        const r = await fetch(url.toString());
        const data = await r.json();
        const products = data?.products || [];

        this.results = products.map((p) => ({
          name: p.product_name || "(no name)",
          brand: p.brands || "",
          kcal: p.nutriments?.["energy-kcal_100g"] ?? null,
          protein: p.nutriments?.["proteins_100g"] ?? null,
          fat: p.nutriments?.["fat_100g"] ?? null,
          carbs: p.nutriments?.["carbohydrates_100g"] ?? null,
          img: p.image_small_url || "",
        }));
      } catch {
        this.error = "Failed to generate suggestions from pantry.";
      } finally {
        this.loading = false;
      }
    },
  };
}

function householdsPage() {
  return {
    name: "",
    households: [],

    async init() {
      try {
        this.households = await api("/households");
      } catch {
        this.households = [];
      }
    },

    async addHousehold() {
      if (!this.name?.trim()) return;
      try {
        const h = await api("/households", {
          method: "POST",
          body: { name: this.name },
        });
        this.households.push(h);
        this.name = "";
      } catch {
        alert("Failed to add household");
      }
    },

    async removeHousehold(id) {
      try {
        await api(`/households/${id}`, { method: "DELETE" });
        this.households = this.households.filter((h) => h.id !== id);
      } catch {
        alert("Failed to delete");
      }
    },
  };
}

function topNav() {
  return {
    get loggedIn() {
      return !!getToken();
    },
    logout() {
      if (window.API && typeof window.API.clearToken === "function")
        window.API.clearToken();
      localStorage.removeItem(window.STORE_KEYS.token);
      localStorage.removeItem(window.STORE_KEYS.user);
      window.location.href = "./login.html";
    },
  };
}

// expose factories globally
console.log("ui.js loaded (expose step)");
try {
  window.authPage = authPage;
  window.pantryPage = pantryPage;
  window.recipesPage = recipesPage;
  window.homePage = homePage;
  window.householdsPage = householdsPage;
  window.topNav = topNav;

  console.log("ui.js: exposed OK");
} catch (e) {
  console.warn("ui.js: expose failed", e);
}
