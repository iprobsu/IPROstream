import streamlit as st
import pandas as pd

# --- Save logic ---
def save_changes(df):
    df.to_csv("data/edited_data.csv", index=False)
    st.success("✅ Changes saved successfully!")

# --- Render edit page ---
def render(df):
    st.title("✏️ Edit IP Data")

    if st.session_state.role != "Admin":
        st.warning("⚠️ Only Admins can edit or delete data.")
        st.dataframe(df, use_container_width=True)
        return

    st.markdown("### 🧮 Toggle Edit Mode")
    edit_mode = st.toggle("Enable editing", key="edit_mode")

    if edit_mode:
        st.markdown("#### 📝 Excel-like Editor")
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            key="editable_table"
        )

        st.markdown("---")
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("💾 Save Changes"):
                save_changes(edited_df)

        with col2:
            row_to_delete = st.number_input(
                "Enter row index to delete",
                min_value=0,
                max_value=len(edited_df)-1,
                step=1,
                key="row_delete_input"
            )
            if st.button("🗑️ Delete Row"):
                edited_df.drop(index=row_to_delete, inplace=True)
                edited_df.reset_index(drop=True, inplace=True)
                save_changes(edited_df)
                st.rerun()

    else:
        st.markdown("#### 🔒 View-Only Table")
        st.dataframe(df, use_container_width=True)
