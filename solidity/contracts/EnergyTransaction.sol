// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EnergyTrading {
    struct User {
        bool isProsumer;
        uint256 energyBalance;
    }

    mapping(address => User) public users;

    event EnergyListed(address indexed prosumer, uint256 amount);
    event EnergyBought(address indexed buyer, address indexed seller, uint256 amount);

    // Register a user: prosumer or consumer
    function register(bool isProsumer) external {
        users[msg.sender] = User(isProsumer, 0);
    }

    // Prosumer adds energy to their balance (from solar generation)
    function listEnergy(uint256 amount) external {
        require(users[msg.sender].isProsumer, "Only prosumers can list energy");
        users[msg.sender].energyBalance += amount;
        emit EnergyListed(msg.sender, amount);
    }

    // Consumer buys energy from a prosumer
    function buyEnergy(address seller, uint256 amount) external {
        require(!users[msg.sender].isProsumer, "Only consumers can buy");
        require(users[seller].energyBalance >= amount, "Not enough energy to sell");

        users[seller].energyBalance -= amount;
        users[msg.sender].energyBalance += amount;

        emit EnergyBought(msg.sender, seller, amount);
    }

    // Check your energy balance
    function getBalance() external view returns (uint256) {
        return users[msg.sender].energyBalance;
    }
}
