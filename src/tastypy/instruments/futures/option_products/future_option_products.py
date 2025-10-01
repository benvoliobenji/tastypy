from ....session import Session
from ....errors import translate_error_code
from ..common.future_option_product import FutureOptionProduct
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class FutureOptionProducts:
    _endpoint_url = ""
    _session: Session
    _future_option_product: FutureOptionProduct

    def __init__(self, active_session: Session):
        self._session = active_session

    def sync(self, exchange: str, root_symbol: str):
        """Fetch the latest data for future option products."""
        self._endpoint_url = (
            f"/instruments/future-option-products/{exchange}/{root_symbol}"
        )

        response = self._session._client.get(
            self._endpoint_url,
        )
        if response.status_code == 200:
            data = response.json()
            data_dict = data.get("data", {})
            self._future_option_product = FutureOptionProduct(data_dict)
        else:
            error_code = response.status_code
            error_message = response.json().get("error", {}).get("message", "")
            raise translate_error_code(error_code, error_message)

    @property
    def product(self) -> FutureOptionProduct:
        """Get the currently loaded future option product."""
        if not hasattr(self, "_future_option_product"):
            raise ValueError("No future option product data loaded. Call sync() first.")
        return self._future_option_product

    def print_summary(self) -> None:
        """Print a simple text summary of the future option products data."""
        print(f"\n{'=' * 60}")
        print("FUTURE OPTION PRODUCTS SUMMARY")
        print(f"{'=' * 60}")

        if hasattr(self, "_future_option_product"):
            print("Product Loaded: Yes")
            print(f"Product Code: {self.product.code}")
            print(f"Root Symbol: {self.product.root_symbol}")
            print(f"Exchange: {self.product.exchange}")
            print(f"Market Sector: {self.product.market_sector}")
            print(f"Product Subtype: {self.product.product_subtype}")
            print(f"Supported: {'Yes' if self.product.supported else 'No'}")
            print(f"Cash Settled: {'Yes' if self.product.cash_settled else 'No'}")
            print(f"Is AM Settled: {'Yes' if self.product.is_am_settled else 'No'}")
            print(f"Display Factor: {self.product.display_factor:g}")
            print(f"Expiration Type: {self.product.expiration_type}")
            print(f"ITM Rule: {self.product.itm_rule}")
        else:
            print("Product Loaded: No - Call sync() first")
            print("No product data available")

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print the future option products data in nicely formatted tables."""
        console = Console()

        # Check if data is loaded
        if not hasattr(self, "_future_option_product"):
            error_table = Table(
                title="Future Option Products",
                show_header=True,
                header_style="bold red",
            )
            error_table.add_column("Status", style="red", justify="center")
            error_table.add_row("No data loaded - Please call sync() first")

            console.print(
                Panel(
                    error_table,
                    title="[bold red]Error[/bold red]",
                    border_style="red",
                )
            )
            return

        # Create overview table
        overview_table = Table(
            title="Future Option Products Overview",
            show_header=True,
            header_style="bold blue",
        )
        overview_table.add_column("Property", style="cyan", no_wrap=True)
        overview_table.add_column("Value", style="green")

        overview_table.add_row("Data Status", "✓ Loaded Successfully")
        overview_table.add_row("Product Code", str(self.product.code))
        overview_table.add_row("Root Symbol", str(self.product.root_symbol))
        overview_table.add_row("Exchange", str(self.product.exchange))
        overview_table.add_row("Market Sector", str(self.product.market_sector))
        overview_table.add_row("Product Subtype", str(self.product.product_subtype))

        console.print(
            Panel(
                overview_table,
                title="[bold blue]Overview[/bold blue]",
                border_style="blue",
            )
        )

        # Show detailed product information using the product's pretty_print method
        console.print("\n[bold white]📊 Detailed Product Information:[/bold white]\n")
        self.product.pretty_print()

    def __str__(self):
        return "FutureOptionProducts"
