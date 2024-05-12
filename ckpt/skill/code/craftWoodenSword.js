async function craftWoodenSword(bot) {
  let stickCount = bot.inventory.count(mcData.itemsByName.stick.id);
  let woodPlankCount = bot.inventory.count(mcData.itemsByName.oak_planks.id);
  while (stickCount < 2 || woodPlankCount < 3) {
    if (stickCount < 2) {
      await mineBlock(bot, "oak_log", 1);
      await craftItem(bot, "stick", 1);
      stickCount++;
      bot.chat(`Crafted ${stickCount} sticks.`);
    }
    if (woodPlankCount < 3) {
      await mineBlock(bot, "oak_log", 1);
      await craftItem(bot, "oak_planks", 1);
      woodPlankCount++;
      bot.chat(`Crafted ${woodPlankCount} oak planks.`);
    }
  }
  let craftingTableCount = bot.inventory.count(mcData.itemsByName.crafting_table.id);
  if (craftingTableCount < 1) {
    await craftItem(bot, "crafting_table", 1);
    bot.chat("Crafted a crafting table.");
  }
  const craftingTablePosition = bot.entity.position.offset(1, 0, 0);
  await placeItem(bot, "crafting_table", craftingTablePosition);
  await craftItem(bot, "wooden_sword", 1);
  bot.chat("Wooden sword crafted.");
}