from .equity import Equity
from ...session import Session
from ...errors import translate_error_code


class EquitySymbol:
    _endpoint_url = ""
    _session: Session
    _equity: Equity

    def __init__(self, active_session: Session):
        self._session = active_session

    def sync(self, symbol: str):
        """Fetch the latest data for the specified equity symbol."""
        self._endpoint_url = f"/instruments/equities/{symbol}"

        response = self._session._client.get(
            self._endpoint_url,
        )
        if response.status_code == 200:
            data = response.json()
            equity_data = data.get("data", {})
            if equity_data:
                self._equity = Equity(equity_data)
            else:
                raise ValueError(f"No data found for symbol: {symbol}")
        else:
            error_code = response.status_code
            error_message = response.json().get("error", {}).get("message", "")
            raise translate_error_code(error_code, error_message)

    @property
    def equity(self) -> Equity:
        """Get the currently loaded equity."""
        if not hasattr(self, "_equity"):
            raise ValueError("No equity data loaded. Call sync() first.")
        return self._equity

    def __str__(self):
        return f"EquitySymbol: {self.equity.symbol} - {self.equity.description}"

    def print_summary(self):
        """Print a simple text summary of the equity."""
        self.equity.print_summary()

    def pretty_print(self):
        """Pretty print equity data in a nicely formatted table."""
        self.equity.pretty_print()
