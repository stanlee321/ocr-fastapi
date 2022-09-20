from cnocr import CnOcr

img_fp = './impuestos.jpeg'

rec_model_path = './models/cnocr'
det_model_path = './models/cnstd'

ocr = CnOcr(det_model_name='en_PP-OCRv3_det',
    rec_model_name='en_PP-OCRv3',
    rec_root=rec_model_path,
    det_root=det_model_path)

out = ocr.ocr(img_fp)

#print(out)

word = ""

for o in out:
    word = word + o['text']

print(word)
