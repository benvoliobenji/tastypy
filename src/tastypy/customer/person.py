import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class Person:
    def __init__(self, person_data: dict[str, str]):
        self._person_data = person_data

    @property
    def external_id(self) -> str:
        return self._person_data.get("external-id", "")

    @property
    def first_name(self) -> str:
        return self._person_data.get("first-name", "")

    @property
    def last_name(self) -> str:
        return self._person_data.get("last-name", "")

    @property
    def middle_name(self) -> str:
        return self._person_data.get("middle-name", "")

    @property
    def prefix_name(self) -> str:
        return self._person_data.get("prefix-name", "")

    @property
    def suffix_name(self) -> str:
        return self._person_data.get("suffix-name", "")

    @property
    def birth_country(self) -> str:
        return self._person_data.get("birth-country", "")

    @property
    def birth_date(self) -> datetime.datetime | None:
        birth_date_str = self._person_data.get("birth-date", "")
        if not birth_date_str:
            return None
        # This is just YYY-MM-DD, unlike above which is ISO
        return datetime.datetime.strptime(birth_date_str, "%Y-%m-%d")

    @property
    def citizenship_country(self) -> str:
        return self._person_data.get("citizenship-country", "")

    @property
    def usa_citizenship_type(self) -> str:
        return self._person_data.get("usa-citizenship-type", "")

    @property
    def visa_expiration_date(self) -> datetime.datetime | None:
        visa_expiration_date_str = self._person_data.get("visa-expiration-date", "")
        if not visa_expiration_date_str:
            return None
        return datetime.datetime.strptime(visa_expiration_date_str, "%Y-%m-%d")

    @property
    def visa_type(self) -> str:
        return self._person_data.get("visa-type", "")

    @property
    def employer_name(self) -> str:
        return self._person_data.get("employer-name", "")

    @property
    def employment_status(self) -> str:
        return self._person_data.get("employment-status", "")

    @property
    def job_title(self) -> str:
        return self._person_data.get("job-title", "")

    @property
    def marital_status(self) -> str:
        return self._person_data.get("marital-status", "")

    @property
    def number_of_dependents(self) -> int:
        return int(self._person_data.get("number-of-dependents", 0))

    @property
    def occupation(self) -> str:
        return self._person_data.get("occupation", "")

    def pretty_print(self) -> None:
        """Pretty print all person data in a nicely formatted table."""
        console = Console()

        # Create personal information table
        personal_table = Table(
            title=f"Person Details: {self.first_name} {self.last_name}",
            show_header=True,
            header_style="bold blue",
        )
        personal_table.add_column("Property", style="cyan", no_wrap=True)
        personal_table.add_column("Value", style="green")

        # Basic personal information
        personal_table.add_row("External ID", str(self.external_id))
        personal_table.add_row(
            "Full Name",
            f"{self.prefix_name} {self.first_name} {self.middle_name} {self.last_name} {self.suffix_name}".strip(),
        )
        personal_table.add_row(
            "Birth Date", str(self.birth_date) if self.birth_date else "N/A"
        )
        personal_table.add_row("Birth Country", str(self.birth_country))
        personal_table.add_row("Citizenship Country", str(self.citizenship_country))
        personal_table.add_row("USA Citizenship Type", str(self.usa_citizenship_type))

        # Employment information table
        employment_table = Table(
            title="Employment Information", show_header=True, header_style="bold yellow"
        )
        employment_table.add_column("Property", style="cyan")
        employment_table.add_column("Value", style="green")

        employment_table.add_row("Employment Status", str(self.employment_status))
        employment_table.add_row("Employer Name", str(self.employer_name))
        employment_table.add_row("Job Title", str(self.job_title))
        employment_table.add_row("Occupation", str(self.occupation))

        # Personal status table
        status_table = Table(
            title="Personal Status", show_header=True, header_style="bold magenta"
        )
        status_table.add_column("Property", style="cyan")
        status_table.add_column("Value", style="green")

        status_table.add_row("Marital Status", str(self.marital_status))
        status_table.add_row("Number of Dependents", str(self.number_of_dependents))

        # Visa information table
        visa_table = Table(
            title="Visa Information", show_header=True, header_style="bold red"
        )
        visa_table.add_column("Property", style="cyan")
        visa_table.add_column("Value", style="green")

        visa_table.add_row(
            "Visa Type", str(self.visa_type) if self.visa_type else "N/A"
        )
        visa_table.add_row(
            "Visa Expiration",
            str(self.visa_expiration_date) if self.visa_expiration_date else "N/A",
        )

        # Print all tables
        console.print(
            Panel(
                personal_table,
                title="[bold blue]Personal Information[/bold blue]",
                border_style="blue",
            )
        )
        console.print(
            Panel(
                employment_table,
                title="[bold yellow]Employment Information[/bold yellow]",
                border_style="yellow",
            )
        )
        console.print(
            Panel(
                status_table,
                title="[bold magenta]Personal Status[/bold magenta]",
                border_style="magenta",
            )
        )
        console.print(
            Panel(
                visa_table,
                title="[bold red]Visa Information[/bold red]",
                border_style="red",
            )
        )

    def print_summary(self) -> None:
        """Print a simple text summary of the person."""
        print(f"\n{'=' * 60}")
        print(f"PERSON SUMMARY: {self.first_name} {self.last_name}")
        print(f"{'=' * 60}")
        print(f"External ID: {self.external_id}")
        print(f"Birth Date: {self.birth_date}")
        print(f"Birth Country: {self.birth_country}")
        print(f"Citizenship: {self.citizenship_country}")
        print(f"USA Citizenship Type: {self.usa_citizenship_type}")
        print(f"Employment: {self.employment_status} - {self.job_title}")
        print(f"Employer: {self.employer_name}")
        print(f"Occupation: {self.occupation}")
        print(f"Marital Status: {self.marital_status}")
        print(f"Dependents: {self.number_of_dependents}")
        if self.visa_type:
            print(f"Visa Type: {self.visa_type}")
            print(f"Visa Expiration: {self.visa_expiration_date}")
        print(f"{'=' * 60}\n")

    def __str__(self) -> str:
        return f"Person({self.external_id})"
