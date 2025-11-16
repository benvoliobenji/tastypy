"""Simple orders endpoints."""

from .customer_orders import CustomerOrders
from .orders import Orders

__all__ = ["Orders", "CustomerOrders"]
