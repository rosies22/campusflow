# Design Decisions

Team members/date: fill in after both fellows discuss and confirm these starter decisions.

- Tickets are dictionaries in a list with fields `id`, `title`, `category`, `urgency`, `affected_users`, `priority`, `status`, and `assigned_to`.
- Business logic is separate from interactive input to make it unit-testable.
- Invalid user data raises `TicketValidationError`; persistence failures raise `StorageError`.
- IDs use the highest existing numeric suffix plus one, so IDs remain unique after reload even if there are gaps.
- Priority logic is deterministic Python business logic, not an AI model.
- The queue returns only `open` tickets, sorted by critical/high/medium/low and then numeric ID.
- JSON writes use a temporary file and atomic replacement. Malformed JSON is reported rather than replaced.
- Tests use standard-library `unittest`.
- Suggested split: Fellow A—creation, validation, priority and tests; Fellow B—assignment, workflow, queue, reports and tests; both—persistence integration, reviews, docs and demo.
- Update this document with the actual team agreement and any changes made during implementation.
