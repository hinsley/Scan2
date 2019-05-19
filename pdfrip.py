#!/usr/bin/env python

import os
import re
import shutil

from pdf2image import convert_from_path
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


debug = False

coc_dir_path = r"U:\Quality\CERTIFICATE OF COMPLIANCE\Vendor Provided COCs"

def get_coc_filing_data(ocr_text):
    if debug:
        print(ocr_text)
    try:
        return {
            "dates": re.findall(u"(?<=Date: )[0-9]+/[0-9]+/[0-9]+", ocr_text),
            "parts": re.findall(u"(?<=P[/I]N )[0-9]\\S+", ocr_text),
            "purchase orders": re.findall(u"(?<=PO: )[0-9]+", ocr_text),
            "quantities": re.findall(u"(?<=Quantity: )[0-9]+", ocr_text)
        }
    except Exception as e:
        print(e)


def pdf_to_txt(path, output_path):
    pages = convert_from_path(path)
    with open(output_path, "a") as output_file:
        for page in pages:
            page.save("out.jpg", "JPEG")
            # Perform OCR reading and store in output file.
            output_file.write(pytesseract.image_to_string(Image.open("out.jpg")) + "\n")
    os.remove("out.jpg")


def construct_cocs(coc_filing_data):
    coc_quantity = max([len(coc_filing_data[field]) for field in coc_filing_data])
    cocs = []

    for n in range(coc_quantity):
        cocs.append({})

        try:
            cocs[n]["date"] = coc_filing_data["dates"][n].replace("/", "-")
        except IndexError:
            pass
        try:
            cocs[n]["part"] = coc_filing_data["parts"][n]
        except IndexError:
            pass
        try:
            cocs[n]["purchase order"] = coc_filing_data["purchase orders"][n]
        except IndexError:
            pass
        try:
            cocs[n]["quantity"] = coc_filing_data["quantities"][n]
        except IndexError:
            pass

    return cocs


if __name__ == "__main__":
    while True:
        try:
            try:
                path = input("")
                if not path.endswith(".pdf"):
                    print("Path '{}' does not have a '.pdf' file extension.".format(path))
                    continue
            except EOFError:
                break
            output_file_name = "{}.txt".format(path)
            try:
                os.remove(output_file_name)
            except OSError:
                pass

            pdf_to_txt(path, output_file_name)


            with open(output_file_name) as output_file:
                coc_filing_data = get_coc_filing_data(output_file.read())

            cocs = construct_cocs(coc_filing_data)
            coc_file_names = []
            for coc in cocs:
                coc_file_name = ""
                if "part" in coc:
                    coc_file_name += "{} ".format(coc["part"])
                coc_file_name += "COC"
                if "purchase order" in coc:
                    coc_file_name += " PO# {}".format(coc["purchase order"])
                if "date" in coc:
                    coc_file_name += " {}".format(coc["date"])
                if "quantity" in coc:
                    coc_file_name += " - {} PCS".format(coc["quantity"])
                coc_file_name += ".pdf"
                coc_file_names.append(coc_file_name)

            for coc_file_name in coc_file_names:
                write_path = "{}\\{}".format(coc_dir_path, coc_file_name)
                path_to_check = write_path
                coc_edition = 1
                while True:
                    path_to_check = write_path
                    if coc_edition != 1:
                        path_to_check = "{} ({}){}".format(path_to_check[:-len(".pdf")], str(coc_edition), path_to_check[-len(".pdf"):])

                    if os.path.isfile(path_to_check):
                        coc_edition += 1
                    else:
                        write_path = path_to_check
                        break
                print("'{}' -> '{}'".format(path, write_path))
                shutil.copy2(path, write_path)
                os.remove(path)
                os.remove(output_file_name)
        except:
            pass
