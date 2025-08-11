#!/usr/bin/env python3
"""
Database initialization script for the Hex Puzzle Game
"""
from app import app, db

def init_database():
    """Initialize the database with tables"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        print("Database file: puzzle_game.db")

if __name__ == '__main__':
    init_database() 