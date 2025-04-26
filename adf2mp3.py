import os

def adf_to_mp3(input_file_path, output_file_path):
    buffer_size = 16 * 1024 * 1024  # 16 MB buffer

    try:
        with open(input_file_path, 'rb') as input_file, open(output_file_path, 'wb') as output_file:
            while True:
                buffer = input_file.read(buffer_size)
                if not buffer:
                    break
                # XOR each byte with 0x22
                decoded_buffer = bytes(b ^ 0x22 for b in buffer)
                output_file.write(decoded_buffer)
    except FileNotFoundError:
        print(f"File not found: {input_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Get the folder where the script itself is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # List all .adf files in that folder
    adf_files = [f for f in os.listdir(script_dir) if f.lower().endswith('.adf')]

    if not adf_files:
        print("No ADF files found in the script directory.")
        sys.exit(0)

    for adf_file in adf_files:
        input_path = os.path.join(script_dir, adf_file)
        output_filename = os.path.splitext(adf_file)[0] + '.mp3'
        output_path = os.path.join(script_dir, output_filename)

        print(f"Converting {adf_file} to {output_filename}...")
        adf_to_mp3(input_path, output_path)

    print("All conversions complete!")
