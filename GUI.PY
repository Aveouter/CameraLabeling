import tkinter as tk
import os
from PIL import Image, ImageTk

class AnnotationApp:
    def __init__(self, master,imgfile_path,len_data):
        self.master = master
        self.master.title("Image Annotation Tool")
        self.images = []
        self.imgfile_path = imgfile_path
        self.len_data = len_data
        # Load sample images
        for frame_count in range(1,24,self.len_data + 1):
            for i in range(1, 7):
                file_path = os.path.join(self.imgfile_path,str(i))
                img_path = f"video_{i}_{frame_count}.jpg"  # Replace with your image paths
                file_path = os.path.join(file_path,img_path)
                image = Image.open(file_path)
                image = image.resize((300, 200), Image.ANTIALIAS)
                self.images.append(ImageTk.PhotoImage(image))

        # Create and layout image buttons
        for i, img in enumerate(self.images):
            row = i // 3
            col = i % 3
            btn = tk.Button(master, image=img, command=lambda idx=i: self.annotate(idx))
            btn.grid(row=row, column=col, padx=5, pady=5)
        # Create text output box
        self.output_text = tk.Text(master, height=10, width=40)
        self.output_text.grid(row=3, columnspan=3, padx=5, pady=5)

    def annotate(self, idx):
        # Output the index of the clicked image
        annotation_text = f"Clicked on Image {idx+1}\n"
        self.output_text.insert(tk.END, annotation_text)


def GUI_main():
    root = tk.Tk()
    app = AnnotationApp(root)
    root.mainloop()

if __name__ == "__main__":
    GUI_main()
