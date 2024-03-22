import requests
import serial
import time
from maze import MazeGenerator

class BotTelegram:
    def __init__(self, serial_port='COM5', baud_rate=9600):
        self.ser = serial.Serial(serial_port, baud_rate, timeout=1)
        self.lampu_A_status = 'OFF'
        self.lampu_B_status = 'OFF'
        self.maze_generator = MazeGenerator((5, 5))

    def send_telegram_request(self, method, data):
        token = "7181750288:AAEsny_8Yxefryhbe3Z5-FW3qZB4X8AFzK0"
        url = f"https://api.telegram.org/bot{token}/{method}"
        response = requests.post(url, json=data)
        return response.json()

    def start(self, message):
        chat_id = message["chat"]["id"]
        self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": "Halo! Saya adalah bot dari TeamUno1. Bagaimana kabarmu? Sudah makan? Belum? Lapar dong."})
        self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": "Silahkan Ketik /Menu untuk mengakses tombol"})

    def menu_bot(self, message):
        chat_id = message["chat"]["id"]
        keyboard = self.get_markup()
        self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": "Pilih Opsi Menu Berikut:", "reply_markup": keyboard})

    def get_markup(self):
        keyboard = {
            "inline_keyboard": [
                [{"text": f'Lampu A : {self.lampu_A_status}', "callback_data": "lampu_A"}],
                [{"text": f'Lampu B : {self.lampu_B_status}', "callback_data": "lampu_B"}],
                [{"text": "Baca Sensor Jarak", "callback_data": "Read_J"}],
                [{"text": "Baca Sensor Suhu", "callback_data": "Read_S"}],
                [{"text": "Generate Maze", "callback_data": "generate_maze"}],
                [{"text": "Solve Maze", "callback_data": "solve_maze"}]
            ]
        }
        return keyboard

    def handle_button_click(self, callback_query):
        button_data = callback_query["data"]
        message = callback_query["message"]
        message_id = message["message_id"]
        chat_id = message["chat"]["id"]
        

        if button_data == "lampu_A":
            if self.lampu_A_status == 'OFF':
                self.ser.write(b'R1 ON\n')
                self.lampu_A_status = 'ON'
                keyboard = self.get_markup()
                self.send_telegram_request("editMessageReplyMarkup", {"chat_id": chat_id, "message_id": message_id, "reply_markup": keyboard})
            else:
                self.ser.write(b'R1 OFF\n')
                self.lampu_A_status = 'OFF'
                keyboard = self.get_markup()
                self.send_telegram_request("editMessageReplyMarkup", {"chat_id": chat_id, "message_id": message_id, "reply_markup": keyboard})
        elif button_data == "lampu_B":
            if self.lampu_B_status == 'OFF':
                self.ser.write(b'R2 ON\n')
                self.lampu_B_status = 'ON'
                keyboard = self.get_markup()
                self.send_telegram_request("editMessageReplyMarkup", {"chat_id": chat_id, "message_id": message_id, "reply_markup": keyboard})
            else:
                self.ser.write(b'R2 OFF\n')
                self.lampu_B_status = 'OFF'
                keyboard = self.get_markup()
                self.send_telegram_request("editMessageReplyMarkup", {"chat_id": chat_id, "message_id": message_id, "reply_markup": keyboard})
        elif button_data == "Read_J":
            self.ser.write(b'RU\n')
            time.sleep(1)
            self.ser.flushInput()
            response = self.ser.readline().decode().strip()
            self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": response})
        elif button_data == "Read_S":
            self.ser.write(b'RS\n')
            time.sleep(1)
            self.ser.flushInput()
            response = self.ser.readline().decode().strip()
            self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": response})
        elif button_data == "generate_maze":
            self.maze_generator.generate()
            maze_text = self.maze_generator.generate_text(self.maze_generator.generated_maze)
            self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": f"""
Maze dibuat:
```
{maze_text}
```""", "parse_mode": "MarkdownV2"})
        elif button_data == "solve_maze":
            if self.maze_generator.generated_maze == None:
                response = "Maze belum dibuat. Silakan gunakan opsi 'Generate Maze' terlebih dahulu."
                self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": response})
                self.send_telegram_request("answerCallbackQuery", {"callback_query_id": callback_query["id"]})
            else:
                response = self.maze_generator.solve_maze()
                self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": response})
                self.send_telegram_request("answerCallbackQuery", {"callback_query_id": callback_query["id"]})

    def process_message(self, message):
        text = message.get("text", "")
        if "/start" in text:
            self.start(message)
        elif "/Menu" in text:
            self.menu_bot(message)
        # Add more message handling logic as needed
    def close_arduino_connection(self):
        self.ser.close()

