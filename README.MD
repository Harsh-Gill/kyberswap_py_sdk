# KyberSwap Python SDK

This Python SDK provides a simple and easy-to-use interface for interacting with the KyberSwap Aggregator API. It allows you to fetch swap routes, build transactions, and execute swaps on supported chains. The SDK is designed to be modular, extensible, and developer-friendly.

## Before Anything, Thank You KyberSwap!

We would like to extend our heartfelt thanks to KyberSwap for providing such an amazing and free service. Your aggregator API has made it incredibly easy for developers to integrate decentralized swaps into their applications. Keep up the great work!

## Developed with ❤️ by Harsh from BaseNerds/Basehound.

For questions or feedback, feel free to reach out!

## Features

- **Chain Selection**: Easily switch between supported chains (e.g., Ethereum, Polygon, BSC, Arbitrum, etc.).
- **Token Management**: Define tokens with the `Token` class.
- **Route Fetching**: Fetch the best swap route for a given token pair.
- **Swap Execution**: Build and execute swaps with encoded transaction data.
- **Error Handling**: Robust error handling for API calls and on-chain transactions.
- **Testnet Support**: Includes examples for testnet usage.

## Installation - Tested on Python 3.10 or higher.

1. Pip install Library

```Bash
pip install kyberswap_py_sdk
```

2. Or Directly Clone the repository:

   ```Bash
   git clone https://github.com/Harsh-Gill/kyberswap_py_sdk.git
   cd kyberswap-python-sdk
   pip install -r requirements.txt
   ```

## Usage - Example with Polygon

### 1. Initialize the SDK

To use the SDK, initialize it with the desired chain, RPC URL, and your private key (optional for read-only operations).

```Python
from kyberswap_py_sdk import KyberSwapSDK, ChainName, Token

# Initialize SDK for Polygon Mainnet
sdk = KyberSwapSDK(
chain=ChainName.MATIC,
rpc_url="https://polygon.llamarpc.com", # Example for Polygon
private_key="your_private_key_here" # Optional for read-only operations
)
```

### 2. Define Tokens

Use the `Token` class to define the tokens you want to swap.

```python

# Define USDC.e (Polygon) as token_in

token_in = Token(
address="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
chain_id=ChainId.MATIC,
decimals=6,
symbol="USDC.e",
name="USD Coin (PoS)"
)


# Define KNC (Polygon) as token_out

token_out = Token(
address="0x1C954E8fe737F99f68Fa1CCda3e51ebDB291948C",
chain_id=ChainId.MATIC,
decimals=18,
symbol="KNC",
name="KyberNetwork Crystal v2 (PoS)"
)
```

### 3. Fetch Swap Routes

Fetch the best swap route for a given token pair and amount.

```python
import asyncio
async def fetch_swap_route():
   swap_route = await sdk.get_swap_route(token_in, token_out,amount_in=10.0)
   print("Swap Route:", swap_route)

# Run the function
asyncio.run(fetch_swap_route())
```

### 4. Build Swap Transaction

Build a swap transaction with encoded data.

```python
async def build_swap_tx():
   swap_data = await sdk.build_swap_transaction(token_in, token_out, amount_in=10.0)
   print("Swap Data:", swap_data)

# Run the function
asyncio.run(build_swap_tx())
```

### 5. Execute Swap

Execute the swap transaction on-chain.

```python
async def execute_swap():
tx_hash = await sdk.execute_swap(token_in, token_out, amount_in=10.0)
if tx_hash:
print(f"Swap executed successfully! Transaction hash: {tx_hash}")

# Run the function

asyncio.run(execute_swap())
```

## Ethereum Mainnet Example - Can use Tenderly

### 1. Initialize SDK for Ethereum Mainnet

Use the appropriate RPC URL and token addresses.

```python

from kyberswap_py_sdk import KyberSwapSDK, ChainName, ChainId, Token
import asyncio

# Define tokens
token_in = Token(
    address="0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",
    chain_id=ChainId.MAINNET,
    decimals=18,
    symbol="SHIB",
    name="Shiba Inu"
)
token_out = Token(
    address="0x6982508145454Ce325dDbE47a25d4ec3d2311933",
    chain_id=ChainId.MAINNET,
    decimals=18,
    symbol="PEPE",
    name="Pepe"
)

# Initialize SDK
private_key = "YOUR_PRIVATE_KEY"  # Replace with your actual private key
RPC_URL = "YOUR_RPC_URL"  # Replace with your actual RPC URL
sdk = KyberSwapSDK(chain=ChainName.MAINNET, rpc_url=RPC_URL, private_key=private_key)

# get swap route
swap_route = asyncio.run(sdk.get_swap_route(token_in, token_out, amount_in=10.0))

# get info about swap route
print(f"Swap Route: {swap_route}")

# Execute swap
tx_receipt = asyncio.run(sdk.execute_swap(token_in, token_out, amount_in=10.0))
if tx_receipt:
    print(f"Swap executed successfully! Transaction: {tx_receipt}")

```

## Error Handling

The SDK includes robust error handling for:

- Invalid RPC URLs.
- Invalid private keys.
- Insufficient token allowances.
- API request failures.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

# kyberswap_py_sdk
