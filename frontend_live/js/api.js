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
      // expose helpful message
      const msg =
        (body && (body.detail || body.message)) || `HTTP ${res.status}`;
      console.error("API request failed:", method, url, res.status, body);
      throw new Error(msg);
    }

    return body;
  }

  return {
    login: async (email, password) => {
      const r = await req("auth/login", "POST", { email, password }, false);
      // defensive token extraction
      const token =
        r?.access_token ||
        r?.token ||
        r?.accessToken ||
        (r?.data && r.data.token);
      if (token) setToken(token);
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
    setToken,
    clearToken,
  };
})();
