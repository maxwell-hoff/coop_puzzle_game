# Setup Guide for Hex Puzzle Game Backend

## Quick Start

1. **Clone and navigate to the project**:
   ```bash
   cd coop_puzzle_game
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**:
   ```bash
   python init_db.py
   ```

5. **Start the server**:
   ```bash
   ./start_server.sh  # On Windows: python run.py
   ```

6. **Open your browser** to `http://localhost:5001`

## What's Been Added

### Backend (Python Flask)
- **`app.py`**: Main Flask application with all API endpoints
- **`requirements.txt`**: Python dependencies
- **`run.py`**: Simple server startup script
- **`init_db.py`**: Database initialization script

### Database (SQLite)
- **User Management**: Registration, login, session handling
- **Progress Tracking**: Puzzle completion status, moves used, hints used
- **Game Sessions**: Track active games and move history
- **Chapter Progression**: Unlock new chapters based on completion

### API Endpoints
- **Authentication**: `/api/register`, `/api/login`, `/api/logout`
- **Progress**: `/api/progress`, `/api/profile`
- **Gameplay**: `/api/puzzle/start`, `/api/puzzle/complete`, `/api/puzzle/move`
- **Chapters**: `/api/chapter/{id}`, `/api/chapter/{id}/unlock`

### Frontend Updates
- **`puzzle_hex_game.html`**: Updated to use backend API instead of local storage
- **Async Operations**: Login, registration, progress saving
- **Session Management**: Persistent user sessions
- **Real-time Progress**: Fetch progress from database

## Testing

Run the API test script to verify everything works:
```bash
source venv/bin/activate
pip install requests  # If not already installed
python test_api.py
```

## Database Schema

The SQLite database (`puzzle_game.db`) contains:

- **`user`**: User accounts and authentication
- **`puzzle_progress`**: Individual puzzle completion status
- **`game_session`**: Active game sessions
- **`game_move`**: Recorded moves for analysis

## File Structure

```
coop_puzzle_game/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── run.py                # Server startup script
├── init_db.py            # Database initialization
├── start_server.sh       # Shell script to start server
├── test_api.py           # API testing script
├── puzzle_game.db        # SQLite database (created automatically)
├── src/
│   └── templates/
│       └── puzzle_hex_game.html  # Updated frontend
├── README.md             # Project overview
└── SETUP.md              # This setup guide
```

## Troubleshooting

### Port Already in Use
If port 5000 is busy:
```bash
lsof -ti:5000 | xargs kill -9
```

### Database Issues
Reset the database:
```bash
rm puzzle_game.db
python init_db.py
```

### Dependencies
If you get import errors:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Next Steps

1. **Customize Puzzles**: Add more puzzles and chapters
2. **Enhance Analytics**: Track more detailed game statistics
3. **Multiplayer**: Add real-time cooperative play
4. **User Profiles**: Add avatars, achievements, leaderboards
5. **Mobile Support**: Optimize for mobile devices 