async function craftWoodenPickaxe(bot) {
  // Check if we have enough oak planks (3) and sticks (2)
  let oakPlankCount = bot.inventory.count(mcData.itemsByName.oak_planks.id);
  let stickCount = bot.inventory.count(mcData.itemsByName.stick.id);
  while (oakPlankCount < 3 || stickCount < 2) {
    if (oakPlankCount < 3) {
      await mineBlock(bot, "oak_log", 1);
      oakPlankCount++;
      bot.chat(`Mined ${oakPlankCount} oak logs.`);
    }
    if (stickCount < 2) {
      await mineBlock(bot, "stick", 1);
      stickCount++;
      bot.chat(`Mined ${stickCount} sticks.`);
    }
  }

  // Craft a crafting table if we don't already have one
  let craftingTableCount = bot.inventory.count(mcData.itemsByName.crafting_table.id);
  if (craftingTableCount < 1) {
    await craftItem(bot, "crafting_table", 1);
    bot.chat("Crafted a crafting table.");
  }

  // Place the crafting table near the player
  const craftingTablePosition = bot.entity.position.offset(1, 0, 0);
  await placeItem(bot, "crafting_table", craftingTablePosition);

  // Open the crafting table and arrange the oak planks and sticks to craft a wooden pickaxe
  await craftItem(bot, "wooden_pickaxe", 1);
  bot.chat("Wooden pickaxe crafted.");
}