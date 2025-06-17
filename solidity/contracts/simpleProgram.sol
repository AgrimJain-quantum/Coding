// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.18 < 0.9.0; // stating the version of the compiler

contract  SimpleStorage {
    // basic types : boolean, uint , int, address, bytes
    // bool hasFavoriteNumber = false;
    // uint256 favoriteNumber = 88;
    // int number = -99;
    // string favoriteNumberText = "77";
    // int256 favoriteItem = -100;
    // address myAddress = 0x723CF559702e8bfBcc8a2E9De051634Faf78EB2F;
    // bytes32 favorite = "cat";
    // bytes25 name = "Jonathan";
    // string surname = "Smith";
    // uint256 favoriteNumber2 = 99;
    // // array
    // uint256[] favoriteNumbers = [1, 2, 3, 4];
    uint256 favoriteNumber;
    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }
    
}
