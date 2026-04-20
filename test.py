import pandas as pd
import matplotlib.pyplot as plt
from PartA import i_o

# 2. Load data
df = pd.read_csv('MP3 Starter Code/MP3_52 copy.csv')
df['Input_SB'] = pd.to_datetime(df['Input_SB'], format='%I:%M %p')
df = df.sort_values(by='Input_SB').reset_index(drop=True)
df = df.dropna(subset=['Input_SB', 'Output_SB'])

# 3. Call the function directly
max_q, max_time, peak_info, df_final = i_o(df, input_col='Input_SB', output_col='Output_SB', title='52 Southbound', in_label='El Cerrito BART', out_label='Bancroft & Telegraph')

durations = df_final['Output_SB'] - df_final['Input_SB']
total_timedelta = durations.sum()

# 3. Convert to a readable number (Total Hours as a float)
total_hours = total_timedelta.total_seconds() / 3600



print(f"Total Bus Hours: {total_hours:.2f}")
print(f"Analysis Complete. Max Busses: {max_q} at time: {max_time} for period: {peak_info}")