import enum
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..errors import translate_error_code
from ..session import Session
import datetime


class Currency(enum.Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"

    def __str__(self):
        return self.value


class Balance:
    """Represents a user's account balance. Note this is different from snapshot as this is the most current values."""

    _url_endpoint = ""
    _session: Session
    _currency: Currency = Currency.USD

    def __init__(self, account_number: str, active_session: Session):
        self._session = active_session
        self._url_endpoint = f"/accounts/{account_number}/balances"

    def sync(self, currency: Currency = Currency.USD):
        self._currency = currency
        true_url_endpoint = self._url_endpoint + f"/{currency.value}"
        response = self._session.client.get(true_url_endpoint)
        if response.status_code == 200:
            self._balance_json = response.json()["data"]
        else:
            error_code = response.status_code
            error_message = response.json()["error"]["message"]
            raise translate_error_code(error_code, error_message)

    @property
    def account_number(self) -> str:
        return self._balance_json.get("account-number", "")

    @property
    def available_trading_funds(self) -> float:
        value = self._balance_json.get("available-trading-funds", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def bond_margin_requirement(self) -> float:
        value = self._balance_json.get("bond-margin-requirement", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def cash_available_to_withdraw(self) -> float:
        value = self._balance_json.get("cash-available-to-withdraw", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def cash_balance(self) -> float:
        value = self._balance_json.get("cash-balance", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def cash_settle_balance(self) -> float:
        value = self._balance_json.get("cash-settle-balance", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def closed_loop_available_balance(self) -> float:
        value = self._balance_json.get("closed-loop-available-balance", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def cryptocurrency_margin_requirement(self) -> float:
        value = self._balance_json.get("cryptocurrency-margin-requirement", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def currency(self) -> str:
        return self._balance_json.get("currency", "")

    @property
    def day_equity_call_value(self) -> float:
        value = self._balance_json.get("day-equity-call-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def day_trade_excess(self) -> float:
        value = self._balance_json.get("day-trade-excess", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def day_trading_buying_power(self) -> float:
        value = self._balance_json.get("day-trading-buying-power", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def day_trading_call_value(self) -> float:
        value = self._balance_json.get("day-trading-call-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def derivative_buying_power(self) -> float:
        value = self._balance_json.get("derivative-buying-power", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def equity_buying_power(self) -> float:
        value = self._balance_json.get("equity-buying-power", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def equity_offering_margin_requirement(self) -> float:
        value = self._balance_json.get("equity-offering-margin-requirement", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def fixed_income_security_margin_requirement(self) -> float:
        value = self._balance_json.get("fixed-income-security-margin-requirement", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def intraday_equities_cash_amount(self) -> float:
        value = self._balance_json.get("intraday-equities-cash-amount", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def intraday_equities_cash_effect(self) -> str:
        return self._balance_json.get("intraday-equities-cash-effect", "")

    @property
    def intraday_equities_cash_effective_date(self) -> datetime.date | None:
        intraday_equities_cash_effective_date_str = self._balance_json.get(
            "intraday-equities-cash-effective-date", ""
        )
        if not intraday_equities_cash_effective_date_str:
            return None
        # This is just YYY-MM-DD
        return datetime.datetime.strptime(
            intraday_equities_cash_effective_date_str, "%Y-%m-%d"
        ).date()

    @property
    def intraday_futures_cash_amount(self) -> float:
        value = self._balance_json.get("intraday-futures-cash-amount", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def intraday_futures_cash_effect(self) -> str:
        return self._balance_json.get("intraday-futures-cash-effect", "")

    @property
    def intraday_futures_cash_effective_date(self) -> datetime.date | None:
        intraday_futures_cash_effective_date_str = self._balance_json.get(
            "intraday-futures-cash-effective-date", ""
        )
        if not intraday_futures_cash_effective_date_str:
            return None
        # This is just YYY-MM-DD
        return datetime.datetime.strptime(
            intraday_futures_cash_effective_date_str, "%Y-%m-%d"
        ).date()

    @property
    def long_bond_value(self) -> float:
        value = self._balance_json.get("long-bond-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def long_cryptocurrency_value(self) -> float:
        value = self._balance_json.get("long-cryptocurrency-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def long_equity_value(self) -> float:
        value = self._balance_json.get("long-equity-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def long_fixed_income_security_value(self) -> float:
        value = self._balance_json.get("long-fixed-income-security-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def long_futures_derivative_value(self) -> float:
        value = self._balance_json.get("long-futures-derivative-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def long_futures_value(self) -> float:
        value = self._balance_json.get("long-futures-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def long_margineable_value(self) -> float:
        value = self._balance_json.get("long-margineable-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def maintenance_call_value(self) -> float:
        value = self._balance_json.get("maintenance-call-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def maintenance_requirement(self) -> float:
        value = self._balance_json.get("maintenance-requirement", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def margin_equity(self) -> float:
        value = self._balance_json.get("margin-equity", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def margin_settle_balance(self) -> float:
        value = self._balance_json.get("margin-settle-balance", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def net_liquidating_value(self) -> float:
        value = self._balance_json.get("net-liquidating-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def pending_cash(self) -> float:
        value = self._balance_json.get("pending-cash", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def pending_cash_effect(self) -> str:
        return self._balance_json.get("pending-cash-effect", "")

    @property
    def previous_day_cryptocurrency_fiat_amount(self) -> float:
        value = self._balance_json.get("previous-day-cryptocurrency-fiat-amount", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def previous_day_cryptocurrency_fiat_effect(self) -> str:
        return self._balance_json.get("previous-day-cryptocurrency-fiat-effect", "")

    @property
    def reg_t_call_value(self) -> float:
        value = self._balance_json.get("reg-t-call-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def short_cryptocurrency_value(self) -> float:
        value = self._balance_json.get("short-cryptocurrency-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def short_derivative_value(self) -> float:
        value = self._balance_json.get("short-derivative-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def short_equity_value(self) -> float:
        value = self._balance_json.get("short-equity-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def short_futures_derivative_value(self) -> float:
        value = self._balance_json.get("short-futures-derivative-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def short_futures_value(self) -> float:
        value = self._balance_json.get("short-futures-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def short_marginable_value(self) -> float:
        value = self._balance_json.get("short-margineable-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def sma_equity_option_buying_power(self) -> float:
        value = self._balance_json.get("sma-equity-option-buying-power", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def special_memorandum_account_apex_adjustment(self) -> float:
        value = self._balance_json.get(
            "special-memorandum-account-apex-adjustment", 0.0
        )
        return float(value) if value is not None else 0.0

    @property
    def special_memorandum_account_value(self) -> float:
        value = self._balance_json.get("special-memorandum-account-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def total_settle_balance(self) -> float:
        value = self._balance_json.get("total-settle-balance", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def unsettled_cryptocurrency_fiat_effect(self) -> str:
        return self._balance_json.get("unsettled-cryptocurrency-fiat-effect", "")

    @property
    def used_derivative_buying_power(self) -> float:
        value = self._balance_json.get("used-derivative-buying-power", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def shapshot_date(self) -> datetime.date | None:
        snapshot_date = self._balance_json.get("snapshot-date", "")
        if not snapshot_date:
            return None
        # This is just YYY-MM-DD
        return datetime.datetime.strptime(snapshot_date, "%Y-%m-%d").date()

    @property
    def time_of_day(self) -> str:
        return self._balance_json.get("time-of-day", "")

    @property
    def reg_t_margin_requirement(self) -> float:
        value = self._balance_json.get("reg-t-margin-requirement", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def futures_overnight_margin_requirement(self) -> float:
        value = self._balance_json.get("futures-overnight-margin-requirement", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def futures_intraday_margin_requirement(self) -> float:
        value = self._balance_json.get("futures-intraday-margin-requirement", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def maintenance_excess(self) -> float:
        value = self._balance_json.get("maintenance-excess", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def pending_margin_interest(self) -> float:
        value = self._balance_json.get("pending-margin-interest", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def apex_starting_day_margin_equity(self) -> float:
        value = self._balance_json.get("apex-starting-day-margin-equity", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def buying_power_adjustment(self) -> float:
        value = self._balance_json.get("buying-power-adjustment", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def buying_power_adjustment_effect(self) -> str:
        return self._balance_json.get("buying-power-adjustment-effect", "")

    @property
    def total_pending_liquidity_poll_rebate(self) -> float:
        value = self._balance_json.get("total-pending-liquidity-poll-rebate", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def long_index_derivative_value(self) -> float:
        value = self._balance_json.get("long-index-derivative-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def short_index_derivative_value(self) -> float:
        value = self._balance_json.get("short-index-derivative-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def updated_at(self) -> datetime.datetime | None:
        updated_at = self._balance_json.get("updated-at", "")
        if not updated_at:
            return None
        # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
        return datetime.datetime.fromisoformat(updated_at.replace("Z", "+00:00"))

    def __str__(self):
        return f"Balance({self.account_number}): {self.net_liquidating_value} {self.currency}"

    def print_summary(self) -> None:
        """Print a simple text summary of the balance."""
        print(f"\n{'=' * 60}")
        print(f"BALANCE SUMMARY: Account {self.account_number}")
        print(f"{'=' * 60}")
        print(f"Account Number: {self.account_number}")
        print(f"Currency: {self.currency}")
        print(f"Snapshot Date: {self.shapshot_date}")
        print(f"Time of Day: {self.time_of_day}")
        print(f"Updated At: {self.updated_at}")

        # Get currency symbol for formatting
        currency_symbol = "$" if self.currency == "USD" else self.currency

        # Key balances
        print(
            f"Net Liquidating Value: {currency_symbol}{self.net_liquidating_value:,.2f}"
        )
        print(f"Cash Balance: {currency_symbol}{self.cash_balance:,.2f}")
        print(
            f"Available Trading Funds: {currency_symbol}{self.available_trading_funds:,.2f}"
        )
        print(
            f"Cash Available to Withdraw: {currency_symbol}{self.cash_available_to_withdraw:,.2f}"
        )

        # Buying power
        print(f"Equity Buying Power: {currency_symbol}{self.equity_buying_power:,.2f}")
        print(
            f"Day Trading Buying Power: {currency_symbol}{self.day_trading_buying_power:,.2f}"
        )
        print(
            f"Derivative Buying Power: {currency_symbol}{self.derivative_buying_power:,.2f}"
        )

        # Margin information
        print(f"Margin Equity: {currency_symbol}{self.margin_equity:,.2f}")
        print(
            f"Maintenance Requirement: {currency_symbol}{self.maintenance_requirement:,.2f}"
        )

        # Position values
        total_long_value = (
            self.long_equity_value
            + self.long_futures_derivative_value
            + self.long_futures_value
            + self.long_cryptocurrency_value
        )
        total_short_value = (
            self.short_derivative_value
            + self.short_equity_value
            + self.short_futures_derivative_value
            + self.short_futures_value
            + self.short_cryptocurrency_value
        )
        print(f"Total Long Position Value: {currency_symbol}{total_long_value:,.2f}")
        print(f"Total Short Position Value: {currency_symbol}{total_short_value:,.2f}")

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all balance data in a nicely formatted table."""
        console = Console()

        # Get currency symbol for formatting
        currency_symbol = "$" if self.currency == "USD" else self.currency

        # Create basic account information table
        basic_table = Table(
            title=f"Balance: Account {self.account_number}",
            show_header=True,
            header_style="bold blue",
        )
        basic_table.add_column("Property", style="cyan", no_wrap=True)
        basic_table.add_column("Value", style="green")

        # Basic information
        basic_table.add_row("Account Number", str(self.account_number))
        basic_table.add_row("Currency", str(self.currency))
        basic_table.add_row(
            "Snapshot Date", str(self.shapshot_date) if self.shapshot_date else "N/A"
        )
        basic_table.add_row("Time of Day", str(self.time_of_day))
        basic_table.add_row(
            "Updated At", str(self.updated_at) if self.updated_at else "N/A"
        )

        # Key balances table
        balances_table = Table(
            title="Key Account Balances",
            show_header=True,
            header_style="bold green",
        )
        balances_table.add_column("Balance Type", style="cyan")
        balances_table.add_column("Amount", style="green")

        balances_table.add_row(
            "Net Liquidating Value",
            f"{currency_symbol}{self.net_liquidating_value:,.2f}",
        )
        balances_table.add_row(
            "Cash Balance", f"{currency_symbol}{self.cash_balance:,.2f}"
        )
        balances_table.add_row(
            "Cash Settle Balance", f"{currency_symbol}{self.cash_settle_balance:,.2f}"
        )
        balances_table.add_row(
            "Margin Settle Balance",
            f"{currency_symbol}{self.margin_settle_balance:,.2f}",
        )
        balances_table.add_row(
            "Total Settle Balance", f"{currency_symbol}{self.total_settle_balance:,.2f}"
        )
        balances_table.add_row(
            "Available Trading Funds",
            f"{currency_symbol}{self.available_trading_funds:,.2f}",
        )
        balances_table.add_row(
            "Cash Available to Withdraw",
            f"{currency_symbol}{self.cash_available_to_withdraw:,.2f}",
        )
        balances_table.add_row(
            "Pending Cash", f"{currency_symbol}{self.pending_cash:,.2f}"
        )

        # Buying power table
        buying_power_table = Table(
            title="Buying Power & Trading Limits",
            show_header=True,
            header_style="bold yellow",
        )
        buying_power_table.add_column("Type", style="cyan")
        buying_power_table.add_column("Amount", style="green")

        buying_power_table.add_row(
            "Equity Buying Power", f"{currency_symbol}{self.equity_buying_power:,.2f}"
        )
        buying_power_table.add_row(
            "Day Trading Buying Power",
            f"{currency_symbol}{self.day_trading_buying_power:,.2f}",
        )
        buying_power_table.add_row(
            "Derivative Buying Power",
            f"{currency_symbol}{self.derivative_buying_power:,.2f}",
        )
        buying_power_table.add_row(
            "Used Derivative Buying Power",
            f"{currency_symbol}{self.used_derivative_buying_power:,.2f}",
        )
        buying_power_table.add_row(
            "SMA Equity Option Buying Power",
            f"{currency_symbol}{self.sma_equity_option_buying_power:,.2f}",
        )
        buying_power_table.add_row(
            "Day Trade Excess", f"{currency_symbol}{self.day_trade_excess:,.2f}"
        )

        # Margin and calls table
        margin_table = Table(
            title="Margin & Maintenance Information",
            show_header=True,
            header_style="bold red",
        )
        margin_table.add_column("Type", style="cyan")
        margin_table.add_column("Amount", style="green")

        margin_table.add_row(
            "Margin Equity", f"{currency_symbol}{self.margin_equity:,.2f}"
        )
        margin_table.add_row(
            "Maintenance Requirement",
            f"{currency_symbol}{self.maintenance_requirement:,.2f}",
        )
        margin_table.add_row(
            "Maintenance Call Value",
            f"{currency_symbol}{self.maintenance_call_value:,.2f}",
        )
        margin_table.add_row(
            "Day Trading Call Value",
            f"{currency_symbol}{self.day_trading_call_value:,.2f}",
        )
        margin_table.add_row(
            "Day Equity Call Value",
            f"{currency_symbol}{self.day_equity_call_value:,.2f}",
        )
        margin_table.add_row(
            "Reg T Call Value", f"{currency_symbol}{self.reg_t_call_value:,.2f}"
        )

        # Position values table
        positions_table = Table(
            title="Position Values by Asset Class",
            show_header=True,
            header_style="bold magenta",
        )
        positions_table.add_column("Asset Class", style="cyan")
        positions_table.add_column("Long Value", style="green")
        positions_table.add_column("Short Value", style="red")

        positions_table.add_row(
            "Equities",
            f"{currency_symbol}{self.long_equity_value:,.2f}",
            f"{currency_symbol}{self.short_equity_value:,.2f}",
        )
        positions_table.add_row(
            "Derivatives",
            f"{currency_symbol}{self.long_futures_derivative_value:,.2f}",
            f"{currency_symbol}{self.short_derivative_value:,.2f}",
        )
        positions_table.add_row(
            "Futures",
            f"{currency_symbol}{self.long_futures_value:,.2f}",
            f"{currency_symbol}{self.short_futures_value:,.2f}",
        )
        positions_table.add_row(
            "Futures Derivatives",
            f"{currency_symbol}{self.long_futures_derivative_value:,.2f}",
            f"{currency_symbol}{self.short_futures_derivative_value:,.2f}",
        )
        positions_table.add_row(
            "Cryptocurrency",
            f"{currency_symbol}{self.long_cryptocurrency_value:,.2f}",
            f"{currency_symbol}{self.short_cryptocurrency_value:,.2f}",
        )
        positions_table.add_row(
            "Bonds", f"{currency_symbol}{self.long_bond_value:,.2f}", "N/A"
        )
        positions_table.add_row(
            "Fixed Income Securities",
            f"{currency_symbol}{self.long_fixed_income_security_value:,.2f}",
            "N/A",
        )
        positions_table.add_row(
            "Index Derivatives",
            f"{currency_symbol}{self.long_index_derivative_value:,.2f}",
            f"{currency_symbol}{self.short_index_derivative_value:,.2f}",
        )

        # Margin requirements table
        margin_reqs_table = Table(
            title="Margin Requirements by Asset Class",
            show_header=True,
            header_style="bold cyan",
        )
        margin_reqs_table.add_column("Asset Class", style="cyan")
        margin_reqs_table.add_column("Margin Requirement", style="green")

        margin_reqs_table.add_row(
            "Reg T", f"{currency_symbol}{self.reg_t_margin_requirement:,.2f}"
        )
        margin_reqs_table.add_row(
            "Futures Overnight",
            f"{currency_symbol}{self.futures_overnight_margin_requirement:,.2f}",
        )
        margin_reqs_table.add_row(
            "Futures Intraday",
            f"{currency_symbol}{self.futures_intraday_margin_requirement:,.2f}",
        )
        margin_reqs_table.add_row(
            "Cryptocurrency",
            f"{currency_symbol}{self.cryptocurrency_margin_requirement:,.2f}",
        )
        margin_reqs_table.add_row(
            "Equity Offering",
            f"{currency_symbol}{self.equity_offering_margin_requirement:,.2f}",
        )
        margin_reqs_table.add_row(
            "Bonds", f"{currency_symbol}{self.bond_margin_requirement:,.2f}"
        )
        margin_reqs_table.add_row(
            "Fixed Income Securities",
            f"{currency_symbol}{self.fixed_income_security_margin_requirement:,.2f}",
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
                balances_table,
                title="[bold green]Account Balances[/bold green]",
                border_style="green",
            )
        )
        console.print(
            Panel(
                buying_power_table,
                title="[bold yellow]Buying Power[/bold yellow]",
                border_style="yellow",
            )
        )
        console.print(
            Panel(
                margin_table,
                title="[bold red]Margin & Calls[/bold red]",
                border_style="red",
            )
        )
        console.print(
            Panel(
                positions_table,
                title="[bold magenta]Position Values[/bold magenta]",
                border_style="magenta",
            )
        )
        console.print(
            Panel(
                margin_reqs_table,
                title="[bold cyan]Margin Requirements[/bold cyan]",
                border_style="cyan",
            )
        )
