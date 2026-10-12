# CampusFlow

A Python command-line campus helpdesk ticket manager. Standard library only; Python 3.10+ recommended.

## Run
```bash
python main.py
```

## Test
```bash
python -m unittest discover -s tests -v
```

## Features
- Create and validate tickets with unique IDs.
- Calculate priority using ordered rules: high urgency AND >=10 users = critical; high urgency OR >=10 users = high; medium urgency OR >=3 users = medium; otherwise low.
- List/view tickets, assign staff, manage `open -> in_progress -> resolved`, and reopen resolved tickets.
- Queue open tickets by priority then numeric ID.
- Reports by status and priority, including an empty state.
- JSON persistence at `data/tickets.json`. Missing file starts empty; malformed data raises a clear error and is not silently overwritten.

## Team workflow
Use separate feature branches. Each fellow must contribute code and tests, open a PR, review the partner's PR with at least two substantive observations, obtain approval, and merge only after review. Keep AI learning logs truthful and verify suggestions independently.

Suggested ownership: Fellow A owns creation/validation/priority; Fellow B owns assignment/workflow/queue/reports. Both work on persistence integration, testing, review, and demo.

## Demo checklist
1. Create tickets with different priority levels and an invalid ticket.
2. Assign and progress a ticket through the lifecycle.
3. Demonstrate a rejected invalid transition.
4. Show queue and reports.
5. Restart to verify persistence.
6. Run tests and show real PR reviews.

## Limitations
Local single-user CLI; no authentication or staff directory; JSON is not intended for concurrent multi-user writes.
