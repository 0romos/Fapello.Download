import os
import re
import requests
import argparse

class Downloader:
    def __init__(self, model_name, quantity):
        self.model_name = model_name
        self.quantity = quantity
        self.folder_name = model_name
        os.makedirs(self.folder_name, exist_ok=True)

    @staticmethod
    def check_num(no):
        return {
            range(9000, 10000): '/2000/',
            range(8000, 9000): '/9000/',
            range(7000, 8000): '/8000/',
            range(6000, 7000): '/7000/',
            range(5000, 6000): '/6000/',
            range(4000, 5000): '/5000/',
            range(3000, 4000): '/4000/',
            range(2000, 3000): '/3000/',
            range(1000, 2000): '/2000/',
        }.get(no, '/1000/')

    @staticmethod
    def video_exists(path):
        r = requests.head(path)
        return r.status_code == requests.codes.ok

    def download_media(self):
        if not self.quantity:
            r = requests.get(f"https://fapello.com/{self.model_name}/", headers=self.headers)
            soup = BeautifulSoup(r.text, features="lxml")
            q = soup.select_one("div#content a").get("href").split("/")[-2] # select the first image from the model's site, giving the highest image number.
            self.quantity = int(q)
        
        for i in range(self.quantity, 0, -1):
            model_num = self.check_num(i)
            model_url = 'https://fapello.com/content/' + self.model_name[0] + '/' + self.model_name[1] + '/' + self.model_name + model_num
            complete_url = model_url + self.model_name + '_' + str(i).zfill(4) + '.jpg'
            complete_video_url = model_url + self.model_name + '_' + str(i).zfill(4) + '.mp4'

            downloaded_file = requests.get(complete_url)
            file_name = complete_url[complete_url.rindex('/') + 1:]
            file_path = os.path.join(self.folder_name, file_name)
            print("[ DOWNLOADED ] ~> ", model_num+file_path)
            open(file_path, 'wb').write(downloaded_file.content)

            video_available = self.video_exists(complete_video_url)

            if video_available:
                print("[ DOWNLOADED ] ~> ", model_num+file_path)
                downloaded_video_file = requests.get(complete_video_url)
                video_file_name = complete_video_url[complete_video_url.rindex('/') + 1:]
                video_file_path = os.path.join(self.folder_name, video_file_name)
                open(video_file_path, 'wb').write(downloaded_video_file.content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help="Model name to be downloaded.", required=True)
    parser.add_argument("-q", "--quantity", help="Quantity of media to be downloaded.", required=False)
    args = parser.parse_args()

    downloader = Downloader(args.m, args.q)
    downloader.download_media()

