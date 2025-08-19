class Address:
    def __init__(self, address_data: dict[str, str]):
        self._address_data = address_data

    @property
    def city(self) -> str:
        return self._address_data.get("city", "")

    @property
    def country(self) -> str:
        return self._address_data.get("country", "")

    @property
    def is_domestic(self) -> bool:
        return self._address_data.get("country", "") == "United States"

    @property
    def is_foreign(self) -> bool:
        return self._address_data.get("country", "") != "United States"

    @property
    def postal_code(self) -> str:
        return self._address_data.get("postal-code", "")

    @property
    def state_region(self) -> str:
        return self._address_data.get("state-region", "")

    @property
    def street(self) -> str:
        return (
            self._address_data.get("street-one", "")
            + " "
            + self._address_data.get("street-two", "")
            + " "
            + self._address_data.get("street-three", "")
        )

    def __str__(self) -> str:
        return f"{self.street}, {self.city}, {self.state_region}, {self.postal_code}, {self.country}"
