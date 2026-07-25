# Mid-Course Project Reflection

This project extended an existing Task Tracker with two small end-to-end features: search with combined filters, and due dates with overdue filtering. The most important lesson was that using AI effectively requires more than accepting generated code. I had to define the behavior first, constrain the scope, inspect the real diff, run focused tests, and correct assumptions before keeping changes.

For the search feature, I extended the existing `GET /tasks` endpoint instead of creating a separate search endpoint or filtering only in the browser. Search is partial and case-insensitive across titles and optional descriptions, and it combines with status and priority. One AI suggestion initially used `task.description.lower()`, which would fail when a description was `None`. I corrected this to `(task.description or "").casefold()`. This showed why generated code still needs careful review, even when the overall approach is correct.

For the due-date feature, I chose a date-only value rather than adding times, time zones, reminders, or calendar libraries. This kept the feature aligned with the project’s scope. The frontend required additional review. A broad CSS selector unintentionally targeted the new checkbox, and the first PATCH comparison treated an unchanged empty due date as changed because it compared `null` with an empty string. Both problems were corrected before the feature was committed.

Testing was not limited to proving that the completed implementation passed. I first added tests that failed because the features did not exist yet. I also performed two Break Tests by deliberately damaging working behavior. The search test detected a disabled search filter, and the overdue test detected completed tasks being incorrectly returned as overdue. After each failure, I restored the correct implementation and confirmed the full suite passed.

Finally, I documented a behavior contract before extracting the overdue condition into a private helper. The test result remained `28 passed, 1 warning` before and after the refactor, providing evidence that code structure improved without changing observable behavior.

Overall, the project taught me to use AI as a reviewed development assistant rather than an automatic source of truth. Small prompts, narrow diffs, independent verification, and explicit scope decisions produced a safer and more understandable result.
