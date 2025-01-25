import os
import re
import pandas as pd

def merge_txt_files_to_list(folder_path):
    """
    Merge all .txt files in the given folder into a single list of lines.

    Args:
        folder_path (str): Path to the folder containing .txt files.

    Returns:
        list: A list of all lines from the merged .txt files.
    """
    all_text = []
    
    # Loop through all files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):  # Check for .txt files
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                all_text.extend(file.readlines())  # Add lines from the file
                
    return all_text


def preprocess_text_to_csv(lines, output_csv_path):
    """
    Preprocess text lines and save them as a line-by-line CSV.

    Args:
        lines (list): A list of raw text lines.
        output_csv_path (str): Path to save the processed CSV file.
    """
    processed_lines = []
    
    for line in lines:
        # Remove excessive spaces, tabs, and newline characters
        line = line.strip()
        # Replace special artifacts like "?s" with "'s"
        line = re.sub(r'\?s', "'s", line)
        # Normalize spaces
        line = re.sub(r'\s+', ' ', line)
        
        # Append non-empty lines to the list
        if line:
            processed_lines.append(line)
    
    # Create a DataFrame and save to CSV
    df = pd.DataFrame({"text": processed_lines})
    df.to_csv(output_csv_path, index=False, encoding="utf-8")
    print(f"Processed CSV saved at: {output_csv_path}")


# Example usage
if __name__ == "__main__":
    # Path to the folder containing .txt files
    folder_path = "data"
    # Path to save the output CSV file
    output_csv_path = "data/star_wars_dataset.csv"
    
    # Step 1: Merge .txt files
    merged_lines = merge_txt_files_to_list(folder_path)
    # Step 2: Preprocess and save to CSV
    preprocess_text_to_csv(merged_lines, output_csv_path)
