const API = "https://mygrocer-backend.onrender.com/api/v1";
const TOKEN_KEY = "mygrocer_token";

// === Local storage helpers ===
function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}
function setToken(t) {
  localStorage.setItem(TOKEN_KEY, t);
}
function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

// === Auth Page ===
window.authPage = function () {
  return {
    mode: "login",
    email: "",
    password: "",
    message: "",
    async login() {
      try {
        const res = await fetch(`${API}/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: this.email, password: this.password }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.message || "Login failed");
        setToken(data.access_token);
        window.location.href = "./index.html";
      } catch (err) {
        this.message = err.message;
      }
    },
    async register() {
      try {
        const res = await fetch(`${API}/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: this.email, password: this.password }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.message || "Registration failed");
        this.message = "Account created! Please log in.";
        this.mode = "login";
      } catch (err) {
        this.message = err.message;
      }
    },
  };
};

// === Home Page ===
window.homePage = function () {
  return {
    message: "Welcome to MyGrocer",
  };
};

// === Pantry Page ===
window.pantryPage = function () {
  return {
    items: [],
    async init() {
      try {
        const res = await fetch(`${API}/pantry`);
        this.items = await res.json();
      } catch {
        this.items = [{ id: 1, name: "Error loading pantry" }];
      }
    },
  };
};

// === Households Page ===
window.householdsPage = function () {
  return {
    households: [],
    async init() {
      try {
        const res = await fetch(`${API}/households`);
        this.households = await res.json();
      } catch {
        this.households = [{ id: 1, name: "Error loading households" }];
      }
    },
  };
};

// === Recipes Page ===
window.recipesPage = function () {
  return {
    recipes: [],
    async init() {
      try {
        // Example: live nutrition/recipe API
        const res = await fetch(
          "https://world.openfoodfacts.org/api/v2/product/737628064502.json"
        );
        const data = await res.json();
        this.recipes = data.product ? [data.product] : [];
      } catch {
        this.recipes = [{ id: 1, name: "Error fetching recipe data" }];
      }
    },
  };
};
