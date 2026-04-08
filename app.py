import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# PAGE CONFIG
st.set_page_config(page_title="University Dashboard", layout="wide")

# GLOBAL STYLE (SPACING)
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# TITLE
st.markdown("## Global University Analysis Dashboard")

# LOAD DATA
df = pd.read_csv("top_100_universities_dataset.csv")

# CLEAN COLUMNS

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# SIDEBAR FILTERS

st.sidebar.header(" Filters")

location = st.sidebar.selectbox("Select Location", ["All"] + list(df['location'].unique()))
uni_type = st.sidebar.selectbox("University Type", ["All"] + list(df['university_type'].unique()))

# APPLY FILTERS FIRST 

filtered_df = df.copy()

if location != "All":
    filtered_df = filtered_df[filtered_df['location'] == location]

if uni_type != "All":
    filtered_df = filtered_df[filtered_df['university_type'] == uni_type]

# KPI COLUMNS
col1, col2, col3 = st.columns(3)

# KPIs 

col1.metric(" Total Universities", len(filtered_df))

col2.metric(
    "Avg Students",
    int(filtered_df['total_students'].mean()) if not filtered_df.empty else 0
)

col3.metric(
    " Locations",
    filtered_df['location'].nunique()
)

# ROW 1

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### Top 10 Universities")

    top_uni = filtered_df.sort_values(by='position').head(10)

    fig1, ax1 = plt.subplots(figsize=(5,3.5))
    sns.barplot(x='position', y='university_name',
                data=top_uni, palette='magma', ax=ax1)

    ax1.set_xlabel("")
    ax1.set_ylabel("")
    st.pyplot(fig1)

    st.markdown(
        "<div style='background-color:#e6f0ff;padding:10px;border-radius:10px;'>"
        "Top-ranked universities consistently show strong academic performance and global reputation."
        "</div>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown("### Universities by Location")

    loc_counts = filtered_df['location'].value_counts().head(10)

    fig2, ax2 = plt.subplots(figsize=(5,3.5))
    sns.barplot(x=loc_counts.values,
                y=loc_counts.index,
                palette='viridis',
                ax=ax2)

    ax2.set_xlabel("")
    ax2.set_ylabel("")
    st.pyplot(fig2)

    st.markdown(
        "<div style='background-color:#e6f0ff;padding:10px;border-radius:10px;'>"
        "Certain locations dominate rankings due to strong education ecosystems."
        "</div>",
        unsafe_allow_html=True
    )

st.markdown("---")

# -------- Row 2 --------
col3, col4 = st.columns(2, gap="large")

# LEFT SIDE
with col3:
    st.markdown("### Student Distribution")

    container1 = st.container()

    with container1:
        fig3, ax3 = plt.subplots(figsize=(5,3.5))  
        sns.histplot(filtered_df['total_students'],
                     bins=20,
                     kde=True,
                     color='blue',
                     ax=ax3)

        ax3.set_xlabel("")
        ax3.set_ylabel("")

        st.pyplot(fig3)

        st.markdown("""
        <div style='
            background-color:#e6f0ff;
            padding:12px;
            border-radius:10px;
            margin-top:10px;
            min-height:80px;
        '>
        Most universities have moderate student populations, with few very large institutions.
        </div>
        """, unsafe_allow_html=True)

# RIGHT SIDE
with col4:
    st.markdown("### University Type")

    container2 = st.container()

    with container2:
        type_counts = filtered_df['university_type'].value_counts()

        fig4, ax4 = plt.subplots(figsize=(4,3.5))  
        ax4.pie(type_counts,
                labels=type_counts.index,
                autopct='%1.1f%%',
                colors=sns.color_palette('Set2'),
                textprops={'fontsize':8})

        ax4.set_ylabel("")

        st.pyplot(fig4)

        st.markdown("""
        <div style='
            background-color:#e6f0ff;
            padding:8px;
            border-radius:5px;
            margin-top:5px;
            min-height:10px;
        '>
        Shows the distribution of public vs private universities.
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ROW 3
col5, col6 = st.columns(2, gap="large")

with col5:
    st.markdown("###  Faculty vs Students")

    fig5, ax5 = plt.subplots(figsize=(5,3.5))
    sns.scatterplot(data=filtered_df,
                    x='total_faculty',
                    y='total_students',
                    hue='university_type',
                    palette='cool',
                    ax=ax5)

    st.pyplot(fig5)

    st.markdown(
        "<div style='background-color:#e6f0ff;padding:10px;border-radius:10px;'>"
        "Faculty size generally increases with student population."
        "</div>",
        unsafe_allow_html=True
    )

with col6:
    st.markdown("### Campus Area vs Students")

    fig6, ax6 = plt.subplots(figsize=(5,3.5))
    sns.scatterplot(data=filtered_df,
                    x='campus_area_acres',
                    y='total_students',
                    ax=ax6)

    st.pyplot(fig6)

    st.markdown(
        "<div style='background-color:#e6f0ff;padding:10px;border-radius:10px;'>"
        "Larger campuses tend to accommodate more students, but not always proportionally."
        "</div>",
        unsafe_allow_html=True
    )

st.markdown("---")

# ROW 4
st.markdown("### Establishment Year Trend")

fig7, ax7 = plt.subplots(figsize=(5,3.5))
sns.histplot(filtered_df['established_year'],
             bins=20,
             color='purple',
             ax=ax7)

st.pyplot(fig7)

st.markdown(
    "<div style='background-color:#e6f0ff;padding:10px;border-radius:10px;'>"
    "Older universities often maintain higher rankings due to legacy and reputation."
    "</div>",
    unsafe_allow_html=True
)

st.markdown("---")

# DATA TABLE
st.subheader(" Filtered Data")
st.dataframe(filtered_df)

#FINAL INSIGHTS

st.markdown("### Final Insights")

st.success("""
 Top universities are concentrated in specific locations  
 Most universities have moderate student capacity  
 Public & private universities are nearly balanced  
 Larger campuses generally support more students  
""")

# FOOTER
st.markdown("### Built using Python, Pandas, Seaborn & Streamlit")


