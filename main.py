import json
import os
import chardet
from tkinter import Tk, filedialog, Label, Entry, Button,messagebox,Canvas
from tkinterdnd2 import TkinterDnD, DND_FILES

class TexturePackerConverter:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("Old Texture Packer to Unity Converter")

        self.file_path_entry = Entry(self.root, width=40)
        self.file_path_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(self.root, text="File Path:").grid(row=0, column=0, padx=10, pady=10)

        # 绑定拖拽事件
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop)

        Button(self.root, text="Browse", command=self.choose_json_file).grid(row=0, column=2, padx=10, pady=10)
        Button(self.root, text="Export", command=self.convert_and_export).grid(row=1, column=1, pady=10)


    def handle_drop(self, event):
        # 从拖拽事件中获取文件路径
        file_path = event.data

        # 检查文件扩展名是否为 .txt
        if file_path.lower().endswith('.txt'):
            # 更新 Entry 中的文本
            self.file_path_entry.delete(0, 'end')
            self.file_path_entry.insert(0, file_path)
        else:
            messagebox.showinfo("Invalid File", "Please drop a valid .txt file.")
            print("Please drop a valid .txt file.")

    def choose_json_file(self):
        file_path = filedialog.askopenfilename(
            title="Choose JSON or TXT file",
            filetypes=[("Txt files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        self.file_path_entry.delete(0, 'end')
        self.file_path_entry.insert(0, file_path)

    def convert_and_export(self):
        json_file = self.file_path_entry.get()

        if not json_file:
            print("Please choose a JSON or TXT file.")
            return

        # filename = os.path.splitext(json_file)
        # new_file = filename + ".tpsheet"
        # output_file = new_file

        filename, extension = os.path.splitext(json_file)
        new_file = filename + ".tpsheet"
        output_file = new_file

        self.convert_texture_packer_to_unity(json_file, output_file)

    def convert_texture_packer_to_unity(self, json_file, output_file):
        encoding = self.detect_encoding(json_file)

        with open(json_file, 'r', encoding=encoding) as f:
            data = json.load(f)

        frames = data['frames']
        meta = data['meta']
        texture_size = meta['size']

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("#\n")
            f.write("# Sprite sheet data for Unity.\n")
            f.write("#\n")
            f.write(f":format=40300\n")
            f.write(f":texture={meta['image']}\n")
            f.write(f":size={texture_size['w']}x{texture_size['h']}\n")
            f.write(":pivotpoints=enabled\n")
            f.write(":borders=disabled\n")
            f.write(":alphahandling=ClearTransparentPixels\n")
            f.write("\n")

            for frame_name, frame_data in frames.items():
                frame = frame_data['frame']
                source_size = frame_data['sourceSize']
                sprite_source_size = frame_data['spriteSourceSize']

                x = frame['x']
                y = texture_size['h'] - frame['y'] - frame['h']
                w = frame['w']
                h = frame['h']

                pivot_x = sprite_source_size['x'] / source_size['w']
                pivot_y = 1 - (sprite_source_size['y'] / source_size['h'])

                pivot_x = 0.5
                pivot_y = 0.5

                f.write(f"{frame_name.replace('.png', '')};{x};{y};{w};{h}; {pivot_x};{pivot_y}; 0;0;0;0\n")

    def detect_encoding(self, file_path, fallback_encodings=['utf-8', 'gb2312']):
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        detected_encoding = result['encoding']

        for encoding in fallback_encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read()
                return encoding
            except UnicodeDecodeError:
                pass

        return detected_encoding

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    converter = TexturePackerConverter()
    converter.run()
