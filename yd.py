import os
import subprocess


def get_video_resolutions(url):
    try:
        # Command to get video information
        command = ["yt-dlp", "-F", url]
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Extract available formats from the output
        formats = []
        for line in result.stdout.splitlines():
            if line.startswith(" "):
                parts = line.split()
                if len(parts) > 3:
                    format_id = parts[0]
                    resolution = parts[2]
                    formats.append((format_id, resolution))
        return formats

    except subprocess.CalledProcessError as e:
        print(f"Error fetching video resolutions: {e}")
        return []


def download_url(url, output_folder, audio_only, format_id=None):
    try:
        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Base command to download
        command = [
            "yt-dlp",
            "-i",  # Ignore errors
            "--output",
            f"{output_folder}/%(title)s.%(ext)s",
            url,
        ]

        if audio_only:
            command.extend(
                [
                    "--extract-audio",  # Extract audio only
                    "--audio-format",
                    "mp3",  # Convert to MP3
                ]
            )
        elif format_id:
            command.extend(["-f", format_id])
        else:
            command.extend(["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"])

        # Run the command
        subprocess.run(command, check=True)

        print(f"URL has been successfully downloaded to {output_folder}.")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading URL: {e}")


def handle_single_videos(audio_only):
    urls = input("Enter the YouTube URLs (comma-separated): ")
    url_list = [url.strip() for url in urls.split(",")]
    base_output_folder = os.path.expanduser("~/downloaded_by_yd")

    # Create base output folder if it doesn't exist
    if not os.path.exists(base_output_folder):
        os.makedirs(base_output_folder)

    for i, url in enumerate(url_list):
        if not audio_only:
            formats = get_video_resolutions(url)
            if formats:
                print("Available video resolutions:")
                for idx, (_, resolution) in enumerate(formats):
                    print(f"{idx + 1}. {resolution}")

                format_choice = int(input("Select the format number: ")) - 1
                if 0 <= format_choice < len(formats):
                    format_id = formats[format_choice][0]
                else:
                    print("Invalid choice. Downloading with default settings.")
                    format_id = None
            else:
                format_id = None
        else:
            format_id = None

        output_folder = os.path.join(base_output_folder, f"Video_{i}")
        download_url(url, output_folder, audio_only, format_id)


def handle_playlists(audio_only):
    urls = input("Enter the YouTube playlist URLs (comma-separated): ")
    url_list = [url.strip() for url in urls.split(",")]
    base_output_folder = os.path.expanduser("~/downloaded_by_yd")

    # Create base output folder if it doesn't exist
    if not os.path.exists(base_output_folder):
        os.makedirs(base_output_folder)

    for i, url in enumerate(url_list):
        output_folder = os.path.join(base_output_folder, f"Playlist_{i}")
        download_url(url, output_folder, audio_only)


def main():
    while True:
        print("\nMenu:")
        print("1. Download single videos")
        print("2. Download playlists")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "3":
            print("Exiting...")
            break

        audio_option = (
            input("Do you want to download as MP3 (audio only)? (yes/no): ")
            .strip()
            .lower()
            == "yes"
        )

        if choice == "1":
            handle_single_videos(audio_option)
        elif choice == "2":
            handle_playlists(audio_option)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
