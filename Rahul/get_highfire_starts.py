def get_highfire_starts(sdf):
    h=25;
    sgma=h/2;
    conv_fn=stats.norm.pdf(np.arange(-25,25)/sgma)
    sdf_trend=np.convolve(sdf);
    sdf_max=np.max(sdf_trend);
    sdf_thresh=(25.0/100)*sdf_max;
    mask=np.where(sdf_trend<=sdf_thresh);
    sdf_trend_subset=sdf_trend[mask];
    thresh = -10000;
    minima_idx=argrelextrema(sdf_trend_subset, np.less)[0];
    i=1;
    out_idx=minima_idx[len(minima_idx)-i];
    while sdf_trend_subset[out_idx]>thresh:
        out_idx_old=out_idx;
        sdf_sub_2 = sdf[:out_idx];
        thresh=np.quantile(sdf_sub_2,0.75)
        sdf_trend_subset = sdf_sub_2;
        i+=1;
        out_idx=minima_idx[len(minima_idx)-i];
    return out_idx