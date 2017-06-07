def gen_data(file, N=None, min_n=4, max_n=10):
    if N is None:
        N = np.random.randint(min_n, max_n)
    r = []
    kern = np.exp(-np.arange(30)/10)
    for i in range(N):
        x = np.abs(np.random.randn(1000))
        spikes = x > 2
        y = np.convolve(spikes, kern, mode='same')
        r.append(y)
    r = np.vstack(r)
    r = r.squeeze()
    np.save(file, r, allow_pickle=False)
    
