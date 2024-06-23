import streamlit as st
import pandas as pd
import pdfplumber

from transaction_processing import *

def extract_tables_from_pdf(pdf_files, variant=None):
    all_tables = []
    for pdf_file in pdf_files:
        with pdfplumber.open(pdf_file) as pdf:
            tables_in_pdf = []

            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    df = eval(variant.name)().transactions(table=table)
                    tables_in_pdf.append(df)

            # Generate txn_id based on transaction date and an incremental number if multiple transactions on the same date
            pdf_df = pd.concat(tables_in_pdf, ignore_index=True)
            pdf_df['txn_id'] = pdf_df['Txn Date'].apply(lambda date: pd.to_datetime(date).strftime('%Y-%m-%d')) + '_' + pdf_df.groupby('Txn Date').cumcount().astype(str).str.zfill(2)
            all_tables.append(pdf_df)
    final_df = pd.concat(all_tables, ignore_index=True)
    final_df = final_df.set_index('txn_id').sort_index()
    final_df.reset_index(inplace=True)
    return final_df

def extract_tables_from_csv(csv_files, variant=None):
    all_tables = []
    for csv_file in csv_files:
        tables_in_csv = []

        table = pd.read_csv(csv_file)
        df = eval(variant.name)().transactions(table=table)
        tables_in_csv.append(df)

        # Generate txn_id based on transaction date and an incremental number if multiple transactions on the same date
        csv_df = pd.concat(tables_in_csv, ignore_index=True)
        csv_df['txn_id'] = csv_df['Txn Date'].apply(lambda date: pd.to_datetime(date).strftime('%Y-%m-%d')) + '_' + csv_df.groupby('Txn Date').cumcount().astype(str).str.zfill(2)
        all_tables.append(csv_df)
    final_df = pd.concat(all_tables, ignore_index=True)
    final_df = final_df.set_index('txn_id').sort_index()
    final_df.reset_index(inplace=True)
    return final_df

def main():
    pdf_files, csv_files = None, None

    st.set_page_config(page_title="Transactions Converter", page_icon=":bank:")
    st.title(":bank: Transactions Converter")
    variant = "SBI"
    st.markdown("This application extracts transaction tables from **PDF files** and converts them into **CSV**.")
    with st.sidebar:
        variant = st.radio("Select the variant of PDF you want to convert.", [e.value for e in Variant])
        variant = Variant(variant)

    st.subheader("Working for :rainbow[{}] transactions".format(variant.value))
    st.write(eval(variant.name)().help)
    
    # Allow the user to upload multiple PDF files
    if variant.name == "STK":
        csv_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)
    else:
        pdf_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
    
    if pdf_files:
        # Extract tables from the PDF files
        try:
            tables_df = extract_tables_from_pdf(pdf_files, variant=variant)
            
            # Offer the option to download the sorted table as a CSV file
            st.download_button(label="Download Transactions as CSV", data=tables_df.to_csv(index=False), file_name="{}_transactions.csv".format(variant.name), mime="text/csv")
            
            # Display the sorted table
            st.write("Transactions:")
            st.dataframe(tables_df)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    
    elif csv_files:
        tables_df = extract_tables_from_csv(csv_files=csv_files, variant=variant)

        # Offer the option to download the sorted table as a CSV file
        st.download_button(label="Download Transactions as CSV", data=tables_df.to_csv(index=False), file_name="{}_transactions.csv".format(variant.name), mime="text/csv")
        
        # Display the sorted table
        st.write("Transactions:")
        st.dataframe(tables_df)


if __name__ == "__main__":
    main()
