# estx.exchange

## Deployment

- **Production:** Push to `main` → auto-deploys to `estx.exchange`
- **Staging:** Push to `staging` → auto-deploys to `stage.estx.exchange`

Deployments are handled by GitHub Actions via FTP to ChemiCloud.

## Workflow

```
staging branch → push → stage.estx.exchange (review here)
    ↓ merge
main branch    → push → estx.exchange (live site)
```

## Setup Checklist

- [ ] GitHub Secrets configured (FTP_SERVER, FTP_USERNAME, FTP_PASSWORD)
- [ ] GoDaddy nameservers pointed to ChemiCloud
- [ ] Subdomain `stage.estx.exchange` created in cPanel
- [ ] DNS propagated (up to 24h)
