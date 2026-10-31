MENU = {
    # Biryani
    "chicken biryani": {"price": 280, "veg": False, "spicy": 3},
    "mutton biryani": {"price": 380, "veg": False, "spicy": 4},
    "chicken dum biryani": {"price": 300, "veg": False, "spicy": 4},
    "mutton dum biryani": {"price": 400, "veg": False, "spicy": 4},
    "egg biryani": {"price": 220, "veg": False, "spicy": 3},
    "veg biryani": {"price": 200, "veg": True, "spicy": 2},

    # Starters and Kebabs
    "chicken 65": {"price": 220, "veg": False, "spicy": 4},
    "chicken tikka": {"price": 260, "veg": False, "spicy": 3},
    "chicken seekh kebab": {"price": 250, "veg": False, "spicy": 3},
    "tandoori chicken": {"price": 320, "veg": False, "spicy": 3},
    "apollo fish": {"price": 280, "veg": False, "spicy": 4},
    "paneer tikka": {"price": 220, "veg": True, "spicy": 2},

    # Hyderabadi Specialities
    "haleem": {"price": 180, "veg": False, "spicy": 3},
    "mutton marag": {"price": 280, "veg": False, "spicy": 2},
    "chicken  pulao": {"price": 250, "veg": False, "spicy": 3},
    "bagara baingan": {"price": 180, "veg": True, "spicy": 3},
    "mirchi ka salan": {"price": 120, "veg": True, "spicy": 4},

    # Main Course
    "butter chicken": {"price": 280, "veg": False, "spicy": 2},
    "chicken curry": {"price": 240, "veg": False, "spicy": 3},
    "mutton curry": {"price": 350, "veg": False, "spicy": 4},
    "paneer butter masala": {"price": 220, "veg": True, "spicy": 2},
    "dal tadka": {"price": 150, "veg": True, "spicy": 2},

    # Breads
    "rumali roti": {"price": 35, "veg": True, "spicy": 0},
    "butter naan": {"price": 55, "veg": True, "spicy": 0},
    "tandoori roti": {"price": 30, "veg": True, "spicy": 0},
    "garlic naan": {"price": 65, "veg": True, "spicy": 0},

    # Irani Cafe Specialities
    "irani chai": {"price": 40, "veg": True, "spicy": 0},
    "osmania biscuits": {"price": 50, "veg": True, "spicy": 0},
    "lukhmi": {"price": 100, "veg": False, "spicy": 2},
    "khara biscuit": {"price": 40, "veg": True, "spicy": 1},

    # Desserts
    "double ka meetha": {"price": 100, "veg": True, "spicy": 0},
    "qubani ka meetha": {"price": 120, "veg": True, "spicy": 0},
    "khubani ice cream": {"price": 140, "veg": True, "spicy": 0},

    # Beverages
    "badam milk": {"price": 70, "veg": True, "spicy": 0},
    "lassi": {"price": 60, "veg": True, "spicy": 0},
    "mango lassi": {"price": 80, "veg": True, "spicy": 0},
    "fresh lime soda": {"price": 50, "veg": True, "spicy": 0},
    "soft drink": {"price": 40, "veg": True, "spicy": 0},
}

COUPONS = {
    # First-time customer offers
    "FIRST50": {"type": "flat", "value": 50, "min_order": 300},
    "WELCOME100": {"type": "flat", "value": 100, "min_order": 600},

    # Percentage discounts
    "BIRYANI10": {"type": "percentage", "value": 10, "min_order": 250},
    "FOOD15": {"type": "percentage", "value": 15, "min_order": 500},
    "FAMILY20": {"type": "percentage", "value": 20, "min_order": 1000},

    # Flat discounts
    "SAVE75": {"type": "flat", "value": 75, "min_order": 500},
    "SAVE150": {"type": "flat", "value": 150, "min_order": 1000},
    "SAVE250": {"type": "flat", "value": 250, "min_order": 1500},

    # Special offers
    "HALEEM50": {"type": "flat", "value": 50, "min_order": 300},
    "IRANICHAI": {"type": "percentage", "value": 10, "min_order": 200},
    "WEEKEND25": {"type": "percentage", "value": 25, "min_order": 800},

    # Delivery and festive offers
    "FREEDEL": {"type": "flat", "value": 40, "min_order": 400},
    "CHARMINAR10": {"type": "percentage", "value": 10, "min_order": 300},
}

