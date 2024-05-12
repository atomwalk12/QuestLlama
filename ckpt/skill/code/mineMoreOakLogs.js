async function mineMoreOakLogs(bot) {
  let oakLogsCount = bot.inventory.count(mcData.itemsByName.oak_log.id);
  const logsNeeded = 2;
  while (oakLogsCount < logsNeeded + 5) {
    // Explore until an oak tree is found
    let oakTreeBlock;
    oakTreeBlock = await exploreUntil(bot, new Vec3(Math.floor(Math.random() * 3) - 1, 0, Math.floor(Math.random() * 3) - 1), 60, () => {
      return bot.findBlock({
        matching: block => block.name === "oak_log",
        maxDistance: 32
      });
    });
    if (oakTreeBlock) {
      // Mine the oak tree using a wooden pickaxe
      bot.chat("Oak tree found. Mining...");
      await mineBlock(bot, "oak_log", 1);
      oakLogsCount++;
      bot.chat(`Mined ${oakLogsCount} oak logs.`);
    } else {
      bot.chat("Could not find an oak tree within range.");
    }
  }
}