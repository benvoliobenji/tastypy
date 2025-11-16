"""Placed order response data model."""

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .complex_order import ComplexOrder
from .order import Order


class OrderError:
    """Represents an error in order placement."""

    def __init__(self, json_data: dict[str, Any]) -> None:
        """Initialize OrderError from JSON data."""
        self._json = json_data

    @property
    def code(self) -> str:
        """The error code."""
        return self._json.get("code", "")

    @property
    def message(self) -> str:
        """The error message."""
        return self._json.get("message", "")

    @property
    def preflight_id(self) -> str:
        """The preflight ID associated with the error."""
        return self._json.get("preflight-id", "")


class OrderNote:
    """Represents a note in order placement response."""

    def __init__(self, json_data: dict[str, Any]) -> None:
        """Initialize OrderNote from JSON data."""
        self._json = json_data

    @property
    def code(self) -> str:
        """The note code."""
        return self._json.get("code", "")

    @property
    def message(self) -> str:
        """The note message."""
        return self._json.get("message", "")

    @property
    def preflight_id(self) -> str:
        """The preflight ID associated with the note."""
        return self._json.get("preflight-id", "")

    @property
    def url(self) -> str:
        """URL for more information."""
        return self._json.get("url", "")


class OrderWarning:
    """Represents a warning in order placement response."""

    def __init__(self, json_data: dict[str, Any]) -> None:
        """Initialize OrderWarning from JSON data."""
        self._json = json_data

    @property
    def code(self) -> str:
        """The warning code."""
        return self._json.get("code", "")

    @property
    def message(self) -> str:
        """The warning message."""
        return self._json.get("message", "")

    @property
    def preflight_id(self) -> str:
        """The preflight ID associated with the warning."""
        return self._json.get("preflight-id", "")


class PlacedOrderResponse:
    """Represents the response from placing an order."""

    def __init__(self, json_data: dict[str, Any]) -> None:
        """Initialize PlacedOrderResponse from JSON data."""
        self._json = json_data
        self._order: Order | None = None
        self._complex_order: ComplexOrder | None = None
        self._errors: list[OrderError] = []
        self._notes: list[OrderNote] = []
        self._warnings: list[OrderWarning] = []

        # Parse order if present
        order_data = self._json.get("order")
        if order_data:
            self._order = Order(order_data)

        # Parse complex order if present
        complex_data = self._json.get("complex-order")
        if complex_data:
            self._complex_order = ComplexOrder(complex_data)

        # Parse errors if present
        errors_data = self._json.get("errors", [])
        if errors_data:
            self._errors = [OrderError(err) for err in errors_data]

        # Parse notes if present
        notes_data = self._json.get("notes", [])
        if notes_data:
            self._notes = [OrderNote(note) for note in notes_data]

        # Parse warnings if present
        warnings_data = self._json.get("warnings", [])
        if warnings_data:
            self._warnings = [OrderWarning(warn) for warn in warnings_data]

    @property
    def buying_power_effect(self) -> str:
        """The buying power effect."""
        return self._json.get("buying-power-effect", "")

    @property
    def closing_fee_calculation(self) -> str:
        """The closing fee calculation."""
        return self._json.get("closing-fee-calculation", "")

    @property
    def fee_calculation(self) -> str:
        """The fee calculation."""
        return self._json.get("fee-calculation", "")

    @property
    def order(self) -> Order | None:
        """The placed order."""
        return self._order

    @property
    def complex_order(self) -> ComplexOrder | None:
        """The placed complex order."""
        return self._complex_order

    @property
    def errors(self) -> list[OrderError]:
        """Errors from order placement."""
        return self._errors

    @property
    def notes(self) -> list[OrderNote]:
        """Notes from order placement."""
        return self._notes

    @property
    def warnings(self) -> list[OrderWarning]:
        """Warnings from order placement."""
        return self._warnings

    def print_summary(self) -> None:
        """Print a simple text summary of the response."""
        print(f"\n{'=' * 80}")
        print("PLACED ORDER RESPONSE")
        print(f"{'=' * 80}")

        if self.buying_power_effect:
            print(f"Buying Power Effect: {self.buying_power_effect}")
        if self.fee_calculation:
            print(f"Fee Calculation: {self.fee_calculation}")

        if self.errors:
            print(f"\n[ERRORS] {len(self.errors)} error(s):")
            for err in self.errors:
                print(f"  - {err.code}: {err.message}")

        if self.warnings:
            print(f"\n[WARNINGS] {len(self.warnings)} warning(s):")
            for warn in self.warnings:
                print(f"  - {warn.code}: {warn.message}")

        if self.notes:
            print(f"\n[NOTES] {len(self.notes)} note(s):")
            for note in self.notes:
                print(f"  - {note.code}: {note.message}")

        if self.order:
            print(f"\nOrder ID: {self.order.id}")
            print(
                f"Status: {self.order.status.value if self.order.status else 'Unknown'}"
            )

        if self.complex_order:
            print(f"\nComplex Order ID: {self.complex_order.id}")
            print(
                f"Type: {self.complex_order.type.value if self.complex_order.type else 'Unknown'}"
            )

        print(f"{'=' * 80}\n")

    def pretty_print(self) -> None:
        """Print a rich formatted output of the response."""
        console = Console()

        # Response Summary Panel
        summary_table = Table(show_header=False, box=None)
        summary_table.add_column("Field", style="cyan", width=25)
        summary_table.add_column("Value", style="white")

        if self.buying_power_effect:
            summary_table.add_row("Buying Power Effect", str(self.buying_power_effect))
        if self.fee_calculation:
            summary_table.add_row("Fee Calculation", str(self.fee_calculation))
        if self.closing_fee_calculation:
            summary_table.add_row("Closing Fee Calc", str(self.closing_fee_calculation))

        summary_table.add_row("Errors", str(len(self.errors)))
        summary_table.add_row("Warnings", str(len(self.warnings)))
        summary_table.add_row("Notes", str(len(self.notes)))

        console.print(
            Panel(
                summary_table,
                title="[bold]Order Response Summary[/bold]",
                border_style="blue",
            )
        )

        # Errors
        if self.errors:
            error_table = Table(title="Errors", border_style="red")
            error_table.add_column("Code", style="red")
            error_table.add_column("Message", style="white")
            error_table.add_column("Preflight ID", style="dim")

            for err in self.errors:
                error_table.add_row(err.code, err.message, err.preflight_id)

            console.print(error_table)

        # Warnings
        if self.warnings:
            warning_table = Table(title="Warnings", border_style="yellow")
            warning_table.add_column("Code", style="yellow")
            warning_table.add_column("Message", style="white")
            warning_table.add_column("Preflight ID", style="dim")

            for warn in self.warnings:
                warning_table.add_row(warn.code, warn.message, warn.preflight_id)

            console.print(warning_table)

        # Notes
        if self.notes:
            note_table = Table(title="Notes", border_style="blue")
            note_table.add_column("Code", style="blue")
            note_table.add_column("Message", style="white")
            note_table.add_column("URL", style="dim")

            for note in self.notes:
                note_table.add_row(note.code, note.message, note.url)

            console.print(note_table)

        # Order or Complex Order
        if self.order:
            console.print("\n[bold green]Placed Order:[/bold green]")
            self.order.pretty_print()

        if self.complex_order:
            console.print("\n[bold green]Placed Complex Order:[/bold green]")
            self.complex_order.pretty_print()
