// Create your bot
const mineflayer = require("mineflayer");
bot = mineflayer.createBot({
    host: "localhost", // minecraft server ip
    port: 43571, // minecraft server port
    username: "bot",
    disableChatSigning: true,
    checkTimeoutInterval: 60 * 60 * 1000,
});
let mcData;

// Load collect block
bot.loadPlugin(require('mineflayer-collectblock').plugin);

async function collectGrass() {
  // Find a nearby oak log
  const oakLog = bot.findBlock({
    matching: mcData.blocksByName.oak_log.id,
    maxDistance: 64
  });

  if (oakLog) {
    // If we found one, collect it.
    try {
      await bot.collectBlock.collect(oakLog);
      console.log('Collected an oak log. Current inventory:');
      printInventory(); // Print the current inventory
      collectGrass(); // Try to collect another oak log
    } catch (err) {
      console.log(err); // Handle errors, if any
    }
  }
}

function printInventory() {
  bot.inventory.items().forEach(item => {
    console.log(`${item.name} x ${item.count}`);
  });
}

// On spawn, start collecting all nearby oak logs and print inventory
bot.once('spawn', () => {
  mcData = require('minecraft-data')(bot.version);
  collectGrass();
});