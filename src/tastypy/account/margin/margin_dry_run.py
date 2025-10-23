"""Margin requirements dry-run estimation for hypothetical orders."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ...errors import translate_error_code
from ...session import Session
from .margin_order_leg import MarginRequirementLeg
from .margin_types import PriceEffect, parse_price_effect
from ...utils.decode_json import parse_float


class MarginRequirementsDryRun:
    """Estimate margin requirements for an order without placing it.

    This class allows you to test how an order would affect margin requirements
    before actually placing the order (dry-run).
    """

    def __init__(self, account_number: str, session: Session):
        """Initialize MarginRequirementsDryRun with account number and session.

        Args:
            account_number: The account number to estimate margin requirements for
            session: Active session with valid authentication
        """
        self._session = session
        self._url_endpoint = f"/margin/accounts/{account_number}/dry-run"
        self._account_number = account_number
        self._dry_run_json: dict = {}

    def estimate(
        self,
        underlying_symbol: str,
        order_type: str,
        time_in_force: str,
        legs: list[MarginRequirementLeg],
        gtc_date: str | None = None,
        price: str | None = None,
        price_effect: PriceEffect | None = None,
        stop_trigger: str | None = None,
        replaces_order_id: str | None = None,
    ) -> None:
        """Estimate margin requirements for a hypothetical order.

        Args:
            underlying_symbol: The underlying symbol for the order
            order_type: Type of order (e.g., "Limit", "Market")
            time_in_force: Time in force (e.g., "Day", "GTC")
            legs: List of MarginRequirementLeg objects (minimum 1, maximum 4, must be unique)
            gtc_date: Good-til-canceled date (format: YYYY-MM-DD)
            price: Limit price for the order
            price_effect: PriceEffect.CREDIT or PriceEffect.DEBIT
            stop_trigger: Stop trigger price
            replaces_order_id: ID of order being replaced

        Raises:
            ValueError: If legs list is invalid (not 1-4 legs or contains duplicates)
            Exception: If the API request fails
        """
        # Validate legs requirements
        if not legs or len(legs) < 1:
            raise ValueError("At least 1 leg is required")
        if len(legs) > 4:
            raise ValueError("Maximum of 4 legs allowed")

        # Check for unique legs
        if len(legs) != len(set(legs)):
            raise ValueError("All legs must be unique")

        # Convert legs to dict format for API
        legs_data = [leg.to_dict() for leg in legs]

        order_data = {
            "account-number": self._account_number,
            "underlying-symbol": underlying_symbol,
            "order-type": order_type,
            "time-in-force": time_in_force,
            "legs": legs_data,
        }

        # Add optional parameters
        if gtc_date:
            order_data["gtc-date"] = gtc_date
        if price:
            order_data["price"] = price
        if price_effect:
            order_data["price-effect"] = price_effect.value
        if stop_trigger:
            order_data["stop-trigger"] = stop_trigger
        if replaces_order_id:
            order_data["replaces-order-id"] = replaces_order_id

        response = self._session.client.post(self._url_endpoint, json=order_data)
        if response.status_code == 200:
            if not response.text:
                self._dry_run_json = {}
                return
            try:
                response_data = response.json()
                self._dry_run_json = response_data.get("data", {})
            except Exception as e:
                raise Exception(
                    f"Failed to parse response: {e}. Response text: {response.text[:200]}"
                )
        else:
            error_code = response.status_code
            try:
                error_message = (
                    response.json().get("error", {}).get("message", "Unknown error")
                )
            except Exception:
                error_message = f"HTTP {error_code}: {response.text[:200]}"
            raise translate_error_code(error_code, error_message)

    @property
    def change_in_margin_requirement(self) -> float:
        """Get the change in margin requirement amount."""
        return parse_float(self._dry_run_json.get("change-in-margin-requirement"))

    @property
    def change_in_margin_requirement_effect(self) -> PriceEffect | None:
        """Get the change in margin requirement effect (Debit/Credit)."""
        return parse_price_effect(
            self._dry_run_json.get("change-in-margin-requirement-effect")
        )

    @property
    def isolated_order_margin_requirement(self) -> float:
        """Get the isolated order margin requirement amount."""
        return parse_float(self._dry_run_json.get("isolated-order-margin-requirement"))

    @property
    def isolated_order_margin_requirement_effect(self) -> PriceEffect | None:
        """Get the isolated order margin requirement effect (Debit/Credit)."""
        return parse_price_effect(
            self._dry_run_json.get("isolated-order-margin-requirement-effect")
        )

    @property
    def current_buying_power(self) -> float:
        """Get the current buying power amount."""
        return parse_float(self._dry_run_json.get("current-buying-power"))

    @property
    def current_buying_power_effect(self) -> PriceEffect | None:
        """Get the current buying power effect (Debit/Credit)."""
        return parse_price_effect(self._dry_run_json.get("current-buying-power-effect"))

    @property
    def new_buying_power(self) -> float:
        """Get the new buying power amount after the order."""
        return parse_float(self._dry_run_json.get("new-buying-power"))

    @property
    def new_buying_power_effect(self) -> PriceEffect | None:
        """Get the new buying power effect (Debit/Credit)."""
        return parse_price_effect(self._dry_run_json.get("new-buying-power-effect"))

    @property
    def change_in_buying_power(self) -> float:
        """Get the change in buying power amount."""
        return parse_float(self._dry_run_json.get("change-in-buying-power"))

    @property
    def change_in_buying_power_effect(self) -> PriceEffect | None:
        """Get the change in buying power effect (Debit/Credit)."""
        return parse_price_effect(
            self._dry_run_json.get("change-in-buying-power-effect")
        )

    @property
    def is_spread(self) -> bool:
        """Check if the order is a spread."""
        return bool(self._dry_run_json.get("is-spread", False))

    @property
    def sufficient(self) -> bool:
        """Check if buying power is sufficient for the order."""
        return bool(self._dry_run_json.get("sufficient", False))

    @property
    def current_maintenance_buying_power(self) -> float:
        """Get the current maintenance buying power amount."""
        return parse_float(self._dry_run_json.get("current-maintenance-buying-power"))

    @property
    def current_maintenance_buying_power_effect(self) -> PriceEffect | None:
        """Get the current maintenance buying power effect (Debit/Credit)."""
        return parse_price_effect(
            self._dry_run_json.get("current-maintenance-buying-power-effect")
        )

    @property
    def current_sma_buying_power(self) -> float:
        """Get the current SMA (Special Memorandum Account) buying power amount."""
        return parse_float(self._dry_run_json.get("current-sma-buying-power"))

    @property
    def current_sma_buying_power_effect(self) -> PriceEffect | None:
        """Get the current SMA buying power effect (Debit/Credit)."""
        return parse_price_effect(
            self._dry_run_json.get("current-sma-buying-power-effect")
        )

    @property
    def current_individual_account_buying_power(self) -> float:
        """Get the current individual account buying power amount."""
        return parse_float(
            self._dry_run_json.get("current-individual-account-buying-power")
        )

    @property
    def current_individual_account_buying_power_effect(self) -> PriceEffect | None:
        """Get the current individual account buying power effect (Debit/Credit)."""
        return parse_price_effect(
            self._dry_run_json.get("current-individual-account-buying-power-effect")
        )

    @property
    def new_individual_account_buying_power(self) -> float:
        """Get the new individual account buying power amount after the order."""
        return parse_float(
            self._dry_run_json.get("new-individual-account-buying-power")
        )

    @property
    def new_individual_account_buying_power_effect(self) -> PriceEffect | None:
        """Get the new individual account buying power effect (Debit/Credit)."""
        return parse_price_effect(
            self._dry_run_json.get("new-individual-account-buying-power-effect")
        )

    @property
    def change_in_sma(self) -> float:
        """Get the change in SMA (Special Memorandum Account) amount."""
        return parse_float(self._dry_run_json.get("change-in-sma"))

    @property
    def change_in_sma_effect(self) -> PriceEffect | None:
        """Get the change in SMA effect (Debit/Credit)."""
        return parse_price_effect(self._dry_run_json.get("change-in-sma-effect"))

    @property
    def change_in_base_buying_power(self) -> float:
        """Get the change in base buying power amount."""
        return parse_float(self._dry_run_json.get("change-in-base-buying-power"))

    @property
    def change_in_base_buying_power_effect(self) -> PriceEffect | None:
        """Get the change in base buying power effect (Debit/Credit)."""
        return parse_price_effect(
            self._dry_run_json.get("change-in-base-buying-power-effect")
        )

    @property
    def change_in_rolled_buying_power(self) -> float:
        """Get the change in rolled buying power amount."""
        return parse_float(self._dry_run_json.get("change-in-rolled-buying-power"))

    @property
    def change_in_rolled_buying_power_effect(self) -> PriceEffect | None:
        """Get the change in rolled buying power effect (Debit/Credit)."""
        return parse_price_effect(
            self._dry_run_json.get("change-in-rolled-buying-power-effect")
        )

    @property
    def isolated_order_buying_power_effect(self) -> float:
        """Get the isolated order buying power effect amount."""
        return parse_float(self._dry_run_json.get("isolated-order-buying-power-effect"))

    @property
    def isolated_order_buying_power_effect_effect(self) -> PriceEffect | None:
        """Get the isolated order buying power effect effect (Debit/Credit)."""
        return parse_price_effect(
            self._dry_run_json.get("isolated-order-buying-power-effect-effect")
        )

    @property
    def change_in_long_derivative_value(self) -> float:
        """Get the change in long derivative value amount."""
        return parse_float(self._dry_run_json.get("change-in-long-derivative-value"))

    @property
    def change_in_short_derivative_value(self) -> float:
        """Get the change in short derivative value amount."""
        return parse_float(self._dry_run_json.get("change-in-short-derivative-value"))

    def print_summary(self) -> None:
        """Print a simple text summary of the estimated margin requirements."""
        print("=== Estimated Margin Requirements (Dry Run) ===")
        print(f"Sufficient Buying Power: {self.sufficient}")
        print(f"Is Spread: {self.is_spread}")
        print()

        change_effect_str = (
            str(self.change_in_margin_requirement_effect)
            if self.change_in_margin_requirement_effect
            else "N/A"
        )
        print(
            f"Change in Margin Requirement: ${self.change_in_margin_requirement:,.2f} ({change_effect_str})"
        )

        isolated_effect_str = (
            str(self.isolated_order_margin_requirement_effect)
            if self.isolated_order_margin_requirement_effect
            else "N/A"
        )
        print(
            f"Isolated Order Margin: ${self.isolated_order_margin_requirement:,.2f} ({isolated_effect_str})"
        )
        print()

        current_bp_effect = (
            str(self.current_buying_power_effect)
            if self.current_buying_power_effect
            else "N/A"
        )
        print(
            f"Current Buying Power: ${self.current_buying_power:,.2f} ({current_bp_effect})"
        )

        new_bp_effect = (
            str(self.new_buying_power_effect) if self.new_buying_power_effect else "N/A"
        )
        print(f"New Buying Power: ${self.new_buying_power:,.2f} ({new_bp_effect})")

        change_bp_effect = (
            str(self.change_in_buying_power_effect)
            if self.change_in_buying_power_effect
            else "N/A"
        )
        print(
            f"Change in Buying Power: ${self.change_in_buying_power:,.2f} ({change_bp_effect})"
        )

    def pretty_print(self) -> None:
        """Pretty print the estimated margin requirements using Rich formatting."""
        console = Console()

        # Order validation info
        validation_table = Table(
            title="Order Validation",
            show_header=True,
            header_style="bold blue",
        )
        validation_table.add_column("Property", style="cyan")
        validation_table.add_column("Value", style="green")

        validation_table.add_row(
            "Sufficient Buying Power",
            "[green]Yes[/green]" if self.sufficient else "[red]No[/red]",
        )
        validation_table.add_row("Is Spread", "Yes" if self.is_spread else "No")

        # Margin impact table
        margin_table = Table(
            title="Margin Impact",
            show_header=True,
            header_style="bold red",
        )
        margin_table.add_column("Type", style="cyan")
        margin_table.add_column("Amount", style="green")
        margin_table.add_column("Effect", style="yellow")

        margin_table.add_row(
            "Change in Margin Requirement",
            f"${self.change_in_margin_requirement:,.2f}",
            (
                str(self.change_in_margin_requirement_effect)
                if self.change_in_margin_requirement_effect
                else ""
            ),
        )
        margin_table.add_row(
            "Isolated Order Margin",
            f"${self.isolated_order_margin_requirement:,.2f}",
            (
                str(self.isolated_order_margin_requirement_effect)
                if self.isolated_order_margin_requirement_effect
                else ""
            ),
        )

        # Buying power table
        bp_table = Table(
            title="Buying Power",
            show_header=True,
            header_style="bold green",
        )
        bp_table.add_column("Type", style="cyan")
        bp_table.add_column("Amount", style="green")
        bp_table.add_column("Effect", style="yellow")

        bp_table.add_row(
            "Current Buying Power",
            f"${self.current_buying_power:,.2f}",
            (
                str(self.current_buying_power_effect)
                if self.current_buying_power_effect
                else ""
            ),
        )
        bp_table.add_row(
            "New Buying Power",
            f"${self.new_buying_power:,.2f}",
            str(self.new_buying_power_effect) if self.new_buying_power_effect else "",
        )
        bp_table.add_row(
            "Change in Buying Power",
            f"${self.change_in_buying_power:,.2f}",
            (
                str(self.change_in_buying_power_effect)
                if self.change_in_buying_power_effect
                else ""
            ),
        )

        console.print(Panel(validation_table, border_style="blue"))
        console.print(Panel(margin_table, border_style="red"))
        console.print(Panel(bp_table, border_style="green"))
