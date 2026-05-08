# ============================================================================
# EGYPT PRICE LEVEL AND CURRENCY DEPRECIATION ANALYSIS (1960-2024)
# Price Level Histories
# ============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator


# ============================================================================
# LOAD DATA
# ============================================================================
cpi_raw = pd.read_excel("egypt_cpi.xls", sheet_name="Data", skiprows=3, index_col=0)
exc_raw = pd.read_excel(
    "egypt_exchange.xls", sheet_name="Data", skiprows=3, index_col=0
)

# Extract and clean Egypt data
cpi_egypt = (
    pd.to_numeric(cpi_raw.loc["Egypt, Arab Rep."], errors="coerce")
    .dropna()
    .sort_index()
)
exc_egypt = (
    pd.to_numeric(exc_raw.loc["Egypt, Arab Rep."], errors="coerce")
    .dropna()
    .sort_index()
)

cpi_egypt.index = cpi_egypt.index.astype(int)
exc_egypt.index = exc_egypt.index.astype(int)


# ============================================================================
# CREATE CHART - LINEAR SCALE
# ============================================================================
plt.style.use("fivethirtyeight")

fig, ax = plt.subplots(figsize=(15, 10), facecolor="#f0f0f0")
ax.set_facecolor("#f0f0f0")
ax2 = ax.twinx()
ax2.set_facecolor("#f0f0f0")

# Plot with LINEAR SCALE (not logarithmic)
ax.plot(
    cpi_egypt.index,
    cpi_egypt,
    color="#1f77b4",
    linewidth=2,
    alpha=0.85,
    label="Consumer Price Index ",
)
ax2.plot(
    exc_egypt.index,
    exc_egypt,
    color="#d62728",
    linewidth=2,
    alpha=0.85,
    label="Exchange Rate",
)

# Set linear scales
ax.set_yscale("linear")
ax2.set_yscale("linear")

# Set logical Y-axis ticks
ax.yaxis.set_major_locator(MaxNLocator(nbins=8))
ax2.yaxis.set_major_locator(MaxNLocator(nbins=8))


# Format numbers
def format_cpi(x, pos):
    return f"{x:.0f}" if x >= 100 else (f"{x:.1f}" if x >= 10 else f"{x:.2f}")


def format_exchange(x, pos):
    return f"{x:.1f}" if x >= 1 else f"{x:.2f}"


ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_cpi))
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(format_exchange))

# Tick styling
ax.tick_params(
    axis="y", labelsize=12, labelcolor="#1f77b4", width=0.5, length=3, color="#cccccc"
)
ax2.tick_params(
    axis="y", labelsize=12, labelcolor="#d62728", width=0.5, length=3, color="#cccccc"
)

# Title and labels
ax.set_title(
    "Egypt's Price Level and Currency Depreciation (1960-2024)",
    fontsize=22,
    fontweight="bold",
    color="#333333",
    loc="left",
    pad=25,
    fontstyle="italic",
)


ax.set_ylabel("Price Level (CPI)", fontsize=14, fontweight="medium", color="#1f77b4")
ax2.set_ylabel(
    "Exchange Rate (EGP/USD)", fontsize=14, fontweight="medium", color="#d62728"
)
ax.set_xlabel("Year", fontsize=14, fontweight="medium")

# Grid and events
ax.grid(True, axis="y", linestyle="-", alpha=0.2, color="#cccccc")
ax.grid(False, axis="x")

events = {
    1973: "1973\nWar",
    1991: "1991\nReform",
    2016: "2016\nDevaluation",
    2022: "2022\nCrisis",
}

for year, label in events.items():
    ax.axvline(x=year, color="#0D0C0C", linestyle="--", alpha=0.4, lw=1.1)
    ax.text(
        year,
        ax.get_ylim()[1] * 0.9,
        label,
        fontsize=12,
        color="#000000",
        ha="center",
        fontweight="medium",
    )  # ✅ Centered - looks professional

# Legend
handles1, labels1 = ax.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
ax.legend(
    handles1 + handles2,
    labels1 + labels2,
    loc="upper left",
    bbox_to_anchor=(-0.01, 1),
    prop={"size": 12, "weight": "light"},
    frameon=False,
    borderpad=1,
    labelspacing=1.2,
)
if ax2.get_legend():
    ax2.get_legend().remove()

# Source and save
fig.text(0.01, -0.01, "Source: World Bank (2024)", fontsize=10, color="#777777")
plt.tight_layout()
plt.savefig(
    "Egypt_Price_History_Linear.png",
    dpi=300,
    facecolor=fig.get_facecolor(),
    bbox_inches="tight",
)
plt.show()
