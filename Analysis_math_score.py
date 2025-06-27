import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import io
from PIL import Image

st.title("Phân tích dữ liệu điểm số học sinh")
uploaded_file = st.file_uploader("Chọn file Excel (có cột 'Điểm số')", type=["xlsx"])

# Function
# compute average score
def calculate_average(scores):
    return sum(scores) / len(scores)

def percentage_distribution(scores):
    bins = {"90-100": 0, "80-90": 0, "70-79": 0, "60-69": 0, "<60": 0}
    for score in scores:
        if score >=90:
            bins["90-100"] +=1
        elif score >= 80:
            bins["80-90"] += 1
        elif score >= 70:
            bins["70-79"] += 1
        elif score >= 60:
            bins["60-69"] += 1
        else:
            bins["<60"] += 1
    return bins

# read file 
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    if "Điểm số" not in df.columns:
        st.error("File không chứa cột 'Điểm số'")
        st.stop()
    # Analysis images and scores
    scores = df["Điểm số"].dropna().astype(float).tolist()

    if scores:
    # Show the indices
        st.write("The total of students: ", len(scores))
        st.write("The average: ", round(calculate_average(scores), 2))

    dist = percentage_distribution(scores)
    labels = list(dist.keys())
    values = list(dist.values())

    fig, ax = plt.subplots(figsize=(1,1))
    ax.pie(values, labels=labels, autopct="%1.1f%%", textprops={"fontsize": 3.5})
    ax.axis("equal")
    plt.tight_layout(pad=0.1)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300)
    buf.seek(0)
    st.markdown("Biểu đồ phân bố điểm số")
    img = Image.open(buf)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(img, width=300)
        st.markdown("Biểu đồ phân bố điểm số")

