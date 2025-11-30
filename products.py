"""База продуктов и их КБЖУ на 100 грамм."""

PRODUCT_NUTRITION = {
    # ФРУКТЫ
    "яблоко":      {"kcal": 52,  "protein": 0.3,  "fat": 0.2,  "carbs": 14.0},
    "банан":       {"kcal": 96,  "protein": 1.5,  "fat": 0.5,  "carbs": 21.0},
    "апельсин":    {"kcal": 47,  "protein": 0.9,  "fat": 0.2,  "carbs": 12.0},
    "киви":        {"kcal": 61,  "protein": 1.1,  "fat": 0.5,  "carbs": 15.0},

    # ОВОЩИ
    "огурец":      {"kcal": 16,  "protein": 0.8,  "fat": 0.1,  "carbs": 3.0},
    "помидор":     {"kcal": 18,  "protein": 0.9,  "fat": 0.2,  "carbs": 3.9},
    "морковь":     {"kcal": 41,  "protein": 1.0,  "fat": 0.2,  "carbs": 10.0},
    "картошка":    {"kcal": 77,  "protein": 2.0,  "fat": 0.4,  "carbs": 17.0},

    # КРУПЫ / ЗЛАКИ (сырые)
    "гречка":      {"kcal": 313, "protein": 13.3, "fat": 3.4,  "carbs": 68.0},
    "рис":         {"kcal": 330, "protein": 6.7,  "fat": 0.7,  "carbs": 74.0},
    "овсянка":     {"kcal": 345, "protein": 12.0, "fat": 6.0,  "carbs": 62.0},

    # МЯСО / РЫБА
    "курица":      {"kcal": 165, "protein": 31.0, "fat": 3.6,  "carbs": 0.0},
    "индейка":     {"kcal": 160, "protein": 29.0, "fat": 4.0,  "carbs": 0.0},
    "говядина":    {"kcal": 187, "protein": 26.0, "fat": 9.0,  "carbs": 0.0},
    "лосось":      {"kcal": 208, "protein": 20.0, "fat": 13.0, "carbs": 0.0},

    # МОЛОЧНОЕ
    "молоко":      {"kcal": 42,  "protein": 3.2,  "fat": 1.0,  "carbs": 4.8},
    "кефир":       {"kcal": 40,  "protein": 3.0,  "fat": 1.0,  "carbs": 4.0},
    "творог":      {"kcal": 145, "protein": 17.0, "fat": 5.0,  "carbs": 2.0},
    "сыр":         {"kcal": 350, "protein": 25.0, "fat": 27.0, "carbs": 0.0},

    # ХЛЕБ / СЛАДОСТИ
    "хлеб":        {"kcal": 240, "protein": 8.0,  "fat": 2.0,  "carbs": 45.0},
    "шоколад":     {"kcal": 545, "protein": 7.0,  "fat": 35.0, "carbs": 52.0},
    "печенье":     {"kcal": 450, "protein": 6.0,  "fat": 14.0, "carbs": 72.0},

    # НАПИТКИ
    "сок":         {"kcal": 45,  "protein": 0.7,  "fat": 0.2,  "carbs": 10.0},
    "кола":        {"kcal": 42,  "protein": 0.0,  "fat": 0.0,  "carbs": 10.6},
}
