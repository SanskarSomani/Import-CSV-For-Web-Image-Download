import csv
from bs4 import BeautifulSoup
import requests
import os

# CREATE FOLDER
def folder_create(folder_name):
    try:
        # folder creation
        os.mkdir(folder_name)

    # if folder exists with that name, ask another name
    except FileExistsError:
        print("Folder Exist with that name!")
        folder_create(input("Enter Folder Name:- "))

# DOWNLOAD FIRST 6 IMAGES FROM THAT URL
def download_images(images, folder_name, url_index):
    # initial count is zero
    count = 0

    # print total images found in URL
    print(f"Total {len(images)} Image Found!")

    # checking if images is not zero
    if len(images) != 0:
        for i, image in enumerate(images[:6]):
            # From image tag, fetch image Source URL
            try:
                # In image tag, searching for "data-srcset"
                image_link = image["data-srcset"]
            except:
                try:
                    # In image tag, searching for "data-src"
                    image_link = image["data-src"]
                except:
                    try:
                        # In image tag, searching for "data-fallback-src"
                        image_link = image["data-fallback-src"]
                    except:
                        try:
                            # In image tag, searching for "src"
                            image_link = image["src"]
                        except:
                            pass

            # After getting Image Source URL
            # We will try to get the content of image
            try:
                r = requests.get(image_link).content
                try:
                    # possibility of decode
                    r = str(r, 'utf-8')
                except UnicodeDecodeError:
                    # After checking above condition, Image Download start
                    with open(f"{folder_name}/image_{url_index}_{i + 1:02d}.jpg", "wb+") as f:
                        f.write(r)

                    # counting number of image downloaded
                    count += 1
            except:
                pass

    # There might be possible, that all
    # images not download
    # if all images download
    if count == len(images):
        print(f"First 6 Images for URL {url_index} Downloaded!")

    # if all images not download
    else:
        print(f"Total {count} Images Downloaded Out of {min(6, len(images))}")


# MAIN FUNCTION START
def main(csv_file_path):
    folder_name = input("Enter Folder Name:- ")
    folder_create(folder_name)

    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for url_index, row in enumerate(reader, start=1):
            if not row:
                continue  # Skip empty rows
            url = row[0]
            print(f"\nProcessing URL {url_index}: {url}")
            # content of URL
            r = requests.get(url)

            # Parse HTML Code
            soup = BeautifulSoup(r.text, 'html.parser')

            # find all images in URL
            images = soup.findAll('img')

            # Call image download function
            download_images(images, folder_name, url_index)


# take CSV file path
csv_file_path = input("Enter CSV File Path:- ")

# CALL MAIN FUNCTION
main(csv_file_path)
