from sklearn.metrics.pairwise import cosine_similarity


def rank(products, taste_vector):

    scores = []

    for p in products:

        similarity = cosine_similarity([p["vector"]], [taste_vector])[0][0]

        scores.append((similarity, p))

    scores.sort(reverse=True)

    return [p for s, p in scores]
