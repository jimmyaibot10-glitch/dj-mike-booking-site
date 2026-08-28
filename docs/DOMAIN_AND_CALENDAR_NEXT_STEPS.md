# Domain, Hosting, Gmail, and Google Calendar Next Steps

## Current site

```text
Live Vercel URL: https://dj-mike-booking-site.vercel.app
GitHub repo: https://github.com/jimmyaibot10-glitch/dj-mike-booking-site
Local folder: E:\Website creations\DJ Mike Booking Site
```

## 1. Connect the domain/hosting he already purchased

The website is already hosted on Vercel. The purchased host/domain needs to point to Vercel.

### Information needed from DJ Mik-E or the host account

- Domain name, for example `djmike...com`.
- Where it was purchased: GoDaddy, Namecheap, Wix, Squarespace, Bluehost, IONOS, etc.
- Login access must be handled by the owner directly; do not send passwords in chat.

### Preferred setup

Use Vercel for hosting and use the purchased provider only for DNS/domain registration.

Steps:

1. In Vercel project settings, add the custom domain.
2. Vercel will show the required DNS records.
3. In the domain registrar/DNS panel, add the records Vercel provides.
4. Wait for DNS propagation.
5. Verify both versions:
   - root domain, for example `djmike...com`
   - `www` domain, for example `www.djmike...com`
6. Set the preferred/canonical domain in Vercel.

### Typical DNS records Vercel requests

Vercel usually asks for records like these, but use the exact values Vercel shows for the domain:

```text
A record      @     76.76.21.21
CNAME record  www   cname.vercel-dns.com
```

Do not guess DNS records at the registrar. Copy the exact Vercel instructions once the domain is added.

## 2. Connect Google Calendar for conflict-free bookings

The booking form should eventually check DJ Mik-E's business Google Calendar before confirming availability.

### Safe initial calendar workflow

1. Website visitor submits a booking inquiry.
2. Request is sent to DJ Mik-E / Chris for review.
3. AI or admin checks Google Calendar availability.
4. If open, DJ Mik-E confirms manually.
5. After confirmation/deposit, the event is added to Google Calendar.

This avoids accidental double-booking while the system is being set up.

### Future automated workflow

1. Booking form captures:
   - event date
   - start time
   - estimated end time or event length
   - location
   - event type
   - contact details
2. Backend checks Google Calendar `freebusy` for conflicts.
3. If open, the site shows `Date appears available — request confirmation`.
4. If booked, the site says `That time may be unavailable — request another date`.
5. No event is added until DJ Mik-E confirms.

### Google setup needed

Hermes currently needs Google OAuth authorization for Gmail + Calendar access.

Required Google APIs:

```text
Gmail API
Google Calendar API
```

Recommended scopes:

```text
Gmail read/modify: read owner update emails and apply processed labels
Calendar read: check availability
Calendar write: only if DJ Mik-E wants approved bookings added automatically later
```

## 3. Recommended implementation phases

### Phase 1 — Safe owner-update inbox

- Set up Google OAuth for the AI-agent Gmail.
- Create Gmail labels.
- Run the local script that turns labeled owner emails into GitHub issues.
- Chris reviews and approves updates manually.

### Phase 2 — Booking form sends real inquiries

- Replace copy-only booking output with a real submission path.
- Low-cost options:
  - Formspree
  - Netlify Forms if switching hosts
  - Vercel serverless function + Gmail send
  - Google Apps Script endpoint

### Phase 3 — Calendar conflict checking

- Add a backend endpoint to check Google Calendar free/busy.
- Show only availability guidance, not final confirmation.
- Add confirmed events to Google Calendar only after approval.

### Phase 4 — Owner dashboard, optional

Build this only after the email workflow works.

Possible features:

- login-protected admin page
- pending booking requests
- calendar availability view
- media upload queue
- site-change request queue

## Immediate blockers

- Need the domain name and registrar/host provider.
- Need Google OAuth setup for the AI-agent Gmail account.
- Need to decide whether booking requests should go to email only first or use a backend from day one.
