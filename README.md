# TastyPy

A modern Python wrapper for the TastyTrade API with OAuth2 authentication.

## Features

- 🔐 **OAuth2 Authentication** - Secure authentication with client secret and
  refresh tokens
- 🔄 **Automatic Token Refresh** - Access tokens automatically refresh when
  expired
- 📊 **Full API Coverage** - Access accounts, positions, orders, market data,
  and more
- 🎨 **Rich Console Output** - Beautiful terminal formatting with Rich library
- 🐍 **Modern Python** - Type hints, async support, and Python 3.10+ syntax

## Installation

```bash
pip install tastypy
```

Or with uv:

```bash
uv add tastypy
```

## Quick Start

### 1. Create OAuth Credentials

1. Go to [my.tastytrade.com](https://my.tastytrade.com)
2. Navigate to **Manage > My Profile > API > OAuth Applications**
3. Create a new OAuth application and save your **client_secret**
4. Generate a personal grant and save your **refresh_token**

See the [OAuth2 Quick Start Guide](docs/sessions/oauth-example.md) for detailed
instructions.

### 2. Use TastyPy

```python
from tastypy import Session

# Initialize session with OAuth2 credentials
session = Session(
    client_secret="your_client_secret",
    refresh_token="your_refresh_token"
)

# Access tokens are automatically managed
accounts = session.client.get("/customers/me/accounts")
print(accounts.json())
```

### 3. Environment Variables (Recommended)

Create a `.env` file:

```text
TASTY_CLIENT_SECRET=your_client_secret_here
TASTY_REFRESH_TOKEN=your_refresh_token_here
```

Then load and use:

```python
import os
from dotenv import load_dotenv
from tastypy import Session

load_dotenv()

session = Session(
    client_secret=os.getenv("TASTY_CLIENT_SECRET"),
    refresh_token=os.getenv("TASTY_REFRESH_TOKEN")
)
```

## Documentation

- [OAuth2 Quick Start Guide](docs/sessions/oauth.md) - Complete OAuth2 setup
  guide
- [API Reference](https://developer.tastytrade.com/) - Official API
  documentation

## Examples

### Get Account Information

```python
from tastypy import Session
from tastypy.customer import Customer

session = Session(client_secret="...", refresh_token="...")

customer = Customer(session)
customer.sync()
customer.pretty_print()
```

### Get Positions

```python
from tastypy.account import Account, Positions

account = Account(session, customer.id, account_number)
account.sync()

positions = Positions(session, account_number)
positions.sync()
positions.pretty_print()
```

### Manage Watchlists

```python
from tastypy.watchlists import UserWatchlists

watchlists = UserWatchlists(session)
watchlists.sync()

# Create a new watchlist
new_watchlist = watchlists.create(
    name="Tech Stocks",
    watchlist_entries=[
        {"symbol": "AAPL"},
        {"symbol": "MSFT"},
        {"symbol": "GOOGL"}
    ]
)
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/benvoliobenji/tastypy.git
cd tastypy

# Install dependencies with uv
uv sync

# Copy environment template
cp .env.example .env
# Edit .env with your OAuth2 credentials
```

### Running Tests

```bash
# Run the demo script
uv run python main.py

# With custom credentials
uv run python main.py --client-secret="..." --refresh-token="..."
```

## Migration from Username/Password

If you're upgrading from an older version that used username/password:

**Before:**

```python
session = Session(username="user", password="pass")
session.login()
```

**After:**

```python
session = Session(
    client_secret="your_client_secret",
    refresh_token="your_refresh_token"
)
# No login() call needed - automatic!
```

See the [OAuth2 Quick Start Guide](docs/sessions/oauth.md) for complete
migration instructions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[LICENSE](LICENSE)

## Acknowledgments

- Built for the [TastyTrade API](https://developer.tastytrade.com/)
- Inspired by the tastytrade community
