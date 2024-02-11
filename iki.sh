#!/bin/bash

# About Script stuff
echo " "
echo ".iki/.ik2 converter by Joo"
echo "thanks to timko for helping me with the windows version"
echo " "
echo "install SoX and FFmpeg with pacman"
echo "place the index and the video file on the same place as the script!!!"
echo " "
echo "Current state: Works fine, just slowly"
echo "READ THE READ_ME_TF_OUT.txt FILE BEFORE USING!"
echo " "

# Input Settings
echo "Input Settings:"
echo " "

# Ask the user to select the video file
read -p "video file (has to be the same length as the original video): " video_path

# Ask the user for the FPS value
read -p "Enter the FPS of the cutscene (7,039 for parappa cutscene, 15 for lammy): " fps_value

# Output Settings
echo " "
echo "Output Settings:"
echo " "

# Ask the user for the index file
read -p "Enter the index file: " index_file

# Ask the user for the video number
read -p "Enter the video number: " video_number
audio_id=$((video_number + 1))

# Proceed
echo " "
echo "Starting process..."
echo " "

# Create an XML header
xml_content='<?xml version="1.0"?>
<str-replace version="0.3">
'

# Convert audio to wav
ffmpeg -i "$video_path" out/out.wav

# Resize the video
ffmpeg -i "$video_path" -s 320x240 out/out.mp4

# Convert the video and extract frames
ffmpeg -i out/out.mp4 -r "$fps_value" out/%06d.png

# Convert make audio 37800hz with SOX
sox out/out.wav -r 37800 out/out1.wav

# Generate the XML content
for filename in out/*.png; do
    xml_content+="<replace frame=\"$(basename "${filename%.*}")\">$(realpath "$filename")</replace>
"
done

# Close the XML
xml_content+="</str-replace>"

echo "$xml_content" > out.xml

# Run jpsxdec to replace frames
java -jar "jpsxdec_v2.0/jpsxdec.jar" -x "$index_file" -i "$video_number" -replaceframes out.xml

# Run jpsxdec to replace audio with exact setting
java -jar "jpsxdec_v2.0/jpsxdec.jar" -x "$index_file" -i "$audio_id" -replaceaudio out/out1.wav

echo " "
echo "Process completed."
read -p "Press Enter to close the script: " TheEnd
