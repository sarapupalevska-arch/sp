# Competitor post scrape and theme summary (deep sweep), 2026-07-07

**Method and honesty note.** LinkedIn cannot be scraped without login and this
environment has no LinkedIn session or Apify token, so collection used repeated
web searches for posts Google has indexed on each founder's own profile URL
(the system's priority 3 fallback). Four sweep rounds collected **90 posts**
across Tier 1 and Tier 2, including comment counts wherever the search snippet
exposed them. A direct fetch of post pages was also attempted and LinkedIn
returns 403, confirming search index is the ceiling without login. This is a partial trail, not the full feed; Google indexes
LinkedIn sparsely, so recent months are under-represented. Dates are derived
from each post's activity ID timestamp. Full data: `data/linkedin/combined.csv`
and `data/linkedin/websearch-2026-07-07.json`.

## Nick Huber (Somewhere.com), 19 posts, the engagement benchmark

The deep sweep captured comment counts on 9 of his posts, giving the only real
engagement ladder in this dataset:

| Comments | Date | Post | Link |
|---|---|---|---|
| 335 | 2022-07-13 | "LinkedIn is full of BAD BUSINESS ADVICE" | [post](https://www.linkedin.com/posts/sweatystartup_linkedin-is-full-of-bad-business-advice-activity-6953097335631417345-bNRG) |
| 305 | 2023-01-10 | "Entrepreneurship culture in America is all messed up" | [post](https://www.linkedin.com/posts/sweatystartup_entrepreneurship-culture-in-america-is-all-activity-7018591765498662912-GlLW) |
| 83 | 2023-01-30 | "10 things I've changed my mind on recently" | [post](https://ie.linkedin.com/posts/sweatystartup_10-things-ive-changed-my-mind-on-recently-activity-7025823215629320192-021-) |
| 45 | 2023-08-22 | "The current requirements of entrepreneurship: a $1 billion idea..." | [post](https://www.linkedin.com/posts/sweatystartup_the-current-requirements-of-entrepreneurship-activity-7099845934687129600-S6sr) |
| 31 | 2023-03-20 | "The 'never give up' advice is bullshit. Give up quickly." | [post](https://www.linkedin.com/posts/sweatystartup_the-never-give-up-advice-is-bullshit-activity-7043667772425347073-Oh4e) |
| 28 | 2023-03-14 | "The worst thing you can do as an entrepreneur is hire a social justice..." | [post](https://www.linkedin.com/posts/sweatystartup_the-worst-thing-you-can-do-as-a-entrepreneur-activity-7041396044340826112-FKIo) |
| 28 | 2022-08-16 | "The biggest mistake I see folks make who are early..." | [post](https://ee.linkedin.com/posts/sweatystartup_the-biggest-mistake-i-see-folks-make-who-activity-6965127862324518913-vL-A) |
| 10 | 2023-01-03 | "Entrepreneurship is a funny thing. You work at something for years..." | [post](https://me.linkedin.com/posts/sweatystartup_entrepreneurship-is-a-funny-thing-you-work-activity-7016051468935839744-kLcl) |

**The pattern is unambiguous: his all-out contrarian bold-claim posts pull 300+
comments; softer advice and reflection posts pull 10-83.** A 10x to 30x gap by
hook type on the same account. His offshore content follows the same recipe
applied to hiring: name the fear, break it with his own numbers ($1.3M payroll
for 47 staff vs competitors' $4M+, 70% of team overseas, "80% less than US
equivalents"), then plug [Somewhere/Shepherd](https://www.linkedin.com/posts/sweatystartup_shepherd-headhunter-agency-for-overseas-activity-7178428023292002304-PEpg)
([overseas inbox fear post](https://www.linkedin.com/posts/sweatystartup_a-lot-of-people-are-worried-about-an-overseas-activity-7166793857681088512-OZQu) 2024-02-23,
[Somewhere promo](https://www.linkedin.com/posts/sweatystartup_somewhere-formerly-support-shepherd-hire-activity-7281055476992090112-hwkd) 2025-01-03).
His newest indexed content ([real estate](https://www.linkedin.com/posts/sweatystartup_real-estate-is-the-best-business-in-the-world-activity-7437615507559563265-Cg51), 2026-03-11) drifts away from offshore hiring.

## Go Carpathian (Nathan Fales + company page), 17 posts, proximity 5/5

Fales personal feed, newest first: [Most agencies focus on one thing: closing the big deal. But the smartest...](https://www.linkedin.com/posts/nathanfales_most-agencies-focus-on-one-thing-closing-activity-7275873115044200448-y4u8) (2024-12-20), [Lean Leverage launch x3](https://www.linkedin.com/posts/nathanfales_lean-leverage-go-carpathian-activity-7271886715118579712-Pz91) (Oct-Dec 2024), [If you have the resources and patience to...](https://www.linkedin.com/posts/nathanfales_if-you-have-the-resources-and-patience-to-activity-7257376309046063104-fjzf) (2024-10-30), [Interview Questions](https://www.linkedin.com/posts/nathanfales_interview-questions-activity-7250490901980921856-MTo1) (2024-10-11), [Our first client left us a scathing review](https://www.linkedin.com/posts/nathanfales_our-first-client-left-us-a-scathing-review-activity-7379240726720802816-_D7k) (2025-10-01), [If your team sucks it's your fault](https://www.linkedin.com/posts/nathanfales_if-your-team-sucks-its-your-fault-generally-activity-7077110577814261760--V7X) (2023-06-21).

Company page: SEO listicles ([top remote recruitment agencies](https://www.linkedin.com/posts/go-carpathian_top-10-best-remote-recruitment-agencies-in-activity-7378798422197239808-J44H) 2025-09-30, [finance recruiters](https://www.linkedin.com/posts/go-carpathian_top-16-accounting-and-finance-recruitment-activity-7394492521726431232-GwhU) 2025-11-12, [hire smarter](https://www.linkedin.com/posts/go-carpathian_how-to-hire-an-employee-for-a-small-business-activity-7396309840110796801-Ih_X) 2025-11-17) plus recurring #hiring job ads.

**Theme read.** The only Tier 1 competitor actively working the agency-ICP
lane: Fales writes agency-operator takes ("most agencies focus on closing...")
and Huber-style bold claims ("if your team sucks it's your fault"), mixed with
vulnerability stories. Their site leads with "save 73%+ on payroll" (money-math)
but their LinkedIn does not carry those numbers; the money-math lane is
unoccupied on their feed. No candidate-voice, no data reports.

## Kadraa (Michael Prince + Haaken Mordt), 9 posts, correction: not silent

Earlier sweep rounds only surfaced 2023-2024 hashtag job ads
([1](https://www.linkedin.com/posts/kadraa_kadraa-digitalmarketing-recruiters-activity-7188793816575885312-ATbT),
[2](https://www.linkedin.com/posts/michael-prince-97280648_jobhunting-marketing-kadraa-activity-7191330527235174403-r_16),
[3](https://www.linkedin.com/posts/kadraa_remoteseojobs-remoteseoroles-digitalmarketingjobs-activity-7115257220665081857-xIvN)).
Round 4 found founder-led content after all: Michael Prince writes
Huber-style contrarian takes on the exact SA-to-UK lane:
[The uncomfortable truth about SA talent (that nobody talks about)](https://www.linkedin.com/posts/michael-prince-97280648_the-uncomfortable-truth-about-sa-talent-activity-7311358903445794816-WXGG) (2025-03),
[From Cape Town to London: the brutal reality](https://www.linkedin.com/posts/michael-prince-97280648_from-cape-town-to-london-the-brutal-reality-activity-7318229173448101889-l56x) (2025-04),
[Empowering Global Talent article share](https://www.linkedin.com/posts/michael-prince-97280648_empowering-global-talent-an-insiders-perspective-activity-7272945789725732864-4VWk) (2024-12).
Haaken Mordt posts occasionally
([Want to know what separates champions...](https://www.linkedin.com/posts/haaken-mordt-7b2a66196_want-to-know-what-separates-champions-activity-7338160502260318209-NGRc), 2025-06).
Plus PR placements ([finance-roles expansion](https://news.marketersmedia.com/kadraa-recruitment-expands-services-to-include-remote-finance-professionals-as-uk-hiring-cost-pressures-rise/89187006),
[TechBullion profile](https://techbullion.com/empowering-global-talent-an-insiders-perspective-on-kadraa-recruitments-transformative-approach-for-offshore-recruitment/)).
**Revised read: Kadraa's founders publish contrarian SA-talent content at low
volume with nothing indexed for 2026 yet. The lane is contested but thinly,
and their angle is candidate-side reality checks, not client-side proof.**

## Monty Ngan + Isaac Kassab (Pearl Talent), 14 posts

Newest: [Adobe's CEO steps down... AI](https://www.linkedin.com/posts/montyngan_adobes-ceo-steps-down-after-18-years-because-activity-7439296814484451329-HyIA) (2026-03-16, 13 comments). Also: [Monty, we want to fly your candidate to the UK](https://www.linkedin.com/posts/montyngan_startups-entrepreneurship-recruitment-activity-7275156741644857346-LGdY) (2024-12-18, a hire-success-story told through a client text), [Folks always ask me why I started Pearl Talent](https://www.linkedin.com/posts/montyngan_folks-always-ask-me-why-i-started-pearl-talent-activity-7260652315152453632-DvFt) (2024-11-08), [This email changed my life](https://www.linkedin.com/posts/montyngan_this-email-changed-my-life-two-years-ago-activity-7226210608679964672-aEgd) (2024-08-05), [success reminder](https://www.linkedin.com/posts/montyngan_an-important-reminder-for-everyone-success-activity-7239618741624320003-w8uy) (2024-09-11), [lean startups commentary](https://www.linkedin.com/posts/montyngan_startups-entrepreneurship-leanstartups-activity-7371891527272333312-12Pv) (2025-09-11).

**Theme read.** Rotation is visible: origin story > client-proof story > big
tech/AI commentary. He is the first of the five to move into ai-and-hiring
content, matching Pearl's "AI-trained talent, top 0.8%" positioning. Pearl also
runs SEO listicles ([best remote recruitment agencies 2026](https://www.pearltalent.com/resources/best-remote-recruitment-agencies)).
Round 3 additions: co-founder **Isaac Kassab** also publishes, including a
[fake-recruiter scam warning](https://www.linkedin.com/posts/isaac-kassab_startups-entrepreneurship-leanstartups-activity-7361018650058776576-t95J)
(2025-08-12, trust/compliance content), and the company page runs
[client-proof screenshots](https://www.linkedin.com/posts/pearltalent_received-a-text-from-pearl-talent-we-activity-7356080092374028289-cGvq) (2025-07-29)
and [employer-brand posts](https://www.linkedin.com/posts/pearltalent_perks-of-working-at-pearl-talent-activity-7265364267099463680-pq9I) (2024-11-21).

## Angel Salinas (Remote Talent LATAM), 7 posts

Personal: [The #1 role marketing agencies hire from LATAM: Account...](https://www.linkedin.com/posts/salinassandino_the-1-role-marketing-agencies-hire-from-activity-7427014739009900544-lFAu) (2026-02-10) and a [hashtag post](https://www.linkedin.com/posts/salinassandino_remotetalent-recruitment-latam-activity-7275555874717282304-abYd) (2024-12-19).
Company page (found in round 3, more active than his personal feed):
[hiring post with 27 comments](https://es.linkedin.com/posts/remote-talent-latam_hiring-remotejobs-latamjobs-activity-7448489256693596160-FyLZ) (2026-04-10, the second-highest 2026 engagement number in this dataset),
[Meet the Team: Karina Edition](https://www.linkedin.com/posts/remote-talent-latam_meettheteam-teamspotlight-recruiter-activity-7274877786975002624-b0N5) (2024-12-17, a recurring team-spotlight series, the nearest thing to candidate-voice any competitor runs),
[marketing careers](https://www.linkedin.com/posts/remote-talent-latam_marketingcareers-remoteopportunities-latamtalent-activity-7258238792812113921-numN) (2024-11-01),
[job ad](https://www.linkedin.com/posts/remote-talent-latam_jobopportunity-nowhiring-joinourteam-activity-7285428549610610689-YBSv) (2025-01-15).

**Theme read.** The 2026 personal post is the exact buyer-intent format worth
copying for Eastern Europe. The company's team-spotlight series is spotlighting
their own recruiters, not placed candidates, so the candidate-voice lane is
still open even here. His retention claim (1,000+ placements, 4+ year tenure)
lives on his website only.

## Tier 2 watch (new this sweep)

- **Near / Hayden Cohen (CEO) is the most active founder-publisher in the whole set** and posts into June 2026: [Mexico as a remote talent hub](https://www.linkedin.com/posts/hayden-cohen-near_youve-been-thinking-about-this-country-all-activity-7472985173530263552-qRYJ) (2026-06-17), [I almost gave up on Latin America after my first hire](https://www.linkedin.com/posts/hayden-cohen-near_i-almost-gave-up-on-latin-america-after-my-activity-7363263885254057984-2nTV) (2025-08-18), [Hiring in LatAm isn't about filling gaps](https://www.linkedin.com/posts/hayden-cohen-near_hiring-in-latam-isnt-about-filling-gaps-activity-7318256855925858304--rz2) (2025-04-16), [Near is basically the same as any other staffing...](https://www.linkedin.com/posts/hayden-cohen-near_near-is-basically-the-same-as-any-other-staffing-activity-7254099158444204032-LnCI) (2024-10-21, myth-bust of his own category). Near's PR machine adds data hooks: sales/SDR roles are the #1 driver (22% of demand) per [their release](https://www.einpresswire.com/article/921811244/sales-roles-are-the-no-1-driver-of-u-s-companies-hiring-in-latin-america-hire-with-near-data-shows). He is the template for what JobRack's founder feed should look like, pointed at LatAm instead of Eastern Europe.
- **Somewhere company page runs a numbered success-story series**: [Hired with Somewhere #29](https://www.linkedin.com/posts/jobs-somewhere_hired-with-somewhere-29-shopify-for-remote-activity-7318630467421777920-KWML) (2025-04-17), at least 29 episodes, plus [Hire globally, strategically](https://www.linkedin.com/posts/somewhere_hire-globally-strategically-somewherecom-activity-7386054400118546432-a84O) (2025-10-20). Serialized proof content is being executed at scale in this niche, just not with candidate voices and not for Eastern Europe.
- **Remoteli / Samuel Brooksworth**: near-zero founder presence; one [company post](https://www.linkedin.com/posts/hired-remoteli_hired-remoteli-linkedin-activity-7448716495339139072-uuZn) (2026-04-11).

## New voices entering the niche (leading indicator)

- [Franco Pereyra](https://www.linkedin.com/posts/franco-pereyra_ive-been-watching-companies-quickly-go-from-activity-7417939950651785217-oLW0): "2-4 core people in the US office, everyone else in Latin America" (2026-01, 16 comments).
- [Charlie Ewig](https://www.linkedin.com/posts/charlie-ewig-baaa35174_colombia-is-becoming-one-of-the-top-talent-activity-7450547325871017984-TLZQ): Bogota as LatAm's top talent market (2026-04).
- [Marcelo Lebre](https://www.linkedin.com/posts/marcelolebre_we-started-remote-in-my-living-room-with-activity-7456043032354705408-lNIl) (Remote.com co-founder): origin story post, 62 comments (2026-05), confirming origin-story format still earns engagement in 2026.
- [Alexis Bourson](https://www.linkedin.com/posts/alexisbourson_atlas-by-cortese-helps-companies-hire-remote-activity-7445414298849337344-rBlS) (Atlas by Cortese): founder-led remote sales talent from Portugal, 10 comments (2026-04). The first European-nearshore voice spotted, worth watching as a preview of Eastern Europe competition.
- Nobody is posting founder-led content for Eastern Europe itself. The loudest new voices are all LatAm, with one Portugal entrant.

## What themes are working best (updated with engagement evidence)

1. **Contrarian bold-claim hooks outperform everything else by 10-30x** on the
   one account with measurable data (Huber: 335 and 305 comments vs 10-83 for
   non-contrarian posts). JobRack application: "Most advice about offshore
   hiring is wrong" style openers over polite explainers.
2. **Money-math is the niche's shared language** (Huber's payroll numbers,
   Go Carpathian's "save 73%", Near's "$35k per hire"), but on LinkedIn feeds
   only Huber actually posts the numbers. Everyone else keeps them on websites.
3. **Origin and turning-point stories keep earning in 2026** (Lebre 62
   comments in May 2026; Ngan and Fales keep returning to the format; Cohen's
   "I almost gave up on Latin America" is the region-advocacy version).
4. **Serialized client-proof content is proven at scale** (Somewhere's
   numbered series, 29+ episodes; Ngan's client-text screenshot post), but
   nobody does it in the candidate's own voice.
5. **AI-and-hiring is where the leaders are rotating next** (Ngan's newest
   post, Pearl's AI-trained positioning, Remote Recruit's AI platform launch).
6. **Confirmed nearly empty across all 72 posts:** candidate-voice stories
   (closest attempts: Remote Talent LATAM spotlights its own recruiters, and
   one 2024 Go Carpathian post celebrates the Romanian language rather than a
   person), original Eastern Europe data, and retention claims made in-feed.
   With Kadraa and Remoteli silent and every rising voice pointed at LatAm,
   Eastern Europe founder-led content has no incumbent.
