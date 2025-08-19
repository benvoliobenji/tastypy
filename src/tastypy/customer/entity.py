from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .address import Address
from .officer import Officer
from .suitability import Suitability


class Entity:
    def __init__(self, entity_data: dict[str, str]):
        self._entity_data = entity_data

    @property
    def id(self) -> str:
        return self._entity_data.get("id", "")

    @property
    def address(self) -> Address:
        address_data = self._entity_data.get("address", {})
        # Ensure we have a dict, not a string
        if isinstance(address_data, dict):
            return Address(address_data)
        return Address({})

    @property
    def business_nature(self) -> str:
        return self._entity_data.get("business-nature", "")

    @property
    def email(self) -> str:
        return self._entity_data.get("email", "")

    @property
    def officers(self) -> list[Officer]:
        officers_data = self._entity_data.get("officers", [])
        # Ensure we have a list of dicts
        if isinstance(officers_data, list):
            return [Officer(data) for data in officers_data if isinstance(data, dict)]
        return []

    @property
    def suitability(self) -> Suitability:
        suitability_data = self._entity_data.get("suitability", {})
        # Ensure we have a dict, not a string
        if isinstance(suitability_data, dict):
            return Suitability(suitability_data)
        return Suitability({})

    @property
    def type(self) -> str:
        return self._entity_data.get("entity-type", "")

    @property
    def foreign_institution(self) -> str:
        return self._entity_data.get("foreign-institution", "")

    @property
    def grantor_birth_date(self) -> str:
        return self._entity_data.get("grantor-birth-date", "")

    @property
    def grantor_email(self) -> str:
        return self._entity_data.get("grantor-email", "")

    @property
    def grantor_first_name(self) -> str:
        return self._entity_data.get("grantor-first-name", "")

    @property
    def grantor_last_name(self) -> str:
        return self._entity_data.get("grantor-last-name", "")

    @property
    def grantor_middle_name(self) -> str:
        return self._entity_data.get("grantor-middle-name", "")

    @property
    def grantor_tax_number(self) -> str:
        return self._entity_data.get("grantor-tax-number", "")

    @property
    def has_foreign_institution_affiliation(self) -> bool:
        return bool(self._entity_data.get("has-foreign-institution-affiliation", False))

    @property
    def is_domestic(self) -> bool:
        return bool(self._entity_data.get("is-domestic", False))

    @property
    def legal_name(self) -> str:
        return self._entity_data.get("legal-name", "")

    @property
    def phone_number(self) -> str:
        return self._entity_data.get("phone-number", "")

    @property
    def tax_number(self) -> str:
        return self._entity_data.get("tax-number", "")

    def pretty_print(self) -> None:
        """Pretty print all entity data in a nicely formatted table."""
        console = Console()

        # Create basic entity information table
        entity_table = Table(
            title=f"Entity Details: {self.legal_name}",
            show_header=True,
            header_style="bold blue",
        )
        entity_table.add_column("Property", style="cyan", no_wrap=True)
        entity_table.add_column("Value", style="green")

        # Basic entity information
        entity_table.add_row("Entity ID", str(self.id))
        entity_table.add_row("Legal Name", str(self.legal_name))
        entity_table.add_row("Entity Type", str(self.type))
        entity_table.add_row("Business Nature", str(self.business_nature))
        entity_table.add_row("Email", str(self.email))
        entity_table.add_row("Phone Number", str(self.phone_number))
        entity_table.add_row("Tax Number", str(self.tax_number))
        entity_table.add_row("Is Domestic", "✓" if self.is_domestic else "✗")

        # Foreign affiliation table
        foreign_table = Table(
            title="Foreign Institution Information",
            show_header=True,
            header_style="bold yellow",
        )
        foreign_table.add_column("Property", style="cyan")
        foreign_table.add_column("Value", style="green")

        foreign_table.add_row(
            "Has Foreign Affiliation",
            "✓" if self.has_foreign_institution_affiliation else "✗",
        )
        foreign_table.add_row("Foreign Institution", str(self.foreign_institution))

        # Grantor information table
        grantor_table = Table(
            title="Grantor Information", show_header=True, header_style="bold magenta"
        )
        grantor_table.add_column("Property", style="cyan")
        grantor_table.add_column("Value", style="green")

        grantor_table.add_row("Grantor First Name", str(self.grantor_first_name))
        grantor_table.add_row("Grantor Middle Name", str(self.grantor_middle_name))
        grantor_table.add_row("Grantor Last Name", str(self.grantor_last_name))
        grantor_table.add_row("Grantor Email", str(self.grantor_email))
        grantor_table.add_row("Grantor Birth Date", str(self.grantor_birth_date))
        grantor_table.add_row("Grantor Tax Number", str(self.grantor_tax_number))

        # Officers summary table
        officers_table = Table(
            title="Officers Summary", show_header=True, header_style="bold red"
        )
        officers_table.add_column("Name", style="cyan")
        officers_table.add_column("Title", style="green")
        officers_table.add_column("Relationship", style="yellow")

        for officer in self.officers:
            officers_table.add_row(
                f"{officer.first_name} {officer.last_name}",
                str(officer.job_title),
                str(officer.relationship_to_entity),
            )

        # Print all tables
        console.print(
            Panel(
                entity_table,
                title="[bold blue]Entity Information[/bold blue]",
                border_style="blue",
            )
        )
        console.print(
            Panel(
                foreign_table,
                title="[bold yellow]Foreign Affiliation[/bold yellow]",
                border_style="yellow",
            )
        )
        console.print(
            Panel(
                grantor_table,
                title="[bold magenta]Grantor Information[/bold magenta]",
                border_style="magenta",
            )
        )
        console.print(
            Panel(
                officers_table,
                title="[bold red]Officers[/bold red]",
                border_style="red",
            )
        )

        # Print address separately
        print(f"\nEntity Address: {self.address}")

    def print_summary(self) -> None:
        """Print a simple text summary of the entity."""
        print(f"\n{'=' * 60}")
        print(f"ENTITY SUMMARY: {self.legal_name}")
        print(f"{'=' * 60}")
        print(f"Entity ID: {self.id}")
        print(f"Entity Type: {self.type}")
        print(f"Business Nature: {self.business_nature}")
        print(f"Email: {self.email}")
        print(f"Phone: {self.phone_number}")
        print(f"Tax Number: {self.tax_number}")
        print(f"Is Domestic: {'Yes' if self.is_domestic else 'No'}")
        print(
            f"Foreign Affiliation: {'Yes' if self.has_foreign_institution_affiliation else 'No'}"
        )
        if self.grantor_first_name or self.grantor_last_name:
            print(f"Grantor: {self.grantor_first_name} {self.grantor_last_name}")
            print(f"Grantor Email: {self.grantor_email}")
        print(f"Number of Officers: {len(self.officers)}")
        for officer in self.officers:
            print(
                f"  - {officer.first_name} {officer.last_name} ({officer.relationship_to_entity})"
            )
        print(f"Address: {self.address}")
        print(f"{'=' * 60}\n")

    def __str__(self) -> str:
        return f"Entity({self.id})"
