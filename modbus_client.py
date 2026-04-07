#!/usr/bin/env python3
"""
Modbus TCP Client for RI-F200-C Power Meter
Supports reading various data types including FLOAT REVERSE WORD format
"""

import argparse
import struct
import sys
import time
from typing import Union, List, Tuple
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException


class ModbusPowerMeterClient:
    def __init__(self, host: str, port: int = 502, unit_id: int = 1):
        """
        Initialize Modbus TCP client
        
        Args:
            host: Modbus server hostname/IP address
            port: Modbus TCP port (default: 502)
            unit_id: Slave unit ID (default: 1)
        """
        self.host = host
        self.port = port
        self.unit_id = unit_id
        self.client = None
        
    def connect(self, timeout: float = 5.0) -> bool:
        """Connect to Modbus server"""
        try:
            print(f"Attempting to connect to {self.host}:{self.port} (Unit ID: {self.unit_id}, Timeout: {timeout}s)")
            self.client = ModbusTcpClient(self.host, port=self.port, timeout=timeout)
            result = self.client.connect()
            if result:
                print(f"Successfully connected to Modbus server at {self.host}:{self.port}")
                return True
            else:
                print(f"Failed to connect to Modbus server at {self.host}:{self.port}")
                return False
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from Modbus server"""
        if self.client:
            self.client.close()
            print("Disconnected from Modbus server")
    
    def read_registers(self, address: int, count: int) -> Union[List[int], None]:
        """
        Read holding registers
        
        Args:
            address: Starting register address
            count: Number of registers to read
            
        Returns:
            List of register values or None if error
        """
        try:
            result = self.client.read_holding_registers(address=address, count=count, slave=self.unit_id)
            if result.isError():
                print(f"Error reading registers: {result}")
                return None
            return result.registers
        except ModbusException as e:
            print(f"Modbus error: {e}")
            return None
        except Exception as e:
            print(f"Error reading registers: {e}")
            return None
    
    def parse_value(self, registers: List[int], data_type: str, reverse_words: bool = False) -> Union[float, int, None]:
        """
        Parse register values based on data type
        
        Args:
            registers: List of register values
            data_type: Data type (INT16, UINT16, INT32, UINT32, FLOAT)
            reverse_words: Whether to reverse word order for 32-bit values
            
        Returns:
            Parsed value or None if error
        """
        try:
            if data_type.upper() == "INT16":
                if len(registers) < 1:
                    return None
                # Convert to signed 16-bit
                value = registers[0]
                if value > 32767:
                    value -= 65536
                return value
            
            elif data_type.upper() == "UINT16":
                if len(registers) < 1:
                    return None
                return registers[0]
            
            elif data_type.upper() in ["INT32", "UINT32", "FLOAT"]:
                if len(registers) < 2:
                    return None
                
                # Combine two 16-bit registers into 32-bit value
                if reverse_words:
                    # Reverse word order (little-endian)
                    combined = (registers[1] << 16) | registers[0]
                else:
                    # Normal word order (big-endian)
                    combined = (registers[0] << 16) | registers[1]
                
                if data_type.upper() == "UINT32":
                    return combined
                
                elif data_type.upper() == "INT32":
                    # Convert to signed 32-bit
                    if combined > 2147483647:
                        combined -= 4294967296
                    return combined
                
                elif data_type.upper() == "FLOAT":
                    # Convert to IEEE 754 float
                    bytes_data = struct.pack('>I', combined) if not reverse_words else struct.pack('<I', combined)
                    return struct.unpack('>f', bytes_data)[0]
            
            else:
                print(f"Unsupported data type: {data_type}")
                return None
                
        except Exception as e:
            print(f"Error parsing value: {e}")
            return None
    
    def read_parameter(self, address: int, data_type: str, count: int = None, 
                      reverse_words: bool = False, scale_factor: float = 1.0) -> Union[float, int, None]:
        """
        Read a single parameter from the power meter
        
        Args:
            address: Register address
            data_type: Data type (INT16, UINT16, INT32, UINT32, FLOAT)
            count: Number of registers to read (auto-calculated if None)
            reverse_words: Whether to reverse word order for 32-bit values
            scale_factor: Scale factor to apply to the result
            
        Returns:
            Parsed and scaled value or None if error
        """
        # Calculate register count based on data type
        if count is None:
            if data_type.upper() in ["INT16", "UINT16"]:
                count = 1
            elif data_type.upper() in ["INT32", "UINT32", "FLOAT"]:
                count = 2
            else:
                print(f"Unknown data type: {data_type}")
                return None
        
        # Read registers
        registers = self.read_registers(address, count)
        if registers is None:
            return None
        
        # Parse value
        value = self.parse_value(registers, data_type, reverse_words)
        if value is None:
            return None
        
        # Apply scale factor
        return value * scale_factor


def main():
    parser = argparse.ArgumentParser(
        description="Modbus TCP Client for RI-F200-C Power Meter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Read voltage (assuming register 0, UINT16 type)
  python modbus_client.py 192.168.1.100 0 UINT16
  
  # Read current as FLOAT with reverse word order
  python modbus_client.py 192.168.1.100 1 FLOAT --reverse-words
  
  # Read power with scale factor
  python modbus_client.py 192.168.1.100 2 UINT32 --scale 0.001
  
  # Read multiple parameters
  python modbus_client.py 192.168.1.100 0,1,2 UINT16,UINT16,FLOAT --scale 1,1,0.001

Common RI-F200-C Register Examples (verify with your device manual):
  Voltage L-N:     0 (UINT16, scale 0.1)
  Voltage L-L:     1 (UINT16, scale 0.1)  
  Current L1:      3 (UINT16, scale 0.001)
  Current L2:      4 (UINT16, scale 0.001)
  Current L3:      5 (UINT16, scale 0.001)
  Power Total:     20 (FLOAT, scale 1.0)
  Energy Total:    30 (FLOAT, scale 1.0)
  Power Factor:     40 (INT16, scale 0.01)
  Frequency:       50 (UINT16, scale 0.1)
        """
    )
    
    parser.add_argument("hostname", help="Modbus server hostname or IP address")
    parser.add_argument("address", help="Register address (comma-separated for multiple)")
    parser.add_argument("datatype", help="Data type (comma-separated for multiple): INT16, UINT16, INT32, UINT32, FLOAT")
    parser.add_argument("--port", type=int, default=502, help="Modbus TCP port (default: 502)")
    parser.add_argument("--unit-id", type=int, default=1, help="Slave unit ID (default: 1)")
    parser.add_argument("--reverse-words", action="store_true", help="Reverse word order for 32-bit values (FLOAT REVERSE WORD)")
    parser.add_argument("--scale", help="Scale factor(s) - comma separated for multiple values")
    parser.add_argument("--timeout", type=float, default=5.0, help="Connection timeout in seconds (default: 5.0)")
    
    args = parser.parse_args()
    
    # Parse multiple addresses and data types
    addresses = [int(addr.strip()) for addr in args.address.split(',')]
    datatypes = [dtype.strip().upper() for dtype in args.datatype.split(',')]
    
    # Parse scale factors
    scale_factors = [1.0] * len(addresses)
    if args.scale:
        scale_list = [float(s.strip()) for s in args.scale.split(',')]
        scale_factors = scale_list + [1.0] * (len(addresses) - len(scale_list))
    
    # Validate inputs
    if len(addresses) != len(datatypes):
        print("Error: Number of addresses must match number of data types")
        sys.exit(1)
    
    # Create client and connect
    client = ModbusPowerMeterClient(args.hostname, args.port, args.unit_id)
    
    if not client.connect(timeout=args.timeout):
        sys.exit(1)
    
    try:
        print(f"Reading {len(addresses)} parameter(s) from unit {args.unit_id}")
        print("-" * 60)
        
        for i, (address, datatype) in enumerate(zip(addresses, datatypes)):
            print(f"Reading address {address} ({datatype})...", end=" ")
            
            value = client.read_parameter(
                address=address,
                data_type=datatype,
                reverse_words=args.reverse_words,
                scale_factor=scale_factors[i]
            )
            
            if value is not None:
                print(f"= {value}")
            else:
                print("FAILED")
        
        print("-" * 60)
        print("Read completed successfully")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
