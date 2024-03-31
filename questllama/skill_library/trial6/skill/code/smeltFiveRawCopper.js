async function smeltFiveRawCopper(bot) {
  // Check if there is a furnace in the inventory
  const furnace = bot.inventory.findInventoryItem(mcData.itemsByName["furnace"].id);
  if (!furnace) {
    // Craft a furnace using cobblestone
    await craftFurnace(bot);
  }

  // Place the furnace near the player
  const furnacePosition = bot.entity.position.offset(1, 0, 0);
  await placeItem(bot, "furnace", furnacePosition);

  // Smelt 5 raw copper using coal as fuel
  await smeltItem(bot, "raw_copper", "coal", 5);
  bot.chat("5 raw copper smelted.");
}