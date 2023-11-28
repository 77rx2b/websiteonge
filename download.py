import os
import re
import requests

downloaded_files = {}

def download_file(url, folder):
    if url in downloaded_files:
        return downloaded_files[url]

    response = requests.get(url)
    if response.status_code == 200:
        file_name = os.path.join(folder, url.split("/")[-1])
        file_name = get_unique_filename(file_name)
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {file_name}")
        downloaded_files[url] = file_name
        return file_name
    else:
        print(f"Failed to download: {url}")
        return None

def get_unique_filename(file_path):
    base_name, ext = os.path.splitext(file_path)
    counter = 1
    while os.path.exists(file_path):
        file_path = f"{base_name}_{counter}{ext}"
        counter += 1
    return file_path

def replace_urls_in_script(script_content, old_urls, new_urls):
    for old_url, new_url in zip(old_urls, new_urls):
        script_content = script_content.replace(old_url, new_url)
    return script_content

def extract_urls_from_script(script_content):
    # Use a regular expression to find all URLs in the script
    url_pattern = r"'(https://(?:cdn\.discordapp\.com|media\.discordapp\.net)/.*?\.(?:png|webp|gif))'"
    urls = re.findall(url_pattern, script_content)
    return urls

def main(input_file, output_folder):
    global downloaded_files
    downloaded_files = {}

    with open(input_file, 'r', encoding='utf-8') as file:
        script_content = file.read()

    old_urls = extract_urls_from_script(script_content)
    new_urls = [f"https://77rx2b.github.io/3D-models/portfolio/{os.path.basename(download_file(url, output_folder))}" for url in old_urls]

    # Replace old URLs with new formatted URLs
    updated_script_content = replace_urls_in_script(script_content, old_urls, new_urls)

    # Save the updated script to the input file
    with open(input_file, 'w', encoding='utf-8') as file:
        file.write(updated_script_content)

if __name__ == "__main__":
    input_file_path = "blog.txt"  # Replace with the path to your input HTML file
    output_folder_path = "portfolio"  # Replace with the desired output folder

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    main(input_file_path, output_folder_path)
