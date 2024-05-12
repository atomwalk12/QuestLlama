async function craftCraftingTable(bot) {
  const oakPlankCount = bot.inventory.count(mcData.itemsByName.oak_planks.id);
  if (oakPlankCount < 3) {
    let oakLogCount = bot.inventory.count(mcData.itemsByName.oak_log.id);
    while (oakLogCount < 1) {
      await mineBlock(bot, "oak_log", 1);
      oakLogCount++;
      bot.chat(`Mined ${oakLogCount} oak logs.`);
    }
    while (oakPlankCount < 3) {
      await craftItem(bot, "oak_planks", 1);
      oakPlankCount++;
      bot.chat(`Crafted ${oakPlankCount} oak planks.`);
    }
  }
  await craftItem(bot, "crafting_table", 1);
  bot.chat("Crafted a crafting table.");
}