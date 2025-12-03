import datetime

import httpx
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..account.account import Account
from ..errors import translate_error_code
from ..session import Session
from .address import Address
from .entity import Entity
from .person import Person
from .suitability import Suitability


class Customer:
    _me_url = "/customers/me"
    _session_client: httpx.Client
    _accounts: list[Account] = []
    _active_session: Session

    def __init__(self, active_session: Session):
        self._active_session = active_session
        self._session_client = active_session.client

    def sync(self):
        """
        Sync the customer data with the Tastyworks API.
        """
        response = self._session_client.get(self._me_url)
        if response.status_code != 200:
            error_code = response.status_code
            error_message = response.json()["error"]["message"]
            raise translate_error_code(error_code, error_message)
        else:
            self._request_json_data = response.json()["data"]

    def deep_sync(self):
        """Sync the customer information alongside all accounts."""
        self.sync()

        # If we can get our customer data, it's time we get our accounts
        response = self._session_client.get(f"{self._me_url}/accounts")
        if response.status_code == 200:
            accounts = response.json()["data"]["items"]
            for account in accounts:
                account_number = account["account"]["account-number"]
                # Check if the account already exists in the list
                if any(acc.account_number == account_number for acc in self.accounts):
                    continue

                # If not, create a new Account instance, synchronize, and append it to the list
                new_account = Account(self._active_session, self.id, account_number)
                new_account.deep_sync()
                self.accounts.append(new_account)
        else:
            error_code = response.status_code
            error_message = response.json()["error"]["message"]
            raise translate_error_code(error_code, error_message)

    @property
    def accounts(self) -> list[Account]:
        return self._accounts

    @property
    def id(self) -> str:
        return self._request_json_data.get("id", "")

    @property
    def first_name(self) -> str:
        return self._request_json_data.get("first-name", "")

    @property
    def last_name(self) -> str:
        return self._request_json_data.get("last-name", "")

    @property
    def middle_name(self) -> str:
        return self._request_json_data.get("middle-name", "")

    @property
    def prefix_name(self) -> str:
        return self._request_json_data.get("prefix-name", "")

    @property
    def second_surname(self) -> str:
        return self._request_json_data.get("second-surname", "")

    @property
    def suffix_name(self) -> str:
        return self._request_json_data.get("suffix-name", "")

    @property
    def address(self) -> Address:
        address_data = self._request_json_data.get("address", {})
        return Address(address_data)

    @property
    def customer_suitability(self) -> Suitability:
        return Suitability(self._request_json_data.get("customer-suitability", {}))

    @property
    def mailing_address(self) -> Address:
        mailing_address_data = self._request_json_data.get("mailing-address", {})
        return Address(mailing_address_data)

    @property
    def is_foreign(self) -> str:
        return self._request_json_data.get("is-foreign", "")

    @property
    def regulatory_domain(self) -> str:
        return self._request_json_data.get("regulatory-domain", "")

    @property
    def usa_citizenship_type(self) -> str:
        return self._request_json_data.get("usa-citizenship-type", "")

    @property
    def home_phone_number(self) -> str:
        return self._request_json_data.get("home-phone-number", "")

    @property
    def mobile_phone_number(self) -> str:
        return self._request_json_data.get("mobile-phone-number", "")

    @property
    def work_phone_number(self) -> str:
        return self._request_json_data.get("work-phone-number", "")

    @property
    def birth_date(self) -> str:
        return self._request_json_data.get("birth-date", "")

    @property
    def email(self) -> str:
        return self._request_json_data.get("email", "")

    @property
    def external_id(self) -> str:
        return self._request_json_data.get("external-id", "")

    @property
    def foreign_tax_number(self) -> str:
        return self._request_json_data.get("foreign-tax-number", "")

    @property
    def tax_number(self) -> str:
        return self._request_json_data.get("tax-number", "")

    @property
    def tax_number_type(self) -> str:
        return self._request_json_data.get("tax-number-type", "")

    @property
    def birth_country(self) -> str:
        return self._request_json_data.get("birth-country", "")

    @property
    def citizenship_country(self) -> str:
        return self._request_json_data.get("citizenship-country", "")

    @property
    def visa_expiration_date(self) -> str:
        return self._request_json_data.get("visa-expiration-date", "")

    @property
    def visa_type(self) -> str:
        return self._request_json_data.get("visa-type", "")

    @property
    def agreed_to_margining(self) -> bool:
        return self._request_json_data.get("agreed-to-margining", False)

    @property
    def subject_to_tax_withholding(self) -> bool:
        return self._request_json_data.get("subject-to-tax-withholding", False)

    @property
    def agreed_to_terms(self) -> bool:
        return self._request_json_data.get("agreed-to-terms", False)

    @property
    def signature_of_agreement(self) -> str:
        return self._request_json_data.get("signature-of-agreement", "")

    @property
    def desk_customer_id(self) -> str:
        return self._request_json_data.get("desk-customer-id", "")

    @property
    def ext_crm_id(self) -> str:
        return self._request_json_data.get("ext-crm-id", "")

    @property
    def family_member_names(self) -> list[str]:
        return self._request_json_data.get("family-member-names", [])

    @property
    def gender(self) -> str:
        return self._request_json_data.get("gender", "")

    @property
    def has_industry_affiliation(self) -> bool:
        return self._request_json_data.get("has-industry-affiliation", False)

    @property
    def has_institutional_assets(self) -> bool:
        return self._request_json_data.get("has-institutional-assets", False)

    @property
    def has_listed_affiliation(self) -> bool:
        return self._request_json_data.get("has-listed-affiliation", False)

    @property
    def has_politial_affiliation(self) -> bool:
        return self._request_json_data.get("has-political-affiliation", False)

    @property
    def industry_affiliation_firm(self) -> str:
        return self._request_json_data.get("industry-affiliation-firm", "")

    @property
    def is_investment_advisor(self) -> bool:
        return self._request_json_data.get("is-investment-advisor", False)

    @property
    def listed_affiliation_symbol(self) -> str:
        return self._request_json_data.get("listed-affiliation-symbol", "")

    @property
    def political_organization(self) -> str:
        return self._request_json_data.get("political-organization", "")

    @property
    def user_id(self) -> str:
        return self._request_json_data.get("user-id", "")

    @property
    def has_delayed_quotes(self) -> bool:
        return self._request_json_data.get("has-delayed-quotes", False)

    @property
    def has_pending_or_approved_application(self) -> str:
        return self._request_json_data.get("has-pending-or-approved-application", "")

    @property
    def is_professional(self) -> bool:
        return self._request_json_data.get("is-professional", False)

    @property
    def permitted_account_type(self) -> str:
        return self._request_json_data.get("permitted-account-type", "")

    @property
    def created_at(self) -> datetime.datetime | None:
        created_at_str = self._request_json_data.get("created-at", "")
        if not created_at_str:
            return None
        # Handle ISO 8601 format with timezone: 2019-03-14T15:39:31.265+00:00
        return datetime.datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))

    @property
    def entity(self) -> Entity:
        return Entity(self._request_json_data.get("entity", {}))

    @property
    def identifiable_type(self) -> str:
        return self._request_json_data.get("identifiable-type", "")

    @property
    def person(self) -> Person:
        return Person(self._request_json_data.get("person", {}))

    def pretty_print(self) -> None:
        """Pretty print all customer data in a nicely formatted table."""
        console = Console()

        # Create basic information table
        basic_table = Table(
            title=f"Customer Details: {self.first_name} {self.last_name}",
            show_header=True,
            header_style="bold blue",
        )
        basic_table.add_column("Property", style="cyan", no_wrap=True)
        basic_table.add_column("Value", style="green")

        # Basic customer information
        basic_table.add_row("Customer ID", str(self.id))
        basic_table.add_row("External ID", str(self.external_id))
        basic_table.add_row(
            "Full Name",
            f"{self.prefix_name} {self.first_name} {self.middle_name} {self.last_name} {self.second_surname} {self.suffix_name}".strip(),
        )
        basic_table.add_row("Email", str(self.email))
        basic_table.add_row("Birth Date", str(self.birth_date))
        basic_table.add_row("Birth Country", str(self.birth_country))
        basic_table.add_row("Gender", str(self.gender))
        basic_table.add_row(
            "Created At", str(self.created_at) if self.created_at else "N/A"
        )

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
        contact_table.add_row("Mailing Address", str(self.mailing_address))

        # Legal and regulatory information table
        legal_table = Table(
            title="Legal & Regulatory Information",
            show_header=True,
            header_style="bold magenta",
        )
        legal_table.add_column("Property", style="cyan")
        legal_table.add_column("Value", style="green")

        legal_table.add_row("Regulatory Domain", str(self.regulatory_domain))
        legal_table.add_row("Is Foreign", str(self.is_foreign))
        legal_table.add_row("USA Citizenship Type", str(self.usa_citizenship_type))
        legal_table.add_row("Citizenship Country", str(self.citizenship_country))
        legal_table.add_row("Tax Number", str(self.tax_number))
        legal_table.add_row("Tax Number Type", str(self.tax_number_type))
        legal_table.add_row("Foreign Tax Number", str(self.foreign_tax_number))
        legal_table.add_row("Visa Type", str(self.visa_type))
        legal_table.add_row("Visa Expiration", str(self.visa_expiration_date))

        # Account and agreement information table
        account_table = Table(
            title="Account & Agreement Information",
            show_header=True,
            header_style="bold red",
        )
        account_table.add_column("Property", style="cyan")
        account_table.add_column("Value", style="green")

        account_table.add_row("User ID", str(self.user_id))
        account_table.add_row("Desk Customer ID", str(self.desk_customer_id))
        account_table.add_row("Ext CRM ID", str(self.ext_crm_id))
        account_table.add_row("Identifiable Type", str(self.identifiable_type))
        account_table.add_row(
            "Permitted Account Type", str(self.permitted_account_type)
        )
        account_table.add_row(
            "Agreed to Margining", "✓" if self.agreed_to_margining else "✗"
        )
        account_table.add_row("Agreed to Terms", "✓" if self.agreed_to_terms else "✗")
        account_table.add_row(
            "Subject to Tax Withholding",
            "✓" if self.subject_to_tax_withholding else "✗",
        )
        account_table.add_row(
            "Signature of Agreement", str(self.signature_of_agreement)
        )

        # Professional and affiliation information table
        professional_table = Table(
            title="Professional & Affiliation Information",
            show_header=True,
            header_style="bold cyan",
        )
        professional_table.add_column("Property", style="cyan")
        professional_table.add_column("Value", style="green")

        professional_table.add_row(
            "Is Professional", "✓" if self.is_professional else "✗"
        )
        professional_table.add_row(
            "Is Investment Advisor", "✓" if self.is_investment_advisor else "✗"
        )
        professional_table.add_row(
            "Has Delayed Quotes", "✓" if self.has_delayed_quotes else "✗"
        )
        professional_table.add_row(
            "Has Industry Affiliation", "✓" if self.has_industry_affiliation else "✗"
        )
        professional_table.add_row(
            "Has Listed Affiliation", "✓" if self.has_listed_affiliation else "✗"
        )
        professional_table.add_row(
            "Has Political Affiliation", "✓" if self.has_politial_affiliation else "✗"
        )
        professional_table.add_row(
            "Has Institutional Assets", "✓" if self.has_institutional_assets else "✗"
        )
        professional_table.add_row(
            "Industry Affiliation Firm", str(self.industry_affiliation_firm)
        )
        professional_table.add_row(
            "Listed Affiliation Symbol", str(self.listed_affiliation_symbol)
        )
        professional_table.add_row(
            "Political Organization", str(self.political_organization)
        )
        professional_table.add_row(
            "Has Pending/Approved Application",
            str(self.has_pending_or_approved_application),
        )
        family_members = (
            ", ".join(self.family_member_names) if self.family_member_names else "None"
        )
        professional_table.add_row("Family Member Names", family_members)

        # Linked accounts information table
        accounts_table = Table(
            title="Linked Accounts",
            show_header=True,
            header_style="bold green",
        )
        accounts_table.add_column("Account Number", style="cyan")
        accounts_table.add_column("Account Type", style="yellow")
        accounts_table.add_column("Status", style="green")

        if self.accounts:
            for account in self.accounts:
                # Get basic account info safely
                account_number = getattr(account, "account_number", "N/A")
                account_type = getattr(account, "account_type_name", "N/A")
                is_closed = getattr(account, "is_closed", None)
                status = (
                    "Closed"
                    if is_closed
                    else "Active"
                    if is_closed is not None
                    else "N/A"
                )

                accounts_table.add_row(str(account_number), str(account_type), status)
        else:
            accounts_table.add_row("No accounts found", "", "")

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
                contact_table,
                title="[bold yellow]Contact Information[/bold yellow]",
                border_style="yellow",
            )
        )
        console.print(
            Panel(
                legal_table,
                title="[bold magenta]Legal & Regulatory[/bold magenta]",
                border_style="magenta",
            )
        )
        console.print(
            Panel(
                account_table,
                title="[bold red]Account & Agreements[/bold red]",
                border_style="red",
            )
        )
        console.print(
            Panel(
                professional_table,
                title="[bold cyan]Professional & Affiliations[/bold cyan]",
                border_style="cyan",
            )
        )
        console.print(
            Panel(
                accounts_table,
                title="[bold green]Linked Accounts[/bold green]",
                border_style="green",
            )
        )

    def print_summary(self) -> None:
        """Print a simple text summary of the customer."""
        print(f"\n{'=' * 60}")
        print(f"CUSTOMER SUMMARY: {self.first_name} {self.last_name}")
        print(f"{'=' * 60}")
        print(f"Customer ID: {self.id}")
        print(f"External ID: {self.external_id}")
        print(f"Email: {self.email}")
        print(f"Birth Date: {self.birth_date}")
        print(f"Birth Country: {self.birth_country}")
        print(f"Citizenship: {self.citizenship_country}")
        print(f"Gender: {self.gender}")
        print(f"Is Foreign: {self.is_foreign}")
        print(f"Regulatory Domain: {self.regulatory_domain}")
        print(f"USA Citizenship Type: {self.usa_citizenship_type}")
        print(f"Tax Number: {self.tax_number} ({self.tax_number_type})")
        print(f"Created At: {self.created_at}")
        print(f"User ID: {self.user_id}")
        print(f"Professional: {'Yes' if self.is_professional else 'No'}")
        print(f"Investment Advisor: {'Yes' if self.is_investment_advisor else 'No'}")
        print(f"Agreed to Terms: {'Yes' if self.agreed_to_terms else 'No'}")
        print(f"Agreed to Margining: {'Yes' if self.agreed_to_margining else 'No'}")
        print(
            f"Phone: Home={self.home_phone_number}, Mobile={self.mobile_phone_number}, Work={self.work_phone_number}"
        )
        print(f"Address: {self.address}")
        print(f"Mailing Address: {self.mailing_address}")
        if self.family_member_names:
            family_members = ", ".join(self.family_member_names)
            print(f"Family Members: {family_members}")

        # Display linked accounts
        if self.accounts:
            print(f"Linked Accounts ({len(self.accounts)}):")
            for account in self.accounts:
                account_number = getattr(account, "account_number", "N/A")
                account_type = getattr(account, "account_type_name", "N/A")
                is_closed = getattr(account, "is_closed", None)
                status = (
                    "Closed"
                    if is_closed
                    else "Active"
                    if is_closed is not None
                    else "N/A"
                )

                try:
                    nlv = getattr(account, "net_liquidating_value", None)
                    nlv_display = f" (${nlv:,.2f})" if nlv is not None else ""
                except (AttributeError, TypeError):
                    nlv_display = ""

                print(f"  - {account_number}: {account_type} - {status}{nlv_display}")
        else:
            print("Linked Accounts: None")

        print(f"{'=' * 60}\n")
