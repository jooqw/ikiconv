import os
import sys
import subprocess

def main():
    # About Script stuff
    print(".iki/.ik2 converter by Joo")
    print("Slightly modified by Timkho")
    print("Current state: Works fine, just slowly")
    print(" ")
    print("READ THE READ_ME_TF_OUT.txt FILE BEFORE USING!")
    print(" ")
    
    # Input Settings
    print("Input Settings:")
    print(" ")
   
    # Ask the user to select the video file
    video_path = input("Enter the path to the video file(has to be the same lenght as the original video): ")

    # Ask the user for the FPS value
    fps_value = input("Enter the FPS of the cutscene (7,039 for parappa cutscene,15 for lammy): ")
    
    # Output Settings
    print(" ")
    print("Output Settings:")
    print(" ")

    # Ask the user for the path to jpsxdec
    jpsxdec_path = input("Enter the path to the directory containing jpsxdec: ")

    # Ask the user for the index file
    index_file = input("Enter the index file: ")

    # Ask the user for the video number
    video_number = input("Enter the video number: ")
    audio_id = str(int(video_number) + 1)

    # Proceed
    print(" ")
    print("Starting process...")
    print(" ")
    
    # Create an XML header
    xml_content = '<?xml version="1.0"?>\n<str-replace version="0.3">\n'

    #convert audio to wav
    ffmpeg_audio = ['ffmpeg.exe', '-i', video_path, 'out/out.wav']
    subprocess.run(ffmpeg_audio, shell=True)

    #convert make audio 37800hz with SOX
    sox_audio = ['sox.exe', 'out/out.wav', '-r', '37800', 'out/out1.wav']
    subprocess.run(sox_audio, shell=True)
    
    #Resize the vid 
    ffmpeg_resize = ['ffmpeg.exe', '-i', video_path, '-s', '320x240', 'out/out.mp4']
    subprocess.run(ffmpeg_resize, shell=True)

    # Convert the video and extract frames
    ffmpeg_command = ['ffmpeg.exe', '-i', 'out/out.mp4', '-r', fps_value, 'out/%06d.png']
    subprocess.run(ffmpeg_command, shell=True)

    # Generate the XML content
    for filename in os.listdir('out'):
        if filename.endswith('.png'):
            xml_content += f'<replace frame="{os.path.splitext(filename)[0]}">{os.path.abspath(os.path.join("out", filename))}</replace>\n'

    # Close the XML
    xml_content += '</str-replace>'

    with open('out.xml', 'w') as xml_file:
        xml_file.write(xml_content)

    # Run jpsxdec to replace frames
    jpsxdec_replace_command = [
        'java', '-jar', os.path.join(jpsxdec_path, 'jpsxdec.jar'),
        '-x', index_file, '-i', video_number,
        '-replaceframes', 'out.xml'
    ]
    subprocess.run(jpsxdec_replace_command, shell=True)

    # Run jpsxdec to replace audio with exact setting
    jpsxdec_audio_replace_command = [
        'java', '-jar', os.path.join(jpsxdec_path, 'jpsxdec.jar'),
        '-x', index_file, '-i', audio_id,
        '-replaceaudio', 'out/out1.wav'
    ]
    subprocess.run(jpsxdec_audio_replace_command, shell=True)

    print(" ")
    print("Process completed.")
    TheEnd = input("Press any key to close the script: ")

if __name__ == "__main__":
    main()
