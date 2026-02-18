import asyncio
import datetime
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class SenderAgent(Agent):
    """
    Simple agent that sends REQUEST messages
    """
    class SendRequest(CyclicBehaviour):
        async def run(self):
            # Create a FIPA-ACL REQUEST message
            msg = Message(to="receiver@localhost")
            msg.set_metadata("performative", "request")  # FIPA-ACL performative
            msg.body = "What time is it?"
            
            print(f"\n[SENDER] Sending REQUEST: '{msg.body}'")
            await self.send(msg)
            
            # Wait for response
            response = await self.receive(timeout=10)
            if response:
                print(f"[SENDER] Received response: '{response.body}'")
            else:
                print("[SENDER] No response received")
            
            await asyncio.sleep(3)  # Wait 3 seconds before next request
    
    async def setup(self):
        print(f"[SENDER] Agent started: {self.jid}")
        self.add_behaviour(self.SendRequest())

class ReceiverAgent(Agent):
    """
    Simple agent that receives REQUEST and sends INFORM responses
    """
    class HandleRequest(CyclicBehaviour):
        async def run(self):
            # Wait for a message
            msg = await self.receive(timeout=5)
            
            if msg:
                # FIX: get_metadata() doesn't take default parameter
                performative = msg.get_metadata("performative") or ""
                
                print(f"\n[RECEIVER] Received message:")
                print(f"  From: {msg.sender}")
                print(f"  Type: {performative}")
                print(f"  Content: '{msg.body}'")
                
                # Parse the message (LAB TASK 3: Parse incoming messages)
                if performative == "request":
                    if "time" in msg.body.lower() or "what" in msg.body.lower():
                        # Trigger action: Get current time
                        current_time = datetime.datetime.now().strftime("%H:%M:%S")
                        
                        # Send INFORM response with the time
                        reply = msg.make_reply()
                        reply.set_metadata("performative", "inform")  # FIPA-ACL performative
                        reply.body = f"The current time is {current_time}"
                        
                        print(f"[RECEIVER] Sending INFORM: '{reply.body}'")
                        await self.send(reply)
    
    async def setup(self):
        print(f"[RECEIVER] Agent started: {self.jid}")
        self.add_behaviour(self.HandleRequest())