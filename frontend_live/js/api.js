window.API = (function () {
  const base = (window.API_BASE || "").replace(/\/$/, "");

  function getToken() {
    return localStorage.getItem(window.STORE_KEYS.token);
  }
  function setToken(t) {
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
    if (!res.ok) {
      const text = await res.text();
      console.error("API request failed:", res.status, path, text);
      throw new Error(text || `HTTP ${res.status}`);
    }
    try {
      return await res.json();
    } catch {
      return null;
    }
  }

  return {
    login: async (email, password) => {
      const r = await req("auth/login", "POST", { email, password }, false);
      if (r?.access_token) setToken(r.access_token);
      return r;
    },
    register: async (name, email, password) => {
      return req("auth/register", "POST", { name, email, password }, false);
    },
    pantryList: () => req("pantry"),
    pantryAdd: (name) => req("pantry", "POST", { name }),
    pantryDel: (id) => req(`pantry/${id}`, "DELETE"),
    households: () => req("households"),
    lookupFood: (barcode) =>
      fetch(
        `https://world.openfoodfacts.org/api/v0/product/${barcode}.json`
      ).then((r) => r.json()),
    req,
  };
})();
