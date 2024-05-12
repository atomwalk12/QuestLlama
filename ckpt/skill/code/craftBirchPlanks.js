async function craftBirchPlanks(bot) {
  let birchLogCount = bot.inventory.count(mcData.itemsByName.birch_log.id);
  if (birchLogCount < 1) {
    // Explore and mine a birch log
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
      birchLogCount++;
      bot.chat(`Mined ${birchLogCount} birch logs.`);
    } else {
      bot.chat("Could not find a birch tree within range.");
    }
  }

  // Craft 4 birch planks from the birch log
  let craftingTableCount = bot.inventory.count(mcData.itemsByName.crafting_table.id);
  if (craftingTableCount < 1) {
    await craftItem(bot, "crafting_table", 1);
    bot.chat("Crafted a crafting table.");
  }
  const craftingTablePosition = bot.entity.position.offset(1, 0, 0);
  await placeItem(bot, "crafting_table", craftingTablePosition);
  await craftItem(bot, "birch_planks", 4);
  bot.chat("Birch planks crafted.");
}