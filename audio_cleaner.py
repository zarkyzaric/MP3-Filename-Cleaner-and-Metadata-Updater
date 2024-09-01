import os
import re
from mutagen.easyid3 import EasyID3
from mutagen import File
from mutagen.id3 import ID3NoHeaderError

# Define the current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# Supported audio file extensions
supported_extensions = ['.mp3', '.flac', '.wav', '.m4a', '.aac', '.ogg', '.wma']

# Compile regex patterns for reuse
trash_patterns = [
    # General clean-up patterns
    re.compile(r'\s*-\s*Youtube', re.IGNORECASE),
    re.compile(r'\s*\(Official\sVideo\)', re.IGNORECASE),
    re.compile(r'\s*\(Official\sMusic\sVideo\)', re.IGNORECASE),
    re.compile(r'\s*\(Official\sAudio\)', re.IGNORECASE),
    re.compile(r'\s*\(HD\)', re.IGNORECASE),
    re.compile(r'\s*\(4K\)', re.IGNORECASE),
    re.compile(r'\s*\(Official\sChannel\)', re.IGNORECASE),
    re.compile(r'\s*-\s*Audio\s\d*\s*\.*$', re.IGNORECASE),
    re.compile(r'\s*\(\d{3,4}p\)', re.IGNORECASE),
    re.compile(r'\s*\(\d+\skbps\)', re.IGNORECASE),
    re.compile(r'\s*Official\s', re.IGNORECASE),
    re.compile(r'\s*Full\sSong', re.IGNORECASE),
    re.compile(r'\s*\bHQ\b', re.IGNORECASE),
    re.compile(r'\s*\bLYRICS?\b', re.IGNORECASE),
    re.compile(r'\s*\bAUDIO\b', re.IGNORECASE),
    re.compile(r'\s*\bVIDEO\b', re.IGNORECASE),
    re.compile(r'\s*\bALBUM\b', re.IGNORECASE),
    re.compile(r'\s*\bTRACK\b', re.IGNORECASE),
    re.compile(r'\s*\bPROMO\b', re.IGNORECASE),
    re.compile(r'\s*\bDEMO\b', re.IGNORECASE),
    re.compile(r'\s*\bOUTRO\b', re.IGNORECASE),
    re.compile(r'\s*\bINTRO\b', re.IGNORECASE),
    re.compile(r'\s*\bCLIP\b', re.IGNORECASE),
    re.compile(r'\s*\bEDIT\b', re.IGNORECASE),
    re.compile(r'\s*\bCOVER\b', re.IGNORECASE),
    re.compile(r'\s*\(.*PART.*\)', re.IGNORECASE),
    re.compile(r'\s*\-\sBassivity\sDigital.*', re.IGNORECASE),
    re.compile(r'\s*#.*\s', re.IGNORECASE),
    
    re.compile(r'\s*Remastered\s\d{4}', re.IGNORECASE),
    re.compile(r'\s*\(\s*\)', re.IGNORECASE),
    
    # Leading/trailing spaces and hyphens
    re.compile(r'^\s+', re.IGNORECASE),
    re.compile(r'\s+$', re.IGNORECASE),
    re.compile(r'^\s*-\s*', re.IGNORECASE),
    re.compile(r'\s*-\s*$', re.IGNORECASE),

    # Specific website patterns
    re.compile(r'\[SPOTIFY-DOWNLOADER\.COM\]', re.IGNORECASE),
    re.compile(r'\(Snap2s\.com\)', re.IGNORECASE),
    re.compile(r'\sProd\.\sby\sJhinsen', re.IGNORECASE),
    re.compile(r'\bfree\sdownload\b', re.IGNORECASE),
    re.compile(r'\s*from\s*YouTube\s*', re.IGNORECASE),
    re.compile(r'\s*downloaded\sfrom\sYouTube', re.IGNORECASE),
]

def clean_filenames(start_directory, trash_patterns, extensions):
    for current_dir, dirnames, filenames in os.walk(start_directory):
        for filename in filenames:
            original_filename = filename
            cleaned_filename = filename

            # Split the filename into parts and keep only the first two if there are more
            parts = cleaned_filename.rsplit(' - ', 2)
            if len(parts) > 2:
                cleaned_filename = ' - '.join(parts[:-1])

            # Apply all trash patterns to the filename
            for pattern in trash_patterns:
                cleaned_filename = pattern.sub('', cleaned_filename)

            # Remove extra spaces and trailing hyphens
            cleaned_filename = re.sub(r'\s+', ' ', cleaned_filename).strip()
            cleaned_filename = re.sub(r'\s*-\s*$', '', cleaned_filename)

            # Ensure the filename has the correct extension
            ext = os.path.splitext(original_filename)[1].lower()
            if ext in extensions and not cleaned_filename.lower().endswith(ext):
                cleaned_filename += ext

            # If the filename has changed, rename the file
            if cleaned_filename != original_filename:
                original_filepath = os.path.join(current_dir, original_filename)
                cleaned_filepath = os.path.join(current_dir, cleaned_filename)
                os.rename(original_filepath, cleaned_filepath)
                print(f'Renamed: "{original_filename}" to "{cleaned_filename}"')

def update_metadata(filepath, extensions):
    try:
        ext = os.path.splitext(filepath)[1].lower()
        filename = os.path.basename(filepath)
        base_name = os.path.splitext(filename)[0]

        if ext == '.mp3':
            audio = EasyID3(filepath)
        else:
            audio = File(filepath, easy=True)
            if audio is None:
                raise Exception(f"Unsupported file type: {ext}")

        if " - " in base_name:
            artist_song, song_name = base_name.split(" - ", 1)
        else:
            artist_song = None
            song_name = base_name

        # Only update the title if it's different from the filename
        if audio.get('title', [None])[0] != base_name.strip():
            audio['title'] = song_name.strip()

        # Only update the artist if the title and filename are not the same
        if artist_song and audio.get('title', [None])[0] != base_name.strip():
            audio['artist'] = artist_song.strip()

        audio.save()
        print(f"Updated metadata for {filepath}")

    except FileNotFoundError:
        print(f"File not found: {filepath} (errno 2)")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    clean_filenames(current_directory, trash_patterns, supported_extensions)

    for root, dirs, files in os.walk(current_directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in supported_extensions:
                filepath = os.path.join(root, file)
                update_metadata(filepath, supported_extensions)

if __name__ == "__main__":
    main()
