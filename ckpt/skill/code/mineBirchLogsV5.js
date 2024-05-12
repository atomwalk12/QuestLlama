async function mineBirchLogs(bot) {
  let birchLogs = bot.inventory.count(mcData.itemsByName["birch_log"].id);
  let logsNeeded = 3 - birchLogs;
  if (logsNeeded > 0) {
    while (logsNeeded > 0) {
      const direction = new Vec3(Math.floor(Math.random() * 3) - 1, 0, Math.floor(Math.random() * 3) - 1);
      let birchTreeBlock;
      birchTreeBlock = await exploreUntil(bot, direction, 60, () => {
        return bot.findBlock({
          matching: block => block.name === "birch_log",
          maxDistance: 32
        });
      });
      if (birchTreeBlock) {
        bot.chat("Birch tree found. Mining...");
        await mineBlock(bot, "birch_log", 1);
        logsNeeded--;
        birchLogs++;
        bot.chat(`Mined ${birchLogs} birch logs.`);
      } else {
        bot.chat("Could not find a birch tree within range.");
      }
    }
  } else {
    bot.chat("Already have 3 birch logs in the inventory.");
  }
}