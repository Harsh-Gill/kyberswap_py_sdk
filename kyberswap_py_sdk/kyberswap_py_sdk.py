import json
import requests
from web3 import Web3
from eth_account import Account
from typing import Optional, Dict, Any
from web3.middleware import geth_poa_middleware
import importlib.resources

# Constants
class AggregatorDomain:
    URL = "https://aggregator-api.kyberswap.com"

class ChainName:
    MAINNET = "ethereum"
    BSC = "bsc"
    ARBITRUM = "arbitrum"
    MATIC = "polygon"
    OPTIMISM = "optimism"
    AVAX = "avalanche"
    BASE = "base"
    CRONOS = "cronos"
    ZKSYNC = "zksync"
    FANTOM = "fantom"
    LINEA = "linea"
    POLYGONZKEVM = "polygon-zkevm"
    AURORA = "aurora"
    BTTC = "bittorrent"
    SCROLL = "scroll"

class ChainId:
    MAINNET = 1
    BSC = 56
    ARBITRUM = 42161
    MATIC = 137
    OPTIMISM = 10
    AVAX = 43114
    BASE = 8453
    CRONOS = 25
    ZKSYNC = 324
    FANTOM = 250
    LINEA = 59144
    POLYGONZKEVM = 1101
    AURORA = 1313161554
    BTTC = 199
    ZKEVM = 1101
    SCROLL = 534352

# Token Class
class Token:
    def __init__(self, address: str, chain_id: int, decimals: int, symbol: Optional[str] = None, name: Optional[str] = None):
        self.address = address
        self.chain_id = chain_id
        self.decimals = decimals
        self.symbol = symbol
        self.name = name

# KyberSwap SDK
class KyberSwapSDK:
    def __init__(self, chain: str, rpc_url: str, private_key: Optional[str] = None):
        self.chain = chain
        self.rpc_url = rpc_url
        self.private_key = private_key
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))

        # Add POA middleware for chains like Polygon, BSC, etc.
        if self.chain in [ChainName.MATIC, ChainName.BSC, ChainName.ARBITRUM]:
            self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        self.signer = self._get_signer() if private_key else None

    def _get_signer(self):
        if not self.private_key:
            raise ValueError("Private key is required for signing transactions.")
        return Account.from_key(self.private_key)

    async def get_swap_route(self, token_in: Token, token_out: Token, amount_in: float) -> Optional[Dict[str, Any]]:
        """Fetch the best swap route for a given token pair."""
        target_path = f"/{self.chain}/api/v1/routes"
        params = {
            "tokenIn": token_in.address,
            "tokenOut": token_out.address,
            "amountIn": str(int(amount_in * 10 ** token_in.decimals))
        }
        try:
            response = requests.get(AggregatorDomain.URL + target_path, params=params)
            response.raise_for_status()
            return response.json().get('data')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching swap route: {e}")
            return None

    async def build_swap_transaction(self, token_in: Token, token_out: Token, amount_in: float, slippage_tolerance: int = 10) -> Optional[Dict[str, Any]]:
        """Build a swap transaction with encoded data."""
        swap_route = await self.get_swap_route(token_in, token_out, amount_in)
        if not swap_route:
            return None

        target_path = f"/{self.chain}/api/v1/route/build"
        request_body = {
            "routeSummary": swap_route['routeSummary'],
            "sender": self.signer.address,
            "recipient": self.signer.address,
            "slippageTolerance": slippage_tolerance
        }
        try:
            response = requests.post(AggregatorDomain.URL + target_path, json=request_body)
            response.raise_for_status()
            return response.json().get('data')
        except requests.exceptions.RequestException as e:
            print(f"Error building swap transaction: {e}")
            return None

    async def execute_swap(self, 
                           token_in: Token, 
                           token_out: Token, 
                           amount_in: float, 
                           slippage_tolerance: int = 10,
                           gas_fee_wei : int = 100,
                           gas : int = 200000,
                           nonce: Optional[int] = None,
                           ) -> Optional[str]:
        """Execute a swap transaction on-chain."""
        if not self.signer:
            raise ValueError("Signer is required to execute swaps.")

        swap_data = await self.build_swap_transaction(token_in, token_out, amount_in, slippage_tolerance)
        if not swap_data:
            return None

        # Approve token spending
        await self._approve_token(token_in, swap_data['routerAddress'], swap_data['amountIn'])

        # Build and send transaction
        transaction = {
            'to': swap_data['routerAddress'],
            'data': swap_data['data'],
            'gas': gas,
            'gasPrice': self.web3.to_wei( str(gas_fee_wei), 'gwei'),
            'nonce': self.web3.eth.get_transaction_count(self.signer.address) if nonce is None else nonce,
        }
        signed_tx = self.signer.sign_transaction(transaction)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Swap transaction sent with hash: {tx_hash.hex()}")

        # Wait for transaction receipt
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt #.transactionHash.hex()

    async def _approve_token(self, token: Token, spender: str, amount: int):
        """Approve token spending for a given spender."""
        if not self.signer:
            raise ValueError("Signer is required for token approval.")

        token_contract = self.web3.eth.contract(address=token.address, abi=self._load_erc20_abi())
        allowance = token_contract.functions.allowance(self.signer.address, spender).call()
        
        allowance = int(allowance)
        amount = int(amount)
        
        if allowance >= amount:
            return

        print(f"Approving {token.symbol} for spending...")
        approve_tx = token_contract.functions.approve(spender, amount).build_transaction({
            'from': self.signer.address,
            'nonce': self.web3.eth.get_transaction_count(self.signer.address),
        })
        signed_approve_tx = self.signer.sign_transaction(approve_tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
        self.web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Approval transaction confirmed with hash: {tx_hash.hex()}")

    def _load_erc20_abi(self) -> list:
        """Load the ERC20 ABI from a JSON file."""
        # Load the ERC20 ABI from the package
        with importlib.resources.open_text("kyberswap_py_sdk.abis", "erc20.json") as f:
            return json.load(f)
