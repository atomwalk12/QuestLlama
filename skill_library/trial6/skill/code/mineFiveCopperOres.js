async function mineFiveCopperOres(bot) {
  // Equip the stone pickaxe
  const stonePickaxe = bot.inventory.findInventoryItem(mcData.itemsByName["stone_pickaxe"].id);
  await bot.equip(stonePickaxe, "hand");

  // Mine 5 copper ores
  await mineBlock(bot, "copper_ore", 5);
  bot.chat("5 copper ores mined.");
}