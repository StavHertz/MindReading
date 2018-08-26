def get_highfire_starts(sdf):
    h=25;
    sgma=h/2;
    conv_fn=stats.norm.pdf(np.arange(-25,25)/sgma)
    sdf_trend=np.convolve(sdf);
    sdf_max=np.max(sdf_trend);
    sdf_thresh=(25.0/100)*sdf_max;
    mask=np.where(sdf_trend<=sdf_thresh);
    sdf_trend_subset=sdf_trend[mask];
    minima=np.r_[True, sdf_trend_subset[1:] < sdf_trend_subset[:-1]] & np.r_[sdf_trend_subset[:-1] < sdf_trend_subset[1:], True]
