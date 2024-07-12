import streamlit as st
import pandas as pd
import csv
import time


def read_file(file):
    if file.name.endswith('.xlsx'):
        return read_excel(file)
    elif file.name.endswith('.csv'):
        return read_csv(file)
    else:
        raise ValueError("Unsupported file type. Please provide a .xlsx or .csv file.")


def check_number(codes, numbers):
    final_numbers = set()
    total_numbers = len(numbers)
    progress_bar = st.progress(0)

    for i, number in enumerate(numbers):
        for code in codes:
            if str(number).startswith(str(code)):
                final_numbers.add(number)
                break
        progress_bar.progress((i + 1) / total_numbers)

    return final_numbers


def read_excel(file):
    df = pd.read_excel(file)
    return df.values.flatten().tolist()


def read_csv(file):
    df = pd.read_csv(file)
    return df.values.flatten().tolist()


def save_to_csv(final_numbers):
    try:
        with open('scrubbed_final_numbers.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([[item] for item in final_numbers])

        return 'scrubbed_final_numbers.csv'
    except Exception as e:
        st.error(f"Error while saving to CSV: {e}")


def main_area():
    st.title("Area Code Scrubber By zainalialvi")

    code_file = st.file_uploader("Upload Area Codes File", type=['xlsx', 'csv'], key='code_file')
    number_file = st.file_uploader("Upload Phone Numbers File", type=['xlsx', 'csv'], key='number_file')

    if code_file and number_file:
        codes = read_file(code_file)
        phone_numbers = read_file(number_file)

        st.write("-" * 30)
        st.write(" Total Area Codes: ", len(codes))
        st.write("Total Raw Numbers: ", len(phone_numbers))
        st.write("-" * 30)

        if st.button("Process Numbers"):
            final_nums = check_number(codes, phone_numbers)

            st.write("=" * 30)
            st.write("    Total Final Numbers: ", len(final_nums))
            st.write("Total Not Final Numbers: ", len(phone_numbers) - len(final_nums))
            st.write("=" * 30)

            csv_file = save_to_csv(final_nums)

            if csv_file:
                with open(csv_file, 'rb') as f:
                    st.download_button(
                        label="Download Scrubbed Numbers",
                        data=f,
                        file_name=csv_file,
                        mime='text/csv',
                    )


if __name__ == '__main__':
    main_area()
