
import asyncio
import spade
from fipa_acl_comm import SenderAgent, ReceiverAgent

async def main():
    print("=" * 50)
    print("SIMPLE FIPA-ACL DEMO")
    print("Two agents communicating")
    print("=" * 50)


    # Create agents
    sender = SenderAgent("sender@localhost", "password123")
    receiver = ReceiverAgent("receiver@localhost", "password123")
    
    print("\nStarting agents...")
    
    # Start receiver FIRST so it's ready when sender sends messages
    await receiver.start()
    await asyncio.sleep(2)  
    
    await sender.start()
    await asyncio.sleep(1)  # Brief pause
    
    print("\nAgents started successfully!")
    print("\nAGENT COMMUNICATION:")
    print("1. Sender → REQUEST (asks for time)")
    print("2. Receiver → INFORM (responds with time)")
    print("\nThey will talk for 20 seconds...")
    print("=" * 50)
    
    # Letting the them communicate for 20 seconds
    try:
        await asyncio.sleep(20)
    except KeyboardInterrupt:
        print("\nStopping early...")
    
   
    print("\nStopping agents...")
    await sender.stop()
    await receiver.stop()
    print("Demo complete!")

if __name__ == "__main__":
    spade.run(main())