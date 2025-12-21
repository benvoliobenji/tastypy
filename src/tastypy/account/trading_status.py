import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from ..session import Session
from ..errors import translate_error_code


class TradingStatus:
    """Represents the trading status of an account."""

    def __init__(self, account_number: str, active_session: Session):
        self._session = active_session
        self._url_endpoint = f"/accounts/{account_number}/trading-status"

    def sync(self):
        """
        Get the trading status for the account.
        """
        response = self._session.client.get(self._url_endpoint)
        if response.status_code == 200:
            self._trading_status_json = response.json()["data"]
        else:
            error_code = response.status_code
            error_message = response.json()["error"]["message"]
            raise translate_error_code(error_code, error_message)

    @property
    def id(self) -> int:
        return self._trading_status_json.get("id", 0)

    @property
    def account_number(self) -> str:
        return self._trading_status_json.get("account-number", "")

    @property
    def are_deep_itm_carry_options_enabled(self) -> bool:
        return self._trading_status_json.get(
            "are-deep-itm-carry-options-enabled", False
        )

    @property
    def are_far_otm_net_options_restricted(self) -> bool:
        return self._trading_status_json.get(
            "are-far-otm-net-options-restricted", False
        )

    @property
    def are_options_values_restricted_to_nlv(self) -> bool:
        return self._trading_status_json.get(
            "are-options-values-restricted-to-nlv", False
        )

    @property
    def are_single_tick_expiring_hedges_ignored(self) -> bool:
        return self._trading_status_json.get(
            "are-single-tick-expiring-hedges-ignored", False
        )

    @property
    def autotrade_account_type(self) -> str:
        return self._trading_status_json.get("autotrade-account-type", "")

    @property
    def clearing_account_number(self) -> str:
        return self._trading_status_json.get("clearing-account-number", "")

    @property
    def clearing_aggregation_identifier(self) -> str:
        return self._trading_status_json.get("clearing-aggregation-identifier", "")

    @property
    def cmta_override(self) -> int:
        return self._trading_status_json.get("cmta-override", 0)

    @property
    def day_trade_count(self) -> int:
        return self._trading_status_json.get("day-trade-count", 0)

    @property
    def enhanced_fraud_safeguards_enabled_at(self) -> datetime.datetime | None:
        enhanced_fraud_safeguards_str = self._trading_status_json.get(
            "enhanced-fraud-safeguards-enabled-at", ""
        )
        if not enhanced_fraud_safeguards_str:
            return None
        # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
        return datetime.datetime.fromisoformat(
            enhanced_fraud_safeguards_str.replace("Z", "+00:00")
        )

    @property
    def equities_margin_calculation_type(self) -> str:
        return self._trading_status_json.get("equities-margin-calculation-type", "")

    @property
    def ext_crm_id(self) -> str:
        return self._trading_status_json.get("ext-crm-id", "")

    @property
    def fee_schedule_name(self) -> str:
        return self._trading_status_json.get("fee-schedule-name", "")

    @property
    def futures_margin_rate_multiplier(self) -> float:
        value = self._trading_status_json.get("futures-margin-rate-multiplier", 1.0)
        return float(value) if value is not None else 1.0

    @property
    def has_intraday_equities_margin(self) -> bool:
        return self._trading_status_json.get("has-intraday-equities-margin", False)

    @property
    def is_aggregated_at_clearing(self) -> bool:
        return self._trading_status_json.get("is-aggregated-at-clearing", False)

    @property
    def is_closed(self) -> bool:
        return self._trading_status_json.get("is-closed", False)

    @property
    def is_closing_only(self) -> bool:
        return self._trading_status_json.get("is-closing-only", False)

    @property
    def is_cryptocurrency_closing_only(self) -> bool:
        return self._trading_status_json.get("is-cryptocurrency-closing-only", False)

    @property
    def is_cryptocurrency_enabled(self) -> bool:
        return self._trading_status_json.get("is-cryptocurrency-enabled", False)

    @property
    def is_equity_offering_closing_only(self) -> bool:
        return self._trading_status_json.get("is-equity-offering-closing-only", False)

    @property
    def is_equity_offering_enabled(self) -> bool:
        return self._trading_status_json.get("is-equity-offering-enabled", False)

    @property
    def is_frozen(self) -> bool:
        return self._trading_status_json.get("is-frozen", False)

    @property
    def is_full_equity_margin_required(self) -> bool:
        return self._trading_status_json.get("is-full-equity-margin-required", False)

    @property
    def is_futures_closing_only(self) -> bool:
        return self._trading_status_json.get("is-futures-closing-only", False)

    @property
    def is_futures_enabled(self) -> bool:
        return self._trading_status_json.get("is-futures-enabled", False)

    @property
    def is_futures_intra_day_enabled(self) -> bool:
        return self._trading_status_json.get("is-futures-intra-day-enabled", False)

    @property
    def is_in_day_trade_equity_maintenance_call(self) -> bool:
        return self._trading_status_json.get(
            "is-in-day-trade-equity-maintenance-call", False
        )

    @property
    def is_in_margin_call(self) -> bool:
        return self._trading_status_json.get("is-in-margin-call", False)

    @property
    def is_pattern_day_trader(self) -> bool:
        return self._trading_status_json.get("is-pattern-day-trader", False)

    @property
    def is_portfolio_margin_enabled(self) -> bool:
        return self._trading_status_json.get("is-portfolio-margin-enabled", False)

    @property
    def is_risk_reducing_only(self) -> bool:
        return self._trading_status_json.get("is-risk-reducing-only", False)

    @property
    def is_roll_the_day_forward_enabled(self) -> bool:
        return self._trading_status_json.get("is-roll-the-day-forward-enabled", False)

    @property
    def is_small_notional_futures_intra_day_enabled(self) -> bool:
        return self._trading_status_json.get(
            "is-small-notional-futures-intra-day-enabled", False
        )

    @property
    def options_level(self) -> str:
        return self._trading_status_json.get("options-level", "")

    @property
    def pdt_reset_on(self) -> datetime.datetime | None:
        pdt_reset_on_str = self._trading_status_json.get("pdt-reset-on", "")
        if not pdt_reset_on_str:
            return None
        # This is just YYY-MM-DD, unlike above which is ISO
        return datetime.datetime.strptime(pdt_reset_on_str, "%Y-%m-%d")

    @property
    def short_calls_enabled(self) -> bool:
        return self._trading_status_json.get("short-calls-enabled", False)

    @property
    def small_notional_futures_margin_rate_multiplier(self) -> float:
        value = self._trading_status_json.get(
            "small-notional-futures-margin-rate-multiplier", 1.0
        )
        return float(value) if value is not None else 1.0

    @property
    def updated_at(self) -> datetime.datetime | None:
        updated_at_str = self._trading_status_json.get("updated-at", "")
        if not updated_at_str:
            return None
        # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
        return datetime.datetime.fromisoformat(updated_at_str.replace("Z", "+00:00"))

    def print_summary(self) -> None:
        """Print a simple text summary of the trading status."""
        print(f"\n{'=' * 60}")
        print(f"TRADING STATUS SUMMARY: Account {self.account_number}")
        print(f"{'=' * 60}")
        print(f"Account ID: {self.id}")
        print(f"Account Number: {self.account_number}")
        print(f"Options Level: {self.options_level}")
        print(f"Fee Schedule: {self.fee_schedule_name}")
        print(f"Updated At: {self.updated_at}")

        # Account Status
        status_items = []
        if self.is_closed:
            status_items.append("CLOSED")
        if self.is_frozen:
            status_items.append("FROZEN")
        if self.is_closing_only:
            status_items.append("CLOSING ONLY")
        if self.is_risk_reducing_only:
            status_items.append("RISK REDUCING ONLY")
        if self.is_pattern_day_trader:
            status_items.append("PATTERN DAY TRADER")
        if self.is_in_margin_call:
            status_items.append("MARGIN CALL")
        if self.is_in_day_trade_equity_maintenance_call:
            status_items.append("DAY TRADE EQUITY MAINTENANCE CALL")

        account_status = ", ".join(status_items) if status_items else "ACTIVE"
        print(f"Account Status: {account_status}")

        # Trading Permissions
        print(f"Futures Enabled: {'Yes' if self.is_futures_enabled else 'No'}")
        print(
            f"Cryptocurrency Enabled: {'Yes' if self.is_cryptocurrency_enabled else 'No'}"
        )
        print(
            f"Equity Offering Enabled: {'Yes' if self.is_equity_offering_enabled else 'No'}"
        )
        print(
            f"Portfolio Margin: {'Yes' if self.is_portfolio_margin_enabled else 'No'}"
        )
        print(
            f"Intraday Equities Margin: {'Yes' if self.has_intraday_equities_margin else 'No'}"
        )

        # Day Trading
        print(f"Day Trade Count: {self.day_trade_count}")
        if self.pdt_reset_on:
            print(f"PDT Reset Date: {self.pdt_reset_on}")

        # Margin Information
        print(
            f"Futures Margin Rate Multiplier: {self.futures_margin_rate_multiplier:.2f}"
        )
        print(
            f"Small Notional Futures Margin Rate Multiplier: {self.small_notional_futures_margin_rate_multiplier:.2f}"
        )
        print(
            f"Equities Margin Calculation Type: {self.equities_margin_calculation_type}"
        )

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all trading status data in a nicely formatted table."""
        console = Console()

        # Create basic account information table
        basic_table = Table(
            title=f"Trading Status: Account {self.account_number}",
            show_header=True,
            header_style="bold blue",
        )
        basic_table.add_column("Property", style="cyan", no_wrap=True)
        basic_table.add_column("Value", style="green")

        # Basic information
        basic_table.add_row("Account ID", str(self.id))
        basic_table.add_row("Account Number", str(self.account_number))
        basic_table.add_row("Options Level", str(self.options_level))
        basic_table.add_row("Fee Schedule Name", str(self.fee_schedule_name))
        basic_table.add_row(
            "Updated At", str(self.updated_at) if self.updated_at else "N/A"
        )
        basic_table.add_row(
            "Clearing Account Number", str(self.clearing_account_number)
        )
        basic_table.add_row(
            "Clearing Aggregation ID", str(self.clearing_aggregation_identifier)
        )
        basic_table.add_row("Ext CRM ID", str(self.ext_crm_id))
        basic_table.add_row("CMTA Override", str(self.cmta_override))

        # Account status table
        status_table = Table(
            title="Account Status & Restrictions",
            show_header=True,
            header_style="bold red",
        )
        status_table.add_column("Status/Restriction", style="cyan")
        status_table.add_column("Value", style="green")

        status_table.add_row("Is Closed", "✓" if self.is_closed else "✗")
        status_table.add_row("Is Frozen", "✓" if self.is_frozen else "✗")
        status_table.add_row("Is Closing Only", "✓" if self.is_closing_only else "✗")
        status_table.add_row(
            "Is Risk Reducing Only", "✓" if self.is_risk_reducing_only else "✗"
        )
        status_table.add_row(
            "Is Pattern Day Trader", "✓" if self.is_pattern_day_trader else "✗"
        )
        status_table.add_row(
            "Is In Margin Call", "✓" if self.is_in_margin_call else "✗"
        )
        status_table.add_row(
            "Is In Day Trade Equity Maintenance Call",
            "✓" if self.is_in_day_trade_equity_maintenance_call else "✗",
        )
        status_table.add_row(
            "Is Aggregated at Clearing", "✓" if self.is_aggregated_at_clearing else "✗"
        )

        # Trading permissions table
        permissions_table = Table(
            title="Trading Permissions",
            show_header=True,
            header_style="bold green",
        )
        permissions_table.add_column("Permission", style="cyan")
        permissions_table.add_column("Status", style="green")

        permissions_table.add_row(
            "Futures Trading", "✓ Enabled" if self.is_futures_enabled else "✗ Disabled"
        )
        permissions_table.add_row(
            "Futures Closing Only", "✓" if self.is_futures_closing_only else "✗"
        )
        permissions_table.add_row(
            "Futures Intraday",
            "✓ Enabled" if self.is_futures_intra_day_enabled else "✗ Disabled",
        )
        permissions_table.add_row(
            "Small Notional Futures Intraday",
            (
                "✓ Enabled"
                if self.is_small_notional_futures_intra_day_enabled
                else "✗ Disabled"
            ),
        )
        permissions_table.add_row(
            "Cryptocurrency Trading",
            "✓ Enabled" if self.is_cryptocurrency_enabled else "✗ Disabled",
        )
        permissions_table.add_row(
            "Cryptocurrency Closing Only",
            "✓" if self.is_cryptocurrency_closing_only else "✗",
        )
        permissions_table.add_row(
            "Equity Offering",
            "✓ Enabled" if self.is_equity_offering_enabled else "✗ Disabled",
        )
        permissions_table.add_row(
            "Equity Offering Closing Only",
            "✓" if self.is_equity_offering_closing_only else "✗",
        )
        permissions_table.add_row(
            "Short Calls", "✓ Enabled" if self.short_calls_enabled else "✗ Disabled"
        )

        # Margin and options table
        margin_table = Table(
            title="Margin & Options Configuration",
            show_header=True,
            header_style="bold yellow",
        )
        margin_table.add_column("Property", style="cyan")
        margin_table.add_column("Value", style="green")

        margin_table.add_row(
            "Portfolio Margin Enabled", "✓" if self.is_portfolio_margin_enabled else "✗"
        )
        margin_table.add_row(
            "Intraday Equities Margin",
            "✓" if self.has_intraday_equities_margin else "✗",
        )
        margin_table.add_row(
            "Full Equity Margin Required",
            "✓" if self.is_full_equity_margin_required else "✗",
        )
        margin_table.add_row(
            "Equities Margin Calculation Type",
            str(self.equities_margin_calculation_type),
        )
        margin_table.add_row(
            "Futures Margin Rate Multiplier",
            f"{self.futures_margin_rate_multiplier:.2f}",
        )
        margin_table.add_row(
            "Small Notional Futures Margin Rate Multiplier",
            f"{self.small_notional_futures_margin_rate_multiplier:.2f}",
        )

        # Options restrictions table
        options_table = Table(
            title="Options Trading Configuration",
            show_header=True,
            header_style="bold magenta",
        )
        options_table.add_column("Configuration", style="cyan")
        options_table.add_column("Status", style="green")

        options_table.add_row(
            "Deep ITM Carry Options",
            "✓ Enabled" if self.are_deep_itm_carry_options_enabled else "✗ Disabled",
        )
        options_table.add_row(
            "Far OTM Net Options Restricted",
            "✓" if self.are_far_otm_net_options_restricted else "✗",
        )
        options_table.add_row(
            "Options Values Restricted to NLV",
            "✓" if self.are_options_values_restricted_to_nlv else "✗",
        )
        options_table.add_row(
            "Single Tick Expiring Hedges Ignored",
            "✓" if self.are_single_tick_expiring_hedges_ignored else "✗",
        )
        options_table.add_row(
            "Roll the Day Forward Enabled",
            "✓" if self.is_roll_the_day_forward_enabled else "✗",
        )

        # Day trading information table
        day_trading_table = Table(
            title="Day Trading Information",
            show_header=True,
            header_style="bold cyan",
        )
        day_trading_table.add_column("Property", style="cyan")
        day_trading_table.add_column("Value", style="green")

        day_trading_table.add_row("Day Trade Count", str(self.day_trade_count))
        day_trading_table.add_row(
            "PDT Reset Date", str(self.pdt_reset_on) if self.pdt_reset_on else "N/A"
        )
        day_trading_table.add_row(
            "Autotrade Account Type", str(self.autotrade_account_type)
        )
        if self.enhanced_fraud_safeguards_enabled_at:
            day_trading_table.add_row(
                "Enhanced Fraud Safeguards Enabled",
                str(self.enhanced_fraud_safeguards_enabled_at),
            )

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
                status_table,
                title="[bold red]Status & Restrictions[/bold red]",
                border_style="red",
            )
        )
        console.print(
            Panel(
                permissions_table,
                title="[bold green]Trading Permissions[/bold green]",
                border_style="green",
            )
        )
        console.print(
            Panel(
                margin_table,
                title="[bold yellow]Margin Configuration[/bold yellow]",
                border_style="yellow",
            )
        )
        console.print(
            Panel(
                options_table,
                title="[bold magenta]Options Configuration[/bold magenta]",
                border_style="magenta",
            )
        )
        console.print(
            Panel(
                day_trading_table,
                title="[bold cyan]Day Trading Information[/bold cyan]",
                border_style="cyan",
            )
        )

    def __str__(self) -> str:
        return f"TradingStatus(id={self.id}, account_number={self.account_number})"
