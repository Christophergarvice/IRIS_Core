<<<<<<< HEAD
# IRIS_Core
=======
# SimpleBook Parser

SimpleBook is a modular accounting and statement-parsing system built for builders, landlords, and small business owners.  
It converts complex bank statements (PDF or OCR) into structured data — separating Deposits, Other Credits, Checks, and Debits — then verifies totals against declared statement balances.

## Current Modules
- **Module 1 – Deposits**
- **Module 2 – Other Credits**
- **Module 3 – Checks**
- **Module 4 – Other Debits**
- **Module 5+ – OCR Pipeline, Memory Logging, and IRIS Integration**

## System Components
- `simplebook_memory_logger.py`: records each module’s success/failure
- `iris_main.py`: controls session memory and tracks system learning
- `simplebook_backup.py`: automates data backup
- `requirements.txt`: defines project dependencies

## Goals
- Full statement reconciliation
- Intelligent OCR parsing
- Adaptive learning via IRIS (Inner Reasoning Integration System)
- GitHub-based version tracking and modular independence

---

### Run the System
```bash
python iris/iris_main.py
>>>>>>> 7d0917d (Added full project README)
