async function craftOakPlanks(bot) {
  // Place a crafting table near the bot
  await placeItem(bot, "crafting_table", bot.entity.position.offset(1, 0, 0));
  let oakLogCount = bot.inventory.count(mcData.itemsByName.oak_log.id);
  while (oakLogCount < 1) {
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
      oakLogCount++;
      bot.chat(`Mined ${oakLogCount} oak logs.`);
    } else {
      bot.chat("Could not find an oak tree within range.");
    }
  }
  await craftItem(bot, "oak_planks", 4);
  bot.chat("Crafted 4 oak planks.");
}