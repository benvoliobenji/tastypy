import enum


class Exchange(enum.Enum):
    """Enumeration of supported exchanges for futures and options."""

    CBOED = "CBOED"  # Chicago Board Options Exchange
    CFE = "CFE"  # CBOE Futures Exchange
    CME = "CME"  # Chicago Mercantile Exchange
    SMALLS = "SMALLS"  # Small Exchange

    def __str__(self):
        return self.value
