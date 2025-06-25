import streamlit as st
import pandas as pd
import altair as alt


def render(df=None):
    st.title("📊 Summary Statistics")

    if df is None or df.empty:
        st.warning("⚠️ No summary data available.")
        return

    # --- Ensure Month column is sorted properly ---
    if pd.api.types.is_string_dtype(df['Month']) or pd.api.types.is_object_dtype(df['Month']):
        try:
            df['Month'] = pd.to_datetime(df['Month'], format='%B')  # Try converting month names
        except Exception:
            pass
    df = df.sort_values("Month")

    # --- Sidebar Filters ---
    st.sidebar.header("🔎 Filter Summary Statistics")

    # Unique filter options
    locations = sorted(df['Location'].dropna().unique()) if 'Location' in df else []
    months = sorted(df['Month'].dropna().unique()) if 'Month' in df else []
    authors = sorted(df['Author'].dropna().unique()) if 'Author' in df else []
    colleges = sorted(df['College'].dropna().unique()) if 'College' in df else []
    ip_types = sorted(df['IP Type'].dropna().unique()) if 'IP Type' in df else []

    # Detect numeric/stat categories
    non_cat_cols = ['Unnamed: 0', 'Location', 'Month', 'Author', 'College', 'IP Type']
    categories = [col for col in df.columns if col not in non_cat_cols and pd.api.types.is_numeric_dtype(df[col])]

    # Sidebar filter widgets
    selected_locations = st.sidebar.multiselect("📍 Location", locations, default=locations)
    selected_months = st.sidebar.multiselect("📅 Month", months, default=months)
    selected_authors = st.sidebar.multiselect("👤 Author", authors, default=authors)
    selected_colleges = st.sidebar.multiselect("🏫 College", colleges, default=colleges)
    selected_ip_types = st.sidebar.multiselect("🔖 IP Type", ip_types, default=ip_types)
    selected_categories = st.sidebar.multiselect("📊 Metrics to Analyze", categories, default=categories[:5])

    # --- Apply Filters ---
    filtered_df = df[
        df['Location'].isin(selected_locations) &
        df['Month'].isin(selected_months) &
        df['Author'].isin(selected_authors) &
        df['College'].isin(selected_colleges) &
        df['IP Type'].isin(selected_ip_types)
    ][['Location', 'Month', 'Author', 'College', 'IP Type'] + selected_categories]

    if filtered_df.empty:
        st.info("ℹ️ No data matches your filters.")
        return

    # --- Summary Cards ---
    st.markdown("### 📈 Summary of Results")
    kpi_cols = st.columns(min(4, len(selected_categories)))
    for i, cat in enumerate(selected_categories[:4]):
        avg_val = filtered_df[cat].mean()
        with kpi_cols[i]:
            st.metric(label=cat, value=f"{avg_val:,.2f}")

    # --- Line Chart: Trend Over Time ---
    st.markdown("### 📅 Trends Over Time")
    melted_df = filtered_df.melt(
        id_vars=['Location', 'Month', 'Author', 'College', 'IP Type'],
        var_name='Category',
        value_name='Value'
    )

    if not melted_df.empty:
        line_chart = alt.Chart(melted_df).mark_line(point=True).encode(
            x='Month:T',
            y='Value:Q',
            color='Category:N',
            tooltip=['Location', 'Month', 'Author', 'College', 'IP Type', 'Category', 'Value']
        ).interactive().properties(height=400)
        st.altair_chart(line_chart, use_container_width=True)

    # --- Grouped Bar Chart ---
    st.markdown("### 🏙️ Category Breakdown by Location")
    bar_df = melted_df.groupby(['Location', 'Category'])['Value'].mean().reset_index()

    if not bar_df.empty:
        bar_chart = alt.Chart(bar_df).mark_bar().encode(
            x=alt.X('Category:N', title="Category"),
            y=alt.Y('Value:Q', title="Avg Value"),
            color='Category:N',
            column=alt.Column('Location:N', title="Location"),
            tooltip=['Category', 'Location', 'Value']
        ).properties(height=300).interactive()
        st.altair_chart(bar_chart, use_container_width=True)

    # --- Download Button ---
    st.markdown("### 📥 Download Filtered Summary")
    st.download_button(
        label="Download CSV",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_summary.csv",
        mime="text/csv"
    )
