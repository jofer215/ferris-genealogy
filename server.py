#!/usr/bin/env python3
"""
Flask API server for Ferris genealogy database.
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
from pathlib import Path

app = Flask(__name__)
CORS(app)

DB_PATH = '/home/claude/ferris_genealogy.db'

def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Serve main page."""
    return send_from_directory('/home/claude', 'index.html')

@app.route('/api/person/<path:person_id>')
def get_person(person_id):
    """Get person by ID."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, secondary_id, name, text, parent_id, source_file
        FROM people
        WHERE id = ?
    ''', (person_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return jsonify(dict(row))
    else:
        return jsonify({'error': 'Person not found'}), 404

@app.route('/api/children/<path:parent_id>')
def get_children(parent_id):
    """Get children of a person."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, secondary_id
        FROM people
        WHERE parent_id = ?
        ORDER BY id
    ''', (parent_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in rows])

@app.route('/api/root')
def get_root():
    """Get Jeffrey's children (the 5 root entries)."""
    conn = get_db()
    cursor = conn.cursor()
    # Get entries with ID pattern like '1', '2', '3', '4', '5' (single digit, no dots)
    cursor.execute('''
        SELECT id, name, secondary_id
        FROM people
        WHERE id NOT LIKE '%.%'
        AND CAST(id AS INTEGER) BETWEEN 1 AND 5
        ORDER BY CAST(id AS INTEGER)
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in rows])

@app.route('/api/search/<query>')
def search(query):
    """Search for people by name."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, secondary_id, source_file
        FROM people
        WHERE name LIKE ?
        ORDER BY id
        LIMIT 100
    ''', (f'%{query}%',))
    
    rows = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in rows])

@app.route('/api/stats')
def stats():
    """Get database statistics."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM people')
    total = cursor.fetchone()['total']
    
    cursor.execute('SELECT source_file, COUNT(*) as count FROM people GROUP BY source_file')
    by_source = {row['source_file']: row['count'] for row in cursor.fetchall()}
    
    conn.close()
    
    return jsonify({
        'total_entries': total,
        'by_source': by_source
    })

if __name__ == '__main__':
    print("Starting Ferris Genealogy Server...")
    print(f"Database: {DB_PATH}")
    print("Open http://localhost:5000 in your browser")
    app.run(host='0.0.0.0', port=5000, debug=True)
