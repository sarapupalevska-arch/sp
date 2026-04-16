# Lovable Display Prompt — humansofaiatwork.lovable.app

**Lovable Editor:** https://lovable.dev/projects/98ffdabe-c611-4db3-9150-f1d8aae6ba72

Paste the prompt below into the Lovable AI chat to build the Q&A story display.

---

## Prompt

```
Build a Q&A interview-style story display. The site should have:

## Homepage (/)
- Hero section with "Humans of AIatWork" title
- Grid of story cards showing all published spotlights
- Fetch from Supabase: spotlight_submissions WHERE status = 'published' ORDER BY published_at DESC

Each card shows:
- Circular photo (or placeholder avatar)
- Full name
- Role, Company
- Industry tag
- "Read their story →" link to /story/[slug]

## Story Page (/story/[slug])
Fetch the submission by slug from spotlight_submissions.

HEADER SECTION:
- Back link "← All Stories" to homepage
- Large circular photo
- Full name (big, bold)
- Role & Company on one line
- Industry as a small muted tag
- Optional: experience_tagline below if present

LAYOUT:
- Left sidebar (sticky): "WHAT WE TALKED ABOUT" with section links
- Right content area: Q&A in chat bubble format

LEFT SIDEBAR SECTIONS:
1. Before AIatWork
2. Experience Inside AIatWork
3. Impact & Transformation
4. Perspective

Clicking a section scrolls to it smoothly.

Q&A CHAT FORMAT:
Each Q&A pair looks like a chat conversation:
- Question: Blue rounded bubble, white text, aligned right, with small AIatWork logo
- Answer: Person's avatar (small, circular) on left, their response text on right

SECTION CONTENT:

**Before AIatWork:**
- Q: "What felt confusing, frustrating, or unclear when you first started exploring AI?" → A: {before_confusion}
- Q: "How were you using AI before joining (if at all)?" → A: {before_ai_usage}
- Q: "What made you decide to join AIatWork specifically?" → A: {why_joined}
- Q: "Was there anything that almost stopped you from joining?" → A: {almost_stopped}

**Experience Inside AIatWork:**
- Q: "What surprised you the most after joining?" → A: {biggest_surprise}
- Q: "What part of AIatWork do you find most useful or enjoyable, and why?" → A: {most_useful_part}
- Q: "Most impactful session, mentor, or moment so far:" → A: {most_impactful_moment}
- Q: "How is AIatWork different from other ways you've tried to learn AI?" → A: {how_different}

**Impact & Transformation:**
- Q: "What can you do in your work today that you couldn't do before joining AIatWork?" → A: {new_capabilities}
- Q: "Have you seen any measurable results from using AI in your work?" → A: {measurable_results}
- Q: "Can you share a specific example where you applied something you learned?" → A: {specific_example}
(If example_file_urls exists, show the images/files below this answer)

**Perspective:**
- Q: "Do you see yourself differently when it comes to AI compared to before?" → A: {self_perception}
- Q: "Have colleagues, clients, or people around you noticed a difference in how you work?" → A: {external_feedback}
- Q: "What would you say to someone who is still waiting instead of joining AIatWork?" → A: {advice_to_others}

STYLING:
- Question bubbles: bg-blue-600 text-white rounded-2xl px-5 py-3, shadow-sm
- Answer text: text-gray-800 dark:text-gray-200, good line-height
- Section headers: uppercase, text-xs, text-gray-400, tracking-wide, mb-6
- Mobile: Stack layout vertically, hide sticky sidebar

Handle 404 if slug not found or status is not 'published'.
```
