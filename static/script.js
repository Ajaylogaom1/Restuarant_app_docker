
/* =========================
   1. SHOPPING CART
========================= */

// Store the selected food items
let cart = [];


/* =========================
   2. ADD ITEM TO CART
========================= */

function addToCart(name, price) {

    // Add the selected food to the cart
    cart.push({
        name: name,
        price: price
    });

    // Update the cart item count
    updateCartCount();

    // Show confirmation
    alert(name + " added to cart!");
}


/* =========================
   3. UPDATE CART COUNT
========================= */

function updateCartCount() {

    const countElement = document.getElementById("count");

    if (countElement) {
        countElement.textContent = cart.length;
    }
}


/* =========================
   4. DISPLAY CART
========================= */

function showCart() {

    // Check whether the cart is empty
    if (cart.length === 0) {
        alert("Your cart is empty! Add some delicious food.");
        return;
    }

    // Create a list of selected food items
    const items = cart
        .map(function(item, index) {
            return (
                (index + 1) + ". " +
                item.name + " - ₹" + item.price
            );
        })
        .join("\n");

    // Calculate total price
    const total = cart.reduce(function(sum, item) {
        return sum + item.price;
    }, 0);

    // Display items and total
    alert(
        "YOUR GOOD FOOD CART\n\n" +
        items +
        "\n\nTotal Items: " + cart.length +
        "\nTotal Price: ₹" + total
    );
}


/* =========================
   5. INITIALIZE WEBSITE
========================= */

document.addEventListener("DOMContentLoaded", function() {

    updateCartCount();

    console.log("The Good Food website is ready!");

});
