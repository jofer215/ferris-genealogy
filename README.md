# Ferris Family Genealogy Database

## Credit

This genealogical research was compiled by **James G. Ferris** and originally published at ferristree.com (now offline). 

From the original site:
> "Bombs and Bones is a compilation of information from printed and individual sources and presented to you by James G. Ferris. No attempt's have been made to verify the information within this website. All sources are listed at the end of each chapter."

The original site has been archived at: https://sites.google.com/view/ferris-tree/

**All credit for this genealogical research goes to James G. Ferris.** This database is simply a reorganization of his work into a browsable format.

## Contents

- **ferris_genealogy.db** - SQLite database with 56,322 entries
- **index.html** - Web interface for browsing
- **server.py** - Flask API server
- **parse_genealogy.py** - Parser (for reference/rebuilding)

## Database Structure

```sql
CREATE TABLE people (
    id TEXT PRIMARY KEY,              -- Hierarchical: '3.1.1.2.5'
    secondary_id TEXT,                -- AFN or other IDs
    name TEXT NOT NULL,               -- Full name as written
    text TEXT,                        -- Complete biographical entry
    parent_id TEXT,                   -- Parent's ID
    source_file TEXT NOT NULL         -- Source PDF
);
```

## Quick Start

1. Install dependencies:
   ```bash
   pip install flask flask-cors
   ```

2. Run the server:
   ```bash
   python3 server.py
   ```

3. Open browser to: http://localhost:5000

## Database Stats

Total Entries: 56,322

By Source File:
- Joseph (3): 17,252 entries
- John (1): 12,459 entries  
- Peter (2): 10,966 entries
- James (5): 10,156 entries
- Mary (4): 5,460 entries
- Jeffrey (root): 2 entries

## Jeffrey's Five Children

1. John Ferris
2. Peter Ferris
3. Joseph Ferris
4. Mary Ferris
5. James Ferris

## Usage

### Browse by clicking through descendants
- Start at root (Jeffrey's children)
- Click any person to view details
- Children are listed at bottom
- Breadcrumb trail shows path

### Direct queries (Python)
```python
import sqlite3
conn = sqlite3.connect('ferris_genealogy.db')
cursor = conn.cursor()

# Get person by ID
cursor.execute("SELECT * FROM people WHERE id = '3.1.1'")

# Get all children
cursor.execute("SELECT * FROM people WHERE parent_id = '3.1'")

# Search by name
cursor.execute("SELECT * FROM people WHERE name LIKE '%FERRIS%'")
```

## Notes

- Data preserved as-is from original PDFs
- Contains uncertainties, conflicts, and speculation noted by researcher
- Read-only database - browse, don't edit
- See original PDFs for complete context
