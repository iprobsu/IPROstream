import streamlit as st
import pandas as pd
import altair as alt


def render(df):
    st.title("🏠 IP Dashboard Home")

    if df is None or df.empty:
        st.warning("⚠️ No data available.")
        return

    st.markdown("### 🔍 Quick Glance Overview")

    # --- Summary Cards ---
    total_records = len(df)
    unique_authors = df['Author'].nunique() if 'Author' in df else 0
    unique_colleges = df['College'].nunique() if 'College' in df else 0
    ip_types = df['IP Type'].value_counts() if 'IP Type' in df else pd.Series()

    col1, col2, col3 = st.columns(3)
    col1.metric("📄 Total Records", f"{total_records:,}")
    col2.metric("👥 Unique Authors", f"{unique_authors:,}")
    col3.metric("🏫 Colleges", f"{unique_colleges:,}")

    st.markdown("---")
    st.markdown("### 📊 IP Type Distribution")

    if not ip_types.empty:
        ip_df = ip_types.reset_index()
        ip_df.columns = ['IP Type', 'Count']

        bar_chart = alt.Chart(ip_df).mark_bar().encode(
            x=alt.X('IP Type:N', title="IP Type"),
            y=alt.Y('Count:Q', title="Total Records"),
            color='IP Type:N',
            tooltip=['IP Type', 'Count']
        ).properties(height=300).interactive()

        st.altair_chart(bar_chart, use_container_width=True)
    else:
        st.info("No IP type data available.")

    # Optional: Add pie chart or trends if 'Year' is available
    if 'Year' in df:
        st.markdown("---")
        st.markdown("### 📅 Yearly Trends")
        yearly_counts = df.groupby('Year').size().reset_index(name='Count')

        line_chart = alt.Chart(yearly_counts).mark_line(point=True).encode(
            x='Year:N',
            y='Count:Q',
            tooltip=['Year', 'Count']
        ).properties(height=300).interactive()

        st.altair_chart(line_chart, use_container_width=True)
