import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SLACK_WEBHOOK_URL = Deno.env.get("SLACK_WEBHOOK_URL");
const ANTHROPIC_API_KEY = Deno.env.get("ANTHROPIC_API_KEY");
const SUPABASE_URL = Deno.env.get("SUPABASE_URL");
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");

serve(async (req) => {
  try {
    const payload = await req.json();
    const record = payload.record as Record<string, string>;

    // 1. Send Slack notification
    if (SLACK_WEBHOOK_URL) {
      const storyUrl = `https://humansofaiatwork.lovable.app/story/${record.slug}`;
      await fetch(SLACK_WEBHOOK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text:
            `🎉 *New Learner Spotlight Submitted!*\n\n` +
            `*${record.full_name}*\n` +
            `${record.role ?? ""}${record.company ? " at " + record.company : ""}\n` +
            `Industry: ${record.industry ?? "—"}\n\n` +
            `📖 View story: ${storyUrl}`,
        }),
      });
    }

    // 2. Generate social media summary with Claude
    if (ANTHROPIC_API_KEY) {
      const claudeResponse = await fetch(
        "https://api.anthropic.com/v1/messages",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
          },
          body: JSON.stringify({
            model: "claude-sonnet-4-20250514",
            max_tokens: 300,
            messages: [
              {
                role: "user",
                content:
                  `Write a 2-3 sentence LinkedIn post promoting this learner spotlight. ` +
                  `Keep their voice authentic.\n\n` +
                  `Name: ${record.full_name}\n` +
                  `Role: ${record.role ?? ""}${record.company ? " at " + record.company : ""}\n` +
                  `Their key advice: "${record.advice_to_others ?? ""}"\n` +
                  `Their transformation: "${record.new_capabilities ?? ""}"\n\n` +
                  `Write an engaging, authentic post that would make others want to read their full story. ` +
                  `Include a call-to-action to read the full spotlight. ` +
                  `Do not use hashtags. Keep it human and warm.`,
              },
            ],
          }),
        },
      );

      const claudeData = await claudeResponse.json() as {
        content?: Array<{ text: string }>;
      };
      const socialSummary = claudeData.content?.[0]?.text;

      // 3. Update the submission with the generated social summary
      if (socialSummary && SUPABASE_URL && SUPABASE_SERVICE_ROLE_KEY) {
        const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);
        await supabase
          .from("spotlight_submissions")
          .update({
            social_summary: socialSummary,
            social_summary_generated_at: new Date().toISOString(),
          })
          .eq("id", record.id);
      }
    }

    return new Response(JSON.stringify({ success: true }), {
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    console.error("Error processing spotlight submission:", error);
    return new Response(
      JSON.stringify({ error: (error as Error).message }),
      { status: 500, headers: { "Content-Type": "application/json" } },
    );
  }
});
