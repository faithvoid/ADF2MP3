import os

def mp3_to_adf(input_file_path, output_file_path):
    buffer_size = 16 * 1024 * 1024  # 16 MB buffer

    try:
        with open(input_file_path, 'rb') as input_file, open(output_file_path, 'wb') as output_file:
            while True:
                buffer = input_file.read(buffer_size)
                if not buffer:
                    break
                # XOR each byte with 0x22
                encoded_buffer = bytes(b ^ 0x22 for b in buffer)
                output_file.write(encoded_buffer)
    except FileNotFoundError:
        print(f"File not found: {input_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Get the folder where the script itself is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # List all .mp3 files in that folder
    mp3_files = [f for f in os.listdir(script_dir) if f.lower().endswith('.mp3')]

    if not mp3_files:
        print("No MP3 files found in the script directory.")
        sys.exit(0)

    for mp3_file in mp3_files:
        input_path = os.path.join(script_dir, mp3_file)
        output_filename = os.path.splitext(mp3_file)[0] + '.adf'
        output_path = os.path.join(script_dir, output_filename)

        print(f"Converting {mp3_file} to {output_filename}...")
        mp3_to_adf(input_path, output_path)

    print("All conversions complete!")
