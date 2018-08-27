def find_min_highfire(a):
    idx_range = np.arange(len(a))
    for idx in idx_range[::-1][1:-1]:
        if (a[idx]<a[idx+1]) and (a[idx]<=a[idx-1]):
            break;
    if idx==2:
        idx=1;
    return(idx)