def anime_searcher(map_dict, input_anime):
    from fuzzywuzzy import fuzz
    match_tuple = []
    for title, idx in map_dict.items():
        ratio = fuzz.ratio(title.lower(), input_anime.lower())
        if ratio >= 60:
            match_tuple.append((title, idx, ratio))
    match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
    if not match_tuple:
        print('not found')
        return
    print('found possible matches: {0}\n'.format([x[0] for x in match_tuple]))
    return match_tuple, match_tuple[0][1]

def make_recommendation(knn_model, data, map_dict, input_anime, n_recommendations):
    match_tuple,idx = anime_searcher(map_dict, input_anime)

    temp_txt = ''
    temp_txt += 'Possible match: ' + str([x[0] for x in match_tuple])

    knn_model.fit(data)

    distances, indices = knn_model.kneighbors(data[idx], n_neighbors=n_recommendations+1)
    raw_recommends = \
        sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
    reverse_mapper = {v: k for k, v in map_dict.items()}
    

    temp_txt += '\nYou have input movie: ' + str(input_anime)
    temp_txt += '\nRecommendation system start to make inference'
    temp_txt += '\n......'
    temp_txt += '\nRecommendations for {}:'.format(input_anime)
    
    for i, (idx, dist) in enumerate(raw_recommends):
        temp_txt += '\n{0}: {1}, with distance of {2}'.format(i+1, reverse_mapper[idx], dist)

    return temp_txt


def getPredictions(input_anime):
    import pickle
    from scipy.sparse import csr_matrix, load_npz
    knn_model = pickle.load(open(r"C:\Users\Peter\personal\recommendation\animeDjango\animeDjangoApp\knnpickle_file", "rb"))
    anime_map = pickle.load(open(r"C:\Users\Peter\personal\recommendation\animeDjango\animeDjangoApp\anime_map", "rb"))
    spar_mat = load_npz(r"C:\Users\Peter\personal\recommendation\animeDjango\animeDjangoApp\user_ratings_sparse.npz")

    pred = make_recommendation(knn_model, spar_mat, anime_map, input_anime, 10)

    return pred