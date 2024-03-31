async function craftShield(bot) {
  // Check if there are enough oak planks and iron ingots in the inventory
  let oakPlanks = bot.inventory.findInventoryItem(mcData.itemsByName["oak_planks"].id);
  let ironIngots = bot.inventory.findInventoryItem(mcData.itemsByName["iron_ingot"].id);

  // If not, get the required items from the chest
  if (!oakPlanks || oakPlanks.count < 6 || !ironIngots || ironIngots.count < 1) {
    const chestPosition = new Vec3(-17, 1, 17);
    await getItemFromChest(bot, chestPosition, {
      "oak_planks": 6 - (oakPlanks ? oakPlanks.count : 0),
      "iron_ingot": 1 - (ironIngots ? ironIngots.count : 0)
    });
    oakPlanks = bot.inventory.findInventoryItem(mcData.itemsByName["oak_planks"].id);
    ironIngots = bot.inventory.findInventoryItem(mcData.itemsByName["iron_ingot"].id);
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

  // Craft a shield using the crafting table, 6 oak planks, and 1 iron ingot
  await craftItem(bot, "shield", 1);
  bot.chat("Shield crafted.");
}