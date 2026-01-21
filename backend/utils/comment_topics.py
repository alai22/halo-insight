"""
Comment Topic Taxonomy Configuration

Defines the categories used for multi-label classification of customer support comments.
Each comment can be tagged with multiple topics.
"""

# Topic taxonomy for comment classification
# Each topic has a name, description, and keywords to help LLM identify it
# Note: We focus on actionable issue categories, not sentiment (positive/negative)
COMMENT_TOPICS = [
    {
        "id": "battery_charging",
        "name": "Battery & Charging Issues",
        "description": "Power, charging, battery life problems",
        "keywords": ["battery", "charging", "won't charge", "not charging", "power", "dead", "drain"]
    },
    {
        "id": "hardware_malfunction",
        "name": "Hardware Malfunction",
        "description": "Device not working, technical failures, collar issues",
        "keywords": ["not working", "broken", "malfunction", "defective", "technical issue", "stopped working"]
    },
    {
        "id": "gps_location",
        "name": "GPS & Location Accuracy",
        "description": "Tracking, location, GPS problems",
        "keywords": ["gps", "location", "tracking", "accuracy", "inaccurate", "wrong location", "can't find"]
    },
    {
        "id": "warranty_replacement",
        "name": "Warranty & Replacement",
        "description": "Replacement requests, warranty claims",
        "keywords": ["replacement", "warranty", "replace", "exchange", "send back", "return old"]
    },
    {
        "id": "returns_refunds",
        "name": "Returns & Refunds",
        "description": "Return requests, refund inquiries",
        "keywords": ["return", "refund", "money back", "return label", "send back"]
    },
    {
        "id": "shipping_delivery",
        "name": "Shipping & Delivery",
        "description": "Order status, delivery issues",
        "keywords": ["shipping", "delivery", "order", "tracking", "shipped", "arrived", "address"]
    },
    {
        "id": "billing_subscription",
        "name": "Billing & Subscription",
        "description": "Payment, subscription, pricing issues",
        "keywords": ["billing", "subscription", "payment", "charge", "cancel subscription", "expensive", "price"]
    },
    {
        "id": "account_login",
        "name": "Account & Login Issues",
        "description": "Account access, login problems",
        "keywords": ["account", "login", "password", "sign in", "can't access", "locked out"]
    },
    {
        "id": "feature_howto",
        "name": "Feature Questions & How-To",
        "description": "Usage help, feature inquiries, setup questions",
        "keywords": ["how to", "how do I", "feature", "setting", "configure", "setup", "use"]
    },
    {
        "id": "dog_training",
        "name": "Dog Training & Behavior",
        "description": "Collar effectiveness, dog response, training",
        "keywords": ["dog", "training", "respond", "behavior", "doesn't work on dog", "collar effectiveness"]
    },
    {
        "id": "wait_time",
        "name": "Wait Time & Response Delay",
        "description": "Long wait times, slow response, delayed callbacks",
        "keywords": ["wait", "hold", "long time", "slow", "delayed", "took forever", "hours"]
    },
    {
        "id": "life_situation_change",
        "name": "Life Situation Change",
        "description": "Customer circumstances changed",
        "keywords": ["no longer", "passed away", "gave away", "moving", "situation changed", "don't need"]
    },
    {
        "id": "product_recommendation",
        "name": "Product Recommendations",
        "description": "Purchasing advice, product questions",
        "keywords": ["recommend", "which one", "best", "accessories", "purchase", "buy"]
    },
    {
        "id": "phone_support",
        "name": "Phone Support Request",
        "description": "Wants to speak to someone by phone",
        "keywords": ["phone", "call", "speak to someone", "talk to", "call back"]
    },
    {
        "id": "other",
        "name": "Other",
        "description": "Doesn't fit other categories",
        "keywords": []
    }
]

# Get topic IDs as a list (for validation)
TOPIC_IDS = [topic["id"] for topic in COMMENT_TOPICS]

# Get topic names for display
TOPIC_NAMES = {topic["id"]: topic["name"] for topic in COMMENT_TOPICS}

# Build LLM prompt section with topic definitions
def get_topic_definitions_for_prompt():
    """Generate topic definitions text for LLM prompt"""
    lines = []
    for topic in COMMENT_TOPICS:
        keywords_str = ", ".join(topic["keywords"]) if topic["keywords"] else "general catch-all"
        lines.append(f'- {topic["id"]}: {topic["name"]} - {topic["description"]} (keywords: {keywords_str})')
    return "\n".join(lines)

# Color palette for topics (for UI visualization)
TOPIC_COLORS = {
    "battery_charging": "#EF4444",      # Red
    "hardware_malfunction": "#F97316",   # Orange
    "gps_location": "#F59E0B",           # Amber
    "warranty_replacement": "#EAB308",   # Yellow
    "returns_refunds": "#84CC16",        # Lime
    "shipping_delivery": "#22C55E",      # Green
    "billing_subscription": "#14B8A6",   # Teal
    "account_login": "#06B6D4",          # Cyan
    "feature_howto": "#0EA5E9",          # Sky
    "dog_training": "#3B82F6",           # Blue
    "wait_time": "#6366F1",              # Indigo
    "life_situation_change": "#8B5CF6",  # Violet
    "product_recommendation": "#A855F7", # Purple
    "phone_support": "#D946EF",          # Fuchsia
    "other": "#6B7280",                  # Gray
}
