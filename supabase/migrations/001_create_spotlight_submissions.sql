-- ============================================
-- SPOTLIGHT SUBMISSIONS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS spotlight_submissions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- ============================================
    -- STEP 1: About You
    -- ============================================
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    current_status TEXT,           -- "Working professional", "Student", etc.
    role TEXT,                     -- "Head of Partnerships"
    industry TEXT,                 -- "Technology", "Education", "Finance"
    company TEXT,
    photo_url TEXT,                -- URL from Supabase Storage

    -- Additional profile info (for display)
    experience_tagline TEXT,       -- e.g., "PhD, 30+ years in AI research"
    linkedin_url TEXT,

    -- ============================================
    -- STEP 2: Before AIatWork
    -- ============================================
    before_confusion TEXT,
    before_ai_usage TEXT,
    why_joined TEXT,
    almost_stopped TEXT,

    -- ============================================
    -- STEP 3: Experience Inside AIatWork
    -- ============================================
    biggest_surprise TEXT,
    most_useful_part TEXT,
    most_impactful_moment TEXT,
    how_different TEXT,

    -- ============================================
    -- STEP 4: What Changed (Impact & Transformation)
    -- ============================================
    new_capabilities TEXT,
    measurable_results TEXT,
    specific_example TEXT,
    example_file_urls TEXT[],      -- Array of uploaded file URLs

    -- ============================================
    -- STEP 5: Final Thoughts (Perspective)
    -- ============================================
    self_perception TEXT,
    external_feedback TEXT,
    advice_to_others TEXT,

    -- ============================================
    -- Consent & Publishing
    -- ============================================
    consent_given BOOLEAN DEFAULT false,
    status TEXT DEFAULT 'published' CHECK (status IN ('pending', 'published', 'rejected')),
    -- NOTE: Default is 'published' for full automation.
    -- Change to 'pending' if you want manual approval before stories go live.

    published_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    slug TEXT UNIQUE,

    -- ============================================
    -- Auto-generated content (by Claude API)
    -- ============================================
    social_summary TEXT,
    social_summary_generated_at TIMESTAMP WITH TIME ZONE
);

-- ============================================
-- AUTO-GENERATE URL SLUG FROM NAME
-- ============================================
CREATE OR REPLACE FUNCTION generate_spotlight_slug()
RETURNS TRIGGER AS $$
DECLARE
    base_slug TEXT;
    final_slug TEXT;
    counter INTEGER := 0;
BEGIN
    base_slug := LOWER(REGEXP_REPLACE(
        REGEXP_REPLACE(TRIM(NEW.full_name), '[^a-zA-Z0-9\s]', '', 'g'),
        '\s+', '-', 'g'
    ));

    final_slug := base_slug;

    WHILE EXISTS (
        SELECT 1 FROM spotlight_submissions
        WHERE slug = final_slug
          AND id != COALESCE(NEW.id, '00000000-0000-0000-0000-000000000000'::uuid)
    ) LOOP
        counter := counter + 1;
        final_slug := base_slug || '-' || counter;
    END LOOP;

    NEW.slug := final_slug;
    NEW.updated_at := NOW();

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_spotlight_slug ON spotlight_submissions;
CREATE TRIGGER set_spotlight_slug
    BEFORE INSERT OR UPDATE ON spotlight_submissions
    FOR EACH ROW
    EXECUTE FUNCTION generate_spotlight_slug();

-- ============================================
-- AUTO-SET published_at ON INSERT
-- ============================================
CREATE OR REPLACE FUNCTION auto_publish_spotlight()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'published' AND NEW.published_at IS NULL THEN
        NEW.published_at := NOW();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS auto_publish_spotlight_trigger ON spotlight_submissions;
CREATE TRIGGER auto_publish_spotlight_trigger
    BEFORE INSERT OR UPDATE ON spotlight_submissions
    FOR EACH ROW
    EXECUTE FUNCTION auto_publish_spotlight();

-- ============================================
-- ROW LEVEL SECURITY
-- ============================================
ALTER TABLE spotlight_submissions ENABLE ROW LEVEL SECURITY;

-- Anyone can submit the form
CREATE POLICY "Anyone can insert submissions" ON spotlight_submissions
    FOR INSERT WITH CHECK (true);

-- Anyone can read published stories
CREATE POLICY "Anyone can read published" ON spotlight_submissions
    FOR SELECT USING (status = 'published');

-- Service role can do everything (used by Edge Functions)
CREATE POLICY "Service role full access" ON spotlight_submissions
    FOR ALL USING (auth.role() = 'service_role');

-- ============================================
-- STORAGE BUCKET FOR PHOTO & FILE UPLOADS
-- ============================================
INSERT INTO storage.buckets (id, name, public)
VALUES ('spotlight-uploads', 'spotlight-uploads', true)
ON CONFLICT (id) DO NOTHING;

-- Allow anyone to upload files
CREATE POLICY "Public upload to spotlight" ON storage.objects
    FOR INSERT WITH CHECK (bucket_id = 'spotlight-uploads');

-- Allow anyone to read uploaded files
CREATE POLICY "Public read spotlight files" ON storage.objects
    FOR SELECT USING (bucket_id = 'spotlight-uploads');
