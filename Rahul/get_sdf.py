def kernel_fn(x,h):
    return (1./h)*(np.exp(1)**(-(x**2)/h**2))

def get_sdf(spike_train,h=None):
    n=len(spike_train)
    sdf=np.zeros(n);
    out=np.abs(np.mgrid[0:n,0:n][0]-np.matrix.transpose(np.mgrid[0:n,0:n][0]))
    sdf=1000*np.mean(kernel_fn(out,h)*spike_train,axis=1)
#     for i in range(n):
#         for j in range(n):
#             sdf[i] += (1./n)*kernel_fn(np.abs(i-j),h)*spike_train[j]
    return sdf