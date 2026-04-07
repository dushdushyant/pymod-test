#!/usr/bin/env python3
"""
Simple Test Modbus TCP Server - pymodbus v3.x compatible
"""

import struct
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext


def create_simple_server():
    """Create a simple test server with basic values"""
    
    # Create register values
    register_values = [0] * 100
    
    # Set some test values
    register_values[0] = 2305   # Voltage: 230.5V
    register_values[26] = 4321  # Your requested address 0x1A
    
    # Create holding register block
    hr = ModbusSequentialDataBlock(0, register_values)
    
    # Create server context
    store = {"hr": hr}
    context = ModbusServerContext(store, single=True)
    
    return context


def main():
    print("Starting Simple Modbus TCP Server...")
    print("Host: localhost")
    print("Port: 5020")
    print("Test Values:")
    print("  Address 0: 2305 (Voltage)")
    print("  Address 26: 4321 (Your test address)")
    print("\nPress Ctrl+C to stop")
    
    try:
        context = create_simple_server()
        StartTcpServer(context, address=("localhost", 5020))
    except KeyboardInterrupt:
        print("\nServer stopped")


if __name__ == "__main__":
    main()
