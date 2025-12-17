# Survicate Question Management System

## Problem

When questions are added, removed, or reordered in Survicate, the sequential question numbers (Q#9, Q#10, etc.) change. This breaks code that references questions by number.

**Example:** The "Learn training curriculum" question was Q#9, but after adding new Q#9 and Q#10, it's now Q#11.

## Solution

Use **logical question identifiers** instead of sequential numbers. Questions are matched by **text content patterns**, not by number.

### How It Works

1. **Question Configuration** (`backend/utils/survicate_question_config.py`)
   - Defines logical identifiers (e.g., `learn_engagement`, `battery_issues`)
   - Maps each identifier to search patterns (keywords in question text)
   - Maintains backward compatibility with legacy Q# numbers

2. **Text-Based Matching**
   - Questions are found by matching text patterns, not sequential numbers
   - Works even when question numbers shift
   - Primary matching strategy in `survicate_routes.py`

3. **Logical Identifiers**
   - Code references questions by semantic meaning: `learn_engagement` instead of `Q9` or `Q11`
   - When questions renumber, only the config file needs updating

## Adding/Updating Questions

### When a New Question is Added

1. Add entry to `QUESTION_CONFIG` in `backend/utils/survicate_question_config.py`:
```python
'new_question_id': {
    'patterns': ['keyword1', 'keyword2', 'keyword3'],
    'display_name': 'Human-Readable Question Name',
    'legacy_q_number': 'Q9',  # Current sequential number
    'is_new': True  # Mark as newly added
}
```

2. Update any UI components that list questions (e.g., `ChurnTrendsChart.js`)

### When Questions Renumber

1. Update `legacy_q_number` in the config
2. Optionally add to `previous_q_numbers` for reference
3. **No code changes needed** - text matching handles it automatically

### Example: Learn Question Renumbering

**Before:**
```python
'learn_engagement': {
    'patterns': ['engage', 'Learn training curriculum'],
    'legacy_q_number': 'Q9'
}
```

**After new Q9/Q10 added:**
```python
'learn_engagement': {
    'patterns': ['engage', 'Learn training curriculum'],
    'legacy_q_number': 'Q11',  # Updated
    'previous_q_numbers': ['Q9']  # Track history
}
```

## Migration Guide

### For API Routes

**Old way:**
```python
question_patterns = {
    'Q9': ['engage', 'Learn training curriculum']
}
```

**New way:**
```python
from backend.utils.survicate_question_config import QUESTION_CONFIG

# Use logical ID
config = QUESTION_CONFIG['learn_engagement']
pattern = config['patterns']
```

### For Frontend

**Old way:**
```javascript
{ id: 'Q9', text: 'Q#9: Did you engage with the Learn training curriculum?' }
```

**New way:**
```javascript
{ 
  id: 'learn_engagement',  // Logical ID
  text: 'Did you engage with the Learn training curriculum?',
  legacyNumber: 'Q11'  // For display if needed
}
```

## Benefits

1. **Resilient to renumbering** - Questions found by content, not position
2. **Semantic naming** - `learn_engagement` is clearer than `Q9` or `Q11`
3. **Single source of truth** - All question mappings in one config file
4. **Backward compatible** - Legacy Q# numbers still work
5. **Easy updates** - Change config, not code

## Current Question Mappings

See `backend/utils/survicate_question_config.py` for the complete list of logical identifiers and their patterns.

