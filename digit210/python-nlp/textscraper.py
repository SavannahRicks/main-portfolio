
import bs4
import requests
import os

archive_url = "https://digitalmitford.org/lettersInterface.php"
def get_linkContents():
    r = requests.get(archive_url)
    print(f"{r=}")

    soup = bs4.BeautifulSoup(r.content, 'html.parser')


    linkText = []
    for item in soup.findAll('a'):
        print(f"{item.text}")
        linkText.append(item.text)
    print(linkText)
    download_toFile(linkText)
    return

def download_toFile(linkText):
    file_name = "my-scrapped-links.txt"  # MANUALLY CREATING A NEW FILE IN FILES
    print("Downloading file: " + file_name)
    working_dir = os.getcwd()
    file_deposit = os.path.join(working_dir, file_name)
    print(file_deposit)
    with open(file_deposit, 'w') as f:

        for item in linkText:
            f.write(item + '\n')
            # the '\n' adds a return character so each piece of text goes on its own line.
            print("Downloaded " + item)

    return

if __name__ == "__main__":
    get_links = get_linkContents()
