async function mineBirchLogs(bot) {
  let birchLogsCount = bot.inventory.count(mcData.itemsByName.birch_log.id);
  while (birchLogsCount < 2) {
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
      birchLogsCount++;
      bot.chat(`Mined ${birchLogsCount} birch logs.`);
    } else {
      bot.chat("Could not find a birch tree within range.");
    }
  }
}