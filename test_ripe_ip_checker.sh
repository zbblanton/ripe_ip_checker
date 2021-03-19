#!/bin/sh

# Inputs: $1 = input, $2 = expected output, $3 expected exit code
run_test () {
    cmd=$(python3 ripe_ip_checker.py $1 2>&1)
    cmd_exit_code=$?
    expected_output=$2
    expected_exit_code=$3

    
    if [ "$cmd" = "$expected_output" ] && [ $cmd_exit_code -eq $expected_exit_code ]; then
        echo "Test Passed:"
    else
        echo "Test Failed:"
    fi
    echo "--------------------"
    echo "Input: $1"
    echo "Expected output: $2"
    echo "Actual output: $cmd"
    echo "Expected exit code: $3"
    echo "Actual exit code: $cmd_exit_code"
    echo "--------------------"
    echo ""
}

run_test "" "Usage python3 ripe_ip_checker.py <IP>" 1
run_test "3.0.0.2" "Found" 0 # Technically this could change if the CIDR range was removed
run_test "230.0.0.3" "Not Found" 0 # Technically this could change if the CIDR range was removed
run_test "192.168.1.3" "This IP address is for a private network" 1
run_test "127.0.0.1" "This IP address is for a private network" 1
run_test "3" "Not a Valid IPv4 address" 1
run_test "-111999" "Not a Valid IPv4 address" 1
run_test "\n3.0.0.2" "Not a Valid IPv4 address" 1
run_test "imnotanip" "Not a Valid IPv4 address" 1
run_test "3.0.0.2 1232321" "Found" 0
run_test "2001:0db8:85a3:0000:0000:8a2e:0370:7334" "Not a Valid IPv4 address" 1
