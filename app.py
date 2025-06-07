from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# Настройки сервера
HOST = 'localhost'
PORT = 8000

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Метод для обработки входящих GET-запросов"""
        try:
            # Получаем путь к директории, где находится скрипт
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Всегда используем contacts.html независимо от запрошенного пути
            html_path = os.path.join(current_dir, 'contacts.html')
            
            print(f"Requested path: {self.path}")
            print(f"Serving contacts.html from: {html_path}")
            
            # Читаем файл contacts.html
            with open(html_path, 'r', encoding='utf-8') as f:
                html = f.read()
                print(f"Successfully read {len(html)} characters from file")
            
            # Отправляем заголовки и содержимое
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
            print("Successfully sent response to client")
            
        except FileNotFoundError:
            print(f'File not found: {html_path}')
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            error_message = f"""
            <h1>404 Not Found</h1>
            <p>Файл contacts.html не найден.</p>
            <p>Убедитесь, что файл contacts.html находится в той же директории, что и скрипт.</p>
            """
            self.wfile.write(error_message.encode('utf-8'))
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            self.send_response(500)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            error_message = f"""
            <h1>500 Internal Server Error</h1>
            <p>Произошла ошибка при обработке запроса: {str(e)}</p>
            """
            self.wfile.write(error_message.encode('utf-8'))

def run_server():
    """Запуск веб-сервера"""
    server = HTTPServer((HOST, PORT), SimpleHandler)
    print(f'Server starting - serving contacts.html on http://{HOST}:{PORT}')
    print(f'All GET requests will return contacts.html')
    try:
        # Старт веб-сервера в бесконечном цикле прослушивания входящих запросов
        server.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через
        # сочетание клавиш Ctrl + C
        pass
    finally:
        # Корректная остановка веб-сервера
        server.server_close()
        print("\nServer stopped.")

if __name__ == '__main__':
    run_server()