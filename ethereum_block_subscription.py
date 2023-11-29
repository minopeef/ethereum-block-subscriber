import asyncio
import json

from websockets import connect


class BlockSubscriber:
    """
    Class for subscribing to new block events using a WebSocket connection.

    Attributes:
    - web_socket_url (str): The WebSocket URL for connecting to the Ethereum node.
    - observers (set): Set to store observers interested in block updates.
    """

    def __init__(self, web_socket_url):
        """
        Initializes a new instance of the BlockSubscriber class.

        Parameters:
        - web_socket_url (str): The WebSocket URL for connecting to the Ethereum node.
        """
        self.web_socket_url = web_socket_url
        self.observers = set()

    def add_observer(self, observer):
        """
        Adds an observer to the set of observers.

        Parameters:
        - observer: The observer object that wants to receive block updates.
        """
        self.observers.add(observer)

    def remove_observer(self, observer):
        """
        Removes an observer from the set of observers.

        Parameters:
        - observer: The observer object to be removed.
        """
        self.observers.remove(observer)

    async def notify_observers(self, block_number):
        """
        Notifies all registered observers about a new block.

        Parameters:
        - block_number (int): The block number to be sent to observers.
        """
        for observer in self.observers:
            await observer.update(block_number)

    async def subscribe_to_blocks(self):
        """
        Connects to the Ethereum node via WebSocket and subscribes to new block events.
        Notifies observers when a new block is received.
        """
        async with connect(self.web_socket_url) as ws:
            # Subscribe to new block events
            await ws.send(
                json.dumps({"id": 1, "method": "eth_subscribe", "params": ["newHeads"]})
            )
            subscription_response = await ws.recv()
            print(f"Subscription response: {subscription_response}")

            while True:
                try:
                    # Receive messages from the WebSocket
                    message = await asyncio.wait_for(ws.recv(), timeout=60)
                    json_message = json.loads(message)
                    # Extract block number from the received message
                    block_number = int(json_message["params"]["result"]["number"], 16)
                    print(f"New block mined - Block Number: {block_number}")
                    # Notify all observers about the new block
                    await self.notify_observers(block_number)
                except asyncio.exceptions.TimeoutError as e:
                    print(e)


class BlockObserver:
    """
    Class representing an observer interested in receiving updates about new blocks.

    Methods:
    - update(block_number): Called when a new block is mined, passing the block number.
    """

    async def update(self, block_number):
        """
        Called when a new block is mined. Prints a message with the block number.

        Parameters:
        - block_number (int): The block number of the newly mined block.
        """
        print(f"Observer notified - New block mined - Block Number: {block_number}")


if __name__ == "__main__":
    # WebSocket URL for connecting to the Ethereum node
    web_socket_url = "wss://mainnet.gateway.tenderly.co"

    # Create instances of BlockSubscriber and BlockObserver
    subscriber = BlockSubscriber(web_socket_url)
    observer = BlockObserver()

    # Add the observer to the subscriber's list of observers
    subscriber.add_observer(observer)

    try:
        # Set up the asyncio event loop and run the subscriber's subscription task
        loop = asyncio.get_event_loop()
        loop.create_task(subscriber.subscribe_to_blocks())
        loop.run_forever()
    except Exception as e:
        print(e)
    finally:
        # Close the event loop in the finally block
        loop.close()
