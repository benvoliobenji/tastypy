from ....session import Session
from ....errors import translate_error_code
from ..common.exchanges import Exchange
from ..common.months import FuturesMonth
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class FutureProduct:
    """Represents the futures product endpoint."""

    _endpoint_url = ""
    _session: Session
    _future_product_json: dict

    def __init__(self, active_session: Session):
        self._session = active_session

    @classmethod
    def from_json(cls, active_session: Session, future_product_json: dict):
        """Create a FutureProduct instance from a JSON dictionary."""
        instance = cls(active_session)
        instance._future_product_json = future_product_json
        return instance

    def sync(self, exchange: Exchange, root_symbol: str):
        """Fetch the latest data for futures products."""
        # If the root symbol starts with "/", remove it (protect against user error)
        if root_symbol.startswith("/"):
            root_symbol = root_symbol[1:]

        self._endpoint_url = (
            f"/instruments/future-products/{exchange.value}/{root_symbol}"
        )

        response = self._session._client.get(
            self._endpoint_url,
        )
        if response.status_code == 200:
            data = response.json()
            self._future_product_json = data.get("data", {})
        else:
            error_code = response.status_code
            error_message = response.json().get("error", {}).get("message", "")
            raise translate_error_code(error_code, error_message)

    @property
    def active_months(self) -> list[FuturesMonth]:
        months = self._future_product_json.get("active-months", [])
        return [
            FuturesMonth(month)
            for month in months
            if month in FuturesMonth._value2member_map_
        ]

    @property
    def back_month_first_calendar_symbol(self) -> bool:
        return self._future_product_json.get("back-month-first-calendar-symbol", False)

    @property
    def base_tick(self) -> int:
        return self._future_product_json.get("base-tick", 0)

    @property
    def cash_settled(self) -> bool:
        return self._future_product_json.get("cash-settled", False)

    @property
    def code(self) -> str:
        return self._future_product_json.get("code", "")

    @property
    def contract_limit(self) -> int:
        return self._future_product_json.get("contract-limit", 0)

    @property
    def description(self) -> str:
        return self._future_product_json.get("description", "")

    @property
    def display_factor(self) -> float:
        value = self._future_product_json.get("display-factor", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def exchange(self) -> str:
        return self._future_product_json.get("exchange", "")

    @property
    def first_notice(self) -> bool:
        return self._future_product_json.get("first-notice", False)

    @property
    def listed_months(self) -> list[FuturesMonth]:
        months = self._future_product_json.get("listed-months", "")
        return [
            FuturesMonth(month)
            for month in months
            if month in FuturesMonth._value2member_map_
        ]

    @property
    def market_sector(self) -> str:
        return self._future_product_json.get("market-sector", "")

    @property
    def notional_multiplier(self) -> float:
        value = self._future_product_json.get("notional-multiplier", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def price_format(self) -> str:
        return self._future_product_json.get("price-format", "")

    @property
    def product_subtype(self) -> str:
        return self._future_product_json.get("product-subtype", "")

    @property
    def product_type(self) -> str:
        return self._future_product_json.get("product-type", "")

    @property
    def security_group(self) -> str:
        return self._future_product_json.get("security-group", "")

    @property
    def small_notional(self) -> bool:
        return self._future_product_json.get("small-notional", False)

    @property
    def streamer_exchange_code(self) -> str:
        return self._future_product_json.get("streamer-exchange-code", "")

    @property
    def sub_tick(self) -> int:
        return self._future_product_json.get("sub-tick", 0)

    @property
    def supported(self) -> bool:
        return self._future_product_json.get("supported", False)

    @property
    def root_symbol(self) -> str:
        return self._future_product_json.get("root-symbol", "")

    @property
    def tick_size(self) -> float:
        value = self._future_product_json.get("tick-size", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def true_underlying_code(self) -> str:
        return self._future_product_json.get("true-underlying-code", "")

    @property
    def underlying_description(self) -> str:
        return self._future_product_json.get("underlying-description", "")

    @property
    def underlying_identifier(self) -> str:
        return self._future_product_json.get("underlying-identifier", "")

    def print_summary(self) -> None:
        """Print a simple text summary of the futures product."""
        print(f"\n{'=' * 60}")
        print(f"FUTURES PRODUCT SUMMARY: {self.root_symbol}")
        print(f"{'=' * 60}")
        print(f"Root Symbol: {self.root_symbol}")
        print(f"Code: {self.code}")
        print(f"Description: {self.description}")
        print(f"Exchange: {self.exchange}")
        print(f"Market Sector: {self.market_sector}")

        # Product classification
        print(f"Product Type: {self.product_type}")
        print(f"Product Subtype: {self.product_subtype}")
        print(f"Security Group: {self.security_group}")

        # Trading specifications
        print(f"Supported: {'Yes' if self.supported else 'No'}")
        print(f"Cash Settled: {'Yes' if self.cash_settled else 'No'}")
        print(f"Small Notional: {'Yes' if self.small_notional else 'No'}")
        print(f"Contract Limit: {self.contract_limit}")

        # Pricing information
        print(f"Notional Multiplier: {self.notional_multiplier:,.2f}")
        print(f"Display Factor: {self.display_factor:g}")
        print(f"Tick Size: {self.tick_size:g}")
        print(f"Base Tick: {self.base_tick}")
        print(f"Price Format: {self.price_format}")

        # Month information
        if self.active_months:
            active_months_str = ", ".join([month.name for month in self.active_months])
            print(f"Active Months: {active_months_str}")
        else:
            print("Active Months: None")

        if self.listed_months:
            listed_months_str = ", ".join([month.name for month in self.listed_months])
            print(f"Listed Months: {listed_months_str}")
        else:
            print("Listed Months: None")

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all futures product data in nicely formatted tables."""
        console = Console()

        # Create basic product information table
        basic_table = Table(
            title=f"Futures Product: {self.root_symbol}",
            show_header=True,
            header_style="bold blue",
        )
        basic_table.add_column("Property", style="cyan", no_wrap=True)
        basic_table.add_column("Value", style="green")

        # Basic information
        basic_table.add_row("Root Symbol", str(self.root_symbol))
        basic_table.add_row("Code", str(self.code))
        basic_table.add_row("Description", str(self.description))
        basic_table.add_row("Exchange", str(self.exchange))
        basic_table.add_row("Streamer Exchange Code", str(self.streamer_exchange_code))
        basic_table.add_row("Market Sector", str(self.market_sector))
        basic_table.add_row("Supported", "Yes" if self.supported else "No")

        # Product classification table
        classification_table = Table(
            title="Product Classification",
            show_header=True,
            header_style="bold green",
        )
        classification_table.add_column("Property", style="cyan")
        classification_table.add_column("Value", style="green")

        classification_table.add_row("Product Type", str(self.product_type))
        classification_table.add_row("Product Subtype", str(self.product_subtype))
        classification_table.add_row("Security Group", str(self.security_group))
        classification_table.add_row(
            "True Underlying Code", str(self.true_underlying_code)
        )
        classification_table.add_row(
            "Underlying Identifier", str(self.underlying_identifier)
        )
        classification_table.add_row(
            "Underlying Description", str(self.underlying_description)
        )

        # Contract specifications table
        contract_table = Table(
            title="Contract Specifications",
            show_header=True,
            header_style="bold yellow",
        )
        contract_table.add_column("Property", style="cyan")
        contract_table.add_column("Value", style="green")

        contract_table.add_row("Cash Settled", "Yes" if self.cash_settled else "No")
        contract_table.add_row("Small Notional", "Yes" if self.small_notional else "No")
        contract_table.add_row("First Notice", "Yes" if self.first_notice else "No")
        contract_table.add_row(
            "Back Month First Calendar Symbol",
            "Yes" if self.back_month_first_calendar_symbol else "No",
        )
        contract_table.add_row("Contract Limit", str(self.contract_limit))

        # Pricing specifications table
        pricing_table = Table(
            title="Pricing Specifications",
            show_header=True,
            header_style="bold magenta",
        )
        pricing_table.add_column("Property", style="cyan")
        pricing_table.add_column("Value", style="green")

        pricing_table.add_row("Notional Multiplier", f"{self.notional_multiplier:,.2f}")
        pricing_table.add_row("Display Factor", f"{self.display_factor:g}")
        pricing_table.add_row("Tick Size", f"{self.tick_size:g}")
        pricing_table.add_row("Base Tick", str(self.base_tick))
        pricing_table.add_row("Sub Tick", str(self.sub_tick))
        pricing_table.add_row("Price Format", str(self.price_format))

        # Month information table
        months_table = Table(
            title="Month Information",
            show_header=True,
            header_style="bold cyan",
        )
        months_table.add_column("Property", style="cyan")
        months_table.add_column("Value", style="green")

        # Format active months
        if self.active_months:
            active_months_str = ", ".join([month.name for month in self.active_months])
            months_table.add_row("Active Months", active_months_str)
        else:
            months_table.add_row("Active Months", "None")

        # Format listed months
        if self.listed_months:
            listed_months_str = ", ".join([month.name for month in self.listed_months])
            months_table.add_row("Listed Months", listed_months_str)
        else:
            months_table.add_row("Listed Months", "None")

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
                classification_table,
                title="[bold green]Product Classification[/bold green]",
                border_style="green",
            )
        )

        console.print(
            Panel(
                contract_table,
                title="[bold yellow]Contract Specifications[/bold yellow]",
                border_style="yellow",
            )
        )

        console.print(
            Panel(
                pricing_table,
                title="[bold magenta]Pricing Specifications[/bold magenta]",
                border_style="magenta",
            )
        )

        console.print(
            Panel(
                months_table,
                title="[bold cyan]Month Information[/bold cyan]",
                border_style="cyan",
            )
        )

    def __str__(self):
        return f"FutureProduct({self.root_symbol}): {self.description}"
