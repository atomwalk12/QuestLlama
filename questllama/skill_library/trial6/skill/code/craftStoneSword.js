async function craftStoneSword(bot) {
  // Check if there is a crafting table nearby
  const craftingTable = bot.findBlock({
    matching: mcData.blocksByName["crafting_table"].id,
    maxDistance: 32
  });
  if (!craftingTable) {
    // Place the crafting table from the inventory near the player
    const tablePosition = bot.entity.position.offset(1, 0, 0);
    await placeItem(bot, "crafting_table", tablePosition);
  }

  // Check if there are enough cobblestones in the inventory
  const cobblestone = bot.inventory.findInventoryItem(mcData.itemsByName["cobblestone"].id);
  if (!cobblestone || cobblestone.count < 2) {
    // Mine more cobblestones using the stone pickaxe
    await mineBlock(bot, "stone", 2 - (cobblestone ? cobblestone.count : 0));
  }

  // Check if there are enough sticks in the inventory
  const sticks = bot.inventory.findInventoryItem(mcData.itemsByName["stick"].id);
  if (!sticks || sticks.count < 1) {
    // Craft sticks using oak planks
    await craftItem(bot, "stick", 1);
  }

  // Craft a stone sword using cobblestones and sticks
  await craftItem(bot, "stone_sword", 1);
  bot.chat("Stone sword crafted.");
}