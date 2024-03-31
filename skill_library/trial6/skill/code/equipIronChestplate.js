async function equipIronChestplate(bot) {
  // Find the iron chestplate in the bot's inventory
  const ironChestplate = bot.inventory.findInventoryItem(mcData.itemsByName["iron_chestplate"].id);

  // Equip the iron chestplate in the "torso" slot
  if (ironChestplate) {
    await bot.equip(ironChestplate, "torso");
    bot.chat("Iron chestplate equipped.");
  } else {
    bot.chat("No iron chestplate found in inventory.");
  }
}