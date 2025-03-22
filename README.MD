# KyberSwap Python SDK

This Python SDK provides a simple and easy-to-use interface for interacting with the KyberSwap Aggregator API. It allows you to fetch swap routes, build transactions, and execute swaps on supported chains. The SDK is designed to be modular, extensible, and developer-friendly.

## Before Anything, Thank You KyberSwap!

We would like to extend our heartfelt thanks to KyberSwap for providing such an amazing and free service. Your aggregator API has made it incredibly easy for developers to integrate decentralized swaps into their applications. Keep up the great work!

## Developed with ❤️ by Harsh from BaseNerds/Basehound.

For questions or feedback, feel free to reach out!

## Features

- **Chain Selection**: Easily switch between supported chains (e.g., Ethereum, Polygon, BSC, Arbitrum, etc.).
- **Route Fetching**: Fetch the best swap route for a given token pair.
- **Swap Execution**: Build and execute swaps with encoded transaction data.

## Installation - Tested on Python 3.10 or higher.

1. Pip install Library

```Bash
pip install kyberswap_py_sdk
```

2. Or Directly Clone the repository:

   ```Bash
   git clone https://github.com/your-repo/kyberswap-python-sdk.git
   cd kyberswap-python-sdk
   pip install -r requirements.txt
   ```

## Usage - Example with Polygon

### 1. Initialize the SDK

To use the SDK, initialize it with the desired chain, RPC URL, and your private key (optional for read-only operations).

```Python
from kyberswap_py_sdk import KyberSwapSDK, ChainName, Token
import asyncio

# Define tokens - 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE represents ETH
token_in = Token(
    address="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
    chain_id=ChainId.BASE,
    decimals=18,
    symbol="ETH",
    name="Ethereum"
)

token_out = Token(
    address="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    chain_id=ChainId.BASE,
    decimals=18,
    symbol="USDC",
    name="USDC"
)

token_in_amount = 0.1

# Initialize SDK
private_key = "YOUR_PRIVATE_KEY"  # Replace with your actual private key

sdk = KyberSwapSDK(
    chain=ChainName.BASE,
    rpc_url="YOUR_RPC_OF_CHOICE",
    private_key=private_key)

# get swap route
swap_route = asyncio.run(sdk.get_swap_route(token_in,
                                            token_out,
                                            amount_in=token_in_amount))

# get info about swap route
print(f"Swap Route: {swap_route}")

route_gas = int(swap_route['routeSummary']['gas'])
route_gas_price = int(swap_route['routeSummary']['gasPrice'])


# # Execute swap

# # Legacy Transaction (Type 0)
# tx_receipt = asyncio.run(sdk.execute_swap(
#     token_in,
#     token_out,
#     amount_in=token_in_amount,
#     gas=route_gas*1.5,
#     gas_fee_wei= route_gas_price,
#     txn_type=0
#     ))

# # EIP-2930 Transaction (Type 1)
# tx_receipt = asyncio.run(sdk.execute_swap(
#     token_in,
#     token_out,
#     amount_in=0.1,
#     slippage_tolerance=10,
#     gas=int(route_gas*3),
#     gas_fee_wei=int(route_gas_price*1.5),
#     txn_type=1,
#     access_list=[{
#         "address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  # USDC contract
#         "storageKeys": ["0x0000000000000000000000000000000000000000000000000000000000000000"]
#     }]
# ))

# EIP-1559 Transaction (Type 2)
tx_receipt = asyncio.run(sdk.execute_swap(
    token_in,
    token_out,
    amount_in=token_in_amount,
    slippage_tolerance=10,
    gas=route_gas*3,
    gas_fee_wei=route_gas_price*1.5,
    txn_type=2,
    max_priority_fee_wei=route_gas_price*1.1
))


if tx_receipt:
    print(f"Swap executed successfully! Transaction: {tx_receipt}")

```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
