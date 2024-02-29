from pdfminer.high_level import extract_text

text = extract_text("./paper/1512.03385.pdf")
print(text.find("accuracy"))
print(text[700:760])