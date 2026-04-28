import streamlit as st
import pandas as pd
from datetime import datetime

if "step" not in st.session_state:
    st.session_state.step = 1

if "data" not in st.session_state:
    st.session_state.data = None

if "mapped_columns" not in st.session_state:
    st.session_state.mapped_columns = {}

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

if st.session_state.step == 1:
    st.title("Step 1: Upload CSV")
    file = st.file_uploader("Upload your CSV file", type=["csv"])

    if file:
        df = load_data(file)
        st.session_state.data = df
        st.success("File uploaded successfully!")
        st.dataframe(df.head(100))

        st.button("Next", on_click=next_step)

elif st.session_state.step == 2:
    st.title("Step 2: Column Mapping")

    df = st.session_state.data
    columns = df.columns.tolist()

    required_fields = ["User_ID", "Transaction_Date", "Amount"]

    for field in required_fields:
        st.session_state.mapped_columns[field] = st.selectbox(
            f"Map {field}", columns, key=field
        )

    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)

elif st.session_state.step == 3:
    st.title("Step 3: Validation & Transformation")

    df = st.session_state.data.copy()
    mapping = st.session_state.mapped_columns

    amount_col = mapping["Amount"]
    date_col = mapping["Transaction_Date"]

    st.subheader("Validation")

    if not pd.to_numeric(df[amount_col], errors='coerce').notnull().all():
        st.error("Amount column contains non-numeric values!")
    else:
        st.success("Amount column is valid.")

    try:
        pd.to_datetime(df[date_col])
        st.success("Date column is valid.")
    except:
        st.error("Date column format is invalid!")

    st.subheader("Transformations")

    if st.checkbox("Remove Duplicates"):
        key = st.selectbox("Select key column", df.columns)
        df = df.drop_duplicates(subset=[key])

    if st.checkbox("Handle Nulls"):
        fill_value = st.text_input("Fill value (or leave blank for mean)")
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if fill_value:
                    df[col] = df[col].fillna(fill_value)
                else:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        df[col] = df[col].fillna(df[col].mean())

    if st.checkbox("Add Adjusted Amount"):
        multiplier = st.number_input("Tax Multiplier", value=1.0)
        df["Adjusted_Amount"] = df[amount_col].astype(float) * multiplier

    st.session_state.data = df

    st.dataframe(df.head(100))

    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)

elif st.session_state.step == 4:
    st.title("Step 4: Export Data")

    df = st.session_state.data

    file_format = st.selectbox("Select format", ["CSV", "Excel"])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if file_format == "CSV":
        file_name = f"processed_{timestamp}.csv"
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, file_name, "text/csv")
    else:
        file_name = f"processed_{timestamp}.xlsx"
        import io
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        st.download_button("Download Excel", buffer.getvalue(), file_name)

    st.button("Back", on_click=prev_step)