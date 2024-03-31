async function craftIronChestplate(bot) {
  // Check if there is a crafting table in the inventory or nearby
  let craftingTable = bot.inventory.findInventoryItem(mcData.itemsByName["crafting_table"].id);
  if (!craftingTable) {
    craftingTable = bot.findBlock({
      matching: mcData.blocksByName["crafting_table"].id,
      maxDistance: 32
    });
    if (!craftingTable) {
      // Mine oak logs and craft oak planks
      await mineBlock(bot, "oak_log", 1);
      await craftItem(bot, "oak_planks", 2);
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

  // Check if there are enough iron ingots in the inventory
  let ironIngots = bot.inventory.findInventoryItem(mcData.itemsByName["iron_ingot"].id);
  if (!ironIngots || ironIngots.count < 8) {
    // Mine iron ores and smelt them using a furnace
    await mineBlock(bot, "iron_ore", 8 - (ironIngots ? ironIngots.count : 0));
    await smeltItem(bot, "raw_iron", "coal", 8 - (ironIngots ? ironIngots.count : 0));
    ironIngots = bot.inventory.findInventoryItem(mcData.itemsByName["iron_ingot"].id);
  }

  // Craft an iron chestplate using the crafting table and 8 iron ingots
  await craftItem(bot, "iron_chestplate", 1);
  bot.chat("Iron chestplate crafted.");
}