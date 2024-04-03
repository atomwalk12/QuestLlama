// Create your bot
const mineflayer = require("mineflayer");
bot = mineflayer.createBot({
    host: "localhost", // minecraft server ip
    port: 43571, // minecraft server port
    username: "bot",
    disableChatSigning: true,
    checkTimeoutInterval: 60 * 60 * 1000,
});
let mcData

// Load collect block
bot.loadPlugin(require('mineflayer-collectblock').plugin)

async function collectGrass() {
  // Find a nearby grass block
  const grass = bot.findBlock({
    matching: mcData.blocksByName.grass_block.id,
    maxDistance: 64
  })

  if (grass) {
    // If we found one, collect it.
    try {
      await bot.collectBlock.collect(grass)
      printInventory()
      collectGrass() // Collect another grass block
    } catch (err) {
      console.log(err) // Handle errors, if any
    }
  }
}

function printInventory() {
    bot.inventory.items().forEach(item => {
      console.log(`${item.name} x ${item.count}`);
    });
  }

// On spawn, start collecting all nearby grass
bot.once('spawn', () => {
  mcData = require('minecraft-data')(bot.version)
  collectGrass()
})