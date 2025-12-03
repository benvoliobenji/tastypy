# OAuth2 Quick Start Guide

This guide shows you how to use TastyPy with OAuth2 authentication.

## Why OAuth2?

OAuth2 is now **mandatory** for accessing the TastyTrade API. Legacy
username/password authentication is no longer supported.

In addition, OAuth2 is more secure than username/password authentication:

- **Access tokens expire every 15 minutes** (vs 24-hour session tokens)
- **Scoped permissions** (read-only or trading access)
- **Refresh tokens never expire** (no need to re-authenticate)
- **No password storage** (your password never leaves TastyTrade)

## Setup Steps

### 1. Create an OAuth Application

1. Go to [my.tastytrade.com](https://my.tastytrade.com)
2. Navigate to **Manage > My Profile > API > OAuth Applications**
3. Click **+ New OAuth client**
4. Fill in:
   - **Redirect URI**: `http://localhost:8000` (for personal use)
   - **Scopes**: Check `read` and/or `trade`
5. Click **Create**
6. **IMPORTANT**: Save your **Client Secret** immediately (shown only once!)

### 2. Generate a Personal Grant

1. On the OAuth Applications page, click **Manage** on your application
2. Click **Create Grant**
3. **Save your Refresh Token** (this is what you'll use to authenticate)

### 3. Use TastyPy

#### Option A: Environment Variables (.env file)

Create a `.env` file in your project root:

```
TASTY_CLIENT_SECRET=your_client_secret_here
TASTY_REFRESH_TOKEN=your_refresh_token_here
```

Then use TastyPy:

```python
from tastypy import Session

session = Session(
    client_secret="your_client_secret",
    refresh_token="your_refresh_token"
)

# Access token is automatically fetched on first API call
response = session.client.get("/customers/me")
print(response.json())
```

#### Option B: Direct Credentials

```python
from tastypy import Session

session = Session(
    client_secret="your_client_secret_here",
    refresh_token="your_refresh_token_here"
)

# Use the session
accounts = session.client.get("/customers/me/accounts")
print(accounts.json())
```

#### Option C: Sandbox Testing

```python
from tastypy import Session

session = Session(
    client_secret="your_sandbox_client_secret",
    refresh_token="your_sandbox_refresh_token",
    base_url="https://api.cert.tastyworks.com"  # Sandbox URL
)

# Test with sandbox account
response = session.client.get("/customers/me")
```

## Automatic Token Refresh

TastyPy automatically refreshes your access token when it expires:

```python
session = Session(client_secret="...", refresh_token="...")

# First call: Gets access token automatically
accounts = session.client.get("/customers/me/accounts")

# ... 20 minutes later ...

# This call: Automatically refreshes the expired token
positions = session.client.get("/accounts/ABC123/positions")
```

## Manual Token Refresh

You can manually refresh if needed:

```python
session = Session(client_secret="...", refresh_token="...")

# Check if logged in (has valid access token)
if not session.is_logged_in():
    session.refresh()

# Or refresh proactively
session.refresh()
```

## Context Manager Usage

Use the session as a context manager for automatic cleanup:

```python
from tastypy import Session

with Session(client_secret="...", refresh_token="...") as session:
    accounts = session.client.get("/customers/me/accounts")
    print(accounts.json())
    # Session is automatically closed when exiting the block
```

## Complete Example

```python
from tastypy import Session
from tastypy.customer import Customer
from tastypy.account import Account

# Initialize session
session = Session(
    client_secret="your_client_secret",
    refresh_token="your_refresh_token"
)

# Get customer info
customer = Customer(session)
customer.sync()
print(f"Customer: {customer.first_name} {customer.last_name}")

# Get accounts
accounts_response = session.client.get("/customers/me/accounts")
accounts_data = accounts_response.json()["data"]["items"]

for account_data in accounts_data:
    account_number = account_data["account"]["account-number"]

    # Get account details
    account = Account(session, customer.id, account_number)
    account.sync()

    print(f"Account: {account.account_number}")
    print(f"  Type: {account.account_type}")
    print(f"  Nickname: {account.nickname}")

# Session automatically refreshes tokens as needed throughout
```

## Troubleshooting

### Invalid client_secret

- Make sure you copied the entire secret when creating the OAuth app
- Client secrets are only shown once - if lost, regenerate a new one

### Invalid refresh_token

- Refresh tokens from grants never expire unless you delete the grant
- Make sure you copied the entire token
- If compromised, delete the grant and create a new one

### 401 Unauthorized errors

- Your OAuth app might not have the required scopes
- Check that your app has `read` and/or `trade` scopes enabled

### Sandbox vs Production

- Make sure your credentials match the environment
- Sandbox URL: `https://api.cert.tastyworks.com`
- Production URL: `https://api.tastyworks.com`

## Security Best Practices

1. **Never commit credentials to git**

   - Add `.env` to your `.gitignore`
   - Use environment variables in production

2. **Store secrets securely**

   - Use a password manager for your client secret
   - Never share your refresh token

3. **Use appropriate scopes**

   - Only request `read` scope if you don't need trading
   - Separate apps for different use cases

4. **Rotate credentials periodically**
   - Delete old grants and create new ones
   - Regenerate client secrets if concerned about exposure

## Migration from Username/Password

If you're upgrading from the old username/password authentication:

**Before (Old):**

```python
session = Session(username="user", password="pass")
session.login()
```

**After (New):**

```python
session = Session(
    client_secret="your_client_secret",
    refresh_token="your_refresh_token"
)
# No need to call login() - automatic!
```

The new OAuth2 approach is more secure and doesn't require storing passwords.
