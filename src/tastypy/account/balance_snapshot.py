import datetime
import enum

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from ..errors import translate_error_code
from ..session import Session


class TimeOfDaySnapshot(enum.Enum):
    BOD = "BOD"  # Beginning of Day
    EOD = "EOD"  # End of Day

    @staticmethod
    def from_string(time_of_day_str: str) -> "TimeOfDaySnapshot | None":
        if time_of_day_str == "BOD":
            return TimeOfDaySnapshot.BOD
        elif time_of_day_str == "EOD":
            return TimeOfDaySnapshot.EOD
        raise ValueError(f"Unknown TimeOfDaySnapshot value: {time_of_day_str}")


class BalanceSnapshot:
    _snapshot_data: dict

    def __init__(self, snapshot_data: dict):
        self._snapshot_data = snapshot_data

    @property
    def account_number(self) -> str:
        return self._snapshot_data.get("account-number", "")

    @property
    def available_trading_funds(self) -> float:
        value = self._snapshot_data.get("available-trading-funds", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def bond_margin_requirement(self) -> float:
        value = self._snapshot_data.get("bond-margin-requirement", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def cash_available_to_withdraw(self) -> float:
        value = self._snapshot_data.get("cash-available-to-withdraw", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def cash_balance(self) -> float:
        value = self._snapshot_data.get("cash-balance", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def cash_settle_balance(self) -> float:
        value = self._snapshot_data.get("cash-settle-balance", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def closed_loop_available_balance(self) -> float:
        value = self._snapshot_data.get("closed-loop-available-balance", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def cryptocurrency_margin_requirement(self) -> float:
        value = self._snapshot_data.get("cryptocurrency-margin-requirement", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def currency(self) -> str:
        return self._snapshot_data.get("currency", "")

    @property
    def day_equity_call_value(self) -> float:
        value = self._snapshot_data.get("day-equity-call-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def day_trade_excess(self) -> float:
        value = self._snapshot_data.get("day-trade-excess", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def day_trading_buying_power(self) -> float:
        value = self._snapshot_data.get("day-trading-buying-power", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def day_trading_call_value(self) -> float:
        value = self._snapshot_data.get("day-trading-call-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def derivative_buying_power(self) -> float:
        value = self._snapshot_data.get("derivative-buying-power", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def equity_buying_power(self) -> float:
        value = self._snapshot_data.get("equity-buying-power", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def equity_offering_margin_requirement(self) -> float:
        value = self._snapshot_data.get("equity-offering-margin-requirement", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def fixed_income_security_margin_requirement(self) -> float:
        value = self._snapshot_data.get("fixed-income-security-margin-requirement", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def futures_margin_requirement(self) -> float:
        value = self._snapshot_data.get("futures-margin-requirement", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def intraday_equities_cash_amount(self) -> float:
        value = self._snapshot_data.get("intraday-equities-cash-amount", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def intraday_equities_cash_effect(self) -> str:
        return self._snapshot_data.get("intraday-equities-cash-effect", "")

    @property
    def intraday_futures_cash_effective_date(self) -> datetime.date | None:
        intraday_futures_cash_effective_date_str = self._snapshot_data.get(
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
        value = self._snapshot_data.get("long-bond-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def long_cryptocurrency_value(self) -> float:
        value = self._snapshot_data.get("long-cryptocurrency-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def long_derivative_value(self) -> float:
        value = self._snapshot_data.get("long-derivative-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def long_equity_value(self) -> float:
        value = self._snapshot_data.get("long-equity-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def long_fixed_income_security_value(self) -> float:
        value = self._snapshot_data.get("long-fixed-income-security-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def long_futures_derivative_value(self) -> float:
        value = self._snapshot_data.get("long-futures-derivative-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def long_futures_value(self) -> float:
        value = self._snapshot_data.get("long-futures-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def long_margineable_value(self) -> float:
        value = self._snapshot_data.get("long-margineable-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def maintenance_call_value(self) -> float:
        value = self._snapshot_data.get("maintenance-call-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def maintenance_requirement(self) -> float:
        value = self._snapshot_data.get("maintenance-requirement", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def margin_equity(self) -> float:
        value = self._snapshot_data.get("margin-equity", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def margin_settle_balance(self) -> float:
        value = self._snapshot_data.get("margin-settle-balance", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def net_liquidating_value(self) -> float:
        value = self._snapshot_data.get("net-liquidating-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def pending_cash(self) -> float:
        value = self._snapshot_data.get("pending-cash", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def pending_cash_effect(self) -> str:
        return self._snapshot_data.get("pending-cash-effect", "")

    @property
    def previous_day_cryptocurrency_fiat_amount(self) -> float:
        value = self._snapshot_data.get("previous-day-cryptocurrency-fiat-amount", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def previous_day_cryptocurrency_fiat_effect(self) -> str:
        return self._snapshot_data.get("previous-day-cryptocurrency-fiat-effect", "")

    @property
    def reg_t_call_value(self) -> float:
        value = self._snapshot_data.get("reg-t-call-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def short_cryptocurrency_value(self) -> float:
        value = self._snapshot_data.get("short-cryptocurrency-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def short_derivative_value(self) -> float:
        value = self._snapshot_data.get("short-derivative-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def short_equity_value(self) -> float:
        value = self._snapshot_data.get("short-equity-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def short_futures_derivative_value(self) -> float:
        value = self._snapshot_data.get("short-futures-derivative-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def short_futures_value(self) -> float:
        value = self._snapshot_data.get("short-futures-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def short_marginable_value(self) -> float:
        value = self._snapshot_data.get("short-margineable-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def sma_equity_option_buying_power(self) -> float:
        value = self._snapshot_data.get("sma-equity-option-buying-power", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def special_memorandum_account_apex_adjustment(self) -> float:
        value = self._snapshot_data.get(
            "special-memorandum-account-apex-adjustment", 0.0
        )
        return float(value) if value is not None else 0.0

    @property
    def special_memorandum_account_value(self) -> float:
        value = self._snapshot_data.get("special-memorandum-account-value", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def total_settle_balance(self) -> float:
        value = self._snapshot_data.get("total-settle-balance", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def unsettled_cryptocurrency_fiat_amount(self) -> float:
        value = self._snapshot_data.get("unsettled-cryptocurrency-fiat-amount", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def unsettled_cryptocurrency_fiat_effect(self) -> str:
        return self._snapshot_data.get("unsettled-cryptocurrency-fiat-effect", "")

    @property
    def used_derivative_buying_power(self) -> float:
        value = self._snapshot_data.get("used-derivative-buying-power", 0.0)
        return float(value) if value is not None else 0.0

    @property
    def snapshot_date(self) -> datetime.date | None:
        snapshot_date_str = self._snapshot_data.get("snapshot-date", "")
        if not snapshot_date_str:
            return None
        # This is just YYY-MM-DD
        return datetime.datetime.strptime(snapshot_date_str, "%Y-%m-%d").date()

    @property
    def time_of_day(self) -> TimeOfDaySnapshot | None:
        time_of_day_str = self._snapshot_data.get("time-of-day", "")
        if not time_of_day_str:
            return None
        # This is just HH:MM:SS
        return TimeOfDaySnapshot.from_string(time_of_day_str)

    def print_summary(self) -> None:
        """Print a simple text summary of the balance snapshot."""
        print(f"\n{'=' * 60}")
        print(f"BALANCE SNAPSHOT SUMMARY: Account {self.account_number}")
        print(f"{'=' * 60}")
        print(f"Account Number: {self.account_number}")
        print(f"Currency: {self.currency}")
        print(f"Snapshot Date: {self.snapshot_date}")
        print(f"Time of Day: {self.time_of_day.value if self.time_of_day else 'N/A'}")

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
            + self.long_derivative_value
            + self.long_futures_value
            + self.long_cryptocurrency_value
        )
        total_short_value = (
            self.short_equity_value
            + self.short_derivative_value
            + self.short_futures_value
            + self.short_cryptocurrency_value
        )
        print(f"Total Long Position Value: {currency_symbol}{total_long_value:,.2f}")
        print(f"Total Short Position Value: {currency_symbol}{total_short_value:,.2f}")

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all balance snapshot data in a nicely formatted table."""
        console = Console()

        # Get currency symbol for formatting
        currency_symbol = "$" if self.currency == "USD" else self.currency

        # Create basic account information table
        basic_table = Table(
            title=f"Balance Snapshot: Account {self.account_number}",
            show_header=True,
            header_style="bold blue",
        )
        basic_table.add_column("Property", style="cyan", no_wrap=True)
        basic_table.add_column("Value", style="green")

        # Basic information
        basic_table.add_row("Account Number", str(self.account_number))
        basic_table.add_row("Currency", str(self.currency))
        basic_table.add_row(
            "Snapshot Date", str(self.snapshot_date) if self.snapshot_date else "N/A"
        )
        basic_table.add_row(
            "Time of Day", str(self.time_of_day.value) if self.time_of_day else "N/A"
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
            f"{currency_symbol}{self.long_derivative_value:,.2f}",
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

        # Margin requirements table
        margin_reqs_table = Table(
            title="Margin Requirements by Asset Class",
            show_header=True,
            header_style="bold cyan",
        )
        margin_reqs_table.add_column("Asset Class", style="cyan")
        margin_reqs_table.add_column("Margin Requirement", style="green")

        margin_reqs_table.add_row(
            "Futures", f"{currency_symbol}{self.futures_margin_requirement:,.2f}"
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

    def __str__(self):
        return f"BalanceSnapshot(id={self.account_number}, date={self.snapshot_date}, time_of_day={self.time_of_day})"


class BalanceSnapshots:
    _url_endpoint = ""
    _session: Session

    def __init__(self, account_number: str, session: Session):
        self._session = session
        self._url_endpoint = f"/accounts/{account_number}/balance-snapshots"

    def sync(
        self,
        page_offset: int = 0,
        per_page: int = 250,
        currency: str = "USD",
        snapshot_date: str = "",
        time_of_day: TimeOfDaySnapshot = TimeOfDaySnapshot.EOD,
        start_date: str = "",
        end_date: str = "",
    ):
        if not snapshot_date:
            # YYYY-MM-DD
            snapshot_date = datetime.date.today().strftime("%Y-%m-%d")
        if not start_date:
            start_date = snapshot_date
        if not end_date:
            end_date = snapshot_date

        params = {
            "page-offset": page_offset,
            "per-page": per_page,
            "currency": currency,
            "snapshot-date": snapshot_date,
            "time-of-day": time_of_day.value,
            # "start-date": start_date,
            # "end-date": end_date,
        }

        response = self._session.client.get(self._url_endpoint, params=params)
        if response.status_code == 200:
            self._snapshot_data_array = response.json().get("data", {}).get("items", [])
            self._snapshot_data = [
                BalanceSnapshot(data) for data in self._snapshot_data_array
            ]
        else:
            error_code = response.status_code
            error_message = response.json()["error"]["message"]
            raise translate_error_code(error_code, error_message)

    @property
    def snapshot_data(self) -> list[BalanceSnapshot]:
        return self._snapshot_data

    def print_summary(self) -> None:
        """Print a simple text summary of the balance snapshots collection."""
        print(f"\n{'=' * 60}")
        print("BALANCE SNAPSHOTS SUMMARY")
        print(f"{'=' * 60}")
        print(f"Total Snapshots: {len(self._snapshot_data)}")

        if self._snapshot_data:
            # Get date range
            dates = [
                snapshot.snapshot_date
                for snapshot in self._snapshot_data
                if snapshot.snapshot_date
            ]
            if dates:
                min_date = min(dates)
                max_date = max(dates)
                if min_date == max_date:
                    print(f"Date: {min_date}")
                else:
                    print(f"Date Range: {min_date} to {max_date}")

            # Show account numbers
            account_numbers = list(
                set(snapshot.account_number for snapshot in self._snapshot_data)
            )
            print(f"Account(s): {', '.join(account_numbers)}")

            # Show latest snapshot key metrics with dynamic currency
            latest = self._snapshot_data[0]  # Assuming first is most recent
            currency_symbol = "$" if latest.currency == "USD" else latest.currency
            print(
                f"Latest Net Liquidating Value: {currency_symbol}{latest.net_liquidating_value:,.2f}"
            )
            print(f"Latest Cash Balance: {currency_symbol}{latest.cash_balance:,.2f}")
            print(
                f"Latest Available Trading Funds: {currency_symbol}{latest.available_trading_funds:,.2f}"
            )
        else:
            print("No snapshots available")

        print(f"{'=' * 60}\n")

    def pretty_print(self) -> None:
        """Pretty print all balance snapshots data in a nicely formatted table."""
        console = Console()

        if not self._snapshot_data:
            console.print(
                Panel(
                    "No balance snapshots available",
                    title="Balance Snapshots",
                    border_style="red",
                )
            )
            return

        # Create summary table
        summary_table = Table(
            title="Balance Snapshots Collection Summary",
            show_header=True,
            header_style="bold blue",
        )
        summary_table.add_column("Property", style="cyan", no_wrap=True)
        summary_table.add_column("Value", style="green")

        summary_table.add_row("Total Snapshots", str(len(self._snapshot_data)))

        # Get date range
        dates = [
            snapshot.snapshot_date
            for snapshot in self._snapshot_data
            if snapshot.snapshot_date
        ]
        if dates:
            min_date = min(dates)
            max_date = max(dates)
            if min_date == max_date:
                summary_table.add_row("Date", str(min_date))
            else:
                summary_table.add_row("Date Range", f"{min_date} to {max_date}")

        # Show account numbers
        account_numbers = list(
            set(snapshot.account_number for snapshot in self._snapshot_data)
        )
        summary_table.add_row("Account(s)", ", ".join(account_numbers))

        # Create detailed snapshots table
        snapshots_table = Table(
            title="Individual Balance Snapshots",
            show_header=True,
            header_style="bold green",
        )
        snapshots_table.add_column("Date", style="cyan")
        snapshots_table.add_column("Time", style="yellow")
        snapshots_table.add_column("Account", style="blue")
        snapshots_table.add_column("Net Liquidating Value", style="green")
        snapshots_table.add_column("Cash Balance", style="green")
        snapshots_table.add_column("Available Trading", style="green")
        snapshots_table.add_column("Buying Power", style="green")

        for snapshot in self._snapshot_data:
            date_str = str(snapshot.snapshot_date) if snapshot.snapshot_date else "N/A"
            time_str = snapshot.time_of_day.value if snapshot.time_of_day else "N/A"
            account_str = snapshot.account_number
            currency_symbol = "$" if snapshot.currency == "USD" else snapshot.currency
            nlv_str = f"{currency_symbol}{snapshot.net_liquidating_value:,.2f}"
            cash_str = f"{currency_symbol}{snapshot.cash_balance:,.2f}"
            available_str = f"{currency_symbol}{snapshot.available_trading_funds:,.2f}"
            buying_power_str = f"{currency_symbol}{snapshot.equity_buying_power:,.2f}"

            snapshots_table.add_row(
                date_str,
                time_str,
                account_str,
                nlv_str,
                cash_str,
                available_str,
                buying_power_str,
            )

        # Create key metrics comparison table if multiple snapshots
        if len(self._snapshot_data) > 1:
            # Get currency symbol from first snapshot for consistency
            currency_symbol = (
                "$"
                if self._snapshot_data[0].currency == "USD"
                else self._snapshot_data[0].currency
            )

            metrics_table = Table(
                title="Key Metrics Comparison",
                show_header=True,
                header_style="bold yellow",
            )
            metrics_table.add_column("Metric", style="cyan")
            metrics_table.add_column("Min", style="red")
            metrics_table.add_column("Max", style="green")
            metrics_table.add_column("Average", style="blue")

            # Calculate stats for key metrics
            nlv_values = [s.net_liquidating_value for s in self._snapshot_data]
            cash_values = [s.cash_balance for s in self._snapshot_data]
            available_values = [s.available_trading_funds for s in self._snapshot_data]
            buying_power_values = [s.equity_buying_power for s in self._snapshot_data]

            metrics_table.add_row(
                "Net Liquidating Value",
                f"{currency_symbol}{min(nlv_values):,.2f}",
                f"{currency_symbol}{max(nlv_values):,.2f}",
                f"{currency_symbol}{sum(nlv_values) / len(nlv_values):,.2f}",
            )
            metrics_table.add_row(
                "Cash Balance",
                f"{currency_symbol}{min(cash_values):,.2f}",
                f"{currency_symbol}{max(cash_values):,.2f}",
                f"{currency_symbol}{sum(cash_values) / len(cash_values):,.2f}",
            )
            metrics_table.add_row(
                "Available Trading Funds",
                f"{currency_symbol}{min(available_values):,.2f}",
                f"{currency_symbol}{max(available_values):,.2f}",
                f"{currency_symbol}{sum(available_values) / len(available_values):,.2f}",
            )
            metrics_table.add_row(
                "Equity Buying Power",
                f"{currency_symbol}{min(buying_power_values):,.2f}",
                f"{currency_symbol}{max(buying_power_values):,.2f}",
                f"{currency_symbol}{sum(buying_power_values) / len(buying_power_values):,.2f}",
            )

        # Print all tables
        console.print(
            Panel(
                summary_table,
                title="[bold blue]Collection Summary[/bold blue]",
                border_style="blue",
            )
        )
        console.print(
            Panel(
                snapshots_table,
                title="[bold green]Snapshot Details[/bold green]",
                border_style="green",
            )
        )

        if len(self._snapshot_data) > 1:
            console.print(
                Panel(
                    metrics_table,
                    title="[bold yellow]Metrics Comparison[/bold yellow]",
                    border_style="yellow",
                )
            )

    def __str__(self):
        return f"BalanceSnapshots({len(self._snapshot_data)})"
