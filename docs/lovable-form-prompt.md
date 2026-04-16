# Lovable Form Prompt — spotlight.aiatwork.ai

**Lovable Editor:** https://lovable.dev/projects/9034d8ed-55e3-4209-b42a-57ad3d59c4ee

Paste the prompt below into the Lovable AI chat to wire up all 6 form steps to Supabase.

---

## Prompt

```
Update the spotlight form to submit all data to Supabase. The form has 6 steps and should save to the `spotlight_submissions` table.

STEP 1 - About You:
- full_name (required)
- email (required)
- current_status (dropdown: "Working professional", "Student", "Career changer", "Entrepreneur", "Other")
- role (text input, placeholder: "e.g. Head of Partnerships")
- industry (text input, placeholder: "e.g. Technology, Education, Finance")
- company (text input)
- photo_url (file upload to Supabase Storage bucket "spotlight-uploads", save public URL)

STEP 2 - Before AIatWork:
- before_confusion: "What felt confusing, frustrating, or unclear when you first started exploring AI?" (textarea, required)
- before_ai_usage: "How were you using AI before joining (if at all)?" (textarea, required)
- why_joined: "What made you decide to join AIatWork specifically?" (textarea, required)
- almost_stopped: "Was there anything that almost stopped you from joining?" (textarea, required)

STEP 3 - Your Experience Inside AIatWork:
- biggest_surprise: "What surprised you the most after joining? Did anything turn out differently than you expected? Tell us the story." (textarea, required)
- most_useful_part: "What part of AIatWork do you find most useful or enjoyable, and why? Sessions, tools, models, academies, quizzes/challenges, etc." (textarea, required)
- most_impactful_moment: "Most impactful session, mentor, or moment so far: What made it stand out?" (textarea, required)
- how_different: "How is AIatWork different from other ways you've tried to learn AI?" (textarea, required)

STEP 4 - What Changed:
- new_capabilities: "What can you do in your work today that you couldn't do before joining AIatWork?" (textarea, required)
- measurable_results: "Have you seen any measurable results from using AI in your work? Time saved, revenue impact, fewer errors, faster delivery, etc." (textarea, required)
- specific_example: "Can you share a specific example where you applied something you learned?" (textarea, required)
- example_file_urls: "Upload files (screenshots, images, docs)" (multi-file upload to Supabase Storage bucket "spotlight-uploads", save URLs as array)

STEP 5 - Final Thoughts:
- self_perception: "Do you see yourself differently when it comes to AI compared to before?" (textarea, required)
- external_feedback: "Have colleagues, clients, or people around you noticed a difference in how you work? If yes, what changed?" (textarea, required)
- advice_to_others: "What would you say to someone who is still waiting instead of joining AIatWork?" (textarea, required)
- consent_given: Checkbox "I agree that AIatWork can use my responses, name, and submitted materials for content and promotional purposes." (required, must be checked to proceed)

STEP 6 - Thank You:
Show the existing thank you message after successful submission.

On submit:
1. Upload any files to Supabase Storage bucket "spotlight-uploads"
2. Insert all data into spotlight_submissions table
3. Set status to "published" and consent_given to true
4. Show success/thank you screen

Make sure the form uses the existing Supabase connection and the exact field names specified above.
```
