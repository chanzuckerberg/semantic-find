import os
import sys
import pdftotext

# Ensure the user provides the directory with PDF files as an argument
if len(sys.argv) < 2:
    print("Usage: python script_name.py <pdf_directory>")
    sys.exit(1)

# Get the directory with PDFs from the command line argument
pdf_dir = sys.argv[1]

# Ensure the provided path is a directory
if not os.path.isdir(pdf_dir):
    print(f"{pdf_dir} is not a valid directory")
    sys.exit(1)

# Set up the output directory (assuming the script is in the src folder and we want data at the same level)
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(os.path.dirname(script_dir), 'data')

# Create the output directory if it doesn't exist
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Iterate over all the PDF files in the provided directory
for file in os.listdir(pdf_dir):
    if not file.endswith(".pdf"):
        continue

    pdf_path = os.path.join(pdf_dir, file)
    print(f"Converting {pdf_path} to text")

    with open(pdf_path, "rb") as f:
      pdf = pdftotext.PDF(f)

    output_text_file = os.path.join(data_dir, f"{os.path.splitext(file)[0]}.txt")
    with open(output_text_file, 'w') as f_out:
      for page in pdf:
        f_out.write(f"{page}\n")

    print(f"Finished processing {file}, output saved to {output_text_file}")
