import numpy as np

def gen_data(file=None, bins=1000, min_spikes=10, max_spikes=50, 
        kern_width=30, decay_factor=5, peak=1, noise_std=0.1):
    kern = peak * np.exp(-np.arange(kern_width)/decay_factor)
    spikes = np.zeros(bins)
    count = np.random.randint(min_spikes, max_spikes)
    idx = np.random.choice(bins, count, replace=False)
    spikes[idx] = 1
    r  = np.convolve(spikes, kern, mode='same')
    r += np.random.randn(bins) * noise_std
    if file is not None:
        np.save(file, r, allow_pickle=False)
    return r, count
