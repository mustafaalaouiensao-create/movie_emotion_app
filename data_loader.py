def search_movie(collection, title):
    return collection.find_one({"title": {"$regex": title, "$options": "i"}})

def get_recommendations(collection, emotion, genre="Tous", top_n=5):
    mapping = {
        "sadness": "joy",
        "empty": "enthusiasm",
        "hate": "love",
        "joy": "joy",
        "enthusiasm": "enthusiasm",
        "love": "love"
    }
    target = mapping.get(emotion.lower(), "joy")

    query = {}
    if genre != "Tous":
        query["genres"] = genre

    films = collection.find(query).sort([(f"vecteursentiment.{target}", -1)]).limit(top_n)
    return list(films), target
