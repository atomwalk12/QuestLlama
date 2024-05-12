async function mineWoodLogs(bot) {
  let axeCount = bot.inventory.count(mcData.itemsByName.wooden_axe.id);
  if (axeCount < 1) {
    await craftItem(bot, "wooden_axe", 1);
    bot.chat("Crafted a wooden axe.");
  }
  let woodLogCount = bot.inventory.count(mcData.itemsByName.oak_log.id);
  while (woodLogCount < 25) {
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
      woodLogCount++;
      bot.chat(`Mined ${woodLogCount} oak logs.`);
    } else {
      bot.chat("Could not find an oak tree within range.");
    }
  }
}