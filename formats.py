video_formats : list[str] = ["mp4", "mov", "avi", "mkv", "wmv", "flv", "webm", "mpeg", "mpg"]

audio_formats : list[str] = ["mp3", "wav", "flac", "aac", "ogg", "wma", "m4a", "aiff", "aif"]

image_formats : list[str] = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "webp", "heic"]

allFormats : list[list[str]] = [video_formats, audio_formats, image_formats]

def getFormats(fileName: str) -> list[str]:
    fileExt = fileName.split('.')[1]
    for formats in allFormats:
        if fileExt in formats:
            return formats
    return []
