async function craftStoneSword(bot) {
  let cobblestoneCount = bot.inventory.count(mcData.itemsByName.cobblestone.id);
  let stickCount = bot.inventory.count(mcData.itemsByName.stick.id);
  while (cobblestoneCount < 2 || stickCount < 1) {
    if (cobblestoneCount < 2) {
      await mineBlock(bot, "cobblestone", 1);
      cobblestoneCount++;
      bot.chat(`Mined ${cobblestoneCount} cobblestones.`);
    }
    if (stickCount < 1) {
      await mineBlock(bot, "oak_log", 1);
      await craftItem(bot, "stick", 1);
      stickCount++;
      bot.chat("Crafted a stick.");
    }
  }
  let craftingTableCount = bot.inventory.count(mcData.itemsByName.crafting_table.id);
  if (craftingTableCount < 1) {
    await craftItem(bot, "crafting_table", 1);
    bot.chat("Crafted a crafting table.");
  }
  const craftingTablePosition = bot.entity.position.offset(1, 0, 0);
  await placeItem(bot, "crafting_table", craftingTablePosition);
  await craftItem(bot, "stone_sword", 1);
  bot.chat("Stone sword crafted.");
}