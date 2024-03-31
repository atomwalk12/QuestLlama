async function mineTenCobblestone(bot) {
  // Equip the wooden pickaxe
  const woodenPickaxe = bot.inventory.findInventoryItem(mcData.itemsByName["wooden_pickaxe"].id);
  await bot.equip(woodenPickaxe, "hand");

  // Mine 10 cobblestone
  await mineBlock(bot, "stone", 10);
  bot.chat("10 cobblestone mined.");
}