from .equity_option import EquityOption
from ....session import Session
from ....errors import translate_error_code
import datetime
import enum


class OptionType(enum.Enum):
    CALL = "C"
    PUT = "P"


class EquityOptionSymbol:
    _endpoint_url = ""
    _session: Session
    _equity_option: EquityOption

    def __init__(self, active_session: Session):
        self._session = active_session

    def sync(
        self,
        symbol: str,
        expiration_date: datetime.date,
        option_type: OptionType,
        strike_price: float,
    ):
        """Fetch the latest data for the specified equity symbol."""
        # Convert to OCC format:
        # Symbol (padded to 6 characters)
        # Expiration Date (YYMMDD)
        # Option Type (C or P)
        # Strike Price (8 digits, leading zeros, 3 decimal places implied)
        occ_symbol = f"{symbol.upper():<6}{expiration_date.strftime('%y%m%d')}{option_type.value}{int(strike_price * 1000):08d}"

        self._endpoint_url = f"/instruments/equity-options/{occ_symbol}"

        response = self._session._client.get(
            self._endpoint_url,
        )
        if response.status_code == 200:
            data = response.json()
            equity_data = data.get("data", {})
            if equity_data:
                self._equity_option = EquityOption(equity_data)
            else:
                raise ValueError(f"No data found for symbol: {symbol}")
        else:
            error_code = response.status_code
            error_message = response.json().get("error", {}).get("message", "")
            raise translate_error_code(error_code, error_message)

    @property
    def equity_option(self) -> EquityOption:
        """Get the currently loaded equity option."""
        if not hasattr(self, "_equity_option"):
            raise ValueError("No equity option data loaded. Call sync() first.")
        return self._equity_option

    def __str__(self):
        return f"EquitySymbol: {self.equity_option.symbol}"

    def print_summary(self):
        """Print a simple text summary of the equity option."""
        self.equity_option.print_summary()

    def pretty_print(self):
        """Pretty print equity option data in a nicely formatted table."""
        self.equity_option.pretty_print()
