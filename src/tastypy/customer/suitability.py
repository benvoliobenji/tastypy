from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class Suitability:
    def __init__(self, suitability_data: dict):
        self._suitability_data = suitability_data

    @property
    def id(self) -> str:
        return self._suitability_data.get("id", "")

    @property
    def annual_net_income(self) -> int:
        return self._suitability_data.get("annual-net-income", 0)

    @property
    def covered_options_trading_experience(self) -> str:
        return self._suitability_data.get("covered-options-trading-experience", "")

    @property
    def customer_id(self) -> int:
        return self._suitability_data.get("customer-id", 0)

    @property
    def employer_name(self) -> str:
        return self._suitability_data.get("employer-name", "")

    @property
    def employment_status(self) -> str:
        return self._suitability_data.get("employment-status", "")

    @property
    def futures_trading_experience(self) -> str:
        return self._suitability_data.get("futures-trading-experience", "")

    @property
    def job_title(self) -> str:
        return self._suitability_data.get("job-title", "")

    @property
    def liquid_net_worth(self) -> int:
        return self._suitability_data.get("liquid-net-worth", 0)

    @property
    def marital_status(self) -> str:
        return self._suitability_data.get("marital-status", "")

    @property
    def net_worth(self) -> int:
        return self._suitability_data.get("net-worth", 0)

    @property
    def number_of_dependents(self) -> int:
        return self._suitability_data.get("number-of-dependents", 0)

    @property
    def occupation(self) -> str:
        return self._suitability_data.get("occupation", "")

    @property
    def stock_trading_experience(self) -> str:
        return self._suitability_data.get("stock-trading-experience", "")

    @property
    def tax_bracket(self) -> str:
        return self._suitability_data.get("tax-bracket", "")

    @property
    def uncovered_options_trading_experience(self) -> str:
        return self._suitability_data.get("uncovered-options-trading-experience", "")

    def pretty_print(self) -> None:
        """Pretty print all customer suitability data in a nicely formatted table."""
        console = Console()

        # Create financial information table
        financial_table = Table(
            title=f"Financial Information: {self.id}",
            show_header=True,
            header_style="bold blue",
        )
        financial_table.add_column("Property", style="cyan", no_wrap=True)
        financial_table.add_column("Value", style="green")

        # Financial data
        financial_table.add_row(
            "Annual Net Income",
            f"${self.annual_net_income:,}" if self.annual_net_income else "N/A",
        )
        financial_table.add_row(
            "Net Worth", f"${self.net_worth:,}" if self.net_worth else "N/A"
        )
        financial_table.add_row(
            "Liquid Net Worth",
            f"${self.liquid_net_worth:,}" if self.liquid_net_worth else "N/A",
        )
        financial_table.add_row(
            "Tax Bracket", str(self.tax_bracket) if self.tax_bracket else "N/A"
        )

        # Personal information table
        personal_table = Table(
            title="Personal Information", show_header=True, header_style="bold yellow"
        )
        personal_table.add_column("Property", style="cyan")
        personal_table.add_column("Value", style="green")

        personal_table.add_row("Customer ID", str(self.customer_id))
        personal_table.add_row("Employment Status", str(self.employment_status))
        personal_table.add_row("Employer Name", str(self.employer_name))
        personal_table.add_row("Job Title", str(self.job_title))
        personal_table.add_row("Occupation", str(self.occupation))
        personal_table.add_row("Marital Status", str(self.marital_status))
        personal_table.add_row("Number of Dependents", str(self.number_of_dependents))

        # Trading experience table
        experience_table = Table(
            title="Trading Experience", show_header=True, header_style="bold magenta"
        )
        experience_table.add_column("Experience Type", style="cyan")
        experience_table.add_column("Level", style="green")

        experience_table.add_row("Stock Trading", str(self.stock_trading_experience))
        experience_table.add_row(
            "Covered Options", str(self.covered_options_trading_experience)
        )
        experience_table.add_row(
            "Uncovered Options", str(self.uncovered_options_trading_experience)
        )
        experience_table.add_row(
            "Futures Trading", str(self.futures_trading_experience)
        )

        # Print all tables
        console.print(
            Panel(
                financial_table,
                title="[bold blue]Financial Profile[/bold blue]",
                border_style="blue",
            )
        )
        console.print(
            Panel(
                personal_table,
                title="[bold yellow]Personal Information[/bold yellow]",
                border_style="yellow",
            )
        )
        console.print(
            Panel(
                experience_table,
                title="[bold magenta]Trading Experience[/bold magenta]",
                border_style="magenta",
            )
        )

    def print_summary(self) -> None:
        """Print a simple text summary of the customer suitability."""
        print(f"\n{'=' * 60}")
        print(f"SUITABILITY: {self.id}")
        print(f"{'=' * 60}")
        print(f"Customer ID: {self.customer_id}")
        print(f"Employment: {self.employment_status} - {self.job_title}")
        print(f"Employer: {self.employer_name}")
        print(
            f"Annual Income: ${self.annual_net_income:,}"
            if self.annual_net_income
            else "Annual Income: N/A"
        )
        print(f"Net Worth: ${self.net_worth:,}" if self.net_worth else "Net Worth: N/A")
        print(
            f"Liquid Net Worth: ${self.liquid_net_worth:,}"
            if self.liquid_net_worth
            else "Liquid Net Worth: N/A"
        )
        print(f"Marital Status: {self.marital_status}")
        print(f"Dependents: {self.number_of_dependents}")
        print(f"Stock Experience: {self.stock_trading_experience}")
        print(
            f"Options Experience: Covered={self.covered_options_trading_experience}, Uncovered={self.uncovered_options_trading_experience}"
        )
        print(f"Futures Experience: {self.futures_trading_experience}")
        print(f"{'=' * 60}\n")

    def __str__(self) -> str:
        return f"CustomerSuitability({self.id})"
