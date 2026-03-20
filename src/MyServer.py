import os
import time
import webbrowser
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import parse_qs

hostName = "localhost"
serverPort = 8080

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "page_contacts.html"), "r", encoding="utf-8") as file:
    CONTENT = file.read()


class MyServer(BaseHTTPRequestHandler):
    """
    Специальный класс, который отвечает за
    обработку входящих запросов от клиентов
    """

    def do_GET(self):
        """Метод для обработки GET-запросов"""
        self.send_response(200)  # Отправка кода ответа
        self.send_header(
            "Content-type", "text/html; charset=utf-8"
        )  # Отправка типа данных, который будет передаваться
        self.end_headers()  # Завершение формирования заголовков ответа
        self.wfile.write(CONTENT.encode("utf-8"))  # Тело ответа

    def do_POST(self):
        """Метод для обработки POST-запросов"""
        content_length = int(self.headers["Content-Length"])

        body = self.rfile.read(content_length).decode("utf-8")

        data = parse_qs(body)
        for key, value in data.items():
            print(f"{key} = {value[0]}")

        # Перенаправляем обратно на главную страницу
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()


def run_server():
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started http://{hostName}:{serverPort}")
    time.sleep(1)
    webbrowser.open(f"http://{hostName}:{serverPort}")

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    webServer.server_close()
    print("Server stopped.")
