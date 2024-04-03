/**
 * This bot example show how to direct a bot to collect a specific block type
 * or a group of nearby blocks of that type.
 */

const mineflayer = require('mineflayer')
const collectBlock = require('./mineflayer-collectblock').plugin


bot = mineflayer.createBot({
    host: "localhost", // minecraft server ip
    port: 43571, // minecraft server port
    username: "bot",
    disableChatSigning: true,
    checkTimeoutInterval: 60 * 60 * 1000,
});

bot.loadPlugin(collectBlock)

// Listen for when a player says "collect [something]" in chat
bot.on('chat', async (username, message) => {
    const args = message.split(' ')
    if (args[0] !== 'collect') return
  
    // Get the correct block type
    const blockType = bot.registry.blocksByName[args[1]]
    if (!blockType) {
      bot.chat("I don't know any blocks with that name.")
      return
    }
  
    bot.chat('Collecting the nearest ' + blockType.name)
  
    // Try and find that block type in the world
    const block = bot.findBlock({
      matching: blockType.id,
      maxDistance: 120
    })
  
    if (!block) {
      bot.chat("I don't see that block nearby.")
      return
    }
  
    // Collect the block if we found one
    await bot.collectBlock.collect(block);
    bot.chat('Done.')
    bot.chat('My inventory is:')
    sayItems()
  })



function sayItems (items = bot.inventory.items()) {
const output = items.map(itemToString).join(', ')
if (output) {
    bot.chat(output)
} else {
    bot.chat('empty')
}
}

function itemToString (item) {
    if (item) {
    return `${item.name} x ${item.count}`
    } else {
    return '(nothing)'
    }
}