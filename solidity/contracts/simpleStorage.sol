//SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;
contract SimpleStorage {
    // State variable to store a number
    uint256 private storedNumber;

    // Function to set the stored number
    function setNumber(uint256 _number) public {
        storedNumber = _number;
    }

    // Function to get the stored number
    function getNumber() public view returns (uint256) {
        return storedNumber;
    }
}