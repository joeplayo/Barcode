import barcode
from barcode.writer import ImageWriter
import pandas as pd
import os


def generate_barcode(data, filename):
    try:
        # Print barcode data for debugging
        print(f"Generating barcode for data: {data}")

        # Generate the barcode
        ean = barcode.get_barcode_class('ean13')
        ean_instance = ean(data, writer=ImageWriter())

        # Save the barcode
        ean_instance.save(filename)
        print(f"Generated barcode for {data}, saved as {filename}")
    except Exception as e:
        print(f"Error generating barcode for {data}: {e}")

def read_inventory_from_csv(file_path):
    try:
        # Read the CSV file using pandas
        inventory = pd.read_csv(file_path)
        print(f"Read {len(inventory)} items from CSV.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        inventory = pd.DataFrame()  # Return an empty DataFrame in case of error
    return inventory


def main():
    # Ensure the output directory exists
    output_dir = 'barcodes'
    os.makedirs(output_dir, exist_ok=True)

    # Path to the inventory CSV file
    csv_file_path = 'barcodes/inventory.csv'

    # Read inventory data from CSV file
    inventory = read_inventory_from_csv(csv_file_path)

    for index, item in inventory.iterrows():
        # Assuming the CSV has columns 'id' and 'description'
        barcode_data = str(item['id']).zfill(12)  # Ensure ID is a string and zero-padded to 12 digits
        barcode_filename = os.path.join(output_dir, f"{barcode_data}.png")

        # Check the length of barcode_data to ensure it has 12 digits for EAN-13
        if len(barcode_data) == 12 and barcode_data.isdigit():
            generate_barcode(barcode_data, barcode_filename)
        else:
            print(f"Invalid barcode data: {barcode_data}")


if __name__ == "__main__":
    main()
