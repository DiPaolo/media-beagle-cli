# from subprocess import Popen, PIPE, STDOUT, check_output, CalledProcessError
import os
import subprocess
import json


def print_ffmpeg_version():
    output = subprocess.run(["ffprobe", "-version"], capture_output=True)
    print(output.stdout.decode('utf-8'))


def analyze_file(filename: str, level: int):
    print('  ' * level + f'{filename}')

    output = subprocess.run(["ffprobe", filename, '-show_format', '-show_streams', '-print_format', 'json', '-loglevel', '0'], capture_output=True)

    # print(output.stderr.decode('utf-8'))
    # print(output.stdout.decode('utf-8'))

    try:
        info = json.loads(output.stdout.decode('utf-8'))
    except:
        # print('  ' * (level + 1) + 'Not a media file')
        return

    if 'streams' not in info.keys():
        # print('  ' * (level + 1) + 'Not a media file')
        return

    for stream in info['streams']:
        codec_info = ''

        if 'codec_type' in stream.keys():
            if stream['codec_type'] == 'video':
                codec_info = '{0}x{1}'.format(stream['width'], stream['height'])
            elif stream['codec_type'] == 'audio':
                codec_info = stream['channel_layout'] if 'channel_layout' in stream else '-'

        print('  ' * (level + 1) + '{0}: {1}'.format(stream['codec_name'] if 'codec_name' in stream.keys() else 'unknown stream type', codec_info))


def analyze_dir(path: str, level: int = 0):
    print('  ' * level + f'{path}')
    with os.scandir(path) as entries:
        for entry in entries:
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                analyze_dir(full_path, level + 1)
            elif os.path.isfile(full_path):
                analyze_file(full_path, level + 1)
            # else:
            #     print('  ' * (level + 1) + f"ERROR what is '{full_path}'?")
