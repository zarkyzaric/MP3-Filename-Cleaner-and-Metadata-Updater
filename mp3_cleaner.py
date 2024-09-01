import os
import re
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, ID3NoHeaderError

# Define the current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# Compile regex patterns for reuse
trash_patterns = [
    # General clean-up patterns
    re.compile(r'\s*-\s*Youtube', re.IGNORECASE),  # Removes ' - Youtube'
    re.compile(r'\s*\(Official\sVideo\)', re.IGNORECASE),  # Removes '(Official Video)'
    re.compile(r'\s*\(Official\sMusic\sVideo\)', re.IGNORECASE),  # Removes '(Official Music Video)'
    re.compile(r'\s*\(Official\sAudio\)', re.IGNORECASE),  # Removes '(Official Audio)'
    re.compile(r'\s*\(HD\)', re.IGNORECASE),  # Removes '(HD)'
    re.compile(r'\s*\(4K\)', re.IGNORECASE),  # Removes '(4K)'
    re.compile(r'\s*\(Official\sChannel\)', re.IGNORECASE),  # Removes '(Official Channel)'
    re.compile(r'\s*-\s*Audio\s\d*\s*\.*$', re.IGNORECASE),  # Removes ' - Audio 320kbps'
    re.compile(r'\s*\(\d{3,4}p\)', re.IGNORECASE),  # Removes resolutions like '(720p)', '(1080p)'
    re.compile(r'\s*\(\d+\skbps\)', re.IGNORECASE),  # Removes '(320 kbps)', '(128 kbps)'
    re.compile(r'\s*Official\s', re.IGNORECASE),  # Removes 'Official' on its own
    re.compile(r'\s*Full\sSong', re.IGNORECASE),  # Removes 'Full Song'
    re.compile(r'\s*\bHQ\b', re.IGNORECASE),  # Removes 'HQ' (High Quality)
    re.compile(r'\s*\bLYRICS?\b', re.IGNORECASE),  # Removes 'LYRICS' or 'LYRIC'
    re.compile(r'\s*\bAUDIO\b', re.IGNORECASE),  # Removes 'AUDIO'
    re.compile(r'\s*\bVIDEO\b', re.IGNORECASE),  # Removes 'VIDEO'
    re.compile(r'\s*\bALBUM\b', re.IGNORECASE),  # Removes 'ALBUM'
    re.compile(r'\s*\bTRACK\b', re.IGNORECASE),  # Removes 'TRACK'
    re.compile(r'\s*\bPROMO\b', re.IGNORECASE),  # Removes 'PROMO'
    re.compile(r'\s*\bDEMO\b', re.IGNORECASE),  # Removes 'DEMO'
    re.compile(r'\s*\bOUTRO\b', re.IGNORECASE),  # Removes 'OUTRO'
    re.compile(r'\s*\bINTRO\b', re.IGNORECASE),  # Removes 'INTRO'
    re.compile(r'\s*\bCLIP\b', re.IGNORECASE),  # Removes 'CLIP'
    re.compile(r'\s*\bEDIT\b', re.IGNORECASE),  # Removes 'EDIT'
    re.compile(r'\s*\bCOVER\b', re.IGNORECASE),  # Removes 'COVER'
    re.compile(r'\s*\(.*PART.*\)', re.IGNORECASE),  # Removes 'PART'
    re.compile(r'\s*\-\sBassivity\sDigital.*', re.IGNORECASE),  # Removes 'Bassivity Digital'
    re.compile(r'\s*#.*\s', re.IGNORECASE),  # Removes hashtags
    
    re.compile(r'\s*Remastered\s\d{4}', re.IGNORECASE),  # Removes 'Remastered YYYY'
    re.compile(r'\s*\(\s*\)', re.IGNORECASE),  # Removes empty brackets '()'
    
    # Leading/trailing spaces and hyphens
    re.compile(r'^\s+', re.IGNORECASE),  # Removes leading spaces
    re.compile(r'\s+$', re.IGNORECASE),  # Removes trailing spaces
    re.compile(r'^\s*-\s*', re.IGNORECASE),  # Removes leading hyphens
    re.compile(r'\s*-\s*$', re.IGNORECASE),  # Removes trailing hyphens

    # Specific website patterns
    re.compile(r'\[SPOTIFY-DOWNLOADER\.COM\]', re.IGNORECASE),  # Removes '[SPOTIFY-DOWNLOADER.COM]'
    re.compile(r'\(Snap2s\.com\)', re.IGNORECASE),  # Removes '(Snap2s.com)'
    re.compile(r'\sProd\.\sby\sJhinsen', re.IGNORECASE),  # Removes 'Prod. by Jhinsen'
    re.compile(r'\bfree\sdownload\b', re.IGNORECASE),  # Removes 'free download'
    re.compile(r'\s*from\s*YouTube\s*', re.IGNORECASE),  # Removes 'from YouTube'
    re.compile(r'\s*downloaded\sfrom\sYouTube', re.IGNORECASE),  # Removes 'downloaded from YouTube'
]

def clean_filenames(start_directory, trash_patterns):
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

            # Ensure the filename ends with '.mp3'
            if not cleaned_filename.lower().endswith('.mp3'):
                cleaned_filename += '.mp3'

            # If the filename has changed, rename the file
            if cleaned_filename != original_filename:
                original_filepath = os.path.join(current_dir, original_filename)
                cleaned_filepath = os.path.join(current_dir, cleaned_filename)
                os.rename(original_filepath, cleaned_filepath)
                print(f'Renamed: "{original_filename}" to "{cleaned_filename}"')

def update_mp3_metadata(filepath):
    try:
        filename = os.path.basename(filepath)
        base_name = os.path.splitext(filename)[0]

        if " - " in base_name:
            artist_song, song_name = base_name.split(" - ", 1)
        else:
            artist_song = None
            song_name = base_name

        try:
            audio = EasyID3(filepath)
        except ID3NoHeaderError:
            audio = EasyID3()
            audio.add_tags()

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
    clean_filenames(current_directory, trash_patterns)

    for root, dirs, files in os.walk(current_directory):
        for file in files:
            if file.endswith('.mp3'):
                filepath = os.path.join(root, file)
                update_mp3_metadata(filepath)

if __name__ == "__main__":
    main()
