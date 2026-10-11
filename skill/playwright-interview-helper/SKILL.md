---
name: playwright-interview-helper
description: Interview prep and interview-running toolkit for Python + Playwright (with Pytest) test automation roles. Use whenever the user wants interview questions, model answers, a mock interview, live-coding exercises, framework/architecture design questions, or a rubric to evaluate candidates for SDET / automation / QA engineer roles involving Playwright, pytest-playwright, Selenium-to-Playwright migration, flaky tests, CI/CD for UI tests, or API testing with Playwright. Trigger even if the user only says "prep me for my automation interview", "quiz me on Playwright", "I'm interviewing an SDET tomorrow", or "give me questions to screen a Playwright candidate" without naming this skill.
---

# Python + Playwright Interview Helper

Helps with both sides of a Python + Playwright automation interview:

- **Candidate mode**: the user is preparing to be interviewed.
- **Interviewer mode**: the user is hiring and needs questions, exercises, and a way to judge answers.

Default level is **Senior SDET**: assume the candidate is expected to have deep hands-on Playwright + Pytest skill, be able to design a maintainable framework, and reason about flakiness and CI. Shift up (Lead/Manager: strategy, team scaling, trade-offs, metrics) or down (mid-level: fundamentals, syntax) when the user says so or the request clearly implies it.

## Step 1: Work out mode and format

Infer from the request; ask only if it is genuinely unclear.

| Signal | Mode |
|---|---|
| "prep me", "quiz me", "my interview", "how should I answer" | Candidate |
| "screen a candidate", "interviewing someone", "rubric", "what should a good answer include" | Interviewer |

Then pick the output format:

1. **Q&A with model answers**: a set of questions with strong answers. Default when the user asks for "questions".
2. **Mock interview**: one question at a time, wait for the user's answer, then critique it. Use when the user says "mock", "quiz me", "test me", "ask me".
3. **Coding exercise**: a live-coding task with a reference solution. Use for "coding round", "live coding", "write a test for…".
4. **Framework / design round**: open-ended architecture or strategy questions. Use for "framework design", "system design for automation", "how would you build…".

Several can combine; for example, a full prep pack might mix 1, 3 and 4.

## Step 2: Pull the material

Read only the reference file(s) you need:

- `references/question-bank.md`: concept and scenario questions by topic, with what a strong answer covers. Use for Q&A and mock modes.
- `references/coding-exercises.md`: live-coding tasks with reference solutions and the follow-ups interviewers ask. Use for coding rounds.
- `references/design-and-leadership.md`: framework design, CI/CD, flakiness strategy, Selenium migration, and lead-level questions.
- `references/interviewer-rubric.md`: scoring scale, green and red flags per topic, and a debrief template. Use in interviewer mode.

Treat the bank as a starting point, not a script. Vary the questions, adapt them to any company, domain, or job description the user mentions, and write fresh ones when it helps. If the user shares a JD, map the questions to its stated requirements.

## Step 3: Produce the output

### Q&A with model answers

For each question:

```
**Q: <question>**
*What they're really testing:* <one line>
**Strong answer:** <answer at the target level: concise, concrete, with a short code snippet where it helps>
*Follow-up to expect:* <one likely follow-up>
```

Keep answers spoken-length. A model answer that would take five minutes to say is not a model answer. Lead with the direct answer, then the reasoning, then a real-world detail (a trade-off, a gotcha, or what you'd do on a real project). Real-world detail is what separates a senior answer from a textbook one.

### Mock interview

- Ask **one** question, then stop and wait. Don't reveal the answer in the same message.
- After the user answers, give a score (1–4 per `interviewer-rubric.md`), what was strong, what was missing, and a tightened version of their answer in their own voice rather than a replacement in yours.
- Ramp difficulty: start with a warm-up, then go deeper on whatever they answer well, and probe gaps the way a real interviewer would.
- Every 5 questions, or when the user stops, give a short summary: strengths, gaps, and the 2–3 topics to drill next.

### Coding exercise

Provide:

1. **Problem statement** as an interviewer would say it, including the app or page under test and constraints such as time-box or "no hard waits".
2. **Starter context** if needed (HTML snippet, URL, or API shape).
3. **Reference solution** in Python using `pytest-playwright` (sync API unless the user asks for async).
4. **What the interviewer looks for**: locator choice, waiting strategy, assertions, structure.
5. **Follow-ups**: 2–3 extensions, such as "now make it run across 3 browsers" or "now mock the API".

In candidate mode, offer to hide the solution so the user can attempt the task first.

Code standards for every solution:
- Use user-facing locators (`get_by_role`, `get_by_label`, `get_by_test_id`) over CSS/XPath, and say why.
- Use web-first assertions (`expect(locator).to_have_text(...)`). Never `time.sleep` or `wait_for_timeout` for synchronization.
- Use fixtures for setup; keep tests independent and parallel-safe.
- Write current Playwright Python APIs only. Don't invent methods. If unsure an API exists, say so instead of guessing.

### Framework / design round

Give the question, the dimensions a strong answer covers (structure, data, environments, reporting, CI, flakiness, scaling), a model answer outline, and the trade-off questions an interviewer will push on. For interviewer mode, add what separates a 3 from a 4.

## Interviewer mode extras

- When asked for a question set, balance it: roughly 40% hands-on Playwright/Pytest, 25% framework/design, 20% debugging/flakiness/CI, 15% behavioral or collaboration.
- Pair each question with green flags, red flags, and a probing follow-up, so the interviewer can tell real experience from memorized answers.
- If the user pastes a candidate's answer, evaluate it against the rubric and say what to probe next.
- Offer the debrief template from `interviewer-rubric.md` at the end of a session.

## Tone

Be direct and practical, like a senior colleague doing prep with you. Don't pad. When a user's answer is weak, say so clearly and show how to fix it. Interviews punish vague answers, so honest critique helps more than reassurance.
