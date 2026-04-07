package main

import (
	"encoding/binary"
	"fmt"
	"math"
)

// ReadFloatReverseWord reads a 32-bit float from two 16-bit registers with reverse word order
func ReadFloatReverseWord(register0, register1 uint16) float32 {
	// Reverse word order (little-endian)
	// register0 = low word, register1 = high word
	combined := (uint32(register1) << 16) | uint32(register0)
	
	// Convert 32-bit to IEEE 754 float
	bits := make([]byte, 4)
	binary.BigEndian.PutUint32(bits, combined)
	return math.Float32frombits(binary.BigEndian.Uint32(bits))
}

// ReadFloatNormalWord reads a 32-bit float from two 16-bit registers with normal word order
func ReadFloatNormalWord(register0, register1 uint16) float32 {
	// Normal word order (big-endian)
	// register0 = high word, register1 = low word
	combined := (uint32(register0) << 16) | uint32(register1)
	
	// Convert 32-bit to IEEE 754 float
	bits := make([]byte, 4)
	binary.BigEndian.PutUint32(bits, combined)
	return math.Float32frombits(binary.BigEndian.Uint32(bits))
}

// Alternative implementation using byte slices (more efficient)
func ReadFloatReverseWordBytes(register0, register1 uint16) float32 {
	// Create 4-byte slice in reverse order
	bytes := []byte{
		byte(register1 >> 8), byte(register1),      // High word bytes
		byte(register0 >> 8), byte(register0),      // Low word bytes
	}
	
	// Convert bytes to float32
	bits := binary.BigEndian.Uint32(bytes)
	return math.Float32frombits(bits)
}

// Alternative implementation using byte slices for normal word order
func ReadFloatNormalWordBytes(register0, register1 uint16) float32 {
	// Create 4-byte slice in normal order
	bytes := []byte{
		byte(register0 >> 8), byte(register0),      // High word bytes
		byte(register1 >> 8), byte(register1),      // Low word bytes
	}
	
	// Convert bytes to float32
	bits := binary.BigEndian.Uint32(bytes)
	return math.Float32frombits(bits)
}

// ModbusFloatReader handles Modbus float reading with word order options
type ModbusFloatReader struct {
	reverseWords bool
}

func (r *ModbusFloatReader) ReadFloat(registers []uint16) float32 {
	if len(registers) < 2 {
		return 0
	}
	
	if r.reverseWords {
		return ReadFloatReverseWord(registers[0], registers[1])
	}
	return ReadFloatNormalWord(registers[0], registers[1])
}

func main() {
	// Example usage
	register0 := uint16(0x1234)  // Low word in reverse order
	register1 := uint16(0x5678)  // High word in reverse order
	
	fmt.Println("=== Go Modbus Float Reading Example ===")
	fmt.Printf("Input registers: 0x%04X, 0x%04X\n", register0, register1)
	
	// Test reverse word reading
	reverseValue := ReadFloatReverseWord(register0, register1)
	fmt.Printf("Reverse word float: %f\n", reverseValue)
	
	// Test normal word reading
	normalValue := ReadFloatNormalWord(register0, register1)
	fmt.Printf("Normal word float: %f\n", normalValue)
	
	// Test using byte slice methods
	reverseBytesValue := ReadFloatReverseWordBytes(register0, register1)
	fmt.Printf("Reverse word (bytes): %f\n", reverseBytesValue)
	
	normalBytesValue := ReadFloatNormalWordBytes(register0, register1)
	fmt.Printf("Normal word (bytes): %f\n", normalBytesValue)
	
	// Test with ModbusFloatReader
	fmt.Println("\n=== Using ModbusFloatReader ===")
	
	// Normal word order
	readerNormal := &ModbusFloatReader{reverseWords: false}
	normalReaderValue := readerNormal.ReadFloat([]uint16{register0, register1})
	fmt.Printf("Reader (normal): %f\n", normalReaderValue)
	
	// Reverse word order
	readerReverse := &ModbusFloatReader{reverseWords: true}
	reverseReaderValue := readerReverse.ReadFloat([]uint16{register0, register1})
	fmt.Printf("Reader (reverse): %f\n", reverseReaderValue)
	
	// Test with actual float values
	fmt.Println("\n=== Testing with Known Float Values ===")
	
	// Test value: 1234.56
	testFloat := float32(1234.56)
	testBits := math.Float32bits(testFloat)
	testHigh := uint16(testBits >> 16)
	testLow := uint16(testBits & 0xFFFF)
	
	fmt.Printf("Test float: %f\n", testFloat)
	fmt.Printf("Test bits: 0x%08X\n", testBits)
	fmt.Printf("Test registers: High=0x%04X, Low=0x%04X\n", testHigh, testLow)
	
	// Read back using normal word order
	readBack := ReadFloatNormalWord(testHigh, testLow)
	fmt.Printf("Read back (normal): %f\n", readBack)
	
	// Read back using reverse word order (should give different result)
	readBackReverse := ReadFloatReverseWord(testLow, testHigh)
	fmt.Printf("Read back (reverse): %f\n", readBackReverse)
}
