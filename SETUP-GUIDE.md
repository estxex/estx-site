# SETUP GUIDE — estx.exchange hybrid deployment

Everything you need to do, in order. Estimated time: 20 minutes.

---

## STEP 1 — Create the GitHub repo

1. Go to https://github.com/new
2. Repository name: `estx-site` (or whatever you prefer)
3. Set to **Public** (free GitHub Pages + Actions)
4. Do NOT initialize with README (we already have one)
5. Click **Create repository**

---

## STEP 2 — Add GitHub Secrets

Go to your new repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these three secrets one by one:

| Name           | Value                        |
|----------------|------------------------------|
| FTP_SERVER     | ftp.wallstreet-ipo.com       |
| FTP_USERNAME   | upload@estx.exchange         |
| FTP_PASSWORD   | *(your FTP password)*        |

---

## STEP 3 — Push code from your Mac

Open Terminal and run these commands (replace YOUR-GITHUB-USERNAME with `estxex`):

```bash
# Navigate to where you downloaded the project files
cd ~/Downloads/estx-site

# Initialize git and push
git init
git add .
git commit -m "initial site"
git branch -M main
git remote add origin git@github.com:estxex/estx-site.git
git push -u origin main

# Create and push staging branch
git checkout -b staging
git push -u origin staging
```

If you haven't set up SSH keys with GitHub yet, use HTTPS instead:
```bash
git remote add origin https://github.com/estxex/estx-site.git
```

---

## STEP 4 — Create staging subdomain in ChemiCloud cPanel

1. Log into ChemiCloud cPanel (from ChemiCloud dashboard → **Open cPanel**)
2. Find **Subdomains** (under Domains section)
3. Create subdomain:
   - Subdomain: `stage`
   - Domain: `estx.exchange`
   - Document Root will auto-fill (probably `/home/.../stage.estx.exchange`)
4. Click **Create**

Note the document root path — if it's different from `/stage/`, let me know
and I'll update the workflow file.

---

## STEP 5 — Point GoDaddy nameservers to ChemiCloud

1. Find your ChemiCloud nameservers:
   - ChemiCloud dashboard → click your hosting service → look for **Nameservers**
   - Usually looks like: `ns1.chemicloud.com`, `ns2.chemicloud.com`, `ns3.chemicloud.com`

2. Go to https://dcc.godaddy.com → select `estx.exchange`
3. Click **DNS** → scroll to **Nameservers** → click **Change**
4. Select **"I'll use my own nameservers"**
5. Enter the ChemiCloud nameservers from step 1
6. Click **Save**

⚠️  DNS propagation takes 12–24 hours (sometimes up to 48h).
    During this time your site may be intermittently unavailable.

---

## STEP 6 — Verify everything works

After DNS propagates:

```bash
# Check DNS is pointing correctly
dig estx.exchange +short

# Should return your ChemiCloud server IP
```

Then visit:
- https://estx.exchange → should show your production site
- https://stage.estx.exchange → should show your staging site

---

## DAILY WORKFLOW

```bash
# Work on staging
git checkout staging
# ... make changes ...
git add .
git commit -m "description of changes"
git push
# → auto-deploys to stage.estx.exchange

# Review at stage.estx.exchange, then promote to production:
git checkout main
git merge staging
git push
# → auto-deploys to estx.exchange
```

---

## TROUBLESHOOTING

**GitHub Action fails with FTP connection error:**
- Try changing `protocol: ftps` to `protocol: ftp` in deploy.yml
- Verify FTP_PASSWORD secret is correct
- Check if ChemiCloud firewall blocks GitHub's IPs

**Site not loading after nameserver change:**
- Wait full 24–48 hours
- Flush DNS on Mac: `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`
- Test with: `dig estx.exchange`

**Staging subdomain not working:**
- Verify subdomain was created in cPanel
- Check document root matches the workflow's `server-dir`
- The FTP user may need access to the subdomain's directory
