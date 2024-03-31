async function craftLightningRod(bot) {
  // Check if there are enough copper ingots and sticks in the inventory
  let copperIngots = bot.inventory.findInventoryItem(mcData.itemsByName["copper_ingot"].id);
  let sticks = bot.inventory.findInventoryItem(mcData.itemsByName["stick"].id);

  // If not, get the required items from the chest
  if (!copperIngots || copperIngots.count < 3 || !sticks || sticks.count < 2) {
    const chestPosition = new Vec3(-17, 1, 17);
    await getItemFromChest(bot, chestPosition, {
      "copper_ingot": 3 - (copperIngots ? copperIngots.count : 0),
      "stick": 2 - (sticks ? sticks.count : 0)
    });
    copperIngots = bot.inventory.findInventoryItem(mcData.itemsByName["copper_ingot"].id);
    sticks = bot.inventory.findInventoryItem(mcData.itemsByName["stick"].id);
  }

  // Check if there is a crafting table nearby or in the inventory
  let craftingTable = bot.inventory.findInventoryItem(mcData.itemsByName["crafting_table"].id);
  if (!craftingTable) {
    craftingTable = bot.findBlock({
      matching: mcData.blocksByName["crafting_table"].id,
      maxDistance: 32
    });
    if (!craftingTable) {
      // Craft a crafting table using oak planks
      await craftItem(bot, "crafting_table", 1);
    }
  }

  // Place the crafting table near the player if it's not already placed
  const tablePosition = bot.entity.position.offset(1, 0, 0);
  const tableBlock = bot.blockAt(tablePosition);
  if (!tableBlock || tableBlock.name !== "crafting_table") {
    await placeItem(bot, "crafting_table", tablePosition);
  }

  // Craft a lightning rod using the crafting table, 3 copper ingots, and 2 sticks
  await craftItem(bot, "lightning_rod", 1);
  bot.chat("Lightning rod crafted.");
}