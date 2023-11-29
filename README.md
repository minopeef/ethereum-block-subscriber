# Ethereum Block Subscriber

This Python script provides a simple Ethereum block subscriber using WebSocket to receive updates about new blocks. It includes a class for the subscriber and an observer class that can be extended to perform custom actions when a new block is mined.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- `websockets` library (install via `pip install websockets`)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/okpyjs/ethereum-block-subscriber.git
   cd ethereum-block-subscriber
   ```

2. Install dependencies:

   ```bash
   pip install websockets
   ```

### Usage

1. Modify the script to include your desired WebSocket URL.

   ```python
   web_socket_url = "wss://your-ethereum-node-url"
   ```

2. Run the script:

   ```bash
   python ethereum_block_subscriber.py
   ```

## Features

- Subscribes to new block events on the Ethereum network using WebSocket.
- Notifies registered observers when a new block is mined.

## Classes

### `BlockSubscriber`

- Manages the WebSocket connection and subscribes to new block events.
- Maintains a set of observers interested in receiving block updates.

### `BlockObserver`

- An abstract class that can be extended to define custom actions when a new block is mined.
- Must implement the `update` method.

## Example

```python
import asyncio

from ethereum_block_subscriber import BlockSubscriber, BlockObserver

# Initialize the subscriber and observer
web_socket_url = "wss://mainnet.gateway.tenderly.co"
subscriber = BlockSubscriber(web_socket_url)
observer = BlockObserver()

# Add the observer to the subscriber's list
subscriber.add_observer(observer)

try:
    # Run the subscriber's event loop
    loop = asyncio.get_event_loop()
    loop.create_task(subscriber.subscribe_to_blocks())
    loop.run_forever()
except Exception as e:
    print(e)
finally:
    loop.close()
```

## License

This project is licensed under the MIT License.
