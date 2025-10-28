from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tastypy.market_metrics.option_expiration_implied_volatility import (
    OptionExpirationImpliedVolatility,
)
from tastypy.utils.decode_json import parse_float


class MarketMetricInfo:
    """Dataclass containing volatility and liquidity data for a symbol."""

    def __init__(self, data: dict[str, Any]) -> None:
        """
        Initialize market metric info from JSON data.

        Args:
            data: Dictionary containing market metric data from API.
        """
        self._data = data
        self._option_expirations: list[OptionExpirationImpliedVolatility] = []

        # Parse option expiration implied volatilities
        option_exp_data = self._data.get("option-expiration-implied-volatilities", [])
        self._option_expirations = [
            OptionExpirationImpliedVolatility(exp_data) for exp_data in option_exp_data
        ]

    @property
    def symbol(self) -> str:
        """Symbol."""
        return self._data.get("symbol", "")

    @property
    def implied_volatility_index(self) -> float:
        """IV Index of underlying."""
        return parse_float(self._data.get("implied-volatility-index"), 0.0)

    @property
    def implied_volatility_index_5_day_change(self) -> float:
        """5 day change of IV index of underlying."""
        return parse_float(self._data.get("implied-volatility-index-5-day-change"), 0.0)

    @property
    def implied_volatility_rank(self) -> float:
        """IV Rank of underlying."""
        return parse_float(self._data.get("implied-volatility-rank"), 0.0)

    @property
    def implied_volatility_percentile(self) -> float:
        """IV percentile of underlying."""
        return parse_float(self._data.get("implied-volatility-percentile"), 0.0)

    @property
    def liquidity(self) -> float:
        """Liquidity of underlying."""
        return parse_float(self._data.get("liquidity"), 0.0)

    @property
    def liquidity_rank(self) -> float:
        """Liquidity rank of underlying."""
        return parse_float(self._data.get("liquidity-rank"), 0.0)

    @property
    def liquidity_rating(self) -> int:
        """Liquidity rating of underlying."""
        value = self._data.get("liquidity-rating", 0)
        return int(value) if value is not None else 0

    @property
    def option_expiration_implied_volatilities(
        self,
    ) -> list[OptionExpirationImpliedVolatility]:
        """List of option volatility data."""
        return self._option_expirations

    def print_summary(self) -> None:
        """Print a plain text summary of the market metric."""
        print(f"\n{'=' * 80}")
        print(f"Market Metrics for {self.symbol}")
        print(f"{'=' * 80}")
        print(f"  IV Index: {self.implied_volatility_index * 100:.2f}%")
        print(
            f"  IV Index 5-Day Change: {self.implied_volatility_index_5_day_change * 100:.2f}%"
        )
        print(f"  IV Rank: {self.implied_volatility_rank * 100:.2f}%")
        print(f"  IV Percentile: {self.implied_volatility_percentile * 100:.2f}%")
        print(f"  Liquidity: {self.liquidity:.4f}")
        print(f"  Liquidity Rank: {self.liquidity_rank:.4f}")
        print(f"  Liquidity Rating: {self.liquidity_rating}")
        print(f"  Option Expirations: {len(self._option_expirations)}")
        if self._option_expirations:
            print("  Option Expiration IV Data:")
            for exp in self._option_expirations[:5]:  # Show first 5
                exp.print_summary()
            if len(self._option_expirations) > 5:
                print(f"  ... and {len(self._option_expirations) - 5} more")
        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of the market metric."""
        console = Console()

        # Main metrics table
        metrics_table = Table(
            title=f"Market Metrics for {self.symbol}",
            show_header=True,
            header_style="bold cyan",
        )
        metrics_table.add_column("Metric", style="cyan", no_wrap=True)
        metrics_table.add_column("Value", style="magenta")

        metrics_table.add_row("IV Index", f"{self.implied_volatility_index * 100:.2f}%")
        metrics_table.add_row(
            "IV Index 5-Day Change",
            f"{self.implied_volatility_index_5_day_change * 100:.2f}%",
        )
        metrics_table.add_row("IV Rank", f"{self.implied_volatility_rank * 100:.2f}%")
        metrics_table.add_row(
            "IV Percentile", f"{self.implied_volatility_percentile * 100:.2f}%"
        )
        metrics_table.add_row("Liquidity", f"{self.liquidity:.4f}")
        metrics_table.add_row("Liquidity Rank", f"{self.liquidity_rank:.4f}")
        metrics_table.add_row("Liquidity Rating", str(self.liquidity_rating))

        console.print(
            Panel(
                metrics_table,
                title=f"[bold blue]{self.symbol} Metrics[/bold blue]",
                border_style="blue",
            )
        )

        # Option expirations table
        if self._option_expirations:
            exp_table = Table(
                title=f"Option Expiration IVs ({len(self._option_expirations)} expirations)",
                show_header=True,
                header_style="bold green",
            )
            exp_table.add_column("Expiration Date", style="cyan")
            exp_table.add_column("Settlement", style="yellow")
            exp_table.add_column("Chain Type", style="magenta")
            exp_table.add_column("Implied Vol", style="green", justify="right")

            for exp in self._option_expirations[:10]:  # Show first 10
                exp_date_str = (
                    exp.expiration_date.strftime("%Y-%m-%d")
                    if exp.expiration_date
                    else "N/A"
                )
                exp_table.add_row(
                    exp_date_str,
                    exp.settlement_type,
                    exp.option_chain_type,
                    f"{exp.implied_volatility * 100:.2f}%",
                )

            if len(self._option_expirations) > 10:
                exp_table.add_row(
                    "...",
                    "...",
                    "...",
                    f"({len(self._option_expirations) - 10} more)",
                    style="dim",
                )

            console.print(
                Panel(
                    exp_table,
                    title="[bold green]Option Expiration Volatilities[/bold green]",
                    border_style="green",
                )
            )
