import PyPDF2

fileobject = open('CertificationGuidelines.pdf','rb')

pdffileReader = PyPDF2.PdfFileReader(fileobject)

extracted_text = ""

for pageNum in range(pdffileReader.numPages):
    pdfpageObj = pdffileReader.getPage(pageNum)

    extracted_text += pdfpageObj.extractText()
    
fileobject.close()
print(extracted_text)
