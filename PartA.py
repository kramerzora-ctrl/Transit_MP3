import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def i_o(df, input_col='Input', output_col='Output', title = None, in_label='Input', out_label='Output'):
    """
    Analyzes traffic flow from a DataFrame, handles midnight rollovers,
    and plots smooth N-Curves.
    """
    df = df.copy()
    df[input_col] = pd.to_datetime(df[input_col], format='%I:%M %p')
    df[output_col] = pd.to_datetime(df[output_col], format='%I:%M %p')

    for col in [input_col, output_col]:
        for i in range(1, len(df)):
            if df.loc[i, col] < df.loc[i-1, col]:
                df.loc[i:, col] += pd.Timedelta(days=1)

    timestamps = sorted(pd.concat([df[input_col], df[output_col]]).unique())
    results = pd.DataFrame({'Time': timestamps})

    results['In_Count'] = results['Time'].apply(lambda t: (df[input_col] <= t).sum())
    results['Out_Count'] = results['Time'].apply(lambda t: (df[output_col] <= t).sum())
    results['Queue'] = results['In_Count'] - results['Out_Count']

    max_q = results['Queue'].max()
    max_time = results.loc[results['Queue'].idxmax(), 'Time']
    
    peak_times = results[results['Queue'] == max_q]['Time']
    
    peak_start = peak_times.min()
    peak_end = peak_times.max()
    
    if peak_start == peak_end:
        peak_display_end = peak_start + pd.Timedelta(minutes=5)
    else:
        peak_display_end = peak_end

    peak_info = {
        'start': peak_start,
        'end': peak_end,
        'max_count': max_q
    }

    plt.figure(figsize=(12, 6))
    
    plt.step(results['Time'], results['In_Count'], label=in_label, 
             color='blue', lw=2, where='post')
    plt.step(results['Time'], results['Out_Count'], label=out_label, 
             color='red', lw=2, where='post')
    
    plt.fill_between(results['Time'], results['In_Count'], results['Out_Count'], 
                     step='post', color='gray', alpha=0.2, label='Vehicles in System')

    plt.axvline(max_time, color='green', linestyle='--', alpha=0.7)

    # Format the Time Axis
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
    plt.xticks(rotation=45)
    
    if title:
        plt.title(f"{title}\nMax Busses: {max_q} at {max_time.strftime('%I:%M %p')}")
    else:
        plt.title(f"N-Curve Analysis: {input_col}\nMax Busses: {max_q}")    
    plt.ylabel('Cumulative Vehicles')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return max_q, max_time, peak_info, df


# To use the function:
# max_val, max_t = analyze_traffic_flow(your_dataframe)