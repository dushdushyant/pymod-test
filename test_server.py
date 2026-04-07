#!/usr/bin/env python3
"""
Test Modbus TCP Server for testing the modbus_client.py script
Simulates a power meter with various data types and values
"""

import time
import struct
import threading
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusServerContext


class TestModbusServer:
    def __init__(self, host='localhost', port=5020):
        """
        Initialize test Modbus TCP server
        
        Args:
            host: Server host (default: localhost)
            port: Server port (default: 5020)
        """
        self.host = host
        self.port = port
        self.server = None
        self.running = False
        
    def setup_registers(self):
        """Setup test register values simulating a power meter"""
        
        # Create register blocks with initial values
        register_values = [0] * 100
        
        # 16-bit values
        register_values[0] = 2305      # Voltage L-N: 230.5V (scale 0.1)
        register_values[1] = 4000      # Voltage L-L: 400.0V (scale 0.1)
        register_values[3] = 1234      # Current L1: 1.234A (scale 0.001)
        register_values[4] = 1567      # Current L2: 1.567A (scale 0.001)
        register_values[5] = 1890      # Current L3: 1.890A (scale 0.001)
        register_values[40] = 99       # Power Factor: 0.99 (scale 0.01)
        register_values[50] = 500      # Frequency: 50.0Hz (scale 0.1)
        
        # 32-bit values (stored as two 16-bit registers)
        # Power Total: 1234.56W (FLOAT)
        power_float = struct.pack('>f', 1234.56)
        power_high = struct.unpack('>H', power_float[0:2])[0]
        power_low = struct.unpack('>H', power_float[2:4])[0]
        register_values[20] = power_high
        register_values[21] = power_low
        
        # Energy Total: 5678.9kWh (FLOAT)
        energy_float = struct.pack('>f', 5678.9)
        energy_high = struct.unpack('>H', energy_float[0:2])[0]
        energy_low = struct.unpack('>H', energy_float[2:4])[0]
        register_values[30] = energy_high
        register_values[31] = energy_low
        
        # Test values for reverse word order
        # Register 60-61: Float with reverse word order test
        test_float = struct.pack('<f', 987.65)  # Little-endian
        test_high = struct.unpack('>H', test_float[0:2])[0]
        test_low = struct.unpack('>H', test_float[2:4])[0]
        register_values[60] = test_low   # Store reversed
        register_values[61] = test_high
        
        # 32-bit integer test
        register_values[70] = 0x1234
        register_values[71] = 0x5678
        
        # Test register 0x1A (26) as requested
        register_values[26] = 4321  # Test value: 4321
        
        # Create register block with values
        hr = ModbusSequentialDataBlock(0, register_values)
        
        return {"hr": hr}
    
    def start_server(self):
        """Start the Modbus TCP server"""
        try:
            # Setup registers
            store = self.setup_registers()
            
            # Create server context - v3.x uses simple dictionary
            context = ModbusServerContext(store, single=True)
            
            print(f"Starting Modbus TCP Server on {self.host}:{self.port}")
            print("Test Register Values:")
            print("  Address 0:  Voltage L-N (230.5V)")
            print("  Address 1:  Voltage L-L (400.0V)")
            print("  Address 3:  Current L1 (1.234A)")
            print("  Address 4:  Current L2 (1.567A)")
            print("  Address 5:  Current L3 (1.890A)")
            print("  Address 20: Power Total (1234.56W - FLOAT)")
            print("  Address 26: Test Value (4321)")
            print("  Address 30: Energy Total (5678.9kWh - FLOAT)")
            print("  Address 40: Power Factor (0.99)")
            print("  Address 50: Frequency (50.0Hz)")
            print("  Address 60: Float Reverse Test (987.65)")
            print("  Address 70: 32-bit Integer (0x12345678)")
            print("\nPress Ctrl+C to stop the server")
            
            self.running = True
            # Start server with new API
            StartTcpServer(context, address=(self.host, self.port))
            
        except KeyboardInterrupt:
            print("\nServer stopped by user")
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.stop_server()
    
    def stop_server(self):
        """Stop the Modbus TCP server"""
        print("Server stopped")
        self.running = False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Modbus TCP Server")
    parser.add_argument("--host", default="localhost", help="Server host (default: localhost)")
    parser.add_argument("--port", type=int, default=5020, help="Server port (default: 5020)")
    
    args = parser.parse_args()
    
    server = TestModbusServer(args.host, args.port)
    server.start_server()


if __name__ == "__main__":
    main()
