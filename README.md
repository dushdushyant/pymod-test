# Modbus TCP Client for RI-F200-C Power Meter

A Python script to connect to a TCP Modbus server and read data from the RI-F200-C powermeter. Supports various data types including FLOAT REVERSE WORD format.

## Features

- Connect to Modbus TCP servers
- Read multiple register addresses
- Support for multiple data types: INT16, UINT16, INT32, UINT32, FLOAT
- FLOAT REVERSE WORD option for 32-bit values
- Configurable scale factors
- Multiple parameter reading in single command
- Comprehensive error handling

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Read a single 16-bit unsigned integer
python modbus_client.py 192.168.1.100 0 UINT16

# Read a 32-bit float with reverse word order
python modbus_client.py 192.168.1.100 1 FLOAT --reverse-words

# Read with scale factor
python modbus_client.py 192.168.1.100 2 UINT32 --scale 0.001
```

### Advanced Usage

```bash
# Read multiple parameters at once
python modbus_client.py 192.168.1.100 0,1,2 UINT16,UINT16,FLOAT --scale 1,1,0.001

# Specify different port and unit ID
python modbus_client.py 192.168.1.100 0 UINT16 --port 502 --unit-id 1

# Set timeout
python modbus_client.py 192.168.1.100 0 UINT16 --timeout 10.0
```
```
# Read as 16-bit unsigned integer (default)
python modbus_client.py 192.168.1.100 26 UINT16

# Read as 32-bit float with reverse word order
python modbus_client.py 192.168.1.100 26 FLOAT --reverse-words

# Read with scale factor
python modbus_client.py 192.168.1.100 26 UINT16 --scale 0.1
```

## Command Line Arguments

- `hostname`: Modbus server hostname or IP address (required)
- `address`: Register address(es) - comma-separated for multiple (required)
- `datatype`: Data type(s) - comma-separated for multiple (required)
  - Supported: INT16, UINT16, INT32, UINT32, FLOAT
- `--port`: Modbus TCP port (default: 502)
- `--unit-id`: Slave unit ID (default: 1)
- `--reverse-words`: Reverse word order for 32-bit values (FLOAT REVERSE WORD)
- `--scale`: Scale factor(s) - comma separated for multiple values
- `--timeout`: Connection timeout in seconds (default: 5.0)

## Common RI-F200-C Register Examples

**Note:** Verify these addresses with your device manual, as they may vary by firmware version.

| Parameter | Register | Data Type | Scale Factor | Description |
|-----------|----------|-----------|--------------|-------------|
| Voltage L-N | 0 | UINT16 | 0.1 | Line-to-Neutral Voltage |
| Voltage L-L | 1 | UINT16 | 0.1 | Line-to-Line Voltage |
| Current L1 | 3 | UINT16 | 0.001 | Phase 1 Current |
| Current L2 | 4 | UINT16 | 0.001 | Phase 2 Current |
| Current L3 | 5 | UINT16 | 0.001 | Phase 3 Current |
| Power Total | 20 | FLOAT | 1.0 | Total Active Power |
| Energy Total | 30 | FLOAT | 1.0 | Total Active Energy |
| Power Factor | 40 | INT16 | 0.01 | Power Factor |
| Frequency | 50 | UINT16 | 0.1 | System Frequency |

### Example Commands for RI-F200-C

```bash
# Read all three phase currents
python modbus_client.py 192.168.1.100 3,4,5 UINT16,UINT16,UINT16 --scale 0.001,0.001,0.001

# Read voltage and frequency
python modbus_client.py 192.168.1.100 0,50 UINT16,UINT16 --scale 0.1,0.1

# Read total power (may need reverse words depending on device)
python modbus_client.py 192.168.1.100 20 FLOAT --reverse-words

# Read power factor
python modbus_client.py 192.168.1.100 40 INT16 --scale 0.01
```

## Data Types

- **INT16**: Signed 16-bit integer (-32768 to 32767)
- **UINT16**: Unsigned 16-bit integer (0 to 65535)
- **INT32**: Signed 32-bit integer
- **UINT32**: Unsigned 32-bit integer
- **FLOAT**: IEEE 754 32-bit floating point

## FLOAT REVERSE WORD

Some Modbus devices store 32-bit values with reverse word order (little-endian). Use the `--reverse-words` flag for such devices.

## Error Handling

The script includes comprehensive error handling for:
- Connection failures
- Modbus communication errors
- Invalid data types
- Register read failures
- Data parsing errors

## Troubleshooting

1. **Connection Failed**: Check hostname/IP address and port
2. **Modbus Error**: Verify unit ID and register addresses
3. **Invalid Values**: Check data type and scale factor
4. **Timeout**: Increase timeout value with `--timeout`

## Dependencies

- pymodbus>=3.0.0

## License

This script is provided as-is for educational and industrial use.
