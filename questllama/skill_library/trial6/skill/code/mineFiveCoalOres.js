async function mineFiveCoalOres(bot) {
  // Equip the wooden pickaxe
  const woodenPickaxe = bot.inventory.findInventoryItem(mcData.itemsByName["wooden_pickaxe"].id);
  await bot.equip(woodenPickaxe, "hand");

  // Mine 5 coal ores
  await mineBlock(bot, "coal_ore", 5);
  bot.chat("5 coal ores mined.");
}