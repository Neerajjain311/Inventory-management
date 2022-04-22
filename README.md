# Inventory-management
Basic project for Backend Practice - APIs + Stream processing (FastAPI + Redis Stream)  

## Tech Stack
- FastAPI
- Redis
- Redis Stream

## Key Learnings
- API Development using FastAPI
- Event based stream processing

## Procedure to replicate the project and see it in action
1. Clone the repo.
2. Change the Redis DB connection and credentials (as I've already dropped the DB)
3. Run the two main modules (inventory, payment) in different ports (ex. 8000, 8001)
4. Run the two consumer scripts in different terminals
5. Use POST/GET/DELETE HTTP methods to populate/read/delete data
