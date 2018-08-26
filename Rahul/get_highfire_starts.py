def get_highfire_starts(sdf):
    sdf=sdf_out;
    sdf_trend=sdf;
    sdf_max_idx=np.argmax(sdf_trend);
    sdf_trend_subset=sdf_trend[:sdf_max_idx];
    thresh = -10000;
    minima_idx=argrelextrema(sdf_trend_subset, np.less)[0];
    i=1;
    out_idx=minima_idx[len(minima_idx)-i];
    while sdf_trend_subset[out_idx]>thresh:
        out_idx_old=out_idx;
        sdf_sub_2 = sdf[:out_idx];
        thresh=np.percentile(sdf_sub_2,75)
        sdf_trend_subset = sdf_sub_2;
        i+=1;
        out_idx=minima_idx[len(minima_idx)-i];
    return out_idx