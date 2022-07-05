import glob
import bs4
import os
from urllib import request
import shutil
import json
import subprocess

class PdfTask:
    @staticmethod
    def createPdf(input_dir, output_dir):
        xml_files = glob.glob(output_dir + "/*/xml/*.xml")

        xml_file = xml_files[0]
        file_id = xml_file.split("/")[-3]

        soup = bs4.BeautifulSoup(open(xml_file), 'xml')

        pages = soup.find_all("PAGE")

        textAnnotationsMap = {}

        for i in range(len(pages)):
            page = pages[i]
            xs = 0
            if i == 1:
                xs = int(pages[i-1].get("WIDTH"))
            
            lines = page.find_all("LINE")

            IMAGENAME = page.get("IMAGENAME")

            IMAGENAME = IMAGENAME.replace("_L.jpg", ".jpg").replace("_R.jpg", ".jpg")

            if IMAGENAME not in textAnnotationsMap:
                textAnnotationsMap[IMAGENAME] = []

            textAnnotations = textAnnotationsMap[IMAGENAME]
            
            for line in lines:
                string = line.get("STRING")
                height = int(line.get("HEIGHT"))
                width = int(line.get("WIDTH"))
                x = int(line.get("X"))
                y  = int(line.get("Y"))

                x0 = xs + x
                y0 = y

                x1 = x0 + width
                y1 = y0 + height

                e = {
                    "description": string,
                    "boundingPoly": {
                    "vertices": [
                        {
                        "x": x0,
                        "y": y0              
                    },
                        {
                        "x": x1,
                        "y": y0
                        },
                        {
                        "x": x1,
                        "y": y1
                        },
                        {
                        "x": x0,
                        "y": y1
                        }
                    ]
                    }
                }

                if len(textAnnotations) == 0:
                    # ダミー
                    textAnnotations.append(e)
                textAnnotations.append(e)

        output_id_dir = output_dir + "/" + file_id
        pdf_tmp_dir = output_id_dir + "/tmp"
        os.makedirs(pdf_tmp_dir, exist_ok=True)

        if not os.path.exists("gcv2hocr.py"):
            # !wget https://raw.githubusercontent.com/nakamura196/ndl_ocr/main/lib/gcv2hocr.py
            request.urlretrieve("https://raw.githubusercontent.com/nakamura196/ndl_ocr/main/lib/gcv2hocr.py", "gcv2hocr.py")

        for filename in textAnnotationsMap:
            image_path = input_dir + "/img/" + filename
            image_output_path = pdf_tmp_dir + "/" + filename
            json_output_path = pdf_tmp_dir + "/" + filename.replace(".jpg", ".json")
            hocr_output_path = pdf_tmp_dir + "/" + filename.replace(".jpg", ".hocr")

            if not os.path.exists(image_path):
                # 一時対応。もっと良い方法があると思われる。
                image_path = image_path.replace(".jpg", ".jpeg")
            
            # !cp $image_path $image_output_path
            # copyFile(image_path, image_output_path)
            shutil.copyfile(image_path, image_output_path)

            textAnnotations = textAnnotationsMap[filename]

            if len(textAnnotations) > 0:
                df = {
                    "responses": [
                        {
                            "textAnnotations": textAnnotationsMap[filename]
                        }
                    ]
                }
            else:
                df = {
                    "responses": [{}]
                }
            json.dump(df, open(json_output_path, "w"), ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))
            
            # !python gcv2hocr.py $json_output_path > $hocr_output_path
            line = "python gcv2hocr.py \"{}\" > \"{}\"".format(json_output_path, hocr_output_path)
            # print(line)
            subprocess.call(line, shell=True)
            
        if not os.path.exists("hocr-pdf.py"):
            # !wget https://raw.githubusercontent.com/nakamura196/ndl_ocr/main/lib/hocr-pdf.py 
            request.urlretrieve("https://raw.githubusercontent.com/nakamura196/ndl_ocr/main/lib/hocr-pdf.py", "hocr-pdf.py")

        pdf_path = output_id_dir + "/" + file_id + ".pdf"
        # !python hocr-pdf.py --savefile $pdf_path $pdf_tmp_dir
        line = "python hocr-pdf.py --savefile {} {}".format(pdf_path, pdf_tmp_dir)
        # subprocess.call(["python", "hocr-pdf.py", "--savefile", pdf_path, pdf_tmp_dir], shell=True)
        subprocess.call(line, shell=True)