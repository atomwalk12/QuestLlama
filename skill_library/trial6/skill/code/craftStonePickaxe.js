async function craftStonePickaxe(bot) {
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

  // Check if there are enough sticks in the inventory
  const sticks = bot.inventory.findInventoryItem(mcData.itemsByName["stick"].id);
  if (!sticks || sticks.count < 2) {
    // Craft sticks using oak planks
    await craftItem(bot, "stick", 1);
  }

  // Check if there are enough cobblestone in the inventory
  const cobblestone = bot.inventory.findInventoryItem(mcData.itemsByName["cobblestone"].id);
  if (!cobblestone || cobblestone.count < 3) {
    // Mine cobblestone using the wooden pickaxe
    await mineBlock(bot, "stone", 3);
  }

  // Craft a stone pickaxe using cobblestone and sticks
  await craftItem(bot, "stone_pickaxe", 1);
  bot.chat("Stone pickaxe crafted.");
}