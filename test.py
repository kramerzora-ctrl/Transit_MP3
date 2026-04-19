import pandas as pd
import matplotlib.pyplot as plt
from cumulative_curves import i_o

# 2. Load data
df = pd.read_csv('18_MF_NB_Test.csv')

# 3. Call the function directly
max_q, max_time = i_o(df)

print(f"Analysis Complete. Max Queue: {max_q}")