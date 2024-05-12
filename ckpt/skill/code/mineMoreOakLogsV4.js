async function mineMoreOakLogs(bot) {
  let oakLogsCount = bot.inventory.count(mcData.itemsByName["oak_log"].id);
  while (oakLogsCount < 18) {
    const direction = new Vec3(Math.floor(Math.random() * 3) - 1, 0, Math.floor(Math.random() * 3) - 1);
    let oakTreeBlock;
    oakTreeBlock = await exploreUntil(bot, direction, 60, () => {
      return bot.findBlock({
        matching: block => block.name === "oak_log",
        maxDistance: 32
      });
    });
    if (oakTreeBlock) {
      bot.chat("Oak tree found. Mining...");
      await mineBlock(bot, "oak_log", 1);
      oakLogsCount++;
      bot.chat(`Mined ${oakLogsCount} oak logs.`);
    } else {
      bot.chat("Could not find an oak tree within range.");
    }
  }
}