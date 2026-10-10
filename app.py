
import os
import time
import html
import mimetypes
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

import mysql.connector
from mysql.connector import Error

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_FILE = BASE_DIR / "templates" / "index.html"
STATIC_DIR = BASE_DIR / "static"

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "database": os.getenv("DB_NAME", "restaurant"),
    "user": os.getenv("DB_USER", "restaurant_user"),
    "password": os.getenv("DB_PASSWORD", ""),
}

SAMPLE_DISHES = [
    ("Margherita Pizza", "Classic pizza with tomato, mozzarella and basil.", 299.00,
     "https://images.unsplash.com/photo-1579751626657-72bc17010498?auto=format&fit=crop&w=700&q=80"),
    ("Creamy Pasta", "Creamy pasta tossed with herbs and fresh vegetables.", 249.00,
     "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=700&q=80"),
    ("Classic Burger", "A juicy burger with fresh lettuce and special sauce.", 199.00,
     "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=700&q=80"),
    ("Chocolate Cake", "Rich chocolate cake for a sweet finish.", 149.00,
     "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=700&q=80"),
]


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def initialize_database():
    """Create the menu table and insert sample dishes if it is empty."""
    for attempt in range(10):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS menu_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description VARCHAR(255) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    image_url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("SELECT COUNT(*) FROM menu_items")
            count = cursor.fetchone()[0]

            if count == 0:
                cursor.executemany("""
                    INSERT INTO menu_items
                        (name, description, price, image_url)
                    VALUES (%s, %s, %s, %s)
                """, SAMPLE_DISHES)

            connection.commit()
            cursor.close()
            connection.close()

            print("MySQL connected. Menu table is ready.")
            return

        except Error as error:
            print(f"MySQL connection attempt {attempt + 1}/10 failed: {error}")
            if attempt < 9:
                time.sleep(3)

    raise RuntimeError("Could not connect to MySQL after 10 attempts.")


def get_menu_items():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id, name, description, price, image_url
            FROM menu_items
            ORDER BY id
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def render_menu_items(items):
    """Convert database rows into HTML cards."""
    cards = []

    for item in items:
        name = html.escape(str(item["name"]))
        description = html.escape(str(item["description"]))
        image_url = html.escape(str(item["image_url"] or ""), quote=True)
        price = float(item["price"])

        cards.append(f"""
            <article class="card">
                <img src="{image_url}" alt="{name}">
                <div class="card-content">
                    <h3>{name}</h3>
                    <p>{description}</p>
                    <div class="price">₹{price:.2f}</div>
                    <button class="btn"
                        onclick="addToCart('{name}', {price})">
                        Add to Cart
                    </button>
                </div>
            </article>
        """)

    return "\n".join(cards)


class RestaurantHandler(BaseHTTPRequestHandler):

    def send_response_body(self, status, content, content_type):
        body = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/":
            try:
                page = TEMPLATE_FILE.read_text(encoding="utf-8")
                menu_items = get_menu_items()
                menu_html = render_menu_items(menu_items)

                if "<!-- MENU_ITEMS -->" not in page:
                    self.send_response_body(
                        500,
                        "Missing <!-- MENU_ITEMS --> placeholder in index.html",
                        "text/plain; charset=utf-8",
                    )
                    return

                page = page.replace("<!-- MENU_ITEMS -->", menu_html)
                self.send_response_body(
                    200, page, "text/html; charset=utf-8"
                )

            except (Error, OSError) as error:
                print(f"Website error: {error}")
                self.send_response_body(
                    500,
                    "Unable to load the restaurant menu. Check application logs.",
                    "text/plain; charset=utf-8",
                )

        elif path.startswith("/static/"):
            relative_path = path.removeprefix("/static/")
            file_path = (STATIC_DIR / relative_path).resolve()

            # Prevent requests from escaping the static directory.
            if not file_path.is_relative_to(STATIC_DIR.resolve()):
                self.send_error(403, "Forbidden")
                return

            if not file_path.is_file():
                self.send_error(404, "File not found")
                return

            content_type = (
                mimetypes.guess_type(str(file_path))[0]
                or "application/octet-stream"
            )

            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(file_path.stat().st_size))
            self.end_headers()

            with file_path.open("rb") as file:
                self.wfile.write(file.read())

        else:
            self.send_error(404, "Page not found")

    def log_message(self, format_string, *args):
        print(f"{self.client_address[0]} - {format_string % args}")


if __name__ == "__main__":
    initialize_database()

    server = HTTPServer(("0.0.0.0", 8000), RestaurantHandler)
    print("Restaurant website running on port 8000")
    server.serve_forever()
