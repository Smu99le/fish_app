def summarize_by_client(df):
    if df.empty:
        return df

    group_cols = ['cust_name']
    if 'phone' in df.columns:
        group_cols.append('phone')
    return (
        df
        .groupby(group_cols, as_index=False)
        .agg(
            total_kg=("kg", "sum"),
            total_amount=("total", "sum")
        )
    )
