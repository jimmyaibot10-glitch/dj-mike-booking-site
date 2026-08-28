# DJ Mik-E Owner Update Workflow

This workflow lets DJ Mik-E request website updates by email while keeping production safe.

## Goal

Use the AI-agent Gmail account as the intake mailbox for website-owner requests, then turn approved requests into GitHub/Vercel updates.

## Recommended flow

1. DJ Mik-E emails the AI-agent Gmail account.
2. The email subject starts with one of these prefixes:
   - `SITE UPDATE:` for copy, photos, pricing, event-type, or contact changes.
   - `MEDIA UPDATE:` for new photo/video requests.
   - `URGENT SITE UPDATE:` for time-sensitive corrections.
3. Hermes/Gmail automation reads only messages with the configured Gmail label or matching subject prefix.
4. The automation creates a GitHub issue in `jimmyaibot10-glitch/dj-mike-booking-site` with:
   - sender
   - subject
   - requested change
   - affected site section
   - attachments/media note if applicable
   - approval checklist
5. Chris reviews the issue before any website file changes are made.
6. Approved work is committed to GitHub.
7. Vercel deploys the GitHub update automatically.
8. The live site is verified after deploy.

## Safety rules

- Email requests should never push directly to production without human review.
- The automation creates reviewable GitHub issues, not direct commits.
- Secrets, passwords, Gmail tokens, Google OAuth files, Vercel tokens, and GitHub tokens stay local and must not be committed.
- Media should be curated before upload; do not blindly publish every attachment.
- Client-facing site copy must not mention demos, templates, internal workflow, or AI automation.

## Suggested Gmail labels

Create these labels in the AI-agent Gmail account:

```text
DJMIKE_SITE_UPDATES
DJMIKE_BOOKING_REQUESTS
DJMIKE_PROCESSED
DJMIKE_NEEDS_REVIEW
```

## Suggested email format for DJ Mik-E

```text
Subject: SITE UPDATE: <short description>

What should change:

Where it should appear:

Exact wording, if you have it:

Photos/videos attached or linked:

Deadline / urgency:
```

## Approval checklist

Before committing a change:

- [ ] Request came from the real owner or an approved contact.
- [ ] Change is clear enough to implement.
- [ ] No private information or unapproved pricing is being exposed.
- [ ] Media is professional enough for the site.
- [ ] Local files were updated and checked.
- [ ] Live deployment was verified after push.
