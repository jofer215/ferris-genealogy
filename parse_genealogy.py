#!/usr/bin/env python3
"""
Parse Ferris genealogy PDFs into SQLite database.
Preserves amateur genealogist's work as-is.
"""

import re
import sqlite3
import subprocess
import sys
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using pdftotext."""
    result = subprocess.run(
        ['pdftotext', str(pdf_path), '-'],
        capture_output=True,
        text=True
    )
    return result.stdout

def parse_entries(text, source_file):
    """Parse genealogy entries from text."""
    entries = []
    
    # Pattern to match entry IDs - must be at start of line followed by name in CAPS
    # This avoids matching stray (2) in middle of paragraphs
    id_pattern = re.compile(r'^\((\d+(?:\.\d+)*)\)\s*([A-Z][A-Z\s]+)', re.MULTILINE)
    
    # Find all entry starts
    matches = list(id_pattern.finditer(text))
    
    for i, match in enumerate(matches):
        entry_id = match.group(1)
        
        # Get entry text (from start of this entry to start of next, or EOF)
        start_pos = match.start()
        end_pos = matches[i+1].start() if i+1 < len(matches) else len(text)
        entry_text = text[start_pos:end_pos].strip()
        
        # Extract first line for name and AFN
        first_line = entry_text.split('\n')[0]
        
        # Remove the ID part
        first_line = re.sub(r'^\(\d+(?:\.\d+)*\)\s*', '', first_line)
        
        # Extract AFN if present
        afn_match = re.search(r'\(AFN:\s*([^)]+)\)', first_line)
        afn = afn_match.group(1) if afn_match else None
        
        # Remove AFN from line
        name_line = re.sub(r'\s*\(AFN:[^)]+\)', '', first_line)
        
        # Extract name - typically ALL CAPS before biographical info
        name_match = re.match(r'([A-Z][A-Za-z\s.,\-\']+?)(?:\s+\((?!AFN)|born|and died|married|\s+\[|$)', name_line + ' born')
        if name_match:
            name = name_match.group(1).strip()
            # Clean up common suffixes
            name = re.sub(r'\s+(Jr|Sr|II|III|IV|Captain|Rev|Dr|Esq)\.?$', '', name)
        else:
            # Fallback
            name = name_line.split('(')[0].strip() if '(' in name_line else name_line.strip()
        
        # Calculate parent_id from hierarchical ID
        id_parts = entry_id.split('.')
        parent_id = '.'.join(id_parts[:-1]) if len(id_parts) > 1 else None
        
        entries.append({
            'id': entry_id,
            'secondary_id': afn,
            'name': name,
            'text': entry_text,
            'parent_id': parent_id,
            'source_file': source_file
        })
    
    return entries

def create_database(db_path):
    """Create SQLite database with schema."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS people (
            id TEXT PRIMARY KEY,
            secondary_id TEXT,
            name TEXT NOT NULL,
            text TEXT,
            parent_id TEXT,
            source_file TEXT NOT NULL,
            FOREIGN KEY (parent_id) REFERENCES people(id)
        );
        
        CREATE INDEX IF NOT EXISTS idx_parent ON people(parent_id);
        CREATE INDEX IF NOT EXISTS idx_secondary ON people(secondary_id);
        CREATE INDEX IF NOT EXISTS idx_name ON people(name);
    ''')
    
    conn.commit()
    return conn

def insert_entries(conn, entries):
    """Insert entries into database."""
    cursor = conn.cursor()
    
    for entry in entries:
        cursor.execute('''
            INSERT OR REPLACE INTO people 
            (id, secondary_id, name, text, parent_id, source_file)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            entry['id'],
            entry['secondary_id'],
            entry['name'],
            entry['text'],
            entry['parent_id'],
            entry['source_file']
        ))
    
    conn.commit()

def main():
    # PDF files to process
    pdf_files = [
        ('JeffreyFerris.pdf', 'Jeffrey'),
        ('JohnFerris.pdf', 'John'),
        ('PeterFerris.pdf', 'Peter'),
        ('JosephFerris.pdf', 'Joseph'),
        ('MaryFerris.pdf', 'Mary'),
        ('JamesFerris.pdf', 'James')
    ]
    
    uploads_dir = Path('/mnt/user-data/uploads')
    db_path = '/home/claude/ferris_genealogy.db'
    
    # Create database
    conn = create_database(db_path)
    
    total_entries = 0
    for pdf_file, source_name in pdf_files:
        pdf_path = uploads_dir / pdf_file
        if not pdf_path.exists():
            print(f"Warning: {pdf_file} not found, skipping")
            continue
        
        print(f"Processing {pdf_file}...")
        text = extract_text_from_pdf(pdf_path)
        entries = parse_entries(text, source_name)
        insert_entries(conn, entries)
        
        print(f"  Extracted {len(entries)} entries")
        total_entries += len(entries)
    
    conn.close()
    
    print(f"\nTotal entries: {total_entries}")
    print(f"Database created: {db_path}")
    
    # Show sample
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, source_file FROM people ORDER BY id LIMIT 10")
    print("\nSample entries:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} ({row[2]})")
    conn.close()

if __name__ == '__main__':
    main()
