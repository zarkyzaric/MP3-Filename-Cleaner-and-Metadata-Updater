# MP3 Filename Cleaner and Metadata Updater

This script is designed to clean up MP3 filenames by removing unwanted patterns and ensures that the metadata tags (such as title and artist) are properly updated based on the cleaned filenames. It helps organize and standardize your MP3 files for better readability and compatibility with media players.

## Features

- Removes unwanted patterns from Audio filenames (e.g., " - YouTube", "Official Video", etc.).https://github.com/zarkyzaric/MP3-Filename-Cleaner-and-Metadata-Updater/blob/main/README.md
- Cleans up extra spaces, trailing hyphens, and other common "trash" elements in filenames.
- Removes everything after the second hyphen in filenames (e.g., "Artist - Song - Extra Info.mp3" becomes "Artist - Song.mp3").
- Ensures that filenames always retain the `.mp3` extension.
- Updates the MP3 metadata tags (`title`, `artist`) based on the cleaned filename.

## Requirements

- Python 3.x
- `mutagen` library for handling MP3 metadata

You can install the required dependencies using:

```bash
pip install mutagen
```

## Usage

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/mp3-cleaner.git
   cd mp3-cleaner
   ```

2. **Place Your MP3 Files:**

   Place the MP3 files you want to clean in the same directory as the script. Alternatively, modify the script to point to a different directory by changing the `current_directory` variable.

3. **Run the Script:**

   Run the script using Python:

   ```bash
   python mp3_cleaner.py
   ```

   The script will:
   - Iterate over all MP3 files in the directory.
   - Clean the filenames based on predefined patterns.
   - Ensure that the filename ends with `.mp3`.
   - Update the MP3 metadata tags (`title`, `artist`) based on the cleaned filename.

4. **Review the Changes:**

   The script prints out each filename that it renames, allowing you to review the changes directly in the terminal. For example:

   ```
   Renamed: "Artist - Song - Extra Info.mp3" to "Artist - Song.mp3"
   ```

## Example

Given a directory containing the following files:

```
Artist - Song Title (Official Video) - YouTube.mp3
Another Artist - Another Song (HD) - Audio 320kbps.mp3
Artist - Song Title.mp3
```

After running the script, the files will be renamed to:

```
Artist - Song Title.mp3
Another Artist - Another Song.mp3
Artist - Song Title.mp3
```

Additionally, the MP3 metadata will be updated to reflect the cleaned filenames.

## Customization

The script uses a list of regex patterns to identify and remove unwanted parts of filenames. You can customize the `trash_patterns` list in the script to add or remove patterns according to your needs.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue to suggest improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This `README.md` provides a comprehensive guide for users to understand how to set up, use, and potentially contribute to your script. You can modify the sections to better fit your specific needs and repository structure.
