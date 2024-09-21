from django.shortcuts import render, redirect, get_object_or_404
from .models import Video, Subtitle
from .utils import extract_subtitles
import re, json
from datetime import datetime
import time
import os


def clear_content(sub_list, video):
    for data in sub_list:
        for language, content in data.items():
            # Regular expression to match SRT subtitle pattern
            srt_pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\d+\n|\Z)', re.DOTALL)

            # Regular expression to remove both HTML-like tags and SSA/ASS-style tags (e.g., <font> and {\an8})
            tag_removal_pattern = re.compile(r'<.*?>|{.*?}')

            # Helper function to convert subtitle time format to datetime.time
            parsed_subtitles = {}
            for match in srt_pattern.findall(content):
                index = int(match[0])
                start_time = match[1]
                end_time = match[2]
                text = match[3].replace('\n', ' ')  # Replace line breaks in the text with spaces

                # Remove formatting tags (HTML-like and SSA/ASS tags)
                clean_text = tag_removal_pattern.sub('', text)

                if language not in parsed_subtitles:
                    parsed_subtitles[language] = []  # Initialize a list for this language

                parsed_subtitles[language].append({
                    'index': index,
                    'start_time': start_time,
                    'end_time': end_time,
                    'text': clean_text.strip()
                })

            # Helper function to convert subtitle time format to datetime.time
            def convert_to_time(sub_time_str):
                return datetime.strptime(sub_time_str, '%H:%M:%S,%f').time()
            
            
            subtitle_instances = []
            # Loop through parsed subtitles and save each one
            for language, parsed_content in parsed_subtitles.items():
                    # Initialize a list to collect all timestamps and texts
                all_timestamps = []
                all_texts = []
                for parsed_data in parsed_content:
                    start_time = convert_to_time(parsed_data['start_time'])
                    end_time = convert_to_time(parsed_data['end_time'])
                
                    # Concatenate start and end time for timestamp
                    timestamp = f"{start_time} --> {end_time}"
                    # Create a new Subtitle instance and append to the list
                    subtitle_instances.append(Subtitle(
                        video=video,
                        language=language,  # Use the current language
                        content=parsed_data['text'],  # Save individual text
                        timestamp=timestamp  # Save individual timestamp
                    ))

            # Use bulk_create to save all instances in one go
            Subtitle.objects.bulk_create(subtitle_instances)

    return "done"

def upload_video(request):
    if request.method == 'POST' and request.FILES['video']:
        video = Video.objects.create(file=request.FILES['video'])
        video_path = video.file.path
        
        # Extract subtitles
        extracted_files = extract_subtitles(video_path)
        sub_list = []
        if extracted_files:
            for subtitles_path in extracted_files:
                try:
                    with open(subtitles_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        language = subtitles_path.split('_')[1].split('.')[0]
                        sub_list.append({language: content})                    
                except FileNotFoundError:
                    print(f"File not found: {subtitles_path}")
            final_content = clear_content(sub_list, video)
            return redirect('video_list')
    return render(request, 'upload.html')

def video_list(request):    
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})

def video_detail(request, video_id):
    video = Video.objects.get(id=video_id)
    subtitles = video.subtitles.filter(language='eng')
    all_subs = video.subtitles.all()
    all_lang = []
    for i in all_subs:
        if i.language not in all_lang:
            all_lang.append(i.language)

    return render(request, 'video_detail.html', {'video': video, 'subtitles': subtitles, 'all_languages': all_lang})

def delete_video(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(Video, pk=video_id)
        
        # Construct the file path based on the video file field
        video_file_path = video.file.path  # Assuming 'file' is the field name for the video

        # Delete the video record from the database
        video.delete()

        # Check if the file exists and delete it
        if os.path.exists(video_file_path):
            os.remove(video_file_path)
        
        return redirect('video_list')  
    else:
        return redirect('video_list')  # Redirect if not a POST request

def search_subtitle(request, video_id):
    query = request.GET.get('language', '').lower()
    video = Video.objects.get(id=video_id)
    subtitles = video.subtitles.filter(language=query)
    all_subs = video.subtitles.all()
    all_lang = []
    for i in all_subs:
        if i.language not in all_lang:
            all_lang.append(i.language)
    return render(request, 'video_detail.html', {'video': video, 'subtitles': subtitles,  'all_languages': all_lang})