// frontend/product.js

const params = new URLSearchParams(window.location.search);
const productId = params.get("id");
const PROD_API_URL = "https://bluemarket-56il.onrender.com/api"; 
const LOCAL_API_URL = "http://127.0.0.1:5000/api";
const API_BASE_URL = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" || window.location.hostname === "") 
    ? LOCAL_API_URL 
    : PROD_API_URL;

if (!productId) {
    window.location.href = "index.html";
}

async function loadProduct() {
    try {
        const res = await fetch(`${API_BASE_URL}/products/${productId}`);
        if (!res.ok) throw new Error("Asset not found in database.");
        const p = await res.json();

        // Populate basic info
        document.getElementById("p-name").innerText = p.name;
        document.getElementById("p-img").src = p.image_url;
        document.getElementById("p-desc").innerText = p.description || "No tactical briefing available for this asset.";
        document.getElementById("p-price").innerText = "KSh " + p.price.toLocaleString();
        document.getElementById("p-category").innerText = p.category || "Unclassified";

        // Rating
        const stars = "★".repeat(Math.round(p.rating)) + "☆".repeat(5 - Math.round(p.rating));
        document.getElementById("p-stars").innerText = stars;
        document.getElementById("p-reviews").innerText = `(${p.review_count} verified reviews)`;


        // Urgency
        if (p.stock < 10) {
            const stockTag = document.getElementById("p-stock-tag");
            stockTag.innerText = `CRITICAL: Only ${p.stock} units remaining`;
            stockTag.style.background = "rgba(255, 77, 77, 0.1)";
            stockTag.style.color = "var(--danger)";
        }

        document.getElementById("addBtn").onclick = () => addToCart(p);

        // UI Transition
        document.getElementById("product-loading").style.display = "none";
        document.getElementById("product-content").style.display = "grid";

    } catch (err) {
        console.error(err);
        document.getElementById("product-loading").innerHTML = `
            <div style="color:var(--danger); padding:40px; background:var(--bg-dark); border-radius:12px;">
                <h3>Protocol Error</h3>
                <p>${err.message}</p>
                <a href="index.html" class="nav-btn" style="text-decoration:none; margin-top:20px;">Return to Exchange</a>
            </div>
        `;
    }
}

function addToCart(p) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    cart.push(p);
    localStorage.setItem("cart", JSON.stringify(cart));
    alert(`${p.name} has been added to your secure cart.`);
}

document.addEventListener("DOMContentLoaded", loadProduct);
