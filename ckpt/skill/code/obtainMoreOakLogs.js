async function obtainMoreOakLogs(bot) {
  const oakLogName = "oak_log";
  let oakLogsCount = bot.inventory.count(mcData.itemsByName[oakLogName].id);
  if (oakLogsCount >= 3) {
    bot.chat("Already have 3 oak logs in inventory.");
    return;
  }
  bot.chat(`Mining ${3 - oakLogsCount} oak logs...`);
  while (oakLogsCount < 3) {
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
      await mineBlock(bot, oakLogName, 1);
      oakLogsCount++;
      bot.chat(`Mined ${oakLogsCount} oak logs.`);
    } else {
      bot.chat("Could not find an oak tree within range.");
    }
  }
}