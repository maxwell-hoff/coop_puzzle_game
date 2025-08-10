# Cooperative Puzzle Game

A cooperative hex-based puzzle game with a Python Flask backend and SQLite database.

## Features

- **Backend API**: Python Flask server with SQLite database
- **User Authentication**: Register, login, and session management
- **Progress Tracking**: Save puzzle completion status and statistics
- **Cooperative Play**: Team mode for multiple players
- **Chapter Progression**: Unlock new chapters by completing puzzles

## Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the backend**:
   ```bash
   python run.py
   ```
   
   Or directly:
   ```bash
   python app.py
   ```

3. **Open your browser** to `http://localhost:5000`

## Database

The game uses SQLite to store:
- User accounts and authentication
- Puzzle progress and completion status
- Game sessions and move history
- Chapter progression

The database file (`puzzle_game.db`) is automatically created when you first run the application.

## API Endpoints

- `POST /api/register` - User registration
- `POST /api/login` - User authentication
- `GET /api/logout` - User logout
- `GET /api/profile` - User profile and stats
- `GET /api/progress` - Puzzle completion progress
- `POST /api/puzzle/start` - Start a new puzzle session
- `POST /api/puzzle/complete` - Mark puzzle as completed
- `POST /api/puzzle/move` - Record a game move
- `GET /api/chapter/{id}` - Get chapter information
- `POST /api/chapter/{id}/unlock` - Unlock a new chapter

## Game Modes

- **Solo Mode**: Single player puzzle solving
- **Team Mode**: Cooperative play with alternating control
- **Progressive Difficulty**: Unlock new chapters and puzzles

## Development

The backend is built with:
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Flask-Login**: User session management
- **Flask-CORS**: Cross-origin resource sharing

The frontend is a single HTML file with JavaScript that communicates with the backend API.