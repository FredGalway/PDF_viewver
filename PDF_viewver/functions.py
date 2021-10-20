from tkinter import *
import os
from PIL import Image, ImageTk

# Global variable lists
page_contents = []
all_images = []
img_idx = [0]
displayed_img = []
preview_img = []

#place LOGO on the grid
def display_logo(url, row, column):
    img = Image.open(url)
    #resize image
    img = img.resize((int(img.size[0]/1.5),int(img.size[1]/1.5)))
    img = ImageTk.PhotoImage(img)
    img_label = Label(image=img, bg="white")
    img_label.image = img
    img_label.grid(column=column, row=row, rowspan=2, sticky=NW, padx=20, pady=40)

#place ICONS on the grid
def display_icon(url, row, column, stick, funct):
    icon = Image.open(url)
    #resize icon
    icon = icon.resize((20,20))
    icon = ImageTk.PhotoImage(icon)
    icon_label = Button(image=icon, command=funct)
    icon_label.image = icon
    icon_label.grid(column=column, row=row, sticky=stick, pady=20)

#place a texbox area on the footer
def display_textbox(content, ro, col, root):
    text_box = Text(root, height=10, width=30, padx=10, pady=10)
    text_box.insert(1.0, content)
    text_box.tag_configure("center", justify="center")
    text_box.tag_add("center", 1.0, "end")
    text_box.grid(column=col, row=ro, sticky=SW, padx=25, pady=15)

#Detect Images inside the PDF document
#Thank you sylvain of Stackoverflow
#https://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python
def extract_images(page):
    images = []
    if '/XObject' in page['/Resources']:
        xObject = page['/Resources']['/XObject'].getObject()

        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].getData()
                mode = ""
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "CMYK"
                img = Image.frombytes(mode, size, data)
                images.append(img)
    return images


# Resize and Display the current_image images
def resize_images(img):
    width, height = int(img.size[0]), int(img.size[1])
    if width > height :
        height = int(300/width*height)
        width = 300
    elif height > width:
        width = int(300/height*width)
        height = 250
    else:
        width, height = 250, 250
    img = img.resize((width, height))
    return img

def display_images(img):
    img = resize_images(img)
    img = ImageTk.PhotoImage(img)
    img_label = Label(image=img, bg="white")
    img_label.image = img
    img_label.grid(row=4, rowspan=2, column=2)
    return img_label


# Function to save PDF Images
def save_all(images):
    counter = 1

    # Detect if the repertory exists before to create it
    if not os.path.exists('PDF-img'):
        os.makedirs('PDF-img')

    # Save all images from an extrated PDF file
    for i in images:
        if i.mode != "RGB":
            i = i.convert("RGB")
        i.save("PDF-img/" + "img" + str(counter) + ".png", format="png")
        counter += 1

# Function to save the current_image image
def save_image(i):
    if not os.path.exists('PDF-img'):
        os.makedirs('PDF-img')

    if i.mode != "RGB":
        i = i.convert("RGB")
    i.save("PDF-img/" + "preview.png", format="png")
