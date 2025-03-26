"""
This example shows how to enhance agents with custom tools.
Key concepts:
- Creating and registering tools - tool/toolplain
- Accessing context in tools
"""


shipping_info_db: Dict[str, str] = {
    "12345": "shipped on 26/03/2025",
    "67890": "out for delivery",
}