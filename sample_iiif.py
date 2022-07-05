from ndl_ocr.util import Util

url = "https://www.dl.ndl.go.jp/api/iiif/3437686/manifest.json" #@param {type:"string"}
output_dir = "aaa/content/drive/MyDrive/ndl_ocr/output/iiif" #@param {type:"string"}
process = "\u3059\u3079\u3066: \u30CE\u30C9\u5143\u5206\u5272,\u50BE\u304D\u88DC\u6B63,\u30EC\u30A4\u30A2\u30A6\u30C8\u62BD\u51FA,\u6587\u5B57\u8A8D\u8B58(OCR)" #@param ["\u3059\u3079\u3066: \u30CE\u30C9\u5143\u5206\u5272,\u50BE\u304D\u88DC\u6B63,\u30EC\u30A4\u30A2\u30A6\u30C8\u62BD\u51FA,\u6587\u5B57\u8A8D\u8B58(OCR)", "\u50BE\u304D\u88DC\u6B63,\u30EC\u30A4\u30A2\u30A6\u30C8\u62BD\u51FA,\u6587\u5B57\u8A8D\u8B58(OCR)", "\u30EC\u30A4\u30A2\u30A6\u30C8\u62BD\u51FA,\u6587\u5B57\u8A8D\u8B58(OCR)", "\u6587\u5B57\u8A8D\u8B58(OCR)"]

process_size =   1#@param {type:"number"}
sleep_time =   1#@param {type:"number"}
ruby = False #@param {type:"boolean"}

ins = Util.iiif(url, output_dir, process, ruby, process_size, sleep_time)