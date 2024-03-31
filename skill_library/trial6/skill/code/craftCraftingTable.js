async function craftCraftingTable(bot) {
  // Check if there is a crafting table in the inventory
  const craftingTable = bot.inventory.findInventoryItem(mcData.itemsByName["crafting_table"].id);
  if (craftingTable) {
    bot.chat("Crafting table already in inventory.");
    return;
  }

  // Check if there are enough oak planks in the inventory
  const oakPlanks = bot.inventory.findInventoryItem(mcData.itemsByName["oak_planks"].id);
  if (!oakPlanks || oakPlanks.count < 4) {
    // Mine oak logs and craft oak planks
    bot.chat("Mining oak logs to craft oak planks...");
    await mineBlock(bot, "oak_log", 1);
    bot.chat("Crafting oak planks...");
    await craftItem(bot, "oak_planks", 1);
  }

  // Craft a crafting table using oak planks
  bot.chat("Crafting crafting table...");
  await craftItem(bot, "crafting_table", 1);
  bot.chat("Crafting table crafted.");
}