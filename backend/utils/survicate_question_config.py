"""
Survicate Question Configuration

This module defines logical question identifiers and their search patterns.
This allows questions to be referenced by semantic meaning rather than 
sequential numbers, making the system resilient to question renumbering.

When questions are added/removed/reordered in Survicate, only the search
patterns need to be updated here - not all the code that references questions.
"""

from typing import Dict, List

# Logical question identifiers mapped to search patterns
# These patterns are used to find questions by text content, not by number
QUESTION_CONFIG: Dict[str, Dict[str, any]] = {
    'location_mismatch': {
        'patterns': ['location pin', 'not match', 'dog'],
        'display_name': 'Location Pin Not Matching Dog Location',
        'legacy_q_number': 'Q2'  # For backward compatibility
    },
    'pet_location_inaccurate': {
        'patterns': ['pet location pin', 'grayed out', 'inaccurate'],
        'display_name': 'Pet Location Pin Grayed Out or Inaccurate',
        'legacy_q_number': 'Q3'
    },
    'collar_not_responding': {
        'patterns': ['collar', 'not sending feedback', 'dog not responding'],
        'display_name': 'Collar Not Sending Feedback or Dog Not Responding',
        'legacy_q_number': 'Q4',
        'prefer_answer': True  # Prefer (Answer) column for this question
    },
    'contact_tips_static': {
        'patterns': ['screw in', 'contact tips', 'static feedback'],
        'display_name': 'Contact Tips Required for Static Feedback',
        'legacy_q_number': 'Q5'
    },
    'battery_issues': {
        'patterns': ['battery life', 'charging', 'power issues'],
        'display_name': 'Battery Life, Charging or Power Issues',
        'legacy_q_number': 'Q6',
        'prefer_answer': True
    },
    'containment_solution_purchased': {
        'patterns': ['containment solution', 'purchase'],
        'display_name': 'Which Containment Solution Did You Purchase?',
        'legacy_q_number': 'Q7'
    },
    'other_gps_purchased': {
        'patterns': ['other GPS', 'wireless fence', 'purchase'],
        'display_name': 'Which Other GPS or Wireless Fence Did You Purchase?',
        'legacy_q_number': 'Q8'
    },
    'one_or_multiple_dogs': {
        'patterns': ['one dog', 'multiple dogs', 'wearing Halo'],
        'display_name': 'Do You Have One Dog or Multiple Dogs Wearing Halo?',
        'legacy_q_number': 'Q9',
        'is_new': True  # Mark as newly added
    },
    'which_dog_issue': {
        'patterns': ['which dog', 'most often experienced', 'issue', 'dog\'s name'],
        'display_name': 'Which Dog Most Often Experienced the Issue?',
        'legacy_q_number': 'Q10',
        'is_new': True,
        'is_conditional': True  # Only shown conditionally
    },
    'learn_engagement': {
        'patterns': ['engage', 'Learn training curriculum'],
        'display_name': 'Did You Engage With the Learn Training Curriculum?',
        'legacy_q_number': 'Q11',  # Was Q9, now Q11 after new questions added
        'previous_q_numbers': ['Q9']  # Track previous numbers for reference
    },
    'learn_incomplete_reason': {
        'patterns': ['main reason', 'didn\'t complete', 'Learn curriculum'],
        'display_name': 'What Was the Main Reason You Didn\'t Complete the Learn Curriculum?',
        'legacy_q_number': 'Q12',  # Was Q10, now Q12
        'previous_q_numbers': ['Q10'],
        'prefer_answer': True
    },
    'customer_service_contact': {
        'patterns': ['contact', 'Customer Service', 'Dog Park'],
        'display_name': 'Did You Contact Our Customer Service Team via Dog Park?',
        'legacy_q_number': 'Q13',  # Was Q11, now Q13
        'previous_q_numbers': ['Q11']
    },
    'free_trainer_session': {
        'patterns': ['free session', 'trainer', 'collar effectively'],
        'display_name': 'Would a Free Session With a Trainer Have Helped?',
        'legacy_q_number': 'Q14',  # Was Q12, now Q14
        'previous_q_numbers': ['Q12']
    }
}


def get_question_by_legacy_number(q_number: str) -> Dict[str, any]:
    """
    Get question config by legacy Q# number (for backward compatibility)
    
    Args:
        q_number: Question number like 'Q9' or 'Q11'
        
    Returns:
        Question config dict or None if not found
    """
    for q_id, config in QUESTION_CONFIG.items():
        if config.get('legacy_q_number') == q_number:
            return {**config, 'logical_id': q_id}
    
    # Also check previous numbers
    for q_id, config in QUESTION_CONFIG.items():
        previous_numbers = config.get('previous_q_numbers', [])
        if q_number in previous_numbers:
            return {**config, 'logical_id': q_id}
    
    return None


def get_question_by_logical_id(logical_id: str) -> Dict[str, any]:
    """
    Get question config by logical identifier
    
    Args:
        logical_id: Logical question ID like 'learn_engagement'
        
    Returns:
        Question config dict or None if not found
    """
    if logical_id in QUESTION_CONFIG:
        return {**QUESTION_CONFIG[logical_id], 'logical_id': logical_id}
    return None


def get_all_question_ids() -> List[str]:
    """Get all logical question identifiers"""
    return list(QUESTION_CONFIG.keys())


def get_question_patterns() -> Dict[str, List[str]]:
    """
    Get mapping of logical IDs to search patterns (for backward compatibility)
    Returns format: {'Q2': ['pattern1', 'pattern2'], ...}
    """
    patterns = {}
    for q_id, config in QUESTION_CONFIG.items():
        legacy_q = config.get('legacy_q_number', '')
        if legacy_q:
            patterns[legacy_q] = config['patterns']
    return patterns

