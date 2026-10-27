# Ventura Multifamily Prep

A personal study site for learning the Ventura County multifamily market in eight weeks: 220 questions across 17 topics, with drafted answers, sources, spaced-repetition flashcards, quizzes, Claude-graded client drills, weekly tests, and weekly check-ins.

The site runs as a private claude.ai Artifact: https://claude.ai/artifact/BZtPZzySGQjSvEWen9B2vW. Progress (mastery ratings, notes, your own answers, flashcard schedule, test results, check-ins) is stored in the artifact's built-in database, so it follows you to any device where you are signed in to claude.ai. No other services are needed.

## Layout

| Path | What it is |
|---|---|
| `content/question-bank.md` | The 220 questions. Question numbers are stable IDs. |
| `content/answers/sNN.json` | Drafted answers for section NN: summary, full answer, key points, sources, last-verified date, confidence, what to verify, and multiple-choice drills. |
| `content/glossary.json` | Terms of art, each linked to related questions. |
| `src/app.html` | The app (HTML, CSS, and JavaScript in one file). |
| `build.py` | Combines the question bank, answers, and glossary into the app. |
| `dist/index.html` | The built page that gets published. |

## Rebuild

```bash
python3 build.py
```

Then republish `dist/index.html` to the same artifact URL (ask Claude to "republish the study site").

## Eight-week plan

| Week | Topics |
|---|---|
| 1 | Geography and submarkets; economy, employers, demographics |
| 2 | Supply and pipeline; rents, occupancy, operations |
| 3 | Pricing and transaction metrics; debt and lending |
| 4 | Buyers and capital; sellers and ownership |
| 5 | State law; local ordinances |
| 6 | Land use and zoning; pending legislation and ballot measures |
| 7 | Taxes and 1031s; physical risk and insurance; affordable housing |
| 8 | Brokerage landscape; client questions; final exam |

Days 1 to 6: read about five questions a day and mark how well you know each, then clear due flashcards. Day 7: weekly test and check-in.

## About the answers

Answers were drafted from public sources in October 2026. Market figures (rents, cap rates, comps, interest rates) and local ordinances change, so each answer carries a confidence level and a note on what to verify. Use the "Needs verifying" filter, confirm against CoStar, FlexMLS, lenders, or city staff, and record corrections in "Your version" on each question. Claude uses your version when grading you.
