import pprint
from pathlib import Path
import requests
import subprocess
import yaml
import shutil
import datetime
import pytz
import os
from tqdm import tqdm
import time
from urllib import request
import sys
from pdf2image import convert_from_path
import glob
from pdf_task import PdfTask
is_colab = 'google.colab' in sys.modules

class Task:

    tmp_top_dir = "/tmp"

    def __init__(self):
        pass

    @staticmethod
    def pdfFromUrl(url, output_dir, process, ruby, debug=True):
        # output_dir = str(Path(output_dir))

        x = Task()
        x.url = url
        x.output_dir = str(Path(output_dir))
        x.process = process
        x.ruby = ruby

        x.getFilenameFromUrl()
        x.prepareTmpDir()
        x.prepareImgDir()

        x.tmp_pdf_path = "{}/{}.pdf".format(x.tmp_dir, x.filename)

        x.downloadFile(x.tmp_pdf_path)

        x.createImagesFromPDF()

        x.main(debug)

        return x

    @staticmethod
    def pdfFromLocal(input_file, output_dir, process, ruby, debug=True):
        output_dir = str(Path(output_dir))

        x = Task()
        # x.url = url

        # パラメータの設定
        x.output_dir =  output_dir
        x.process = process
        x.ruby = ruby



        x.getFilename(input_file)
        x.prepareTmpDir()
        x.prepareImgDir()

        x.tmp_pdf_path = "{}/{}.pdf".format(x.tmp_dir, x.filename)

        # x.downloadFile(x.tmp_pdf_path)
        Task.copyFile(input_file, x.tmp_pdf_path)

        x.createImagesFromPDF()

        x.main(debug)

        return x

    @staticmethod
    def pdfFromLocalDir(input_dir, output_dir, process, ruby, debug=True):
        input_dir = str(Path(input_dir))

        target_files = glob.glob(input_dir+"/**/*.pdf", recursive=True)

        for file in target_files:
            x = Task.pdfFromLocal(file, output_dir, process, ruby)
        
        return x

    @staticmethod
    def imgFromUrl(url, output_dir, process, ruby, debug=True):
        # output_dir = str(Path(output_dir))

        x = Task()
        x.url = url
        x.output_dir = str(Path(output_dir))
        x.process = process
        x.ruby = ruby

        x.getFilenameFromUrl()
        x.prepareTmpDir()
        x.prepareImgDir()

        path = x.tmp_img_dir+"/"+x.filename+".jpg"
        x.downloadFile(path)

        # x.createImagesFromPDF()

        x.main(debug)

        return x

    @staticmethod
    def imgFromLocal(input_file, output_dir, process, ruby, debug=True):
        # output_dir = str(Path(output_dir))

        x = Task()
        # x.url = url
        x.output_dir = str(Path(output_dir))
        x.process = process
        x.ruby = ruby

        # x.getFilenameFromUrl()
        x.getFilename(input_file)
        # x.getFilenameFromPath(input_file)
        x.prepareTmpDir()
        x.prepareImgDir()

        path = x.tmp_img_dir+"/"+x.filename+".jpg"
        # x.downloadFile(path)
        Task.copyFile(input_file, path)

        # x.createImagesFromPDF()

        x.main(debug)

        return x

    @staticmethod
    def imgFromLocalDir(input_dir, output_dir, process, ruby, debug=True):
        output_dir = str(Path(output_dir))

        input_dir = str(Path(input_dir))


        x = Task()
        # x.url = url

        # パラメータの設定
        x.output_dir = output_dir
        x.process = process
        x.ruby = ruby

        folder_name = input_dir.split("/")[-1]

        x.tmp_dir = input_dir
        x.output_dir = "{}/{}".format(output_dir, folder_name)

        x.main(debug)

        return x

    @staticmethod
    def iiif(url, output_dir, process, ruby, process_size, sleep_time, debug=True):
        # output_dir = str(Path(output_dir))

        x = Task()

        # パラメータの設定
        x.url = url
        x.output_dir = str(Path(output_dir))
        x.process = process
        x.ruby = ruby
        x.process_size = process_size
        x.sleep_time = sleep_time

        # 準備
        x.getFilename(url)
        x.prepareTmpDir()
        x.prepareImgDir()

        x.downloadImages()

        x.main(debug)

        return x

    def downloadImages(self):
        # def downloadImages(url, output_dir, time_sleep):
        # print("### IIIFマニフェストを用いた画像のダウンロード ###")

        url = self.url
        process_size = self.process_size
        sleep_time = self.sleep_time
        output_dir = self.tmp_img_dir

        df = requests.get(url).json()
        canvases = df["sequences"][0]["canvases"]
        if process_size > 0:
            canvases = canvases[0:process_size]
        for i in tqdm(range(len(canvases))):
            res = canvases[i]["images"][0]["resource"]
            index = str(i+1).zfill(4)
            path = "{}/{}.jpg".format(output_dir, index)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            url = canvases[i]["images"][0]["resource"]["@id"]
            time.sleep(sleep_time)
            request.urlretrieve(url, path)

    @staticmethod
    def copyFile(in_, out_):
        shutil.copyfile(in_, out_)

    @staticmethod
    def updateConfigRuby(path, ruby):
        c = path # "config.yml"
        with open(c) as file:
            obj = yaml.safe_load(file)
            obj["line_ocr"]["yield_block_rubi"] = ruby
        with open(c, 'w') as file:
            yaml.dump(obj, file)

    def downloadFile(self, path):
        # self.tmp_pdf_path = "{}/{}.pdf".format(self.tmp_dir, self.filename)
        
        filename = Path(path) # self.tmp_pdf_path
        response = requests.get(self.url, verify=False)
        filename.write_bytes(response.content)

    def createImagesFromPDF(self):
        pdf_path = Path(self.tmp_pdf_path)
        img_path=Path(self.tmp_img_dir)
        try:
            convert_from_path(pdf_path, output_folder=img_path,fmt='jpeg', output_file=pdf_path.stem,dpi=100)
        except Exception as e:
            print(e)
    
    def getFilenameFromUrl(self):
        path = self.url
        self.filename = path.split("/")[-1].split(".")[0]

    def getFilename(self, path):
        # path = self.url
        self.filename = path.split("/")[-1].split(".")[0]


    def prepareTmpDir(self):
        tmp_top_dir = self.tmp_top_dir
        file_id = self.filename

        run_id = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y%m%d%H%M%S')
        tmp_dir = "{}/{}/{}".format(tmp_top_dir, run_id, file_id)
        self.tmp_dir = tmp_dir

    def prepareImgDir(self):
        # print("### 入力画像フォルダの作成 ###")

        tmp_dir = self.tmp_dir

        tmp_img_dir = "{}/img".format(tmp_dir)
        os.makedirs(tmp_img_dir, exist_ok=True)

        self.tmp_img_dir = tmp_img_dir

    def main(self, debug: bool) -> None:
        """
        OCR処理を実行し、結果を出力ディレクトリに保存するメイン関数。

        :param debug: デバッグモードが有効かどうかを示すブール値。
        """
        if debug:
            print("### OCR処理を実行しています。 ###")

        self.get_process_param()
        self.create_output_dir_if_exist()

        config_file = "config.yml"

        Task.updateConfigRuby(config_file, self.ruby)

        input_dir = self.tmp_dir
        output_dir = self.output_dir
        process = self.p

        command_line = f"python main.py infer -c {config_file} -s s \"{input_dir}\" \"{output_dir}\" -x -i -p {process}"

        subprocess.call(command_line, shell=True)

        self.merge_txt_and_download()

        PdfTask.createPdf(input_dir, output_dir)

    def merge_txt_and_download(self) -> None:
        """
        テキストファイルをマージし、結果を指定された出力ディレクトリに保存する。
        """
        output_dir = self.output_dir
        tmp_dirs = glob.glob(os.path.join(output_dir, "*/txt"))
        txt_dir = tmp_dirs[0]
        
        file_id = os.path.basename(os.path.dirname(txt_dir))
        output_id_dir = os.path.join(output_dir, file_id)

        txt_files = glob.glob(os.path.join(txt_dir, "*.txt"))
        txt_files.sort()
        merged_txt_file_path = os.path.join(output_id_dir, f"{file_id}.txt")

        with open(merged_txt_file_path, 'a', encoding="utf-8") as merged_txt_file:
            for each_txt_file_path in txt_files:
                with open(each_txt_file_path, 'r', encoding="utf-8") as each_txt_file:
                    data = each_txt_file.read()
                    merged_txt_file.write(f"{data}\n")

    def get_process_param(self):
        process = self.process
        p = "0..3"
        if process == "傾き補正,レイアウト抽出,文字認識(OCR)":
            p = "1..3"
        elif process == "レイアウト抽出,文字認識(OCR)":
            p = "2..3"
        elif process == "文字認識(OCR)":
            p = "3"
        # return p
        self.p = p

    def create_output_dir_if_exist(self): # output_dir, p):
        output_dir = self.output_dir
        p = self.p
        output_dir = output_dir + "@p" + p 
        if os.path.exists(output_dir): 
            run_id = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y%m%d%H%M%S')
            output_dir = output_dir + "_" + run_id
            # print("!!! 指定された出力フォルダが既に存在するため、 {} に出力します。 !!!".format(output_dir))

        self.output_dir = output_dir

        # 親フォルダの作成
        Task.createParentDir(self.output_dir)

    @staticmethod
    def createParentDir(path):
        basename = os.path.basename(path)
        parent_path = os.path.dirname(path)
        os.makedirs(parent_path, exist_ok=True)
