import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(page_title="SONARA SILVA", layout="wide")

st.title("🌿 SONARA SILVA Dashboard")
st.write("Smart City AI for Noise & Green Infrastructure")

# =========================
# DATA
# =========================
np.random.seed(42)
n = 300

data = pd.DataFrame({
    "noise_db": np.random.normal(72, 8, n),
    "green_cover": np.random.uniform(0, 1, n),
    "population_density": np.random.uniform(200, 1200, n),
    "distance_to_road": np.random.uniform(0, 500, n)
})

# =========================
# NORMALISASI
# =========================
scaler = MinMaxScaler()

scaled = pd.DataFrame(
    scaler.fit_transform(data),
    columns=data.columns
)

# =========================
# INDEX
# =========================
data["EDI"] = (
    0.5 * scaled["noise_db"] +
    0.3 * scaled["population_density"] +
    0.2 * (1 - scaled["green_cover"])
)

data["priority_score"] = (
    data["noise_db"] *
    (1 - data["green_cover"]) *
    data["population_density"]
)

# =========================
# KPI
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Avg Noise", f"{data['noise_db'].mean():.2f}")
col2.metric("Avg EDI", f"{data['EDI'].mean():.2f}")
col3.metric("Avg Priority", f"{data['priority_score'].mean():.2f}")

st.divider()

# =========================
# FILTER
# =========================
threshold = st.slider("Noise Threshold", 50, 100, 70)

filtered = data[data["noise_db"] > threshold]

st.subheader("High Noise Areas")
st.write(filtered.head(10))

# =========================
# VISUAL
# =========================
st.subheader("Noise vs Green Coverage")

fig, ax = plt.subplots()
ax.scatter(data["noise_db"], data["green_cover"], c=data["priority_score"], cmap="Greens")
ax.set_xlabel("Noise (dB)")
ax.set_ylabel("Green Cover")

st.pyplot(fig)

# =========================
# TOP ZONES
# =========================
st.subheader("Priority Zones")

top = data.sort_values("priority_score", ascending=False).head(10)
st.dataframe(top)
