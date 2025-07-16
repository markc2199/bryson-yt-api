# Bryson Latest YouTube Video Updater

A Flask web service that automatically fetches the latest video from Bryson DeChambeau's YouTube channel and updates a Home Assistant entity with the video URL.

## Features

- �� Fetches the latest video from Bryson DeChambeau's YouTube channel
- 🏠 Updates Home Assistant entity state with the video URL
- 🌐 RESTful API endpoint for triggering updates

## Prerequisites

- Python 3.7+
- Home Assistant instance with API access
- YouTube channel ID (currently set to Bryson DeChambeau's channel)

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd bryson-yt
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment configuration**
   Create a `.env` file in the project root:
   ```env
   HA_URL=http://your-home-assistant-url:8123
   HA_TOKEN=your_long_lived_access_token
   ENTITY_ID=sensor.bryson_latest_video
   ```

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `HA_URL` | Your Home Assistant instance URL | `http://192.168.1.100:8123` |
| `HA_TOKEN` | Long-lived access token from Home Assistant | `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...` |
| `ENTITY_ID` | Home Assistant entity to update | `sensor.bryson_latest_video` |

### Getting Home Assistant Token

1. Go to your Home Assistant profile page
2. Scroll down to "Long-Lived Access Tokens"
3. Create a new token
4. Copy the token to your `.env` file

## Usage

### Running the Application

```bash
python app.py
```

The server will start on `http://0.0.0.0:5001`

### API Endpoints

#### Update Bryson Video
- **URL**: `/update_bryson`
- **Method**: `POST`
- **Description**: Fetches the latest video and updates Home Assistant

**Example Request:**
```bash
curl -X POST http://localhost:5001/update_bryson
```

**Example Response:**
```json
{
  "success": true,
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

### Home Assistant Integration

The app updates a Home Assistant entity with the latest video URL. You can:

1. **Create an automation** to call the API endpoint periodically
2. **Use the entity state** in your Home Assistant dashboard
3. **Trigger updates** manually via the API

**Example Home Assistant automation:**
```yaml
automation:
  - alias: "Update Bryson Video Daily"
    trigger:
      platform: time
      at: "09:00:00"
    action:
      service: rest_command.update_bryson_video

rest_command:
  update_bryson_video:
    url: "http://localhost:5001/update_bryson"
    method: POST
```

## Project Structure

```
bryson-yt/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in git)
├── .gitignore         # Git ignore rules
├── venv/              # Virtual environment (not in git)
└── README.md          # This file
```

## Development

### Adding New Channels

To track a different YouTube channel, modify the `CHANNEL_ID` variable in `app.py`:

```python
CHANNEL_ID = "NEW_CHANNEL_ID_HERE"
```

### Error Handling

The application includes error handling for:
- Network connectivity issues
- Invalid YouTube RSS feeds
- Home Assistant API errors
- Missing environment variables

## Troubleshooting

### Common Issues

1. **"Missing environment variables" error**
   - Ensure your `.env` file exists and contains all required variables

2. **"Failed to fetch or parse YouTube RSS feed" error**
   - Check your internet connection
   - Verify the channel ID is correct

3. **"Failed to update Home Assistant" error**
   - Verify your HA_URL and HA_TOKEN are correct
   - Ensure Home Assistant is accessible from your network

### Logs

The application prints status messages to the console. Check the output for detailed error information.
