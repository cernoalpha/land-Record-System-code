// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LandRegistry {
    struct Record {
        string name;
        uint256 age;
        string landHistory;
        uint256 timestamp;
        address owner;
    }

    mapping(uint256 => Record) public records;
    uint256 public recordCount;

    event RecordAdded(uint256 uid, string name, uint256 age, string landHistory, uint256 timestamp, address owner);
    event RecordRemoved(uint256 uid);

    function addRecord(uint256 uid, string memory name, uint256 age, string memory landHistory) public {
        require(records[uid].timestamp == 0, "Record already exists");

        records[uid] = Record({
            name: name,
            age: age,
            landHistory: landHistory,
            timestamp: block.timestamp,
            owner: msg.sender
        });

        recordCount++;

        emit RecordAdded(uid, name, age, landHistory, block.timestamp, msg.sender);
    }

    function removeRecord(uint256 uid) public {
        require(records[uid].timestamp != 0, "Record does not exist");
        require(records[uid].owner == msg.sender, "Only the owner can remove this record");

        delete records[uid];
        recordCount--;

        emit RecordRemoved(uid);
    }

    function getRecord(uint256 uid) public view returns (string memory name, uint256 age, string memory landHistory, uint256 timestamp, address owner) {
        require(records[uid].timestamp != 0, "Record does not exist");

        Record memory record = records[uid];
        return (record.name, record.age, record.landHistory, record.timestamp, record.owner);
    }
}
