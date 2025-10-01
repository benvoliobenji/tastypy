from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class FutureOptionProduct:
    """Represents a futures option product."""

    _future_option_product_json: dict

    def __init__(self, future_option_product_json: dict):
        self._future_option_product_json = future_option_product_json

    @property
    def cash_settled(self) -> bool:
        return self._future_option_product_json.get("cash-settled", False)

    @property
    def code(self) -> str:
        return self._future_option_product_json.get("code", "")

    @property
    def display_factor(self) -> float:
        value = self._future_option_product_json.get("display-factor", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def exchange(self) -> str:
        return self._future_option_product_json.get("exchange", "")

    @property
    def expiration_type(self) -> str:
        return self._future_option_product_json.get("expiration-type", "")

    @property
    def is_am_settled(self) -> bool:
        return self._future_option_product_json.get("is-am-settled", False)

    @property
    def itm_rule(self) -> str:
        return self._future_option_product_json.get("itm-rule", "")

    @property
    def market_sector(self) -> str:
        return self._future_option_product_json.get("market-sector", "")

    @property
    def product_subtype(self) -> str:
        return self._future_option_product_json.get("product-subtype", "")

    @property
    def root_symbol(self) -> str:
        return self._future_option_product_json.get("root-symbol", "")

    @property
    def settlement_delay_days(self) -> int:
        return self._future_option_product_json.get("settlement-delay-days", 0)

    @property
    def supported(self) -> bool:
        return self._future_option_product_json.get("supported", False)

    def __str__(self) -> str:
        return f"FutureOptionProduct({self.code}): {self.root_symbol} - {self.exchange}"

    def print_summary(self) -> None:
        """Print a simple text summary of the futures option product."""
        print(f"\n{'=' * 60}")
        print(f"FUTURES OPTION PRODUCT SUMMARY: {self.code}")
        print(f"{'=' * 60}")
        print(f"Code: {self.code}")
        print(f"Root Symbol: {self.root_symbol}")
        print(f"Exchange: {self.exchange}")
        print(f"Market Sector: {self.market_sector}")
        print(f"Product Subtype: {self.product_subtype}")

        # Settlement information
        print(f"Cash Settled: {self.cash_settled}")
        print(f"Is AM Settled: {self.is_am_settled}")
        print(f"Settlement Delay Days: {self.settlement_delay_days}")
        print(f"Expiration Type: {self.expiration_type}")

        # Trading information
        print(f"Supported: {self.supported}")
        print(f"Display Factor: {self.display_factor:g}")
        print(f"ITM Rule: {self.itm_rule}")

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all futures option product data in nicely formatted tables."""
        console = Console()

        # Create basic product information table
        basic_table = Table(
            title=f"Futures Option Product: {self.code}",
            show_header=True,
            header_style="bold blue",
        )
        basic_table.add_column("Property", style="cyan", no_wrap=True)
        basic_table.add_column("Value", style="green")

        # Basic information
        basic_table.add_row("Code", str(self.code))
        basic_table.add_row("Root Symbol", str(self.root_symbol))
        basic_table.add_row("Exchange", str(self.exchange))
        basic_table.add_row("Market Sector", str(self.market_sector))
        basic_table.add_row("Product Subtype", str(self.product_subtype))
        basic_table.add_row("Supported", "Yes" if self.supported else "No")

        # Settlement specifications table
        settlement_table = Table(
            title="Settlement Specifications",
            show_header=True,
            header_style="bold green",
        )
        settlement_table.add_column("Property", style="cyan")
        settlement_table.add_column("Value", style="green")

        settlement_table.add_row("Cash Settled", "Yes" if self.cash_settled else "No")
        settlement_table.add_row("Is AM Settled", "Yes" if self.is_am_settled else "No")
        settlement_table.add_row(
            "Settlement Delay Days", str(self.settlement_delay_days)
        )
        settlement_table.add_row("Expiration Type", str(self.expiration_type))

        # Trading specifications table
        trading_table = Table(
            title="Trading Specifications",
            show_header=True,
            header_style="bold yellow",
        )
        trading_table.add_column("Property", style="cyan")
        trading_table.add_column("Value", style="green")

        trading_table.add_row("Display Factor", f"{self.display_factor:g}")
        trading_table.add_row("ITM Rule", str(self.itm_rule))

        # Print all tables
        console.print(
            Panel(
                basic_table,
                title="[bold blue]Basic Information[/bold blue]",
                border_style="blue",
            )
        )

        console.print(
            Panel(
                settlement_table,
                title="[bold green]Settlement Specifications[/bold green]",
                border_style="green",
            )
        )

        console.print(
            Panel(
                trading_table,
                title="[bold yellow]Trading Specifications[/bold yellow]",
                border_style="yellow",
            )
        )
