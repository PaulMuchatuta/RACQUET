import pandas as pd #need to install pandas library for ease. Note had to pip install openpyxl too
import csv
from docx import Document #need to install docx library for ease
import sys
import os

def excel_to_csv(input_file, output_file):
    try:
        df = pd.read_excel(input_file, header=None)     #Read Excel file at this file path. df=dataframe, which is essentially a table in pandas library
        single_column_data = df.astype(str).apply(lambda x: ' '.join(x), axis=1) # Converts excel data into string (str) and joins them into a single column (axis=1)    
        single_column_data.to_csv(output_file, index=False, header=False, quoting=csv.QUOTE_ALL)    #Save as CSV
        print(f"Flag 1: successfulconversion of {input_file} to {output_file}")
    except Exception as e:
        print(f"Flag 2: Error converting excel file {input_file} to CSV: {e}")

def word_to_csv(input_file, output_file):
    try:
        doc = Document(input_file, header=None)     # Read Word file    
        text = []     # Extract text
        for paragraph in doc.paragraphs: 
            text.append(paragraph.text) #forloop to append text into the one single column
        with open(output_file, mode='w', newline='') as file:     # Save as CSV
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            for line in text:
                writer.writerow([line])
        print(f"Flag 3: successful conversion of {input_file} to {output_file}")
    except Exception as e:
        print(f"Flag 4: Error converting word file {input_file} to CSV: {e}")        

def convert_file(input_file, output_file):
    if input_file.endswith('.xlsx'):
        excel_to_csv(input_file, output_file)
    elif input_file.endswith('.docx'):
        word_to_csv(input_file, output_file)
    else:
        print("Unsupported file format. Please provide an .xlsx or .docx file.")
        sys.exit(1)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Convert Excel or Word file to CSV with one column.')
    parser.add_argument('input_file', help='Path to the input Excel or Word file')
    parser.add_argument('output_file', help='Path to the output CSV file')

    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(f"Error: The file {args.input_file} does not exist.")
        sys.exit(1)    

    convert_file(args.input_file, args.output_file)
