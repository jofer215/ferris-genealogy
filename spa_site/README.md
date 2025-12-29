# Ferris Family Genealogy - Single-Page App

## Credit

This genealogical research was compiled by **James G. Ferris** and originally published at ferristree.com (now offline). 

From the original site:
> "Bombs and Bones is a compilation of information from printed and individual sources and presented to you by James G. Ferris. No attempt's have been made to verify the information within this website. All sources are listed at the end of each chapter."

The original site has been archived at: https://sites.google.com/view/ferris-tree/

**All credit for this genealogical research goes to James G. Ferris.** This database is simply a reorganization of his work into a browsable format.

## What's This?

A single-page web application containing 56,211 genealogy entries.

**Just 2 files:**
- `index.html` - The web interface
- `data.json` - All 56,211 people (22.5MB)

## Deploy to GitHub Pages

1. Create new repo at https://github.com/new
2. Upload both files (index.html + data.json)
3. Settings → Pages → Enable from main branch
4. Done! Your site will be live at: `https://yourusername.github.io/reponame/`

## Features

- Browse by clicking through descendants
- Search by name (top of page)
- Breadcrumb navigation
- No server needed - runs entirely in browser
- Works on any static hosting

## Local Testing

```bash
python3 -m http.server 8000
```
Open http://localhost:8000

## Alternative Hosts

- **Netlify**: Drag folder onto netlify.com
- **Cloudflare Pages**: Upload to pages.cloudflare.com
- **Vercel**: `vercel` command
- **GitHub Pages**: (instructions above)

All are free.
