async function craftFurnace(bot) {
  // Check if there are enough cobblestones in the inventory
  const cobblestone = bot.inventory.findInventoryItem(mcData.itemsByName["cobblestone"].id);
  if (!cobblestone || cobblestone.count < 8) {
    // Mine more cobblestones using the stone pickaxe
    await mineBlock(bot, "stone", 8 - (cobblestone ? cobblestone.count : 0));
  }

  // Place the crafting table near the player
  const tablePosition = bot.entity.position.offset(1, 0, 0);
  await placeItem(bot, "crafting_table", tablePosition);

  // Craft a furnace using the cobblestones
  await craftItem(bot, "furnace", 1);
  bot.chat("Furnace crafted.");
}