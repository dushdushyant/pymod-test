# Test Modbus TCP Server

A test server for validating the modbus_client.py script with simulated power meter data.

## Usage

### Start the Test Server
```bash
python test_server.py
```

### Start Server on Different Port
```bash
python test_server.py --port 5020
```

### Test Commands

Once the server is running, test these commands:

#### Basic 16-bit reads
```bash
# Read voltage (address 0)
python modbus_client.py localhost 0 UINT16 --scale 0.1

# Read current (address 3)
python modbus_client.py localhost 3 UINT16 --scale 0.001

# Read your requested address 0x1A (26)
python modbus_client.py localhost 26 UINT16
```

#### 32-bit float reads
```bash
# Read power (address 20) - normal word order
python modbus_client.py localhost 20 FLOAT

# Read energy (address 30) - normal word order
python modbus_client.py localhost 30 FLOAT

# Read reverse word test (address 60) - needs reverse flag
python modbus_client.py localhost 60 FLOAT --reverse-words
```

#### Multiple reads
```bash
# Read all three currents
python modbus_client.py localhost 3,4,5 UINT16,UINT16,UINT16 --scale 0.001,0.001,0.001

# Read voltage and frequency
python modbus_client.py localhost 0,50 UINT16,UINT16 --scale 0.1,0.1
```

#### 32-bit integer test
```bash
# Read 32-bit integer (address 70)
python modbus_client.py localhost 70 UINT32
```

## Expected Results

| Address | Command | Expected Result |
|---------|---------|-----------------|
| 0 | `python modbus_client.py localhost 0 UINT16 --scale 0.1` | 230.5 |
| 1 | `python modbus_client.py localhost 1 UINT16 --scale 0.1` | 400.0 |
| 3 | `python modbus_client.py localhost 3 UINT16 --scale 0.001` | 1.234 |
| 26 | `python modbus_client.py localhost 26 UINT16` | 4321 |
| 20 | `python modbus_client.py localhost 20 FLOAT` | 1234.56 |
| 30 | `python modbus_client.py localhost 30 FLOAT` | 5678.9 |
| 40 | `python modbus_client.py localhost 40 INT16 --scale 0.01` | 0.99 |
| 50 | `python modbus_client.py localhost 50 UINT16 --scale 0.1` | 50.0 |
| 60 | `python modbus_client.py localhost 60 FLOAT --reverse-words` | 987.65 |
| 70 | `python modbus_client.py localhost 70 UINT32` | 305419896 |

## Alternative Test Options

### Online Simulators
- **Modbus TCP Server Simulator** - Various online tools available
- **ModbusPal** - Java-based Modbus simulator
- **Simply Modbus TCP Client/Server** - Windows application

### Docker Options
```bash
# Using Docker Modbus server
docker run -p 5020:5020 oitc/modbus-server
```

### Python Libraries
- **pymodbus** (already used)
- **minimalmodbus** - Alternative Modbus library

## Troubleshooting

1. **Port in use**: Change port with `--port 5021`
2. **Connection refused**: Ensure server is running first
3. **Wrong results**: Check data type and scale factor
4. **Float issues**: Try with/without `--reverse-words`

## Server Details

- **Host**: localhost (127.0.0.1)
- **Port**: 5020 (default)
- **Unit ID**: 1
- **Register Range**: 0-99
- **Data Types**: Mixed UINT16, INT16, UINT32, FLOAT
