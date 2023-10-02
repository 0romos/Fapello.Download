import os
import re
import requests
import argparse

class Downloader:
    def __init__(self, model_name, quantity, headers, only_update):
        self.model_name = model_name
        self.folder_name = model_name
        self.headers = headers
        self.only_update = only_update
        self.set_quantity(quantity)
        os.makedirs(self.folder_name, exist_ok=True)

    @staticmethod
    def check_num(no):
        if no in range(9000, 10000):
            return'/2000/'
        elif no in range(8000, 9000):
            return '/9000/'
        elif no in range(7000, 8000):
            return '/8000/'
        elif no in range(6000, 7000):
            return '/7000/'
        elif no in range(5000, 6000):
            return '/6000/'
        elif no in range(4000, 5000):
            return '/5000/'
        elif no in range(3000, 4000):
            return '/4000/'
        elif no in range(2000, 3000):
            return  '/3000/'
        elif no in range(1000, 2000):
            return '/2000/'
        else:
            return '/1000/'

    @staticmethod
    def video_exists(path, headers):
        r = requests.head(path, headers=headers)
        return r.status_code == requests.codes.ok

    def set_quantity(self, quantity):
        if not quantity:
            r = requests.get("https://fapello.com/" + self.model_name + "/", headers=self.headers)
            soup = BeautifulSoup(r.text, features="lxml")
            q = soup.select_one("div#content a").get("href").split("/")[-2]
            self.quantity = int(q)
        else:
            self.quantity = quantity

    def download_media(self):
        if not self.quantity:
            r = requests.get("https://fapello.com/" + self.model_name + "/", headers=self.headers)
            soup = BeautifulSoup(r.text, features="lxml")
            q = soup.select_one("div#content a").get("href").split("/")[-2] # select the first image from the model's site, giving the highest image number.
            self.quantity = int(q)
        
        for i in range(self.quantity, 0, -1):
            model_num = self.check_num(i)
            model_url = 'https://fapello.com/content/' + self.model_name[0] + '/' + self.model_name[1] + '/' + self.model_name + model_num
            complete_url = model_url + self.model_name + '_' + str(i).zfill(4) + '.jpg'
            complete_video_url = model_url + self.model_name + '_' + str(i).zfill(4) + '.mp4'

            downloaded_file = requests.get(complete_url, headers=self.headers)
            file_name = complete_url[complete_url.rindex('/') + 1:]
            file_path = os.path.join(self.folder_name, file_name)
            
            if downloaded_file.status_code != requests.codes.ok:
                print("[ " + str(downloaded_file.status_code) + " ] ~> ", model_num+file_path)
                continue

            if self.only_update and os.path.exists(file_path):
                print("[ EXISTS ] ~> ", model_num+file_path)
                break
            
            print("[ DOWNLOADED ] ~> ", model_num+file_path)
            open(file_path, 'wb').write(downloaded_file.content)

            video_available = self.video_exists(complete_video_url, headers=self.headers)

            if video_available:
                print("[ DOWNLOADED ] ~> ", model_num+file_path)
                downloaded_video_file = requests.get(complete_video_url, headers=self.headers)
                video_file_name = complete_video_url[complete_video_url.rindex('/') + 1:]
                video_file_path = os.path.join(self.folder_name, video_file_name)
                open(video_file_path, 'wb').write(downloaded_video_file.content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help="Model name to be downloaded.", required=True)
    parser.add_argument("-q", "--quantity", help="Quantity of media to be downloaded.", required=False)
    parser.add_argument("-u", "--update", help="Only download until there's a file in the countdown that already exists.", action="store_true", required=False)
    args = parser.parse_args()

    headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0"}
    
    downloader = Downloader(args.model, args.quantity, headers, args.update)
    downloader.download_media()

