# DJ Mike Booking Site

Status: `prototype`

Apple/liquid-glass inspired personal DJ booking website for **DJ Mike**.

## Main file

```text
index.html
```

Open locally:

```text
E:\Website creations\DJ Mike Booking Site\index.html
```

## Project goal

Build a clean landing page that helps people quickly decide whether to book DJ Mike for an event.

Primary website jobs:

1. Showcase DJ Mike as a polished event DJ.
2. Display videos and event photos.
3. Explain event types and pricing tiers.
4. Let visitors request/reserve a date.
5. Keep content easy to swap later once real photos/videos are available.

## Design direction

Requested style:

- Apple-inspired layout and typography.
- Liquid glass theme.
- Streamlined, premium UI.
- Icons/cards with clean event categories.
- Media-forward layout.

Implemented as:

- translucent sticky nav with blur.
- cinematic hero section.
- glassmorphism cards.
- blue/violet lighting accents.
- original generated placeholder images.
- mobile-responsive sections.

## Generated images

The placeholder images were generated for this project and copied into:

```text
assets/images/generated/dj-mike-hero.png
assets/images/generated/liquid-glass-dj-icon.png
```

These are original generated placeholders and can be replaced later with real DJ/event photography.

## Media directories

Add future content here:

```text
assets/photos/
assets/videos/
```

Recommended photo types:

```text
.jpg
.png
.webp
```

Recommended video types:

```text
.mp4
.webm
```

For social/YouTube content, replace the current video placeholder cards in `index.html` with embeds.

## Booking flow

The current booking form is frontend-only.

It collects:

- name
- phone/email
- event type
- event date
- start time
- location/town
- event details

On submit it creates a booking inquiry summary and saves the last 20 inquiries to browser `localStorage` under:

```text
dj_mike_booking_inquiries
```

## Event tiers

Current placeholder tiers:

| Event type | Pricing expectation |
|---|---|
| Backyard / house party | Starter / lower-budget |
| Birthday / private party | Standard |
| Wedding | Premium |
| Corporate / formal | Custom quote |

Actual prices still need to be chosen by DJ Mike.

## Next steps

- Replace placeholder visuals with DJ Mike’s real photos.
- Add real video embeds or local clips.
- Choose actual pricing ranges.
- Add social links.
- Add contact email/phone.
- Decide scheduler integration:
  - Calendly
  - TidyCal
  - Google Calendar appointment schedule
  - simple email form endpoint
  - custom backend

## Files

```text
index.html
assets/styles.css
assets/scripts.js
assets/images/generated/
assets/photos/
assets/videos/
docs/
archive/
```
