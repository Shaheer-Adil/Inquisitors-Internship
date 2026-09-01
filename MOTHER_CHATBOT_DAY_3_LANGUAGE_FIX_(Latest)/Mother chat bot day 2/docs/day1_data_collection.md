# Day 1 Data Collection Specification

## MVP finish line
- Persona written.
- Fixed emotion/intent labels.
- Source register with 10–20 authoritative sources.
- 100–300 authored mother-style examples.
- Cleaned structured data ready for Day 2.
- External-source material separated from team-authored examples.

## Source collection protocol
For every external source record: source_id, title, organization, URL, access date, languages, topics, and usage/licensing note.
Before automated extraction, check the source's terms and robots.txt. Prefer permitted/manual extraction of relevant sections. Do not copy whole articles.

## Conversation schema
Each JSONL record contains:
id, content_type, scenario, emotion, secondary_emotion, intent, mother_goal, tone, language, user_message, response, source_type.

## Data families
1. Authoritative parenting knowledge: concise paraphrases tied to source_id.
2. Team-authored mother-style examples: original examples, clearly marked source_type=team_authored.

## Required coverage
Achievement, failure/disappointment, sadness, stress/fear/anger, loneliness, gratitude, motivation, mistakes, advice, and daily conversation. Include English, Urdu, Roman Urdu and mixed-language examples.
