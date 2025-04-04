# URL Shortener

A URL shortening service built with FastAPI that allows you to create and manage shortened URLs.

This project is under active development, with some planned features still in progress.

## Features

- **URL Shortening**: Create short URLs from long ones
- **URL Redirection**: Automatic redirection from short URLs to original destinations
- **Basic Management**: Create and use shortened URLs

### Planned Features
- Analytics for tracking clicks and statistics
- User authentication system
- Web UI for easier interaction
- Update and delete functionality for URLs

## Getting Started

### Prerequisites

- Python 3.8+
- SQLite (default) or other database supported by SQLAlchemy

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nevil-ing/url_shortener.git
   cd url_shortener
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Server

```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

### API Documentation

Once the server is running, you can access the interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint (health check) |
| `/url` | POST | Create a new short URL |
| `/{url_key}` | GET | Redirect to original URL |

#### Example: Creating a Short URL

```bash
curl -X POST "http://localhost:8000/url" \
  -H "Content-Type: application/json" \
  -d '{"target_url": "https://example.com/very/long/url"}'
```

Response:
```json
{
  "target_url": "https://example.com/very/long/url",
  "is_active": true,
  "clicks": 0,
  "url": "http://localhost:8000/example"
}
```

#### Using Short URLs

Simply navigate to the generated short URL in a browser, or use:

```bash
curl -L "http://localhost:8000/example"
```



## Contributing

Contributions are welcome! Feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the GNU General Public License. See the [LICENSE](LICENSE) file for details.
