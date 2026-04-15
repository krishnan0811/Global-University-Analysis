import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# PAGE CONFIG
st.set_page_config(page_title="University Dashboard", layout="wide")

# GLOBAL STYLE (DARK/LIGHT FIX)
st.markdown("""
<style>

/* Insight Box */
.custom-insight {
    padding: 12px;
    border-radius: 10px;
    margin-top: 10px;
    max-width: 650px;
    margin-left: auto;
    margin-right: auto;
    font-size: 15px;
    font-weight: 500;
}

/* LIGHT MODE */
@media (prefers-color-scheme: light) {
    .custom-insight {
        background-color: #e6f0ff;
        color: #1a73e8;
        text-align: center;
    }
}

/* DARK MODE */
@media (prefers-color-scheme: dark) {
    .custom-insight {
        background-color: #1e3a5f;
        color: #4da6ff;
        text-align: left;
    }
}

</style>
""", unsafe_allow_html=True)

# TITLE
st.title(" Global University Analysis Dashboard")

# LOAD DATA

df = pd.read_csv("top_100_universities_dataset.csv")

# CLEAN COLUMNS
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# SIDEBAR FILTERS

st.sidebar.header(" Filters")

location = st.sidebar.selectbox(
    "Select Location",
    ["All"] + list(df['location'].unique())
)

uni_type = st.sidebar.selectbox(
    "University Type",
    ["All"] + list(df['university_type'].unique())
)

# APPLY FILTERS
filtered_df = df.copy()

if location != "All":
    filtered_df = filtered_df[filtered_df['location'] == location]

if uni_type != "All":
    filtered_df = filtered_df[filtered_df['university_type'] == uni_type]

# KPI SECTION

k1, k2, k3 = st.columns(3)

k1.metric(" Total Universities", len(filtered_df))

k2.metric(
    "‍ Avg Students",
    int(filtered_df['total_students'].mean()) if not filtered_df.empty else 0
)

k3.metric(
    " Locations",
    filtered_df['location'].nunique()
)

st.markdown("---")

# ROW 1

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("Top 10 Universities")

    top_uni = filtered_df.sort_values(by='position').head(10)

    fig1, ax1 = plt.subplots(figsize=(5,3))
    sns.barplot(x='position', y='university_name', data=top_uni, ax=ax1)

    ax1.set_xlabel("")
    ax1.set_ylabel("")

    st.pyplot(fig1, use_container_width=True)

    st.markdown("""
    <div class="custom-insight">
    Top-ranked universities show strong academic performance and reputation.
    </div>
    """, unsafe_allow_html=True)


with col2:
    st.subheader("Universities by Location")

    loc_counts = filtered_df['location'].value_counts().head(10)

    fig2, ax2 = plt.subplots(figsize=(5,3))
    sns.barplot(x=loc_counts.values, y=loc_counts.index, ax=ax2)

    ax2.set_xlabel("")
    ax2.set_ylabel("")

    st.pyplot(fig2, use_container_width=True)

    st.markdown("""
    <div class="custom-insight">
    Certain locations dominate global rankings.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ROW 2

col3, col4 = st.columns(2, gap="large")

with col3:
    st.subheader("Student Distribution")

    fig3, ax3 = plt.subplots(figsize=(5,3))
    sns.histplot(filtered_df['total_students'], kde=True, ax=ax3)

    ax3.set_xlabel("")
    ax3.set_ylabel("")

    st.pyplot(fig3, use_container_width=True)

    st.markdown("""
    <div class="custom-insight">
    Most universities have moderate student populations.
    </div>
    """, unsafe_allow_html=True)


with col4:
    st.subheader(" University Type")

    type_counts = filtered_df['university_type'].value_counts()

    fig4, ax4 = plt.subplots(figsize=(5,3))
    ax4.pie(
        type_counts,
        labels=type_counts.index,
        autopct='%1.1f%%',
        startangle=90
    )

    ax4.axis('equal')

    st.pyplot(fig4, use_container_width=True)

    st.markdown("""
    <div class="custom-insight">
    Public and private universities are almost equally distributed.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ROW 3

col5, col6 = st.columns(2, gap="large")

with col5:
    st.subheader("Faculty vs Students")

    fig5, ax5 = plt.subplots(figsize=(5,3))
    sns.scatterplot(
        data=filtered_df,
        x='total_faculty',
        y='total_students',
        hue='university_type',
        ax=ax5
    )

    st.pyplot(fig5, use_container_width=True)

    st.markdown("""
    <div class="custom-insight">
    Faculty size generally increases with student population.
    </div>
    """, unsafe_allow_html=True)


with col6:
    st.subheader("Campus Area vs Students")

    fig6, ax6 = plt.subplots(figsize=(5,3))
    sns.scatterplot(
        data=filtered_df,
        x='campus_area_acres',
        y='total_students',
        ax=ax6
    )

    st.pyplot(fig6, use_container_width=True)

    st.markdown("""
    <div class="custom-insight">
    Larger campuses tend to accommodate more students.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ESTABLISHMENT YEAR TREND 

st.subheader(" Establishment Year Trend")

left, center, right = st.columns([1.5, 2, 1.5])

with center:
    fig7, ax7 = plt.subplots(figsize=(3.8, 2.3))

    sns.histplot(
        data=filtered_df,
        x='established_year',
        bins=12,
        color='steelblue',
        ax=ax7
    )

    ax7.set_xlabel("")
    ax7.set_ylabel("")

    st.pyplot(fig7)

st.markdown("""
<div class="custom-insight">
Older universities often maintain higher rankings due to legacy and reputation.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# DATA TABLE

st.subheader("Filtered Data")
st.dataframe(filtered_df, use_container_width=True)

# FINAL INSIGHTS

st.subheader("Final Insights")

st.success("""
• Top universities are concentrated in specific locations  
• Most universities have moderate student capacity  
• Public & private universities are nearly balanced  
• Larger campuses generally support more students  
""")

# FOOTER

st.markdown("### Built using Python, Pandas, Seaborn & Streamlit")
