import subprocess

# def extract_subtitles(video_path, language='en'):
#     command = [
#         'ffmpeg', '-i', video_path, '-map', '0:s:0', '-c:s', 'srt', '-y', f'subtitles_{language}.srt'
#         # 'ffmpeg', '-i', video_path, '-map' '0:s:0' '-c:s' 'srt' '-y' f'subtitles_{language}.srt'

#     ]
#     subprocess.run(command, check=True)
#     return f'subtitles_{language}.srt'

import subprocess
import json

def list_subtitle_streams(video_path):
    """
    List subtitle streams in the given video file using FFmpeg.

    Args:
        video_path (str): Path to the video file.

    Returns:
        list: List of subtitle language codes found in the video.
    """
    command = [
        'ffmpeg', '-i', video_path, '-hide_banner'
    ]

    try:
        # Run the command and capture output
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
        output = result.stderr  # FFmpeg outputs details to stderr

        # Debug print to see the output (can be removed later)
        print(output, '[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]')

        # Find subtitle stream information
        subtitles = []
        if output:
            for line in output.split('\n'):
                if 'Stream #' in line and 'Subtitle:' in line:
                    parts = line.split(': ')
                    if len(parts) >= 2:
                        stream_info = parts[0]  # e.g., "Stream #0:5(eng)"
                        language_code = stream_info.split('(')[-1].strip(')')  # Extract the language code

                        # Check if the subtitle is forced
                        if 'forced' not in line.lower():
                            subtitles.append(language_code)

        return subtitles

    except FileNotFoundError:
        print("Error: FFmpeg is not installed or not found in the PATH.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return []

def extract_subtitles(video_path):
    languages = list_subtitle_streams(video_path)
    extracted_files = []

    if languages:
        for language in languages:
            command = [
                'ffmpeg', 
                '-i', video_path, 
                '-map', f'0:s:{languages.index(language)}',  # Map based on index
                '-c:s', 'srt', 
                '-y', f'subtitles_{language}.srt'
            ]

            try:
                subprocess.run(command, check=True)
                extracted_files.append(f'subtitles_{language}.srt')
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while extracting subtitles for {language}: {e}")

        return extracted_files

