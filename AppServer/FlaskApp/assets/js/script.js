"use strict";

/**
 * navbar toggle
 */

const navbar = document.querySelector("[data-navbar]");
const navbarLinks = document.querySelectorAll("[data-nav-link]");
const menuToggleBtn = document.querySelector("[data-menu-toggle-btn]");

menuToggleBtn.addEventListener("click", function () {
  navbar.classList.toggle("active");
  this.classList.toggle("active");
});

for (let i = 0; i < navbarLinks.length; i++) {
  navbarLinks[i].addEventListener("click", function () {
    navbar.classList.toggle("active");
    menuToggleBtn.classList.toggle("active");
  });
}

/**
 * header sticky & back to top
 */

const header = document.querySelector("[data-header]");
const backTopBtn = document.querySelector("[data-back-top-btn]");

window.addEventListener("scroll", function () {
  if (window.scrollY >= 100) {
    header.classList.add("active");
    backTopBtn.classList.add("active");
  } else {
    header.classList.remove("active");
    backTopBtn.classList.remove("active");
  }
});

/**
 * search box toggle
 */

const searchBtn = document.querySelector("[data-search-btn]");
const searchContainer = document.querySelector("[data-search-container]");
const searchSubmitBtn = document.querySelector("[data-search-submit-btn]");
const searchCloseBtn = document.querySelector("[data-search-close-btn]");

const searchBoxElems = [searchBtn, searchSubmitBtn, searchCloseBtn];

for (let i = 0; i < searchBoxElems.length; i++) {
  searchBoxElems[i].addEventListener("click", function () {
    searchContainer.classList.toggle("active");
    document.body.classList.toggle("active");
  });
}

/**
 * move cycle on scroll
 */

const deliveryBoy = document.querySelector("[data-delivery-boy]");

let deliveryBoyMove = -80;
let lastScrollPos = 0;

window.addEventListener("scroll", function () {
  let deliveryBoyTopPos = deliveryBoy.getBoundingClientRect().top;

  if (deliveryBoyTopPos < 500 && deliveryBoyTopPos > -250) {
    let activeScrollPos = window.scrollY;

    if (lastScrollPos < activeScrollPos) {
      deliveryBoyMove += 1;
    } else {
      deliveryBoyMove -= 1;
    }

    lastScrollPos = activeScrollPos;
    deliveryBoy.style.transform = `translateX(${deliveryBoyMove}px)`;
  }
});

var filterbuttons = document.querySelectorAll(".filter-btn");
for (let i = 0; i < filterbuttons.length; i++) {
  filterbuttons[i].addEventListener("click", function () {
    document.querySelector(".filter-btn.active").classList.remove("active");
    this.classList.add("active");
    var filter = this.innerText;
    var menu_items = document.querySelectorAll(".food-menu-card-li");
    for (let j = 0; j < menu_items.length; j++) {
      if (
        filter == "All" ||
        menu_items[j].classList.contains("category-" + filter)
      ) {
        menu_items[j].style.display = "block";
      } else {
        menu_items[j].style.display = "none";
      }
    }
  });
}

async function order(product_id, confirmed) {
  try {
    const response = await fetch("/order", {
      method: "post",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ product_id: product_id, confirmed: confirmed }),
    });
    if (!response.ok) {
      throw Error(response.status);
    }
    alert("Order placed succefully");
  } catch (err) {
    if (err.message == "422") alert("Not Enough Ingridients :(");
    else alert("Somthing went wrong :(");
  }
}

async function inv_update(product_name, delta) {
  try {
    const response = await fetch("/update_inv", {
      method: "post",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ product_name: product_name, delta: delta }),
    });
    if (!response.ok) {
      throw Error(response.status);
    }
    alert("Inventory updated succefully");
  } catch (err) {
    alert("Somthing went wrong :(");
  }
}
