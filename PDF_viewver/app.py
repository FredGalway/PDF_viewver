from tkinter import *
from tkinter import ttk
from tkmacosx import Button
import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from functions import *

# Global variable lists
page_contents = []
all_images = []
img_idx = [0]
displayed_img = []
preview_img = []


# Initiate Root Window
root = Tk()
root.title("PDF Viewver")
bt_style = ttk.Style(root)
bt_style.theme_use('clam')
bt_style.configure('browse.TButton', borderwidth=0, highlightthickness=0, background="#20bebe", width=10, font=("Raleway", 17), fg='white')
bt_style.configure('other.TButton', borderwidth=0, highlightthickness=0, background="#f2f2f2", width=14, font=("Raleway", 15), fg='white', padding=6)

# To center the app window on screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = screen_width // 2 - 400
center_y = screen_height // 2 - 215
root.geometry('{}x{}+{}+{}'.format(800, 560, center_x, center_y))

# UI / ROW 0 & 1 / Header Background
# Merge of 3 columns and of 2 lines for the header part
header = Frame(root, width=800, height=180, bg="white")
header.grid(columnspan=3, rowspan=2, row=0)

# UI / Header Background / Logo
# Row(from TOP position), Column(from RIGHT Position)
display_logo('img/logo.png', 0, 0)

# UI / Header Background / Instructions
instructions = Label(root, text="Select a PDF file", font=("shanti", 12), bg="white")
instructions.grid(column=2, row=0, sticky=SE, padx=75, pady=5)

# UI / Header Background / Browse button
browse_text = StringVar()
browse_btn = ttk.Button(root, textvariable=browse_text, style='browse.TButton', command=lambda:open_file())
browse_text.set("Browse")
browse_btn.grid(row=1, column=2, sticky=NE, padx=50)


# UI / ROW 2 / Background
img_menu = Frame(root, width=800, height=40)
img_menu.grid(rowspan=3, row=1, columnspan=3)

# UI / ROW 2 / Middle Label Text
what_text = StringVar()
what_img = Label(root, textvariable=what_text, font=("shanti", 14), justify="right", anchor="e")
what_text.set("image" + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))
what_img.grid(row=2, column=1)

# UI / ROW 2 / Left button / Right Button
display_icon('img/arrow_l.png', 2, 0, E, lambda:left_arrow(all_images, preview_img, what_text))
display_icon('img/arrow_r.png', 2, 2, W, lambda:right_arrow(all_images, preview_img, what_text))


# UI / ROW 3 / Background
save_img = Frame(root, width=800, height=70, bg="#c8c8c8")
save_img.grid(rowspan=1, row=3, columnspan=3)

# UI / ROW 3 / Other Buttons
copyText_btn = ttk.Button(root, text="Copy text", style='other.TButton', command=lambda:copy_text(page_contents))
saveAll_btn = ttk.Button(root, text="Save all images", style='other.TButton', command=lambda:save_all(all_images))
save_btn = ttk.Button(root, text="Save preview", style='other.TButton', command=lambda:save_image(all_images[img_idx[-1]]))

copyText_btn.grid(row=3, column=0)
saveAll_btn.grid(row=3, column=1)
save_btn.grid(row=3, column=2)



# UI ROW 4 / Footer content area / Text and Image preview_img extractions
main_content = Frame(root, width=800, height=250, bg="#20bebe")
main_content.grid(row=4, rowspan=2, columnspan=3)



# Other functions

def open_file():

    bt_text = "loading ..."
    browse_text = StringVar()
    browse_text.set(bt_text)
    file = askopenfile(parent=root, mode='rb', title="Choose a PDF file", filetypes=[("Pdf file", "*.pdf")])

    if file:
        read_pdf = PyPDF2.PdfFileReader(file)
        page = read_pdf.getPage(0)
        page_content = page.extractText()
        page_content = page_content.replace('\u2122', "'")
        page_contents.append(page_content)

        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()

        for i in range(0, len(all_images)):
            all_images.pop()

        images = extract_images(page)

        for i in images:
            all_images.append(i)

        img = images[img_idx[-1]]

        preview_img = display_images(img)
        displayed_img.append(preview_img)

        #show text box on row 4 col 0
        display_textbox(page_content, 4, 0, root)

        #reset the button text back to Browse
        browse_text.set("Browse")



# Left arrow function
def left_arrow(all_images, preview_img, what_text):
    if img_idx[-1] >= 1:
        new_idx = img_idx[-1] - 1
        img_idx.pop()
        img_idx.append(new_idx)

        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()

        new_img = all_images[img_idx[-1]]
        preview_img = display_images(new_img)
        displayed_img.append(preview_img)
        what_text.set("image" + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))

    elif img_idx == - 1:
        print("Index out of range Fred")
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()



# Right arrow function
def right_arrow(all_images, preview_img, what_text):
    if img_idx[-1] < len(all_images) - 1:
        new_idx = img_idx[-1] + 1
        img_idx.pop()
        img_idx.append(new_idx)

        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()

        new_img = all_images[img_idx[-1]]
        preview_img = display_images(new_img)
        displayed_img.append(preview_img)
        what_text.set("image" + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))

    elif img_idx == len(all_images) - 1:
        print("Index out of range toto")
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()



# Function copy text
def copy_text(content):
    root.clipboard_clear()
    root.clipboard_append(content[-1])



root.mainloop()
