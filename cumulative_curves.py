import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def i_o(df, input_col='Input', output_col='Output'):
    """
    Analyzes traffic flow from a DataFrame, handles midnight rollovers,
    and plots smooth N-Curves.
    """
    # 1. Prepare Data
    df = df.copy()
    df[input_col] = pd.to_datetime(df[input_col], format='%I:%M:%S %p')
    df[output_col] = pd.to_datetime(df[output_col], format='%I:%M:%S %p')

    # 2. Fix Midnight Rollover
    for col in [input_col, output_col]:
        for i in range(1, len(df)):
            if df.loc[i, col] < df.loc[i-1, col]:
                df.loc[i:, col] += pd.Timedelta(days=1)

    # 3. Create Unified Timeline
    timestamps = sorted(pd.concat([df[input_col], df[output_col]]).unique())
    results = pd.DataFrame({'Time': timestamps})

    # 4. Calculate Cumulative Counts
    results['In_Count'] = results['Time'].apply(lambda t: (df[input_col] <= t).sum())
    results['Out_Count'] = results['Time'].apply(lambda t: (df[output_col] <= t).sum())
    results['Queue'] = results['In_Count'] - results['Out_Count']

    # 5. Find Maximums
    max_q = results['Queue'].max()
    max_time = results.loc[results['Queue'].idxmax(), 'Time']



    # 6. Step Plotting
    plt.figure(figsize=(12, 6))
    
    # Use .step() instead of .plot() for the staircase look
    plt.step(results['Time'], results['In_Count'], label='Arrivals (Input)', 
             color='blue', lw=2, where='post')
    plt.step(results['Time'], results['Out_Count'], label='Departures (Output)', 
             color='red', lw=2, where='post')
    
    # Fill the area with the 'post' step logic
    plt.fill_between(results['Time'], results['In_Count'], results['Out_Count'], 
                     step='post', color='gray', alpha=0.2, label='Vehicles in System')

    # Vertical line for max queue
    plt.axvline(max_time, color='green', linestyle='--', alpha=0.7)

    # Format the Time Axis
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
    plt.xticks(rotation=45)
    
    plt.title(f'N-Curve Analysis (Staircase)\nMax Fleet: {max_q} vehicles at {max_time.strftime("%I:%M %p")}')
    plt.ylabel('Cumulative Vehicles')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return max_q, max_time

# To use the function:
# max_val, max_t = analyze_traffic_flow(your_dataframe)