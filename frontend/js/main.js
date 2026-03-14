// Set this to your Render/Production backend URL after deployment
const PROD_API_URL = "https://bluemarket-56il.onrender.com/api"; 
const LOCAL_API_URL = "http://127.0.0.1:5000/api";

const API_BASE_URL = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" || window.location.hostname === "")
    ? LOCAL_API_URL
    : PROD_API_URL;
let allProducts = [];

// --- Fetch products from backend ---
async function loadProducts() {
  const container = document.getElementById("products");
  const skeleton = document.getElementById("skeleton-grid");

  if (!container) return;

  try {
    const res = await fetch(`${API_BASE_URL}/products`);
    if (!res.ok) throw new Error("Failed to fetch products");
    allProducts = await res.json();

    // Hide skeleton and show products after a small delay for smoother feel
    setTimeout(() => {
      if (skeleton) skeleton.style.display = "none";
      container.style.display = "grid";
      filterProducts(); // Initial render with filters
    }, 600);

  } catch (err) {
    console.error("Error fetching products:", err);
    skeleton.innerHTML = `<p style="text-align:center; padding:50px; color:var(--danger)">Connection Error: Please check if the backend is running.</p>`;
  }
}

// --- Render products to the grid ---
function renderProducts(products) {
  const container = document.getElementById("products");
  if (!container) return;

  if (products.length === 0) {
    container.innerHTML = "<div style='grid-column: 1/-1; text-align:center; padding:80px;'><p style='font-size:1.5rem; opacity:0.5;'>No matching assets found.</p></div>";
    return;
  }

  container.innerHTML = products.map(p => {
    // Escape single quotes
    const productData = JSON.stringify(p).replace(/'/g, "&apos;");
    const stars = "★".repeat(Math.round(p.rating)) + "☆".repeat(5 - Math.round(p.rating));

    return `
      <div class="card" onclick="openProduct('${p.id}')" style="cursor: pointer;">
        <div class="card-img-wrapper">
          <img src="${p.image_url}" alt="${p.name}" loading="lazy" onerror="this.src='https://via.placeholder.com/400x300?text=Asset+Image'">
        </div>
        <div class="card-content">
          <span class="card-category">${p.category}</span>
          <h3 class="card-title">${p.name}</h3>
          <div class="card-meta">
            <div class="card-price">KSh ${p.price.toLocaleString()}</div>
            <div class="rating">
              <span>${stars}</span>
              <span style="font-size: 0.7rem; opacity: 0.6;">(${p.review_count})</span>
            </div>
          </div>
          <div class="card-footer">
            <button class="btn-add" onclick="event.stopPropagation(); addToCart('${p.id}')">Quick Add</button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// --- Filter & Sort Products ---
function filterProducts() {
  const category = document.getElementById("categoryFilter")?.value || "all";
  const searchTerm = document.getElementById("searchInput")?.value.toLowerCase() || "";
  const sortOrder = document.getElementById("sortOrder")?.value || "newest";

  // Filter
  let filtered = allProducts.filter(p => {
    const matchesCategory = category === "all" || p.category === category;
    const matchesSearch = p.name.toLowerCase().includes(searchTerm) ||
      (p.description && p.description.toLowerCase().includes(searchTerm)) ||
      p.category.toLowerCase().includes(searchTerm);
    return matchesCategory && matchesSearch;
  });

  // Sort
  if (sortOrder === "price-low") {
    filtered.sort((a, b) => a.price - b.price);
  } else if (sortOrder === "price-high") {
    filtered.sort((a, b) => b.price - a.price);
  } else if (sortOrder === "popular") {
    filtered.sort((a, b) => b.review_count - a.review_count);
  } else if (sortOrder === "newest") {
    filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }

  renderProducts(filtered);
}

// --- Navigation ---
function openProduct(id) {
  window.location.href = `product.html?id=${id}`;
}

function goToCart() {
  window.location.href = "cart.html";
}

function goToProfile() {
  window.location.href = "profile.html";
}

// --- Add product to cart ---
function addToCart(productId) {
  const product = allProducts.find(p => p.id === productId);
  if (!product) return;

  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  cart.push(product);
  localStorage.setItem("cart", JSON.stringify(cart));

  updateCartBadge();
  alert(`Asset Secured: ${product.name} added to tactical inventory.`);
}

function updateCartBadge() {
  const cart = JSON.parse(localStorage.getItem("cart")) || [];
  const badge = document.getElementById("cartCountBadge");
  if (badge) {
    if (cart.length > 0) {
      badge.innerText = cart.length;
      badge.style.display = "inline-block";
    } else {
      badge.style.display = "none";
    }
  }
}

// --- Auth Handling ---
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");
const toggleAuth = document.getElementById("toggleAuth");
const statusMsg = document.getElementById("authStatus");

if (toggleAuth) {
  toggleAuth.addEventListener("click", e => {
    e.preventDefault();
    const isLogin = loginForm.style.display !== "none";
    loginForm.style.display = isLogin ? "none" : "block";
    registerForm.style.display = isLogin ? "block" : "none";
    document.getElementById("formTitle").innerText = isLogin ? "Join the Market" : "Welcome Back";
    toggleAuth.innerText = isLogin ? "Login here" : "Register here";
    document.getElementById("toggleText").innerText = isLogin ? "Already a member?" : "New to the exchange?";
    statusMsg.innerText = "";
  });
}

if (loginForm) {
  loginForm.addEventListener("submit", async e => {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
      const res = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();

      if (res.ok) {
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("user_email", data.email);
        window.location.href = "index.html";
      } else {
        statusMsg.innerText = data.error || "Authentication failed";
      }
    } catch (err) {
      console.error("Login error:", err);
      statusMsg.innerText = "Protocol error: check connection";
    }
  });
}

if (registerForm) {
  registerForm.addEventListener("submit", async e => {
    e.preventDefault();
    const username = document.getElementById("reg-username").value;
    const email = document.getElementById("reg-email").value;
    const password = document.getElementById("reg-password").value;

    try {
      const res = await fetch(`${API_BASE_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password })
      });
      const data = await res.json();

      if (res.ok) {
        statusMsg.innerText = "Registration successful! You can now login.";
        statusMsg.style.color = "var(--primary)";
        setTimeout(() => toggleAuth.click(), 2000);
      } else {
        statusMsg.innerText = data.error || "Registration failed";
        statusMsg.style.color = "var(--danger)";
      }
    } catch (err) {
      console.error("Registration error:", err);
      statusMsg.innerText = "Protocol error during registration";
    }
  });
}

// --- Event Listeners ---
document.getElementById("categoryFilter")?.addEventListener("change", filterProducts);
document.getElementById("sortOrder")?.addEventListener("change", filterProducts);
document.getElementById("searchInput")?.addEventListener("input", filterProducts);

// --- Initialize ---
document.addEventListener("DOMContentLoaded", () => {
  loadProducts();
  updateCartBadge();
});
