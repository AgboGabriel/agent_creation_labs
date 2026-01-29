import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

print("=" * 60)
print("LAB 1: BASIC SPADE AGENT")
print("=" * 60)

class BasicAgent(Agent):
    async def setup(self):
        print(f"Agent {self.jid} initialized")
        
        class SimpleBehavior(CyclicBehaviour):
            async def run(self):
                print(f"Agent {self.agent.jid} is active")
                await asyncio.sleep(2)
        
        self.add_behaviour(SimpleBehavior())

async def main():
    print("\nCreating agent: alice@localhost")
    print("Password: password123")
    print("XMPP Server: localhost")
    print("\nStarting agent...")
    
    agent = BasicAgent("alice@localhost", "password123")
    
    await agent.start()
    print("Agent connected successfully")
    print("Running for 10 seconds...\n")
    
    await asyncio.sleep(10)
    
    await agent.stop()
    print("\nAgent stopped")
    print("\n" + "=" * 60)
    print("LAB 1 COMPLETE")
    print("=" * 60)

asyncio.run(main())