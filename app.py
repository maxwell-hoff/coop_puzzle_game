from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///puzzle_game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Game progress
    current_chapter = db.Column(db.Integer, default=1)
    puzzles_completed = db.relationship('PuzzleProgress', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class PuzzleProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    puzzle_id = db.Column(db.String(50), nullable=False)
    chapter = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    moves_used = db.Column(db.Integer)
    hints_used = db.Column(db.Integer)
    team_mode = db.Column(db.Boolean, default=False)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'puzzle_id'),)

class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    puzzle_id = db.Column(db.String(50), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    moves = db.relationship('GameMove', backref='session', lazy=True, cascade='all, delete-orphan')

class GameMove(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('game_session.id'), nullable=False)
    move_number = db.Column(db.Integer, nullable=False)
    move_data = db.Column(db.Text, nullable=False)  # JSON string of move data
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('puzzle_hex_game.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully', 'user_id': user.id})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        user.last_login = datetime.utcnow()
        db.session.commit()
        return jsonify({
            'message': 'Login successful',
            'user_id': user.id,
            'username': user.username,
            'current_chapter': user.current_chapter
        })
    
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})

@app.route('/api/profile')
@login_required
def profile():
    user = current_user
    completed_puzzles = PuzzleProgress.query.filter_by(user_id=user.id, completed=True).count()
    total_puzzles = PuzzleProgress.query.filter_by(user_id=user.id).count()
    
    return jsonify({
        'username': user.username,
        'current_chapter': user.current_chapter,
        'puzzles_completed': completed_puzzles,
        'total_puzzles': total_puzzles,
        'created_at': user.created_at.isoformat(),
        'last_login': user.last_login.isoformat() if user.last_login else None
    })

@app.route('/api/progress')
@login_required
def get_progress():
    user = current_user
    progress = PuzzleProgress.query.filter_by(user_id=user.id).all()
    
    progress_data = {}
    for p in progress:
        if p.chapter not in progress_data:
            progress_data[p.chapter] = []
        progress_data[p.chapter].append({
            'puzzle_id': p.puzzle_id,
            'completed': p.completed,
            'completed_at': p.completed_at.isoformat() if p.completed_at else None,
            'moves_used': p.moves_used,
            'hints_used': p.hints_used,
            'team_mode': p.team_mode
        })
    
    return jsonify(progress_data)

@app.route('/api/puzzle/start', methods=['POST'])
@login_required
def start_puzzle():
    data = request.get_json()
    puzzle_id = data.get('puzzle_id')
    chapter = data.get('chapter', 1)
    
    # Create or get existing progress
    progress = PuzzleProgress.query.filter_by(
        user_id=current_user.id, 
        puzzle_id=puzzle_id
    ).first()
    
    if not progress:
        progress = PuzzleProgress(
            user_id=current_user.id,
            puzzle_id=puzzle_id,
            chapter=chapter
        )
        db.session.add(progress)
    
    # Create new game session
    session = GameSession(
        user_id=current_user.id,
        puzzle_id=puzzle_id
    )
    db.session.add(session)
    db.session.commit()
    
    return jsonify({
        'session_id': session.id,
        'puzzle_id': puzzle_id,
        'chapter': chapter
    })

@app.route('/api/puzzle/complete', methods=['POST'])
@login_required
def complete_puzzle():
    data = request.get_json()
    session_id = data.get('session_id')
    puzzle_id = data.get('puzzle_id')
    moves_used = data.get('moves_used', 0)
    hints_used = data.get('hints_used', 0)
    team_mode = data.get('team_mode', False)
    
    # Update progress
    progress = PuzzleProgress.query.filter_by(
        user_id=current_user.id, 
        puzzle_id=puzzle_id
    ).first()
    
    if progress:
        progress.completed = True
        progress.completed_at = datetime.utcnow()
        progress.moves_used = moves_used
        progress.hints_used = hints_used
        progress.team_mode = team_mode
    
    # Close session
    session = GameSession.query.get(session_id)
    if session and session.user_id == current_user.id:
        session.completed_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'message': 'Puzzle completed successfully'})

@app.route('/api/puzzle/move', methods=['POST'])
@login_required
def record_move():
    data = request.get_json()
    session_id = data.get('session_id')
    move_number = data.get('move_number')
    move_data = data.get('move_data')
    
    session = GameSession.query.get(session_id)
    if not session or session.user_id != current_user.id:
        return jsonify({'error': 'Invalid session'}), 400
    
    move = GameMove(
        session_id=session_id,
        move_number=move_number,
        move_data=move_data
    )
    db.session.add(move)
    db.session.commit()
    
    return jsonify({'message': 'Move recorded successfully'})

@app.route('/api/chapter/<int:chapter_id>')
@login_required
def get_chapter_info(chapter_id):
    # This would contain chapter metadata, story text, etc.
    # For now, returning basic structure
    chapters = {
        1: {
            'title': 'The Whispering Vale',
            'description': 'Begin your journey in the mystical valley...',
            'puzzles': ['puzzle_1', 'puzzle_2', 'puzzle_3']
        },
        2: {
            'title': 'The Crystal Caves',
            'description': 'Deeper into the mountain...',
            'puzzles': ['puzzle_4', 'puzzle_5', 'puzzle_6']
        }
    }
    
    if chapter_id not in chapters:
        return jsonify({'error': 'Chapter not found'}), 404
    
    return jsonify(chapters[chapter_id])

@app.route('/api/chapter/<int:chapter_id>/unlock', methods=['POST'])
@login_required
def unlock_chapter(chapter_id):
    # Check if previous chapter is completed
    if chapter_id > 1:
        prev_chapter = chapter_id - 1
        prev_puzzles = PuzzleProgress.query.filter_by(
            user_id=current_user.id, 
            chapter=prev_chapter
        ).all()
        
        if not all(p.completed for p in prev_puzzles):
            return jsonify({'error': 'Previous chapter not completed'}), 400
    
    current_user.current_chapter = chapter_id
    db.session.commit()
    
    return jsonify({'message': f'Chapter {chapter_id} unlocked'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001) 