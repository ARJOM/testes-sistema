from math import sqrt


def euclidean(base, user1, user2):
    si = {}
    for item in base[user1]:
        if item in base[user2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    summation = sum([pow(base[user1][item] - base[user2][item], 2)
                     for item in base[user1] if item in base[user2]])
    return 1 / (1 + sqrt(summation))


def get_similarity(base, user):
    similarity = [{other: euclidean(base, user, other)}
                  for other in base if other != user]
    similarity.sort()
    similarity.reverse()
    return similarity[0:30]
