import datetime

import httpx
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..errors import translate_error_code
from ..session import Session
from .trading_status import TradingStatus
from .balance import Balance
from .positions import Positions
from .margin import MarginRequirements, MarginRequirementsDryRun


class Account:
    _account_url = ""
    _session_client: httpx.Client
    _active_session: Session
    _trading_status: TradingStatus
    _current_balance: Balance

    def __init__(self, active_session: Session, customer_id: str, account_number: str):
        if not active_session.is_logged_in():
            raise ValueError("Session is not logged in.")
        elif not account_number:
            raise ValueError("Account number is required.")
        self._active_session = active_session
        self._session_client = active_session.client
        self._account_url = f"/customers/{customer_id}/accounts/{account_number}"

    def sync(self):
        """
        Sync the account data with the Tastyworks API and store raw JSON responses.
        """
        # Account details
        response = self._session_client.get(self._account_url)
        if response.status_code != 200:
            error_code = response.status_code
            error_message = response.json()["error"]["message"]
            raise translate_error_code(error_code, error_message)
        self._account_json = response.json()["data"]

    def deep_sync(self):
        """Sync the account information alongside all positions, balances, and other information related to the account specifically.

        Note that this will involve multiple API calls, and may take time to fully synchronize as data is fetched.
        """
        self.sync()
        self.trading_status.sync()

        # Fetch only today's balance snapshot
        self._current_balance = Balance(self.account_number, self._active_session)
        self._current_balance.sync()

        # Fetch positions
        self.positions.sync()

    @property
    def account_number(self) -> str:
        return self._account_json.get("account-number", "")

    @property
    def account_type_name(self) -> str:
        return self._account_json.get("account-type-name", "")

    @property
    def closed_at(self) -> datetime.datetime | None:
        closed_at_str = self._account_json.get("closed-at", "")
        if not closed_at_str:
            return None
        # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
        return datetime.datetime.fromisoformat(closed_at_str.replace("Z", "+00:00"))

    @property
    def created_at(self) -> datetime.datetime | None:
        created_at_str = self._account_json.get("created-at", "")
        if not created_at_str:
            return None
        # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
        return datetime.datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))

    @property
    def day_trader_status(self) -> bool:
        return self._account_json.get("day-trader-status", False)

    @property
    def external_account_id(self) -> str:
        return self._account_json.get("external-account-id", "")

    @property
    def external_crm_id(self) -> str:
        return self._account_json.get("external-crm-id", "")

    @property
    def external_fdid(self) -> str:
        return self._account_json.get("external-fdid", "")

    @property
    def external_id(self) -> str:
        return self._account_json.get("external-id", "")

    @property
    def funding_date(self) -> datetime.datetime | None:
        funding_date_str = self._account_json.get("funding-date", "")
        if not funding_date_str:
            return None
        # This is just YYY-MM-DD, unlike above which is ISO
        return datetime.datetime.strptime(funding_date_str, "%Y-%m-%d")

    @property
    def futures_account_purpose(self) -> str:
        return self._account_json.get("futures-account-purpose", "")

    @property
    def investment_objective(self) -> str:
        return self._account_json.get("investment-objective", "")

    @property
    def investment_time_horizon(self) -> str:
        return self._account_json.get("investment-time-horizon", "")

    @property
    def is_closed(self) -> bool:
        return self._account_json.get("is-closed", False)

    @property
    def is_firm_error(self) -> bool:
        return self._account_json.get("is-firm-error", False)

    @property
    def is_firm_proprietary(self) -> bool:
        return self._account_json.get("is-firm-proprietary", False)

    @property
    def is_foreign(self) -> bool:
        return self._account_json.get("is-foreign", False)

    @property
    def is_futures_approved(self) -> bool:
        return self._account_json.get("is-futures-approved", False)

    @property
    def liquidity_needs(self) -> str:
        return self._account_json.get("liquidity-needs", "")

    @property
    def margin_or_cash(self) -> str:
        return self._account_json.get("margin-or-cash", "")

    @property
    def nickname(self) -> str:
        return self._account_json.get("nickname", "")

    @property
    def opened_at(self) -> datetime.datetime | None:
        opened_at_str = self._account_json.get("opened-at", "")
        if not opened_at_str:
            return None
        # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
        return datetime.datetime.fromisoformat(opened_at_str.replace("Z", "+00:00"))

    @property
    def regulatory_domain(self) -> str:
        return self._account_json.get("regulatory-domain", "")

    @property
    def risk_tolerance(self) -> str:
        return self._account_json.get("risk-tolerance", "")

    @property
    def submitting_user_id(self) -> str:
        return self._account_json.get("submitting-user-id", "")

    @property
    def suitable_options_level(self) -> str:
        return self._account_json.get("suitable-options-level", "")

    # Outside API bound (new API calls)
    @property
    def trading_status(self) -> TradingStatus:
        if not self.account_number:
            raise ValueError("Account number is not set.")
        if not hasattr(self, "_trading_status"):
            self._trading_status = TradingStatus(
                self.account_number, self._active_session
            )
        return self._trading_status

    @property
    def current_balance(self) -> Balance:
        if not self.account_number:
            raise ValueError("Account number is not set.")
        if not hasattr(self, "_current_balance"):
            raise ValueError("Account balance has not been loaded.")
        return self._current_balance

    @property
    def positions(self) -> Positions:
        if not self.account_number:
            raise ValueError("Account number is not set.")
        if not hasattr(self, "_positions"):
            self._positions = Positions(self.account_number, self._active_session)
        return self._positions

    @property
    def margin_requirements(self) -> MarginRequirements:
        """Get margin requirements manager for this account.

        Returns:
            MarginRequirements: Object to fetch current margin/capital requirements

        Example:
            >>> account.margin_requirements.sync()
            >>> print(account.margin_requirements.margin_requirement)
        """
        if not self.account_number:
            raise ValueError("Account number is not set.")
        if not hasattr(self, "_margin_requirements"):
            self._margin_requirements = MarginRequirements(
                self.account_number, self._active_session
            )
        return self._margin_requirements

    @property
    def margin_requirements_dry_run(self) -> MarginRequirementsDryRun:
        """Get margin requirements dry-run estimator for this account.

        Returns:
            MarginRequirementsDryRun: Object to estimate margin requirements for orders

        Example:
            >>> dry_run = account.margin_requirements_dry_run
            >>> dry_run.estimate(
            ...     underlying_symbol="AAPL",
            ...     order_type="Limit",
            ...     time_in_force="Day",
            ...     legs=[{"symbol": "AAPL", "instrument-type": "Equity", "action": "Buy to Open", "quantity": "100"}],
            ...     price="150.00",
            ...     price_effect="Debit"
            ... )
            >>> print(dry_run.margin_requirement)
        """
        if not self.account_number:
            raise ValueError("Account number is not set.")
        if not hasattr(self, "_margin_requirements_dry_run"):
            self._margin_requirements_dry_run = MarginRequirementsDryRun(
                self.account_number, self._active_session
            )
        return self._margin_requirements_dry_run

    def pretty_print(self) -> None:
        """Pretty print all account data in a nicely formatted table."""
        console = Console()

        # Create main account info table
        account_table = Table(
            title=f"Account Details: {self.account_number}",
            show_header=True,
            header_style="bold blue",
        )
        account_table.add_column("Property", style="cyan", no_wrap=True)
        account_table.add_column("Value", style="green")

        # Basic account information
        account_table.add_row("Account Number", str(self.account_number))
        account_table.add_row("Account Type", str(self.account_type_name))
        account_table.add_row("Nickname", str(self.nickname))
        account_table.add_row("Margin or Cash", str(self.margin_or_cash))

        # Dates
        account_table.add_row(
            "Created At", str(self.created_at) if self.created_at else "N/A"
        )
        account_table.add_row(
            "Opened At", str(self.opened_at) if self.opened_at else "N/A"
        )
        account_table.add_row(
            "Closed At", str(self.closed_at) if self.closed_at else "N/A"
        )
        account_table.add_row(
            "Funding Date", str(self.funding_date) if self.funding_date else "N/A"
        )

        # Status flags
        status_table = Table(
            title="Account Status", show_header=True, header_style="bold yellow"
        )
        status_table.add_column("Status", style="cyan")
        status_table.add_column("Value", style="green")

        status_table.add_row("Is Closed", "✓" if self.is_closed else "✗")
        status_table.add_row(
            "Day Trader Status", "✓" if self.day_trader_status else "✗"
        )
        status_table.add_row(
            "Futures Approved", "✓" if self.is_futures_approved else "✗"
        )
        status_table.add_row("Is Foreign", "✓" if self.is_foreign else "✗")
        status_table.add_row("Is Firm Error", "✓" if self.is_firm_error else "✗")
        status_table.add_row(
            "Is Firm Proprietary", "✓" if self.is_firm_proprietary else "✗"
        )

        # External IDs and regulatory info
        external_table = Table(
            title="External IDs & Regulatory",
            show_header=True,
            header_style="bold magenta",
        )
        external_table.add_column("Property", style="cyan")
        external_table.add_column("Value", style="green")

        external_table.add_row("External ID", str(self.external_id))
        external_table.add_row("External Account ID", str(self.external_account_id))
        external_table.add_row("External CRM ID", str(self.external_crm_id))
        external_table.add_row("External FDID", str(self.external_fdid))
        external_table.add_row("Regulatory Domain", str(self.regulatory_domain))
        external_table.add_row("Submitting User ID", str(self.submitting_user_id))

        # Investment profile
        investment_table = Table(
            title="Investment Profile", show_header=True, header_style="bold red"
        )
        investment_table.add_column("Property", style="cyan")
        investment_table.add_column("Value", style="green")

        investment_table.add_row("Investment Objective", str(self.investment_objective))
        investment_table.add_row(
            "Investment Time Horizon", str(self.investment_time_horizon)
        )
        investment_table.add_row("Risk Tolerance", str(self.risk_tolerance))
        investment_table.add_row("Liquidity Needs", str(self.liquidity_needs))
        investment_table.add_row(
            "Suitable Options Level", str(self.suitable_options_level)
        )
        investment_table.add_row(
            "Futures Account Purpose", str(self.futures_account_purpose)
        )

        # Print all tables
        console.print(
            Panel(
                account_table,
                title="[bold blue]Account Information[/bold blue]",
                border_style="blue",
            )
        )
        console.print(
            Panel(
                status_table,
                title="[bold yellow]Account Status Flags[/bold yellow]",
                border_style="yellow",
            )
        )
        console.print(
            Panel(
                external_table,
                title="[bold magenta]External & Regulatory Info[/bold magenta]",
                border_style="magenta",
            )
        )
        console.print(
            Panel(
                investment_table,
                title="[bold red]Investment Profile[/bold red]",
                border_style="red",
            )
        )

    def print_summary(self) -> None:
        """Print a simple text summary of the account."""
        print(f"\n{'=' * 60}")
        print(f"ACCOUNT SUMMARY: {self.account_number}")
        print(f"{'=' * 60}")
        print(f"Account Type: {self.account_type_name}")
        print(f"Nickname: {self.nickname}")
        print(f"Margin/Cash: {self.margin_or_cash}")
        print(f"Created: {self.created_at}")
        print(f"Opened: {self.opened_at}")
        print(f"Day Trader: {'Yes' if self.day_trader_status else 'No'}")
        print(f"Futures Approved: {'Yes' if self.is_futures_approved else 'No'}")
        print(f"Is Closed: {'Yes' if self.is_closed else 'No'}")
        print(f"Options Level: {self.suitable_options_level}")
        print(f"Risk Tolerance: {self.risk_tolerance}")
        print(f"{'=' * 60}\n")

    def __str__(self) -> str:
        return f"Account({self.account_number})"
