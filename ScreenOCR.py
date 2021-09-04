from pyperclip import copy
from  tkinter import Tk, Canvas, mainloop
from PIL import Image, ImageTk, ImageGrab
from pyautogui import screenshot
from os import remove

def getText(way):
    try:
        import requests
        from bs4 import BeautifulSoup

        with open(way, 'rb') as f:
            files = {"uploadfile":  f.read()}
        # efset: 3
        data = {
            'efset1': '41',
            'efset2':'3',
            'efset3': '333',
            'efset4': '444',
            'efset5': '555',
            'efset6':'1',
            'efset7':'1',
            'efset8':'1',
            'submit':'OK'
        }

        URL = 'https://www.imgonline.com.ua/ocr-result.php'
        HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}
        # res = requests.post(URL, HEADERS, data=params)
        res = requests.post(URL,  data=data, headers=HEADERS, files=files)
        soup = BeautifulSoup(res.text, 'html.parser')

        hrefOnDownloadFile = soup.find('a', string='Открыть текстовый файл')

        if hrefOnDownloadFile == None:
            return False
        else:
            text = requests.get(hrefOnDownloadFile['href'], headers=HEADERS)
            copy( text.text.replace('\n', ' ').strip() )


    except Exception as e:
        print('Ошибка', e)
        getText(way)


class Main():
    def __init__(self):
        self.root = Tk()
        self.root.overrideredirect(True)

        self.canvas = Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(),
                             cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.root.attributes("-topmost", True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.x = self.y = 0
        self.rect = None
        self.start_x = None
        self.start_y = None
        screenshot('image.png')
        self.draw_image()

    def draw_image(self):
        self.im = Image.open('image.png')
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        # create rectangle if not yet exist
        # if not self.rect:
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, width='2', outline='black')

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        x1 = self.canvas.coords(self.rect)[0]
        y1 = self.canvas.coords(self.rect)[1]
        x2 = self.canvas.coords(self.rect)[2]
        y2 = self.canvas.coords(self.rect)[3]
        image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        image.save('sc.png')
        self.canvas.quit()
        getText('sc.png')
        remove('sc.png')
        remove('image.png')


m = Main()
mainloop()
