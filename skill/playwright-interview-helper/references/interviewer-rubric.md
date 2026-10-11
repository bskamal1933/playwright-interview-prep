# Interviewer Rubric

## Scoring scale (per question or area)

| Score | Meaning |
|---|---|
| 1: No hire | Wrong or no answer; can't reason through it with hints. |
| 2: Weak | Textbook definitions only; no real-project detail; needs heavy prompting. |
| 3: Hire (Senior SDET bar) | Correct, practical, explains why; cites a real situation; handles one follow-up well. |
| 4: Strong hire | Correct plus trade-offs, gotchas, and what they'd do differently; handles probing; raises points unprompted. |

The gap between 2 and 3 is usually **specificity**. "Use explicit waits" is a 2. "We had a dashboard where the table re-rendered after polling, so we asserted on the row with `expect(...).to_have_count` instead of reading once" is a 3 or above.

## Green and red flags by topic

**Locators**
- Green: role/label-first with reasoning; knows strictness; chaining with `filter`.
- Red: XPath by default; absolute XPaths; `nth()` everywhere; uses ElementHandles.

**Waiting**
- Green: explains actionability checks; uses `expect` as the wait; knows `expect_response`.
- Red: `wait_for_timeout`/`time.sleep` as the fix; `networkidle` everywhere; "increase the timeout".

**Framework design**
- Green: fixtures for setup and teardown, API-seeded unique data, storage state, config from the environment, reporting with traces.
- Red: everything in one giant base class; shared mutable test data; credentials in code; tests depending on order.

**Flakiness and debugging**
- Green: trace viewer first; root-cause categories; quarantine with an owner; tracks a flake rate.
- Red: "add retries"; "it's the environment" with no evidence; never looked at a trace.

**API and network**
- Green: `route` for mocking with trade-offs; `APIRequestContext` for setup; awareness of contract drift.
- Red: can't explain when to mock; all setup through the UI.

**Communication**
- Green: structured answers; asks clarifying questions; admits what they don't know.
- Red: bluffing about APIs (probe by asking them to write the line); long answers that never answer.

## Probes that separate real experience from memorization

- "Show me the exact line you'd write for that."
- "What went wrong the first time you did this on a real project?"
- "What would you do differently now?"
- "How did you know it was fixed?"
- "What's the downside of the approach you just described?"

## Debrief template

```
Candidate: ____    Role: ____    Interviewer: ____    Date: ____

Scores (1–4):
- Playwright hands-on (locators, waits, assertions): _
- Pytest and framework design: _
- Debugging / flakiness / CI: _
- API & network: _
- Communication & collaboration: _

Strongest evidence (quote or paraphrase): ...
Biggest concern: ...
Probe next round on: ...
Recommendation: Strong hire / Hire / No hire / Strong no hire
```
