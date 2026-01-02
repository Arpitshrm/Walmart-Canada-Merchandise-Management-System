"""
Walmart Sales Analytics - Advanced Functions & Lambda
"""

from tabulate import tabulate
from typing import Dict, List, Tuple
import inventory

def calculate_revenue(sales: List[Tuple[str, int]]) -> float:
    """Calculate total revenue from sales list"""
    total = 0.0
    for item_name, qty in sales:
        # Lambda for price lookup
        get_price = lambda name: next((item[2] for item in inventory.INVENTORY 
                                     if item[0] == name), 0)
        total += get_price(item_name) * qty
    return total

def top_sellers(sales: List[Tuple[str, int]], top_n: int = 3) -> List[Tuple[str, float]]:
    """Returns top N selling items by revenue"""
    revenue_dict = {}
    for item, qty in sales:
        price = next((i[2] for i in inventory.INVENTORY if i[0] == item), 0)
        revenue_dict[item] = revenue_dict.get(item, 0) + (price * qty)
    
    # Sort by revenue (descending)
    sorted_items = sorted(revenue_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_items[:top_n]

def generate_report(sales: List[Tuple[str, int]]) -> str:
    """Generates formatted sales report"""
    revenue = calculate_revenue(sales)
    top3 = top_sellers(sales)
    
    table_data = []
    for item, rev in top3:
        table_data.append([item, f"${rev:.2f}"])
    
    report = f"""
📊 WALMART TORONTO - DAILY REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Revenue: ${revenue:.2f} CAD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 TOP SELLERS:
{tabulate(table_data, headers=["Item", "Revenue"], tablefmt="grid")}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return report

# Advanced function with *args, **kwargs
def apply_discounts(*customers: str, discount_pct: float = 0.10, **extra_items: float) -> Dict:
    """Bulk discount calculator"""
    results = {}
    base_discount = discount_pct
    for customer in customers:
        results[customer] = base_discount
    results.update(extra_items)  # merge kwargs
    return results
