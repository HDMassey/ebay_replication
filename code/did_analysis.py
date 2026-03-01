# did_analysis.py — DID Analysis Script
# Estimates the average treatment effect of turning off eBay's paid search.
# Method: Compare pre-post log revenue changes between treatment and control DMAs.
# Uses preprocessed pivot tables from preprocess.py.
# Output: LaTeX table in output/tables/did_table.tex
# Reference: Blake et al. (2014), Taddy Ch. 5
# did_analysis.py — DID Analysis Script
# Estimates the average treatment effect of turning off eBay's paid search.
# Method: Compare pre-post log revenue changes between treatment and contro>
# Uses preprocessed pivot tables from preprocess.py.
# Output: LaTeX table in output/tables/did_table.tex
# Reference: Blake et al. (2014), Taddy Ch. 5


import pandas as pd
import numpy as np
import os

# Ensure tables directory exists
os.makedirs("output/tables", exist_ok=True)

# Load pivot tables saved by preprocess.py
treated_pivot = pd.read_csv('temp/treated_pivot.csv', index_col='dma')
untreated_pivot = pd.read_csv('temp/untreated_pivot.csv', index_col='dma')

# Extract log revenue differences
r1 = treated_pivot['log_revenue_diff']
r0 = untreated_pivot['log_revenue_diff']

# Compute DID estimate
r1_bar = r1.mean()
r0_bar = r0.mean()

gamma_hat = r1_bar - r0_bar

# Compute standard error
se = np.sqrt(r1.var() / len(r1) + r0.var() / len(r0))

# Compute 95% confidence interval
ci_lower = gamma_hat - 1.96 * se
ci_upper = gamma_hat + 1.96 * se

# Print results
print("DID Results (Log Scale)")
print("=======================")
print(f"Gamma hat: {gamma_hat:.4f}")
print(f"Std Error: {se:.4f}")
print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")

import pandas as pd
import numpy as np
import os

# Ensure tables directory exists
os.makedirs("output/tables", exist_ok=True)

# Load pivot tables saved by preprocess.py
treated_pivot = pd.read_csv('temp/treated_pivot.csv', index_col='dma')
untreated_pivot = pd.read_csv('temp/untreated_pivot.csv', index_col='dma')

# Extract log revenue differences
r1 = treated_pivot['log_revenue_diff']
r0 = untreated_pivot['log_revenue_diff']

# Compute DID estimate
r1_bar = r1.mean()
r0_bar = r0.mean()

gamma_hat = r1_bar - r0_bar

# Compute standard error
se = np.sqrt(r1.var() / len(r1) + r0.var() / len(r0))

# Compute 95% confidence interval
ci_lower = gamma_hat - 1.96 * se
ci_upper = gamma_hat + 1.96 * se


# Exponentiated (levels) results
gamma_hat_exp = np.exp(gamma_hat)
ci_lower_exp = np.exp(ci_lower)
ci_upper_exp = np.exp(ci_upper)

# Print results
print("DID Results (Log Scale)")
print("=======================")
print(f"Gamma hat: {gamma_hat_exp:.4f}")
print(f"Std Error: {se:.4f}")
print(f"95% CI: [{ci_lower_exp:.4f}, {ci_upper_exp:.4f}]")

# Create LaTeX table
latex = r"""\begin{table}[h]
\centering
\caption{Difference-in-Differences Estimate of the Effect of Paid Search on Revenue}
\begin{tabular}{lcc}
\hline
& Log Scale & Levels (exp) \\
\hline
Point Estimate ($\hat{\gamma}$) & $%.4f$ & $%.4f$ \\
Standard Error & $%.4f$ & --- \\
95\%% CI & $[%.4f, \; %.4f]$ & $[%.4f, \; %.4f]$ \\
\hline
\end{tabular}
\label{tab:did}
\end{table}""" % (gamma_hat, gamma_hat_exp, se, ci_lower, ci_upper, ci_lower_exp, ci_upper_exp)

with open("output/tables/did_table.tex", "w") as f:
    f.write(latex)

