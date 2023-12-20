import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def fetch_wakatime_stats(api_key):
    api_url = "https://wakatime.com/api/v1/users/current/summaries"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Failed to fetch Wakatime data. Status code: {response.status_code}")
        return None

def get_top_languages(stats, num_languages=5):
    languages = {}

    for day_stat in stats:
        for language_stat in day_stat["languages"]:
            language_name = language_stat["name"]
            time_seconds = language_stat["total_seconds"]

            if language_name in languages:
                languages[language_name] += time_seconds
            else:
                languages[language_name] = time_seconds

    # Sort languages by total time spent and get top languages
    top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:num_languages]

    return top_languages

def generate_readme(stats):
    top_languages = get_top_languages(stats)

    readme_content = "# My Wakatime Stats\n\n"
    
    # Add a section for top languages
    readme_content += "## Top Languages\n\n"
    for rank, (language, time_seconds) in enumerate(top_languages, start=1):
        hours = time_seconds / 3600
        readme_content += f"{rank}. **{language}**: {hours:.2f} hours\n"

    with open("README.md", "w") as readme_file:
        readme_file.write(readme_content)

if __name__ == "__main__":
    wakatime_api_key = os.getenv("WAKATIME_API_KEY")

    if not wakatime_api_key:
        print("Wakatime API Key not found. Please set the WAKATIME_API_KEY environment variable.")
    else:
        wakatime_stats = fetch_wakatime_stats(wakatime_api_key)

        if wakatime_stats:
            generate_readme(wakatime_stats)
            print("README.md updated successfully.")
