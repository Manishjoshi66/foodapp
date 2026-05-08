# 🍽️ FeastFlow — Food Delivery Website

A full-featured food delivery web app built with **Flask** and a stunning dark UI.

## Features
- 🏪 **6 Restaurants** with full menus (30+ items)
- 🛒 **Cart** — add/remove/update items with live drawer
- 🔐 **Auth** — register/login/logout with session management
- 💳 **Checkout** — address selection, 4 payment methods
- 🎟️ **Coupons** — FIRST50, SAVE20, FEAST100
- 📦 **Orders** — place orders, view history, live tracking UI
- 👤 **Profile** — edit details, save addresses
- 🔍 **Search** — global live search across restaurants & items
- 📱 **Responsive** — works on mobile & desktop

## Setup

```bash
cd foodapp
pip install -r requirements.txt
python app.py
```

Open: http://localhost:5000

## Coupon Codes
| Code     | Discount        | Min Order |
|----------|----------------|-----------|
| FIRST50  | ₹50 flat off   | ₹200      |
| SAVE20   | 20% off        | ₹300      |
| FEAST100 | ₹100 flat off  | ₹500      |

## Project Structure
```
foodapp/
├── app.py              # Flask backend (all routes & APIs)
├── requirements.txt
└── templates/
    ├── base.html       # Nav, auth modal, toasts, footer
    ├── index.html      # Homepage with hero, restaurants
    ├── restaurant.html # Menu page with cart drawer
    ├── cart.html       # Cart with coupon support
    ├── checkout.html   # Address, payment, place order
    ├── order_success.html  # Confirmation & tracking
    ├── orders.html     # Order history
    └── profile.html    # User profile & addresses
```
