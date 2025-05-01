import os
import sys
import subprocess

def process_file(input_file_path, output_file_path, mode):
    buffer_size = 16 * 1024 * 1024  # 16 MB buffer

    try:
        with open(input_file_path, 'rb') as input_file, open(output_file_path, 'wb') as output_file:
            while True:
                buffer = input_file.read(buffer_size)
                if not buffer:
                    break
                # XOR each byte with 0x22
                processed_buffer = bytes(b ^ 0x22 for b in buffer)
                output_file.write(processed_buffer)
    except FileNotFoundError:
        print(f"File not found: {input_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_adf_to_wma(input_file_path, output_file_path):
    try:
        # Decode the ADF file to MP3
        temp_mp3_file = os.path.splitext(input_file_path)[0] + '_temp.mp3'
        process_file(input_file_path, temp_mp3_file, mode="adf_to_mp3")

        # Use FFMPEG to convert MP3 to Xbox-compatible WMA with specified settings
        ffmpeg_command = [
            "ffmpeg", 
            "-i", temp_mp3_file, 
            "-c:a", "wmav2", 
            "-b:a", "128k", 
            "-ac", "2", 
            "-ar", "44100", 
            output_file_path
        ]
        subprocess.run(ffmpeg_command, check=True)

        # Remove the temporary MP3 file
        os.remove(temp_mp3_file)

        print(f"Conversion to WMA complete: {output_file_path}")
    except FileNotFoundError:
        print("FFMPEG not found. Please install FFMPEG to use this feature.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while converting to WMA: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_adf_to_wav(input_file_path, output_file_path):
    try:
        # Decode the ADF file to MP3
        temp_mp3_file = os.path.splitext(input_file_path)[0] + '_temp.mp3'
        process_file(input_file_path, temp_mp3_file, mode="adf_to_mp3")

        # Use FFMPEG to convert MP3 to PC-compatible WAV
        ffmpeg_command = [
            "ffmpeg",
            "-i", temp_mp3_file,
            "-c:a", "adpcm_ima_wav",  # ADPCM IMA WAV codec
            "-ar", "32000",           # 32 kHz sample rate
            "-ac", "2",               # Stereo
            output_file_path
        ]
        subprocess.run(ffmpeg_command, check=True)

        # Remove the temporary MP3 file
        os.remove(temp_mp3_file)

        print(f"Conversion to GTA III-compatible WAV complete: {output_file_path}")
    except FileNotFoundError:
        print("FFMPEG not found. Please install FFMPEG to use this feature.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while converting to WAV: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def prompt_user_choice():
    print("\nWhat action would you like to perform?")
    print("1. Convert ADF files to MP3")
    print("2. Convert MP3 files to ADF")
    print("3. Convert ADF files to WMA (Xbox)")
    print("4. Convert ADF files to WAV (PC)")
    print("5. Exit")
    choice = input("Enter the number corresponding to your choice: ").strip()
    return choice

if __name__ == "__main__":
    # Get the folder where the script itself is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        user_choice = prompt_user_choice()

        if user_choice == "1":
            # List all .adf files in the folder
            adf_files = [f for f in os.listdir(script_dir) if f.lower().endswith('.adf')]

            if not adf_files:
                print("No ADF files found in the script directory.")
                continue

            for adf_file in adf_files:
                input_path = os.path.join(script_dir, adf_file)
                output_filename = os.path.splitext(adf_file)[0] + '.mp3'
                output_path = os.path.join(script_dir, output_filename)

                print(f"Converting {adf_file} to {output_filename}...")
                process_file(input_path, output_path, mode="adf_to_mp3")

            print("ADF to MP3 conversions complete!")

        elif user_choice == "2":
            # List all .mp3 files in the folder
            mp3_files = [f for f in os.listdir(script_dir) if f.lower().endswith('.mp3')]

            if not mp3_files:
                print("No MP3 files found in the script directory.")
                continue

            for mp3_file in mp3_files:
                input_path = os.path.join(script_dir, mp3_file)
                output_filename = os.path.splitext(mp3_file)[0] + '.adf'
                output_path = os.path.join(script_dir, output_filename)

                print(f"Converting {mp3_file} to {output_filename}...")
                process_file(input_path, output_path, mode="mp3_to_adf")

            print("MP3 to ADF conversions complete!")

        elif user_choice == "3":
            # List all .adf files in the folder
            adf_files = [f for f in os.listdir(script_dir) if f.lower().endswith('.adf')]

            if not adf_files:
                print("No ADF files found in the script directory.")
                continue

            for adf_file in adf_files:
                input_path = os.path.join(script_dir, adf_file)
                output_filename = os.path.splitext(adf_file)[0] + '.wma'
                output_path = os.path.join(script_dir, output_filename)

                print(f"Converting {adf_file} to {output_filename} using FFMPEG...")
                convert_adf_to_wma(input_path, output_path)

            print("ADF to WMA (Xbox) conversions complete!")

        elif user_choice == "4":
            # List all .adf files in the folder
            adf_files = [f for f in os.listdir(script_dir) if f.lower().endswith('.adf')]

            if not adf_files:
                print("No ADF files found in the script directory.")
                continue

            for adf_file in adf_files:
                input_path = os.path.join(script_dir, adf_file)
                output_filename = os.path.splitext(adf_file)[0] + '.wav'
                output_path = os.path.join(script_dir, output_filename)

                print(f"Converting {adf_file} to {output_filename} using FFMPEG...")
                convert_adf_to_wav(input_path, output_path)

            print("ADF to WAV (PC) conversions complete!")

        elif user_choice == "5":
            sys.exit(0)

        else:
            print("Invalid choice. Please try again.")
