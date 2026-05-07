import numpy as np

# === Les 13 émotions ===
labels = [
    "anger",
    "boredom",
    "empty",
    "enthusiasm",
    "fun",
    "happiness",
    "hate",
    "love",
    "neutral",
    "relief",
    "sadness",
    "surprise",
    "worry"
]

# =========================================================
# Similarité Cosinus
# =========================================================
def cosine_similarity(vec1, vec2):

    v1 = np.array([
        vec1.get(label, 0)
        for label in labels
    ])

    v2 = np.array([
        vec2.get(label, 0)
        for label in labels
    ])

    # éviter division par zéro
    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
        return 0

    return np.dot(v1, v2) / (
        np.linalg.norm(v1) * np.linalg.norm(v2)
    )

# =========================================================
# Entropie émotionnelle
# =========================================================
def balance_entropy(vector):

    v = np.array([
        vector.get(label, 0)
        for label in labels
    ])

    total = np.sum(v)

    if total == 0:
        return 0

    p = v / total

    return -np.sum(
        p * np.log(p + 1e-9)
    )

# =========================================================
# Construction du vecteur cible dynamique
# =========================================================
def build_dynamic_target(user_vector, gamma=0.7):

    user_values = np.array([
        user_vector.get(label, 0)
        for label in labels
    ])

    max_val = np.max(user_values)

    if max_val == 0:
        max_val = 1

    weights = {}

    target = np.zeros(len(labels))

    for i, lbl in enumerate(labels):

        # poids dynamique
        w_i = (user_values[i] / max_val) * gamma

        weights[lbl] = round(w_i, 3)

        target[i] = user_values[i] * w_i

    dominant_idx = np.argmax(user_values)

    dominant_label = labels[dominant_idx]

    # Normalisation
    if np.sum(target) > 0:
        target = target / np.sum(target) * 100

    target_vector = {
        labels[i]: round(float(target[i]), 2)
        for i in range(len(labels))
    }

    return target_vector, dominant_label, weights

# =========================================================
# Score final du film
# =========================================================
def film_score(
    user_vector,
    film_vector,
    target_vector,
    alpha=0.7,
    beta=0.3
):

    sim = cosine_similarity(
        target_vector,
        film_vector
    )

    balance = balance_entropy(
        film_vector
    )

    return alpha * sim + beta * balance

# =========================================================
# Recommandation principale
# =========================================================
def get_recommendations(
    collection,
    user_vector,
    top_n=5,
    year_min=2010
):

    # Construction du vecteur cible
    target_vector, dominant_label, weights = (
        build_dynamic_target(user_vector)
    )

    print("Emotion dominante :", dominant_label)
    print("Poids dynamiques :", weights)

    query = {
        "year": {"$gte": year_min},
        "vecteursentiment": {"$exists": True}
    }

    films = collection.find(query).limit(1000)

    scored = []

    for film in films:

        film_vector = film.get(
            "vecteursentiment",
            {}
        )

        score = film_score(
            user_vector,
            film_vector,
            target_vector
        )

        rating = film.get("rating", 0)

        scored.append(
            (film, score, rating)
        )

    # Tri décroissant
    scored = sorted(
        scored,
        key=lambda x: (x[1], x[2]),
        reverse=True
    )[:top_n]

    results = []

    for f, score, _ in scored:

        results.append({

            "title":
                f.get("title", ""),

            "poster_url":
                f.get("poster_url", ""),

            "synopsis":
                f.get("synopsis", ""),

            "genres":
                f.get("genres", []),

            "year":
                f.get("year", ""),

            "rating":
                f.get("rating", 0),

            "duration":
                f.get("duration", ""),

            "score":
                round(score, 4),

            "vecteursentiment":
                f.get("vecteursentiment", {})
        })

    return results

# =========================================================
# Recommandation par émotion dominante
# =========================================================
def get_recommendations_by_emotion(
    collection,
    emotion,
    top_n=5,
    year_min=2010
):

    query = {
        f"vecteursentiment.{emotion}": {
            "$exists": True
        },
        "year": {
            "$gte": year_min
        }
    }

    films = collection.find(query).limit(1000)

    scored = []

    # vecteur cible émotion pure
    target_vector = {
        emo: 100 if emo == emotion else 0
        for emo in labels
    }

    for film in films:

        film_vector = film.get(
            "vecteursentiment",
            {}
        )

        sim = cosine_similarity(
            target_vector,
            film_vector
        )

        rating = film.get("rating", 0)

        scored.append(
            (film, sim, rating)
        )

    scored = sorted(
        scored,
        key=lambda x: (x[1], x[2]),
        reverse=True
    )[:top_n]

    results = []

    for f, sim, _ in scored:

        results.append({

            "title":
                f.get("title", ""),

            "poster_url":
                f.get("poster_url", ""),

            "synopsis":
                f.get("synopsis", ""),

            "genres":
                f.get("genres", []),

            "year":
                f.get("year", ""),

            "rating":
                f.get("rating", 0),

            "duration":
                f.get("duration", ""),

            "similarity":
                round(sim, 4),

            "vecteursentiment":
                f.get("vecteursentiment", {})
        })

    return results