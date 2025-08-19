import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .address import Address


class Officer:
    def __init__(self, officer_data: dict[str, str]):
        self._officer_data = officer_data

    @property
    def id(self) -> str:
        return self._officer_data.get("id", "")

    @property
    def external_id(self) -> str:
        return self._officer_data.get("external_id", "")

    @property
    def first_name(self) -> str:
        return self._officer_data.get("first_name", "")

    @property
    def last_name(self) -> str:
        return self._officer_data.get("last_name", "")

    @property
    def middle_name(self) -> str:
        return self._officer_data.get("middle_name", "")

    @property
    def prefix_name(self) -> str:
        return self._officer_data.get("prefix_name", "")

    @property
    def suffix_name(self) -> str:
        return self._officer_data.get("suffix_name", "")

    @property
    def address(self) -> Address:
        address_data = self._officer_data.get("address", {})
        # Ensure we have a dict, not a string
        if isinstance(address_data, dict):
            return Address(address_data)
        return Address({})

    @property
    def birth_country(self) -> str:
        return self._officer_data.get("birth_country", "")

    @property
    def birth_date(self) -> datetime.datetime | None:
        birth_date_str = self._officer_data.get("birth_date", "")
        if not birth_date_str:
            return None
        # This is just YYY-MM-DD, unlike above which is ISO
        return datetime.datetime.strptime(birth_date_str, "%Y-%m-%d")

    @property
    def citizenship_country(self) -> str:
        return self._officer_data.get("citizenship_country", "")

    @property
    def email(self) -> str:
        return self._officer_data.get("email", "")

    @property
    def employer_name(self) -> str:
        return self._officer_data.get("employer_name", "")

    @property
    def employment_status(self) -> str:
        return self._officer_data.get("employment_status", "")

    @property
    def home_phone_number(self) -> str:
        return self._officer_data.get("home_phone_number", "")

    @property
    def is_foreign(self) -> str:
        return str(self._officer_data.get("is_foreign", False))

    @property
    def job_title(self) -> str:
        return self._officer_data.get("job_title", "")

    @property
    def marital_status(self) -> str:
        return self._officer_data.get("marital_status", "")

    @property
    def mobile_phone_number(self) -> str:
        return self._officer_data.get("mobile_phone_number", "")

    @property
    def number_of_dependents(self) -> str:
        return str(self._officer_data.get("number_of_dependents", 0))

    @property
    def occupation(self) -> str:
        return self._officer_data.get("occupation", "")

    @property
    def owner_of_record(self) -> bool:
        value = self._officer_data.get("owner_of_record", False)
        # Handle both string and boolean values
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes", "on")
        return bool(value)

    @property
    def relationship_to_entity(self) -> str:
        return self._officer_data.get("relationship_to_entity", "")

    @property
    def tax_number(self) -> str:
        return self._officer_data.get("tax_number", "")

    @property
    def tax_number_type(self) -> str:
        return self._officer_data.get("tax_number_type", "")

    @property
    def usa_citizenship_type(self) -> str:
        return self._officer_data.get("usa_citizenship_type", "")

    @property
    def visa_expiration_date(self) -> datetime.datetime | None:
        visa_expiration_date_str = self._officer_data.get("visa_expiration_date", "")
        if not visa_expiration_date_str:
            return None
        return datetime.datetime.strptime(visa_expiration_date_str, "%Y-%m-%d")

    @property
    def visa_type(self) -> str:
        return self._officer_data.get("visa_type", "")

    @property
    def work_phone_number(self) -> str:
        return self._officer_data.get("work_phone_number", "")

    def pretty_print(self) -> None:
        """Pretty print all officer data in a nicely formatted table."""
        console = Console()

        # Create personal information table
        personal_table = Table(
            title=f"Officer Details: {self.first_name} {self.last_name}",
            show_header=True,
            header_style="bold blue",
        )
        personal_table.add_column("Property", style="cyan", no_wrap=True)
        personal_table.add_column("Value", style="green")

        # Basic personal information
        personal_table.add_row("Officer ID", str(self.id))
        personal_table.add_row("External ID", str(self.external_id))
        personal_table.add_row(
            "Full Name",
            f"{self.prefix_name} {self.first_name} {self.middle_name} {self.last_name} {self.suffix_name}".strip(),
        )
        personal_table.add_row("Email", str(self.email))
        personal_table.add_row(
            "Birth Date", str(self.birth_date) if self.birth_date else "N/A"
        )
        personal_table.add_row("Birth Country", str(self.birth_country))
        personal_table.add_row("Citizenship Country", str(self.citizenship_country))
        personal_table.add_row("USA Citizenship Type", str(self.usa_citizenship_type))

        # Contact information table
        contact_table = Table(
            title="Contact Information", show_header=True, header_style="bold yellow"
        )
        contact_table.add_column("Contact Type", style="cyan")
        contact_table.add_column("Value", style="green")

        contact_table.add_row("Home Phone", str(self.home_phone_number))
        contact_table.add_row("Mobile Phone", str(self.mobile_phone_number))
        contact_table.add_row("Work Phone", str(self.work_phone_number))
        contact_table.add_row("Address", str(self.address))

        # Employment and personal status table
        status_table = Table(
            title="Employment & Personal Status",
            show_header=True,
            header_style="bold magenta",
        )
        status_table.add_column("Property", style="cyan")
        status_table.add_column("Value", style="green")

        status_table.add_row("Employment Status", str(self.employment_status))
        status_table.add_row("Employer Name", str(self.employer_name))
        status_table.add_row("Job Title", str(self.job_title))
        status_table.add_row("Occupation", str(self.occupation))
        status_table.add_row("Marital Status", str(self.marital_status))
        status_table.add_row("Number of Dependents", str(self.number_of_dependents))

        # Legal and entity information table
        legal_table = Table(
            title="Legal & Entity Information",
            show_header=True,
            header_style="bold red",
        )
        legal_table.add_column("Property", style="cyan")
        legal_table.add_column("Value", style="green")

        legal_table.add_row("Relationship to Entity", str(self.relationship_to_entity))
        legal_table.add_row("Owner of Record", "✓" if self.owner_of_record else "✗")
        legal_table.add_row("Is Foreign", str(self.is_foreign))
        legal_table.add_row("Tax Number", str(self.tax_number))
        legal_table.add_row("Tax Number Type", str(self.tax_number_type))
        legal_table.add_row("Visa Type", str(self.visa_type))
        legal_table.add_row(
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
                contact_table,
                title="[bold yellow]Contact Information[/bold yellow]",
                border_style="yellow",
            )
        )
        console.print(
            Panel(
                status_table,
                title="[bold magenta]Employment & Status[/bold magenta]",
                border_style="magenta",
            )
        )
        console.print(
            Panel(
                legal_table,
                title="[bold red]Legal & Entity Info[/bold red]",
                border_style="red",
            )
        )

    def print_summary(self) -> None:
        """Print a simple text summary of the officer."""
        print(f"\n{'=' * 60}")
        print(f"OFFICER SUMMARY: {self.first_name} {self.last_name}")
        print(f"{'=' * 60}")
        print(f"Officer ID: {self.id}")
        print(f"External ID: {self.external_id}")
        print(f"Email: {self.email}")
        print(f"Birth Date: {self.birth_date}")
        print(f"Citizenship: {self.citizenship_country}")
        print(f"Employment: {self.employment_status} - {self.job_title}")
        print(f"Employer: {self.employer_name}")
        print(f"Marital Status: {self.marital_status}")
        print(f"Dependents: {self.number_of_dependents}")
        print(f"Relationship to Entity: {self.relationship_to_entity}")
        print(f"Owner of Record: {'Yes' if self.owner_of_record else 'No'}")
        print(
            f"Phone: Home={self.home_phone_number}, Mobile={self.mobile_phone_number}"
        )
        print(f"Address: {self.address}")
        print(f"{'=' * 60}\n")

    def __str__(self) -> str:
        return f"Officer({self.id})"
