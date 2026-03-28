require("@nomiclabs/hardhat-ethers");
async function main() {
  const [deployer] = await ethers.getSigners();

  console.log("Deploying with account:", deployer.address);

  const Logger = await ethers.getContractFactory("TransactionLogger");
  const logger = await Logger.deploy();

  await logger.deployed();

  console.log("Contract deployed at:", logger.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });