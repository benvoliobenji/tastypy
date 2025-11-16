"""Order builder utilities for easier order construction."""

from typing import Any

from .enums import (
    ComplexOrderType,
    InstrumentType,
    OrderAction,
    OrderType,
    PriceEffect,
    RuleComparator,
    TimeInForce,
)


class OrderLegBuilder:
    """Builder for creating order legs with a fluent API."""

    def __init__(self) -> None:
        """Initialize an empty order leg."""
        self._leg_data: dict[str, Any] = {}

    def equity(self, symbol: str) -> "OrderLegBuilder":
        """
        Set leg to trade an equity.

        Args:
            symbol: The equity symbol (e.g., "AAPL", "MSFT")

        Returns:
            Self for method chaining
        """
        self._leg_data["instrument-type"] = InstrumentType.EQUITY.value
        self._leg_data["symbol"] = symbol
        return self

    def equity_option(self, symbol: str) -> "OrderLegBuilder":
        """
        Set leg to trade an equity option.

        Args:
            symbol: The OCC option symbol (e.g., "AAPL  251219C00200000")

        Returns:
            Self for method chaining
        """
        self._leg_data["instrument-type"] = InstrumentType.EQUITY_OPTION.value
        self._leg_data["symbol"] = symbol
        return self

    def future(self, symbol: str) -> "OrderLegBuilder":
        """
        Set leg to trade a future.

        Args:
            symbol: The future symbol (e.g., "/ESZ24")

        Returns:
            Self for method chaining
        """
        self._leg_data["instrument-type"] = InstrumentType.FUTURE.value
        self._leg_data["symbol"] = symbol
        return self

    def future_option(self, symbol: str) -> "OrderLegBuilder":
        """
        Set leg to trade a future option.

        Args:
            symbol: The future option symbol

        Returns:
            Self for method chaining
        """
        self._leg_data["instrument-type"] = InstrumentType.FUTURE_OPTION.value
        self._leg_data["symbol"] = symbol
        return self

    def cryptocurrency(self, symbol: str) -> "OrderLegBuilder":
        """
        Set leg to trade cryptocurrency.

        Args:
            symbol: The cryptocurrency symbol (e.g., "BTC/USD")

        Returns:
            Self for method chaining
        """
        self._leg_data["instrument-type"] = InstrumentType.CRYPTOCURRENCY.value
        self._leg_data["symbol"] = symbol
        return self

    def quantity(self, qty: int) -> "OrderLegBuilder":
        """
        Set the quantity for this leg.

        Args:
            qty: Number of contracts/shares

        Returns:
            Self for method chaining
        """
        self._leg_data["quantity"] = qty
        return self

    def buy_to_open(self) -> "OrderLegBuilder":
        """Set action to Buy to Open (opening long position)."""
        self._leg_data["action"] = OrderAction.BUY_TO_OPEN.value
        return self

    def buy_to_close(self) -> "OrderLegBuilder":
        """Set action to Buy to Close (closing short position)."""
        self._leg_data["action"] = OrderAction.BUY_TO_CLOSE.value
        return self

    def sell_to_open(self) -> "OrderLegBuilder":
        """Set action to Sell to Open (opening short position)."""
        self._leg_data["action"] = OrderAction.SELL_TO_OPEN.value
        return self

    def sell_to_close(self) -> "OrderLegBuilder":
        """Set action to Sell to Close (closing long position)."""
        self._leg_data["action"] = OrderAction.SELL_TO_CLOSE.value
        return self

    def buy(self) -> "OrderLegBuilder":
        """Set action to Buy (generic buy)."""
        self._leg_data["action"] = OrderAction.BUY.value
        return self

    def sell(self) -> "OrderLegBuilder":
        """Set action to Sell (generic sell)."""
        self._leg_data["action"] = OrderAction.SELL.value
        return self

    def build(self) -> dict[str, Any]:
        """
        Build and return the leg dictionary.

        Returns:
            Dictionary representing the order leg
        """
        return self._leg_data.copy()


class OrderBuilder:
    """Builder for creating orders with a fluent API."""

    def __init__(self) -> None:
        """Initialize an empty order."""
        self._order_data: dict[str, Any] = {"legs": []}

    def limit(self, price: float) -> "OrderBuilder":
        """
        Set order as a limit order.

        Args:
            price: Limit price

        Returns:
            Self for method chaining
        """
        self._order_data["order-type"] = OrderType.LIMIT.value
        self._order_data["price"] = str(price)
        return self

    def market(self) -> "OrderBuilder":
        """Set order as a market order."""
        self._order_data["order-type"] = OrderType.MARKET.value
        return self

    def stop(self, trigger_price: float) -> "OrderBuilder":
        """
        Set order as a stop order.

        Args:
            trigger_price: Price that triggers the stop

        Returns:
            Self for method chaining
        """
        self._order_data["order-type"] = OrderType.STOP.value
        self._order_data["stop-trigger"] = str(trigger_price)
        return self

    def stop_limit(self, trigger_price: float, limit_price: float) -> "OrderBuilder":
        """
        Set order as a stop-limit order.

        Args:
            trigger_price: Price that triggers the order
            limit_price: Limit price once triggered

        Returns:
            Self for method chaining
        """
        self._order_data["order-type"] = OrderType.STOP_LIMIT.value
        self._order_data["stop-trigger"] = str(trigger_price)
        self._order_data["price"] = str(limit_price)
        return self

    def day(self) -> "OrderBuilder":
        """Set time-in-force to Day (expires at market close)."""
        self._order_data["time-in-force"] = TimeInForce.DAY.value
        return self

    def gtc(self) -> "OrderBuilder":
        """Set time-in-force to Good-Til-Cancelled."""
        self._order_data["time-in-force"] = TimeInForce.GTC.value
        return self

    def gtd(self, expiration_date: str) -> "OrderBuilder":
        """
        Set time-in-force to Good-Til-Date.

        Args:
            expiration_date: Date string in format "YYYY-MM-DD"

        Returns:
            Self for method chaining
        """
        self._order_data["time-in-force"] = TimeInForce.GTD.value
        self._order_data["gtc-date"] = expiration_date
        return self

    def ioc(self) -> "OrderBuilder":
        """Set time-in-force to Immediate-or-Cancel."""
        self._order_data["time-in-force"] = TimeInForce.IOC.value
        return self

    def debit(self) -> "OrderBuilder":
        """Set price effect to Debit (paying for the order)."""
        self._order_data["price-effect"] = PriceEffect.DEBIT.value
        return self

    def credit(self) -> "OrderBuilder":
        """Set price effect to Credit (receiving payment)."""
        self._order_data["price-effect"] = PriceEffect.CREDIT.value
        return self

    def add_leg(self, leg_builder: OrderLegBuilder) -> "OrderBuilder":
        """
        Add a leg to the order.

        Args:
            leg_builder: OrderLegBuilder instance with configured leg

        Returns:
            Self for method chaining
        """
        self._order_data["legs"].append(leg_builder.build())
        return self

    def partition_quantity(self, quantity: int) -> "OrderBuilder":
        """
        Set partition quantity for PAIRS orders.

        Args:
            quantity: The partition quantity

        Returns:
            Self for method chaining
        """
        self._order_data["partition-quantity"] = quantity
        return self

    def value(self, notional_value: str) -> "OrderBuilder":
        """
        Set notional value for notional market orders.

        Args:
            notional_value: The notional value amount

        Returns:
            Self for method chaining
        """
        self._order_data["value"] = notional_value
        return self

    def build(self) -> dict[str, Any]:
        """
        Build and return the order dictionary.

        Returns:
            Dictionary representing the order
        """
        return self._order_data.copy()


class ComplexOrderBuilder:
    """Builder for creating complex orders (OCO, OTO, OTOCO, PAIRS, BLAST)."""

    def __init__(self, order_type: ComplexOrderType) -> None:
        """
        Initialize a complex order builder.

        Args:
            order_type: The type of complex order (OCO, OTO, OTOCO, PAIRS, BLAST)
        """
        self._complex_data: dict[str, Any] = {
            "type": order_type.value,
            "orders": [],
        }

    @staticmethod
    def oco() -> "ComplexOrderBuilder":
        """
        Create an OCO (One-Cancels-Other) order builder.

        In an OCO order, when one order fills, the other is automatically cancelled.

        Returns:
            ComplexOrderBuilder for OCO orders
        """
        return ComplexOrderBuilder(ComplexOrderType.OCO)

    @staticmethod
    def oto() -> "ComplexOrderBuilder":
        """
        Create an OTO (One-Triggers-Other) order builder.

        In an OTO order, when the first order fills, it triggers the second order.

        Returns:
            ComplexOrderBuilder for OTO orders
        """
        return ComplexOrderBuilder(ComplexOrderType.OTO)

    @staticmethod
    def otoco() -> "ComplexOrderBuilder":
        """
        Create an OTOCO (One-Triggers-OCO) order builder.

        Combines OTO and OCO: first order triggers two orders that are OCO with each other.

        Returns:
            ComplexOrderBuilder for OTOCO orders
        """
        return ComplexOrderBuilder(ComplexOrderType.OTOCO)

    @staticmethod
    def pairs() -> "ComplexOrderBuilder":
        """
        Create a PAIRS order builder.

        Returns:
            ComplexOrderBuilder for PAIRS orders
        """
        return ComplexOrderBuilder(ComplexOrderType.PAIRS)

    @staticmethod
    def blast() -> "ComplexOrderBuilder":
        """
        Create a BLAST order builder.

        Returns:
            ComplexOrderBuilder for BLAST orders
        """
        return ComplexOrderBuilder(ComplexOrderType.BLAST)

    def add_order(self, order_builder: OrderBuilder) -> "ComplexOrderBuilder":
        """
        Add an order component to the complex order.

        Args:
            order_builder: OrderBuilder instance with configured order

        Returns:
            Self for method chaining
        """
        self._complex_data["orders"].append(order_builder.build())
        return self

    def trigger_order(self, order_builder: OrderBuilder) -> "ComplexOrderBuilder":
        """
        Set the trigger order for OTO/OTOCO orders.

        Args:
            order_builder: OrderBuilder for the trigger order

        Returns:
            Self for method chaining
        """
        self._complex_data["trigger-order"] = order_builder.build()
        return self

    def ratio_price_threshold(
        self, comparator: RuleComparator, threshold: float
    ) -> "ComplexOrderBuilder":
        """
        Set ratio price threshold for PAIRS orders.

        Args:
            comparator: The comparison operator (LTE or GTE)
            threshold: The threshold value

        Returns:
            Self for method chaining
        """
        self._complex_data["ratio-price-comparator"] = comparator.value
        self._complex_data["ratio-price-threshold"] = str(threshold)
        return self

    def build(self) -> dict[str, Any]:
        """
        Build and return the complex order dictionary.

        Returns:
            Dictionary representing the complex order
        """
        return self._complex_data.copy()
