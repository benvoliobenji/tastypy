"""Current margin requirements for an account."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ...errors import translate_error_code
from ...session import Session
from .margin_group import MarginRequirementGroup
from .margin_types import PriceEffect, parse_price_effect
from ...utils.decode_json import parse_float


class MarginRequirements:
    """Represents current margin/capital requirements for an account.

    This class fetches the current margin requirements report from the API.
    """

    def __init__(self, account_number: str, session: Session):
        """Initialize MarginRequirements with account number and session.

        Args:
            account_number: The account number to fetch margin requirements for
            session: Active session with valid authentication
        """
        self._session = session
        self._url_endpoint = f"/margin/accounts/{account_number}/requirements"
        self._requirements_json: dict = {}

    def sync(self) -> None:
        """Fetch current margin/capital requirements report for the account."""
        response = self._session.client.get(self._url_endpoint)
        if response.status_code == 200:
            if not response.text:
                self._requirements_json = {}
                return
            try:
                response_data = response.json()
                self._requirements_json = response_data.get("data", {})
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
    def account_number(self) -> str:
        """Get the account number."""
        return self._requirements_json.get("account-number", "")

    @property
    def description(self) -> str:
        """Get the description of the margin requirements."""
        return self._requirements_json.get("description", "")

    @property
    def margin_requirement(self) -> float:
        """Get the margin requirement amount."""
        return parse_float(self._requirements_json.get("margin-requirement"))

    @property
    def margin_requirement_effect(self) -> PriceEffect | None:
        """Get the margin requirement effect (Debit/Credit)."""
        return parse_price_effect(
            self._requirements_json.get("margin-requirement-effect")
        )

    @property
    def clearing_account_number(self) -> str:
        """Get the clearing account number."""
        return self._requirements_json.get("clearing-account-number", "")

    @property
    def margin_report_type(self) -> str:
        """Get the margin report type."""
        return self._requirements_json.get("margin-report-type", "")

    @property
    def option_level(self) -> str:
        """Get the option level."""
        return self._requirements_json.get("option-level", "")

    @property
    def margin_calculation_type(self) -> str:
        """Get the margin calculation type."""
        return self._requirements_json.get("margin-calculation-type", "")

    @property
    def expected_price_range_up_percent(self) -> float:
        """Get the expected price range up percent."""
        return parse_float(
            self._requirements_json.get("expected-price-range-up-percent")
        )

    @property
    def expected_price_range_down_percent(self) -> float:
        """Get the expected price range down percent."""
        return parse_float(
            self._requirements_json.get("expected-price-range-down-percent")
        )

    @property
    def point_of_no_return_percent(self) -> float:
        """Get the point of no return percent."""
        return parse_float(self._requirements_json.get("point-of-no-return-percent"))

    @property
    def groups(self) -> list[MarginRequirementGroup]:
        """Get the groups of margin requirements.

        Returns:
            List of MarginRequirementGroup objects representing position groups
        """
        groups_data = self._requirements_json.get("groups", [])
        return [MarginRequirementGroup(group) for group in groups_data]

    @property
    def initial_requirement(self) -> float:
        """Get the initial requirement amount."""
        return parse_float(self._requirements_json.get("initial-requirement"))

    @property
    def initial_requirement_effect(self) -> PriceEffect | None:
        """Get the initial requirement effect (Debit/Credit)."""
        return parse_price_effect(
            self._requirements_json.get("initial-requirement-effect")
        )

    @property
    def maintenance_requirement(self) -> float:
        """Get the maintenance requirement amount."""
        return parse_float(self._requirements_json.get("maintenance-requirement"))

    @property
    def maintenance_requirement_effect(self) -> PriceEffect | None:
        """Get the maintenance requirement effect (Debit/Credit)."""
        return parse_price_effect(
            self._requirements_json.get("maintenance-requirement-effect")
        )

    @property
    def margin_equity(self) -> float:
        """Get the margin equity amount."""
        return parse_float(self._requirements_json.get("margin-equity"))

    @property
    def margin_equity_effect(self) -> PriceEffect | None:
        """Get the margin equity effect (Debit/Credit)."""
        return parse_price_effect(self._requirements_json.get("margin-equity-effect"))

    @property
    def option_buying_power(self) -> float:
        """Get the option buying power amount."""
        return parse_float(self._requirements_json.get("option-buying-power"))

    @property
    def option_buying_power_effect(self) -> PriceEffect | None:
        """Get the option buying power effect (Debit/Credit)."""
        return parse_price_effect(
            self._requirements_json.get("option-buying-power-effect")
        )

    @property
    def reg_t_margin_requirement(self) -> float:
        """Get the Reg T margin requirement amount."""
        return parse_float(self._requirements_json.get("reg-t-margin-requirement"))

    @property
    def reg_t_margin_requirement_effect(self) -> PriceEffect | None:
        """Get the Reg T margin requirement effect (Debit/Credit)."""
        return parse_price_effect(
            self._requirements_json.get("reg-t-margin-requirement-effect")
        )

    @property
    def reg_t_option_buying_power(self) -> float:
        """Get the Reg T option buying power amount."""
        return parse_float(self._requirements_json.get("reg-t-option-buying-power"))

    @property
    def reg_t_option_buying_power_effect(self) -> PriceEffect | None:
        """Get the Reg T option buying power effect (Debit/Credit)."""
        return parse_price_effect(
            self._requirements_json.get("reg-t-option-buying-power-effect")
        )

    @property
    def maintenance_excess(self) -> float:
        """Get the maintenance excess amount."""
        return parse_float(self._requirements_json.get("maintenance-excess"))

    @property
    def maintenance_excess_effect(self) -> PriceEffect | None:
        """Get the maintenance excess effect (Debit/Credit)."""
        return parse_price_effect(
            self._requirements_json.get("maintenance-excess-effect")
        )

    @property
    def bond_margin_requirement(self) -> float:
        """Get the bond margin requirement amount."""
        return parse_float(self._requirements_json.get("bond-margin-requirement"))

    @property
    def bond_margin_requirement_effect(self) -> PriceEffect | None:
        """Get the bond margin requirement effect (Debit/Credit)."""
        return parse_price_effect(
            self._requirements_json.get("bond-margin-requirement-effect")
        )

    @property
    def long_bond_value(self) -> float:
        """Get the long bond value amount."""
        return parse_float(self._requirements_json.get("long-bond-value"))

    @property
    def last_state_timestamp(self) -> int:
        """Get the last state timestamp (Unix timestamp in milliseconds)."""
        value = self._requirements_json.get("last-state-timestamp", 0)
        return int(value) if value is not None else 0

    def print_summary(self) -> None:
        """Print a simple text summary of the margin requirements."""
        print(f"Account: {self.account_number}")
        print(f"Description: {self.description}")
        print(f"Margin Calculation Type: {self.margin_calculation_type}")
        print(f"Option Level: {self.option_level}")
        print()

        # Margin Requirements
        margin_effect = (
            str(self.margin_requirement_effect)
            if self.margin_requirement_effect
            else "N/A"
        )
        print(f"Margin Requirement: ${self.margin_requirement:,.2f} ({margin_effect})")

        initial_effect = (
            str(self.initial_requirement_effect)
            if self.initial_requirement_effect
            else "N/A"
        )
        print(
            f"Initial Requirement: ${self.initial_requirement:,.2f} ({initial_effect})"
        )

        maint_effect = (
            str(self.maintenance_requirement_effect)
            if self.maintenance_requirement_effect
            else "N/A"
        )
        print(
            f"Maintenance Requirement: ${self.maintenance_requirement:,.2f} ({maint_effect})"
        )
        print()

        # Buying Power & Equity
        equity_effect = (
            str(self.margin_equity_effect) if self.margin_equity_effect else "N/A"
        )
        print(f"Margin Equity: ${self.margin_equity:,.2f} ({equity_effect})")

        bp_effect = (
            str(self.option_buying_power_effect)
            if self.option_buying_power_effect
            else "N/A"
        )
        print(f"Option Buying Power: ${self.option_buying_power:,.2f} ({bp_effect})")

        excess_effect = (
            str(self.maintenance_excess_effect)
            if self.maintenance_excess_effect
            else "N/A"
        )
        print(f"Maintenance Excess: ${self.maintenance_excess:,.2f} ({excess_effect})")

    def pretty_print(self) -> None:
        """Pretty print the margin requirements using Rich formatting."""
        console = Console()

        # Basic information table
        basic_table = Table(
            title="Account Margin Requirements",
            show_header=True,
            header_style="bold blue",
        )
        basic_table.add_column("Property", style="cyan")
        basic_table.add_column("Value", style="green")

        basic_table.add_row("Account Number", self.account_number)
        basic_table.add_row("Description", self.description)
        if self.clearing_account_number:
            basic_table.add_row("Clearing Account", self.clearing_account_number)
        if self.margin_report_type:
            basic_table.add_row("Margin Report Type", self.margin_report_type)
        basic_table.add_row("Calculation Type", self.margin_calculation_type)
        basic_table.add_row("Option Level", self.option_level)

        # Margin requirements table
        margin_table = Table(
            title="Margin Requirements",
            show_header=True,
            header_style="bold red",
        )
        margin_table.add_column("Type", style="cyan")
        margin_table.add_column("Amount", style="green")
        margin_table.add_column("Effect", style="yellow")

        margin_table.add_row(
            "Total Requirement",
            f"${self.margin_requirement:,.2f}",
            (
                str(self.margin_requirement_effect)
                if self.margin_requirement_effect
                else ""
            ),
        )
        margin_table.add_row(
            "Initial Requirement",
            f"${self.initial_requirement:,.2f}",
            (
                str(self.initial_requirement_effect)
                if self.initial_requirement_effect
                else ""
            ),
        )
        margin_table.add_row(
            "Maintenance Requirement",
            f"${self.maintenance_requirement:,.2f}",
            (
                str(self.maintenance_requirement_effect)
                if self.maintenance_requirement_effect
                else ""
            ),
        )
        margin_table.add_row(
            "Reg T Margin Requirement",
            f"${self.reg_t_margin_requirement:,.2f}",
            (
                str(self.reg_t_margin_requirement_effect)
                if self.reg_t_margin_requirement_effect
                else ""
            ),
        )

        # Equity and buying power table
        equity_table = Table(
            title="Equity & Buying Power",
            show_header=True,
            header_style="bold green",
        )
        equity_table.add_column("Type", style="cyan")
        equity_table.add_column("Amount", style="green")
        equity_table.add_column("Effect", style="yellow")

        equity_table.add_row(
            "Margin Equity",
            f"${self.margin_equity:,.2f}",
            str(self.margin_equity_effect) if self.margin_equity_effect else "",
        )
        equity_table.add_row(
            "Option Buying Power",
            f"${self.option_buying_power:,.2f}",
            (
                str(self.option_buying_power_effect)
                if self.option_buying_power_effect
                else ""
            ),
        )
        equity_table.add_row(
            "Reg T Option Buying Power",
            f"${self.reg_t_option_buying_power:,.2f}",
            (
                str(self.reg_t_option_buying_power_effect)
                if self.reg_t_option_buying_power_effect
                else ""
            ),
        )
        equity_table.add_row(
            "Maintenance Excess",
            f"${self.maintenance_excess:,.2f}",
            (
                str(self.maintenance_excess_effect)
                if self.maintenance_excess_effect
                else ""
            ),
        )

        console.print(Panel(basic_table, border_style="blue"))
        console.print(Panel(margin_table, border_style="red"))
        console.print(Panel(equity_table, border_style="green"))

        # Bonds table (if applicable)
        if self.bond_margin_requirement > 0 or self.long_bond_value > 0:
            bonds_table = Table(
                title="Bonds",
                show_header=True,
                header_style="bold cyan",
            )
            bonds_table.add_column("Type", style="cyan")
            bonds_table.add_column("Amount", style="green")
            bonds_table.add_column("Effect", style="yellow")

            bonds_table.add_row(
                "Bond Margin Requirement",
                f"${self.bond_margin_requirement:,.2f}",
                (
                    str(self.bond_margin_requirement_effect)
                    if self.bond_margin_requirement_effect
                    else ""
                ),
            )
            bonds_table.add_row(
                "Long Bond Value",
                f"${self.long_bond_value:,.2f}",
                "",
            )
            console.print(Panel(bonds_table, border_style="cyan"))

        # Price range table
        if (
            self.expected_price_range_up_percent > 0
            or self.expected_price_range_down_percent > 0
            or self.point_of_no_return_percent > 0
        ):
            range_table = Table(
                title="Expected Price Ranges",
                show_header=True,
                header_style="bold yellow",
            )
            range_table.add_column("Range Type", style="cyan")
            range_table.add_column("Percentage", style="green")

            range_table.add_row(
                "Up Range", f"{self.expected_price_range_up_percent:.2f}%"
            )
            range_table.add_row(
                "Down Range", f"{self.expected_price_range_down_percent:.2f}%"
            )
            range_table.add_row(
                "Point of No Return", f"{self.point_of_no_return_percent:.2f}%"
            )
            console.print(Panel(range_table, border_style="yellow"))

        # Print groups if available
        if self.groups:
            groups_table = Table(
                title="Margin Requirement Groups",
                show_header=True,
                header_style="bold magenta",
            )
            groups_table.add_column("Symbol", style="cyan", width=12)
            groups_table.add_column("Type", style="yellow", width=15)
            groups_table.add_column("Margin Req", style="green", justify="right")
            groups_table.add_column("Initial Req", style="green", justify="right")
            groups_table.add_column("Maint Req", style="green", justify="right")
            groups_table.add_column("Buying Power", style="green", justify="right")

            for group in self.groups:
                groups_table.add_row(
                    group.underlying_symbol,
                    group.margin_calculation_type,
                    f"${group.margin_requirement:,.2f}",
                    f"${group.initial_requirement:,.2f}",
                    f"${group.maintenance_requirement:,.2f}",
                    f"${group.buying_power:,.2f}",
                )

            console.print(Panel(groups_table, border_style="magenta"))
