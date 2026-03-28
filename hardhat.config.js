require("@nomiclabs/hardhat-ethers");
require("dotenv").config();
module.exports = {
  solidity: "0.8.20",
  networks: {
    sepolia: {
      url: process.env.rpc_url,
      accounts: [process.env.pvt_key]
    }
  }
};