import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../EmissionTrends-Aug2025 (1).csv")
df = df[df["Month"] != "Total"]

# Reformat "Sep-24" -> "Sep 2024"
def fmt_month(m):
    abbr, yr = m.split("-")
    return f"{abbr} 20{yr}"

df["Month"] = df["Month"].apply(fmt_month)

fig, ax = plt.subplots(figsize=(10, 5))

# Scope2 is all zeros so only plot Scope1 and Scope3
ax.bar(df["Month"], df["Scope3"], label="Scope 3")
ax.bar(df["Month"], df["Scope1"], bottom=df["Scope3"], label="Scope 1")

ax.set_title("Azure Monthly Emissions (September 2024\u2013August 2025)")
ax.set_ylabel("kgCO\u2082e")
ax.set_xlabel("Month")
ax.tick_params(axis="x", rotation=45)
ax.legend()

plt.tight_layout()
plt.savefig("report/azure_monthly.png", dpi=150, bbox_inches="tight")
plt.show()
