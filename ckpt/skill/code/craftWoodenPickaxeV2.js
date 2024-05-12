async function craftWoodenPickaxe(bot) {
  let oakPlankCount = bot.inventory.count(mcData.itemsByName.oak_planks.id);
  let stickCount = bot.inventory.count(mcData.itemsByName.stick.id);
  while (oakPlankCount < 3 || stickCount < 2) {
    if (oakPlankCount < 3) {
      await mineBlock(bot, "oak_log", 1);
      oakPlankCount++;
      bot.chat(`Mined ${oakPlankCount} oak logs.`);
      while (oakPlankCount < 3) {
        await craftItem(bot, "oak_planks", 1);
        oakPlankCount++;
        bot.chat(`Crafted ${oakPlankCount} oak planks.`);
      }
    }
    if (stickCount < 2) {
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
  await craftItem(bot, "wooden_pickaxe", 1);
  bot.chat("Wooden pickaxe crafted.");
}