import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Step 1: Load and prepare data
# ----------------------------

df = pd.read_csv('input/PaidSearch.csv')

# Parse dates (explicit format removes warning)
df['date'] = pd.to_datetime(df['date'], format='%d-%b-%y')

# Create log revenue variable
df['log_revenue'] = np.log(df['revenue'])


# ----------------------------
# Step 2: Create pivot tables
# ----------------------------

# Separate treated and untreated groups
treated = df[df['search_stays_on'] == 0]
untreated = df[df['search_stays_on'] == 1]

# Pivot tables (mean log revenue by DMA and treatment period)
treated_pivot = treated.pivot_table(
    index='dma',
    columns='treatment_period',
    values='log_revenue',
    aggfunc='mean'
)

untreated_pivot = untreated.pivot_table(
    index='dma',
    columns='treatment_period',
    values='log_revenue',
    aggfunc='mean'
)

# Rename columns safely
treated_pivot = treated_pivot.rename(columns={
    0: 'log_revenue_pre',
    1: 'log_revenue_post'
})

untreated_pivot = untreated_pivot.rename(columns={
    0: 'log_revenue_pre',
    1: 'log_revenue_post'
})

# Compute pre-post differences
treated_pivot['log_revenue_diff'] = (
    treated_pivot['log_revenue_post'] -
    treated_pivot['log_revenue_pre']
)

untreated_pivot['log_revenue_diff'] = (
    untreated_pivot['log_revenue_post'] -
    untreated_pivot['log_revenue_pre']
)

# Save intermediate files (not committed to Git)
treated_pivot.to_csv('temp/treated_pivot.csv')
untreated_pivot.to_csv('temp/untreated_pivot.csv')


# ----------------------------
# Step 3: Print summary stats
# ----------------------------

print(f"Treated DMAs: {treated['dma'].nunique()}")
print(f"Untreated DMAs: {untreated['dma'].nunique()}")
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")


# ----------------------------
# Step 4: Reproduce Figure 5.2
# ----------------------------

daily_avg = df.groupby(['date', 'search_stays_on'])['revenue'].mean().reset_index()

pivot = daily_avg.pivot(
    index='date',
    columns='search_stays_on',
    values='revenue'
)

plt.figure(figsize=(10, 6))

plt.plot(pivot.index, pivot[1], label='Control (search stays on)')
plt.plot(pivot.index, pivot[0], label='Treatment (search goes off)')

plt.axvline(pd.to_datetime('2012-05-22'), linestyle='--')

plt.xlabel('Date')
plt.ylabel('Revenue')
plt.title('Average Revenue by Group Over Time')
plt.legend()

plt.savefig('output/figures/figure_5_2.png')
plt.close()


# ----------------------------
# Step 5: Reproduce Figure 5.3
# ----------------------------

daily_log = df.groupby(['date', 'search_stays_on'])['log_revenue'].mean().reset_index()

pivot_log = daily_log.pivot(
    index='date',
    columns='search_stays_on',
    values='log_revenue'
)

pivot_log['diff'] = pivot_log[1] - pivot_log[0]

plt.figure(figsize=(10, 6))

plt.plot(pivot_log.index, pivot_log['diff'])

plt.axvline(pd.to_datetime('2012-05-22'), linestyle='--')

plt.xlabel('Date')
plt.ylabel('log(rev_control) - log(rev_treat)')
plt.title('Log Revenue Difference Over Time')

plt.savefig('output/figures/figure_5_3.png')
plt.close()
