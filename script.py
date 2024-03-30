import streamlit as st
import pandas as pd
import pdfplumber

from transaction_processing import Variant
from transaction_processing import epf_transactions, sbi_transactions

def extract_tables_from_pdf(pdf_files, variant=None):
    all_tables = []
    for pdf_file in pdf_files:
        with pdfplumber.open(pdf_file) as pdf:
            tables_in_pdf = []

            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    df = None
                    if variant == Variant.SBI:
                        df = sbi_transactions(table=table)
                    elif variant == Variant.EPF and page.page_number == 1:
                        df = epf_transactions(table=table)
                    tables_in_pdf.append(df)

            # Generate txn_id based on transaction date and an incremental number if multiple transactions on the same date
            pdf_df = pd.concat(tables_in_pdf, ignore_index=True)
            pdf_df['txn_id'] = pdf_df['Txn Date'].apply(lambda date: pd.to_datetime(date).strftime('%Y-%m-%d')) + '_' + pdf_df.groupby('Txn Date').cumcount().astype(str).str.zfill(2)
            all_tables.append(pdf_df)
    final_df = pd.concat(all_tables, ignore_index=True)
    final_df = final_df.set_index('txn_id').sort_index()
    final_df.reset_index(inplace=True)
    return final_df

def main():
    st.set_page_config(page_title="Transactions Converter", page_icon=":bank:")
    st.title(":bank: Transactions Converter")
    variant = "SBI Txns"
    st.markdown("This application extracts transaction tables from **PDF files** and converts them into **CSV**.")
    with st.sidebar:
        variant = st.radio("Select the variant of PDF you want to convert.", [e.value for e in Variant])
        variant = Variant(variant)

    st.subheader("Working for :rainbow[{}] transactions".format(variant.value))
    
    # Allow the user to upload multiple PDF files
    pdf_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
    
    if pdf_files:
        # Extract tables from the PDF files
        try:
            tables_df = extract_tables_from_pdf(pdf_files, variant=variant)
            
            # Offer the option to download the sorted table as a CSV file
            st.download_button(label="Download Transactions as CSV", data=tables_df.to_csv(index=False), file_name="transactions.csv", mime="text/csv")
            
            # Display the sorted table
            st.write("Transactions:")
            st.dataframe(tables_df)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
