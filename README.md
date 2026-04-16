# AIatWork Learner Spotlight System

A fully autonomous "Humans of AIatWork" spotlight pipeline. A learner fills out
a form once — everything else (publishing, Slack notification, social copy)
happens automatically with zero manual intervention.

---

## Architecture

```
spotlight.aiatwork.ai          humansofaiatwork.lovable.app
      │                                      ▲
      │  INSERT                              │ SELECT (published)
      ▼                                      │
┌─────────────────────────────────────────────────────┐
│                    SUPABASE                         │
│  spotlight_submissions table                        │
│  spotlight-uploads storage bucket                   │
└─────────────────┬───────────────────────────────────┘
                  │ Database Webhook (on INSERT)
                  ▼
        supabase/functions/on-spotlight-submit
                  │
          ┌───────┴────────┐
          ▼                ▼
       Slack           Claude API
    notification     social summary
```

---

## Repository Structure

```
supabase/
  migrations/
    001_create_spotlight_submissions.sql   # Full DB schema, triggers, RLS, storage
  functions/
    on-spotlight-submit/
      index.ts                            # Edge Function: Slack + Claude social copy

docs/
  lovable-form-prompt.md    # Paste into Lovable project 1 (spotlight form)
  lovable-display-prompt.md # Paste into Lovable project 2 (story display)
```

---

## Setup Instructions

### 1. Supabase Database

1. Open your Supabase project's **SQL Editor**.
2. Run the contents of `supabase/migrations/001_create_spotlight_submissions.sql`.
3. This creates:
   - `spotlight_submissions` table with all fields
   - `generate_spotlight_slug` trigger (auto-creates URL slugs like `goran-trajkovski`)
   - `auto_publish_spotlight` trigger (sets `published_at` on insert)
   - Row Level Security policies (public insert + read, service role full access)
   - `spotlight-uploads` storage bucket (public read/write)

### 2. Spotlight Form — spotlight.aiatwork.ai

1. Open the Lovable editor: https://lovable.dev/projects/9034d8ed-55e3-4209-b42a-57ad3d59c4ee
2. Paste the prompt from `docs/lovable-form-prompt.md` into the AI chat.
3. Lovable will wire all 6 form steps to the `spotlight_submissions` table and
   configure file uploads to the `spotlight-uploads` bucket.

### 3. Story Display — humansofaiatwork.lovable.app

1. Open the Lovable editor: https://lovable.dev/projects/98ffdabe-c611-4db3-9150-f1d8aae6ba72
2. Paste the prompt from `docs/lovable-display-prompt.md` into the AI chat.
3. Lovable will build:
   - A homepage grid of all published story cards
   - Individual story pages at `/story/[slug]` in Q&A chat-bubble format
   - A sticky sidebar with section navigation

Both Lovable projects must point to the **same Supabase project**.

### 4. Edge Function (Slack + Social Copy)

Deploy `supabase/functions/on-spotlight-submit/index.ts`:

```bash
supabase functions deploy on-spotlight-submit
```

Set environment variables in **Supabase → Edge Functions → Secrets**:

| Variable | Value |
|---|---|
| `SLACK_WEBHOOK_URL` | `https://hooks.slack.com/services/YOUR/WEBHOOK/URL` |
| `ANTHROPIC_API_KEY` | `sk-ant-…` |
| `SUPABASE_URL` | `https://your-project.supabase.co` |
| `SUPABASE_SERVICE_ROLE_KEY` | `eyJ…` |

Then create a **Database Webhook** in Supabase → Database → Webhooks:

- **Name:** `on-spotlight-submit`
- **Table:** `spotlight_submissions`
- **Events:** INSERT
- **URL:** `https://your-project.supabase.co/functions/v1/on-spotlight-submit`

---

## Data Flow (End to End)

1. Learner visits **spotlight.aiatwork.ai**, fills out the 6-step form, clicks Submit.
2. Form uploads photos/files to the `spotlight-uploads` storage bucket and inserts
   a row into `spotlight_submissions` with `status = 'published'`.
3. The `set_spotlight_slug` trigger auto-generates a URL-friendly slug from the
   learner's name (e.g. `goran-trajkovski`).
4. The Database Webhook fires the `on-spotlight-submit` Edge Function, which:
   - Posts a Slack message to `#spotlight-new` with a direct link to the story.
   - Calls the Claude API to generate a LinkedIn-ready social summary and saves
     it back to the `social_summary` column.
5. **humansofaiatwork.lovable.app** fetches all `published` rows and displays the
   new story immediately — no manual approval required.

---

## Checklist

- [ ] Both Lovable projects connected to the same Supabase project
- [ ] `spotlight_submissions` table created (run migration SQL)
- [ ] `spotlight-uploads` storage bucket created and public
- [ ] Form at spotlight.aiatwork.ai submits all fields correctly
- [ ] Stories appear at humansofaiatwork.lovable.app automatically
- [ ] Slugs auto-generated (e.g. `/story/goran-trajkovski`)
- [ ] Q&A displayed in chat-bubble format
- [ ] (Optional) Slack notifications working
- [ ] (Optional) Claude social summary generated on each submission
