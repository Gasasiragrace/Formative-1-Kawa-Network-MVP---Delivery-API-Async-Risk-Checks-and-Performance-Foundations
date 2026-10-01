# ADR 001: Database-backed queue with a polling worker for risk checks

## Status
Accepted

## Context
The external risk registry takes between two and forty seconds to answer and can be unavailable for hours. Emmanuel records deliveries at a station while farmers wait at the scale, so a plot registration cannot block on the registry.

## Decision
When a plot is registered, the API saves it with risk_status pending and returns immediately. The queued check is stored in the database, and a separate worker (python manage.py run_risk_worker) processes it and logs each attempt.

## Why a database queue instead of Celery + Redis
I chose a database queue with a worker because it was simpler with what I already had installed, instead of adding Celery and Redis. If the server restarts, the queued check is still in the database and can be processed when the worker starts again.

## What this makes harder
The worker has to keep checking the database, so the risk check is not immediate. With many workers or much more traffic, this could put more pressure on the database and become harder to manage.

## Stakeholder who benefits most
Emmanuel benefits most because he needs to record deliveries quickly while farmers are waiting at the scale. Since the registry can take two to forty seconds or be down for hours, the queue means he does not have to wait for the check.

## Non-functional requirements
This mainly helps availability and durability. The delivery process can continue even when the external registry is unavailable, and the queued check is saved so it is not simply lost when the worker or server goes down.

## Plots whose check never succeeds
Yes, deliveries can still be recorded even if the plot check never succeeds, because Emmanuel should not have to stop recording deliveries just because the external registry is down. I would mark those deliveries as pending verification so they can be checked later.

## Performance choice: why pagination first
I chose pagination first because Emmanuel may have around 400 deliveries a day and is using a phone on 2G. Loading all those deliveries at once would make the feed slower, so pagination lets him load smaller amounts and get the information he needs faster.
