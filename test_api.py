#!/usr/bin/env python3
"""
Test script to understand pymodbus v3.x client API
"""

from pymodbus.client import ModbusTcpClient

def test_client_api():
    """Test different ways to read registers"""
    
    client = ModbusTcpClient('localhost', port=5020)
    
    if not client.connect():
        print("Failed to connect")
        return
    
    print("Connected successfully")
    
    # Test different API calls
    try:
        print("Testing read_holding_registers(address, count)...")
        result = client.read_holding_registers(26, 1)
        print(f"Result: {result}")
        if hasattr(result, 'registers'):
            print(f"Registers: {result.registers}")
    except Exception as e:
        print(f"Error: {e}")
    
    try:
        print("\nTesting read_holding_registers(address, count, slave=1)...")
        result = client.read_holding_registers(26, 1, slave=1)
        print(f"Result: {result}")
        if hasattr(result, 'registers'):
            print(f"Registers: {result.registers}")
    except Exception as e:
        print(f"Error: {e}")
    
    try:
        print("\nTesting read_holding_registers(address, count, 1)...")
        result = client.read_holding_registers(26, 1, 1)
        print(f"Result: {result}")
        if hasattr(result, 'registers'):
            print(f"Registers: {result.registers}")
    except Exception as e:
        print(f"Error: {e}")
    
    client.close()

if __name__ == "__main__":
    test_client_api()
