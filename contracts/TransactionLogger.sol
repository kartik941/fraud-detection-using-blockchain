// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TransactionLogger {

    struct Transaction {
        string userId;
        uint amount;
        string status;
        uint riskScore;
        string dataHash;
        uint timestamp;
    }

    Transaction[] public transactions;

    function logTransaction(
        string memory _userId,
        uint _amount,
        string memory _status,
        uint _riskScore,
        string memory _dataHash
    ) public {
        transactions.push(Transaction(
            _userId,
            _amount,
            _status,
            _riskScore,
            _dataHash,
            block.timestamp
        ));
    }

    function getTransaction(uint index) public view returns (
        string memory,
        uint,
        string memory,
        uint,
        uint
    ) {
        Transaction memory txn = transactions[index];
        return (
            txn.userId,
            txn.amount,
            txn.status,
            txn.riskScore,
            txn.timestamp
        );
    }

    function getCount() public view returns (uint) {
        return transactions.length;
    }
}