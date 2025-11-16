"""Orders module for TastyTrade API."""

# Common models and enums
from .common import (
    ComplexOrder,
    ComplexOrderBuilder,
    ComplexOrderType,
    ConfirmationStatus,
    ContingentStatus,
    InstrumentType,
    Order,
    OrderAction,
    OrderBuilder,
    OrderCondition,
    OrderError,
    OrderFill,
    OrderLeg,
    OrderLegBuilder,
    OrderNote,
    OrderRule,
    OrderStatus,
    OrderType,
    OrderWarning,
    PlacedOrderResponse,
    PriceComponent,
    PriceEffect,
    QuantityDirection,
    RelatedOrder,
    RuleAction,
    RuleComparator,
    RuleIndicator,
    SortOrder,
    TimeInForce,
)

# Complex orders endpoints
from .complex import ComplexOrders

# Simple orders endpoints
from .simple import CustomerOrders, Orders

__all__ = [
    # Endpoint classes
    "Orders",
    "CustomerOrders",
    "ComplexOrders",
    # Builder classes (NEW!)
    "OrderBuilder",
    "OrderLegBuilder",
    "ComplexOrderBuilder",
    # Data models
    "Order",
    "OrderLeg",
    "OrderFill",
    "OrderRule",
    "OrderCondition",
    "PriceComponent",
    "ComplexOrder",
    "RelatedOrder",
    "PlacedOrderResponse",
    "OrderError",
    "OrderNote",
    "OrderWarning",
    # Enums
    "OrderType",
    "TimeInForce",
    "PriceEffect",
    "OrderAction",
    "InstrumentType",
    "OrderStatus",
    "ConfirmationStatus",
    "ContingentStatus",
    "ComplexOrderType",
    "RuleComparator",
    "RuleAction",
    "RuleIndicator",
    "QuantityDirection",
    "SortOrder",
]
