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
});

bot.loadPlugin(collectBlock)

let mcData
bot.once('spawn', () => {
  mcData = require('minecraft-data')(bot.version)
})

bot.on('chat', async (username, message) => {
  const args = message.split(' ')
  if (args[0] !== 'collect') return

  let count = 1
  if (args.length === 3) count = parseInt(args[1])

  let type = args[1]
  if (args.length === 3) type = args[2]

  const blockType = mcData.blocksByName[type]
  if (!blockType) {
    return
  }

  const blocks = bot.findBlocks({
    matching: blockType.id,
    maxDistance: 64,
    count: count
  })

  if (blocks.length === 0) {
    bot.chat("I don't see that block nearby.")
    return
  }

  const targets = []
  for (let i = 0; i < Math.min(blocks.length, count); i++) {
    targets.push(bot.blockAt(blocks[i]))
  }

  bot.chat(`Found ${targets.length} ${type}(s)`)

  try {
    await bot.collectBlock.collect(targets)
    // All blocks have been collected.
    bot.chat('Done')
  } catch (err) {
    // An error occurred, report it.
    bot.chat(err.message)
    console.log(err)
  }
})
