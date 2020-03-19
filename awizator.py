import ffmpeg
from os.path import splitext
from os import remove
def get_response_file(audio_path, video_path="source.mp4"):
    video = ffmpeg.input(video_path)
    duration = float(ffmpeg.probe(video_path)['streams'][0]['duration'])
    audio = ffmpeg.input(audio_path).audio.filter('atrim', duration=duration)
    merged = ffmpeg.concat(video, audio, v=1, a=1)
    output_file = splitext(audio_path)[0]+".mkv"
    ffmpeg.output(merged, output_file).run()

    remove(audio_path)
    return output_file