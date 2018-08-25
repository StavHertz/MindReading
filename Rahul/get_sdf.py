def kernel_fn(x,h):
    return (1./h)*(np.exp(1)**(-(x**2)/h**2))

def get_sdf(spike_train,h=5):
    n=len(spike_train)
    sdf=np.zeros(n);
    for i in range(n):
        for j in range(n):
            sdf[i] += (1./n)*kernel_fn(np.abs(i-j),h)*spike_train[j]
    return sdf