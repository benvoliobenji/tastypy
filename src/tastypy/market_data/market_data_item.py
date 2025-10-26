"""MarketDataItem class for market data module."""

import datetime
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tastypy.market_data.enums import ClosePriceType, InstrumentType
from tastypy.utils.decode_json import parse_float, parse_date


class MarketDataItem:
    """Dataclass containing market data for a single symbol."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize market data item from JSON data."""
        self._data = data

    @property
    def symbol(self) -> str:
        """Symbol for this market data."""
        return self._data.get("symbol", "")

    @property
    def instrument_type(self) -> InstrumentType:
        """Type of instrument."""
        value = self._data.get("instrument-type", "")
        return InstrumentType(value) if value else InstrumentType.EQUITY

    @property
    def updated_at(self) -> datetime.datetime | None:
        """Timestamp when data was last updated."""
        value = self._data.get("updated-at")
        if value:
            return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return None

    @property
    def bid(self) -> float | None:
        """Bid price."""
        value = self._data.get("bid")
        return parse_float(value) if value is not None else None

    @property
    def bid_size(self) -> float:
        """Bid size."""
        return parse_float(self._data.get("bid-size"), 0.0)

    @property
    def ask(self) -> float | None:
        """Ask price."""
        value = self._data.get("ask")
        return parse_float(value) if value is not None else None

    @property
    def ask_size(self) -> float:
        """Ask size."""
        return parse_float(self._data.get("ask-size"), 0.0)

    @property
    def mid(self) -> float | None:
        """Mid price."""
        value = self._data.get("mid")
        return parse_float(value) if value is not None else None

    @property
    def mark(self) -> float:
        """Mark price."""
        return parse_float(self._data.get("mark"), 0.0)

    @property
    def last(self) -> float | None:
        """Last price."""
        value = self._data.get("last")
        return parse_float(value) if value is not None else None

    @property
    def last_ext(self) -> float | None:
        """Last extended hours price."""
        value = self._data.get("last-ext")
        return parse_float(value) if value is not None else None

    @property
    def last_mkt(self) -> float | None:
        """Last market price."""
        value = self._data.get("last-mkt")
        return parse_float(value) if value is not None else None

    @property
    def beta(self) -> float | None:
        """Beta value."""
        value = self._data.get("beta")
        return parse_float(value) if value is not None else None

    @property
    def dividend_amount(self) -> float | None:
        """Dividend amount."""
        value = self._data.get("dividend-amount")
        return parse_float(value) if value is not None else None

    @property
    def dividend_frequency(self) -> float | None:
        """Dividend frequency."""
        value = self._data.get("dividend-frequency")
        return parse_float(value) if value is not None else None

    @property
    def open(self) -> float | None:
        """Open price."""
        value = self._data.get("open")
        return parse_float(value) if value is not None else None

    @property
    def day_high_price(self) -> float | None:
        """Day high price."""
        value = self._data.get("day-high-price")
        return parse_float(value) if value is not None else None

    @property
    def day_low_price(self) -> float | None:
        """Day low price."""
        value = self._data.get("day-low-price")
        return parse_float(value) if value is not None else None

    @property
    def close(self) -> float | None:
        """Close price."""
        value = self._data.get("close")
        return parse_float(value) if value is not None else None

    @property
    def close_price_type(self) -> ClosePriceType:
        """Type of close price."""
        value = self._data.get("close-price-type", "Unknown")
        try:
            return ClosePriceType(value)
        except ValueError:
            return ClosePriceType.UNKNOWN

    @property
    def prev_close(self) -> float | None:
        """Previous close price."""
        value = self._data.get("prev-close")
        return parse_float(value) if value is not None else None

    @property
    def prev_close_price_type(self) -> ClosePriceType:
        """Type of previous close price."""
        value = self._data.get("prev-close-price-type", "Unknown")
        try:
            return ClosePriceType(value)
        except ValueError:
            return ClosePriceType.UNKNOWN

    @property
    def summary_date(self) -> datetime.date | None:
        """Summary date."""
        value = self._data.get("summary-date")
        return parse_date(value)

    @property
    def prev_close_date(self) -> datetime.date | None:
        """Previous close date."""
        value = self._data.get("prev-close-date")
        return parse_date(value)

    @property
    def low_limit_price(self) -> float | None:
        """Low limit price."""
        value = self._data.get("low-limit-price")
        return parse_float(value) if value is not None else None

    @property
    def high_limit_price(self) -> float | None:
        """High limit price."""
        value = self._data.get("high-limit-price")
        return parse_float(value) if value is not None else None

    @property
    def trading_halted_reason(self) -> str | None:
        """Reason for trading halt."""
        value = self._data.get("trading-halted-reason")
        return value if value else None

    @property
    def halt_start_time(self) -> int:
        """Halt start time."""
        return int(self._data.get("halt-start-time", -1))

    @property
    def halt_end_time(self) -> int:
        """Halt end time."""
        return int(self._data.get("halt-end-time", -1))

    @property
    def year_low_price(self) -> float | None:
        """52-week low price."""
        value = self._data.get("year-low-price")
        return parse_float(value) if value is not None else None

    @property
    def year_high_price(self) -> float | None:
        """52-week high price."""
        value = self._data.get("year-high-price")
        return parse_float(value) if value is not None else None

    @property
    def volume(self) -> float | None:
        """Volume."""
        value = self._data.get("volume")
        return parse_float(value) if value is not None else None

    @property
    def is_trading_halted(self) -> bool | None:
        """Whether trading is halted."""
        value = self._data.get("is-trading-halted")
        return bool(value) if value is not None else None

    def print_summary(self) -> None:
        """Print a plain text summary of the market data item."""
        print(f"\n{self.symbol} ({self.instrument_type.value})")
        print(f"  Mark: ${self.mark}")
        if self.bid and self.ask:
            print(f"  Bid/Ask: ${self.bid} / ${self.ask}")
        if self.last:
            print(f"  Last: ${self.last}")
        if self.volume:
            print(f"  Volume: {self.volume}")
        if self.day_high_price and self.day_low_price:
            print(f"  Day Range: ${self.day_low_price} - ${self.day_high_price}")
        if self.prev_close:
            print(f"  Prev Close: ${self.prev_close}")
        if self.updated_at:
            print(f"  Updated: {self.updated_at}")

    def pretty_print(self) -> None:
        """Print a rich formatted output of the market data item."""
        console = Console()

        # Create main table
        table = Table(
            title=f"{self.symbol} Market Data",
            show_header=True,
            header_style="bold blue",
        )
        table.add_column("Field", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        # Basic info
        table.add_row("Symbol", str(self.symbol))
        table.add_row("Type", str(self.instrument_type.value))
        table.add_row("Mark", f"${self.mark:.2f}")

        # Bid/Ask
        if self.bid and self.ask:
            table.add_row("Bid", f"${self.bid:.2f}")
            table.add_row("Ask", f"${self.ask:.2f}")
            table.add_row("Bid Size", f"{self.bid_size}")
            table.add_row("Ask Size", f"{self.ask_size}")

        # Price info
        if self.last:
            table.add_row("Last", f"${self.last:.2f}")
        if self.close:
            table.add_row("Close", f"${self.close:.2f}")
        if self.prev_close:
            table.add_row("Prev Close", f"${self.prev_close:.2f}")

        # Day range
        if self.day_high_price and self.day_low_price:
            table.add_row("Day High", f"${self.day_high_price:.2f}")
            table.add_row("Day Low", f"${self.day_low_price:.2f}")

        # Volume
        if self.volume:
            table.add_row("Volume", f"{self.volume:,.0f}")

        # Updated time
        if self.updated_at:
            table.add_row("Updated", str(self.updated_at))

        console.print(Panel(table, border_style="blue"))
