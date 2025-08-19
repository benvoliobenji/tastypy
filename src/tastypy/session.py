import httpx
from .errors import translate_error_code
from pathlib import Path


# TODO: ADD OAUTH2 SUPPORT
class Session:
    _extension_url = "/sessions"
    session_id: str = ""
    _remember_token: str = ""
    _remember_token_file: Path = Path("~/.tastyworks/remember_token.txt").expanduser()

    def __init__(
        self,
        username: str,
        password: str,
        remember_me: bool = True,
        base_url: str = "https://api.tastyworks.com",
    ):
        self.username = username
        self.password = password
        self.remember_me = remember_me
        self.session_id = ""
        self._remember_token = ""
        self.base_url = base_url
        self._full_url = base_url + self._extension_url

    @classmethod
    def from_remember_token(
        cls,
        username: str,
        remember_token: str,
        base_url: str = "https://api.tastyworks.com",
    ):
        """
        Create a Session instance and log in from an existing remember token.
        """
        instance = cls(
            username=username, password="", remember_me=True, base_url=base_url
        )
        instance._remember_token = remember_token
        return instance

    def login(self) -> bool:
        """
        Log in to the Tastyworks API and retrieve session and remember tokens.
        """
        if self._remember_token is not None:
            # Default to try to use remember token over password for safety
            payload = {
                "login": self.username,
                "remember-token": self._remember_token,
                "remember-me": self.remember_me,
            }
        else:
            # Fallback to password if no remember token is provided
            payload = {
                "login": self.username,
                "password": self.password,
                "remember-me": self.remember_me,
            }
        response = httpx.post(self._full_url, json=payload)
        if response.status_code == 201:
            data = response.json()["data"]
            self.session_id = data["session-token"]
            self._remember_token = data["remember-token"]
            return True
        else:
            error_code = response.status_code
            error_message = response.json()["error"]["message"]
            raise translate_error_code(error_code, error_message)

    def is_logged_in(self) -> bool:
        """Check if the session is logged in. This does not make an API call, but relies on the user to have a valid session token generated (either by logging in or providing a non-expired remember token).


        Returns:
            bool: _description_
        """
        return self.session_id is not None

    def dump_remember_token(self, file_out: Path):
        """Dumps the remember token to a file.
        This is useful for persisting the remember token across sessions without needing to save a password.

        Args:
            file_out (Path): The file to write the remember token to.
        """
        self._remember_token_file = file_out
        if not file_out.exists():
            file_out.touch()
        file_out.write_text(self._remember_token)

    def logout(self) -> bool:
        """
        Log out of the Tastyworks API and invalidate the session token. This will also delete the remember token if it exists, as deleting a session invalidates all generated tokens.
        """
        headers = {"Authorization": self.session_id}
        response = httpx.delete(self._full_url, headers=headers)
        if response.status_code == 204:  # No Content
            # Delete the remember token if it exists
            if (
                self._remember_token_file is not None
                and self._remember_token_file.exists()
            ):
                self._remember_token_file.unlink()
            return True
        else:
            error_code = response.status_code
            error_message = response.json()["error"]["message"]
            raise translate_error_code(error_code, error_message)

    def __open__(self):
        """Open the session."""
        self.login()

    def __close__(self):
        """Close the session."""
        self.logout()
