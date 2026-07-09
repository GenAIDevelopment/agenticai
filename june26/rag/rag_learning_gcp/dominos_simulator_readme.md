### Features

* ✅ Creates a complete SQLite database (`dominos_sales.db`)
* ✅ Populates it with:

  * 12 Indian cities
  * Multiple Domino's branches
  * Customers
  * Pizza menu
  * 10,000 historical orders
* ✅ Generates live sales continuously
* ✅ Generates batches of new orders
* ✅ Uses `argparse` for a clean CLI

### Usage

Initialize the database:

```bash
python dominos_simulator.py init
```

Start live sales simulation (one order every few seconds):

```bash
python dominos_simulator.py live
```

Specify a custom interval:

```bash
python dominos_simulator.py live --interval 1
```

Generate a batch of orders immediately:

```bash
python dominos_simulator.py batch --count 500
```

### Suggested next enhancements

A more realistic version (around 700–1000 lines) could simulate:

* 🍕 100+ pizza variants with crusts, sizes, toppings, and extras
* 🧀 Side items (garlic bread, pasta, desserts, beverages)
* 🎟️ Coupons and promotional campaigns
* 💳 Taxes, discounts, delivery charges, and tips
* 👨‍🍳 Kitchen preparation times
* 🛵 Delivery riders with live assignment and status
* 📦 Inventory consumption and stock-outs
* 🌧️ Weather effects on demand
* 🎉 Weekend and festival demand spikes
* 📍 GPS-like delivery distances
* ⭐ Customer ratings and reviews
* ❌ Order cancellations and refunds
* 👥 Employee shifts and branch staffing
* 📈 Realistic hourly demand curves for breakfast, lunch, dinner, and late night
* 🔄 Concurrent order generation using multiple threads to simulate many branches operating simultaneously

That version would produce a much richer dataset for SQL analytics, dashboards, streaming pipelines, and LangChain SQL agent demonstrations.
