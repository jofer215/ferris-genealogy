# Deploy Ferris Genealogy to GitHub Pages

## What You Have

**ferris_genealogy_spa.tar.gz** (4.7MB compressed, 23MB uncompressed)

Contains just **2 files**:
- `index.html` - Single-page web app
- `data.json` - All 56,211 people

No database, no server, no 56,000 files. Just 2 files that work anywhere.

## GitHub Pages Deployment (5 minutes, FREE forever)

### Step 1: Extract files
```bash
tar -xzf ferris_genealogy_spa.tar.gz
cd spa_site
```

You'll see: `index.html`, `data.json`, `README.md`

### Step 2: Create GitHub repository

1. Go to https://github.com/new
2. Repository name: `ferris-genealogy` (or anything)
3. Make it **Public** (required for free GitHub Pages)
4. Click "Create repository"

### Step 3: Upload files

**Option A: Drag and Drop (easiest)**
1. On your new repo page, click "uploading an existing file"
2. Drag `index.html` and `data.json` into the browser
3. Scroll down, click "Commit changes"

**Option B: Command Line**
```bash
cd spa_site
git init
git add index.html data.json README.md
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ferris-genealogy.git
git push -u origin main
```

### Step 4: Enable GitHub Pages

1. In your repo, click **Settings** (top right)
2. Click **Pages** in left sidebar
3. Under "Source": Select **Deploy from a branch**
4. Branch: Select **main** and **/ (root)**
5. Click **Save**

### Step 5: Wait ~2 minutes

GitHub will build your site. Refresh the Pages settings page to see:

**Your site is live at: `https://yourusername.github.io/ferris-genealogy/`**

## That's It!

Your genealogy site is now:
- ✅ Live on the internet
- ✅ Free forever
- ✅ Fast and searchable
- ✅ No maintenance needed

## Even Easier Alternatives

**Netlify** (30 seconds):
1. Go to https://app.netlify.com/drop
2. Drag the `spa_site` folder onto the page
3. Done - instant URL

**Cloudflare Pages** (similar):
1. Sign up at pages.cloudflare.com
2. Upload folder
3. Done

## Notes

- GitHub Pages has 1GB size limit (you're using 23MB - plenty of room)
- 100GB bandwidth/month free (more than enough)
- Site loads instantly - all data downloads once, then cached

## Custom Domain (Optional)

Want `ferris.yourdomain.com` instead of GitHub's URL?

1. Buy domain ($8-12/year from Namecheap)
2. In GitHub Pages settings, add custom domain
3. Update DNS records (GitHub shows you how)

## Troubleshooting

**Site shows 404**: Wait 2-3 minutes after enabling Pages, then refresh

**Search not working**: Make sure `data.json` was uploaded

**Blank page**: Check browser console (F12) for errors - usually means `data.json` is missing

## File Size Concerns?

If 23MB `data.json` seems large:
- It loads once per session
- Cached by browser after first visit
- Typical webpage with images is 3-5MB
- This is 56,000 people in one file - very efficient

Most users on WiFi/4G won't notice. Mobile users see "Loading..." for 2-3 seconds max.
