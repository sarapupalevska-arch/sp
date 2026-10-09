"""Stage 1: turn a theme into N distinct page ideas."""
import json
import os

from .config import BookSpec

FALLBACK = [
    "a smiling T-rex waving",
    "a baby triceratops hatching from an egg",
    "a long-necked brachiosaurus eating leaves",
    "a stegosaurus with big plates under the sun",
    "two dinosaurs playing in a puddle",
    "a pterodactyl flying over mountains",
    "a dinosaur family walking together",
    "a baby dinosaur sleeping on a pile of leaves",
    "a dinosaur blowing out birthday candles",
    "a dinosaur riding a bicycle",
    "a dinosaur planting flowers in a garden",
    "a dinosaur reading a book under a tree",
    "a dinosaur at the beach with a bucket",
    "a dinosaur baking a cake",
    "a dinosaur flying a kite",
    "a dinosaur with a backpack going to school",
    "a dinosaur painting a picture",
    "a dinosaur in a rain boots jumping in rain",
    "a dinosaur camping with a tent",
    "a dinosaur juggling balls",
    "a dinosaur on a swing",
    "a dinosaur building a sandcastle",
    "a dinosaur with a balloon",
    "a dinosaur watering plants",
    "a dinosaur sitting on a rocket ship",
    "a dinosaur feeding ducks",
    "a dinosaur playing a drum",
    "a dinosaur skating on ice",
    "a dinosaur picking apples",
    "a dinosaur waving goodbye",
]


def generate_ideas(spec: BookSpec, dry_run: bool = False) -> list[str]:
    if dry_run or not os.environ.get("OPENAI_API_KEY"):
        return (FALLBACK * 3)[: spec.pages]

    from openai import OpenAI

    client = OpenAI()
    prompt = (
        f"Give {spec.pages} different scene ideas for a children's coloring book "
        f"about '{spec.theme}' for ages {spec.age_range}. Each idea is one short "
        "phrase describing a single simple scene. Use only original, generic "
        "characters: no brands, no existing cartoon characters, no real people. "
        'Return JSON: {"ideas": ["...", ...]}'
    )
    resp = client.chat.completions.create(
        model=spec.text_model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    ideas = json.loads(resp.choices[0].message.content)["ideas"]
    return [i.strip() for i in ideas if i.strip()][: spec.pages]
