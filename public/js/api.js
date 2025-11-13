window.API = (function () {
  const base = (window.API_BASE || "").replace(/\/$/, "");

  function getToken() {
    return localStorage.getItem(window.STORE_KEYS.token);
  }

  function setToken(t) {
    if (!t) return;
    localStorage.setItem(window.STORE_KEYS.token, t);
  }

  function clearToken() {
    localStorage.removeItem(window.STORE_KEYS.token);
  }

  async function req(path, method = "GET", data = null, auth = true) {
    const headers = { "Content-Type": "application/json" };
    if (auth && getToken()) headers["Authorization"] = `Bearer ${getToken()}`;

    const url = `${base}/${path.replace(/^\//, "")}`;
    const res = await fetch(url, {
      method,
      headers,
      body: data ? JSON.stringify(data) : null,
      credentials: "include",
    });

    const raw = await res.text();
    let body = null;
    try {
      body = raw ? JSON.parse(raw) : null;
    } catch {
      body = raw;
    }

    if (!res.ok) {
      const msg =
        (body && (body.detail || body.message)) || `HTTP ${res.status}`;
      throw new Error(msg);
    }

    return body;
  }

  // Spoonacular: recipes by ingredients
  async function recipesByIngredients(ingredientList) {
    const key = window.SPOONACULAR_KEY;
    const q = ingredientList.join(",");

    const url = `https://api.spoonacular.com/recipes/findByIngredients?apiKey=${key}&ingredients=${encodeURIComponent(
      q
    )}&number=8&ranking=1`;

    const res = await fetch(url);
    if (!res.ok) throw new Error(`Spoonacular ${res.status}`);
    return res.json();
  }

  return {
    login: async (email, password) => {
      const r = await req("auth/login", "POST", { email, password }, false);
      const token =
        r?.access_token ||
        r?.token ||
        r?.accessToken ||
        (r?.data && r.data.token);
      if (token) setToken(token);
      return r;
    },

    register: (name, email, password) =>
      req("auth/register", "POST", { name, email, password }, false),

    pantryList: () => req("pantry"),
    pantryAdd: (name) => req("pantry", "POST", { name }),
    pantryDel: (id) => req(`pantry/${id}`, "DELETE"),

    recipesByIngredients,
    req,
    setToken,
    clearToken,
  };
})();
