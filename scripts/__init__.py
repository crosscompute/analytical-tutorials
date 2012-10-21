from sklearn.datasets import make_blobs
import numpy as np
import random


def make_shirts(count=500):
    def did_shirt_sell(hasPhoto, hasModel, price, reviewCount, reviewAverageLength, isAdvertised, isListedForSale):
        p = 0.2
        if hasModel:
            p = np.mean([p, 0.4])
        elif hasPhoto:
            p = np.mean([p, 0.3])
        if isAdvertised:
            p = np.mean([p, 0.6])
        if isListedForSale:
            p = np.mean([p, 0.5])
        if reviewCount < 5:
            p = np.mean([p, 0.1])
        price = min(30, price)
        price = max(5, price)
        p = np.mean([p, -0.04 * price + 1])
        p = np.mean([p, 0.6 / (1 + np.exp(-3 + 2))])
        return np.random.binomial(1, p)
    data = np.array([(
        random.choice([1, 0]),
        random.choice([1, 0]),
        random.gauss(15, 5),
        random.randint(0, 100),
        random.randint(10, 5000),
        random.choice([1, 0]),
        random.choice([1, 0]),
    ) for x in xrange(count)])
    target = np.array([did_shirt_sell(*x) for x in data])
    return type('Dataset', (object,), dict(
        data=data,
        target=target,
        feature_names=[
            'hasPhoto',
            'hasModel',
            'price',
            'reviewCount',
            'reviewAverageLength',
            'isAdvertised',
            'isListedForSale',
        ]))


def make_users(teenCount=250, twentyCount=500, thirtyCount=150, fortyCount=100):
    def make_user(meanAge, commonDevice):
        age = random.gauss(meanAge, 3)
        gender = random.choice(xrange(2))
        if np.random.binomial(1, 0.8):
            device = commonDevice
        else:
            otherDevices = list(set(xrange(5)) - set([commonDevice]))
            device = random.choice(otherDevices)
        return age, gender, device
    data = []
    target = []
    for x in xrange(teenCount):
        data.append(make_user(meanAge=15, commonDevice=4))
    for x in xrange(twentyCount):
        data.append(make_user(meanAge=25, commonDevice=3))
    for x in xrange(thirtyCount):
        data.append(make_user(meanAge=35, commonDevice=1))
    for x in xrange(fortyCount):
        data.append(make_user(meanAge=45, commonDevice=0))
    userCount = teenCount + twentyCount + thirtyCount + fortyCount
    locations = make_blobs(n_samples=userCount, n_features=2, centers=3)[0]
    data = np.c_[
        np.array(data),
        np.array(locations)]
    return type('Dataset', (object,), dict(
        data=data,
        feature_names=[
            'age',
            'gender',
            'device',
            'x',
            'y',
        ]))


def make_logs(inlierCount=1000, outlierCount=0):
    # Make normal data
    locations = make_blobs(n_samples=inlierCount, n_features=2, centers=3)[0]
    weekdays = [random.choice([1, 2, 3, 4, 5]) for x in xrange(inlierCount)]
    times = np.random.uniform(low=8, high=20, size=inlierCount)
    urlCounts = np.random.uniform(low=1, high=5, size=inlierCount)
    averageURLAccessCounts = np.random.uniform(low=1, high=10, size=inlierCount)
    X1 = np.c_[
        np.array(locations),
        np.array(weekdays),
        np.array(times),
        np.array(urlCounts),
        np.array(averageURLAccessCounts)]
    if not outlierCount:
        return type('Dataset', (object,), dict(data=X1))
    # Make abnormal data
    locations = make_blobs(n_samples=outlierCount, n_features=2, centers=3)[0]
    weekdays = [random.choice(xrange(7)) for x in xrange(outlierCount)]
    times = np.random.uniform(low=0, high=23, size=outlierCount)
    urlCounts = np.random.uniform(low=1, high=1000, size=outlierCount)
    averageURLAccessCounts = np.random.uniform(low=1, high=1000, size=outlierCount)
    X2 = np.c_[
        np.array(locations),
        np.array(weekdays),
        np.array(times),
        np.array(urlCounts),
        np.array(averageURLAccessCounts)]
    return type('Dataset', (object,), dict(data=np.r_[X1, X2]))
